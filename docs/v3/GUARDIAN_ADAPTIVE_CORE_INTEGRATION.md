# Guardian Wallet v3 — Adaptive Core Integration (DONE Criteria)

Status: **integration-ready**

This document defines the **single supported integration surface** between  
**Guardian Wallet v3** (producer) and **Adaptive Core v3** (consumer).

Guardian Wallet is an **event emitter**, not a callable analyzer.
Integration is **one‑way, non‑blocking, and authority‑free**.

---

## 1) Single Supported Integration Surface

Guardian Wallet supports **exactly one** Adaptive Core integration mechanism:

```text
extra_signals["adaptive_sink"]: Callable[[AdaptiveEvent], None]
```

- The sink is provided **by the caller** (e.g. wallet runtime or orchestrator).
- Guardian Wallet **never imports or instantiates Adaptive Core directly**.
- Any other integration path is **unsupported**.

---

## 2) When Events Are Emitted

Guardian Wallet emits an Adaptive Core event **only when**:

- A transaction is evaluated, AND
- The resulting `RiskLevel` is **not NORMAL**

Event emission occurs:
- **after** the Guardian decision is computed
- **before** returning the decision envelope to the caller

---

## 3) Event Semantics (Contract‑Stable)

Guardian Wallet emits a single standardized event per evaluation:

### Required Fields

| Field | Description |
|---|---|
| `layer` | Always `"guardian_wallet"` |
| `event_id` | Transaction identifier (`tx_id`) |
| `action` | `"wallet_risk_decision"` |
| `severity` | Normalized float (see mapping below) |
| `fingerprint` | Wallet or device fingerprint |
| `metadata` | Decision context (see below) |
| `created_at` | UTC timestamp |

### Severity Mapping (Normative)

| Risk Level | Severity |
|---|---|
| ELEVATED | `0.45` |
| HIGH | `0.70` |
| CRITICAL | `0.90` |

Severity values are **fixed and regression‑locked**.

---

## 4) Metadata Payload

The emitted event metadata includes:

- `risk_level` (string)
- `score` (float)
- `actions` (list of suggested actions)
- `amount` (transaction amount)
- `destination` (destination address)
- optional `user_id` (if provided)

Metadata is **diagnostic only** and MUST NOT be treated as authority.

---

## 5) Fail‑Closed Integration Rules

Guardian Wallet’s decision is **independent** of Adaptive Core.

Rules:
- If `adaptive_sink` is **not provided** → no event is emitted.
- If `adaptive_sink` **raises an exception** → the exception is swallowed.
- Guardian Wallet’s decision **MUST NOT change** based on sink behavior.

Adaptive Core has **zero authority** over Guardian Wallet outcomes.

---

## 6) What Guardian Wallet Does NOT Do

Guardian Wallet does **not**:

- wait for Adaptive Core responses
- request permission from Adaptive Core
- modify its decision based on Adaptive Core feedback
- perform retries or buffering
- persist events

Guardian Wallet only **signals**.

---

## 7) Determinism Guarantees

For identical inputs:
- the Guardian decision is identical
- the emitted event fields (excluding timestamp) are identical
- severity bands are stable
- metadata keys and values are stable

Event emission is **deterministic in structure**, not in time.

---

## 8) Regression Locks (DONE Criteria)

Integration is considered **DONE** when:

- A single integration surface exists (`extra_signals["adaptive_sink"]`)
- Events are emitted only for non‑NORMAL risk levels
- Severity bands match the mapping above
- Event emission cannot affect allow / deny outcomes
- CI tests enforce the above invariants

These conditions are already enforced by tests.

---

## 9) Final Authority Statement

This integration is **intentional, minimal, and frozen**.

Any future changes require:
- explicit contract revision
- regression tests
- CI proof

Guardian Wallet v3 → Adaptive Core integration is **COMPLETE**.
