# Security Policy — DGB Wallet Guardian

## Supported Versions

Only **Guardian Wallet v3** is supported and security-maintained.

| Version | Supported |
|--------|-----------|
| v3     | ✅ Yes |
| v2     | ❌ No (archived) |

All legacy documentation is retained **for reference only** and is **non-authoritative**.

---

## Security Model

DGB Wallet Guardian is built under **fail-closed, deterministic, glass-box** principles.

Core guarantees:
- Deterministic inputs → deterministic outputs
- Explicit, stable reason codes
- No silent allow paths
- No mutable decision state
- No hidden authority
- CI-enforced invariants

If Guardian cannot **prove safety**, it **blocks execution**.

---

## Reporting a Vulnerability

If you believe you have found a security issue:

1. **Do NOT open a public issue**
2. Email: **security@dgb-guardian.local** *(replace with real address when ready)*
3. Include:
   - A clear description of the issue
   - Steps to reproduce (if applicable)
   - Expected vs actual behavior
   - Affected commit hash or tag

We aim to acknowledge valid reports within **72 hours**.

---

## Responsible Disclosure

We strongly encourage responsible disclosure.
Coordinated fixes will be released **before public disclosure** whenever possible.

---

## Scope

In-scope:
- Guardian Wallet v3 contract behavior
- Determinism violations
- Fail-closed bypasses
- Reason code ambiguity
- CI/test coverage gaps affecting security

Out-of-scope:
- UI/UX issues
- Performance tuning
- Non-security refactors

---

## Final Note

Guardian Wallet is a **security boundary**, not a feature.
Any change that weakens determinism or fail-closed behavior will be rejected.
