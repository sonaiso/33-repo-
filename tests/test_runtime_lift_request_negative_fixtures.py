"""Negative Runtime Embargo Lift request fixtures (audit-only).

trace_ref: docs/12_RUNTIME_EMBARGO_CONSTITUTION.md; docs/18_RUNTIME_EMBARGO_LIFT_PROTOCOL.md
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from tests.test_runtime_lift_request_schema import (
    ValidationError,
    _load_schema,
    _validate_payload,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_DIR = REPO_ROOT / "tests" / "fixtures" / "runtime_lift_requests"
MANIFEST_PATH = FIXTURE_DIR / "manifest.json"
REQUIRED_INVALID_CASES = [
    "prompt_authorization_only",
    "user_delegation_only",
    "agent_response_only",
    "readiness_status_only",
    "broad_runtime_lift_without_artifacts",
    "artifact_wildcard_lift",
    "unspecified_artifact_scope",
    "runtime_lift_without_explicit_pr_number_or_pr_marker",
    "runtime_lift_without_failure_alignment_reference",
    "runtime_lift_without_proof_policy_reference",
    "runtime_lift_without_rollback_policy",
    "runtime_lift_that_attempts_kernel_or_decision_engine_by_default",
    "runtime_lift_that_mentions_binding_kernel_py_without_exact_explicit_artifact_authorization",
    "runtime_lift_that_mentions_coverage_matrix_v0_1_yaml_before_computed_coverage_schema_authorization",
]


def _load_manifest() -> dict[str, Any]:
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def _fixture_cases() -> list[Any]:
    manifest = _load_manifest()
    return [
        pytest.param(case["case_id"], case["file"], id=case["case_id"])
        for case in manifest["cases"]
    ]


def test_runtime_lift_negative_fixture_manifest_lists_required_cases():
    manifest = _load_manifest()
    assert manifest["required_invalid_cases"] == REQUIRED_INVALID_CASES
    assert [case["case_id"] for case in manifest["cases"]] == REQUIRED_INVALID_CASES


@pytest.mark.parametrize("case_id,file_name", _fixture_cases())
def test_invalid_runtime_lift_request_fixture_is_schema_rejected(
    case_id: str,
    file_name: str,
):
    payload = json.loads((FIXTURE_DIR / file_name).read_text(encoding="utf-8"))
    with pytest.raises((ValidationError, ValueError)):
        _validate_payload(_load_schema(), payload)
    assert case_id in REQUIRED_INVALID_CASES


def test_runtime_lift_negative_fixtures_do_not_create_forbidden_runtime_artifacts():
    forbidden_paths = [
        "src/taaqqul_slot_geometry/runtime/binding_kernel.py",
        "src/taaqqul_slot_geometry/runtime/decision_engine.py",
        "coverage_matrix_v0.1.yaml",
    ]
    assert all(not (REPO_ROOT / path).exists() for path in forbidden_paths)
