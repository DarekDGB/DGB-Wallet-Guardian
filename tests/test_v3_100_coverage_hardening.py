from __future__ import annotations

from typing import Any

import pytest

from dgb_wallet_guardian.client import WalletGuardian
from dgb_wallet_guardian.contracts.v3_types import GWv3Request
from dgb_wallet_guardian.guardian_engine import GuardianEngine
from dgb_wallet_guardian.models import RiskLevel, TransactionContext, WalletContext
from dgb_wallet_guardian.v3 import GuardianWalletV3


def _base_tx_request() -> dict[str, Any]:
    return {
        "contract_version": 3,
        "component": "guardian_wallet",
        "mode": "tx",
        "request_id": "tx-hardening",
        "wallet_ctx": {"balance": 100.0, "typical_amount": 10.0},
        "tx_ctx": {"to_address": "DGB_DEST", "amount": 1.0, "fee": 0.1},
        "auth_ctx": {},
        "extra_signals": {"trusted_device": True},
    }


def _base_qid_request() -> dict[str, Any]:
    return {
        "contract_version": 3,
        "component": "guardian_wallet",
        "mode": "qid_auth",
        "request_id": "qid-hardening",
        "wallet_ctx": {},
        "tx_ctx": {},
        "auth_ctx": {
            "qid_verified": True,
            "service_id": "example.com",
            "callback_url": "https://example.com/qid",
            "nonce": "nonce",
            "address": "DGB_ADDR",
            "pubkey": "PUBKEY",
        },
        "extra_signals": {},
    }


def test_client_is_safe_to_send_covers_true_and_false_paths() -> None:
    guardian = WalletGuardian()

    assert guardian.is_safe_to_send(
        wallet_ctx={"balance": 100.0, "known_addresses": ["DGB_KNOWN"]},
        tx_ctx={"to_address": "DGB_KNOWN", "amount": 1.0},
    ) is True

    assert guardian.is_safe_to_send(
        wallet_ctx={"balance": 100.0, "typical_amount": 1.0, "known_addresses": []},
        tx_ctx={"to_address": "DGB_NEW", "amount": 100.0},
        extra_signals={"sentinel_status": "CRITICAL"},
    ) is False


@pytest.mark.parametrize("mode", ["", " ", "unknown"])
def test_from_dict_rejects_invalid_modes(mode: str) -> None:
    raw = {
        "contract_version": 3,
        "component": "guardian_wallet",
        "request_id": "bad-mode",
        "mode": mode,
        "wallet_ctx": {},
        "tx_ctx": {},
        "auth_ctx": {},
        "extra_signals": {},
    }
    with pytest.raises(ValueError):
        GWv3Request.from_dict(raw)


def test_from_dict_rejects_non_dict_auth_ctx() -> None:
    raw = {
        "contract_version": 3,
        "component": "guardian_wallet",
        "request_id": "bad-auth",
        "wallet_ctx": {},
        "tx_ctx": {},
        "auth_ctx": [],
        "extra_signals": {},
    }
    with pytest.raises(ValueError):
        GWv3Request.from_dict(raw)  # type: ignore[arg-type]


