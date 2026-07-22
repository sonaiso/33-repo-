"""Tests for audit-only operation boundary contracts."""

from __future__ import annotations

from taaqqul_slot_geometry.L1.operation_boundary_contracts import (
    AuthorizationContext,
    AuthorizationStatus,
    CandidateProposal,
    OperationContract,
    TotalizedStatus,
    process,
)


def _proposal(*, input_types: tuple[str, ...] = ("LetterCarrier",)) -> CandidateProposal:
    return CandidateProposal(
        operation_id="BIND",
        input_ids=("carrier-1",),
        input_types=input_types,
        domain="phonology",
        evidence_ids=("ev-1",),
        expected_effect="AtomicPhonologicalUnit",
    )


def _contract(
    *,
    delegated_domain_bridges: frozenset[str] = frozenset(),
) -> OperationContract:
    return OperationContract(
        operation_id="BIND",
        source_types=frozenset({"LetterCarrier", "HarakaOperator"}),
        target_type="AtomicPhonologicalUnit",
        domain="phonology",
        licensed_domain_bridges=frozenset({"phonology->phonology"}),
        delegated_domain_bridges=delegated_domain_bridges,
        preconditions=frozenset({"LETTER_LICENSED"}),
        evidence_policy=frozenset({"EVIDENCE_PHONETIC"}),
        blockers=frozenset({"BLOCKING_RESIDUAL"}),
        preserved_identity_keys=frozenset({"RootId", "CarrierId"}),
    )


def _context(
    *,
    source_domain: str = "phonology",
    target_domain: str = "phonology",
    available_preconditions: frozenset[str] = frozenset({"LETTER_LICENSED"}),
    available_evidence: frozenset[str] = frozenset({"EVIDENCE_PHONETIC"}),
    active_blockers: frozenset[str] = frozenset(),
    source_identity: dict[str, str] | None = None,
    target_identity: dict[str, str] | None = None,
) -> AuthorizationContext:
    return AuthorizationContext(
        source_domain=source_domain,
        target_domain=target_domain,
        available_preconditions=available_preconditions,
        available_evidence=available_evidence,
        active_blockers=active_blockers,
        source_identity=source_identity or {"RootId": "r1", "CarrierId": "c1"},
        target_identity=target_identity or {"RootId": "r1", "CarrierId": "c1"},
    )


def test_type_mismatch_returns_undefined() -> None:
    result = process(
        proposal=_proposal(input_types=("RootCandidate",)),
        contract=_contract(),
        context=_context(),
        effect_executor=lambda _: "out-1",
    )

    assert result.status == TotalizedStatus.UNDEFINED
    assert "TYPE_MISMATCH" in result.residuals


def test_domain_delegation_returns_deferred() -> None:
    result = process(
        proposal=_proposal(),
        contract=_contract(delegated_domain_bridges=frozenset({"phonology->syntax"})),
        context=_context(target_domain="syntax"),
        effect_executor=lambda _: "out-1",
    )

    assert result.status == TotalizedStatus.DEFERRED
    assert "DOMAIN_BRIDGE_UNPROVEN" in result.residuals


def test_missing_precondition_returns_deferred() -> None:
    result = process(
        proposal=_proposal(),
        contract=_contract(),
        context=_context(available_preconditions=frozenset()),
        effect_executor=lambda _: "out-1",
    )

    assert result.status == TotalizedStatus.DEFERRED
    assert "PRECONDITION_MISSING:LETTER_LICENSED" in result.residuals


def test_missing_evidence_returns_deferred() -> None:
    result = process(
        proposal=_proposal(),
        contract=_contract(),
        context=_context(available_evidence=frozenset()),
        effect_executor=lambda _: "out-1",
    )

    assert result.status == TotalizedStatus.DEFERRED
    assert "EVIDENCE_MISSING:EVIDENCE_PHONETIC" in result.residuals


def test_blocker_returns_blocked() -> None:
    result = process(
        proposal=_proposal(),
        contract=_contract(),
        context=_context(active_blockers=frozenset({"BLOCKING_RESIDUAL"})),
        effect_executor=lambda _: "out-1",
    )

    assert result.status == TotalizedStatus.BLOCKED
    assert "BLOCKING_RESIDUAL:BLOCKING_RESIDUAL" in result.residuals


def test_identity_break_returns_failure() -> None:
    result = process(
        proposal=_proposal(),
        contract=_contract(),
        context=_context(target_identity={"RootId": "r2", "CarrierId": "c1"}),
        effect_executor=lambda _: "out-1",
    )

    assert result.status == TotalizedStatus.FAILURE
    assert "IDENTITY_VIOLATION:RootId" in result.residuals


def test_success_runs_full_sequence_and_preserves_execution_boundary() -> None:
    touched: dict[str, AuthorizationStatus | None] = {"seen": None}

    def _execute(approved_context):
        touched["seen"] = AuthorizationStatus.APPROVED
        return "bind-output-1"

    result = process(
        proposal=_proposal(),
        contract=_contract(),
        context=_context(),
        effect_executor=_execute,
        next_transition_hints=("READY_FOR_SYNTAX",),
    )

    assert result.status == TotalizedStatus.SUCCESS
    assert result.output_id == "bind-output-1"
    assert result.closure_state == "CLOSED"
    assert result.next_transitions == ("READY_FOR_SYNTAX",)
    assert touched["seen"] == AuthorizationStatus.APPROVED
    assert [item.stage for item in result.checks][-6:] == [
        "ExecuteEffect",
        "RankBound",
        "ResidualEmit",
        "TraceCommit",
        "ClosureEvaluate",
        "TransitionReadiness",
    ]


def test_residuals_keep_closure_state_visible() -> None:
    result = process(
        proposal=_proposal(),
        contract=OperationContract(
            operation_id="BIND",
            source_types=frozenset({"LetterCarrier", "HarakaOperator"}),
            target_type="AtomicPhonologicalUnit",
            domain="phonology",
            licensed_domain_bridges=frozenset({"phonology->phonology"}),
            preconditions=frozenset({"LETTER_LICENSED"}),
            evidence_policy=frozenset({"EVIDENCE_PHONETIC"}),
            blockers=frozenset({"BLOCKING_RESIDUAL"}),
            preserved_identity_keys=frozenset({"RootId", "CarrierId"}),
            residuals=frozenset({"PATTERN_SHARED"}),
        ),
        context=_context(),
        effect_executor=lambda _: "bind-output-2",
    )

    assert result.status == TotalizedStatus.SUCCESS
    assert result.closure_state == "CLOSED_WITH_RESIDUALS"
    assert "PATTERN_SHARED" in result.residuals
