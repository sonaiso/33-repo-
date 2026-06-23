"""
Tests for Euclidean transition contracts and staged energy-aware evaluation.

Origin: docs/59_ARABIC_DIGITAL_IDENTITY_LAW.md §TransitionRegistry
"""
import pytest

from taaqqul_slot_geometry.constitution.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.core.transition_registry import (
    EUCLIDEAN_GATE_SEQUENCE,
    EuclideanGate,
    EuclideanTransitionContract,
    EuclideanTransitionProbe,
    TransitionVerdict,
    evaluate_euclidean_transition,
)


def _full_contract() -> EuclideanTransitionContract:
    return EuclideanTransitionContract(
        contract_id="EUCLIDEAN_TEST_01",
        origin_ref="origin:Zayd",
        branch_ref="branch:NominalPredication",
        preserved_identity=frozenset({"entity", "candidate"}),
        common_illah="assignability",
        effective_description="known subject + valid predicate",
        qadih_difference_rule="no disqualifying transitivity mismatch",
        condition="two valid sides for relation",
        cause="licensed predication relation",
        preventers=frozenset({"missing_predicate"}),
        minimal_complete_gates=EUCLIDEAN_GATE_SEQUENCE,
    )


def _full_probe() -> EuclideanTransitionProbe:
    return EuclideanTransitionProbe(
        origin_ref="origin:Zayd",
        branch_ref="branch:NominalPredication",
        source_identity=frozenset({"entity", "candidate"}),
        target_identity=frozenset({"entity", "candidate", "relation"}),
        common_illah_valid=True,
        effective_description_valid=True,
        qadih_difference_absent=True,
        condition_met=True,
        cause_active=True,
        preventer_active=False,
    )


def test_contract_rejects_non_progressive_minimal_gates() -> None:
    with pytest.raises(ValueError) as exc_info:
        EuclideanTransitionContract(
            contract_id="EUCLIDEAN_BAD",
            origin_ref="o",
            branch_ref="b",
            preserved_identity=frozenset({"id"}),
            common_illah="illah",
            effective_description="desc",
            qadih_difference_rule="rule",
            condition="condition",
            cause="cause",
            preventers=frozenset(),
            minimal_complete_gates=(
                EuclideanGate.IDENTITY_LINK,
                EuclideanGate.EFFECTIVE_DESCRIPTION,
            ),
        )
    assert FailureCode.M_CX_02.value in str(exc_info.value)


def test_full_chain_success_is_licensed() -> None:
    result = evaluate_euclidean_transition(_full_contract(), _full_probe())
    assert result.verdict == TransitionVerdict.LICENSED
    assert result.result_rank == "LICENSED"
    assert result.failed_gate is None
    assert result.identity_preserved is True
    assert result.minimal_complete_reached is True
    assert result.executed_gates == EUCLIDEAN_GATE_SEQUENCE
    assert result.energy_used == len(EUCLIDEAN_GATE_SEQUENCE)


def test_qadih_difference_blocks_and_stops_early() -> None:
    probe = _full_probe()
    probe = EuclideanTransitionProbe(
        origin_ref=probe.origin_ref,
        branch_ref=probe.branch_ref,
        source_identity=probe.source_identity,
        target_identity=probe.target_identity,
        common_illah_valid=True,
        effective_description_valid=True,
        qadih_difference_absent=False,
        condition_met=True,
        cause_active=True,
        preventer_active=False,
    )
    result = evaluate_euclidean_transition(_full_contract(), probe)
    assert result.verdict == TransitionVerdict.BLOCKED
    assert result.failed_gate == EuclideanGate.QADIH_DIFFERENCE
    assert result.energy_used == 4
    assert EuclideanGate.CONDITION not in result.executed_gates


def test_minimal_complete_prefix_preserves_energy() -> None:
    contract = EuclideanTransitionContract(
        contract_id="EUCLIDEAN_MINIMAL",
        origin_ref="origin:Zayd",
        branch_ref="branch:NominalPredication",
        preserved_identity=frozenset({"entity"}),
        common_illah="assignability",
        effective_description="known subject + valid predicate",
        qadih_difference_rule="none",
        condition="condition",
        cause="cause",
        preventers=frozenset({"future_preventer"}),
        minimal_complete_gates=(
            EuclideanGate.IDENTITY_LINK,
            EuclideanGate.COMMON_ILLAH,
            EuclideanGate.EFFECTIVE_DESCRIPTION,
        ),
    )
    probe = EuclideanTransitionProbe(
        origin_ref="origin:Zayd",
        branch_ref="branch:NominalPredication",
        source_identity=frozenset({"entity"}),
        target_identity=frozenset({"entity", "relation"}),
        common_illah_valid=True,
        effective_description_valid=True,
        qadih_difference_absent=False,
        condition_met=False,
        cause_active=False,
        preventer_active=True,
    )
    result = evaluate_euclidean_transition(contract, probe)
    assert result.verdict == TransitionVerdict.DEFERRED
    assert result.result_rank == "CANDIDATE"
    assert result.minimal_complete_reached is True
    assert result.energy_used == 3
    assert result.executed_gates == contract.minimal_complete_gates


def test_identity_link_mismatch_blocks_immediately() -> None:
    probe = EuclideanTransitionProbe(
        origin_ref="origin:Other",
        branch_ref="branch:NominalPredication",
        source_identity=frozenset({"entity", "candidate"}),
        target_identity=frozenset({"entity", "candidate", "relation"}),
        common_illah_valid=True,
        effective_description_valid=True,
        qadih_difference_absent=True,
        condition_met=True,
        cause_active=True,
        preventer_active=False,
    )
    result = evaluate_euclidean_transition(_full_contract(), probe)
    assert result.verdict == TransitionVerdict.BLOCKED
    assert result.failed_gate == EuclideanGate.IDENTITY_LINK
    assert result.energy_used == 1
