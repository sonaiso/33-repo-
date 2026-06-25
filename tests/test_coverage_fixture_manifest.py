"""Coverage fixture manifest quarantine tests (PR #82).

trace_ref: docs/18_COMPUTED_COVERAGE_SCHEMA_CONSTITUTION.md
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator
from jsonschema.exceptions import ValidationError

from taaqqul_slot_geometry.L1.domain_ids import DomainID

REPO_ROOT = Path(__file__).parent.parent
FIXTURES_DIR = REPO_ROOT / "tests" / "fixtures" / "coverage_cases"
MANIFEST_PATH = FIXTURES_DIR / "manifest.json"
SCHEMA_PATH = REPO_ROOT / "schemas" / "coverage_case.schema.json"
LOCKED_DOMAINS = {DomainID.D5_IFADAH.value, DomainID.D6_HUKM.value, DomainID.D7_TANZIL.value}
EXPECTED_FIXTURE_POLICY = "SCHEMA_ONLY_AUDIT_FIXTURES"
EXPECTED_RUNTIME_STATUS = "EMBARGOED"
EXPECTED_TRACE_REF = "docs/18_COMPUTED_COVERAGE_SCHEMA_CONSTITUTION.md"
FORBIDDEN_RANK_VALUES = {"CERTIFICATE", "Rank.CERTIFICATE"}
OUTCOME_SPECIFIC_FIELDS = {
    "expected_failure_family",
    "expected_residual_policy",
    "required_bridges",
}
VERDICT_REQUIRED_FIELDS = {
    "EXPECTED_ACCEPTED_CANDIDATE": set(),
    "EXPECTED_BLOCKED": {"expected_failure_family"},
    "EXPECTED_PROOF_REQUIRED": {"expected_failure_family"},
    "EXPECTED_RESIDUAL": {"expected_residual_policy"},
    "EXPECTED_BRIDGE_REQUIRED": {"required_bridges"},
}
# Map manifest must_fail_reason labels to expected JSON Schema error-message hints.
INVALID_REASON_HINTS = {
    "LOCKED_DOMAIN_ACCEPTED_FORBIDDEN": "EXPECTED_ACCEPTED_CANDIDATE",
    "COMPUTED_VERDICT_FORBIDDEN": "computed_verdict",
    "MRK_DEFAULTS_FORBIDDEN": "mrk_defaults",
    "BOOLEAN_PROOF_FORBIDDEN": "domain_proved",
    "RANK_CERTIFICATE_FORBIDDEN": "Rank.CERTIFICATE",
    "OUTCOME_FAILURE_FAMILY_FORBIDDEN": "expected_failure_family",
    "OUTCOME_RESIDUAL_POLICY_FORBIDDEN": "expected_residual_policy",
    "OUTCOME_REQUIRED_BRIDGES_FORBIDDEN": "required_bridges",
}


def _load_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def _load_manifest() -> dict[str, object]:
    return _load_json(MANIFEST_PATH)


def _load_schema() -> dict[str, object]:
    return _load_json(SCHEMA_PATH)


def _validate_payload(schema: dict[str, object], payload: dict[str, object]) -> None:
    Draft202012Validator(schema).validate(payload)


def _all_fixture_files() -> set[str]:
    return {path.name for path in FIXTURES_DIR.glob("*.json") if path.name != "manifest.json"}


def _manifest_entries(manifest: dict[str, object], key: str) -> list[dict[str, object]]:
    entries = manifest.get(key, [])
    if not isinstance(entries, list):
        raise ValueError(f"{key} must be a list")
    for entry in entries:
        if not isinstance(entry, dict):
            raise ValueError(f"{key} entries must be objects")
    return entries


def _fixture_payload(file_name: str) -> dict[str, object]:
    return _load_json(FIXTURES_DIR / file_name)


def _invalid_reason_map(manifest: dict[str, object]) -> dict[str, str]:
    result: dict[str, str] = {}
    for entry in _manifest_entries(manifest, "invalid_fixtures"):
        file_name = entry.get("file")
        reason = entry.get("must_fail_reason")
        if not isinstance(file_name, str) or not isinstance(reason, str):
            raise ValueError("invalid_fixtures entries must include string file and must_fail_reason")
        result[file_name] = reason
    return result


def test_manifest_exists_and_has_embargo_metadata():
    manifest = _load_manifest()
    assert MANIFEST_PATH.exists()
    assert manifest["fixture_policy"] == EXPECTED_FIXTURE_POLICY
    assert manifest["runtime_status"] == EXPECTED_RUNTIME_STATUS
    assert manifest["trace_ref"] == EXPECTED_TRACE_REF


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


def test_manifest_covers_all_schema_expected_verdict_classes():
    manifest = _load_manifest()
    schema = _load_schema()
    expected_verdicts = set(schema["properties"]["expected_verdict"]["enum"])
    observed_verdicts = {
        entry["expected_verdict"]
        for section in ("valid_fixtures", "invalid_fixtures")
        for entry in _manifest_entries(manifest, section)
        if "expected_verdict" in entry
    }
    assert expected_verdicts <= observed_verdicts


def test_manifest_quarantines_required_forbidden_patterns():
    manifest = _load_manifest()
    required_reasons = {
        "COMPUTED_VERDICT_FORBIDDEN",
        "MRK_DEFAULTS_FORBIDDEN",
        "BOOLEAN_PROOF_FORBIDDEN",
        "RANK_CERTIFICATE_FORBIDDEN",
    }
    observed_reasons = {
        entry["must_fail_reason"]
        for entry in _manifest_entries(manifest, "invalid_fixtures")
        if "must_fail_reason" in entry
    }
    assert required_reasons <= observed_reasons


def test_valid_manifest_fixtures_match_declared_domain_and_verdict_and_pass_schema():
    manifest = _load_manifest()
    schema = _load_schema()

    for entry in _manifest_entries(manifest, "valid_fixtures"):
        payload = _fixture_payload(entry["file"])
        assert payload["input_domain"] == entry["input_domain"]
        assert payload["expected_verdict"] == entry["expected_verdict"]
        if "expected_failure_family" in entry:
            assert payload["expected_failure_family"] == entry["expected_failure_family"]
        if "expected_residual_policy" in entry:
            assert payload["expected_residual_policy"] == entry["expected_residual_policy"]
        if "required_bridges" in entry:
            assert payload["required_bridges"] == entry["required_bridges"]
        _validate_payload(schema, payload)


def test_invalid_manifest_fixtures_fail_schema():
    manifest = _load_manifest()
    schema = _load_schema()

    for entry in _manifest_entries(manifest, "invalid_fixtures"):
        payload = _fixture_payload(entry["file"])
        with pytest.raises(ValidationError) as exc_info:
            _validate_payload(schema, payload)
        expected_reason = entry["must_fail_reason"]
        assert isinstance(expected_reason, str)
        hint = INVALID_REASON_HINTS[expected_reason]
        assert hint in str(exc_info.value)


def test_locked_domain_never_accepted_in_manifest_valid_cases():
    manifest = _load_manifest()

    for entry in _manifest_entries(manifest, "valid_fixtures"):
        if entry["input_domain"] in LOCKED_DOMAINS:
            assert entry["expected_verdict"] != "EXPECTED_ACCEPTED_CANDIDATE"


def test_manifest_covers_bridge_required_transition_guards():
    manifest = _load_manifest()
    required_transition_bridges = {
        "D1_DAL_ONLY": "D1_DAL_ONLY_TO_D2_LAFZI_FORM_BRIDGE",
        "D2_LAFZI_FORM": "D2_LAFZI_FORM_TO_D3_LEXICAL_MADLUL_BRIDGE",
        "D3_LEXICAL_MADLUL": "RELATION_BRIDGE",
    }
    bridge_entries = [
        entry
        for entry in _manifest_entries(manifest, "valid_fixtures")
        if entry.get("expected_verdict") == "EXPECTED_BRIDGE_REQUIRED"
    ]
    observed_by_domain = {entry["input_domain"]: entry["file"] for entry in bridge_entries}

    for input_domain, bridge_name in required_transition_bridges.items():
        assert input_domain in observed_by_domain, (
            f"missing EXPECTED_BRIDGE_REQUIRED fixture coverage for {input_domain}"
        )
        file_name = observed_by_domain[input_domain]
        payload = _fixture_payload(file_name)
        required_bridges = payload.get("required_bridges", [])
        assert bridge_name in required_bridges


def test_manifest_covers_residual_with_explicit_policy():
    manifest = _load_manifest()
    residual_entries = [
        entry
        for entry in _manifest_entries(manifest, "valid_fixtures")
        if entry.get("expected_verdict") == "EXPECTED_RESIDUAL"
    ]
    assert residual_entries
    for entry in residual_entries:
        payload = _fixture_payload(entry["file"])
        assert isinstance(payload.get("expected_residual_policy"), str)
        assert payload["expected_residual_policy"]


def test_locked_domain_accepted_case_quarantined_as_invalid():
    manifest = _load_manifest()
    invalid_entries = _invalid_reason_map(manifest)

    for file_name in _all_fixture_files():
        payload = _fixture_payload(file_name)
        if (
            payload.get("input_domain") in LOCKED_DOMAINS
            and payload.get("expected_verdict") == "EXPECTED_ACCEPTED_CANDIDATE"
        ):
            assert invalid_entries.get(file_name) == "LOCKED_DOMAIN_ACCEPTED_FORBIDDEN"


def test_forbidden_fields_or_rank_values_are_quarantined_in_invalid_manifest_entries():
    manifest = _load_manifest()
    invalid_entries = _invalid_reason_map(manifest)

    for file_name in _all_fixture_files():
        payload = _fixture_payload(file_name)
        forbidden_reason = None
        if "computed_verdict" in payload:
            forbidden_reason = "COMPUTED_VERDICT_FORBIDDEN"
        elif "mrk_defaults" in payload:
            forbidden_reason = "MRK_DEFAULTS_FORBIDDEN"
        elif payload.get("rank") in FORBIDDEN_RANK_VALUES:
            forbidden_reason = "RANK_CERTIFICATE_FORBIDDEN"

        if forbidden_reason is not None:
            assert invalid_entries.get(file_name) == forbidden_reason


def test_valid_manifest_entries_do_not_include_forbidden_fields_or_rank_values():
    manifest = _load_manifest()

    for entry in _manifest_entries(manifest, "valid_fixtures"):
        payload = _fixture_payload(entry["file"])
        assert "computed_verdict" not in payload
        assert "mrk_defaults" not in payload
        assert payload.get("rank") not in FORBIDDEN_RANK_VALUES


def test_manifest_verdict_matrix_has_positive_fixture_for_each_verdict():
    manifest = _load_manifest()
    schema = _load_schema()
    expected_verdicts = set(schema["properties"]["expected_verdict"]["enum"])
    positive_matrix_verdicts = {
        entry["expected_verdict"]
        for entry in _manifest_entries(manifest, "valid_fixtures")
        if entry.get("fixture_matrix") == "VERDICT_POSITIVE"
    }

    assert positive_matrix_verdicts == expected_verdicts


def test_manifest_verdict_matrix_positive_fixtures_use_only_their_required_outcome_fields():
    manifest = _load_manifest()

    for entry in _manifest_entries(manifest, "valid_fixtures"):
        if entry.get("fixture_matrix") != "VERDICT_POSITIVE":
            continue
        payload = _fixture_payload(entry["file"])
        verdict = payload["expected_verdict"]
        observed_outcome_fields = OUTCOME_SPECIFIC_FIELDS & set(payload)

        assert observed_outcome_fields == VERDICT_REQUIRED_FIELDS[verdict]


def test_manifest_verdict_matrix_has_negative_fixture_for_each_irrelevant_outcome_field():
    manifest = _load_manifest()
    schema = _load_schema()
    expected_verdicts = set(schema["properties"]["expected_verdict"]["enum"])
    negative_entries = [
        entry
        for entry in _manifest_entries(manifest, "invalid_fixtures")
        if entry.get("fixture_matrix") == "VERDICT_NEGATIVE"
        and entry.get("forbidden_field") in OUTCOME_SPECIFIC_FIELDS
    ]

    observed = {
        (entry["expected_verdict"], entry["forbidden_field"])
        for entry in negative_entries
    }
    expected = {
        (verdict, field)
        for verdict in expected_verdicts
        for field in OUTCOME_SPECIFIC_FIELDS - VERDICT_REQUIRED_FIELDS[verdict]
    }

    assert observed == expected


def test_manifest_verdict_matrix_has_computed_verdict_negative_fixture_for_each_verdict():
    manifest = _load_manifest()
    schema = _load_schema()
    expected_verdicts = set(schema["properties"]["expected_verdict"]["enum"])
    computed_verdict_matrix = {
        entry["expected_verdict"]
        for entry in _manifest_entries(manifest, "invalid_fixtures")
        if entry.get("fixture_matrix") == "VERDICT_NEGATIVE"
        and entry.get("forbidden_field") == "computed_verdict"
    }

    assert computed_verdict_matrix == expected_verdicts
