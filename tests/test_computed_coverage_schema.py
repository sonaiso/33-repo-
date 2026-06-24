"""Schema-only guardrails for computed coverage cases (PR #76).

trace_ref: docs/18_COMPUTED_COVERAGE_SCHEMA_CONSTITUTION.md
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
    if "pattern" in rule and isinstance(value, str) and not re.fullmatch(rule["pattern"], value):
        raise ValueError(f"{key} must satisfy pattern")


def _fallback_validate(schema: dict[str, Any], payload: dict[str, Any]) -> None:
    """Validate payloads when jsonschema is unavailable.

    Supports required fields, type/minLength/minItems, enum/const checks,
    additionalProperties blocking, forbidden `not.anyOf` rules, and `allOf`
    conditional requirements used by this schema.
    """
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
        _validate_rule(key, value, properties.get(key, {}))

    forbidden = schema.get("not", {}).get("anyOf", [])
    for entry in forbidden:
        required_fields = entry.get("required", [])
        if required_fields and all(field in payload for field in required_fields):
            if "properties" not in entry:
                raise ValueError(f"Forbidden field present: {required_fields[0]}")

        for field, prop_rule in entry.get("properties", {}).items():
            if field not in payload:
                continue
            if "const" in prop_rule and payload[field] == prop_rule["const"]:
                raise ValueError(f"Forbidden const value for {field}")
            if "enum" in prop_rule and payload[field] in prop_rule["enum"]:
                raise ValueError(f"Forbidden enum value for {field}")

    for conditional in schema.get("allOf", []):
        if_clause = conditional.get("if", {})
        if any(field not in payload for field in if_clause.get("required", [])):
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
        for field in then_clause.get("required", []):
            if field not in payload:
                raise ValueError(f"Missing conditional required field: {field}")
        for field, rule in then_clause.get("properties", {}).items():
            if field in payload:
                _validate_rule(field, payload[field], rule)


def _validate_payload(schema: dict[str, Any], payload: dict[str, Any]) -> None:
    if Draft202012Validator is None:
        _fallback_validate(schema, payload)
        return
    Draft202012Validator(schema).validate(payload)


def _minimal_valid_case() -> dict[str, Any]:
    return {
        "case_id": "case-001",
        "input_text": "example input",
        "input_domain": "D2_LAFZI_FORM",
        "expected_verdict": "EXPECTED_ACCEPTED_CANDIDATE",
        "required_contracts": [
            "docs/10_DAL_ATOMIC_CONSTITUTION.md",
            "docs/11_LAFZI_FORM_CONSTITUTION.md",
        ],
        "trace_ref": "docs/18_COMPUTED_COVERAGE_SCHEMA_CONSTITUTION.md",
    }


def _assert_invalid(payload: dict[str, Any]) -> None:
    schema = _load_schema()
    with pytest.raises((ValidationError, ValueError)):
        _validate_payload(schema, payload)


def test_schema_file_exists():
    assert SCHEMA_PATH.exists()


def test_schema_is_valid_draft_2020_12():
    schema = _load_schema()
    if Draft202012Validator is not None:
        Draft202012Validator.check_schema(schema)
    else:
        assert isinstance(schema, dict)


def test_schema_accepts_valid_expected_accepted_case():
    schema = _load_schema()
    _validate_payload(schema, _minimal_valid_case())


@pytest.mark.parametrize(
    "domain",
    [
        "D0_TRACE",
        "D1_DAL_ONLY",
        "D2_LAFZI_FORM",
        "D3_LEXICAL_MADLUL",
        "D4_RELATION",
    ],
)
def test_schema_accepts_canonical_input_domains(domain: str):
    schema = _load_schema()
    payload = _minimal_valid_case() | {"input_domain": domain}
    _validate_payload(schema, payload)


@pytest.mark.parametrize(
    ("domain", "expected_verdict", "extra"),
    [
        ("D5_IFADAH", "EXPECTED_RESIDUAL", {"expected_residual_policy": "KEEP_RESIDUALS"}),
        ("D6_HUKM", "EXPECTED_PROOF_REQUIRED", {"expected_failure_family": "FAMILY_PROOF_REQUIRED"}),
        ("D7_TANZIL", "EXPECTED_BRIDGE_REQUIRED", {"required_bridges": ["L2_TO_L3_BRIDGE"]}),
    ],
)
def test_schema_accepts_locked_domains_with_embargo_safe_expected_verdicts(
    domain: str,
    expected_verdict: str,
    extra: dict[str, Any],
):
    schema = _load_schema()
    payload = _minimal_valid_case() | {
        "input_domain": domain,
        "expected_verdict": expected_verdict,
    } | extra
    _validate_payload(schema, payload)


def test_schema_rejects_unknown_input_domain():
    _assert_invalid(_minimal_valid_case() | {"input_domain": "RELATION_RUNTIME"})


@pytest.mark.parametrize("domain", ["D5_IFADAH", "D6_HUKM", "D7_TANZIL"])
def test_schema_rejects_expected_accepted_candidate_for_locked_domains(domain: str):
    _assert_invalid(
        _minimal_valid_case()
        | {
            "input_domain": domain,
            "expected_verdict": "EXPECTED_ACCEPTED_CANDIDATE",
        }
    )


def test_schema_accepts_valid_expected_blocked_only_with_failure_family():
    schema = _load_schema()
    payload = _minimal_valid_case() | {
        "expected_verdict": "EXPECTED_BLOCKED",
        "expected_failure_family": "FAMILY_EMBARGO",
    }
    _validate_payload(schema, payload)


def test_schema_rejects_expected_blocked_without_failure_family():
    _assert_invalid(_minimal_valid_case() | {"expected_verdict": "EXPECTED_BLOCKED"})


def test_schema_accepts_expected_proof_required_only_with_failure_family():
    schema = _load_schema()
    payload = _minimal_valid_case() | {
        "expected_verdict": "EXPECTED_PROOF_REQUIRED",
        "expected_failure_family": "FAMILY_PROOF_REQUIRED",
    }
    _validate_payload(schema, payload)


def test_schema_rejects_expected_proof_required_without_failure_family():
    _assert_invalid(_minimal_valid_case() | {"expected_verdict": "EXPECTED_PROOF_REQUIRED"})


@pytest.mark.parametrize("invalid_family", ["PROOF/MRK", "rank family", "family_lower", "meaning-leak!"])
def test_schema_rejects_non_schema_safe_expected_failure_family(invalid_family: str):
    _assert_invalid(
        _minimal_valid_case()
        | {
            "expected_verdict": "EXPECTED_BLOCKED",
            "expected_failure_family": invalid_family,
        }
    )


def test_schema_accepts_expected_residual_only_with_residual_policy():
    schema = _load_schema()
    payload = _minimal_valid_case() | {
        "expected_verdict": "EXPECTED_RESIDUAL",
        "expected_residual_policy": "KEEP_RESIDUALS",
    }
    _validate_payload(schema, payload)


def test_schema_rejects_expected_residual_without_residual_policy():
    _assert_invalid(_minimal_valid_case() | {"expected_verdict": "EXPECTED_RESIDUAL"})


@pytest.mark.parametrize("invalid_policy", ["POLICY/ONE", "policy one", "policy_lower", "policy!"])
def test_schema_rejects_non_schema_safe_expected_residual_policy(invalid_policy: str):
    _assert_invalid(
        _minimal_valid_case()
        | {
            "expected_verdict": "EXPECTED_RESIDUAL",
            "expected_residual_policy": invalid_policy,
        }
    )


def test_schema_accepts_expected_bridge_required_only_with_non_empty_required_bridges():
    schema = _load_schema()
    payload = _minimal_valid_case() | {
        "expected_verdict": "EXPECTED_BRIDGE_REQUIRED",
        "required_bridges": ["DAL_TO_LAFZI_BRIDGE"],
    }
    _validate_payload(schema, payload)


def test_schema_rejects_expected_bridge_required_without_required_bridges():
    _assert_invalid(_minimal_valid_case() | {"expected_verdict": "EXPECTED_BRIDGE_REQUIRED"})


def test_schema_rejects_expected_bridge_required_with_empty_required_bridges():
    _assert_invalid(
        _minimal_valid_case()
        | {
            "expected_verdict": "EXPECTED_BRIDGE_REQUIRED",
            "required_bridges": [],
        }
    )


def test_schema_rejects_computed_verdict():
    _assert_invalid(_minimal_valid_case() | {"computed_verdict": "manual"})


def test_schema_rejects_mrk_defaults():
    _assert_invalid(_minimal_valid_case() | {"mrk_defaults": {"domain_proved": True}})


@pytest.mark.parametrize(
    "forbidden_bool_field",
    [
        "domain_proved",
        "unit_proved",
        "identity_preserved",
        "trace_preserved",
        "gate_passed",
        "is_preserved",
    ],
)
def test_schema_rejects_forbidden_boolean_fields(forbidden_bool_field: str):
    _assert_invalid(_minimal_valid_case() | {forbidden_bool_field: True})


def test_schema_rejects_manual_dashboard():
    _assert_invalid(_minimal_valid_case() | {"manual_dashboard": {"total": 1}})


@pytest.mark.parametrize("rank_value", ["CERTIFICATE", "REJECTED", "Rank.CERTIFICATE", "Rank.REJECTED"])
def test_schema_rejects_forbidden_rank_values(rank_value: str):
    _assert_invalid(_minimal_valid_case() | {"rank": rank_value})


def test_schema_keeps_coverage_matrix_forbidden_and_absent():
    _assert_invalid(_minimal_valid_case() | {"coverage_matrix_v0.1.yaml": "forbidden"})
    assert not (REPO_ROOT / "coverage_matrix_v0.1.yaml").exists()


@pytest.mark.parametrize(
    "verdict",
    [
        "EXPECTED_ACCEPTED_CANDIDATE",
        "EXPECTED_BLOCKED",
        "EXPECTED_RESIDUAL",
        "EXPECTED_BRIDGE_REQUIRED",
        "EXPECTED_PROOF_REQUIRED",
    ],
)
def test_expected_verdict_enum_is_supported(verdict: str):
    schema = _load_schema()
    payload = _minimal_valid_case() | {"expected_verdict": verdict}
    if verdict in {"EXPECTED_BLOCKED", "EXPECTED_PROOF_REQUIRED"}:
        payload["expected_failure_family"] = "FAMILY"
    if verdict == "EXPECTED_RESIDUAL":
        payload["expected_residual_policy"] = "KEEP"
    if verdict == "EXPECTED_BRIDGE_REQUIRED":
        payload["required_bridges"] = ["BRIDGE"]
    _validate_payload(schema, payload)


def test_fallback_validator_accepts_valid_case(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr("tests.test_computed_coverage_schema.Draft202012Validator", None)
    schema = _load_schema()
    _validate_payload(schema, _minimal_valid_case())


def test_fallback_validator_rejects_computed_verdict(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr("tests.test_computed_coverage_schema.Draft202012Validator", None)
    _assert_invalid(_minimal_valid_case() | {"computed_verdict": "manual"})
