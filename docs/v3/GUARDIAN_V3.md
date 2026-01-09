# Guardian Wallet — Technical Specification v3

> **Author:** DarekDGB  
> **Status:** Authoritative (v3) • Regression‑Locked  
> **Scope:** Shield Layer 4 — Guardian Wallet  
> **License:** MIT

---

## 1. Purpose

Guardian Wallet v3 is a **contract gate** that evaluates outgoing wallet intent and returns a
**deterministic, fail‑closed verdict envelope**.

It exists to:
- **observe** wallet + transaction context
- **evaluate** risk using an auditable rule engine (via the v2 engine adapter)
- **signal** allow / escalate / deny to upstream orchestrators

Guardian Wallet v3 does **not** execute, sign, broadcast, or mutate state.

---

## 2. System Boundaries (Non‑Goals)

Guardian Wallet v3 explicitly does **not**:
- hold / derive / access private keys
- sign transactions
- broadcast transactions or perform network I/O
- modify wallet balances or persistent state
- replace runtime enforcement (EQC / WSQK / Orchestrator)

This module is an **evaluator**, not an executor.

---

## 3. Public Entrypoint

The public v3 entrypoint is:

- `GuardianWalletV3.evaluate(request: Dict[str, Any]) -> Dict[str, Any]`

Consumers MUST treat:
- `outcome="deny"` as **BLOCK**
- `outcome="escalate"` as **REQUIRE EXTRA CONFIRMATION / USER ACTION**

Consumers MUST NOT call internal engine methods directly.

---

## 4. Contract Versioning

- Supported contract version: **3 only**
- Requests with any other version fail closed.

Constants:
- `CONTRACT_VERSION = 3`
- `COMPONENT = "guardian_wallet"`

---

## 5. Request Schema (Strict)

Top‑level keys (unknown keys are rejected):

| Field | Type | Required | Notes |
|---|---|---:|---|
| `contract_version` | int | ✅ | Must be `3` |
| `component` | str | ✅ | Must be `guardian_wallet` |
| `request_id` | str | ✅ | Caller‑defined identifier |
| `wallet_ctx` | object | ⛔ default `{}` | Strict allowlist |
| `tx_ctx` | object | ⛔ default `{}` | Strict allowlist |
| `extra_signals` | object | ⛔ default `{}` | Strict allowlist |

Nested allowlists:

`wallet_ctx` allowed keys:
- `balance`
- `typical_amount`
- `wallet_age_days`
- `tx_count_24h`

`tx_ctx` allowed keys:
- `to_address`
- `amount`
- `fee`
- `memo`
- `asset_id`

`extra_signals` allowed keys:
- `device_fingerprint`
- `sentinel_status`
- `geo_ip`
- `session`
- `trusted_device`

---

## 6. Deterministic Abuse Caps

- Requests larger than **128KB** (deterministic encoded size) fail closed.
- Size is computed via canonical JSON encoding (sorted keys, compact separators, UTF‑8).

Constant:
- `MAX_PAYLOAD_BYTES = 128_000`

---

## 7. Bad Number Rules (NaN/Inf)

Numeric fields used by the gate MUST be finite.
If any are `NaN`, `+Inf`, or `-Inf`, the request fails closed.

Checked fields:
- `wallet_ctx.balance`
- `wallet_ctx.typical_amount`
- `wallet_ctx.wallet_age_days`
- `wallet_ctx.tx_count_24h`
- `tx_ctx.amount`
- `tx_ctx.fee`

---

## 8. Evaluation Flow (Normative)

1) Parse request via `GWv3Request.from_dict` (strict top‑level validation).
2) Enforce `contract_version == 3` and `component == "guardian_wallet"`.
3) Enforce payload size cap.
4) Enforce nested allowlists (`wallet_ctx`, `tx_ctx`, `extra_signals`).
5) Enforce finite number rules.
6) Evaluate risk using the **v2 engine via adapter**:
   - `WalletGuardian.evaluate_transaction(...)`

