# Wallet Guardian Shield v4 Component Verdict Contract

Status: controlled `4.0.0` release candidate; not released or tagged
Author attribution: DarekDGB

## Scope

This document defines the Wallet Guardian Shield v4 component-verdict
contract. It is parallel to the frozen v3 compatibility surface. The
distribution-version bump changes no protocol or schema identity.

## Authority boundary

Wallet Guardian produces user-protection component decision evidence only. It
does not sign or broadcast DigiByte transactions, hold wallet keys, change
consensus, approve spending or execution, produce the final Shield receipt,
bypass the Shield Orchestrator, or override AdamantineOS.

The Shield Orchestrator verifies Wallet Guardian evidence. AdamantineOS remains
the final fail-closed policy and execution boundary.

## Frozen identities

```text
component_id: guardian_wallet
component_role: shield_component_guardian_wallet
contract_version: 4
schema_version: shield.verdict.v2
canonicalization_profile: shield-v4-canon.v1
signature_policy: policy.v1
signature_bundle_schema: shield.signature_bundle.v1
key_registry_schema: shield.key_registry.v1
```

## Signed payload

The domain-separated canonical payload contains:

```text
component_id
contract_version
schema_version
request_id
context_hash
freshness_nonce
not_before
not_after
decision
reason_ids
evidence_hash
evidence_families
metadata
fail_closed
canonicalization_profile
signature_policy
key_registry_version
```

The bundle and `signed_payload_hash` are outside the payload they sign. The
component domain is:

```text
DGB-SHIELD-V4-COMPONENT-VERDICT:shield.verdict.v2:policy.v1
```

A Wallet Guardian signature cannot verify as an Orchestrator receipt signature
or transaction signature.

## Signature policy

`policy.v1` requires strict AND verification in canonical order:

```text
classical-ed25519
ml-dsa
fn-dsa                    optional and last only
```

A producer canonicalizes supported caller entries without mutation or
aliasing. A verifier never repairs or sorts a received bundle. Reversed,
interleaved, optional-first, duplicated, or unknown entries fail before trust
lookup or cryptographic verification.

Optional FN-DSA may be absent. If present, it must verify and cannot replace or
rescue either required path.

## Profiles

```text
classical-ed25519 -> rfc8032-ed25519-v1
ml-dsa            -> fips204-ml-dsa-65-v1
fn-dsa            -> fips206-draft-falcon1024-v1
```

The profile is authenticated inside the real-signature input. Falcon-1024 is
optional draft evidence, not final FIPS 206 proof.

## Trust profile and key separation

Only role `shield_component_guardian_wallet` is valid for this component.
Trust entries bind role, algorithm, key ID, key version, status, validity
window, and public key. Unknown, revoked, expired, not-yet-valid, wrong-role,
wrong-algorithm, or mismatched entries fail closed.

The verifier controls trust. Caller-supplied metadata cannot grant authority.

## Real backend

The backend-neutral adapter accepts reviewed implementations without adding a
hard provider dependency. Optional liboqs adapters map `ml-dsa` to
`ML-DSA-65` and `fn-dsa` to `Falcon-1024`.

Real public keys and signatures use strict unpadded
`b64u:<base64url-bytes>` encoding. TEST-ONLY IDs, keys, or private references
are rejected at the real-backend boundary. Missing providers, disabled or
wrong mechanisms, malformed material, native exceptions, and non-boolean
verifier results fail closed. There is no fallback to deterministic test
signatures.

The repository does not add a production classical Ed25519 backend. A
production deployment must satisfy both required paths through reviewed
providers.

## Required rejection behavior

Reject missing required signatures, noncanonical order, duplicates,
unsupported algorithms or profiles, required-path rescue, role or key
mismatch, revoked or out-of-window keys, context or payload mutation,
freshness or request mutation, forbidden authority metadata, malformed
canonical or binary material, deterministic TEST-ONLY material at a real
boundary, and all backend exceptions.

## Proof boundary

Standard CI proves deterministic and fail-closed contract behavior with 100
percent statement coverage. The dedicated workflow must run the exact native
ML-DSA-65 and Falcon-1024 nodes with tests=2, skipped=0, failures=0, and
errors=0.

Native proof uses test keys. It does not establish production custody, HSM
assurance, provider hardening, transaction signing, or final FIPS 206
conformance.
