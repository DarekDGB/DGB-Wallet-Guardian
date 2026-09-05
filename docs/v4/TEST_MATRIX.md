# Wallet Guardian Shield v4 Test Matrix

Status: V4.10-E2 controlled release-candidate evidence
Author attribution: DarekDGB

## Standard gate

```text
pytest --cov=dgb_wallet_guardian --cov-report=term-missing --cov-fail-under=100 -q
```

The standard gate proves deterministic contracts, KATs, negative paths, and
100 percent Wallet Guardian statement coverage. The two native-OQS nodes are
approved local skips and must execute with zero skips in the dedicated
workflow.

The policy order is `classical-ed25519`, `ml-dsa`, then optional `fn-dsa`
under `fips206-draft-falcon1024-v1`. Optional FN-DSA cannot replace or rescue
either required path and is not final FIPS 206 proof.

## Contract and policy mapping

| Property | Primary evidence |
|---|---|
| Frozen v4 identities | `tests/test_v4_crypto_verdict_contract.py::test_guardian_wallet_v4_signed_component_verdict_contract_validates` |
| Required classical and ML-DSA paths | `tests/test_v4_missing_signature_fail_closed.py` |
| Optional FN-DSA absent or valid | `tests/test_v48h_fn_dsa_optional_evidence.py::test_v48h_guardian_wallet_fn_dsa_absent_allowed_and_valid_optional_evidence_recorded` |
| Optional FN-DSA cannot rescue | `tests/test_v48h_fn_dsa_optional_evidence.py::test_v48h_guardian_wallet_valid_fn_dsa_cannot_rescue_required_failure` |
| Canonical producer order | `tests/test_v48h_fn_dsa_optional_evidence.py::test_v49i2_guardian_wallet_bundle_builder_emits_canonical_order_without_mutating_input` |
| Noncanonical received order fails pre-crypto | `tests/test_v48h_fn_dsa_optional_evidence.py::test_v49i2_guardian_wallet_verifier_rejects_noncanonical_order_before_key_lookup_or_crypto` |
| Wallet Guardian role and trust separation | `tests/test_v4_crypto_verdict_contract.py` |
| Shared component KAT | `tests/test_v4_component_kat_vectors.py::test_v48g_r4_component_kat_vector_freezes_canonical_bytes_and_hash` |
| FN-DSA signed-message KAT | `tests/test_v48h_fn_dsa_signed_message_kat.py` |
| Real-backend fail-closed contract | `tests/test_v4_real_crypto_backend_contract.py` |
| ML-DSA provider contract | `tests/test_v4_oqs_mldsa_backend.py` |
| Falcon-1024 provider contract | `tests/test_v48h_e_oqs_falcon_backend.py` |
| Repository encoding and attribution | `tests/test_v49i2_repository_hygiene_lock.py` |
| Candidate release-pack truth | `tests/test_v410e2_release_pack_lock.py` |

## Negative matrix

The committed suite rejects missing required signatures, tampering, changed
context or payload hash, duplicate or unknown algorithms, reversed or
interleaved bundle order, wrong role, missing or revoked keys, invalid validity
windows, unsupported profiles, malformed canonical payloads, malformed
`b64u:` material, TEST-ONLY material at the real boundary, native provider
exceptions, non-boolean verification results, and optional-evidence rescue
attempts.

## Dedicated real-OQS gate

The workflow `.github/workflows/shield-v4-real-oqs.yml` runs exactly:

```text
tests/test_v48g_real_oqs_mldsa_backend.py::test_v48g_real_oqs_mldsa65_guardian_backend_round_trip_and_negatives
tests/test_v48h_e_real_oqs_falcon_backend.py::test_v48h_e_real_oqs_falcon1024_backend_round_trip_and_negatives
```

The current command executes the two named nodes. Its JUnit guard requires at
least two tests, both required testcase identities, skipped=0, failures=0, and
errors=0. Standard CI is not a substitute for this native proof, and the native
proof is not a claim about production keys, an HSM, transaction signing, or
final FIPS 206 conformance.

## Authority boundary

Passing these tests proves Wallet Guardian component evidence behavior only.
It grants no transaction-signing, broadcast, consensus, custody,
Orchestrator-receipt, or AdamantineOS final authority.
