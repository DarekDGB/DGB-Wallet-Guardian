# Wallet Guardian Shield v4.0.0 Release Status

Status: CONTROLLED PRE-RELEASE
Release decision: NOT YET AUTHORIZED
Distribution version: 4.0.0
Runtime version: 4.0.0
Candidate tag: v4.0.0
Tag created: no
Author attribution: DarekDGB

## Current state

V4.10-E2 aligns the Wallet Guardian distribution, active top-level runtime
version, and release pack to the coordinated Shield `4.0.0` candidate. It does
not announce a release and does not authorize a tag.

The candidate preserves the frozen v3 compatibility surface and all v4
protocol identities. Other than the active `__version__` string, this package
changes release truth, documentation, and regression locking only. It does not
modify cryptographic behavior, schemas, trust profiles, workflow behavior, or
KATs. The standard workflow's stale `(v3)` display suffix is removed; every
trigger, job, matrix, action, and command remains unchanged.

## Candidate controls

- Required classical Ed25519 and ML-DSA paths remain strict AND.
- Optional FN-DSA/Falcon-1024 remains optional-last draft evidence.
- Optional evidence cannot replace or rescue either required path.
- Canonical signature order is enforced before trust or crypto work.
- Trust remains role-separated to `shield_component_guardian_wallet`.
- Shared component and FN-DSA KAT fixture bytes remain frozen.
- Standard CI requires 100 percent statement coverage.
- Dedicated real-OQS proof requires exactly two native nodes with zero skips,
  failures, or errors.

The exact policy order is `classical-ed25519`, `ml-dsa`, then optional
`fn-dsa` under `fips206-draft-falcon1024-v1`. Optional FN-DSA cannot replace
or rescue either required path and is not final FIPS 206 proof.

## Authority boundary

Wallet Guardian does not sign or broadcast transactions, hold wallet keys,
change DigiByte consensus, approve execution, produce the final Shield
receipt, bypass the Shield Orchestrator, or override AdamantineOS.

AdamantineOS remains the final fail-closed policy and execution boundary.

## Remaining roadmap gates

V4.10-E2: package prepared; post-commit CI, native proof, and fresh-ZIP
verification pending.
V4.10-E3: DQSN release-pack alignment pending.
V4.10-E4: Sentinel AI release-pack alignment pending.
V4.10-E5: ADN release-pack alignment pending.
V4.10-F: AdamantineOS final verifier proof pack pending.
V4.10-G: compatibility-repository release truth pending.
V4.10-H: final full-system deterministic matrix pending.
V4.10-I: final guarded real-OQS matrix pending.
V4.10-J: final negative matrix and adversarial audit pending.
V4.10-K: final hashes, attribution, and fresh-ZIP lock pending.
V4.10-L: final release decision pending.

## Release rule

Do not create or move `v4.0.0`. A green repository, a candidate version, or a
completed V4.10-E2 package is not release authorization. Only an explicit
DarekDGB decision after the complete V4.10 roadmap may authorize the tag.
