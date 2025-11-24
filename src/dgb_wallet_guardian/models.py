from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class WalletState:
    balance: float
    daily_sent_amount: float = 0.0
    last_reset_at: Optional[datetime] = None

@dataclass
class DeviceState:
    device_id: str
    trusted: bool = True
    first_seen_at: Optional[datetime] = None
    last_seen_at: Optional[datetime] = None

@dataclass
class TxContext:
    amount: float
    destination_address: str
    created_at: datetime
