# Guardian Wallet v3 - Superseded Technical Specification

Author: DarekDGB

Status: Historical and non-authoritative

## Supersession notice

This file preserves the location of an early Guardian Wallet v3 draft. Its
former request shape, response vocabulary, integration map, and execution
authority wording no longer define the repository contract.

Use these current sources instead:

- `README.md` for the supported v3.2.0 overview;
- `SECURITY.md` for the fail-closed and authority boundary;
- `docs/v3/GUARDIAN_V3.md` for the current v3 request and verdict contract;
- `docs/v3/MANIFEST.md` for the v3.2.0 identity and registry lock;
- `docs/v3/RELEASE_STATUS_v3.2.0.md` for release status; and
- `docs/v4/CONTRACT.md` for Shield v4 component evidence.

If this historical notice conflicts with current code, tests, or the listed
documents, the current sources control.

## Correct authority boundary

Guardian Wallet evaluates wallet intent and verified authentication context. It
returns deterministic, fail-closed risk or component verdict evidence.

Guardian output is not authoritative for user execution. Guardian Wallet does
not:

- sign or broadcast DigiByte transactions;
- hold, derive, or access wallet private keys;
- execute wallet actions;
- change DigiByte consensus;
- create a Shield Orchestrator receipt;
- override Shield verification; or
- approve AdamantineOS execution.

Shield v4 cryptographic adapters sign Guardian component evidence only. That
must not be described as transaction signing or wallet-key custody.

The Shield Orchestrator consumes component evidence and produces the Shield
receipt. AdamantineOS independently verifies that evidence and remains the final
fail-closed policy and execution boundary.

## Historical status

The former draft used stale `intent` and `risk_context` request fields and
`ALLOW`, `WARN`, `BLOCK`, and `ERROR` response labels. Those shapes are not the
current v3 contract and must not be implemented from this file.

Tests and the current authoritative contract documents define present
behavior. This file grants no execution, approval, bypass, rescue, or signing
authority.
