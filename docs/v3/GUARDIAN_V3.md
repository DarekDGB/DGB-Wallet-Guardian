# Guardian Wallet v3 — Contract Specification

**Status:** Active • Contract-Locked • Production-Grade  
**Applies to:** Shield v3 • Adamantine Wallet OS integration

Guardian Wallet v3 is the **final, auditable protection layer** between wallet intent
and execution. It enforces strict, deterministic, fail-closed safety rules for
high‑risk wallet actions.

This document is **authoritative**. Behavior described here is enforced by code and tests.

---

## Core Guarantees

Guardian Wallet v3 guarantees the following invariants:

1. **Fail‑Closed Semantics**
   - Any malformed, incomplete, or invalid request results in `DENY`.
   - No silent fallback paths exist.

2. **Deterministic Decisions**
   - Identical input → identical output.
   - No time, randomness, environment, or global state influence results.

3. **Strict Contract Parsing**
   - Unknown top‑level keys are rejected.
   - Schema violations are rejected explicitly.

4. **Explicit Reason Codes**
   - Every decision includes a stable `reason_id`.
   - Reason IDs come from a single enum source.

5. **No Hidden Authority**
   - Guardian Wallet cannot sign, mint, broadcast, or mutate wallet state.
   - It only evaluates and returns a verdict.

6. **Order Independence**
   - Input ordering does not affect the result.

---

## Non‑Goals (Explicit)

Guardian Wallet v3 **does NOT**:

- Hold or derive private keys
- Sign transactions
- Broadcast transactions
- Perform network I/O
- Modify wallet balances
- Override user consent
- Replace runtime enforcement

Guardian Wallet v3 is a **decision authority**, not an executor.

---

## Decision Model

Guardian Wallet returns a single **verdict envelope**:

- `ALLOW` — operation permitted
- `DENY` — operation blocked
- `ESCALATE` — additional confirmation / delay required

Each verdict includes:

- `schema_version = v3`
- `verdict_type`
- `reason_id`
- `context_hash` (deterministic)

---

## Invariants (Audit IDs)

- **GW_V3_INV_001** — Unknown keys rejected
- **GW_V3_INV_002** — Deterministic output for identical input
- **GW_V3_INV_003** — Fail‑closed on schema violation
- **GW_V3_INV_004** — No time or randomness dependency
- **GW_V3_INV_005** — Reason IDs from enum only
- **GW_V3_INV_006** — Order‑independent evaluation

Each invariant is enforced by regression tests in CI.

---

## Integration Rules

- Guardian Wallet v3 MUST be called through its v3 public entrypoint.
- No internal functions may be invoked directly.
- Orchestrator and Adamantine Wallet OS MUST treat the verdict as authoritative.

---

## Security Review Mode

Any change affecting Guardian Wallet v3 must include:
- Threat model update
- Regression tests
- Red‑team failure analysis

No exception.

---

## Status

Guardian Wallet v3 is **locked**.

No new features may be added without:
- Contract version bump
- Full re‑audit
- CI proof
