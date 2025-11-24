from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional


class RiskLevel(str, Enum):
    """Risk classification for a wallet action or transaction."""
    NORMAL = "NORMAL"
    ELEVATED = "ELEVATED"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


@dataclass
class WalletContext:
    """
    Snapshot of wallet state at the time of evaluation.

    All balances are expressed in DGB for simplicity in this reference
    implementation. Production systems may want satoshi-level precision.
    """

    balance: float
    typical_amount: Optional[float] = None
    typical_fee: Optional[float] = None

    recent_send_count: int = 0
    recent_window_seconds: int = 0

    known_addresses: List[str] = field(default_factory=list)

    # Daily statistics (added for v2 behaviour / limits)
    daily_sent_amount: float = 0.0
    last_daily_reset_at: Optional[datetime] = None

    # room for additional metadata
    extra: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TransactionContext:
    """Information about the outgoing transaction being evaluated."""

    to_address: str
    amount: float

    fee: Optional[float] = None
    destination_risk_score: Optional[float] = None  # 0.0–1.0 if available

    # optional fields for richer scenarios
    memo: Optional[str] = None
    created_at: Optional[int] = None  # unix timestamp
    extra: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DeviceState:
    """
    Information about the device that is initiating the transaction.
    Used to detect new / untrusted devices.
    """

    device_id: str
    trusted: bool = True
    first_seen_at: Optional[datetime] = None
    last_seen_at: Optional[datetime] = None
    extra: Dict[str, Any] = field(default_factory=dict)


@dataclass
class GuardianDecision:
    """
    Final decision returned by Wallet Guardian.

    - level   – RiskLevel classification
    - score   – internal numeric score (for logs/analysis)
    - actions – recommended wallet/ADN actions
    - reasons – human/machine-readable rule descriptions
    """

    level: RiskLevel
    score: float
    actions: List[str] = field(default_factory=list)
    reasons: List[str] = field(default_factory=list)

    def is_blocking(self) -> bool:
        """Convenience helper: True if signing should be blocked."""
        return self.level in {RiskLevel.HIGH, RiskLevel.CRITICAL}
