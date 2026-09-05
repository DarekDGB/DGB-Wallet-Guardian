from __future__ import annotations

import ast
import hashlib
import re
import unicodedata
from pathlib import Path

from dgb_wallet_guardian import __version__
from dgb_wallet_guardian.contracts.v3_2_lock import PACKAGE_VERSION
from dgb_wallet_guardian.v4 import (
    CANONICALIZATION_PROFILE,
    COMPONENT_ID,
    COMPONENT_ROLE,
    CONTRACT_VERSION,
    KEY_REGISTRY_SCHEMA_VERSION,
    POLICY_VERSION,
    SIGNATURE_BUNDLE_SCHEMA_VERSION,
    VERDICT_SCHEMA_VERSION,
)
from dgb_wallet_guardian.v4.trust_profile import (
    ALGORITHM_STANDARD_PROFILES,
    OPTIONAL_ALGORITHMS,
    REQUIRED_ALGORITHMS,
    SUPPORTED_ALGORITHMS,
)


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_AUTHOR = "DarekDGB"

CONTROLLED_FILES = (
    ".github/workflows/tests.yml",
    "pyproject.toml",
    "src/dgb_wallet_guardian/__init__.py",
    "README.md",
    "CHANGELOG.md",
    "SECURITY.md",
    "CONTRIBUTING.md",
    "docs/v3/PROOF_PACK.md",
    "docs/v3/REASON_IDS.md",
    "docs/v3/RELEASE_STATUS_v3.2.0.md",
    "docs/v3/technical-spec-guardian-v3.md",
    "docs/v4/CONTRACT.md",
    "docs/v4/MANIFEST.md",
    "docs/v4/REAL_CRYPTO_BACKEND.md",
    "docs/v4/TEST_MATRIX.md",
    "docs/v4/PROOF_PACK.md",
    "docs/v4/RELEASE_STATUS_v4.0.0.md",
    "tests/test_v410e2_release_pack_lock.py",
    "tests/test_v49i2_repository_hygiene_lock.py",
)

REQUIRED_V4_DOCUMENTS = (
    "docs/v4/CONTRACT.md",
    "docs/v4/MANIFEST.md",
    "docs/v4/REAL_CRYPTO_BACKEND.md",
    "docs/v4/TEST_MATRIX.md",
    "docs/v4/PROOF_PACK.md",
    "docs/v4/RELEASE_STATUS_v4.0.0.md",
)

FROZEN_FIXTURES = {
    "tests/fixtures/v4/component_verdict_policy_v1_kat.json": (
        "176d9d8f7d16be456f2bf783c3031b65c46fd5f9efed1aba89d216b98406b0ff"
    ),
    "tests/fixtures/v4/fn_dsa_signed_message_draft_profile_kat.json": (
        "b799b963cb46ccf579a0380cffeecd81f99fa616267e6d69fec4f2bf06e9f6ef"
    ),
}

REAL_OQS_NODES = (
    "tests/test_v48g_real_oqs_mldsa_backend.py::"
    "test_v48g_real_oqs_mldsa65_guardian_backend_round_trip_and_negatives",
    "tests/test_v48h_e_real_oqs_falcon_backend.py::"
    "test_v48h_e_real_oqs_falcon1024_backend_round_trip_and_negatives",
)


def _bytes(relative: str) -> bytes:
    return (ROOT / relative).read_bytes()


def _text(relative: str) -> str:
    return _bytes(relative).decode("utf-8", errors="strict")


def _project_string(field: str) -> str:
    match = re.search(
        rf'(?m)^{re.escape(field)}\s*=\s*"(?P<value>[^"]+)"\s*$',
        _text("pyproject.toml"),
    )
    assert match is not None, field
    return match.group("value")


def _project_authors() -> list[dict[str, str]]:
    match = re.search(
        r'(?m)^authors\s*=\s*\[\{\s*name\s*=\s*"(?P<value>[^"]+)"\s*\}\]\s*$',
        _text("pyproject.toml"),
    )
    assert match is not None
    return [{"name": match.group("value")}]


def test_v410e2_distribution_runtime_author_and_frozen_identities_are_locked() -> None:
    assert _project_string("version") == "4.0.0"
    assert __version__ == "4.0.0"
    assert _project_authors() == [{"name": EXPECTED_AUTHOR}]
    assert _project_string("description") == (
        "Guardian Wallet - deterministic Shield v4 user-protection evidence "
        "component for DigiByte wallets."
    )

    assert PACKAGE_VERSION == "3.2.0"
    assert COMPONENT_ID == "guardian_wallet"
    assert COMPONENT_ROLE == "shield_component_guardian_wallet"
    assert CONTRACT_VERSION == 4
    assert VERDICT_SCHEMA_VERSION == "shield.verdict.v2"
    assert CANONICALIZATION_PROFILE == "shield-v4-canon.v1"
    assert POLICY_VERSION == "policy.v1"
    assert SIGNATURE_BUNDLE_SCHEMA_VERSION == "shield.signature_bundle.v1"
    assert KEY_REGISTRY_SCHEMA_VERSION == "shield.key_registry.v1"


def test_v410e2_algorithm_order_profiles_and_role_are_locked() -> None:
    assert REQUIRED_ALGORITHMS == ("classical-ed25519", "ml-dsa")
    assert OPTIONAL_ALGORITHMS == ("fn-dsa",)
    assert SUPPORTED_ALGORITHMS == (
        "classical-ed25519",
        "ml-dsa",
        "fn-dsa",
    )
    assert ALGORITHM_STANDARD_PROFILES == {
        "classical-ed25519": ("rfc8032-ed25519-v1",),
        "ml-dsa": ("fips204-ml-dsa-65-v1",),
        "fn-dsa": ("fips206-draft-falcon1024-v1",),
    }


