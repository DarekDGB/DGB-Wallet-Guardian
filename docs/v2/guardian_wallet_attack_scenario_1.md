# DigiByte Wallet Guardian v2 - Historical Attack Scenario GW-SIM-001

Author: DarekDGB

Status: Historical, simulation-only, and non-authoritative

## Purpose

GW-SIM-001 preserves an early threat-analysis scenario for Wallet Guardian v2.
It is not an executable current test, a testnet result, or proof of implemented
wallet enforcement.

Current contract identity and Shield v4 behavior are documented in
`docs/v3/MANIFEST.md` and `docs/v4/CONTRACT.md`.

The conceptual scenario explored escalating withdrawal risk:

| Step | Relative time | Conceptual risk | Amount | Intended observation |
|---|---:|---|---:|---|
| 1 | 0 minutes | LOW | 3,000 DGB | ordinary initial request |
| 2 | 3 minutes | LOW | 4,000 DGB | rapid repeat activity |
| 3 | 8 minutes | MEDIUM | 5,000 DGB | aggregate-volume concern |
| 4 | 15 minutes | HIGH | 2,500 DGB | elevated upstream risk |
| 5 | 25 minutes | HIGH | 1,000 DGB | persistent attempts |

Earlier versions mapped this sequence to `ALLOW`, `DELAY`, `FREEZE`, and
`REJECT`. Those labels describe the historical proposal, not the current
implementation contract.

## Current implementation difference

The current retained reference engine:

- evaluates `WalletContext` and `TransactionContext` with
  `GuardianEngine.evaluate_transaction`;
- classifies risk as `NORMAL`, `ELEVATED`, `HIGH`, or `CRITICAL`;
- returns recommended actions and reasons;
- accepts optional external signals; and
- can send best-effort advisory telemetry to a caller-supplied Adaptive Core
  sink.

It does not implement the exact GW-SIM-001 cooldown, rolling daily-volume,
persistent-freeze, `evaluate_withdrawal`, log-file, or ADN-risk state machine.

`docs/v2/legacy/simulate_guardian_wallet_scenario_1.py` contains archived
pseudo-code and Markdown. It is intentionally not imported, collected, or
claimed as a runnable proof. Formal retirement or conversion of that path
requires a separate controlled decision.

## Security and authority boundary

The scenario uses no real keys, UTXOs, RPC connection, wallet, or testnet.

Wallet Guardian risk output is component evidence only. It cannot:

- sign or broadcast DigiByte transactions;
- hold or use wallet private keys;
- change DigiByte consensus;
- execute an `ALLOW`, `DELAY`, `FREEZE`, or `REJECT` action;
- bypass the Shield Orchestrator; or
- grant AdamantineOS final policy or execution authority.

Shield v4 evidence signing is separate from transaction signing. AdamantineOS
remains the final fail-closed policy and execution boundary.

## Use

This scenario may inform future tests, but any implementation or integration
claim requires current code, regression tests, green CI, and fresh repository
verification.
