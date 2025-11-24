from dataclasses import dataclass
from enum import Enum

class GuardianDecision(str, Enum):
    ALLOW = "allow"
    WARN = "warn"
    DELAY = "delay"
    BLOCK = "block"
    REQUIRE_EXTRA_AUTH = "require_extra_auth"

@dataclass
class GuardianResult:
    decision: GuardianDecision
    reason: str
    cooldown_seconds: int = 0
    require_second_factor: bool = False
