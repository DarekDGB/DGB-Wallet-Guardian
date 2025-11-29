# 🛡 DigiByte Wallet Guardian v2

Status: **v2 reference implementation – experimental**  
Layer: **4 — Wallet Behaviour & Withdrawal Protection**

---

## 1. Project Intent

DigiByte Wallet Guardian v2 (**DWG v2**) is **not** a wallet, key manager, or signing engine.  
It never holds private keys, never signs transactions, and does not modify DigiByte consensus.

Instead, it is a **behavioural firewall** that sits *next to* wallet infrastructure and node software.  
Its job is to monitor **withdrawal patterns** and apply **defensive policies** such as:

- per-transaction limits  
- rolling 24h limits  
- cooldowns between withdrawals  
- emergency freeze under elevated risk  
- escalation signals to higher-level security / monitoring layers

In the full DigiByte 5-layer shield, Wallet Guardian v2 is **Layer 4**, connected to:

- **Layer 3 – ADN v2 (Autonomous Defense Node):** provides node / network risk state  
- **Adaptive Core (future):** receives behaviour fingerprints & events for long-term learning

---

## 2. What Wallet Guardian v2 *is not*

To avoid confusion:

- ❌ does **not** generate or store keys  
- ❌ does **not** sign or broadcast transactions  
- ❌ does **not** change DigiByte’s consensus rules or cryptography  
- ❌ does **not** offer financial, custodial, or regulatory guarantees

It is a **policy + decision engine** focused purely on *behaviour*:

> “Given this risk level and this withdrawal history, should this withdrawal be  
> ALLOWed, DELAYed, FREEZE the wallet, or REJECTed?”

---

## 3. Core Capabilities

At a high level DWG v2 can:

1. **Track withdrawal history**
   - per wallet / account  
   - rolling time windows (e.g. last N minutes / hours / 24h)

2. **Apply configurable policies**
   - maximum per-transaction amount  
   - maximum rolling 24h volume  
   - minimum cooldown between withdrawals  
   - optional emergency freeze rules under MEDIUM / HIGH risk

3. **Ingest external risk signals**
   - especially from **ADN v2** (Layer 3) and/or other monitoring components  
   - expected risk states: `LOW`, `MEDIUM`, `HIGH`

4. **Emit structured decisions**
   - `ALLOW` – transaction proceeds  
   - `DELAY` – soft throttle, can be retried later  
   - `FREEZE` – wallet locked until manual review or risk downgrade  
   - `REJECT` – hard block under high risk / abuse

5. **Export events to Adaptive Core**
   - freeze events  
   - persistent attempts under HIGH risk  
   - behavioural spikes, limit breaches, etc.

---

## 4. Architecture Overview

Code lives under:

```text
src/dgb_wallet_guardian/
    __init__.py
    adaptive_bridge.py
    client.py
    config.py
    decisions.py
    guardian_engine.py
    models.py
    policies.py
```

### 4.1 `guardian_engine.py` – main pipeline

- orchestrates the evaluation flow  
- consumes withdrawal events (from `client.py`)  
- loads configuration & policies  
- queries current risk state (e.g. from ADN v2)  
- returns a `Decision` object and writes logs

Typical flow:

1. Receive `WithdrawalEvent` from client / upstream caller  
2. Load relevant policy configuration  
3. Evaluate policies using recent history  
4. Combine policy result with current risk state  
5. Produce final decision (`ALLOW` / `DELAY` / `FREEZE` / `REJECT`)  
6. Log decision + reasons  
7. Export any high-value events to `adaptive_bridge.py`

### 4.2 `decisions.py`

- defines decision types and decision objects  
- encapsulates helper logic for generating consistent decisions, e.g.:

  - reason codes (`"cooldown_breach"`, `"daily_limit"`, `"high_risk_lockdown"`, etc.)  
  - optional metadata fields for future analytics

### 4.3 `policies.py`

- centralises all policy evaluation logic  
- examples:

  - `evaluate_amount_limits()`  
  - `evaluate_daily_volume()`  
  - `evaluate_cooldown()`

