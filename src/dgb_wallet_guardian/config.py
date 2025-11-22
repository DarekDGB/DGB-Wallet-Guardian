from __future__ import annotations

from dataclasses import dataclass


@dataclass
class GuardianConfig:
    """
    Configuration for DGB Wallet Guardian.

    In this reference version we keep it minimal and safe.
    Real wallet teams can extend this with:
    - risk thresholds
    - profile modes (safe/normal/advanced)
    - external reputation sources
    """

    # Basic thresholds for demo / reference
    max_normal_send_ratio: float = 0.5  # fraction of balance for "normal" sends
    large_send_warning_ratio: float = 0.9  # fraction of balance that triggers WARNING
    block_full_balance_if_high_risk: bool = True


def load_config(path: str | None = None) -> GuardianConfig:
    """
    Load configuration from file or return defaults.

    For now we ignore `path` and just return a default config object.
    Wallet developers can plug in real config loading (YAML/JSON) here.
    """
    _ = path
    return GuardianConfig()
