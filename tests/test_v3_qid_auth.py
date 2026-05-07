from dgb_wallet_guardian.v3 import GuardianWalletV3
from dgb_wallet_guardian.contracts.v3_hash import canonical_sha256


def _base_qid_auth_request():
    return {
        "contract_version": 3,
        "component": "guardian_wallet",
        "mode": "qid_auth",
        "request_id": "qid-r1",
        "wallet_ctx": {},
        "tx_ctx": {},
        "auth_ctx": {
            "qid_verified": True,
            "service_id": "example.com",
            "callback_url": "https://example.com/qid",
            "nonce": "abc123",
            "address": "DGB_ADDR",
            "pubkey": "PUBKEY",
            "require": "legacy",
        },
        "extra_signals": {
            "trusted_device": True,
            "session": "s1",
            "sentinel_status": "NORMAL",
        },
    }


def test_qid_auth_allow_happy_path():
    gw = GuardianWalletV3()
    req = _base_qid_auth_request()
    out = gw.evaluate(req)
    assert out["outcome"] == "allow"
    assert out["reason_codes"] == ["GW_OK_QID_AUTH_ALLOW"]
    assert out["risk"]["level"] == "NORMAL"
    assert out["meta"]["mode"] == "qid_auth"


def test_qid_auth_denies_when_unverified():
    gw = GuardianWalletV3()
    req = _base_qid_auth_request()
    req["auth_ctx"]["qid_verified"] = False
    out = gw.evaluate(req)
    assert out["outcome"] == "deny"
    assert out["reason_codes"] == ["GW_DENY_QID_UNVERIFIED"]


def test_qid_auth_denies_when_dual_proof_missing_binding():
    gw = GuardianWalletV3()
    req = _base_qid_auth_request()
    req["auth_ctx"]["require"] = "dual-proof"
    out = gw.evaluate(req)
    assert out["outcome"] == "deny"
    assert out["reason_codes"] == ["GW_DENY_QID_BINDING_REQUIRED"]


def test_qid_auth_escalates_untrusted_device():
    gw = GuardianWalletV3()
    req = _base_qid_auth_request()
    req["extra_signals"]["trusted_device"] = False
    out = gw.evaluate(req)
    assert out["outcome"] == "escalate"
    assert out["reason_codes"] == ["GW_ESCALATE_QID_UNTRUSTED_DEVICE"]


def test_qid_auth_rejects_unknown_auth_key_fail_closed():
    gw = GuardianWalletV3()
    req = _base_qid_auth_request()
    req["auth_ctx"]["unknown"] = 1
    out = gw.evaluate(req)
    assert out["outcome"] == "deny"
    assert out["reason_codes"] == ["GW_ERROR_UNKNOWN_AUTH_KEY"]


def test_qid_auth_context_hash_is_deterministic():
    gw = GuardianWalletV3()
    req = _base_qid_auth_request()
    out1 = gw.evaluate(req)
    out2 = gw.evaluate(req)
    assert out1["context_hash"] == out2["context_hash"]

    expected = canonical_sha256(
        {
            "component": gw.COMPONENT,
            "contract_version": gw.CONTRACT_VERSION,
            "mode": "qid_auth",
            "request_id": "qid-r1",
            "wallet_ctx": {},
            "tx_ctx": {},
            "auth_ctx": {
                "qid_verified": True,
                "service_id": "example.com",
                "callback_url": "https://example.com/qid",
                "nonce": "abc123",
                "address": "DGB_ADDR",
                "pubkey": "PUBKEY",
                "require": "legacy",
            },
            "extra_signals": {
                "trusted_device": True,
                "session": "s1",
                "sentinel_status": "NORMAL",
            },
            "outcome": "allow",
            "risk_level": "NORMAL",
            "reason_codes": ["GW_OK_QID_AUTH_ALLOW"],
        }
    )
    assert out1["context_hash"] == expected