- returns a structured policy result that Guardian Engine can combine with risk state.

### 4.4 `models.py`

- defines data models such as:

  - `WithdrawalEvent`  
  - `Decision`  
  - internal helper structs

- keeps types consistent across the engine.

### 4.5 `config.py`

- loads configuration and policy values (e.g. from environment, files, or defaults)  
- examples:

  - `MAX_WITHDRAWAL_PER_TX`  
  - `MAX_WITHDRAWAL_24H`  
  - `COOLDOWN_MINUTES`  
  - behaviour for `MEDIUM` vs `HIGH` risk

### 4.6 `client.py`

- thin interface for upstream systems (wallet services, RPC wrappers, etc.)  
- prepares `WithdrawalEvent` objects and passes them to Guardian Engine.

### 4.7 `adaptive_bridge.py`

- provides a single, well-defined export path to the **Adaptive Core**  
- used for high-value events like:

  - wallet freezes  
  - persistent attempts after freeze  
  - repeated policy violations under elevated risk

This allows the future Adaptive Core to learn which behaviour patterns tend to precede attacks.

---

## 5. Tests

Tests live under:

```text
tests/
    test_decisions.py
    test_imports.py
    test_models.py
    test_policies.py
    test_smoke.py
```

These currently focus on:

- import / packaging sanity checks  
- model and policy behaviour  
- smoke tests for the main engine

Future work can add:

- end-to-end simulations mirroring the scenarios in  
  `docs/guardian_wallet_attack_scenario_1.md`.

GitHub Actions (see `.github/workflows/tests.yml`) run the test suite on each push.

---

## 6. Virtual Attack / Simulation Scenarios

Simulation / analysis of behaviour is documented in:

```text
docs/guardian_wallet_attack_scenario_1.md
```

Scenario **GW-SIM-001** demonstrates:

- normal behaviour under LOW risk → `ALLOW`  
- cooldown breach → `DELAY`  
- daily limit breach under elevated risk → `FREEZE`  
- persistent attempts under HIGH risk → `REJECT` + Adaptive export

These scenarios run **entirely in simulation mode** and do **not** touch real keys or funds.

---

## 7. Intended Testnet Usage

When integrated into a DigiByte testnet or sandbox environment, Wallet Guardian v2 can be wired to:

- testnet-only wallet services or RPC event streams  
- ADN v2 risk feeds (e.g. via HTTP, message bus, or direct call)  
- optional monitoring / logging infrastructure (Prometheus, ELK, etc.)

In this mode, DWG v2 acts as a **non-consensus guardrail** around existing wallet flows:

- monitoring behaviour  
- enforcing guard-rails  
- generating rich events for Sentinel / DQSN / ADN / Adaptive Core to consume

---

## 8. Security & Safety Notes

- DWG v2 should only be used with **testnet** or **heavily-sandboxed** wallets until fully reviewed.  
- It is not a replacement for proper key management, HSMs, or multi-sig.  
- It introduces additional logic and complexity; operators should carefully monitor logs and decisions.  
- All parameters (limits, cooldowns, freeze rules) **must be tuned** for the specific environment where it runs.

---

## 9. Roadmap

Planned next steps include:

1. Additional end-to-end simulation tests (multi-wallet, burst patterns, coordinated attacks).  
2. Integration tests with ADN v2 risk feeds.  
3. Exporting richer event data to Adaptive Core for replay & learning.  
4. Packaging as part of a standalone **“DigiByte Shield Testnet Bundle”** so core developers can evaluate the full 5-layer architecture in a controlled environment.

---

## 📄 License (MIT)

This project is released under the **MIT License**.

```text
MIT License

Copyright (c) 2025 DarekDGB

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 👤 Author

**Created by:**  
🛡 **DarekDGB** — DigiByte Community Builder & Quantum Shield Architect  

All code, architecture, documentation and simulations authored with the intention  
to strengthen DigiByte for the coming decade and beyond.
