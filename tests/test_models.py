from dgb_wallet_guardian.models import (
    RiskLevel,
    WalletContext,
    TransactionContext,
    GuardianDecision,
)


def test_wallet_context_defaults():
    ctx = WalletContext(balance=100.0)

    assert ctx.balance == 100.0
    assert ctx.recent_send_count == 0
    assert ctx.recent_window_seconds == 0
    assert ctx.known_addresses == []
    assert ctx.extra == {}


def test_transaction_context_defaults():
    tx = TransactionContext(
        to_address="dgb1qexampleaddress",
        amount=42.0,
    )

    assert tx.to_address == "dgb1qexampleaddress"
    assert tx.amount == 42.0
    # optional fields should have sane defaults
    assert tx.fee is None
    assert tx.destination_risk_score is None
    assert tx.extra == {}


def test_guardian_decision_blocking_levels():
    critical = GuardianDecision(level=RiskLevel.CRITICAL, score=0.99)
    high = GuardianDecision(level=RiskLevel.HIGH, score=0.9)
    normal = GuardianDecision(level=RiskLevel.NORMAL, score=0.1)

    assert critical.is_blocking()
    assert high.is_blocking()
    assert not normal.is_blocking()
