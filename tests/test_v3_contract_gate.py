import math

from dgb_wallet_guardian.v3 import GuardianWalletV3
from dgb_wallet_guardian.contracts.v3_hash import canonical_sha256


def _base_request():
    return {
        "contract_version": 3,
        "component": "guardian_wallet",
        "request_id": "r1",
        "wallet_ctx": {
            "balance": 100.0,
            "typical_amount": 1.0,
            "wallet_age_days": 10,
            "tx_count_24h": 1,
        },
        "tx_ctx": {
            "to_address": "DGB_ADDR",
            "amount": 1.0,
            "fee": 0.1,
            "memo": "x",
            "asset_id": "asset",
        },
        "extra_signals": {
            "device_fingerprint": "dfp",
            "sentinel_status": "NORMAL",
            "geo_ip": "1.2.3.4",
            "session": "s",
            "trusted_device": True,
        },
    }


def test_rejects_wrong_contract_version_fail_closed():
    gw = GuardianWalletV3()
    req = _base_request()
    req["contract_version"] = 2

    out = gw.evaluate(req)
    assert out["contract_version"] == 3
    assert out["component"] == "guardian_wallet"
    assert out["request_id"] == "r1"
    assert out["outcome"] == "deny"
    assert out["meta"]["fail_closed"] is True


def test_rejects_wrong_component_fail_closed():
    gw = GuardianWalletV3()
    req = _base_request()
    req["component"] = "not_guardian"

    out = gw.evaluate(req)
    assert out["outcome"] == "deny"
    assert out["meta"]["fail_closed"] is True


def test_rejects_oversize_payload_deterministically():
    gw = GuardianWalletV3()
    req = _base_request()
    # Make it definitely exceed 128KB
    req["tx_ctx"]["memo"] = "A" * (GuardianWalletV3.MAX_PAYLOAD_BYTES + 10)

    out = gw.evaluate(req)
    assert out["outcome"] == "deny"
    assert out["meta"]["fail_closed"] is True
    assert "GW_ERROR_OVERSIZE" in out["reason_codes"][0]


def test_rejects_unknown_nested_wallet_key():
    gw = GuardianWalletV3()
    req = _base_request()
    req["wallet_ctx"]["unknown_wallet_key"] = 1

    out = gw.evaluate(req)
    assert out["outcome"] == "deny"
    assert "GW_ERROR_UNKNOWN_WALLET_KEY" in out["reason_codes"][0]


def test_rejects_unknown_nested_tx_key():
    gw = GuardianWalletV3()
    req = _base_request()
    req["tx_ctx"]["unknown_tx_key"] = 1

    out = gw.evaluate(req)
    assert out["outcome"] == "deny"
    assert "GW_ERROR_UNKNOWN_TX_KEY" in out["reason_codes"][0]


def test_rejects_unknown_nested_signal_key():
    gw = GuardianWalletV3()
    req = _base_request()
    req["extra_signals"]["unknown_signal_key"] = 1

    out = gw.evaluate(req)
    assert out["outcome"] == "deny"
    assert "GW_ERROR_UNKNOWN_SIGNAL_KEY" in out["reason_codes"][0]


def test_rejects_nan_inf_numbers_fail_closed():
    gw = GuardianWalletV3()

    req = _base_request()
    req["tx_ctx"]["amount"] = float("nan")
    out = gw.evaluate(req)
    assert out["outcome"] == "deny"
    assert "GW_ERROR_BAD_NUMBER" in out["reason_codes"][0]

    req2 = _base_request()
    req2["wallet_ctx"]["balance"] = float("inf")
    out2 = gw.evaluate(req2)
    assert out2["outcome"] == "deny"
    assert "GW_ERROR_BAD_NUMBER" in out2["reason_codes"][0]


def test_error_context_hash_matches_contract_error_payload():
    gw = GuardianWalletV3()
    req = _base_request()
    req["contract_version"] = 999  # schema version error path

    out = gw.evaluate(req)
    reason_code = out["reason_codes"][0]

    expected = canonical_sha256(
        {
            "component": gw.COMPONENT,
            "contract_version": gw.CONTRACT_VERSION,
            "request_id": "r1",
            "reason_code": reason_code,
        }
    )
    assert out["context_hash"] == expected


def test_success_is_deterministic_for_same_input():
    gw = GuardianWalletV3()
    req = _base_request()

    out1 = gw.evaluate(req)
    out2 = gw.evaluate(req)

    # Even though v2 engine is involved, for the same input we expect stable output
    assert out1["context_hash"] == out2["context_hash"]
    assert out1["outcome"] == out2["outcome"]
    assert out1["reason_codes"] == out2["reason_codes"]
