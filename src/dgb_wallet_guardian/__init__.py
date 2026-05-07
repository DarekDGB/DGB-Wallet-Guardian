"""
DGB Wallet Guardian – Layer-4 protection gate for DigiByte wallets.

Guardian Wallet evaluates:
- transaction intent (`mode="tx"`)
- Q-ID authentication facts (`mode="qid_auth"`)

It is deterministic, fail-closed, and non-executing.
Guardian never signs, never broadcasts, and never touches keys.
"""

from .client import WalletGuardian
from .v3 import GuardianWalletV3

__all__ = ["WalletGuardian", "GuardianWalletV3"]
__version__ = "3.0.0"
