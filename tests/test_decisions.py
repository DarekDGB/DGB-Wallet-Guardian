from dgb_wallet_guardian.decisions import (
    GuardianDecisionType,
    GuardianResult,
)


def test_decision_enum_values():
    assert GuardianDecisionType.ALLOW == "allow"
    assert GuardianDecisionType.WARN == "warn"
    assert GuardianDecisionType.BLOCK == "block"


def test_guardian_result_defaults():
    r = GuardianResult(
        decision=GuardianDecisionType.ALLOW,
        reason="ok"
    )
    assert r.cooldown_seconds == 0
    assert r.require_second_factor is False
    assert r.reason == "ok"