def test_v410e2_readme_links_complete_release_pack() -> None:
    readme = _text("README.md")
    for relative in REQUIRED_V4_DOCUMENTS:
        assert (ROOT / relative).is_file()
        assert relative in readme

    assert "controlled pre-release; not released and not tagged" in readme
    assert "Candidate tag: `v4.0.0`" in readme


def test_v410e2_frozen_kat_bytes_are_unchanged() -> None:
    proof = _text("docs/v4/PROOF_PACK.md")
    manifest = _text("docs/v4/MANIFEST.md")

    for relative, expected in FROZEN_FIXTURES.items():
        assert hashlib.sha256(_bytes(relative)).hexdigest() == expected
        assert relative in proof
        assert relative in manifest
        assert expected in proof
        assert expected in manifest


def test_v410e2_release_documents_lock_policy_and_authority_boundaries() -> None:
    documents = tuple(_text(relative) for relative in REQUIRED_V4_DOCUMENTS)
    for document in documents:
        normalized = " ".join(document.split())
        assert "classical-ed25519" in normalized
        assert "ml-dsa" in normalized
        assert "fn-dsa" in normalized
        assert "fips206-draft-falcon1024-v1" in normalized
        assert "cannot replace or rescue" in normalized
        assert "not final FIPS 206 proof" in normalized

    combined = " ".join(documents)
    for phrase in (
        "sign or broadcast",
        "consensus",
        "wallet keys",
        "Shield Orchestrator",
        "AdamantineOS remains the final",
    ):
        assert phrase in combined


def test_v410e2_real_oqs_workflow_locks_exact_two_nodes_and_no_skip_guard() -> None:
    workflow = _text(".github/workflows/shield-v4-real-oqs.yml")

    for node in REAL_OQS_NODES:
        path, function = node.split("::", maxsplit=1)
        assert path in workflow
        assert f'--require-testcase "{node}"' in workflow

        tree = ast.parse(_text(path), filename=path)
        function_names = {
            item.name
            for item in tree.body
            if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef))
        }
        assert function in function_names

    assert "--min-tests 2" in workflow
    assert 'SHIELD_V4_REAL_OQS: "1"' in workflow
    assert 'SHIELD_V4_REAL_OQS_FALCON: "1"' in workflow


def test_v410e2_historical_v3_files_are_history_not_pending_tag_instructions() -> None:
    historical = (
        "README.md",
        "CHANGELOG.md",
        "docs/v3/PROOF_PACK.md",
        "docs/v3/REASON_IDS.md",
        "docs/v3/RELEASE_STATUS_v3.2.0.md",
        "docs/v3/technical-spec-guardian-v3.md",
    )
    forbidden = (
        r"do not tag v3\.2\.0",
        r"no v3\.2\.0 tag is allowed",
        r"ready for the `v3\.2\.0`.*only after",
        r"before v3\.2\.0 tagging",
    )

    for relative in historical:
        text = _text(relative)
        assert all(
            re.search(pattern, text, flags=re.IGNORECASE | re.DOTALL) is None
            for pattern in forbidden
        )

    technical_spec = _text("docs/v3/technical-spec-guardian-v3.md")
    assert (
        "`README.md` for the active distribution and Shield v4 candidate overview"
        in technical_spec
    )


def test_v410e2_release_status_is_candidate_only() -> None:
    status = _text("docs/v4/RELEASE_STATUS_v4.0.0.md")
    expected = {
        "Status": "CONTROLLED PRE-RELEASE",
        "Release decision": "NOT YET AUTHORIZED",
        "Distribution version": "4.0.0",
        "Runtime version": "4.0.0",
        "Candidate tag": "v4.0.0",
        "Tag created": "no",
        "Author attribution": EXPECTED_AUTHOR,
    }

    for field, value in expected.items():
        matches = re.findall(
            rf"^{re.escape(field)}:\s*(.+?)\s*$",
            status,
            flags=re.IGNORECASE | re.MULTILINE,
        )
        assert matches == [value], (field, matches)

    assert "Do not create or move `v4.0.0`" in status


def test_v410e2_controlled_files_are_ascii_strict_utf8_nfc_lf() -> None:
    for relative in CONTROLLED_FILES:
        payload = _bytes(relative)
        text = payload.decode("utf-8", errors="strict")

        assert payload
        assert payload.endswith(b"\n"), relative
        assert not payload.startswith(b"\xef\xbb\xbf"), relative
        assert b"\r" not in payload, relative
        assert b"\x00" not in payload, relative
        if relative != "src/dgb_wallet_guardian/__init__.py":
            assert text.isascii(), relative
        assert text == unicodedata.normalize("NFC", text), relative
        if relative not in {
            ".github/workflows/tests.yml",
            "src/dgb_wallet_guardian/__init__.py",
        }:
            assert EXPECTED_AUTHOR in text, relative


def test_v410e2_coverage_artifacts_are_excluded_from_repository_text_scan() -> None:
    hygiene = _text("tests/test_v49i2_repository_hygiene_lock.py")
    workflow = _text(".github/workflows/tests.yml")

    assert 'path.name.startswith(".coverage.")' in hygiene
    assert '".coverage"' in hygiene
    assert workflow.startswith("name: Wallet Guardian Tests\n")
    assert "Wallet Guardian Tests (v3)" not in workflow