def test_evaluate_converts_unexpected_parser_exception_to_fail_closed(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def boom(_raw: dict[str, Any]) -> GWv3Request:
        raise RuntimeError("parser exploded")

    monkeypatch.setattr(GWv3Request, "from_dict", staticmethod(boom))
    out = GuardianWalletV3().evaluate({"request_id": None})

    assert out["outcome"] == "deny"
    assert out["request_id"] == "unknown"
    assert out["reason_codes"] == ["GW_ERROR_INVALID_REQUEST"]
    assert out["meta"]["fail_closed"] is True


def test_tx_mode_rejects_any_auth_context() -> None:
    req = _base_tx_request()
    req["auth_ctx"] = {"qid_verified": True}

    out = GuardianWalletV3().evaluate(req)

    assert out["outcome"] == "deny"
    assert out["reason_codes"] == ["GW_ERROR_UNKNOWN_AUTH_KEY"]


def test_oversize_guard_fails_closed_when_payload_cannot_be_encoded() -> None:
    req = _base_tx_request()
    req["tx_ctx"]["memo"] = object()

    out = GuardianWalletV3().evaluate(req)

    assert out["outcome"] == "deny"
    assert out["reason_codes"] == ["GW_ERROR_OVERSIZE"]


def test_stable_normalization_edge_paths_are_deterministic() -> None:
    wallet = GuardianWalletV3._stable_wallet(
        {
            "balance": True,
            "typical_amount": "10",
            "wallet_age_days": "7",
            "tx_count_24h": "2",
        }
    )
    tx = GuardianWalletV3._stable_tx({"amount": "1.25", "fee": "0.2"})
    auth = GuardianWalletV3._stable_auth(
        {
            "qid_verified": 1,
            "binding_verified": 0,
            "issued_at": "100",
            "expires_at": "200",
        }
    )
    signals = GuardianWalletV3._stable_signals({"trusted_device": 1, "device_mismatch": 0})

    assert wallet == {
        "balance": 1.0,
        "typical_amount": 10.0,
        "wallet_age_days": 7,
        "tx_count_24h": 2,
    }
    assert tx == {"amount": 1.25, "fee": 0.2}
    assert auth == {
        "qid_verified": True,
        "binding_verified": False,
        "issued_at": 100,
        "expires_at": 200,
    }
    assert signals == {"trusted_device": True, "device_mismatch": False}


def test_qid_auth_rejects_wallet_and_tx_contexts() -> None:
    gw = GuardianWalletV3()

    req_wallet = _base_qid_request()
    req_wallet["wallet_ctx"] = {"balance": 1}
    assert gw.evaluate(req_wallet)["reason_codes"] == ["GW_ERROR_UNKNOWN_WALLET_KEY"]

    req_tx = _base_qid_request()
    req_tx["tx_ctx"] = {"amount": 1}
    assert gw.evaluate(req_tx)["reason_codes"] == ["GW_ERROR_UNKNOWN_TX_KEY"]


def test_qid_auth_rejects_unknown_signal_key() -> None:
    req = _base_qid_request()
    req["extra_signals"] = {"unknown_signal": "x"}

    out = GuardianWalletV3().evaluate(req)

    assert out["outcome"] == "deny"
    assert out["reason_codes"] == ["GW_ERROR_UNKNOWN_SIGNAL_KEY"]


@pytest.mark.parametrize(
    "auth_update",
    [
        {"qid_verified": "true"},
        {"service_id": ""},
        {"callback_url": 123},
        {"nonce": ""},
        {"address": None},
        {"pubkey": ""},
        {"binding_verified": "yes"},
        {"key_id": ""},
        {"require": "unsupported"},
        {"issued_at": 100},
        {"issued_at": 200, "expires_at": 100},
        {"issued_at": 0, "expires_at": 100},
        {"issued_at": 100, "expires_at": "200"},
    ],
)
def test_qid_auth_rejects_invalid_auth_fields(auth_update: dict[str, Any]) -> None:
    req = _base_qid_request()
    req["auth_ctx"].update(auth_update)

    out = GuardianWalletV3().evaluate(req)

    assert out["outcome"] == "deny"
    assert out["reason_codes"] == ["GW_ERROR_INVALID_REQUEST"]


@pytest.mark.parametrize(
    "signal_update",
    [
        {"trusted_device": "yes"},
        {"device_mismatch": "no"},
        {"sentinel_status": ""},
        {"session": 123},
    ],
)
def test_qid_auth_rejects_invalid_signal_fields(signal_update: dict[str, Any]) -> None:
    req = _base_qid_request()
    req["extra_signals"].update(signal_update)

    out = GuardianWalletV3().evaluate(req)

    assert out["outcome"] == "deny"
    assert out["reason_codes"] == ["GW_ERROR_INVALID_REQUEST"]


def test_qid_auth_escalates_on_sentinel_alert_and_normalizes_optional_fields() -> None:
    req = _base_qid_request()
    req["auth_ctx"].update(
        {
            "binding_verified": True,
            "key_id": "key-1",
            "require": "dual-proof",
            "issued_at": 100,
            "expires_at": 200,
        }
    )
    req["extra_signals"] = {"sentinel_status": "CRITICAL", "device_mismatch": False}

    out = GuardianWalletV3().evaluate(req)

    assert out["outcome"] == "escalate"
    assert out["reason_codes"] == ["GW_ESCALATE_QID_SENTINEL_ALERT"]
    assert out["evidence"]["auth_ctx"]["binding_verified"] is True
    assert out["evidence"]["auth_ctx"]["issued_at"] == 100


def test_qid_auth_escalates_on_device_mismatch() -> None:
    req = _base_qid_request()
    req["extra_signals"] = {"device_mismatch": True}

    out = GuardianWalletV3().evaluate(req)

    assert out["outcome"] == "escalate"
    assert out["reason_codes"] == ["GW_ESCALATE_QID_UNTRUSTED_DEVICE"]


def test_helper_methods_return_expected_fail_closed_defaults() -> None:
    gw = GuardianWalletV3()

    assert gw._is_finite_number(True) is True
    assert gw._is_finite_number("not-a-number") is True
    assert gw._safe_request_id("not-a-dict") == "unknown"


def test_engine_adaptive_sink_covers_high_and_critical_severity_paths() -> None:
    seen: list[Any] = []

    high_wallet = WalletContext(balance=100.0, known_addresses=["DGB_KNOWN"])
    high_tx = TransactionContext(to_address="DGB_KNOWN", amount=90.0)
    high_decision = GuardianEngine().evaluate_transaction(
        high_wallet,
        high_tx,
        extra_signals={"adaptive_sink": seen.append},
    )
    assert high_decision.level.name == "HIGH"
    assert seen[-1].severity == 0.7

    critical_wallet = WalletContext(balance=100.0, typical_amount=1.0, known_addresses=[])
    critical_tx = TransactionContext(to_address="DGB_NEW", amount=100.0)
    critical_decision = GuardianEngine().evaluate_transaction(
        critical_wallet,
        critical_tx,
        extra_signals={"adaptive_sink": seen.append, "sentinel_status": "CRITICAL"},
    )
    assert critical_decision.level.name == "CRITICAL"
    assert seen[-1].severity == 0.9


def test_v3_unreachable_safety_fallbacks_are_explicitly_denying(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    gw = GuardianWalletV3()

    req = _base_tx_request()
    parsed = GWv3Request.from_dict(req)

    monkeypatch.setattr(
        GWv3Request,
        "from_dict",
        staticmethod(
            lambda _raw: parsed.__class__(
                contract_version=parsed.contract_version,
                component=parsed.component,
                request_id=parsed.request_id,
                mode="impossible-mode",
                wallet_ctx=parsed.wallet_ctx,
                tx_ctx=parsed.tx_ctx,
                auth_ctx=parsed.auth_ctx,
                extra_signals=parsed.extra_signals,
            )
        ),
    )

    out = gw.evaluate(req)
    assert out["outcome"] == "deny"
    assert out["reason_codes"] == ["GW_ERROR_INVALID_MODE"]


def test_direct_mapping_helpers_cover_normal_high_and_default_paths() -> None:
    gw = GuardianWalletV3()

    assert gw._map_outcome(GuardianEngine()._map_score_to_level(0.0)) == "allow"
    assert gw._map_outcome(RiskLevel.HIGH) == "deny"
    assert GuardianEngine()._map_score_to_level(2.0).name == "HIGH"
    assert GuardianEngine()._suggest_actions(GuardianEngine()._map_score_to_level(2.0)) == [
        "REQUIRE_EXTRA_CONFIRMATION",
        "WARN_USER",
        "LOG_EVENT",
    ]
    assert gw._extract_reason_codes([], GuardianEngine()._map_score_to_level(0.0))[0] == (
        "GW_OK_HEALTHY_ALLOW"
    )
    assert gw._extract_reason_codes([], RiskLevel.HIGH)[0] == "GW_DENY_HIGH_OR_CRITICAL"
