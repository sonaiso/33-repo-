"""Schema-only guardrails for computed coverage cases (PR #58)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

try:
    from jsonschema import Draft202012Validator
    from jsonschema.exceptions import ValidationError
except ImportError:  # pragma: no cover - fallback for minimal envs.
    Draft202012Validator = None
    ValidationError = ValueError


REPO_ROOT = Path(__file__).parent.parent
SCHEMA_PATH = REPO_ROOT / "schemas" / "coverage_case.schema.json"


def _load_schema() -> dict[str, Any]:
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


def _fallback_validate(schema: dict[str, Any], payload: dict[str, Any]) -> None:
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
                if item_rule.get("minLength", 0) and len(item) < item_rule["minLength"]:
                    raise ValueError(f"{key} array items must satisfy minLength")

        if "enum" in rule and value not in rule["enum"]:
            raise ValueError(f"{key} must be one of enum values")

    forbidden = schema["not"]["anyOf"]
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


def _validate_payload(schema: dict[str, Any], payload: dict[str, Any]) -> None:
    if Draft202012Validator is None:
        _fallback_validate(schema, payload)
        return
    Draft202012Validator(schema).validate(payload)


def _minimal_valid_case() -> dict[str, Any]:
    return {
        "case_id": "case-001",
        "input_text": "example input",
        "input_domain": "D1_DAL_ONLY",
        "input_contract_ref": "docs/07_GATE_BRIDGE_CONSTITUTION.md#contract",
        "expected_verdict": "EXPECTED_BLOCKED",
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


def test_valid_minimal_expected_case_passes():
    """trace_ref: docs/09_COMPUTED_COVERAGE_CONSTITUTION.md Coverage Computation Law."""
    schema = _load_schema()
    _validate_payload(schema, _minimal_valid_case())


def test_computed_verdict_is_rejected():
    case = _minimal_valid_case() | {"computed_verdict": "manual"}
    _assert_invalid(case)


def test_mrk_defaults_is_rejected():
    case = _minimal_valid_case() | {"mrk_defaults": {"identity_preserved": True}}
    _assert_invalid(case)


def test_domain_proved_true_is_rejected():
    case = _minimal_valid_case() | {"domain_proved": True}
    _assert_invalid(case)


def test_identity_preserved_true_is_rejected():
    case = _minimal_valid_case() | {"identity_preserved": True}
    _assert_invalid(case)


def test_gate_passed_true_is_rejected():
    case = _minimal_valid_case() | {"gate_passed": True}
    _assert_invalid(case)


def test_rank_certificate_is_rejected_if_rank_appears():
    case = _minimal_valid_case() | {"rank": "CERTIFICATE"}
    _assert_invalid(case)


def test_expected_verdict_is_allowed():
    schema = _load_schema()
    for expected_verdict in [
        "EXPECTED_ACCEPTED_CANDIDATE",
        "EXPECTED_BLOCKED",
        "EXPECTED_RESIDUAL",
        "EXPECTED_BRIDGE_REQUIRED",
        "EXPECTED_PROOF_REQUIRED",
    ]:
        payload = _minimal_valid_case() | {"expected_verdict": expected_verdict}
        _validate_payload(schema, payload)


def test_coverage_matrix_v0_1_yaml_does_not_exist():
    forbidden = REPO_ROOT / "coverage_matrix_v0.1.yaml"
    assert not forbidden.exists()
