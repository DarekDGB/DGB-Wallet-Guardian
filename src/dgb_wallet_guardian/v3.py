from __future__ import annotations

import json
import math
from dataclasses import dataclass
from typing import Any, Dict, List

from .client import WalletGuardian
from .models import RiskLevel
from .contracts.v3_hash import canonical_sha256
from .contracts.v3_reason_codes import ReasonCode
from .contracts.v3_types import GWv3Request


@dataclass(frozen=True)
class GuardianWalletV3:
    """
    Guardian Wallet v3 Contract Gate (Layer-4).

    Goals:
    - strict schema, deny unknown keys
    - fail-closed semantics
    - deterministic output + deterministic meta
    - stable reason_codes (no magic strings)
    - calls v2 engine for tx behavior (no authority expansion)
    - provides explicit qid_auth mode for identity-policy evaluation
    """

    COMPONENT: str = "guardian_wallet"
    CONTRACT_VERSION: int = 3

    MAX_PAYLOAD_BYTES: int = 128_000

    WALLET_KEYS = {"balance", "typical_amount", "wallet_age_days", "tx_count_24h"}
    TX_KEYS = {"to_address", "amount", "fee", "memo", "asset_id"}
    AUTH_KEYS = {
        "qid_verified",
        "binding_verified",
        "service_id",
        "callback_url",
        "nonce",
        "address",
        "pubkey",
        "key_id",
        "require",
        "issued_at",
        "expires_at",
    }
    SIGNAL_KEYS = {"device_fingerprint", "sentinel_status", "geo_ip", "session", "trusted_device", "device_mismatch"}

    def evaluate(self, request: Dict[str, Any]) -> Dict[str, Any]:
        latency_ms = 0

        try:
            req = GWv3Request.from_dict(request)
        except ValueError as e:
            code = str(e) or ReasonCode.GW_ERROR_INVALID_REQUEST.value
            return self._error(request_id=self._safe_request_id(request), reason_code=code, latency_ms=latency_ms)
        except Exception:
            return self._error(request_id=self._safe_request_id(request), reason_code=ReasonCode.GW_ERROR_INVALID_REQUEST.value, latency_ms=latency_ms)

        if req.contract_version != self.CONTRACT_VERSION:
            return self._error(request_id=req.request_id, reason_code=ReasonCode.GW_ERROR_SCHEMA_VERSION.value, latency_ms=latency_ms)
        if req.component != self.COMPONENT:
            return self._error(request_id=req.request_id, reason_code=ReasonCode.GW_ERROR_INVALID_REQUEST.value, latency_ms=latency_ms)
        if self._encoded_size_bytes(request) > self.MAX_PAYLOAD_BYTES:
            return self._error(request_id=req.request_id, reason_code=ReasonCode.GW_ERROR_OVERSIZE.value, latency_ms=latency_ms)

        if req.mode == "tx":
            return self._evaluate_tx(req=req, latency_ms=latency_ms)
        if req.mode == "qid_auth":
            return self._evaluate_qid_auth(req=req, latency_ms=latency_ms)
        return self._error(request_id=req.request_id, reason_code=ReasonCode.GW_ERROR_INVALID_MODE.value, latency_ms=latency_ms)

    def _evaluate_tx(self, *, req: GWv3Request, latency_ms: int) -> Dict[str, Any]:
        if set(req.wallet_ctx.keys()) - self.WALLET_KEYS:
            return self._error(request_id=req.request_id, reason_code=ReasonCode.GW_ERROR_UNKNOWN_WALLET_KEY.value, latency_ms=latency_ms)
        if set(req.tx_ctx.keys()) - self.TX_KEYS:
            return self._error(request_id=req.request_id, reason_code=ReasonCode.GW_ERROR_UNKNOWN_TX_KEY.value, latency_ms=latency_ms)
        if set(req.auth_ctx.keys()):
            return self._error(request_id=req.request_id, reason_code=ReasonCode.GW_ERROR_UNKNOWN_AUTH_KEY.value, latency_ms=latency_ms)
        if set(req.extra_signals.keys()) - self.SIGNAL_KEYS:
            return self._error(request_id=req.request_id, reason_code=ReasonCode.GW_ERROR_UNKNOWN_SIGNAL_KEY.value, latency_ms=latency_ms)
        if not self._numbers_ok(req.wallet_ctx, req.tx_ctx):
            return self._error(request_id=req.request_id, reason_code=ReasonCode.GW_ERROR_BAD_NUMBER.value, latency_ms=latency_ms)

        guardian = WalletGuardian()
        decision = guardian.evaluate_transaction(req.wallet_ctx, req.tx_ctx, req.extra_signals)
        outcome = self._map_outcome(decision.level)
        reason_codes = self._extract_reason_codes(decision.reasons, decision.level)

        v3_context = {
            "component": self.COMPONENT,
            "contract_version": self.CONTRACT_VERSION,
            "mode": "tx",
            "request_id": req.request_id,
            "wallet_ctx": self._stable_wallet(req.wallet_ctx),
            "tx_ctx": self._stable_tx(req.tx_ctx),
            "auth_ctx": {},
            "extra_signals": self._stable_signals(req.extra_signals),
            "outcome": outcome,
            "risk_level": decision.level.value,
            "reason_codes": reason_codes,
        }
        context_hash = canonical_sha256(v3_context)

        return {
            "contract_version": self.CONTRACT_VERSION,
            "component": self.COMPONENT,
            "request_id": req.request_id,
            "context_hash": context_hash,
            "outcome": outcome,
            "risk": {"level": decision.level.value, "score": float(decision.score)},
            "reason_codes": reason_codes,
            "evidence": {"actions": list(decision.actions), "reasons": list(decision.reasons)},
            "meta": {"latency_ms": latency_ms, "fail_closed": True, "mode": "tx"},
        }

    def _evaluate_qid_auth(self, *, req: GWv3Request, latency_ms: int) -> Dict[str, Any]:
        if req.wallet_ctx:
            return self._error(request_id=req.request_id, reason_code=ReasonCode.GW_ERROR_UNKNOWN_WALLET_KEY.value, latency_ms=latency_ms)
        if req.tx_ctx:
            return self._error(request_id=req.request_id, reason_code=ReasonCode.GW_ERROR_UNKNOWN_TX_KEY.value, latency_ms=latency_ms)
        if set(req.auth_ctx.keys()) - self.AUTH_KEYS:
            return self._error(request_id=req.request_id, reason_code=ReasonCode.GW_ERROR_UNKNOWN_AUTH_KEY.value, latency_ms=latency_ms)
        if set(req.extra_signals.keys()) - self.SIGNAL_KEYS:
            return self._error(request_id=req.request_id, reason_code=ReasonCode.GW_ERROR_UNKNOWN_SIGNAL_KEY.value, latency_ms=latency_ms)

        auth = req.auth_ctx
        if not isinstance(auth.get("qid_verified"), bool):
            return self._error(request_id=req.request_id, reason_code=ReasonCode.GW_ERROR_INVALID_REQUEST.value, latency_ms=latency_ms)
        for key in ("service_id", "callback_url", "nonce", "address", "pubkey"):
            value = auth.get(key)
            if not isinstance(value, str) or not value:
                return self._error(request_id=req.request_id, reason_code=ReasonCode.GW_ERROR_INVALID_REQUEST.value, latency_ms=latency_ms)
        if "binding_verified" in auth and not isinstance(auth.get("binding_verified"), bool):
            return self._error(request_id=req.request_id, reason_code=ReasonCode.GW_ERROR_INVALID_REQUEST.value, latency_ms=latency_ms)
        if "key_id" in auth and (not isinstance(auth.get("key_id"), str) or not auth.get("key_id")):
            return self._error(request_id=req.request_id, reason_code=ReasonCode.GW_ERROR_INVALID_REQUEST.value, latency_ms=latency_ms)

        require = auth.get("require", "legacy")
        if not isinstance(require, str) or require not in {"legacy", "dual-proof"}:
            return self._error(request_id=req.request_id, reason_code=ReasonCode.GW_ERROR_INVALID_REQUEST.value, latency_ms=latency_ms)
        if ("issued_at" in auth) != ("expires_at" in auth):
            return self._error(request_id=req.request_id, reason_code=ReasonCode.GW_ERROR_INVALID_REQUEST.value, latency_ms=latency_ms)
        if "issued_at" in auth:
            issued_at = auth.get("issued_at")
            expires_at = auth.get("expires_at")
            if not isinstance(issued_at, int) or not isinstance(expires_at, int) or issued_at <= 0 or expires_at <= 0 or issued_at >= expires_at:
                return self._error(request_id=req.request_id, reason_code=ReasonCode.GW_ERROR_INVALID_REQUEST.value, latency_ms=latency_ms)

        for key, value in req.extra_signals.items():
            if key in {"trusted_device", "device_mismatch"} and not isinstance(value, bool):
                return self._error(request_id=req.request_id, reason_code=ReasonCode.GW_ERROR_INVALID_REQUEST.value, latency_ms=latency_ms)
            if key not in {"trusted_device", "device_mismatch"} and (not isinstance(value, str) or not value):
                return self._error(request_id=req.request_id, reason_code=ReasonCode.GW_ERROR_INVALID_REQUEST.value, latency_ms=latency_ms)

        outcome = "allow"
        level = "NORMAL"
        score = 0.0
        actions: List[str] = []
        reason_codes: List[str] = [ReasonCode.GW_OK_QID_AUTH_ALLOW.value]
        evidence_reasons: List[str] = ["QID_AUTH_VERIFIED: Verified Q-ID authentication facts received."]

        if auth["qid_verified"] is not True:
            outcome = "deny"
            level = "HIGH"
            score = 1.0
            reason_codes = [ReasonCode.GW_DENY_QID_UNVERIFIED.value]
            actions = ["deny_auth"]
            evidence_reasons = ["QID_AUTH_UNVERIFIED: Q-ID verification flag is false."]
        elif require == "dual-proof" and auth.get("binding_verified") is not True:
            outcome = "deny"
            level = "HIGH"
            score = 1.0
            reason_codes = [ReasonCode.GW_DENY_QID_BINDING_REQUIRED.value]
            actions = ["deny_auth"]
            evidence_reasons = ["QID_AUTH_BINDING_REQUIRED: dual-proof flow requires verified binding."]
        else:
            sentinel_status = req.extra_signals.get("sentinel_status")
            trusted_device = req.extra_signals.get("trusted_device")
            device_mismatch = req.extra_signals.get("device_mismatch", False)
            if sentinel_status in {"HIGH", "CRITICAL"}:
                outcome = "escalate"
                level = "ELEVATED"
                score = 0.5
                reason_codes = [ReasonCode.GW_ESCALATE_QID_SENTINEL_ALERT.value]
                actions = ["step_up_auth"]
                evidence_reasons = [f"QID_AUTH_SENTINEL_ALERT: Sentinel status is {sentinel_status}."]
            elif trusted_device is False or device_mismatch is True:
                outcome = "escalate"
                level = "ELEVATED"
                score = 0.35
                reason_codes = [ReasonCode.GW_ESCALATE_QID_UNTRUSTED_DEVICE.value]
                actions = ["step_up_auth"]
                evidence_reasons = ["QID_AUTH_UNTRUSTED_DEVICE: Device trust signal requires step-up authentication."]

        v3_context = {
            "component": self.COMPONENT,
            "contract_version": self.CONTRACT_VERSION,
            "mode": "qid_auth",
            "request_id": req.request_id,
            "wallet_ctx": {},
            "tx_ctx": {},
            "auth_ctx": self._stable_auth(req.auth_ctx),
            "extra_signals": self._stable_signals(req.extra_signals),
            "outcome": outcome,
            "risk_level": level,
            "reason_codes": reason_codes,
        }
        context_hash = canonical_sha256(v3_context)

        return {
            "contract_version": self.CONTRACT_VERSION,
            "component": self.COMPONENT,
            "request_id": req.request_id,
            "context_hash": context_hash,
            "outcome": outcome,
            "risk": {"level": level, "score": score},
            "reason_codes": reason_codes,
            "evidence": {"actions": actions, "reasons": evidence_reasons, "auth_ctx": self._stable_auth(req.auth_ctx)},
            "meta": {"latency_ms": latency_ms, "fail_closed": True, "mode": "qid_auth"},
        }

    @staticmethod
    def _safe_request_id(request: Any) -> str:
        if isinstance(request, dict):
            rid = request.get("request_id", "unknown")
            return str(rid) if rid is not None else "unknown"
        return "unknown"

    @staticmethod
    def _encoded_size_bytes(obj: Any) -> int:
        try:
            return len(json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8"))
        except Exception:
            return 10**9

    @staticmethod
    def _is_finite_number(x: Any) -> bool:
        if isinstance(x, bool):
            return True
        if isinstance(x, (int, float)):
            return math.isfinite(float(x))
        return True

    def _numbers_ok(self, wallet_ctx: Dict[str, Any], tx_ctx: Dict[str, Any]) -> bool:
        numeric_fields = [
            wallet_ctx.get("balance"),
            wallet_ctx.get("typical_amount"),
            wallet_ctx.get("wallet_age_days"),
            wallet_ctx.get("tx_count_24h"),
            tx_ctx.get("amount"),
            tx_ctx.get("fee"),
        ]
        return all(self._is_finite_number(v) for v in numeric_fields if v is not None)

    @staticmethod
    def _stable_wallet(w: Dict[str, Any]) -> Dict[str, Any]:
        out: Dict[str, Any] = dict(w)
        if "balance" in out:
            out["balance"] = float(out["balance"])
        if "typical_amount" in out:
            out["typical_amount"] = float(out["typical_amount"])
        if "wallet_age_days" in out and out["wallet_age_days"] is not None:
            out["wallet_age_days"] = int(out["wallet_age_days"])
        if "tx_count_24h" in out and out["tx_count_24h"] is not None:
            out["tx_count_24h"] = int(out["tx_count_24h"])
        return out

    @staticmethod
    def _stable_tx(t: Dict[str, Any]) -> Dict[str, Any]:
        out: Dict[str, Any] = dict(t)
        if "amount" in out:
            out["amount"] = float(out["amount"])
        if "fee" in out and out["fee"] is not None:
            out["fee"] = float(out["fee"])
        return out

    @staticmethod
    def _stable_auth(a: Dict[str, Any]) -> Dict[str, Any]:
        out: Dict[str, Any] = dict(a)
        if "qid_verified" in out:
            out["qid_verified"] = bool(out["qid_verified"])
        if "binding_verified" in out:
            out["binding_verified"] = bool(out["binding_verified"])
        if "issued_at" in out:
            out["issued_at"] = int(out["issued_at"])
        if "expires_at" in out:
            out["expires_at"] = int(out["expires_at"])
        return out

    @staticmethod
    def _stable_signals(s: Dict[str, Any]) -> Dict[str, Any]:
        out: Dict[str, Any] = dict(s)
        if "trusted_device" in out:
            out["trusted_device"] = bool(out["trusted_device"])
        if "device_mismatch" in out:
            out["device_mismatch"] = bool(out["device_mismatch"])
        return out

    @staticmethod
    def _map_outcome(level: RiskLevel) -> str:
        if level == RiskLevel.NORMAL:
            return "allow"
        if level == RiskLevel.ELEVATED:
            return "escalate"
        return "deny"

    def _extract_reason_codes(self, reasons: List[str], level: RiskLevel) -> List[str]:
        rule_ids: List[str] = []
        for r in reasons:
            if isinstance(r, str) and ":" in r:
                rid = r.split(":", 1)[0].strip()
                if rid:
                    rule_ids.append(rid)
        rule_ids = sorted(set(rule_ids))
        if level == RiskLevel.NORMAL:
            base = [ReasonCode.GW_OK_HEALTHY_ALLOW.value]
        elif level == RiskLevel.ELEVATED:
            base = [ReasonCode.GW_ESCALATE_ELEVATED.value]
        else:
            base = [ReasonCode.GW_DENY_HIGH_OR_CRITICAL.value]
        return base + rule_ids

    def _error(self, request_id: str, reason_code: str, latency_ms: int) -> Dict[str, Any]:
        context_hash = canonical_sha256(
            {
                "component": self.COMPONENT,
                "contract_version": self.CONTRACT_VERSION,
                "request_id": str(request_id),
                "reason_code": reason_code,
            }
        )
        return {
            "contract_version": self.CONTRACT_VERSION,
            "component": self.COMPONENT,
            "request_id": str(request_id),
            "context_hash": context_hash,
            "outcome": "deny",
            "risk": {"level": "unknown", "score": 1.0},
            "reason_codes": [str(reason_code)],
            "evidence": {"details": {"error": str(reason_code)}},
            "meta": {"latency_ms": int(latency_ms), "fail_closed": True},
        }
