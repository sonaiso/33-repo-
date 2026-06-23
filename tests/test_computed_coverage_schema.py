"""Schema-only guardrails for computed coverage cases (PR #58).

trace_ref: docs/09_COMPUTED_COVERAGE_CONSTITUTION.md Coverage Computation Law
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

try:
    from jsonschema import Draft202012Validator
    from jsonschema.exceptions import ValidationError
except ImportError:  # pragma: no cover - fallback for minimal environments
    Draft202012Validator = None
    ValidationError = ValueError


REPO_ROOT = Path(__file__).parent.parent
SCHEMA_PATH = REPO_ROOT / "schemas" / "coverage_case.schema.json"


def _load_schema() -> dict[str, Any]:
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


def _validate_rule(key: str, value: Any, rule: dict[str, Any]) -> None:
    expected_type = rule.get("type")
    if expected_type == "string":
        if not isinstance(value, str):
            raise ValueError(f"{key} must be string")
        if "minLength" in rule and len(value) < rule["minLength"]:
            raise ValueError(f"{key} must satisfy minLength")
    elif expected_type == "array":
        if not isinstance(value, list):
            raise ValueError(f"{key} must be array")
        if "minItems" in rule and len(value) < rule["minItems"]:
            raise ValueError(f"{key} must satisfy minItems")
        item_rule = rule.get("items", {})
        for item in value:
            if item_rule.get("type") == "string" and not isinstance(item, str):
                raise ValueError(f"{key} array items must be strings")
            if "minLength" in item_rule and len(item) < item_rule["minLength"]:
                raise ValueError(f"{key} array items must satisfy minLength")

    if "enum" in rule and value not in rule["enum"]:
        raise ValueError(f"{key} must be one of enum values")
    if "const" in rule and value != rule["const"]:
        raise ValueError(f"{key} must match const value")


def _fallback_validate(schema: dict[str, Any], payload: dict[str, Any]) -> None:
    """Fallback validator for required/enum/type/additionalProperties/not-anyOf checks."""
    if not isinstance(payload, dict):
        raise ValueError("Payload must be an object")

    required = set(schema.get("required", []))
    missing = sorted(required - set(payload))
    if missing:
        raise ValueError(f"Missing required fields: {missing}")

    properties = schema.get("properties", {})
    if schema.get("additionalProperties") is False:
        extra = sorted(set(payload) - set(properties))
        if extra:
            raise ValueError(f"Unexpected properties: {extra}")

    for key, value in payload.items():
        rule = properties.get(key, {})
        _validate_rule(key, value, rule)

    forbidden = schema.get("not", {}).get("anyOf")
    if not isinstance(forbidden, list):
        raise ValueError("Schema must include not.anyOf forbiddance list")
    for entry in forbidden:
        required_fields = entry.get("required", [])
        if required_fields and all(field in payload for field in required_fields):
            if "properties" not in entry:
                raise ValueError(f"Forbidden field present: {required_fields[0]}")

        props = entry.get("properties", {})
        for field, prop_rule in props.items():
            if field not in payload:
                continue
            if "const" in prop_rule and payload[field] == prop_rule["const"]:
                raise ValueError(f"Forbidden const value for {field}")
            if "enum" in prop_rule and payload[field] in prop_rule["enum"]:
                raise ValueError(f"Forbidden enum value for {field}")

    for conditional in schema.get("allOf", []):
        if_clause = conditional.get("if", {})
        if_required = if_clause.get("required", [])
        if any(field not in payload for field in if_required):
            continue

        matches = True
        for field, rule in if_clause.get("properties", {}).items():
            if field not in payload:
                continue
            if "const" in rule and payload[field] != rule["const"]:
                matches = False
                break
            if "enum" in rule and payload[field] not in rule["enum"]:
                matches = False
                break
        if not matches:
            continue

        then_clause = conditional.get("then", {})
        then_required = then_clause.get("required", [])
        missing_then = [field for field in then_required if field not in payload]
        if missing_then:
            raise ValueError(f"Missing conditional required fields: {missing_then}")

        for field, rule in then_clause.get("properties", {}).items():
            if field in payload:
                _validate_rule(field, payload[field], rule)


def _validate_payload(schema: dict[str, Any], payload: dict[str, Any]) -> None:
    if Draft202012Validator is None:
        _fallback_validate(schema, payload)
        return
    Draft202012Validator(schema).validate(payload)


def _minimal_valid_case() -> dict[str, Any]:
    """Use EXPECTED_ACCEPTED_CANDIDATE as baseline because it has no conditional fields."""
    return {
        "case_id": "case-001",
        "input_text": "example input",
        "input_domain": "D1_DAL_ONLY",
        "input_contract_ref": "docs/07_GATE_BRIDGE_CONSTITUTION.md#contract",
        "expected_verdict": "EXPECTED_ACCEPTED_CANDIDATE",
        "required_contracts": ["docs/12_RUNTIME_EMBARGO_CONSTITUTION.md"],
        "trace_ref": "docs/09_COMPUTED_COVERAGE_CONSTITUTION.md",
    }


def _assert_invalid(payload: dict[str, Any]) -> None:
    schema = _load_schema()
    with pytest.raises((ValidationError, ValueError)):
        _validate_payload(schema, payload)


def test_schema_file_exists():
    """trace_ref: docs/09_COMPUTED_COVERAGE_CONSTITUTION.md Coverage Computation Law."""
    assert SCHEMA_PATH.exists()


def test_schema_is_valid_draft_2020_12():
    """trace_ref: docs/09_COMPUTED_COVERAGE_CONSTITUTION.md Coverage Computation Law."""
    schema = _load_schema()
    if Draft202012Validator is not None:
        Draft202012Validator.check_schema(schema)
    else:
        assert isinstance(schema, dict)


def test_valid_minimal_expected_case_passes():
    """trace_ref: docs/09_COMPUTED_COVERAGE_CONSTITUTION.md Coverage Computation Law."""
    schema = _load_schema()
    _validate_payload(schema, _minimal_valid_case())


def test_computed_verdict_is_rejected():
    """trace_ref: docs/09_COMPUTED_COVERAGE_CONSTITUTION.md Coverage Computation Law."""
    case = _minimal_valid_case() | {"computed_verdict": "manual"}
    _assert_invalid(case)


def test_computed_verdict_capitalized_is_rejected():
    """trace_ref: docs/09_COMPUTED_COVERAGE_CONSTITUTION.md Coverage Computation Law."""
    case = _minimal_valid_case() | {"ComputedVerdict": "manual"}
    _assert_invalid(case)


def test_mrk_defaults_is_rejected():
    """trace_ref: docs/09_COMPUTED_COVERAGE_CONSTITUTION.md Coverage Computation Law."""
    case = _minimal_valid_case() | {"mrk_defaults": {"identity_preserved": True}}
    _assert_invalid(case)


def test_domain_proved_true_is_rejected():
    """trace_ref: docs/09_COMPUTED_COVERAGE_CONSTITUTION.md Coverage Computation Law."""
    case = _minimal_valid_case() | {"domain_proved": True}
    _assert_invalid(case)


def test_identity_preserved_true_is_rejected():
    """trace_ref: docs/09_COMPUTED_COVERAGE_CONSTITUTION.md Coverage Computation Law."""
    case = _minimal_valid_case() | {"identity_preserved": True}
    _assert_invalid(case)


def test_gate_passed_true_is_rejected():
    """trace_ref: docs/09_COMPUTED_COVERAGE_CONSTITUTION.md Coverage Computation Law."""
    case = _minimal_valid_case() | {"gate_passed": True}
    _assert_invalid(case)


def test_rank_certificate_is_rejected_if_rank_appears():
    """trace_ref: docs/09_COMPUTED_COVERAGE_CONSTITUTION.md Coverage Computation Law."""
    case = _minimal_valid_case() | {"rank": "CERTIFICATE"}
    _assert_invalid(case)


def test_expected_verdict_is_allowed():
    """trace_ref: docs/09_COMPUTED_COVERAGE_CONSTITUTION.md Coverage Computation Law."""
    schema = _load_schema()
    verdict_payloads = {
        "EXPECTED_ACCEPTED_CANDIDATE": {},
        "EXPECTED_BLOCKED": {"expected_failure_family": "EMBARGO_FAMILY"},
        "EXPECTED_RESIDUAL": {"expected_residual_policy": "KEEP_RESIDUALS"},
        "EXPECTED_BRIDGE_REQUIRED": {"required_bridges": ["D1_TO_D2_GATE"]},
        "EXPECTED_PROOF_REQUIRED": {"expected_failure_family": "EMBARGO_FAMILY"},
    }
    for expected_verdict, extra_fields in verdict_payloads.items():
        payload = _minimal_valid_case() | {"expected_verdict": expected_verdict} | extra_fields
        _validate_payload(schema, payload)


def test_expected_blocked_requires_expected_failure_family():
    """trace_ref: docs/09_COMPUTED_COVERAGE_CONSTITUTION.md Coverage Computation Law."""
    case = _minimal_valid_case() | {"expected_verdict": "EXPECTED_BLOCKED"}
    _assert_invalid(case)


def test_expected_proof_required_requires_expected_failure_family():
    """trace_ref: docs/09_COMPUTED_COVERAGE_CONSTITUTION.md Coverage Computation Law."""
    case = _minimal_valid_case() | {"expected_verdict": "EXPECTED_PROOF_REQUIRED"}
    _assert_invalid(case)


def test_expected_failure_family_requires_non_empty_string_when_required():
    """trace_ref: docs/09_COMPUTED_COVERAGE_CONSTITUTION.md Coverage Computation Law."""
    case = _minimal_valid_case() | {
        "expected_verdict": "EXPECTED_BLOCKED",
        "expected_failure_family": "",
    }
    _assert_invalid(case)


def test_expected_residual_requires_expected_residual_policy():
    """trace_ref: docs/09_COMPUTED_COVERAGE_CONSTITUTION.md Coverage Computation Law."""
    case = _minimal_valid_case() | {"expected_verdict": "EXPECTED_RESIDUAL"}
    _assert_invalid(case)


def test_expected_bridge_required_requires_non_empty_required_bridges():
    """trace_ref: docs/09_COMPUTED_COVERAGE_CONSTITUTION.md Coverage Computation Law."""
    missing_bridges_case = _minimal_valid_case() | {"expected_verdict": "EXPECTED_BRIDGE_REQUIRED"}
    _assert_invalid(missing_bridges_case)

    empty_bridges_case = missing_bridges_case | {"required_bridges": []}
    _assert_invalid(empty_bridges_case)


def test_high_domains_are_allowed_as_labels_only_without_runtime_artifacts():
    """trace_ref: docs/12_RUNTIME_EMBARGO_CONSTITUTION.md Explicit Prohibitions."""
    schema = _load_schema()
    case = _minimal_valid_case() | {"input_domain": "D6_HUKM"}
    _validate_payload(schema, case)
    assert "labels only" in schema["description"]
    assert "docs/12_RUNTIME_EMBARGO_CONSTITUTION.md" in schema["description"]

    assert not (REPO_ROOT / "coverage_matrix_v0.1.yaml").exists()
    assert not (REPO_ROOT / "binding_kernel.py").exists()
    assert not (REPO_ROOT / "decision_engine.py").exists()


def test_coverage_matrix_v0_1_yaml_does_not_exist():
    """trace_ref: docs/12_RUNTIME_EMBARGO_CONSTITUTION.md Explicit Prohibitions."""
    forbidden = REPO_ROOT / "coverage_matrix_v0.1.yaml"
    assert not forbidden.exists()


def test_fallback_validator_accepts_minimal_valid_case(monkeypatch: pytest.MonkeyPatch):
    """trace_ref: docs/09_COMPUTED_COVERAGE_CONSTITUTION.md Coverage Computation Law."""
    monkeypatch.setattr("tests.test_computed_coverage_schema.Draft202012Validator", None)
    schema = _load_schema()
    _validate_payload(schema, _minimal_valid_case())


def test_fallback_validator_rejects_forbidden_fields(monkeypatch: pytest.MonkeyPatch):
    """trace_ref: docs/09_COMPUTED_COVERAGE_CONSTITUTION.md Coverage Computation Law."""
    monkeypatch.setattr("tests.test_computed_coverage_schema.Draft202012Validator", None)
    _assert_invalid(_minimal_valid_case() | {"computed_verdict": "manual"})
