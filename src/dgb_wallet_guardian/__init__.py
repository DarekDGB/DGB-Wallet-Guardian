"""
DGB Wallet Guardian – Layer-4 protection for DigiByte wallets.

This package provides a reference skeleton for:
- transaction risk evaluation
- device / behaviour checks
- integration with Sentinel AI v2 + ADN
"""

from .client import WalletGuardian  # convenience re-export

__all__ = ["WalletGuardian"]
__version__ = "0.1.0"
