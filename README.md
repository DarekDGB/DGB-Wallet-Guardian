# 🛡️ DGB Wallet Guardian

[![Guardian Tests](https://github.com/DarekDGB/DGB-Wallet-Guardian/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/DarekDGB/DGB-Wallet-Guardian/actions/workflows/tests.yml)
![Python](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Shield Contract](https://img.shields.io/badge/Shield%20Contract-v3-red)
![Security](https://img.shields.io/badge/security-fail--closed-critical)

---

## Overview

**DGB Wallet Guardian** is the **user-side protection layer** of the DigiByte Quantum Shield.

It enforces **Shield Contract v3** rules at the wallet boundary, ensuring that **no transaction, signing request, or sensitive wallet action** can bypass security checks — even if the wallet UI, plugins, or integrations are compromised.

This module is designed to be:
- **Fail-closed**
- **Deterministic**
- **Bypass-resistant**
- **Maintainer-safe**
- **Integration-safe for Adamantine Wallet OS**

---

## Core Principles (v3)

- **Fail-Closed by Default**  
  Any invalid, malformed, ambiguous, or unexpected input results in `ERROR`.

- **Deterministic Responses**  
  Identical inputs always produce identical outputs (including `context_hash`).

- **Strict Contract Parsing**  
  Unknown keys, invalid enums, invalid versions → hard reject.

- **No Implicit Trust**  
  UI, plugins, extensions, and maintainers are treated as untrusted.

- **User Sovereignty**  
  Guardian protects users even from buggy or malicious wallet updates.

---

## What Guardian v3 Protects Against

- Malicious or compromised wallet updates
- Plugin-based signing abuse
- Transaction manipulation
- Replay and escalation attempts
- Silent bypass paths
- Maintainer or supply-chain attacks

Guardian v3 ensures **no one — including the wallet maintainer — can steal user funds**.

---

## Architecture Position

```
User Action
   ↓
Wallet UI / Client
   ↓
🛡️ Wallet Guardian (v3)
   ↓
EQC → WSQK → Shield Runtime
   ↓
Blockchain
```

---

## Documentation

### v3 (Active)
- `docs/v3/GUARDIAN_V3.md`
- `docs/v3/technical-spec-guardian-v3.md`
- `docs/v3/guardian_attack_scenarios_v3.md`

### v2 (Archived)
- `docs/v2/` (reference only)

---

## Testing & CI

- Pytest-based test suite
- Enforced fail-closed behavior
- Deterministic hashing tests
- CI runs on Python 3.10 / 3.11 / 3.12

---

## Security

See [SECURITY.md](SECURITY.md) for vulnerability reporting and disclosure policy.

---

## License

MIT License — see [LICENSE](LICENSE)

---

**Status:** 🔒 Guardian Wallet v3 — **LOCKED & ENFORCED**
