# 🔐 DigiByte Wallet Guardian (v3)

![Python](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![CI](https://github.com/DarekDGB/DGB-Wallet-Guardian/actions/workflows/tests.yml/badge.svg)
![Coverage](https://img.shields.io/badge/coverage-%E2%89%A590%25-brightgreen)
![Status](https://img.shields.io/badge/status-CONTRACT--LOCKED-critical)

**Shield Layer 4 • User-Side Protection Gate • Contract-Locked**

Guardian Wallet is the **user-protection layer** of the DigiByte Quantum Shield.  
It evaluates outgoing wallet intent and returns a **deterministic, fail-closed verdict**
before any signing or execution can occur.

> Guardian **never signs**, **never broadcasts**, and **never touches keys**.

---

## What Guardian Wallet Is

Guardian Wallet v3 is a **contract gate**, not a wallet.

It:
- evaluates **wallet context**, **transaction context**, and **external signals**
- produces a deterministic **allow / escalate / deny** outcome
- emits **stable reason codes** for orchestration and audit
- integrates cleanly with **Sentinel AI** and **Adaptive Core**

It does **not** execute anything.

---

## What Guardian Wallet Is NOT

Guardian Wallet does **not**:
- hold or derive private keys
- sign transactions
- broadcast transactions
- modify balances or state
- replace DigiByte Core
- bypass higher-level enforcement (EQC / WSQK / Orchestrator)

---

## Position in the DigiByte Quantum Shield

```
┌─────────────────────────────────────────────┐
│           Adamantine Wallet OS               │
│  (UI, UX, signing flows, orchestration)     │
└─────────────────────────────────────────────┘
                     ▲
                     │  verdict envelope
┌─────────────────────────────────────────────┐
│        Guardian Wallet v3 (Layer 4)          │
│  User-side intent evaluation (fail-closed)  │
└─────────────────────────────────────────────┘
                     ▲
                     │  signals / context
┌─────────────────────────────────────────────┐
│        Sentinel AI & DQSN (Layer 1–3)        │
│  Network / anomaly / signal intelligence    │
└─────────────────────────────────────────────┘
                     ▲
                     │
┌─────────────────────────────────────────────┐
│           Adaptive Core (Orchestrator)       │
│  Correlation • learning • cross-layer logic │
└─────────────────────────────────────────────┘
```

Guardian Wallet sits **between UI intent and signing authority**.

---

## Core Guarantees

### ✅ Fail-Closed by Design
- Any malformed, invalid, oversized, or unsafe request returns `outcome="deny"`.
- Callers **must treat deny as BLOCK**.

### ✅ Deterministic
- Identical input → identical output → identical `context_hash`.
- No time, randomness, or environment leakage.

### ✅ Strict Contract
- Unknown top-level keys are rejected.
- Unknown nested keys are rejected.
- NaN / ±Inf values are rejected.

### ✅ No Hidden Authority
- Guardian can only evaluate and signal.
- It cannot escalate privileges or bypass enforcement.

---

## Public API (v3)

```python
from dgb_wallet_guardian.v3 import GuardianWalletV3

gw = GuardianWalletV3()
result = gw.evaluate(request_dict)
```

### Outcome Mapping

| Risk Level | Outcome |
|-----------|---------|
| NORMAL | allow |
| ELEVATED | escalate |
| HIGH / CRITICAL | deny |

---

## Contract Versioning

- **Supported version:** `3`
- Any other version → fail-closed

Constants:
- `COMPONENT = "guardian_wallet"`
- `CONTRACT_VERSION = 3`

---

## Deterministic Context Hash

Every response includes a `context_hash`:
- SHA-256 over canonical JSON
- Stable across runs
- Safe for audit, replay, and orchestration

---

## Tests & Guarantees

Guardian Wallet v3 is regression-locked with tests that enforce:
- strict schema validation
- fail-closed behavior
- deterministic hashing
- adapter safety (v3 → v2 compatibility)
- ≥90% coverage gate in CI

**Tests define truth.**

---

## Status

**Guardian Wallet v3 is COMPLETE and LOCKED.**

Further changes require:
- contract version bump
- regression tests
- CI proof

---

## License

MIT
