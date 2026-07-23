"""
DGB Wallet Guardian – Layer-4 protection gate for DigiByte wallets.

Guardian Wallet evaluates:
- transaction intent (`mode="tx"`)
- Q-ID authentication facts (`mode="qid_auth"`)

It is deterministic, fail-closed, and non-executing.
Guardian never signs or broadcasts DigiByte transactions and never holds wallet keys.
"""

from .client import WalletGuardian
from .v3 import GuardianWalletV3

__all__ = ["WalletGuardian", "GuardianWalletV3"]
__version__ = "3.2.0"
