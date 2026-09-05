# DGB Wallet Guardian - v3.2.0 Historical Reason IDs

Author attribution: DarekDGB
Status: frozen v3 compatibility registry

Every emitted v3 reason ID was required to be declared and test-covered for
the historical v3.2.0 release. Unknown reason IDs fail closed.

- `GW_OK_HEALTHY_ALLOW`
- `GW_ESCALATE_QID_REQUIRED`
- `GW_DENY_POLICY_BLOCKED`
- `GW_ERROR_INVALID_VERDICT`
- `GW_ERROR_CONTEXT_HASH_MISMATCH`

The `4.0.0` distribution candidate does not rename or reinterpret these v3
compatibility identifiers.
