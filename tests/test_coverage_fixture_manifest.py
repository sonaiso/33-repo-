"""Coverage fixture manifest quarantine tests (PR #82).

trace_ref: docs/18_COMPUTED_COVERAGE_SCHEMA_CONSTITUTION.md
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

try:
    from jsonschema.exceptions import ValidationError
except ImportError:  # pragma: no cover
    ValidationError = ValueError

from tests.test_computed_coverage_schema import _load_schema, _validate_payload


REPO_ROOT = Path(__file__).parent.parent
FIXTURES_DIR = REPO_ROOT / "tests" / "fixtures" / "coverage_cases"
MANIFEST_PATH = FIXTURES_DIR / "manifest.json"
LOCKED_DOMAINS = {"D5_IFADAH", "D6_HUKM", "D7_TANZIL"}


def _load_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def _load_manifest() -> dict[str, object]:
    return _load_json(MANIFEST_PATH)


def _all_fixture_files() -> set[str]:
    return {path.name for path in FIXTURES_DIR.glob("*.json") if path.name != "manifest.json"}


def _manifest_entries(manifest: dict[str, object], key: str) -> list[dict[str, object]]:
    return manifest.get(key, [])  # type: ignore[return-value]


def _fixture_payload(file_name: str) -> dict[str, object]:
    return _load_json(FIXTURES_DIR / file_name)


def test_manifest_exists_and_has_embargo_metadata():
    manifest = _load_manifest()
    assert MANIFEST_PATH.exists()
    assert manifest["fixture_policy"] == "SCHEMA_ONLY_AUDIT_FIXTURES"
    assert manifest["runtime_status"] == "EMBARGOED"
    assert manifest["trace_ref"] == "docs/18_COMPUTED_COVERAGE_SCHEMA_CONSTITUTION.md"


def test_manifest_lists_every_fixture_exactly_once():
    manifest = _load_manifest()
    valid_entries = _manifest_entries(manifest, "valid_fixtures")
    invalid_entries = _manifest_entries(manifest, "invalid_fixtures")
    listed_files = [entry["file"] for entry in [*valid_entries, *invalid_entries]]

    assert set(listed_files) == _all_fixture_files()
    assert len(listed_files) == len(set(listed_files))


def test_manifest_classification_prefix_rules():
    manifest = _load_manifest()
    valid_entries = _manifest_entries(manifest, "valid_fixtures")
    invalid_entries = _manifest_entries(manifest, "invalid_fixtures")

    assert valid_entries
    assert invalid_entries
    assert all(entry["file"].startswith("valid_") for entry in valid_entries)
    assert all(entry["file"].startswith("invalid_") for entry in invalid_entries)


def test_valid_manifest_fixtures_match_declared_domain_and_verdict_and_pass_schema():
    manifest = _load_manifest()
    schema = _load_schema()

    for entry in _manifest_entries(manifest, "valid_fixtures"):
        payload = _fixture_payload(entry["file"])
        assert payload["input_domain"] == entry["input_domain"]
        assert payload["expected_verdict"] == entry["expected_verdict"]
        if "expected_failure_family" in entry:
            assert payload["expected_failure_family"] == entry["expected_failure_family"]
        _validate_payload(schema, payload)


def test_invalid_manifest_fixtures_fail_schema():
    manifest = _load_manifest()
    schema = _load_schema()

    for entry in _manifest_entries(manifest, "invalid_fixtures"):
        payload = _fixture_payload(entry["file"])
        with pytest.raises((ValidationError, ValueError)):
            _validate_payload(schema, payload)


def test_locked_domain_never_accepted_in_manifest_valid_cases():
    manifest = _load_manifest()

    for entry in _manifest_entries(manifest, "valid_fixtures"):
        if entry["input_domain"] in LOCKED_DOMAINS:
            assert entry["expected_verdict"] != "EXPECTED_ACCEPTED_CANDIDATE"


def test_locked_domain_accepted_case_quarantined_as_invalid():
    manifest = _load_manifest()
    invalid_entries = {
        entry["file"]: entry["must_fail_reason"] for entry in _manifest_entries(manifest, "invalid_fixtures")
    }

    for file_name in _all_fixture_files():
        payload = _fixture_payload(file_name)
        if (
            payload.get("input_domain") in LOCKED_DOMAINS
            and payload.get("expected_verdict") == "EXPECTED_ACCEPTED_CANDIDATE"
        ):
            assert invalid_entries.get(file_name) == "LOCKED_DOMAIN_ACCEPTED_FORBIDDEN"


def test_forbidden_fields_or_rank_values_are_quarantined_in_invalid_manifest_entries():
    manifest = _load_manifest()
    invalid_entries = {
        entry["file"]: entry["must_fail_reason"] for entry in _manifest_entries(manifest, "invalid_fixtures")
    }

    for file_name in _all_fixture_files():
        payload = _fixture_payload(file_name)
        forbidden_reason = None
        if "computed_verdict" in payload:
            forbidden_reason = "COMPUTED_VERDICT_FORBIDDEN"
        elif "mrk_defaults" in payload:
            forbidden_reason = "MRK_DEFAULTS_FORBIDDEN"
        elif payload.get("rank") in {"CERTIFICATE", "Rank.CERTIFICATE"}:
            forbidden_reason = "RANK_CERTIFICATE_FORBIDDEN"

        if forbidden_reason is not None:
            assert invalid_entries.get(file_name) == forbidden_reason


def test_valid_manifest_entries_do_not_include_forbidden_fields_or_rank_values():
    manifest = _load_manifest()

    for entry in _manifest_entries(manifest, "valid_fixtures"):
        payload = _fixture_payload(entry["file"])
        assert "computed_verdict" not in payload
        assert "mrk_defaults" not in payload
        assert payload.get("rank") not in {"CERTIFICATE", "Rank.CERTIFICATE"}
