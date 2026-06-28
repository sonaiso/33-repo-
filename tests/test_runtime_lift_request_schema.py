"""Runtime Embargo Lift request schema guardrails (schema-only, no runtime lift).

trace_ref: docs/18_RUNTIME_EMBARGO_LIFT_PROTOCOL.md
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import pytest

from tests.forbidden_runtime_artifacts import load_forbidden_runtime_artifact_paths
from tests.test_runtime_antipatterns_embargo import (
    FORBIDDEN_RUNTIME_ARTIFACT_PATHS as EMBARGO_FORBIDDEN_RUNTIME_ARTIFACTS,
)

try:
    from jsonschema import Draft202012Validator
    from jsonschema.exceptions import ValidationError
except ImportError:  # pragma: no cover
    Draft202012Validator = None
    ValidationError = ValueError


REPO_ROOT = Path(__file__).parent.parent
SCHEMA_PATH = REPO_ROOT / "schemas" / "runtime_lift_request.schema.json"
REJECTED_PATTERNS_DOC_PATH = REPO_ROOT / "docs" / "15_REJECTED_RUNTIME_PATTERNS.md"
TEMPLATE_PATH = REPO_ROOT / "docs" / "19_RUNTIME_EMBARGO_LIFT_PR_TEMPLATE.md"
READY_REQUEST_PATH = REPO_ROOT / "data" / "runtime_lift_request.ready.json"
READINESS_LEDGER_SOURCE = "docs/17_RUNTIME_EMBARGO_READINESS_LEDGER.md"
REQUIRED_NEGATIVE_TESTS = [
    "reject-rank-certificate",
    "reject-rank-rejected",
    "reject-boolean-as-proof",
    "reject-evidence-list-as-proof",
    "reject-domain-open-without-bridge",
    "reject-manual-computed-verdict",
]
LIFT_TYPES = [
    "LIFT_TYPE_SCHEMA_RUNTIME",
    "LIFT_TYPE_PROOF_EVALUATOR",
    "LIFT_TYPE_BRIDGE_EVALUATOR",
    "LIFT_TYPE_COVERAGE_RUNNER",
    "LIFT_TYPE_KERNEL",
]
NON_NONE_DOMAIN_OPENINGS = [
    "D3_LEXICAL_MADLUL",
    "D4_RELATION",
    "D5_IFADAH",
    "D6_HUKM",
    "D7_TANZIL",
]
FORBIDDEN_RUNTIME_ARTIFACTS = load_forbidden_runtime_artifact_paths()


def _load_schema() -> dict[str, Any]:
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


def _schema_forbidden_authorized_artifacts_enum() -> list[str]:
    """Extract the schema-wide forbidden authorized_artifacts enum.

    The runtime lift schema keeps this ban in an allOf constraint under
    properties.authorized_artifacts.not.contains.enum so it applies to every
    current lift type.
    """
    schema = _load_schema()
    for rule in schema.get("allOf", []):
        artifacts = (
            rule.get("properties", {})
            .get("authorized_artifacts", {})
            .get("not", {})
            .get("contains", {})
            .get("enum")
        )
        if artifacts is not None:
            return artifacts
    raise AssertionError("schema-wide forbidden authorized_artifacts enum is missing")


def _schema_required_non_scope_artifacts() -> list[str]:
    """Extract mandatory non_scope artifacts from schema allOf constraints."""
    schema = _load_schema()
    for rule in schema.get("allOf", []):
        clauses = (
            rule.get("properties", {})
            .get("non_scope_artifacts", {})
            .get("allOf", [])
        )
        values = [
            clause.get("contains", {}).get("const")
            for clause in clauses
            if clause.get("contains", {}).get("const")
        ]
        if values:
            return values
    raise AssertionError("schema non_scope_artifacts required set is missing")


def _embargo_test_forbidden_artifacts() -> set[str]:
    return set(EMBARGO_FORBIDDEN_RUNTIME_ARTIFACTS)


def _schema_readiness_ledger_source_const() -> str:
    schema = _load_schema()
    value = schema.get("properties", {}).get("readiness_ledger_source", {}).get("const")
    if not value:
        raise AssertionError("schema readiness_ledger_source const is missing")
    return value


def _forbidden_artifact_path_variants(artifact: str) -> list[str]:
    """Build malformed path variants that must fail schema validation.

    These variants model normalization bypass attempts: leading ./, surrounding
    whitespace, consecutive slashes, backslashes, current-directory/trailing-slash
    tricks, and injected .. segments.
    """
    def replaced_or_prefixed(replacement: str, count: int = -1) -> str:
        if "/" not in artifact:
            return f"safe{replacement}{artifact}"
        if count == -1:
            return artifact.replace("/", replacement)
        return artifact.replace("/", replacement, count)

    leading_whitespace = f" {artifact}"
    trailing_whitespace = f"{artifact} "
    partial_double_slash = replaced_or_prefixed("//", 1)
    full_double_slash = replaced_or_prefixed("//")
    partial_backslash = replaced_or_prefixed("\\", 1)
    full_backslash = replaced_or_prefixed("\\")
    partial_dot_segment = replaced_or_prefixed("/./", 1)
    partial_dotdot = replaced_or_prefixed("/../", 1)
    return [
        f"./{artifact}",
        f"{artifact}/",
        leading_whitespace,
        trailing_whitespace,
        partial_double_slash,
        full_double_slash,
        partial_backslash,
        full_backslash,
        partial_dot_segment,
        partial_dotdot,
        f"safe/../{artifact}",
    ]


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
        "non_scope_artifacts": list(FORBIDDEN_RUNTIME_ARTIFACTS),
        "readiness_ledger_source": READINESS_LEDGER_SOURCE,
        "residual_blockers_acknowledged": True,
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


def test_ready_runtime_lift_request_payload_validates():
    schema = _load_schema()
    payload = json.loads(READY_REQUEST_PATH.read_text(encoding="utf-8"))
    _validate_payload(schema, payload)


def test_ready_runtime_lift_request_payload_declares_full_non_scope_set():
    payload = json.loads(READY_REQUEST_PATH.read_text(encoding="utf-8"))
    assert set(payload["non_scope_artifacts"]) == set(FORBIDDEN_RUNTIME_ARTIFACTS)


def test_runtime_lift_template_states_non_authorization():
    content = TEMPLATE_PATH.read_text(encoding="utf-8")
    assert "Readiness is not lift." in content
    assert "DONE in readiness ledger is not lift." in content
    assert "This template does not authorize runtime." in content
    assert (
        "Runtime lift remains externally blocked until a future explicit Runtime Embargo Lift PR is merged."
        in content
    )
    assert (
        "A task prompt, agent response, or user delegation is not a Runtime Embargo Lift PR."
        in content
    )
    assert f"readiness_ledger_source: {READINESS_LEDGER_SOURCE}" in content
    assert "residual_blockers_acknowledged: true" in content


def test_lift_request_template_lists_full_required_negative_tests():
    content = TEMPLATE_PATH.read_text(encoding="utf-8")
    for test_id in REQUIRED_NEGATIVE_TESTS:
        assert test_id in content


def test_lift_request_template_lists_forbidden_runtime_paths():
    content = TEMPLATE_PATH.read_text(encoding="utf-8")
    assert "forbidden_runtime_artifacts.json" in content
    assert (
        "`non_scope_artifacts` in the lift payload must include the full canonical forbidden set."
        in content
    )
    for artifact in FORBIDDEN_RUNTIME_ARTIFACTS:
        assert artifact in content


def test_rejected_patterns_doc_lists_forbidden_runtime_paths():
    content = REJECTED_PATTERNS_DOC_PATH.read_text(encoding="utf-8")
    for artifact in FORBIDDEN_RUNTIME_ARTIFACTS:
        assert artifact in content


def test_forbidden_runtime_artifact_lists_do_not_drift():
    schema_artifacts = set(_schema_forbidden_authorized_artifacts_enum())
    schema_non_scope_artifacts = set(_schema_required_non_scope_artifacts())
    test_artifacts = set(FORBIDDEN_RUNTIME_ARTIFACTS)
    embargo_artifacts = _embargo_test_forbidden_artifacts()
    assert schema_artifacts == test_artifacts
    assert schema_non_scope_artifacts == test_artifacts
    assert embargo_artifacts == test_artifacts


def test_schema_readiness_ledger_source_const_does_not_drift():
    assert _schema_readiness_ledger_source_const() == READINESS_LEDGER_SOURCE
    assert (REPO_ROOT / READINESS_LEDGER_SOURCE).exists()


@pytest.mark.parametrize("missing_artifact", FORBIDDEN_RUNTIME_ARTIFACTS)
def test_schema_requires_every_mandatory_non_scope_artifact(
    missing_artifact: str,
):
    payload = _valid_request()
    payload["non_scope_artifacts"] = [
        artifact
        for artifact in payload["non_scope_artifacts"]
        if artifact != missing_artifact
    ]
    _assert_invalid(payload)


def test_forbidden_runtime_artifact_docs_do_not_drift():
    rejected_patterns_content = REJECTED_PATTERNS_DOC_PATH.read_text(encoding="utf-8")
    template_content = TEMPLATE_PATH.read_text(encoding="utf-8")
    for artifact in FORBIDDEN_RUNTIME_ARTIFACTS:
        assert artifact in rejected_patterns_content
        assert artifact in template_content


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


def test_readiness_ledger_source_is_required():
    payload = _valid_request()
    payload.pop("readiness_ledger_source")
    _assert_invalid(payload)


def test_readiness_ledger_source_must_match_canonical_path():
    _assert_invalid(
        _valid_request()
        | {"readiness_ledger_source": "docs/17_runtime_embargo_readiness_ledger.md"}
    )


def test_residual_blockers_acknowledgement_is_required():
    payload = _valid_request()
    payload.pop("residual_blockers_acknowledged")
    _assert_invalid(payload)


def test_residual_blockers_acknowledgement_must_be_true():
    _assert_invalid(_valid_request() | {"residual_blockers_acknowledged": False})


def test_negative_tests_are_required():
    payload = _valid_request()
    payload.pop("negative_tests")
    _assert_invalid(payload)


def test_negative_tests_reject_empty_list():
    payload = _valid_request()
    payload["negative_tests"] = []
    _assert_invalid(payload)


@pytest.mark.parametrize("missing_test_id", REQUIRED_NEGATIVE_TESTS)
def test_negative_tests_must_include_required_minimum_set(missing_test_id: str):
    payload = _valid_request()
    payload["negative_tests"] = [
        test_id
        for test_id in REQUIRED_NEGATIVE_TESTS
        if test_id != missing_test_id
    ]
    _assert_invalid(payload)


def test_negative_tests_reject_partial_required_subset():
    payload = _valid_request()
    payload["negative_tests"] = REQUIRED_NEGATIVE_TESTS[:3]
    _assert_invalid(payload)


def test_negative_tests_accept_exact_required_set():
    payload = _valid_request()
    payload["negative_tests"] = [*REQUIRED_NEGATIVE_TESTS]
    schema = _load_schema()
    _validate_payload(schema, payload)


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


def test_bridge_evaluator_cannot_open_domain():
    _assert_invalid(
        _valid_request()
        | {
            "lift_type": "LIFT_TYPE_BRIDGE_EVALUATOR",
            "domain_opening": "D4_RELATION",
        }
    )


def test_proof_evaluator_cannot_open_domain():
    _assert_invalid(
        _valid_request()
        | {
            "lift_type": "LIFT_TYPE_PROOF_EVALUATOR",
            "domain_opening": "D3_LEXICAL_MADLUL",
        }
    )


def test_coverage_runner_cannot_open_domain():
    _assert_invalid(
        _valid_request()
        | {
            "lift_type": "LIFT_TYPE_COVERAGE_RUNNER",
            "domain_opening": "D5_IFADAH",
        }
    )


def test_kernel_lift_cannot_open_domain():
    _assert_invalid(
        _valid_request()
        | {
            "lift_type": "LIFT_TYPE_KERNEL",
            "domain_opening": "D6_HUKM",
        }
    )


@pytest.mark.parametrize("lift_type", LIFT_TYPES)
@pytest.mark.parametrize("domain_opening", NON_NONE_DOMAIN_OPENINGS)
def test_all_lift_types_require_domain_opening_none(
    lift_type: str,
    domain_opening: str,
):
    payload = _valid_request()
    payload["lift_type"] = lift_type
    payload["domain_opening"] = domain_opening
    _assert_invalid(payload)


def test_domain_opening_rejects_implicit_value():
    _assert_invalid(_valid_request() | {"domain_opening": "implicit_domain"})


def test_rank_policy_cannot_allow_certificate():
    _assert_invalid(_valid_request() | {"rank_policy": "CERTIFICATE_ALLOWED"})


@pytest.mark.parametrize(
    "lift_type",
    LIFT_TYPES,
)
@pytest.mark.parametrize(
    "artifact",
    FORBIDDEN_RUNTIME_ARTIFACTS,
)
def test_all_lift_types_reject_forbidden_authorized_artifacts(
    lift_type: str,
    artifact: str,
):
    payload = _valid_request()
    payload["lift_type"] = lift_type
    payload["authorized_artifacts"] = [artifact]
    _assert_invalid(payload)


@pytest.mark.parametrize(
    "field,value",
    [
        ("authorized_artifacts", "/abs/path.py"),
        ("authorized_artifacts", "../runtime/binding_kernel.py"),
        ("authorized_artifacts", "./src/runtime/binding_kernel.py"),
        ("authorized_artifacts", " src/runtime/binding_kernel.py"),
        ("authorized_artifacts", "src/runtime/binding_kernel.py "),
        ("authorized_artifacts", "src\\windows\\path.py"),
        ("authorized_artifacts", "src//double/slash.py"),
        ("authorized_artifacts", "src/runtime/./binding_kernel.py"),
        ("authorized_artifacts", "src/runtime/binding_kernel.py/"),
        ("non_scope_artifacts", "/abs/path.py"),
        ("non_scope_artifacts", "../runtime/binding_kernel.py"),
        ("non_scope_artifacts", "./src/runtime/binding_kernel.py"),
        ("non_scope_artifacts", " src/runtime/binding_kernel.py"),
        ("non_scope_artifacts", "src/runtime/binding_kernel.py "),
        ("non_scope_artifacts", "src\\windows\\path.py"),
        ("non_scope_artifacts", "src//double/slash.py"),
        ("non_scope_artifacts", "src/runtime/./binding_kernel.py"),
        ("non_scope_artifacts", "src/runtime/binding_kernel.py/"),
    ],
)
def test_paths_reject_non_canonical_entries(field: str, value: str):
    payload = _valid_request()
    payload[field] = [value]
    _assert_invalid(payload)


@pytest.mark.parametrize("field", ["authorized_artifacts", "non_scope_artifacts"])
@pytest.mark.parametrize(
    "value",
    [
        "src/./taaqqul_slot_geometry/runtime/binding_kernel.py",
        "src/taaqqul_slot_geometry/./runtime/binding_kernel.py",
        "src/taaqqul_slot_geometry/runtime/./binding_kernel.py",
        "src/taaqqul_slot_geometry/runtime/binding_kernel.py/",
        "./src/taaqqul_slot_geometry/runtime/binding_kernel.py",
    ],
)
def test_paths_reject_dot_segment_and_trailing_slash_bypasses(field: str, value: str):
    payload = _valid_request()
    payload[field] = [value]
    _assert_invalid(payload)


@pytest.mark.parametrize("artifact", FORBIDDEN_RUNTIME_ARTIFACTS)
def test_forbidden_authorized_artifact_path_variants_are_rejected(artifact: str):
    for variant in _forbidden_artifact_path_variants(artifact):
        payload = _valid_request()
        payload["authorized_artifacts"] = [variant]
        _assert_invalid(payload)


@pytest.mark.parametrize("artifact", FORBIDDEN_RUNTIME_ARTIFACTS)
def test_mixed_authorized_artifacts_reject_any_forbidden_item(artifact: str):
    payload = _valid_request()
    payload["authorized_artifacts"] = [
        "docs/runtime_lift_audit_contract.md",
        artifact,
    ]
    _assert_invalid(payload)


def test_binding_kernel_file_not_created():
    assert not (REPO_ROOT / "src" / "taaqqul_slot_geometry" / "runtime" / "binding_kernel.py").exists()
