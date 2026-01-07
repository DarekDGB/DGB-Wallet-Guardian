# Guardian Wallet — Technical Specification v3

> **Author:** DarekDGB  
> **Status:** Authoritative (v3)  
> **Scope:** Guardian Wallet Layer (Shield Layer 4)  
> **License:** MIT  

---

## 1. Purpose & Scope

This document defines the **authoritative technical specification** for **Guardian Wallet v3**.

Guardian Wallet v3 is a **user-side protection layer** responsible for:
- enforcing wallet-level security policies
- mediating execution requests (send, sign, mint, burn)
- failing closed under all ambiguity
- producing deterministic, auditable decisions

This specification supersedes all previous (v1/v2) Guardian documentation.

---

## 2. Core Design Principles (Non-Negotiable)

| Principle | Description |
|---------|-------------|
| Fail-Closed | Any invalid, unknown, or malformed input results in `ERROR` |
| Determinism | Same input → same output (byte-for-byte) |
| No Hidden Authority | Guardian cannot silently allow execution |
| Glass-Box | Every decision is explainable and testable |
| Policy-Driven | No hardcoded wallet logic outside policy |
| Zero Trust | No upstream signal is trusted implicitly |

---

## 3. Contract Envelope (v3)

### Request (Logical)

```json
{
  "contract_version": 3,
  "component": "guardian_wallet",
  "request_id": "string",
  "intent": { "...": "execution intent" },
  "risk_context": { "...": "QWG signals" }
}
```

### Response (Authoritative)

```json
{
  "contract_version": 3,
  "component": "guardian_wallet",
  "request_id": "string",
  "context_hash": "sha256",
  "decision": "ALLOW | WARN | BLOCK | ERROR",
  "reason_codes": ["GW_*"],
  "meta": {
    "fail_closed": true,
    "latency_ms": 0
  }
}
```

---

## 4. Strict Parsing Rules

Guardian Wallet v3 MUST:

- Reject unknown top-level keys
- Reject missing required fields
- Reject wrong types
- Reject NaN / Infinity values
- Reject oversized payloads
- Reject invalid enums

Parsing errors MUST return:

```json
"decision": "ERROR"
```

---

## 5. Determinism Guarantees

Guardian Wallet v3 MUST NOT:

- read system time
- read randomness
- perform network I/O
- depend on execution order
- mutate shared/global state

### Context Hash

The `context_hash` is computed over:
- canonicalized request
- canonicalized policy snapshot
- canonicalized decision result

Using:
- sorted keys
- fixed encoding (UTF-8)
- SHA-256 only

---

## 6. Decision Semantics

| Decision | Meaning |
|--------|--------|
| ALLOW | Safe to execute immediately |
| WARN | User warning + cooldown |
| BLOCK | Explicitly forbidden |
| ERROR | Contract or input violation |

Guardian Wallet v3 MUST:
- never downgrade a higher-risk decision
- never auto-escalate to ALLOW
- never bypass EQC / WSQK rules

---

## 7. Reason Codes (Single Source of Truth)

All reason codes MUST:
- be stable strings
- live in a single enum
- be covered by tests

Examples:
- `GW_OK`
- `GW_POLICY_VIOLATION`
- `GW_INVALID_REQUEST`
- `GW_RISK_EXCEEDED`
- `GW_FAIL_CLOSED`

No free-form reasons are allowed.

---

## 8. Fail-Closed Invariants

Guardian Wallet v3 MUST fail closed when:

- contract_version ≠ 3
- component mismatch
- missing intent
- malformed risk context
- unknown keys
- policy evaluation errors
- internal exceptions

Fail-closed behavior is **not optional**.

---

## 9. Attack Surface & Explicit Non-Goals

### Defended Against
- malicious UI
- compromised wallet client
- replayed intents
- malformed risk signals
- downgrade attacks

### Non-Goals
- key generation
- cryptographic signing
- network validation
- chain consensus

Guardian Wallet **does not hold keys**.

---

## 10. Integration Contract

Guardian Wallet v3 integrates with:

- **QWG v3** — risk evaluation
- **DQSN v3** — network aggregation
- **ADN v3** — node defense
- **Adaptive Core v3** — learning & feedback
- **EQC / WSQK** — execution gating

Guardian Wallet decisions are **authoritative** for user execution.

---

## 11. Test Coverage Mapping

| Spec Area | Required Tests |
|---------|----------------|
| Parsing | unknown keys, bad types |
| Determinism | identical input → identical output |
| Fail-Closed | invalid input → ERROR |
| Policy | policy limits enforced |
| Reason Codes | exact enum matching |

No spec item is considered complete without tests.

---

## 12. Final Authority Statement

If code, tests, and documentation ever disagree:

> **Tests + This Specification define truth.**

Anything else is a bug.

---

**Guardian Wallet v3 is locked when all tests pass.**
