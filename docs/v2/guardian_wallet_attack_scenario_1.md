# 🛡 DigiByte Wallet Guardian v2 — Virtual Attack Scenario Report (v1)

Status: **Simulation-only, no mainnet impact**  
Layer: **4 — Wallet Behaviour & Withdrawal Protection**

---

## 1. Scenario Overview

**Scenario ID:** GW-SIM-001  
**Goal:** Validate that Wallet Guardian v2 correctly:
- tracks withdrawal frequency and size,
- respects configured limits and cooldowns,
- escalates to DELAY / FREEZE when ADN risk is elevated,
- produces a clear decision + log trail for every withdrawal.

This scenario runs entirely in **simulation mode** using the existing `dgb_wallet_guardian` engine and test harness.  
No real keys, UTXOs, or RPC connections are used.

---

## 2. Setup

### 2.1 Configuration Snapshot

Key parameters (loaded via `config.py` / `policies.py`):

- **MAX_WITHDRAWAL_PER_TX:** 5,000 DGB  
- **MAX_WITHDRAWAL_24H:** 10,000 DGB  
- **COOLDOWN_BETWEEN_TX:** 10 minutes  
- **INITIAL_ADN_RISK:** `LOW`  
- **HIGH_RISK_FREEZE_ENABLED:** `true`

These values are examples and can be adjusted in config for future testnet runs.

### 2.2 Components Under Test

- `guardian_engine.py` — main evaluation pipeline  
- `decisions.py` — ALLOW / DELAY / FREEZE decision logic  
- `policies.py` — static policy rules  
- `models.py` — data structures for withdrawals & decisions  
- `adaptive_bridge.py` — (stubbed) export to Adaptive Core

---

## 3. Simulated Timeline

We simulate a single wallet address over ~40 minutes.

| Step | Time (t) | ADN Risk | Amount (DGB) | Notes |
|------|----------|----------|--------------|-------|
| 1 | t = 0 min   | LOW      | 3,000        | First normal withdrawal |
| 2 | t = 3 min   | LOW      | 4,000        | Second tx too soon (cooldown breach) |
| 3 | t = 8 min   | MEDIUM   | 5,000        | ADN raises risk to MEDIUM |
| 4 | t = 15 min  | HIGH     | 2,500        | ADN raises risk to HIGH after external alerts |
| 5 | t = 25 min  | HIGH     | 1,000        | Wallet keeps trying small withdrawals |

The stacked behaviour is designed to cross:
- cooldown limits,
- daily limit,
- and high-risk state.

---

## 4. Engine Behaviour & Decisions

### 4.1 Withdrawal 1 — 3,000 DGB @ t=0, risk=LOW

Checks:
- amount < MAX_WITHDRAWAL_PER_TX ✅  
- 24h total after tx = 3,000 DGB < MAX_WITHDRAWAL_24H ✅  
- no previous tx → cooldown satisfied ✅  

**Decision:** `ALLOW`  
**Reason:** within limits, LOW risk, normal behaviour.  

Log example:

```text
[GW][ALLOW] addr=X...1 amount=3000 risk=LOW reason="within_limits; cooldown_ok"
```

---

### 4.2 Withdrawal 2 — 4,000 DGB @ t=3, risk=LOW

Checks:
- amount < MAX_WITHDRAWAL_PER_TX ✅  
- 24h total would be 7,000 DGB < MAX_WITHDRAWAL_24H ✅  
- last withdrawal at t=0 → cooldown (10 min) **not satisfied** ❌  

**Decision:** `DELAY`  
**Reason:** cooldown breached; user behaviour mildly suspicious but ADN risk still LOW.  

Log example:

```text
[GW][DELAY] addr=X...1 amount=4000 risk=LOW reason="cooldown_breach; soft_throttle"
```

---

### 4.3 Withdrawal 3 — 5,000 DGB @ t=8, risk=MEDIUM

ADN updates risk → `MEDIUM` (e.g., Sentinel and DQSN see unusual node / mempool patterns).

Checks:
- amount == MAX_WITHDRAWAL_PER_TX ✅  
- 24h total would be 12,000 DGB **> MAX_WITHDRAWAL_24H** ❌  
- cooldown now satisfied ✅  

**Decision:** `FREEZE` or `HARD_DELAY` (config-dependent)  
Recommended default: `FREEZE` until manual review or risk downgrade.

Log example:

```text
[GW][FREEZE] addr=X...1 amount=5000 risk=MEDIUM reason="daily_limit_exceeded; risk_elevated"
```

Adaptive bridge export (stub):

```json
{
  "wallet_id": "X...1",
  "event": "FREEZE",
  "risk_level": "MEDIUM",
  "violations": ["DAILY_LIMIT", "BEHAVIOURAL_SPIKE"],
  "timestamp": "T+8m"
}
```

---

### 4.4 Withdrawal 4 — 2,500 DGB @ t=15, risk=HIGH

ADN increases risk to `HIGH` (maybe multiple alerts from other layers).

Checks:
- wallet already frozen in previous step  
- ADN risk = HIGH → **force-protect** mode  

**Decision:** `REJECT` (hard block)  

Log example:

```text
[GW][REJECT] addr=X...1 amount=2500 risk=HIGH reason="wallet_frozen; high_risk_lockdown"
```

---

### 4.5 Withdrawal 5 — 1,000 DGB @ t=25, risk=HIGH

User keeps trying small withdrawals hoping one gets through.

Wallet Guardian sees:
- persistent attempts after freeze  
- HIGH risk unchanged  

**Decision:** `REJECT`  
**Additional action:** escalate flag to Adaptive Core as **“persistent under high risk”**.

Log example:

```text
[GW][REJECT] addr=X...1 amount=1000 risk=HIGH reason="frozen_persistent_attempts"
```

Adaptive export:

```json
{
  "wallet_id": "X...1",
  "event": "PERSISTENT_ATTEMPTS",
  "risk_level": "HIGH",
  "attempts_last_30m": 3
}
```

---

## 5. Outcome Summary

In this scenario, Wallet Guardian v2:

1. **Allows** normal behaviour under LOW risk.  
2. **Soft-throttles** suspicious timing via DELAY.  
3. **Escalates to FREEZE** when limits are exceeded under MEDIUM risk.  
4. **Hard-blocks** all withdrawals under HIGH risk once frozen.  
5. **Reports behavioural fingerprints** to the Adaptive Core for long-term learning.

This demonstrates that Wallet Guardian v2 can act as a **behavioural firewall** for DigiByte-linked wallets, even before any protocol-level PQC upgrade, and without touching private keys or consensus.

---

## 6. Next Steps for Testnet Integration

When DigiByte testnet evaluation is requested, this scenario can be:

- wired to **real (but testnet-only) wallet RPC / events**,  
- tuned with real-world thresholds,  
- combined with Sentinel / DQSN / ADN signals,  
- and replayed to validate end-to-end behaviour of the 5-layer shield.

For now, this report documents the **v1 virtual attack / stress test** for Wallet Guardian v2 in pure simulation mode.
