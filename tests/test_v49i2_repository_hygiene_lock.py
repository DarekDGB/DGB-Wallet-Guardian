from __future__ import annotations

import re
import unicodedata
from pathlib import Path

from dgb_wallet_guardian import __version__
from dgb_wallet_guardian.contracts.v3_2_lock import (
    COMPONENT_ID,
    CONTRACT_VERSION,
    PACKAGE_VERSION,
    build_manifest,
)

ALLOWED_ATTRIBUTION = "DarekDGB"
CURRENT_VERSION = "3.2.0"

V2_HISTORICAL_DOCUMENTS = (
    "docs/v2/technical-spec-wallet-guardian.md",
    "docs/v2/wallet-guardian-whitepaper.md",
    "docs/v2/guardian_wallet_attack_scenario_1.md",
)

_GENERATED_DIRECTORY_NAMES = frozenset(
    {
        ".git",
        ".mypy_cache",
        ".pytest_cache",
        ".ruff_cache",
        ".tox",
        ".venv",
        "__pycache__",
        "build",
        "dist",
        "venv",
    }
)
_GENERATED_FILE_NAMES = frozenset({".coverage", "coverage.xml"})
_ATTRIBUTION_LINE = re.compile(
    r"^(?:author(?:\s+attribution)?|co-author|maintainer|"
    r"(?:ai\s+)?(?:engineering\s+)?assistant|created\s+by|developed\s+by|written\s+by)"
    r"\s*:\s*(?P<value>.+?)\s*$",
    re.IGNORECASE,
)
_STRUCTURED_ATTRIBUTION_LINE = re.compile(
    r"""^["'](?:author|author_attribution|maintainer)["']\s*:\s*"""
    r"""["'](?P<value>[^"']+)["']\s*,?\s*$""",
    re.IGNORECASE,
)
_COPYRIGHT_LINE = re.compile(
    r"^copyright\s+(?:\(c\)|\N{COPYRIGHT SIGN})\s+\d{4}(?:-\d{4})?"
    r"(?:\s+(?P<value>.+?))?\s*$",
    re.IGNORECASE,
)


def _repo_root() -> Path:
    current = Path(__file__).resolve()
    for candidate in current.parents:
        if (candidate / "pyproject.toml").is_file() and (
            candidate / "src" / "dgb_wallet_guardian"
        ).is_dir():
            return candidate
    raise AssertionError("repository root not found")


def _is_generated(path: Path, root: Path) -> bool:
    relative = path.relative_to(root)
    return (
        path.name in _GENERATED_FILE_NAMES
        or path.suffix in {".pyc", ".pyo"}
        or any(part in _GENERATED_DIRECTORY_NAMES for part in relative.parts)
        or any(part.endswith(".egg-info") for part in relative.parts)
    )


def _repository_files() -> list[Path]:
    root = _repo_root()
    return sorted(
        path for path in root.rglob("*") if path.is_file() and not _is_generated(path, root)
    )


def _display(path: Path) -> str:
    return path.relative_to(_repo_root()).as_posix()


def _text_files() -> list[tuple[Path, str]]:
    return [(path, path.read_bytes().decode("utf-8")) for path in _repository_files()]


def _known_mojibake_markers() -> tuple[str, ...]:
    codepoint_sequences = (
        (0x00C2,),
        (0x00C3,),
        (0x00E2, 0x0153),
        (0x00E2, 0x20AC),
        (0x00EF, 0x00BB, 0x00BF),
        (0x00F0, 0x0178),
    )
    return tuple(
        "".join(chr(codepoint) for codepoint in sequence) for sequence in codepoint_sequences
    )


def _plain_metadata_line(line: str) -> str:
    return line.strip().replace("*", "").replace("`", "")


def _project_metadata_text() -> str:
    return (_repo_root() / "pyproject.toml").read_text(encoding="utf-8")


def _project_version() -> str:
    match = re.search(
        r'(?m)^version\s*=\s*"(?P<value>[^"]+)"\s*$',
        _project_metadata_text(),
    )
    assert match is not None, "pyproject.toml project version not found"
    return match.group("value")


def _project_authors() -> list[str]:
    match = re.search(
        r"(?m)^authors\s*=\s*\[\{\s*name\s*=\s*"
        r'"(?P<value>[^"]+)"\s*\}\]\s*$',
        _project_metadata_text(),
    )
    assert match is not None, "pyproject.toml project authors not found"
    return [match.group("value")]


def test_repository_text_is_strict_utf8_nfc_lf_and_mojibake_free() -> None:
    failures: list[str] = []
    markers = _known_mojibake_markers()

    for path in _repository_files():
        raw = path.read_bytes()
        relative = _display(path)
        if raw and not raw.endswith(b"\n"):
            failures.append(f"{relative}: missing terminal LF")
        if raw.startswith(bytes((0xEF, 0xBB, 0xBF))):
            failures.append(f"{relative}: UTF-8 BOM")
        if bytes((0,)) in raw:
            failures.append(f"{relative}: NUL byte")
        if bytes((13,)) in raw:
            failures.append(f"{relative}: CR byte")
        try:
            text = raw.decode("utf-8", errors="strict")
        except UnicodeDecodeError as exc:
            failures.append(f"{relative}: invalid UTF-8 at byte {exc.start}")
            continue
        if text != unicodedata.normalize("NFC", text):
            failures.append(f"{relative}: text is not NFC-normalized")
        if chr(0xFFFD) in text:
            failures.append(f"{relative}: replacement character")
        if any(0x80 <= ord(character) <= 0x9F for character in text):
            failures.append(f"{relative}: C1 control character")
        if any(marker in text for marker in markers):
            failures.append(f"{relative}: known mojibake marker")

    assert failures == [], "repository text hygiene failures:\n" + "\n".join(failures)


