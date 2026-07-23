# DigiByte Wallet Guardian v2 - Historical Technical Note

Author: DarekDGB

Version: 2.0  
Status: Historical and non-authoritative

## Purpose

This document preserves the design intent of the unsupported Wallet Guardian
v2 line. It is not the current implementation contract, test evidence, or a
testnet-readiness claim.

The current supported contract and authority boundary are documented in:

- `README.md`;
- `SECURITY.md`;
- `docs/v3/GUARDIAN_V3.md`;
- `docs/v3/MANIFEST.md`;
- `docs/v3/RELEASE_STATUS_v3.2.0.md`; and
- `docs/v4/CONTRACT.md`.

If this historical note conflicts with current code, tests, or those documents,
the current sources control.

## Historical concept

The v2 concept treated Wallet Guardian as a transparent behavioral-risk layer
for outgoing wallet intent. Its proposed signals included transaction amount,
destination history, transaction frequency, fees, device context, and upstream
risk indicators. Its goal was to produce explainable risk evidence and
recommended protective actions without changing DigiByte consensus.

The historical labels `ALLOW`, `DELAY`, `FREEZE`, and `REJECT` describe that
early concept. They are not the current `GuardianDecision` or Shield v3/v4
wire contract.

## Current implementation reference

The retained reference engine currently exposes:

```text
GuardianEngine.evaluate_transaction(
    wallet_ctx: WalletContext,
    tx_ctx: TransactionContext,
    extra_signals: dict | None,
) -> GuardianDecision
```

`GuardianDecision` contains a `RiskLevel`, score, recommended actions, and
reasons. Current risk levels are:

```text
NORMAL
ELEVATED
HIGH
CRITICAL
```

`WalletGuardian` provides a dictionary-based adapter for this engine.
`adaptive_bridge.py` can emit best-effort advisory telemetry to a caller-supplied
sink. Sink failure is swallowed and cannot change the Guardian decision.

The repository does not implement the old `WithdrawalEvent`, `PolicyResult`,
`evaluate_withdrawal`, persistent wallet-freeze state, cooldown/daily-volume
scenario, or root-level runnable simulation described by earlier versions of
this note.

The file
`docs/v2/legacy/simulate_guardian_wallet_scenario_1.py` is retained as a
non-runnable historical reference. It is not a supported executable, test, or
proof artifact.

## Authority boundary

Wallet Guardian evaluates risk and produces evidence. It does not:

- sign or broadcast DigiByte transactions;
- hold, derive, or access wallet private keys;
- modify DigiByte consensus;
- execute wallet actions;
- issue a Shield Orchestrator receipt;
- override Shield verification; or
- grant AdamantineOS final policy or execution authority.

Shield v4 cryptographic adapters sign and verify Guardian component evidence
only. Evidence signing must not be confused with transaction signing or wallet
key custody.

Any caller that consumes Guardian risk output remains responsible for its own
policy and execution checks. AdamantineOS remains the final fail-closed policy
and execution boundary for Shield evidence.

## Historical scenario status

The conceptual GW-SIM-001 sequence remains documented in
`docs/v2/guardian_wallet_attack_scenario_1.md`. It is threat-analysis material,
not proof that the current engine implements that state machine or has been
integrated with a DigiByte wallet or testnet.

## License

MIT License.
