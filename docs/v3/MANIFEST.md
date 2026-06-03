# DGB Wallet Guardian — Shield v3.2.0 Manifest

Author attribution: DarekDGB

## Component Identity

- `component_id`: `guardian_wallet`
- `contract_version`: `3`
- `package_version`: `3.2.0`
- `output_schema_version`: `shield.verdict.v1`

## Supported Decisions

- `ALLOW`
- `ESCALATE`
- `DENY`
- `ERROR`
- `SKIPPED`

## Reason ID Registry

- `GW_OK_HEALTHY_ALLOW`
- `GW_ESCALATE_QID_REQUIRED`
- `GW_DENY_POLICY_BLOCKED`
- `GW_ERROR_INVALID_VERDICT`
- `GW_ERROR_CONTEXT_HASH_MISMATCH`

## Evidence Family Registry

- `wallet_context`
- `transaction_context`
- `qid_auth_context`
- `sentinel_signal`
- `device_signal`

## Authority Boundary

This component is evidence-only. It does not sign, broadcast, hold keys, expand authority, override the Orchestrator, or approve AdamantineOS execution directly.

## Orchestrator Role

The component verdict is input evidence only. Final Shield outcome must be produced by the Shield Orchestrator deterministic receipt.

## AdamantineOS Visibility

AdamantineOS must not consume this component directly. AdamantineOS consumes Shield only through one deterministic Orchestrator receipt.
