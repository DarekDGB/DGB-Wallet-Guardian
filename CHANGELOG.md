# Changelog - DGB Wallet Guardian

All notable changes to this repository are documented here.

Tests and normative contract documents define truth. Release notes do not
grant authority or replace the controlled release gates.

## 4.0.0 Candidate - Unreleased

Status: controlled pre-release. Candidate tag: `v4.0.0`. Tag created: no.

### Added

- Added the parallel Shield v4 component-verdict, signature-bundle, and Wallet
  Guardian trust-profile surfaces.
- Added required classical Ed25519 and ML-DSA evidence under `policy.v1`.
- Added optional-last FN-DSA/Falcon-1024 draft-profile evidence with strict
  no-rescue behavior.
- Added deterministic shared KATs, real-backend adapters, and guarded native
  liboqs ML-DSA/Falcon-1024 proof nodes.
- Added the v4 proof pack, release-status record, and release-pack lock tests.

### Changed

- Aligned package metadata and the active top-level `__version__` to the
  `4.0.0` candidate.
- Preserved the v3 `PACKAGE_VERSION = "3.2.0"` compatibility identity.
- Preserved every v3 and v4 protocol, schema, and KAT identity unchanged.
- Historicized old v3.2.0 pending-tag wording without rewriting release
  history.
- Aligned active documentation with canonical bundle order and current proof
  boundaries.
- Removed the stale `(v3)` suffix from the standard workflow display name
  without changing workflow behavior.

### Security

- Required canonical order: `classical-ed25519`, `ml-dsa`, then optional
  `fn-dsa`.
- Required both classical and ML-DSA paths; optional FN-DSA cannot replace or
  rescue a required path.
- Preserved Wallet Guardian-only role and key separation.
- Preserved no transaction signing, no broadcast, no key custody, no consensus
  change, no Orchestrator bypass, and no final authority.

### Release gate

This entry does not announce a release. Remaining V4.10 component, verifier,
compatibility, full-system, adversarial, hash, attribution, fresh-ZIP, and
release-decision gates remain controlling. Only DarekDGB may authorize creation
or movement of the `v4.0.0` tag.

## v3.2.0 - Manifest / Verdict / Receipt Lock

The `v3.2.0` release and its documents are historical evidence. The checklist
below records the pre-release controls that governed that release.

- Added Shield v3.2.0 manifest, registry, canonical verdict, proof-pack, and
  test-matrix documentation.
- Preserved deterministic fail-closed behavior and 100 percent coverage.
- Locked the Orchestrator-first AdamantineOS handoff boundary.

## v3.1.0 - Shield Hardening Release

- Added deterministic Guardian v3 hardening tests for safety paths.
- Raised the CI statement-coverage requirement to 100 percent.

## v3.0.0 - Stable Shield Contract v3 Baseline

- Added the stable Guardian Wallet v3 contract baseline.
- Added deterministic transaction and Q-ID authentication evaluation paths.

Copyright 2025 DarekDGB
