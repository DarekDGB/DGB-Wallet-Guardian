# Guardian Wallet v3 — Q-ID Auth Integration

**Status:** first stable auth-mode integration  
**Guardian Wallet release target:** `v3.0.0`

---

## Purpose

This document defines how Guardian Wallet v3 evaluates **Q-ID authentication facts** using:

- `mode = "qid_auth"`

This mode exists so that Guardian can evaluate identity/auth flows directly without forcing them into transaction semantics.

---

## Design Rule

**Q-ID auth is not a transaction.**

Therefore:

- `wallet_ctx` must be empty
- `tx_ctx` must be empty
- `auth_ctx` carries verified identity facts
- `extra_signals` carries optional device / Sentinel context

---

## Entry Point

Located in:

`src/dgb_wallet_guardian/v3.py`

Public entry remains:

```python
GuardianWalletV3().evaluate(request)
```

---

## Accepted Modes

Guardian Wallet v3 supports:

- `mode = "tx"`
- `mode = "qid_auth"`

Any other mode fails closed.

---

## `qid_auth` Request Shape

```json
{
  "contract_version": 3,
  "component": "guardian_wallet",
  "request_id": "qid-r1",
  "mode": "qid_auth",
  "wallet_ctx": {},
  "tx_ctx": {},
  "auth_ctx": {
    "qid_verified": true,
    "binding_verified": true,
    "service_id": "example.com",
    "callback_url": "https://example.com/qid",
    "nonce": "abc123",
    "address": "DGB_ADDR",
    "pubkey": "PUBKEY",
    "key_id": "primary",
    "require": "dual-proof"
  },
  "extra_signals": {
    "trusted_device": true,
    "session": "s1",
    "sentinel_status": "NORMAL"
  }
}
```

---

## `qid_auth` Decision Rules

### Allow
Guardian returns `allow` when:
- `qid_verified` is `True`
- dual-proof binding is not required, or is satisfied
- device / Sentinel signals do not require step-up

Reason code:
- `GW_OK_QID_AUTH_ALLOW`

### Escalate
Guardian returns `escalate` when:
- Sentinel status is elevated for auth context, or
- device trust signals require extra confirmation

Reason codes:
- `GW_ESCALATE_QID_UNTRUSTED_DEVICE`
- `GW_ESCALATE_QID_SENTINEL_ALERT`

### Deny
Guardian returns `deny` when:
- `qid_verified` is `False`
- dual-proof flow requires verified binding and it is missing
- request shape is invalid

Reason codes:
- `GW_DENY_QID_UNVERIFIED`
- `GW_DENY_QID_BINDING_REQUIRED`
- stable request error codes for schema failures

---

## Fail-Closed Contract Rules

For `qid_auth` mode:

- unknown top-level keys are rejected
- unknown `auth_ctx` keys are rejected
- unknown `extra_signals` keys are rejected
- malformed field types are rejected
- empty required auth fields are rejected
- `issued_at` / `expires_at` must be valid if provided

---

## Determinism

For identical valid input:
- output must be identical
- `context_hash` must be identical
- `reason_codes` ordering must be identical

Guardian Wallet v3 remains:
- deterministic
- fail-closed
- non-executing
- non-signing

---

## Responsibility Boundary

| Layer | Responsibility |
|---|---|
| Q-ID | verifies identity/auth facts |
| Guardian Wallet v3 | evaluates policy outcome for auth mode |
| upstream orchestrator / wallet OS | enforces allow / escalate / deny |

---

## Stability Statement

`qid_auth` is part of the first stable Guardian Wallet v3 public release target.

Breaking changes require:
- contract update
- regression tests
- version bump

---

**Author:** DarekDGB  
**License:** MIT
