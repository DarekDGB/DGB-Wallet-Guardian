# Wallet Guardian Shield v4 Proof Pack

Status: V4.10-E2 controlled `4.0.0` release candidate; not released or tagged
Author attribution: DarekDGB

## Authenticated source

```text
repository: DGB-Wallet-Guardian
commit: d22268540412e42de962306ba63959875fea0d85
git tree: 2524519e576b46c5ac0d19e4fa1149bbfc753c22
fresh ZIP: DGB-Wallet-Guardian-main(20260812-060639).zip
fresh ZIP SHA-256: e96d270dac5f6987b378ebcf83d1fd5f4807a483b04cb6228ae18302fb8229fb
archive inventory: 83 files, 16 directories, 99 entries
```

The archive comment matches the authenticated commit. CRC, root, path,
traversal, and backslash checks passed before modification.

## Version alignment

The distribution and active top-level runtime candidate are `4.0.0`; the
candidate tag name is `v4.0.0`. No tag is created or authorized here.

Frozen protocol and compatibility identities remain:

```text
v3 contract: 3
v3 package compatibility field: 3.2.0
v3 schema: shield.verdict.v1
v4 contract: 4
v4 schema: shield.verdict.v2
v4 canonicalization: shield-v4-canon.v1
v4 policy: policy.v1
v4 signature bundle: shield.signature_bundle.v1
v4 key registry: shield.key_registry.v1
v4 role: shield_component_guardian_wallet
```

## Signature evidence

| Path | Requirement | Profile | Evidence |
|---|---|---|---|
| `classical-ed25519` | required first | `rfc8032-ed25519-v1` | deterministic contract and negative tests |
| `ml-dsa` | required second | `fips204-ml-dsa-65-v1` | deterministic contract plus guarded ML-DSA-65 node |
| `fn-dsa` | optional last | `fips206-draft-falcon1024-v1` | deterministic contract plus guarded Falcon-1024 node |

Both required paths use strict AND semantics. Optional FN-DSA cannot replace or
rescue either required path. Present-invalid optional evidence is fatal.
Falcon-1024 remains draft evidence, not final FIPS 206 proof.

The producer emits canonical order without mutating caller input. The verifier
rejects noncanonical received order before trust lookup or crypto verification.

## Frozen KAT evidence

```text
tests/fixtures/v4/component_verdict_policy_v1_kat.json
SHA-256: 176d9d8f7d16be456f2bf783c3031b65c46fd5f9efed1aba89d216b98406b0ff

tests/fixtures/v4/fn_dsa_signed_message_draft_profile_kat.json
SHA-256: b799b963cb46ccf579a0380cffeecd81f99fa616267e6d69fec4f2bf06e9f6ef
```

These bytes remain unchanged by V4.10-E2.

## Test evidence

Authenticated baseline:

```text
standard collection: 210 passed, 2 approved native-OQS skips
Wallet Guardian statements: 1,333 / 1,333
statement coverage: 100 percent
```

Candidate-package evidence:

```text
Python: 3.11.15
standard suite: 220 passed, 2 approved native-OQS skips
Wallet Guardian statements: 1,333 / 1,333
statement coverage: 100 percent
V4.10-E2 release-pack lock: 10 passed
```

The required post-commit proof is standard CI green across the committed
Python 3.10, 3.11, and 3.12 matrix; the dedicated real-OQS workflow green with
tests=2, skipped=0, failures=0, and errors=0; and a fresh exact-scope ZIP.

## Authority proof

No path grants transaction signing, broadcast, consensus, wallet-key custody,
Orchestrator-receipt authority, AdamantineOS bypass, or final execution
authority. Wallet Guardian signs or verifies only its component decision
evidence. AdamantineOS remains the final fail-closed policy and execution
boundary.

## Residuals

- The native workflow fetches liboqs and liboqs-python from floating default
  branches.
- Workflow actions retain mutable major tags.
- Both workflows use mutable `ubuntu-latest` runner images.
- Workflow installation resolves unpinned pip, setuptools, wheel, pytest,
  pytest-cov, and editable build or test dependencies.
- Standard CI enforces statement, not branch, coverage.
- Native provider tests use test keys and do not prove production custody or
  HSM assurance.
- FN-DSA/Falcon-1024 is a draft-profile path.

These residuals remain visible release inputs.

## Tag rule

Do not create or move `v4.0.0` based on this proof pack. Only an explicit
DarekDGB release decision after the complete V4.10 roadmap may authorize that
action.
