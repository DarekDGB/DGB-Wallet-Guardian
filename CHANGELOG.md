# Changelog — DGB Wallet Guardian

All notable changes to this project are documented here.

## v3.2.0 — Manifest / Verdict / Receipt Lock

- Added Shield v3.2.0 manifest documentation under `docs/v3/`.
- Added reason ID and evidence family registries.
- Added canonical verdict or Orchestrator receipt validation code with negative-first fail-closed tests.
- Preserved 100% coverage gate.
- Locked AdamantineOS boundary language: Shield is consumed only through the deterministic Orchestrator receipt.

## v3.1.0 — Shield Hardening Release

### Added

- Deterministic Guardian v3 hardening tests for previously uncovered safety paths.
- Coverage tests for invalid modes, parser exception fail-closed handling, non-dict contexts, oversized / unserialisable payloads, Q-ID validation, Sentinel escalation, device mismatch escalation, Guardian Engine HIGH / CRITICAL severity paths, normalization helpers, and explicit safety fallbacks.

### Changed

- Package version updated from `3.0.0` to `3.1.0`.
- CI coverage gate raised to `--cov-fail-under=100`.
- README updated to describe the v3.1.0 hardening status and verified 100% coverage proof.
- Security policy updated to identify v3.1.0 as the current hardened release.
- Q-ID integration document updated to target Guardian Wallet `v3.1.0`.

### Verification

```text
89 passed
TOTAL 526 statements, 0 missed
Coverage 100.00%
```

### Security posture

Guardian Wallet v3.1.0 remains deterministic, fail-closed, non-signing, non-broadcasting, and contract-bound.
No release is considered locked unless CI proves 100% coverage.

## v3.0.0 — Stable Shield Contract v3 Baseline

- Stable Guardian Wallet v3 contract baseline.
- Deterministic `tx` and `qid_auth` evaluation paths.
- Stable reason-code behavior and canonical context hashing.
- Fail-closed request validation.
