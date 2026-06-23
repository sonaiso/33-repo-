"""
Euclidean learning domain boundary checks (audit-only, non-runtime).

Origin: docs/14_EUCLIDEAN_LEARNING_DOMAIN_BOUNDARY.md
"""
from pathlib import Path

from taaqqul_slot_geometry.L1.domain_ids import DomainID
from taaqqul_slot_geometry.core.euclidean_learning import (
    EUCLIDEAN_LAYER_DOMAIN_AUDIT_MAP,
    EUCLIDEAN_LAYER_DOMAIN_MAP_IS_AUDIT_ONLY,
    EUCLIDEAN_LEARNING_DECISION_SCOPE,
    EUCLIDEAN_LEARNING_RUNTIME_STATUS,
    Evidence,
    ExecutionRank,
    Layer,
    LearningMemory,
    MinimalCompleteRequirement,
    euclidean_learning_step,
    evaluate_transition,
    learn_failure,
    predict_branch,
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
        transition_id="EUCL_BOUNDARY_01",
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


def test_layer_domain_boundary_map_is_complete_and_audit_only() -> None:
    assert EUCLIDEAN_LAYER_DOMAIN_MAP_IS_AUDIT_ONLY is True
    assert set(EUCLIDEAN_LAYER_DOMAIN_AUDIT_MAP.keys()) == set(Layer)
    assert EUCLIDEAN_LAYER_DOMAIN_AUDIT_MAP[Layer.T8_PHONIC_SIGNIFIER] == DomainID.D1_DAL_ONLY
    assert EUCLIDEAN_LAYER_DOMAIN_AUDIT_MAP[Layer.T9_RAW_MEANING] is None
    assert EUCLIDEAN_LAYER_DOMAIN_AUDIT_MAP[Layer.T10_CONVENTIONAL] == DomainID.D3_LEXICAL_MADLUL
    assert EUCLIDEAN_LAYER_DOMAIN_AUDIT_MAP[Layer.T11_RELATION_AUDIT] == DomainID.D4_RELATION
    assert EUCLIDEAN_LAYER_DOMAIN_AUDIT_MAP[Layer.T12_IFADAH_AUDIT] == DomainID.D5_IFADAH
    assert EUCLIDEAN_LAYER_DOMAIN_AUDIT_MAP[Layer.T13_HUKM_AUDIT] == DomainID.D6_HUKM


def test_relation_ifadah_hukm_audit_layers_do_not_open_runtime_domains() -> None:
    memory = LearningMemory()
    for layer, outputs in (
        (Layer.T11_RELATION_AUDIT, frozenset({"RelationCandidate"})),
        (Layer.T12_IFADAH_AUDIT, frozenset({"IfadahCandidate"})),
        (Layer.T13_HUKM_AUDIT, frozenset({"HukmAuditCandidate"})),
    ):
        memory, decision = euclidean_learning_step(memory, "example", layer, _contract(), outputs)
        assert decision.allowed is True
        assert decision.authoritative is False
        assert decision.decision_scope == EUCLIDEAN_LEARNING_DECISION_SCOPE
        assert decision.runtime_status == EUCLIDEAN_LEARNING_RUNTIME_STATUS
        assert decision.decision_rank in {
            ExecutionRank.CANDIDATE,
            ExecutionRank.HYPOTHESIS,
            ExecutionRank.DEFERRED,
            ExecutionRank.LICENSED,
        }


def test_outputs_remain_non_authoritative_and_no_runtime_verdict_labels() -> None:
    decision = evaluate_transition(_contract())
    _, failure = learn_failure(LearningMemory(), "example", _contract(preventer="MissingRightHost"))
    memory, _ = euclidean_learning_step(
        LearningMemory(),
        "example",
        Layer.T11_RELATION_AUDIT,
        _contract(),
        frozenset({"RelationCandidate"}),
    )
    prediction = predict_branch(memory, "origin:entity")[0]

    assert decision.authoritative is False
    assert failure.authoritative is False
    assert prediction.authoritative is False

    runtime_labels = {"FinalMeaning", "Hukm", "Tanzil"}
    observed_strings = {
        decision.reason,
        decision.handoff,
        failure.failed_transition,
        prediction.handoff,
    }
    assert runtime_labels.isdisjoint(observed_strings)


def test_runtime_embargo_document_stays_active() -> None:
    content = (
        REPO_ROOT / "docs" / "12_RUNTIME_EMBARGO_CONSTITUTION.md"
    ).read_text(encoding="utf-8")
    assert "Runtime remains embargoed" in content
    assert "T11_RELATION_AUDIT" in content
    assert "T12_IFADAH_AUDIT" in content
    assert "T13_HUKM_AUDIT" in content
