# Security Policy — DGB Wallet Guardian

## Supported Versions

Only **Guardian Wallet v3** is supported and security-maintained.

| Version | Supported |
|---|---|
| v3.2.0 | ✅ Yes — current integration-boundary hardening release |
| v3.1.0 | ✅ Yes — previous hardened release |
| v3.0.0 | ✅ Yes — stable v3 baseline |
| v2 | ❌ No — archived |

All legacy documentation is retained **for reference only** and is **non-authoritative**.

---

## Security Model

DGB Wallet Guardian is built under **fail-closed, deterministic, glass-box** principles.

Core guarantees:

- Deterministic inputs produce deterministic outputs.
- Explicit, stable reason codes are required.
- No silent allow paths are permitted.
- No mutable decision state is trusted.
- No hidden authority is allowed.
- Component verdicts are evidence only.
- CI must enforce the 100% coverage gate.

If Guardian cannot **prove safety**, it must **block execution**.

Guardian Wallet is a **security boundary**, not a feature layer.

---

## v3.2.0 Security Boundary

The v3.2.0 boundary locks Guardian into the Shield manifest / verdict / receipt upgrade path.

Guardian may:

- evaluate wallet intent and verified authentication context
- produce deterministic component verdict data
- emit stable reason IDs and evidence-family data
- provide evidence to the Shield Orchestrator

Guardian must never:

- sign transactions
- broadcast transactions
- hold, derive, or access private keys
- approve AdamantineOS execution directly
- override the Shield Orchestrator
- act as final authority for execution
- create hidden authority through fallback behavior

AdamantineOS must consume Shield decisions only through the deterministic **Shield Orchestrator receipt**.

Raw Guardian outputs are **not** final execution authority.

---

## Fail-Closed Requirements

The following conditions must reject deterministically:

- missing required verdict data
- malformed verdict data
- unknown fields in strict contract paths
- duplicated authority claims
- unknown reason IDs
- unknown evidence families
- mismatched component identity
- mismatched context hash
- unsafe or unserialisable input
- any ambiguity that affects authority, determinism, or auditability

A Shield `ALLOW` result only permits AdamantineOS to continue its own checks.

It is **not** final signing or execution approval.

---

## Release Requirements

No Guardian Wallet v3.2.0 release should be tagged unless all of the following are true:

- roadmap checklist is complete
- tests pass locally or in CI
- CI coverage gate remains at 100%
- manifest files are present and aligned
- reason IDs are documented and tested
- evidence families are documented and tested
- verdict boundary tests pass
- Orchestrator receipt boundary is respected
- final fresh ZIP audit is complete
- Red Team report is complete
- no docs-vs-tests mismatch remains

Tests define truth.

Documentation must never claim behavior that tests do not enforce.

---

## Reporting a Vulnerability

If you believe you have found a security issue:

1. **Do not open a public issue.**
2. Use the project’s private security contact when available.
3. Include:
   - clear description of the issue
   - steps to reproduce, if applicable
   - expected behavior
   - actual behavior
   - affected commit hash or tag
   - security impact

The project should acknowledge valid reports within **72 hours** when an active security contact is available.

---

## Responsible Disclosure

Responsible disclosure is strongly encouraged.

Coordinated fixes should be prepared and released before public disclosure whenever possible.

---

## In Scope

Security issues in scope include:

- Guardian Wallet v3 contract behavior
- determinism violations
- fail-closed bypasses
- reason ID ambiguity
- evidence-family ambiguity
- manifest/verdict mismatch
- context hash mismatch
- Orchestrator boundary bypass
- AdamantineOS raw-output bypass risk
- CI or test coverage gaps affecting security

---

## Out of Scope

The following are out of scope unless they create a direct security defect:

- UI/UX preferences
- performance tuning
- cosmetic documentation changes
- non-security refactors
- unsupported archived v2 behavior

---

## Final Security Rule

Any change that weakens determinism, fail-closed behavior, explicit authority boundaries, or the Orchestrator-first receipt model must be rejected.
