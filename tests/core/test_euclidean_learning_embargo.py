"""
Embargo containment checks for Euclidean learning audit sandbox.

Origin: docs/12_RUNTIME_EMBARGO_CONSTITUTION.md §Euclidean Learning Exception Boundary
"""
from dataclasses import FrozenInstanceError
from pathlib import Path

import pytest

from taaqqul_slot_geometry.constitution.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.core.euclidean_learning import (
    EUCLIDEAN_LEARNING_DECISION_SCOPE,
    EUCLIDEAN_LEARNING_RUNTIME_STATUS,
    Evidence,
    ExecutionRank,
    FORBIDDEN_OVERREACH,
    Layer,
    LearningMemory,
    MinimalCompleteRequirement,
    predict_branch,
    euclidean_learning_step,
    evaluate_transition,
    learn_failure,
)


REPO_ROOT = Path(__file__).parent.parent.parent


def _requirement() -> MinimalCompleteRequirement:
    return MinimalCompleteRequirement(
        required_fields=MinimalCompleteRequirement.CONTRACT_FIELD_NAMES,
        forbidden_overreach=frozenset(),
        max_rank=ExecutionRank.LICENSED,
    )


def _contract(preventer: str | None = None):
    from taaqqul_slot_geometry.core.euclidean_learning import EuclideanTransitionContract

    return EuclideanTransitionContract(
        transition_id="EUCL_EMBARGO_01",
        origin="origin:entity",
        branch="branch:relation",
        preserved_identity=("entity",),
        common_illah="assignability",
        effective_description="subject + predicate",
        qadih_difference="no blocking semantic mismatch",
        condition="valid relation",
        sabab="licensed predication",
        preventer=preventer,
        transition_residuals=(),
        execution_rank=ExecutionRank.LICENSED,
        minimal_complete_requirement=_requirement(),
        handoff="T11",
        evidence=(
            Evidence(
                source="example corpus",
                claim="entity can carry predicate",
                evidence_rank=ExecutionRank.CANDIDATE,
            ),
        ),
    )


def test_euclidean_outputs_are_audit_only() -> None:
    decision = evaluate_transition(_contract())
    assert decision.authoritative is False
    assert decision.decision_scope == EUCLIDEAN_LEARNING_DECISION_SCOPE
    assert decision.runtime_status == EUCLIDEAN_LEARNING_RUNTIME_STATUS


def test_learning_step_never_returns_authoritative_decision() -> None:
    _, decision = euclidean_learning_step(
        LearningMemory(),
        "example",
        Layer.T11_RELATION_AUDIT,
        _contract(),
        frozenset({"RelationCandidate"}),
    )
    assert decision.allowed is True
    assert decision.authoritative is False


def test_execution_rank_certified_is_reserved_for_embargoed_runtime() -> None:
    assert not hasattr(ExecutionRank, "CERTIFIED")
    assert hasattr(ExecutionRank, "CERTIFIED_RESERVED")
    assert _contract().rank == "CANDIDATE"


def test_hukm_audit_label_does_not_authorize_hukm_runtime_output() -> None:
    from taaqqul_slot_geometry.core.euclidean_learning import energy_guard

    decision = energy_guard(
        Layer.T13_HUKM_AUDIT,
        frozenset({"RuntimeAuthorityEscalation"}),
        ExecutionRank.LICENSED,
    )
    assert decision.allowed is False
    assert decision.decision_rank == ExecutionRank.BLOCKED


def test_relation_layer_output_remains_audit_only() -> None:
    _, decision = euclidean_learning_step(
        LearningMemory(),
        "example",
        Layer.T11_RELATION_AUDIT,
        _contract(),
        frozenset({"RelationCandidate"}),
    )
    assert decision.allowed is True
    assert decision.authoritative is False


def test_embargo_forbidden_runtime_files_remain_absent() -> None:
    assert not (REPO_ROOT / "src" / "taaqqul_slot_geometry" / "L1" / "binding_kernel.py").exists()
    assert not (REPO_ROOT / "src" / "taaqqul_slot_geometry" / "L1" / "decision_engine.py").exists()


def test_learning_memory_is_immutable_and_non_persistent() -> None:
    memory = LearningMemory()
    with pytest.raises(FrozenInstanceError):
        memory.contracts = ()


def test_predict_branch_returns_suggestions_not_decisions() -> None:
    memory, _ = euclidean_learning_step(
        LearningMemory(),
        "example",
        Layer.T11_RELATION_AUDIT,
        _contract(),
        frozenset({"RelationCandidate"}),
    )
    predictions = predict_branch(memory, "origin:entity")
    assert predictions
    assert predictions[0].authoritative is False
    assert predictions[0].decision_scope == EUCLIDEAN_LEARNING_DECISION_SCOPE


def test_failure_records_are_learning_artifacts_not_failurecode_replacements() -> None:
    memory, failure = learn_failure(LearningMemory(), "example", _contract(preventer="X"))
    assert memory.failures
    assert failure.authoritative is False
    assert not failure.failed_transition.startswith("M_")
    assert failure.active_preventer == "X"
    assert FailureCode.M_CX_08.value == "silent_exception_forbidden"


def test_runtime_embargo_document_remains_active() -> None:
    content = (
        REPO_ROOT / "docs" / "12_RUNTIME_EMBARGO_CONSTITUTION.md"
    ).read_text(encoding="utf-8")
    assert "Runtime remains embargoed" in content
    assert "isolated audit sandbox" in content
    assert "audit-only" in content


def test_forbidden_overreach_map_blocks_hukm_authority_outputs() -> None:
    assert "RuntimeAuthorityEscalation" in FORBIDDEN_OVERREACH[Layer.T13_HUKM_AUDIT]
