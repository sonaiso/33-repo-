"""
Tests for Euclidean learning contracts and staged learning flow.

Origin: docs/15_PROJECT_ROADMAP.md §Euclidean Learning Track
"""
from taaqqul_slot_geometry.constitution.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.core.euclidean_learning import (
    ExecutionRank,
    Evidence,
    EuclideanTransitionContract,
    FORBIDDEN_OVERREACH,
    Layer,
    LearningMemory,
    MinimalCompleteRequirement,
    Residual,
    ResidualKind,
    contract_from_registry,
    energy_guard,
    euclidean_learning_step,
    evaluate_transition,
    has_blocking_residual,
    learn_failure,
    learn_success,
    predict_branch,
)
from taaqqul_slot_geometry.core.transition_registry import (
    EUCLIDEAN_GATE_SEQUENCE,
    EuclideanTransitionContract as RegistryTransitionContract,
)


def _requirement() -> MinimalCompleteRequirement:
    return MinimalCompleteRequirement(
        required_fields=(
            "origin",
            "branch",
            "preserved_identity",
            "common_illah",
            "effective_description",
            "qadih_difference",
            "condition",
            "sabab",
            "handoff",
            "evidence",
        ),
        forbidden_overreach=frozenset(),
        max_rank=ExecutionRank.CERTIFIED,
    )


def _contract(
    *,
    preventer: str | None = None,
    transition_residuals: tuple[Residual, ...] = (),
    execution_rank: ExecutionRank = ExecutionRank.LICENSED,
    handoff: str = "T10",
    condition: str = "valid relation",
) -> EuclideanTransitionContract:
    return EuclideanTransitionContract(
        transition_id="EUCL_LEARN_01",
        origin="origin:entity",
        branch="branch:relation",
        preserved_identity="entity persists",
        common_illah="assignability",
        effective_description="subject + predicate",
        qadih_difference="no blocking semantic mismatch",
        condition=condition,
        sabab="licensed predication",
        preventer=preventer,
        transition_residuals=transition_residuals,
        execution_rank=execution_rank,
        minimal_complete_requirement=_requirement(),
        handoff=handoff,
        evidence=(
            Evidence(
                source="example corpus",
                claim="entity can carry predicate",
                evidence_rank=ExecutionRank.CANDIDATE,
            ),
        ),
    )


def test_contract_from_registry_preserves_origin_branch() -> None:
    assert FailureCode.M_CX_02.value
    registry_contract = RegistryTransitionContract(
        contract_id="R1",
        origin_ref="origin:entity",
        branch_ref="branch:relation",
        preserved_identity=frozenset({"entity"}),
        common_illah="assignability",
        effective_description="subject + predicate",
        qadih_difference_rule="none",
        condition="condition",
        cause="cause",
        preventers=frozenset(),
        minimal_complete_gates=EUCLIDEAN_GATE_SEQUENCE,
    )
    contract = contract_from_registry(
        registry_contract,
        transition_id="EXT1",
        execution_rank=ExecutionRank.CANDIDATE,
        handoff="T10",
        evidence=(
            Evidence(
                source="registry",
                claim="compatible extension",
                evidence_rank=ExecutionRank.CANDIDATE,
            ),
        ),
    )

    assert contract.base_contract is registry_contract
    assert contract.origin == "origin:entity"
    assert contract.branch == "branch:relation"


def test_has_blocking_residual_detects_blocking() -> None:
    contract = _contract(
        transition_residuals=(
            Residual(
                code="MissingSilah",
                kind=ResidualKind.BLOCKING,
                message="relative clause missing",
            ),
        )
    )
    assert has_blocking_residual(contract) is True


def test_evaluate_transition_licenses_valid_contract() -> None:
    decision = evaluate_transition(_contract())
    assert decision.allowed is True
    assert decision.decision_rank == ExecutionRank.LICENSED
    assert decision.reason == "Transition licensed"


def test_evaluate_transition_blocks_active_preventer() -> None:
    decision = evaluate_transition(_contract(preventer="MissingRightHost"))
    assert decision.allowed is False
    assert decision.decision_rank == ExecutionRank.BLOCKED
    assert "Active preventer" in decision.reason


def test_learn_success_appends_contract() -> None:
    memory, decision = learn_success(LearningMemory(), "example", _contract())
    assert decision.allowed is True
    assert len(memory.contracts) == 1
    assert len(memory.failures) == 0


def test_learn_failure_appends_failure_record() -> None:
    memory, failure = learn_failure(
        LearningMemory(),
        "example",
        _contract(preventer="MissingRightHost"),
    )
    assert len(memory.failures) == 1
    assert failure.active_preventer == "MissingRightHost"
    assert failure.repair_suggestion == "Remove preventer: MissingRightHost"


def test_predict_branch_returns_ranked_predictions() -> None:
    low = _contract(execution_rank=ExecutionRank.CANDIDATE)
    high = _contract(execution_rank=ExecutionRank.LICENSED, handoff="T11")
    memory = LearningMemory(contracts=(low, high), failures=())

    predictions = predict_branch(memory, "origin:entity")
    assert len(predictions) == 2
    assert predictions[0].decision_rank == ExecutionRank.LICENSED
    assert predictions[0].handoff == "T11"


def test_energy_guard_blocks_layer_overreach() -> None:
    blocked_output = next(iter(FORBIDDEN_OVERREACH[Layer.T9_RAW_MEANING]))
    decision = energy_guard(
        Layer.T9_RAW_MEANING,
        frozenset({blocked_output}),
        ExecutionRank.CANDIDATE,
    )
    assert decision.allowed is False
    assert decision.decision_rank == ExecutionRank.BLOCKED
    assert decision.transition_residuals[0].code == "LAYER_OVERREACH"


def test_euclidean_learning_step_writes_failure_when_energy_fails() -> None:
    blocked_output = next(iter(FORBIDDEN_OVERREACH[Layer.T9_RAW_MEANING]))
    memory, decision = euclidean_learning_step(
        LearningMemory(),
        "example",
        Layer.T9_RAW_MEANING,
        _contract(),
        frozenset({blocked_output}),
    )
    assert decision.allowed is False
    assert len(memory.failures) == 1
    assert len(memory.contracts) == 0


def test_euclidean_learning_step_writes_contract_when_passes() -> None:
    memory, decision = euclidean_learning_step(
        LearningMemory(),
        "example",
        Layer.T11_RELATION,
        _contract(),
        frozenset({"RelationCandidate"}),
    )
    assert decision.allowed is True
    assert len(memory.contracts) == 1
    assert len(memory.failures) == 0