**Adapter rule (compatibility / safety):**
- v3 may allow additional context keys that the v2 dataclasses do not accept.
- The adapter MUST filter `wallet_ctx` / `tx_ctx` to the v2 model fields before construction.
- This prevents runtime TypeErrors and preserves fail‑closed semantics at the v3 layer.

---

## 9. Outcome Mapping

Risk level → outcome:

- `RiskLevel.NORMAL` → `outcome="allow"`
- `RiskLevel.ELEVATED` → `outcome="escalate"`
- `RiskLevel.HIGH` / `RiskLevel.CRITICAL` → `outcome="deny"`

---

## 10. Response Envelope (v3)

Guardian Wallet v3 returns:

- `contract_version` (always `3`)
- `component` (always `guardian_wallet`)
- `request_id` (echoed)
- `context_hash` (deterministic SHA‑256)
- `outcome` (`allow` | `escalate` | `deny`)
- `risk.level` (engine level)
- `risk.score` (float)
- `reason_codes` (stable codes + extracted rule IDs)
- `evidence.actions` / `evidence.reasons` (diagnostic)
- `meta.fail_closed` (always `true`)
- `meta.latency_ms` (deterministic `0` in reference implementation)

---

## 11. Reason Codes (Stability Rules)

Reason codes are **stable identifiers**. Consumers MUST NOT rely on human strings.

Rules:
- The first code is always the stable **outcome code**:
  - `GW_OK_HEALTHY_ALLOW`
  - `GW_ESCALATE_ELEVATED`
  - `GW_DENY_HIGH_OR_CRITICAL`
- Additional codes are extracted rule IDs from engine reasons:
  - parsed from strings like `"RULE_ID: description"`
  - de‑duplicated and lexicographically sorted for determinism

Error paths emit a single stable error code, e.g.:
- `GW_ERROR_SCHEMA_VERSION`
- `GW_ERROR_INVALID_REQUEST`
- `GW_ERROR_UNKNOWN_TOP_LEVEL_KEY`
- `GW_ERROR_UNKNOWN_WALLET_KEY`
- `GW_ERROR_UNKNOWN_TX_KEY`
- `GW_ERROR_UNKNOWN_SIGNAL_KEY`
- `GW_ERROR_OVERSIZE`
- `GW_ERROR_BAD_NUMBER`

---

## 12. Context Hash (Deterministic)

`context_hash` is computed using canonical JSON + SHA‑256.

### 12.1 Non‑Error Path Hash Payload

```json
{
  "component": "guardian_wallet",
  "contract_version": 3,
  "request_id": "<string>",
  "wallet_ctx": { ... },
  "tx_ctx": { ... },
  "extra_signals": { ... },
  "outcome": "<allow|escalate|deny>",
  "risk_level": "<NORMAL|ELEVATED|HIGH|CRITICAL>",
  "reason_codes": ["<code>", "..."]
}
```

### 12.2 Error Path Hash Payload (Fail‑Closed)

```json
{
  "component": "guardian_wallet",
  "contract_version": 3,
  "request_id": "<string>",
  "reason_code": "<error_code>"
}
```

---

## 13. Determinism Requirements (Hard)

For identical valid input:
- response envelope MUST be identical
- `context_hash` MUST be identical
- `reason_codes` ordering MUST be identical
- no time / randomness / environment can influence output

---

## 14. Required Tests (Regression Locks)

The following behaviors MUST be regression‑locked in CI:

- strict rejection of unknown top‑level keys
- strict rejection of unknown nested keys (wallet/tx/signals)
- oversize cap rejection
- NaN/Inf rejection
- deterministic `context_hash` for error paths
- deterministic output for repeated identical input
- adapter filtering prevents TypeError for v3‑allowed keys not present in v2 models

---

## 15. Final Authority Statement

**Tests define truth.**  
This specification must match the tests and the implementation.

Guardian Wallet v3 is **LOCKED** when:
- CI passes
- coverage gate passes
- all regression tests prove the invariants above

