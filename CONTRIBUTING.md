# Contributing to Guardian Wallet

**Guardian Wallet** is the *user-facing defence layer* of the DigiByte Quantum Shield.  
It receives structured warnings from **QWG**, defence recommendations from **ADN v2**,  
and provides clear prompts, confirmations, and protective flows for the user.

Guardian Wallet is a **security UX layer**, not a consensus or network layer.  
Contributions must strengthen *clarity, safety, and protection* without modifying  
core wallet logic or network behaviour.

---

## ✅ What Contributions Are Welcome

### ✔️ 1. User-Side Protection Improvements
- clearer warnings  
- better human-readable messages  
- improved confirmation flows  
- safer multi-step approval logic  
- accessibility and clarity improvements  

### ✔️ 2. Integration Enhancements
- improved QWG signal mapping  
- better ADN defence translation  
- richer Guardian ↔ Adamantine Wallet interactions  

### ✔️ 3. Runtime Safeguards
- additional checks before sending  
- confirmation heuristics  
- suspicious-pattern detection UX  
- improved handling of unusual fees or amounts  

### ✔️ 4. Documentation & Structure
- diagrams  
- architectural explanations  
- step-by-step behaviour documentation  

### ✔️ 5. Test Improvements
- UI prompt simulations  
- logic-flow validation  
- behavioural tests for safety flows  

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
Guardian Wallet interacts with QWG and ADN, but must **never**:

- validate blocks  
- change mempool rules  
- make consensus decisions  
- act as a validator  

### 🚫 3. Duplicate QWG Logic
Do **not** replicate behavioural or PQC logic already inside QWG.  
Guardian Wallet focuses on *UX-level protection*, not detection.

### 🚫 4. UI-Only Changes Without Security Consideration
Aesthetic changes alone are not accepted unless they improve security comprehension.

### 🚫 5. Black-Box Models
All logic must be:

- transparent  
- deterministic  
- auditable  

---

## 🧱 Design Principles

1. **User Understanding First**  
   Clear, simple, powerful messages.

2. **Explain Every Warning**  
   Users must know *why* an action is dangerous.

3. **Fail-Safe Flows**  
   When uncertain → interrupt, warn, or ask for confirmation.

4. **Layer Separation**  
   Detection happens in QWG and ADN.  
   Guardian Wallet focuses on *how users experience that protection*.

5. **Deterministic Behaviour**  
   No randomness in warnings or prompts.

6. **Interoperability**  
   Guardian’s logic must remain compatible with:

   - Adamantine Wallet  
   - QWG  
   - ADN v2  

---

## 🔄 Pull Request Expectations

A valid PR includes:

- a clear description of your change  
- explanation of its security benefit  
- updated tests or UX flows  
- no breaking changes to folder structure  
- no removal of existing protection paths  
- updated docs if needed  

The architect (@DarekDGB) reviews **direction**.  
Developers review **technical implementation**.

---

## 📝 License

By contributing, you agree your contributions are licensed under the MIT License.

© 2025 **DarekDGB**
