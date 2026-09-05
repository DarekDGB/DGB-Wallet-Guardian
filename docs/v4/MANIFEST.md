# Wallet Guardian Shield v4 Manifest and Trust Profile

Status: controlled `4.0.0` release candidate; not released or tagged
Author attribution: DarekDGB

## Distribution

```text
project: dgb-wallet-guardian
distribution_version: 4.0.0
candidate_tag: v4.0.0
release_authorized: no
```

Distribution metadata is not a protocol identifier.

## Component identity

```text
name: DGB Wallet Guardian
component_id: guardian_wallet
component_role: shield_component_guardian_wallet
contract_version: 4
schema_version: shield.verdict.v2
```

## Frozen profiles

```text
canonicalization_profile: shield-v4-canon.v1
signature_policy: policy.v1
signature_bundle_schema: shield.signature_bundle.v1
key_registry_schema: shield.key_registry.v1
```

The `4.0.0` version alignment changes none of these identities and changes no
v3 compatibility identity.

## Signature policy

Required paths:

```text
classical-ed25519 -> rfc8032-ed25519-v1
ml-dsa            -> fips204-ml-dsa-65-v1
```

Optional-last path:

```text
fn-dsa -> fips206-draft-falcon1024-v1
```

Both required paths must verify. Optional FN-DSA may be absent; if present it
must verify and cannot replace or rescue a required path. The Falcon-1024
profile is draft evidence, not final FIPS 206 proof. Received bundles are not
repaired or reordered.

## Trust entry schema

Each Wallet Guardian trust entry requires:

```text
role
key_id
key_version
algorithm
not_before
not_after
status
public_key
```

Only `shield_component_guardian_wallet` is valid. The algorithm remains
separate from the role. Wrong-role, unknown, revoked, expired, not-yet-valid,
wrong-algorithm, or malformed entries fail closed.

## Real backend mapping

```text
Shield ml-dsa -> liboqs ML-DSA-65
Shield fn-dsa -> liboqs Falcon-1024
```

The provider is lazy and optional. No hard liboqs dependency or production-key
claim is added. Real material uses strict unpadded `b64u:` encoding and
TEST-ONLY material is rejected before provider invocation.

## Evidence-only boundary

Wallet Guardian does not sign or broadcast transactions, hold wallet keys,
modify consensus, approve execution, produce the final Shield receipt, bypass
the Orchestrator, or override AdamantineOS. AdamantineOS remains the final
fail-closed policy and execution boundary.

## Frozen evidence fixtures

```text
tests/fixtures/v4/component_verdict_policy_v1_kat.json
SHA-256: 176d9d8f7d16be456f2bf783c3031b65c46fd5f9efed1aba89d216b98406b0ff

tests/fixtures/v4/fn_dsa_signed_message_draft_profile_kat.json
SHA-256: b799b963cb46ccf579a0380cffeecd81f99fa616267e6d69fec4f2bf06e9f6ef
```

These fixtures are deterministic TEST-ONLY evidence. They do not claim
production keys or native-provider execution.
