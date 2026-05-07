from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict


@dataclass(frozen=True)
class GWv3Request:
    contract_version: int
    component: str
    request_id: str
    mode: str
    wallet_ctx: Dict[str, Any]
    tx_ctx: Dict[str, Any]
    auth_ctx: Dict[str, Any]
    extra_signals: Dict[str, Any]

    @staticmethod
    def from_dict(raw: Dict[str, Any]) -> "GWv3Request":
        if not isinstance(raw, dict):
            raise ValueError("GW_ERROR_INVALID_REQUEST")

        allowed = {
            "contract_version",
            "component",
            "request_id",
            "mode",
            "wallet_ctx",
            "tx_ctx",
            "auth_ctx",
            "extra_signals",
        }
        unknown = set(raw.keys()) - allowed
        if unknown:
            raise ValueError("GW_ERROR_UNKNOWN_TOP_LEVEL_KEY")

        contract_version = raw.get("contract_version")
        component = raw.get("component")
        request_id = raw.get("request_id")
        mode = raw.get("mode", "tx")
        wallet_ctx = raw.get("wallet_ctx", {})
        tx_ctx = raw.get("tx_ctx", {})
        auth_ctx = raw.get("auth_ctx", {})
        extra_signals = raw.get("extra_signals", {})

        if not isinstance(contract_version, int):
            raise ValueError("GW_ERROR_INVALID_REQUEST")
        if not isinstance(component, str) or not component.strip():
            raise ValueError("GW_ERROR_INVALID_REQUEST")
        if not isinstance(request_id, str) or not request_id.strip():
            raise ValueError("GW_ERROR_INVALID_REQUEST")
        if not isinstance(mode, str) or not mode.strip():
            raise ValueError("GW_ERROR_INVALID_REQUEST")
        if mode.strip() not in {"tx", "qid_auth"}:
            raise ValueError("GW_ERROR_INVALID_MODE")
        if not isinstance(wallet_ctx, dict):
            raise ValueError("GW_ERROR_INVALID_REQUEST")
        if not isinstance(tx_ctx, dict):
            raise ValueError("GW_ERROR_INVALID_REQUEST")
        if not isinstance(auth_ctx, dict):
            raise ValueError("GW_ERROR_INVALID_REQUEST")
        if not isinstance(extra_signals, dict):
            raise ValueError("GW_ERROR_INVALID_REQUEST")

        return GWv3Request(
            contract_version=contract_version,
            component=component.strip(),
            request_id=request_id.strip(),
            mode=mode.strip(),
            wallet_ctx=wallet_ctx,
            tx_ctx=tx_ctx,
            auth_ctx=auth_ctx,
            extra_signals=extra_signals,
        )
