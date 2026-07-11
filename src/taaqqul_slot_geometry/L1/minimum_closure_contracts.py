"""
L1 audit-only Minimum Closure contracts (MRK_L) for lexical carriers.

Single-goal claim:
Define executable audit shape for minimum closure in L1 without runtime authority.

Scope:
- RequiredFields
- RequiredEvidence
- IdentityPreserved
- NoBlockingResidual

Non-scope:
- Runtime/kernels/decision engines
- Domain opening (L2/L3 remain locked)
- External verification authority

Authority:
- docs/00_MAQOOL_CONSTITUTION.md
- docs/00A_CONSTITUTIONAL_PROGRAMMING_AMENDMENT.md
- docs/12_RUNTIME_EMBARGO_CONSTITUTION.md
- docs/13_FAILURE_ALIGNMENT_CONSTITUTION.md
- docs/14_EUCLIDEAN_LEARNING_DOMAIN_BOUNDARY.md
- docs/15_PROJECT_ROADMAP.md
- docs/20_AGENT_AUTONOMY_RUNBOOK.md
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, FrozenSet, Literal, Tuple

from taaqqul_slot_geometry.constitution.failure_taxonomy import FailureCode

MinimumClosureRank = Literal["CANDIDATE"]
MinimumClosureStatus = Literal["MINIMUM_CLOSURE_MET", "MINIMUM_CLOSURE_NOT_MET"]
CarrierKind = Literal[
    "SoundUnitCandidate",
    "LetterUnitCandidate",
    "SurfaceWordCandidate",
    "FormalShapeCandidate",
    "RootReadinessCandidate",
    "WeightReadinessCandidate",
    "VerbalSignifiedCandidate",
    "LexicalSenseCandidate",
    "ContractableLexicalUnit",
]

MINIMUM_CLOSURE_TRACE_REF = "docs/15_PROJECT_ROADMAP.md"
MINIMUM_CLOSURE_CARRIERS: Tuple[CarrierKind, ...] = (
    "SoundUnitCandidate",
    "LetterUnitCandidate",
    "SurfaceWordCandidate",
    "FormalShapeCandidate",
    "RootReadinessCandidate",
    "WeightReadinessCandidate",
    "VerbalSignifiedCandidate",
    "LexicalSenseCandidate",
    "ContractableLexicalUnit",
)


def _require_non_empty(values: Tuple[str, ...]) -> None:
    if not values or any(not value for value in values):
        raise ValueError(FailureCode.M_00_22.value)


def _require_trace_ref(trace_ref: str) -> None:
    if not trace_ref:
        raise ValueError(FailureCode.M_01_14.value)


def _require_candidate_rank(rank: str) -> None:
    if rank != "CANDIDATE":
        raise ValueError(FailureCode.M_01_16.value)


@dataclass(frozen=True)
class MinimumClosureContract:
    """Audit contract describing MRK_L for a single L1 carrier."""

    carrier_kind: CarrierKind
    required_fields: Tuple[str, ...]
    required_evidence: Tuple[str, ...]
    required_identity: Tuple[str, ...]
    trace_ref: str = MINIMUM_CLOSURE_TRACE_REF
    rank: MinimumClosureRank = "CANDIDATE"
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        _require_trace_ref(self.trace_ref)
        _require_candidate_rank(self.rank)
        _require_non_empty(self.required_fields)
        _require_non_empty(self.required_evidence)
        _require_non_empty(self.required_identity)


@dataclass(frozen=True)
class MinimumClosureProbe:
    """Observed candidate payload used for audit-only minimum closure checks."""

    carrier_kind: CarrierKind
    present_fields: Tuple[str, ...]
    present_evidence: Tuple[str, ...]
    preserved_identity: Tuple[str, ...]
    blocking_residuals: Tuple[str, ...] = ()
    trace_ref: str = MINIMUM_CLOSURE_TRACE_REF
    rank: MinimumClosureRank = "CANDIDATE"
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        _require_trace_ref(self.trace_ref)
        _require_candidate_rank(self.rank)
        _require_non_empty(self.present_fields)
        _require_non_empty(self.present_evidence)
        _require_non_empty(self.preserved_identity)


@dataclass(frozen=True)
class MinimumClosureAuditResult:
    """Outcome for MRK_L(contract, probe) in audit-only mode."""

    carrier_kind: CarrierKind
    status: MinimumClosureStatus
    required_fields_met: bool
    required_evidence_met: bool
    identity_preserved: bool
    no_blocking_residual: bool
    missing_fields: Tuple[str, ...]
    missing_evidence: Tuple[str, ...]
    missing_identity: Tuple[str, ...]
    trace_ref: str = MINIMUM_CLOSURE_TRACE_REF
    rank: MinimumClosureRank = "CANDIDATE"
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        _require_trace_ref(self.trace_ref)
        _require_candidate_rank(self.rank)


def _missing(required: Tuple[str, ...], observed: Tuple[str, ...]) -> Tuple[str, ...]:
    observed_set = set(observed)
    return tuple(item for item in required if item not in observed_set)


def audit_minimum_closure(
    contract: MinimumClosureContract, probe: MinimumClosureProbe
) -> MinimumClosureAuditResult:
    """Evaluate MRK_L in audit-only mode for one carrier contract."""
    if contract.carrier_kind != probe.carrier_kind:
        raise ValueError(FailureCode.M_CX_02.value)

    missing_fields = _missing(contract.required_fields, probe.present_fields)
    missing_evidence = _missing(contract.required_evidence, probe.present_evidence)
    missing_identity = _missing(contract.required_identity, probe.preserved_identity)

    required_fields_met = not missing_fields
    required_evidence_met = not missing_evidence
    identity_preserved = not missing_identity
    no_blocking_residual = not probe.blocking_residuals

    status: MinimumClosureStatus = (
        "MINIMUM_CLOSURE_MET"
        if (
            required_fields_met
            and required_evidence_met
            and identity_preserved
            and no_blocking_residual
        )
        else "MINIMUM_CLOSURE_NOT_MET"
    )
    return MinimumClosureAuditResult(
        carrier_kind=contract.carrier_kind,
        status=status,
        required_fields_met=required_fields_met,
        required_evidence_met=required_evidence_met,
        identity_preserved=identity_preserved,
        no_blocking_residual=no_blocking_residual,
        missing_fields=missing_fields,
        missing_evidence=missing_evidence,
        missing_identity=missing_identity,
        residuals=frozenset(probe.blocking_residuals),
    )


MINIMUM_CLOSURE_CONTRACTS: Tuple[MinimumClosureContract, ...] = (
    MinimumClosureContract(
        carrier_kind="SoundUnitCandidate",
        required_fields=("sound_unit_id", "trace_ref", "rank", "residuals"),
        required_evidence=("sensory_evidence",),
        required_identity=("TraceIdentity", "PhonemicIdentity"),
    ),
    MinimumClosureContract(
        carrier_kind="LetterUnitCandidate",
        required_fields=("letter_unit_id", "trace_ref", "rank", "residuals"),
        required_evidence=("written_evidence",),
        required_identity=("TraceIdentity", "GraphemicIdentity"),
    ),
    MinimumClosureContract(
        carrier_kind="SurfaceWordCandidate",
        required_fields=("surface_word_id", "trace_ref", "rank", "residuals"),
        required_evidence=("written_evidence", "sensory_evidence"),
        required_identity=("TraceIdentity", "SurfaceWordIdentity"),
    ),
    MinimumClosureContract(
        carrier_kind="FormalShapeCandidate",
        required_fields=("formal_shape_id", "trace_ref", "rank", "residuals"),
        required_evidence=("morphological_evidence",),
        required_identity=("TraceIdentity", "SurfaceWordIdentity"),
    ),
    MinimumClosureContract(
        carrier_kind="RootReadinessCandidate",
        required_fields=("root_readiness_id", "trace_ref", "rank", "residuals"),
        required_evidence=("morphological_evidence", "lexical_attestation"),
        required_identity=("TraceIdentity", "RootIdentity"),
    ),
    MinimumClosureContract(
        carrier_kind="WeightReadinessCandidate",
        required_fields=("weight_readiness_id", "trace_ref", "rank", "residuals"),
        required_evidence=("morphological_evidence",),
        required_identity=("TraceIdentity", "PatternIdentity"),
    ),
    MinimumClosureContract(
        carrier_kind="VerbalSignifiedCandidate",
        required_fields=("verbal_signified_id", "trace_ref", "rank", "residuals"),
        required_evidence=("lexical_attestation", "contextual_evidence"),
        required_identity=("TraceIdentity", "LexicalIdentity"),
    ),
    MinimumClosureContract(
        carrier_kind="LexicalSenseCandidate",
        required_fields=("lexical_sense_id", "trace_ref", "rank", "residuals"),
        required_evidence=("lexical_attestation", "contextual_evidence"),
        required_identity=("TraceIdentity", "LexicalIdentity"),
    ),
    MinimumClosureContract(
        carrier_kind="ContractableLexicalUnit",
        required_fields=("contractable_unit_id", "trace_ref", "rank", "residuals"),
        required_evidence=("lexical_attestation", "syntactic_evidence"),
        required_identity=("TraceIdentity", "LexicalIdentity"),
    ),
)

MINIMUM_CLOSURE_CONTRACT_BY_CARRIER: Dict[CarrierKind, MinimumClosureContract] = {
    contract.carrier_kind: contract for contract in MINIMUM_CLOSURE_CONTRACTS
}


def audit_minimum_closure_for_carrier(probe: MinimumClosureProbe) -> MinimumClosureAuditResult:
    """Resolve contract by carrier and execute audit-only MRK_L check."""
    return audit_minimum_closure(
        contract=MINIMUM_CLOSURE_CONTRACT_BY_CARRIER[probe.carrier_kind],
        probe=probe,
    )


__all__ = [
    "CarrierKind",
    "MINIMUM_CLOSURE_CARRIERS",
    "MINIMUM_CLOSURE_CONTRACT_BY_CARRIER",
    "MINIMUM_CLOSURE_CONTRACTS",
    "MINIMUM_CLOSURE_TRACE_REF",
    "MinimumClosureAuditResult",
    "MinimumClosureContract",
    "MinimumClosureProbe",
    "MinimumClosureRank",
    "MinimumClosureStatus",
    "audit_minimum_closure",
    "audit_minimum_closure_for_carrier",
]
