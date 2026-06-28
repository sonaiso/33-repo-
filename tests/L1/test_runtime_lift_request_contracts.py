"""Runtime lift request contracts are audit-only and keep runtime blocked.

trace_ref: docs/18_RUNTIME_EMBARGO_LIFT_PROTOCOL.md
"""

from __future__ import annotations

from pathlib import Path

import pytest

from taaqqul_slot_geometry.L1.runtime_lift_request import (
    RUNTIME_LIFT_TRACE_REF,
    RuntimeLiftArtifact,
    RuntimeLiftRequest,
    audit_runtime_lift_request_shape,
)


REPO_ROOT = Path(__file__).parent.parent.parent


def _build_runtime_lift_artifact(
    path: str = "src/taaqqul_slot_geometry/L1/example_future_runtime.py",
):
    """Build a hypothetical exact artifact request; the file is not created."""

    return RuntimeLiftArtifact(
        artifact_path=path,
        artifact_kind="MODULE",
        exact_scope_only=True,
        trace_ref=RUNTIME_LIFT_TRACE_REF,
    )


def _build_runtime_lift_request(**overrides):
    payload = {
        "request_id": "runtime-lift-shape-001",
        "request_source_type": "RUNTIME_EMBARGO_LIFT_PR",
        "pr_ref": "Runtime Embargo Lift PR #126",
        "requested_artifacts": (_build_runtime_lift_artifact(),),
        "authority_refs": (
            "docs/00_MAQOOL_CONSTITUTION.md",
            "docs/12_RUNTIME_EMBARGO_CONSTITUTION.md",
            "docs/18_RUNTIME_EMBARGO_LIFT_PROTOCOL.md",
        ),
        "failure_alignment_ref": "docs/13_FAILURE_ALIGNMENT_CONSTITUTION.md",
        "proof_policy_ref": "docs/08_PROOF_OBJECT_CONSTITUTION.md",
        "rollback_policy_ref": "docs/19_RUNTIME_EMBARGO_LIFT_PR_TEMPLATE.md",
        "external_blockage_acknowledged": True,
        "prompt_delegation_disclaimed": True,
        "runtime_status": "EXTERNALLY_BLOCKED",
        "trace_ref": RUNTIME_LIFT_TRACE_REF,
    }
    payload.update(overrides)
    return RuntimeLiftRequest(**payload)


def test_valid_shape_remains_externally_blocked():
    result = audit_runtime_lift_request_shape(_build_runtime_lift_request())

    assert result.shape_valid is True
    assert result.runtime_lift_authorized is False
    assert result.status == "AUDIT_SHAPE_VALID_RUNTIME_STILL_BLOCKED"
    assert result.blocking_reasons == ("runtime_embargo_external_block_still_active",)


@pytest.mark.parametrize(
    "source_type",
    [
        "PROMPT",
        "USER_DELEGATION",
        "AGENT_RESPONSE",
        "READINESS_STATUS",
    ],
)
def test_non_lift_pr_source_types_are_rejected(source_type):
    with pytest.raises(ValueError):
        _build_runtime_lift_request(request_source_type=source_type)


def test_prompt_authorization_is_rejected():
    with pytest.raises(ValueError):
        _build_runtime_lift_request(request_source_type="PROMPT")


def test_user_delegation_is_rejected():
    with pytest.raises(ValueError):
        _build_runtime_lift_request(request_source_type="USER_DELEGATION")


def test_agent_response_is_rejected():
    with pytest.raises(ValueError):
        _build_runtime_lift_request(request_source_type="AGENT_RESPONSE")


def test_readiness_status_is_rejected():
    with pytest.raises(ValueError):
        _build_runtime_lift_request(request_source_type="READINESS_STATUS")


def test_wildcard_artifact_is_rejected():
    with pytest.raises(ValueError):
        _build_runtime_lift_artifact("src/**/*.py")


@pytest.mark.parametrize("artifact_path", ["runtime", "*"])
def test_broad_runtime_scope_is_rejected(artifact_path):
    with pytest.raises(ValueError):
        _build_runtime_lift_artifact(artifact_path)


def test_missing_pr_ref_is_rejected():
    with pytest.raises(ValueError):
        _build_runtime_lift_request(pr_ref="")


def test_missing_failure_alignment_ref_is_rejected():
    with pytest.raises(ValueError):
        _build_runtime_lift_request(failure_alignment_ref="")


def test_missing_proof_policy_ref_is_rejected():
    with pytest.raises(ValueError):
        _build_runtime_lift_request(proof_policy_ref="")


def test_missing_rollback_policy_ref_is_rejected():
    with pytest.raises(ValueError):
        _build_runtime_lift_request(rollback_policy_ref="")


def test_external_blockage_acknowledged_false_is_rejected():
    with pytest.raises(ValueError):
        _build_runtime_lift_request(external_blockage_acknowledged=False)


def test_prompt_delegation_disclaimed_false_is_rejected():
    with pytest.raises(ValueError):
        _build_runtime_lift_request(prompt_delegation_disclaimed=False)


@pytest.mark.parametrize("runtime_status", ["OPEN", "AUTHORIZED"])
def test_runtime_status_cannot_be_open(runtime_status):
    with pytest.raises(ValueError):
        _build_runtime_lift_request(runtime_status=runtime_status)


def test_rank_promotion_rejected():
    with pytest.raises(ValueError):
        _build_runtime_lift_request(rank="CERTIFICATE")


def test_binding_kernel_path_not_authorized_by_shape_validator():
    artifact_path = "src/taaqqul_slot_geometry/L1/binding_kernel.py"
    request = _build_runtime_lift_request(
        requested_artifacts=(_build_runtime_lift_artifact(artifact_path),)
    )
    result = audit_runtime_lift_request_shape(request)

    assert result.shape_valid is True
    assert result.checked_artifacts == (artifact_path,)
    assert result.runtime_lift_authorized is False
    assert not (REPO_ROOT / artifact_path).exists()


def test_no_forbidden_runtime_files_created():
    forbidden_paths = [
        "src/taaqqul_slot_geometry/L1/binding_kernel.py",
        "src/taaqqul_slot_geometry/L1/decision_engine.py",
        "coverage_matrix_v0.1.yaml",
    ]

    for path in forbidden_paths:
        assert not (REPO_ROOT / path).exists()
