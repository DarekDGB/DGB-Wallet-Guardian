from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class WalletContext:
    """
    Minimal context about the wallet and environment.

    This does NOT contain any private keys.
    It only describes metadata that can influence risk decisions.
    """

    balance: float = 0.0
    known_addresses: List[str] = field(default_factory=list)
    device_id: Optional[str] = None
    region: Optional[str] = None
    sentinel_status: str = "NORMAL"  # NORMAL / ELEVATED / HIGH / CRITICAL
    extra: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TxProposal:
    """
    A transaction proposal BEFORE signing.

    The wallet passes this to the guardian so it can evaluate risk first.
    """

    to_address: str
    amount: float
    fee: float
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class EvaluationResult:
    """
    Result of a wallet guardian evaluation.

    status:
        SAFE       – no significant issues found
        WARNING    – user should see a strong warning / confirm twice
        BLOCK      – transaction should be blocked unless user force-overrides

    score:
        0.0 – 1.0 risk score (higher = more dangerous)

    reasons:
        list of machine- and human-readable reason strings.
    """

    status: str
    score: float
    reasons: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "status": self.status,
            "score": self.score,
            "reasons": list(self.reasons),
        }
