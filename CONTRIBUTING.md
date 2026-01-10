# Contributing to Guardian Wallet

**Guardian Wallet** is the *user‑side security decision layer* of the DigiByte Quantum Shield.  
It produces **deterministic, fail‑closed safety verdicts** that can power wallet UX flows  
or be consumed headlessly by orchestrators such as **Adamantine Wallet OS**.

Guardian Wallet is **not** a consensus or network layer.  
It evaluates intent and signals risk — it does **not** execute transactions.

---

## ✅ What Contributions Are Welcome

### ✔️ 1. User‑Side Protection Improvements
- clearer warnings and explanations  
- improved confirmation and escalation flows  
- safer multi‑step approval logic  
- accessibility and clarity improvements  

### ✔️ 2. Integration Enhancements
- improved QWG signal mapping  
- better ADN defence translation  
- cleaner Guardian ↔ Adamantine Wallet interactions  
- Adaptive Core signal hygiene (deterministic, auditable)

### ✔️ 3. Runtime Safeguards
- additional pre‑signing checks  
- confirmation heuristics  
- suspicious‑pattern detection logic  
- improved handling of unusual fees or amounts  

### ✔️ 4. Documentation & Structure
- diagrams  
- architectural explanations  
- step‑by‑step behaviour documentation  
- contract and determinism clarifications  

### ✔️ 5. Test Improvements
- decision‑flow simulations  
- behavioural tests for safety flows  
- regression locks for fail‑closed behaviour  

---

## ❌ What Will NOT Be Accepted

### 🚫 1. Any Attempt to Remove Safety Logic
Guardian Wallet **must never**:

- reduce safety flows  
- bypass confirmations  
- silence warnings  
- allow unsafe transactions without explanation  

Removing core protection triggers immediate rejection.

### 🚫 2. Changing Consensus or Network Behaviour
Guardian Wallet must **never**:

- validate blocks  
- change mempool rules  
- make consensus decisions  
- act as a validator  

### 🚫 3. Duplicate QWG Logic
Do **not** replicate behavioural, cryptographic, or PQC logic already inside QWG.  
Guardian Wallet focuses on **intent evaluation**, not detection.

### 🚫 4. UI‑Only Changes Without Security Impact
Purely aesthetic changes are rejected unless they improve user understanding of risk.

### 🚫 5. Black‑Box Models
All logic must be:

- transparent  
- deterministic  
- auditable  

---

## 🧱 Design Principles

1. **Fail‑Closed First**  
   If Guardian cannot prove safety, it blocks.

2. **Explain Every Warning**  
   Every escalation must be attributable to a reason code.

3. **Deterministic Behaviour**  
   Identical input must always yield identical output.

4. **Layer Separation**  
   Detection happens upstream (QWG, ADN, Sentinel).  
   Guardian evaluates intent and signals outcomes.

5. **No Hidden Authority**  
   Guardian never signs, broadcasts, or touches keys.

6. **Interoperability**  
   Guardian must remain compatible with:
   - Adamantine Wallet OS  
   - QWG  
   - ADN v2 / v3  
   - Adaptive Core  

---

## 🔄 Pull Request Expectations

A valid PR includes:

- a clear description of the change  
- explanation of its security benefit  
- updated or new tests  
- no breaking changes to contracts  
- no removal of existing protection paths  
- updated documentation if behaviour changes  

Architectural direction is reviewed by **@DarekDGB**.  
Technical implementation is reviewed via CI and regression tests.

---

## 📝 License

By contributing, you agree your contributions are licensed under the MIT License.

© 2025 **DarekDGB**