def test_repository_author_attribution_is_darekdgb_only() -> None:
    failures: list[str] = []
    declarations = 0
    noncanonical_name = "An" + "gel"
    noncanonical_name_pattern = re.compile(
        rf"(?<!\w){re.escape(noncanonical_name)}(?!\w)", re.IGNORECASE
    )

    for path, text in _text_files():
        for line_number, line in enumerate(text.splitlines(), start=1):
            if noncanonical_name_pattern.search(line) is not None:
                failures.append(f"{_display(path)}:{line_number}: non-canonical attribution token")
                continue
            plain = _plain_metadata_line(line)
            match = _ATTRIBUTION_LINE.fullmatch(plain)
            if match is None:
                match = _STRUCTURED_ATTRIBUTION_LINE.fullmatch(plain)
            if match is not None:
                declarations += 1
                if match.group("value").strip() != ALLOWED_ATTRIBUTION:
                    failures.append(f"{_display(path)}:{line_number}: non-canonical attribution")
                continue
            copyright_match = _COPYRIGHT_LINE.fullmatch(plain)
            if copyright_match is not None and copyright_match.group("value") is not None:
                declarations += 1
                if copyright_match.group("value").strip() != ALLOWED_ATTRIBUTION:
                    failures.append(
                        f"{_display(path)}:{line_number}: non-canonical copyright owner"
                    )

    package_authors = _project_authors()
    declarations += len(package_authors)
    if package_authors != [ALLOWED_ATTRIBUTION]:
        failures.append(
            "pyproject.toml: project authors must contain only the canonical attribution"
        )

    assert declarations > 0, "no author attribution declarations found"
    assert failures == [], "author attribution lock failures:\n" + "\n".join(failures)


def test_active_version_identity_is_exactly_v3_2_0() -> None:
    manifest = build_manifest()

    assert __version__ == CURRENT_VERSION
    assert _project_version() == CURRENT_VERSION
    assert PACKAGE_VERSION == CURRENT_VERSION
    assert manifest["package_version"] == CURRENT_VERSION
    assert CONTRACT_VERSION == manifest["contract_version"] == 3
    assert COMPONENT_ID == manifest["component_id"] == "guardian_wallet"


def test_v2_documents_are_explicitly_historical_and_non_authoritative() -> None:
    root = _repo_root()

    for relative in V2_HISTORICAL_DOCUMENTS:
        text = (root / relative).read_text(encoding="utf-8")
        normalized = " ".join(text.split())
        assert "Author: DarekDGB" in text
        assert "historical" in text.casefold()
        assert "non-authoritative" in text.casefold()
        assert "not" in text.casefold() and "current" in text.casefold()
        assert "docs/v3/MANIFEST.md" in text
        assert "docs/v4/CONTRACT.md" in text
        assert (
            "AdamantineOS remains the final fail-closed policy and execution boundary" in normalized
        )


def test_superseded_v3_spec_cannot_claim_execution_authority() -> None:
    text = (_repo_root() / "docs/v3/technical-spec-guardian-v3.md").read_text(encoding="utf-8")

    stale_claim = "Guardian Wallet decisions are " + "**authoritative** for user execution."
    assert "Status: Historical and non-authoritative" in text
    assert "Guardian output is not authoritative for user execution" in text
    assert stale_claim not in text
    assert "AdamantineOS" in text
    assert "final fail-closed policy and execution boundary" in " ".join(text.split())


def test_evidence_signing_is_distinct_from_transaction_signing_and_key_custody() -> None:
    root = _repo_root()
    package_text = (root / "src/dgb_wallet_guardian/__init__.py").read_text(encoding="utf-8")
    backend_text = (root / "docs/v4/REAL_CRYPTO_BACKEND.md").read_text(encoding="utf-8")

    assert (
        "never signs or broadcasts DigiByte transactions and never holds wallet keys"
        in package_text
    )
    assert "component decision evidence only" in backend_text
    assert "It does not make Guardian Wallet a transaction signer" in backend_text


def test_real_crypto_algorithm_vocabulary_is_encoding_clean_and_exact() -> None:
    text = (_repo_root() / "docs/v4/REAL_CRYPTO_BACKEND.md").read_text(encoding="utf-8")

    assert "`classical-ed25519` - required classical signature path;" in text
    assert "`ml-dsa` - required PQC path; ML-DSA was formerly CRYSTALS-Dilithium;" in text
    assert "`fn-dsa` - optional evidence path based on Falcon." in text
    assert "FN-DSA/Falcon-1024" in text
    assert "not a final FIPS 206 production proof" in text


def test_legacy_v2_pseudo_script_remains_explicitly_non_runnable() -> None:
    legacy = (_repo_root() / "docs/v2/legacy/simulate_guardian_wallet_scenario_1.py").read_text(
        encoding="utf-8"
    )

    assert legacy.startswith("# ")
    assert "LEGACY (v2) SIMULATION SCRIPT" in legacy
    assert "NOT USED IN v3" in legacy
    assert "NOT compatible with Guardian Wallet v3 APIs" in legacy
