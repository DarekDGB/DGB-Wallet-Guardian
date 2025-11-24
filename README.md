# DGB Wallet Guardian v2

DGB Wallet Guardian v2 is the wallet-side security layer in the **5‑Layer DigiByte Quantum Shield**.
It evaluates outgoing transactions and decides whether to **ALLOW, WARN, DELAY, BLOCK, or require extra authentication**.

This system is designed to protect DigiByte users from:
- wallet draining attacks  
- phishing / new address risk  
- unusual behaviour patterns  
- high-risk network signals (Sentinel AI v2 / DQSN / ADN v2)  
- device anomalies  

---

# 🔐 Place in the 5‑Layer DigiByte Quantum Shield

1. **Sentinel AI v2** – monitors blockchain entropy, mempool, attack patterns  
2. **DQSN** – DigiByte Quantum Shield Network (global risk propagation)  
3. **ADN v2** – Autonomous Defense Node (node‑side defense automation)  
4. **🛡️ DGB Wallet Guardian v2** – *this repo*  
5. **DGB Quantum Wallet Guard** – merges wallet + device + network signals  

Wallet Guardian v2 is the layer that **stops a bad transaction before it is signed**.

---

# ✨ Features

- Rule‑based risk engine  
- Full transaction evaluation  
- Score → RiskLevel mapping  
- Clearly explained reasons for each rule match  
- Device / Sentinel / ADN integration  
- Lightweight, auditable Python implementation  
- GitHub Actions CI tests on every commit  

---

# 📦 Directory Structure

```
src/dgb_wallet_guardian/
│
├── models.py           # WalletState, DeviceState, TxContext, etc.
├── decisions.py        # GuardianDecision + GuardianResult enums
├── policies.py         # Policy rules + evaluation helpers
├── guardian_engine.py  # Core engine (rule evaluator)
├── config.py           # Thresholds & tuning parameters
└── client.py           # Optional: helper client for external apps
```

---

# 🚀 Quick Usage Example

```python
from dgb_wallet_guardian.models import WalletState, TxContext
from dgb_wallet_guardian.guardian_engine import GuardianEngine
from dgb_wallet_guardian.decisions import GuardianDecision

from datetime import datetime

engine = GuardianEngine()

wallet = WalletState(
    balance=5000.0,
    daily_sent_amount=120.0
)

tx = TxContext(
    amount=2000.0,
    destination_address="dgb1qnewaddress123",
    created_at=datetime.utcnow()
)

decision = engine.evaluate(wallet, tx)

print("Decision:", decision.decision)
print("Reason:", decision.reason)
print("Cooldown:", decision.cooldown_seconds)
```

---

# ⚙️ Configuration

Adjust thresholds inside **config.py**:

- `FULL_BALANCE_RATIO`
- `LARGE_TX_MULTIPLIER`
- `DAILY_LIMIT_MULTIPLIER`
- `COOLDOWN_SECONDS`
- `REQUIRE_2FA_THRESHOLD`

Wallet apps may override this at runtime.

---

# 🧪 Tests

Tests run automatically on GitHub Actions after every commit.

Run locally:

```
pytest
```

---

# 📄 License
MIT License — fully open source, free to use.

---

# 👑 Created by DarekDGB
Open‑source, free, for DigiByte and future generations.
