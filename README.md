# 🔐 DigiByte Wallet Guardian (v3.2.0)

![Python](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![CI](https://github.com/DarekDGB/DGB-Wallet-Guardian/actions/workflows/tests.yml/badge.svg)
![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen)
![Status](https://img.shields.io/badge/status-CONTRACT--LOCKED-critical)

**Shield Layer 4 • User-Side Protection Gate • Contract-Locked • v3.2.0 Integration Candidate**

Guardian Wallet is the **user-protection layer** of the DigiByte Quantum Shield.
It evaluates wallet intent, transaction context, verified Q-ID authentication facts, and external safety signals, then returns a **deterministic, fail-closed verdict** before any signing or execution can occur.

> Guardian **never signs**, **never broadcasts**, **never holds keys**, and **never becomes final AdamantineOS execution authority**.

---

## What Guardian Wallet Is

Guardian Wallet v3 is a **contract gate**, not a wallet.

It:

- evaluates wallet and transaction context
- evaluates verified Q-ID authentication facts through explicit `mode="qid_auth"`
- produces deterministic `allow`, `escalate`, or `deny` outcomes
- emits stable reason codes for orchestration and audit
- contributes evidence to the Shield Orchestrator
- supports the v3.2.0 manifest, verdict, evidence, and proof-pack lock required before AdamantineOS integration

Guardian can evaluate and signal risk, but it does **not** execute anything.

---

## What Guardian Wallet Is Not

Guardian Wallet does **not**:

- hold or derive private keys
- sign transactions
- broadcast transactions
- modify balances or chain state
- replace DigiByte Core
- bypass EQC, WSQK, Shield Orchestrator, or AdamantineOS policy
- approve AdamantineOS execution directly

Raw Guardian output is **component evidence only**. AdamantineOS must consume Shield through a deterministic Shield Orchestrator receipt.

---

## Position in the DigiByte Quantum Shield

```text
┌─────────────────────────────────────────────┐
│           Adamantine Wallet OS              │
│  consumes Shield only through receipt       │
└─────────────────────────────────────────────┘
                     ▲
                     │ deterministic Orchestrator receipt
┌─────────────────────────────────────────────┐
│        Shield Orchestrator v3.2.0           │
│  final Shield aggregation / receipt gate    │
└─────────────────────────────────────────────┘
                     ▲
                     │ component verdict evidence
┌─────────────────────────────────────────────┐
│        Guardian Wallet v3.2.0               │
│  user-side intent + auth evaluation gate    │
└─────────────────────────────────────────────┘
                     ▲
          ┌──────────┴──────────┐
          │                     │
  tx request context     Q-ID verified auth facts
```

Guardian Wallet sits **between user intent and authority**, but it remains subordinate to the Shield Orchestrator.

---

## Core Guarantees

### Fail-Closed by Design

- Malformed, invalid, oversized, unsafe, or unsupported requests return `outcome="deny"`.
- Callers must treat `deny` as **BLOCK**.
- Unknown or ambiguous authority is rejected.

### Deterministic

- Identical valid input produces identical output.
- Deterministic hashes are based on canonical JSON.
- No time, randomness, environment state, or hidden external authority may influence verdicts.

### Strict Contract

- Unsupported contract versions fail closed.
- Unknown top-level keys are rejected.
- Unknown nested keys are rejected.
- NaN and ±Inf values are rejected.

### No Hidden Authority

- Guardian can only evaluate and signal.
- Guardian cannot escalate privileges.
- Guardian cannot override the Shield Orchestrator.
- Guardian cannot approve AdamantineOS execution directly.

---

## Public API (v3)

```python
from dgb_wallet_guardian.v3 import GuardianWalletV3

gw = GuardianWalletV3()
result = gw.evaluate(request_dict)
```

Supported modes:

- `tx`
- `qid_auth`

---

## Outcome Mapping

| Risk Level | Outcome |
|---|---|
| `NORMAL` | `allow` |
| `ELEVATED` | `escalate` |
| `HIGH` / `CRITICAL` | `deny` |

---

## Contract Versioning

Supported Guardian contract version:

```text
3
```

Constants:

```text
COMPONENT = "guardian_wallet"
CONTRACT_VERSION = 3
```

Any unsupported contract version must fail closed.

---

## Q-ID Authentication Mode

Guardian Wallet v3 supports direct evaluation of verified Q-ID authentication facts.

For `mode="qid_auth"`:

- `wallet_ctx` must be empty
- `tx_ctx` must be empty
- `auth_ctx` carries verified Q-ID facts
- `extra_signals` may carry optional device or Sentinel signals

Typical auth outcomes:

- `allow` for clean verified authentication
- `escalate` for step-up conditions
- `deny` for unverified, malformed, or invalid authentication requests

See:

- `docs/v3/GUARDIAN_QID_AUTH_INTEGRATION.md`

---

## v3.2.0 Manifest / Verdict / Receipt Boundary

Guardian v3.2.0 adds the integration lock required by the Shield v3.2.0 roadmap.

This repository now includes:

- component manifest documentation
- allowed reason ID registry
- allowed evidence family registry
- canonical component verdict lock
- proof-pack documentation
- test matrix documentation
- negative tests for malformed manifest and verdict behavior

The v3.2.0 rule is strict:

```text
Guardian evidence is not final authority.
AdamantineOS must consume Shield through the deterministic Shield Orchestrator receipt only.
```

See:

- `docs/v3/MANIFEST.md`
- `docs/v3/REASON_IDS.md`
- `docs/v3/EVIDENCE_FAMILIES.md`
- `docs/v3/TEST_MATRIX.md`
- `docs/v3/PROOF_PACK.md`

---

## Deterministic Context Hash

Every Guardian response includes a `context_hash`:

- SHA-256 over canonical JSON
- stable across runs
- suitable for audit, replay checks, and orchestration
- never dependent on runtime environment, object ordering, randomness, or current time

---

## Tests & Guarantees

Guardian Wallet v3 is regression-locked with tests enforcing:

- strict schema validation
- fail-closed behavior
- deterministic hashing
- adapter safety
- `qid_auth` mode correctness
- invalid mode rejection
- parser exception fail-closed handling
- non-dict context rejection
- oversized and unserialisable payload rejection
- Q-ID auth field validation
- Sentinel escalation paths
- device mismatch escalation
- Guardian Engine HIGH / CRITICAL severity paths
- stable normalization helper behavior
- explicit unreachable safety fallbacks
- v3.2.0 manifest and canonical verdict lock behavior

The CI workflow enforces:

```bash
pytest --cov=dgb_wallet_guardian --cov-fail-under=100 -q
```

Current first-pass v3.2.0 proof:

```text
100% coverage enforced
0 missed statements required
```

Tests define truth. No release is considered locked unless CI proves the coverage gate.

---

## Release Status

Current upgrade target:

```text
v3.2.0
```

Previous stable hardening release:

```text
v3.1.0
```

Previous stable baseline:

```text
v3.0.0
```

v3.2.0 is the **manifest / verdict / receipt integration track** for AdamantineOS readiness.

Further changes require:

- contract version review
- regression tests
- CI proof
- no weakening of the 100% coverage gate
- no undocumented behavior change
- no direct AdamantineOS execution authority from raw Guardian output

---

## License

MIT License — DarekDGB 2025
