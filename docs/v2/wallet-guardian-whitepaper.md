# DigiByte Wallet Guardian v2 - Historical Whitepaper

Author: DarekDGB

Version: 2.0  
Status: Historical and non-authoritative

## Scope

This document preserves the original Wallet Guardian v2 vision. Wallet
Guardian v2 is unsupported, and this whitepaper is not the current repository
contract, implementation specification, security proof, or testnet-readiness
statement.

Current behavior and authority boundaries are defined by the repository code,
tests, `README.md`, `SECURITY.md`, `docs/v3/MANIFEST.md`, and
`docs/v4/CONTRACT.md`.

## Historical vision

The v2 proposal described a behavioral protection layer that would examine
wallet intent and surrounding risk signals before a wallet decided whether to
continue. The proposal explored:

- unusually large transfers;
- unfamiliar destinations;
- rapid repeated activity;
- abnormal fees;
- device or session anomalies; and
- upstream risk signals.

The early `ALLOW`, `DELAY`, `FREEZE`, and `REJECT` vocabulary was conceptual.
It is not the current `GuardianDecision` model or a guaranteed state machine.

## Current repository boundary

The retained reference implementation evaluates `WalletContext` and
`TransactionContext` through `GuardianEngine.evaluate_transaction`. It returns
risk evidence with `NORMAL`, `ELEVATED`, `HIGH`, or `CRITICAL` classification,
recommended actions, and reasons.

The v3 contract provides deterministic `allow`, `escalate`, or `deny` verdict
evidence. The v4 contract adds cryptographically verifiable component evidence.
Neither contract executes a wallet action.

The old GW-SIM-001 material is retained only as historical threat analysis. Its
legacy pseudo-script is not a supported executable, current test, testnet
integration, or proof of an implemented cooldown, daily-limit, or persistent
freeze workflow.

## Cryptography and authority

Wallet Guardian Shield v4 cryptographic backends may sign Guardian component
evidence. They do not sign DigiByte transactions and do not handle wallet
private keys.

Wallet Guardian does not:

- broadcast transactions;
- change DigiByte consensus;
- approve final execution;
- replace the Shield Orchestrator;
- override a failed required Shield signature; or
- grant AdamantineOS authority.

Required `classical-ed25519` and `ml-dsa` evidence remains strict AND.
Optional draft FN-DSA/Falcon-1024 evidence cannot replace or rescue either
required path. AdamantineOS remains the final fail-closed policy and execution
boundary.

## Future work

Device analysis, address-similarity checks, automated behavior detection, and
wallet or testnet integration remain separate future work unless current code,
tests, and release evidence explicitly establish them.

## License

MIT License.
