"""Runtime Embargo Lift request schema guardrails (schema-only, no runtime lift).

trace_ref: docs/18_RUNTIME_EMBARGO_LIFT_PROTOCOL.md
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import pytest

try:
    from jsonschema import Draft202012Validator
    from jsonschema.exceptions import ValidationError
except ImportError:  # pragma: no cover
    Draft202012Validator = None
    ValidationError = ValueError


REPO_ROOT = Path(__file__).parent.parent
SCHEMA_PATH = REPO_ROOT / "schemas" / "runtime_lift_request.schema.json"
TEMPLATE_PATH = REPO_ROOT / "docs" / "19_RUNTIME_EMBARGO_LIFT_PR_TEMPLATE.md"
REQUIRED_NEGATIVE_TESTS = [
    "reject-rank-certificate",
    "reject-rank-rejected",
    "reject-boolean-as-proof",
    "reject-evidence-list-as-proof",
    "reject-domain-open-without-bridge",
    "reject-manual-computed-verdict",
]


def _load_schema() -> dict[str, Any]:
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


def _validate_rule(key: str, value: Any, rule: dict[str, Any]) -> None:
    expected_type = rule.get("type")
    if expected_type == "string":
        if not isinstance(value, str):
            raise ValueError(f"{key} must be string")
        if "minLength" in rule and len(value) < rule["minLength"]:
            raise ValueError(f"{key} must satisfy minLength")
        if "pattern" in rule and not re.fullmatch(rule["pattern"], value):
            raise ValueError(f"{key} must satisfy pattern")
    elif expected_type == "boolean":
        if not isinstance(value, bool):
            raise ValueError(f"{key} must be boolean")
    elif expected_type == "array":
        if not isinstance(value, list):
            raise ValueError(f"{key} must be array")
        if "minItems" in rule and len(value) < rule["minItems"]:
            raise ValueError(f"{key} must satisfy minItems")
        if rule.get("uniqueItems"):
            try:
                unique_count = len(set(value))
            except TypeError as exc:
                raise ValueError(f"{key} items must be hashable for uniqueness") from exc
            if len(value) != unique_count:
                raise ValueError(f"{key} must contain unique items")
        item_rule = rule.get("items", {})
        for item in value:
            _validate_rule(key, item, item_rule)

    if "enum" in rule and value not in rule["enum"]:
        raise ValueError(f"{key} must be one of enum values")
    if "const" in rule and value != rule["const"]:
        raise ValueError(f"{key} must match const value")


def _fallback_validate(schema: dict[str, Any], payload: dict[str, Any]) -> None:
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
        _validate_rule(key, value, properties.get(key, {}))


def _validate_payload(schema: dict[str, Any], payload: dict[str, Any]) -> None:
    if Draft202012Validator is None:
        _fallback_validate(schema, payload)
        return
    Draft202012Validator(schema).validate(payload)


def _valid_request() -> dict[str, Any]:
    return {
        "lift_type": "LIFT_TYPE_SCHEMA_RUNTIME",
        "authorized_artifacts": ["schemas/runtime_lift_request.schema.json"],
        "non_scope_artifacts": [
            "src/taaqqul_slot_geometry/runtime/binding_kernel.py",
            "src/taaqqul_slot_geometry/core/decision_engine.py",
            "coverage_matrix_v0.1.yaml",
        ],
        "rollback_plan": "Revert schema and template files; keep embargo active.",
        "negative_tests": [
            *REQUIRED_NEGATIVE_TESTS,
        ],
        "domain_opening": "none",
        "rank_policy": "CANDIDATE_ONLY",
        "blanket_lift": False,
    }


def _assert_invalid(payload: dict[str, Any]) -> None:
    schema = _load_schema()
    with pytest.raises((ValidationError, ValueError)):
        _validate_payload(schema, payload)


def test_runtime_lift_template_and_schema_exist():
    assert TEMPLATE_PATH.exists()
    assert SCHEMA_PATH.exists()


def test_runtime_lift_template_states_non_authorization():
    content = TEMPLATE_PATH.read_text(encoding="utf-8")
    assert "Readiness is not lift." in content
    assert "DONE in readiness ledger is not lift." in content
    assert "This template does not authorize runtime." in content


def test_schema_is_valid_draft_2020_12_or_valid_dict():
    schema = _load_schema()
    if Draft202012Validator is not None:
        Draft202012Validator.check_schema(schema)
    else:
        assert isinstance(schema, dict)


def test_schema_accepts_valid_lift_request_shape():
    schema = _load_schema()
    _validate_payload(schema, _valid_request())


def test_lift_request_cannot_use_glob_artifacts():
    _assert_invalid(_valid_request() | {"authorized_artifacts": ["src/**/*.py"]})


def test_non_scope_artifacts_cannot_use_glob_artifacts():
    _assert_invalid(_valid_request() | {"non_scope_artifacts": ["src/**/*.py"]})


def test_lift_request_cannot_be_blanket_lift():
    _assert_invalid(_valid_request() | {"blanket_lift": True})


def test_rollback_plan_is_required():
    payload = _valid_request()
    payload.pop("rollback_plan")
    _assert_invalid(payload)


def test_negative_tests_are_required():
    payload = _valid_request()
    payload.pop("negative_tests")
    _assert_invalid(payload)


def test_negative_tests_must_include_required_minimum_set():
    payload = _valid_request()
    payload["negative_tests"] = [
        test_id
        for test_id in REQUIRED_NEGATIVE_TESTS
        if test_id != "reject-manual-computed-verdict"
    ]
    _assert_invalid(payload)


def test_authorized_artifacts_must_be_exact_paths_without_wildcards():
    _assert_invalid(_valid_request() | {"authorized_artifacts": ["*"]})


def test_schema_runtime_requires_domain_opening_none():
    _assert_invalid(
        _valid_request()
        | {
            "lift_type": "LIFT_TYPE_SCHEMA_RUNTIME",
            "domain_opening": "D3_LEXICAL_MADLUL",
        }
    )


def test_bridge_evaluator_allows_explicit_domain_opening():
    schema = _load_schema()
    payload = _valid_request() | {
        "lift_type": "LIFT_TYPE_BRIDGE_EVALUATOR",
        "domain_opening": "D4_RELATION",
    }
    _validate_payload(schema, payload)


def test_domain_opening_rejects_implicit_value():
    _assert_invalid(_valid_request() | {"domain_opening": "implicit_domain"})


def test_rank_policy_cannot_allow_certificate():
    _assert_invalid(_valid_request() | {"rank_policy": "CERTIFICATE_ALLOWED"})


@pytest.mark.parametrize(
    "artifact",
    [
        "src/taaqqul_slot_geometry/runtime/binding_kernel.py",
        "src/taaqqul_slot_geometry/core/decision_engine.py",
        "coverage_matrix_v0.1.yaml",
    ],
)
def test_schema_runtime_rejects_forbidden_runtime_artifacts(artifact: str):
    payload = _valid_request()
    payload["authorized_artifacts"] = [artifact]
    _assert_invalid(payload)


@pytest.mark.parametrize(
    "field,value",
    [
        ("authorized_artifacts", "/abs/path.py"),
        ("authorized_artifacts", "../runtime/binding_kernel.py"),
        ("authorized_artifacts", "src\\windows\\path.py"),
        ("authorized_artifacts", "src//double/slash.py"),
        ("non_scope_artifacts", "/abs/path.py"),
        ("non_scope_artifacts", "../runtime/binding_kernel.py"),
        ("non_scope_artifacts", "src\\windows\\path.py"),
        ("non_scope_artifacts", "src//double/slash.py"),
    ],
)
def test_paths_reject_non_canonical_entries(field: str, value: str):
    payload = _valid_request()
    payload[field] = [value]
    _assert_invalid(payload)


def test_binding_kernel_file_not_created():
    assert not (REPO_ROOT / "src" / "taaqqul_slot_geometry" / "runtime" / "binding_kernel.py").exists()
