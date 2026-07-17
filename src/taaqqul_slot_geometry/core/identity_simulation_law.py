"""
IdentitySimulationLaw — audit-only contract for identity-preserving simulation.

Origin: docs/18_TRACESTEP_IDENTITY_PROOF_CONTRACT.md
trace_ref: docs/20_AGENT_AUTONOMY_RUNBOOK.md §Single-Goal audit-only outputs
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import FrozenSet

from taaqqul_slot_geometry.constitution.failure_taxonomy import FailureCode


class IdentitySimulationVerdict(str, Enum):
    """Audit verdict for identity simulation checks."""

    LICENSED = "licensed"
    BLOCKED = "blocked"


@dataclass(frozen=True)
class SimulationTransitionSnapshot:
    """Transition snapshot used as source/target input for identity simulation."""

    domain: str
    state: str
    operation: str
    identity_tokens: FrozenSet[str]
    evidence_tokens: FrozenSet[str]
    transition_verdict: str
    transition_rank: str
    transition_residuals: FrozenSet[str]
    transition_blockers: FrozenSet[str]
    trace_ref: str = "docs/18_TRACESTEP_IDENTITY_PROOF_CONTRACT.md"
    rank: str = "CANDIDATE"
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if not self.domain or not self.state or not self.operation:
            raise ValueError(f"{FailureCode.M_CX_02.value}: transition scope incomplete")
        if not self.identity_tokens:
            raise ValueError(f"{FailureCode.M_CX_01.value}: identity_tokens cannot be empty")
        if not self.evidence_tokens:
            raise ValueError(f"{FailureCode.M_CX_30.value}: evidence_tokens cannot be empty")
        if not self.transition_verdict:
            raise ValueError(
                f"{FailureCode.M_CX_02.value}: transition_verdict cannot be empty"
            )
        if not self.transition_rank:
            raise ValueError(f"{FailureCode.M_00_12.value}: transition_rank cannot be empty")
        if not self.trace_ref:
            raise ValueError(FailureCode.M_00_11.value)
        if self.rank != "CANDIDATE":
            raise ValueError(FailureCode.M_00_10.value)


@dataclass(frozen=True)
class IdentitySimulationLaw:
    """Single-system identity simulation contract (Id_S: S → S)."""

    law_id: str
    system_ref: str
    trace_ref: str = "docs/18_TRACESTEP_IDENTITY_PROOF_CONTRACT.md"
    rank: str = "CANDIDATE"
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if not self.law_id:
            raise ValueError(f"{FailureCode.M_CX_02.value}: law_id cannot be empty")
        if not self.system_ref:
            raise ValueError(f"{FailureCode.M_CX_02.value}: system_ref cannot be empty")
        if not self.trace_ref:
            raise ValueError(FailureCode.M_00_11.value)
        if self.rank != "CANDIDATE":
            raise ValueError(FailureCode.M_00_10.value)


@dataclass(frozen=True)
class IdentitySimulationResult:
    """Result of evaluating an identity simulation attempt."""

    verdict: IdentitySimulationVerdict
    violations: FrozenSet[FailureCode]
    identity_preserved: bool
    trace_ref: str = "docs/18_TRACESTEP_IDENTITY_PROOF_CONTRACT.md"
    rank: str = "CANDIDATE"
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if not self.trace_ref:
            raise ValueError(FailureCode.M_00_11.value)
        if self.rank != "CANDIDATE":
            raise ValueError(FailureCode.M_00_10.value)


def evaluate_identity_simulation(
    law: IdentitySimulationLaw,
    source: SimulationTransitionSnapshot,
    target: SimulationTransitionSnapshot,
) -> IdentitySimulationResult:
    """Evaluate whether target is an identity-preserving simulation of source."""
    if law.system_ref != source.domain or law.system_ref != target.domain:
        return IdentitySimulationResult(
            verdict=IdentitySimulationVerdict.BLOCKED,
            violations=frozenset({FailureCode.M_CX_02}),
            identity_preserved=False,
        )

    violations: set[FailureCode] = set()
    if source.domain != target.domain:
        violations.add(FailureCode.M_CX_02)
    if source.state != target.state:
        violations.add(FailureCode.M_CX_02)
    if source.operation != target.operation:
        violations.add(FailureCode.M_CX_02)
    if source.transition_verdict != target.transition_verdict:
        violations.add(FailureCode.M_CX_02)
    if source.transition_rank != target.transition_rank:
        violations.add(FailureCode.M_CX_09)
    if source.identity_tokens != target.identity_tokens:
        violations.add(FailureCode.M_CX_01)
    if not source.evidence_tokens.issubset(target.evidence_tokens):
        violations.add(FailureCode.M_CX_30)
    if not source.transition_residuals.issubset(target.transition_residuals):
        violations.add(FailureCode.M_CX_01)
    if not source.transition_blockers.issubset(target.transition_blockers):
        violations.add(FailureCode.M_CX_01)

    if violations:
        return IdentitySimulationResult(
            verdict=IdentitySimulationVerdict.BLOCKED,
            violations=frozenset(violations),
            identity_preserved=False,
        )
    return IdentitySimulationResult(
        verdict=IdentitySimulationVerdict.LICENSED,
        violations=frozenset(),
        identity_preserved=True,
    )

