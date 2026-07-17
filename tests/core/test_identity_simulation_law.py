"""
Tests for IdentitySimulationLaw audit-only contract.

Origin: docs/18_TRACESTEP_IDENTITY_PROOF_CONTRACT.md
"""
import pytest

from taaqqul_slot_geometry.constitution.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.core.identity_simulation_law import (
    IdentitySimulationLaw,
    IdentitySimulationVerdict,
    SimulationTransitionSnapshot,
    evaluate_identity_simulation,
)


def _law() -> IdentitySimulationLaw:
    return IdentitySimulationLaw(
        law_id="ID_SIM_001",
        system_ref="DAL_ONLY",
    )


def _source_snapshot() -> SimulationTransitionSnapshot:
    return SimulationTransitionSnapshot(
        domain="DAL_ONLY",
        state="carrier_open",
        operation="assign_haraka",
        identity_tokens=frozenset({"carrier", "trace_ref", "root_hint"}),
        evidence_tokens=frozenset({"licensed_carrier", "operation_guard"}),
        transition_verdict="DEFER",
        transition_rank="CANDIDATE",
        transition_residuals=frozenset({"carrier_pending"}),
        transition_blockers=frozenset({"missing_weight_closure"}),
    )


def test_identity_simulation_licenses_exact_snapshot() -> None:
    source = _source_snapshot()
    target = _source_snapshot()
    result = evaluate_identity_simulation(_law(), source, target)
    assert result.verdict == IdentitySimulationVerdict.LICENSED
    assert result.identity_preserved is True
    assert result.violations == frozenset()


def test_identity_simulation_blocks_rank_inflation() -> None:
    source = _source_snapshot()
    target = SimulationTransitionSnapshot(
        domain=source.domain,
        state=source.state,
        operation=source.operation,
        identity_tokens=source.identity_tokens,
        evidence_tokens=source.evidence_tokens,
        transition_verdict=source.transition_verdict,
        transition_rank="CERTIFICATE",
        transition_residuals=source.transition_residuals,
        transition_blockers=source.transition_blockers,
    )
    result = evaluate_identity_simulation(_law(), source, target)
    assert result.verdict == IdentitySimulationVerdict.BLOCKED
    assert FailureCode.M_CX_09 in result.violations


def test_identity_simulation_blocks_hidden_residuals() -> None:
    source = _source_snapshot()
    target = SimulationTransitionSnapshot(
        domain=source.domain,
        state=source.state,
        operation=source.operation,
        identity_tokens=source.identity_tokens,
        evidence_tokens=source.evidence_tokens,
        transition_verdict=source.transition_verdict,
        transition_rank=source.transition_rank,
        transition_residuals=frozenset(),
        transition_blockers=source.transition_blockers,
    )
    result = evaluate_identity_simulation(_law(), source, target)
    assert result.verdict == IdentitySimulationVerdict.BLOCKED
    assert FailureCode.M_CX_01 in result.violations


def test_identity_simulation_blocks_verdict_mutation() -> None:
    source = _source_snapshot()
    target = SimulationTransitionSnapshot(
        domain=source.domain,
        state=source.state,
        operation=source.operation,
        identity_tokens=source.identity_tokens,
        evidence_tokens=source.evidence_tokens,
        transition_verdict="ACCEPT",
        transition_rank=source.transition_rank,
        transition_residuals=source.transition_residuals,
        transition_blockers=source.transition_blockers,
    )
    result = evaluate_identity_simulation(_law(), source, target)
    assert result.verdict == IdentitySimulationVerdict.BLOCKED
    assert FailureCode.M_CX_02 in result.violations


def test_identity_simulation_law_rejects_empty_law_id() -> None:
    with pytest.raises(ValueError) as exc_info:
        IdentitySimulationLaw(law_id="", system_ref="DAL_ONLY")
    assert FailureCode.M_CX_02.value in str(exc_info.value)

