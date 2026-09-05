# Wallet Guardian Shield v4 Real Crypto Backend

Status: controlled `4.0.0` release candidate; not released or tagged
Author attribution: DarekDGB

## Boundary

The real-backend path signs and verifies Wallet Guardian component decision evidence only.
It does not sign or broadcast DigiByte transactions, hold
wallet keys, change consensus, create the final Shield receipt, bypass the
Orchestrator, or grant AdamantineOS final authority.

It does not make Guardian Wallet a transaction signer. Component evidence
signing remains a separate, domain-bound operation.

## Algorithms and profiles

- `classical-ed25519` - required classical signature path;
- `ml-dsa` - required PQC path; ML-DSA was formerly CRYSTALS-Dilithium;
- `fn-dsa` - optional evidence path based on Falcon.

FN-DSA/Falcon-1024 remains distinct from ML-DSA.

```text
classical-ed25519 -> rfc8032-ed25519-v1       required
ml-dsa            -> fips204-ml-dsa-65-v1    required
fn-dsa            -> fips206-draft-falcon1024-v1 optional-last
```

Optional FN-DSA cannot replace or rescue either required path. Falcon-1024 is
draft-profile evidence, not final FIPS 206 proof.

## Provider mappings

The backend-neutral adapter is
`src/dgb_wallet_guardian/v4/real_crypto_backend.py`. Optional liboqs adapters
map:

```text
ml-dsa -> ML-DSA-65
fn-dsa -> Falcon-1024
```

Providers are imported only when selected. No hard liboqs dependency is added.
A missing provider, disabled or wrong mechanism, native exception, or
non-boolean verifier result fails closed.

## Frozen signature input

Every real Wallet Guardian component signature signs these LF-separated fields
with no terminal LF:

```text
DGB-SHIELD-V4-REAL-CRYPTO-SIGNATURE-INPUT
<domain_tag>
<signed_payload_hash>
<algorithm>
<standard_profile>
<key_id>
<key_version>
```

The domain is
`DGB-SHIELD-V4-COMPONENT-VERDICT:shield.verdict.v2:policy.v1`. The domain,
payload hash, algorithm, profile, key ID, and key version are authenticated in
the real-signature input. The verifier-controlled trust entry separately
enforces role, algorithm, key ID, key version, status, validity window, and
public key.

## Binary material

Real keys and signatures use strict unpadded
`b64u:<base64url-bytes>` encoding. Padding, malformed alphabet, empty bytes,
wrong length, or backend-invalid material fails closed.

Deterministic test IDs, TEST-ONLY public keys, and test-only private references
are rejected at the real-backend boundary. There is no automatic fallback to
test signatures.

## Dedicated native proof

Default CI proves interface and fail-closed behavior but not native liboqs
execution. The dedicated workflow enables both guarded nodes:

```text
tests/test_v48g_real_oqs_mldsa_backend.py::test_v48g_real_oqs_mldsa65_guardian_backend_round_trip_and_negatives
tests/test_v48h_e_real_oqs_falcon_backend.py::test_v48h_e_real_oqs_falcon1024_backend_round_trip_and_negatives
```

The current command executes the two named nodes. Its JUnit guard requires at
least two tests, both required testcase identities, skipped=0, failures=0, and
errors=0. A green native proof uses test keys and does not establish production
custody, HSM assurance, transaction signing, or provider hardening.

It is not a final FIPS 206 production proof.

## Third-party attribution

Provider-family notices belong in `THIRD_PARTY_NOTICES.md`. No third-party PQC
source is vendored unless that notice explicitly says otherwise. First-party
author attribution remains DarekDGB.
