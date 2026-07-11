"""
L1 audit-only Minimum Closure contracts (MRK_L) for lexical carriers.

Single-goal claim:
Harden MRK_L audit contracts by requiring proof objects and preserving probe envelope
without opening runtime authority.

Scope:
- RequiredFields inspection
- EvidenceProof-backed evidence requirements (including ANY_OF)
- IdentityProof-backed identity requirements
- Probe envelope preservation in audit result
- Audit-only MRKProof issuance from a successful audit result

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
from taaqqul_slot_geometry.L1.proof_objects import EvidenceProof, IdentityProof, MRKProof, ProofTrace

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
MINIMUM_CLOSURE_CONSTITUTIONAL_SOURCE = "docs/08_PROOF_OBJECT_CONSTITUTION.md"
MINIMUM_CLOSURE_CONTRACT_ID = "MRK_L"
MINIMUM_CLOSURE_CONTRACT_VERSION = "1.1.0"
MINIMUM_CLOSURE_EFFECTIVE_FROM = "2026-07-11"
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
class EvidenceRequirement:
    """Evidence requirement expression with basic ANY_OF / AT_LEAST_N semantics."""

    requirement_id: str
    accepted_kinds: Tuple[str, ...]
    minimum_matches: int = 1

    def __post_init__(self) -> None:
        if not self.requirement_id:
            raise ValueError(FailureCode.M_00_22.value)
        _require_non_empty(self.accepted_kinds)
        if self.minimum_matches < 1 or self.minimum_matches > len(self.accepted_kinds):
            raise ValueError(FailureCode.M_00_22.value)


@dataclass(frozen=True)
class IdentityRequirement:
    """Identity requirement that must be backed by an IdentityProof."""

    requirement_id: str
    identity_kind: str

    def __post_init__(self) -> None:
        if not self.requirement_id or not self.identity_kind:
            raise ValueError(FailureCode.M_00_22.value)


@dataclass(frozen=True)
class MinimumClosureContract:
    """Audit contract describing MRK_L for a single L1 carrier."""

    carrier_kind: CarrierKind
    required_fields: Tuple[str, ...]
    required_evidence: Tuple[EvidenceRequirement, ...]
    required_identity: Tuple[IdentityRequirement, ...]
    contract_id: str = MINIMUM_CLOSURE_CONTRACT_ID
    contract_version: str = MINIMUM_CLOSURE_CONTRACT_VERSION
    constitutional_source: str = MINIMUM_CLOSURE_CONSTITUTIONAL_SOURCE
    effective_from: str = MINIMUM_CLOSURE_EFFECTIVE_FROM
    supersedes: str = "MRK_L@1.0.0"
    trace_ref: str = MINIMUM_CLOSURE_TRACE_REF
    rank: MinimumClosureRank = "CANDIDATE"
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        _require_trace_ref(self.trace_ref)
        _require_candidate_rank(self.rank)
        _require_non_empty(self.required_fields)
        if not self.contract_id or not self.contract_version:
            raise ValueError(FailureCode.M_00_22.value)
        if not self.constitutional_source or not self.effective_from:
            raise ValueError(FailureCode.M_00_22.value)
        if not self.required_evidence or not self.required_identity:
            raise ValueError(FailureCode.M_00_22.value)


@dataclass(frozen=True)
class MinimumClosureProbe:
    """Observed candidate payload used for audit-only minimum closure checks."""

    carrier_kind: CarrierKind
    carrier_id: str
    present_fields: Tuple[str, ...]
    evidence_proofs: Tuple[EvidenceProof, ...]
    identity_proofs: Tuple[IdentityProof, ...]
    blocking_residuals: Tuple[str, ...] = ()
    claimed_identity_kinds: Tuple[str, ...] = ()
    trace_ref: str = MINIMUM_CLOSURE_TRACE_REF
    rank: MinimumClosureRank = "CANDIDATE"
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        _require_trace_ref(self.trace_ref)
        _require_candidate_rank(self.rank)
        if not self.carrier_id:
            raise ValueError(FailureCode.M_00_22.value)
        _require_non_empty(self.present_fields)
        if not self.evidence_proofs:
            raise ValueError(FailureCode.M_00_22.value)
        if not self.identity_proofs and self.claimed_identity_kinds:
            raise ValueError(FailureCode.M_CX_30.value)


@dataclass(frozen=True)
class MinimumClosureAuditResult:
    """Outcome for MRK_L(contract, probe) in audit-only mode."""

    carrier_kind: CarrierKind
    status: MinimumClosureStatus
    contract_id: str
    contract_version: str
    missing_fields: Tuple[str, ...]
    missing_evidence_requirements: Tuple[str, ...]
    missing_identity_requirements: Tuple[str, ...]
    failure_codes: Tuple[FailureCode, ...]
    blocking_residuals: Tuple[str, ...]
    trace_ref: str = MINIMUM_CLOSURE_TRACE_REF
    rank: MinimumClosureRank = "CANDIDATE"
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        _require_trace_ref(self.trace_ref)
        _require_candidate_rank(self.rank)

    @property
    def required_fields_met(self) -> bool:
        return not self.missing_fields

    @property
    def required_evidence_met(self) -> bool:
        return not self.missing_evidence_requirements

    @property
    def identity_requirements_met(self) -> bool:
        return not self.missing_identity_requirements

    @property
    def no_blocking_residual(self) -> bool:
        return not self.blocking_residuals


def _missing(required: Tuple[str, ...], observed: Tuple[str, ...]) -> Tuple[str, ...]:
    observed_set = set(observed)
    return tuple(item for item in required if item not in observed_set)


def _evidence_satisfies_requirement(
    requirement: EvidenceRequirement,
    proof: EvidenceProof,
    probe: MinimumClosureProbe,
) -> bool:
    if proof.proof_kind not in requirement.accepted_kinds:
        return False
    if proof.domain_id != probe.carrier_id:
        return False
    if proof.trace_ref != probe.trace_ref:
        return False
    if proof.trace.trace_ref != probe.trace_ref:
        return False
    proof_residuals = set(proof.residual_codes) | set(proof.residuals)
    if proof_residuals.intersection(set(probe.blocking_residuals)):
        return False
    return True


def _identity_satisfies_requirement(
    requirement: IdentityRequirement,
    proof: IdentityProof,
    probe: MinimumClosureProbe,
) -> bool:
    if proof.proof_kind != requirement.identity_kind:
        return False
    if proof.domain_id != probe.carrier_id:
        return False
    if proof.trace_ref != probe.trace_ref:
        return False
    if proof.trace.trace_ref != probe.trace_ref:
        return False
    return True


def audit_minimum_closure(
    contract: MinimumClosureContract, probe: MinimumClosureProbe
) -> MinimumClosureAuditResult:
    """Evaluate MRK_L in audit-only mode for one carrier contract."""
    if contract.carrier_kind != probe.carrier_kind:
        raise ValueError(FailureCode.M_CX_02.value)

    missing_fields = _missing(contract.required_fields, probe.present_fields)
    missing_evidence_requirements = tuple(
        requirement.requirement_id
        for requirement in contract.required_evidence
        if sum(
            1
            for proof in probe.evidence_proofs
            if _evidence_satisfies_requirement(requirement=requirement, proof=proof, probe=probe)
        )
        < requirement.minimum_matches
    )
    missing_identity_requirements = tuple(
        requirement.requirement_id
        for requirement in contract.required_identity
        if not any(
            _identity_satisfies_requirement(requirement=requirement, proof=proof, probe=probe)
            for proof in probe.identity_proofs
        )
    )
    blocking_residuals = tuple(probe.blocking_residuals)

    failure_codes: list[FailureCode] = []
    if missing_fields or missing_evidence_requirements:
        failure_codes.append(FailureCode.M_00_22)
    if missing_identity_requirements:
        failure_codes.append(FailureCode.M_CX_30)
    if blocking_residuals:
        failure_codes.append(FailureCode.M_CX_31)

    status: MinimumClosureStatus = (
        "MINIMUM_CLOSURE_MET"
        if (
            not missing_fields
            and not missing_evidence_requirements
            and not missing_identity_requirements
            and not blocking_residuals
        )
        else "MINIMUM_CLOSURE_NOT_MET"
    )

    return MinimumClosureAuditResult(
        carrier_kind=contract.carrier_kind,
        status=status,
        contract_id=contract.contract_id,
        contract_version=contract.contract_version,
        missing_fields=missing_fields,
        missing_evidence_requirements=missing_evidence_requirements,
        missing_identity_requirements=missing_identity_requirements,
        failure_codes=tuple(failure_codes),
        blocking_residuals=blocking_residuals,
        trace_ref=probe.trace_ref,
        rank=probe.rank,
        residuals=frozenset(set(probe.residuals) | set(probe.blocking_residuals)),
    )


MINIMUM_CLOSURE_CONTRACTS: Tuple[MinimumClosureContract, ...] = (
    MinimumClosureContract(
        carrier_kind="SoundUnitCandidate",
        required_fields=("sound_unit_id", "trace_ref", "rank", "residuals"),
        required_evidence=(
            EvidenceRequirement(
                requirement_id="sensory_evidence_required",
                accepted_kinds=("sensory_evidence",),
            ),
        ),
        required_identity=(
            IdentityRequirement(requirement_id="trace_identity_required", identity_kind="TraceIdentity"),
            IdentityRequirement(requirement_id="phonemic_identity_required", identity_kind="PhonemicIdentity"),
        ),
    ),
    MinimumClosureContract(
        carrier_kind="LetterUnitCandidate",
        required_fields=("letter_unit_id", "trace_ref", "rank", "residuals"),
        required_evidence=(
            EvidenceRequirement(
                requirement_id="written_evidence_required",
                accepted_kinds=("written_evidence",),
            ),
        ),
        required_identity=(
            IdentityRequirement(requirement_id="trace_identity_required", identity_kind="TraceIdentity"),
            IdentityRequirement(requirement_id="graphemic_identity_required", identity_kind="GraphemicIdentity"),
        ),
    ),
    MinimumClosureContract(
        carrier_kind="SurfaceWordCandidate",
        required_fields=("surface_word_id", "trace_ref", "rank", "residuals"),
        required_evidence=(
            EvidenceRequirement(
                requirement_id="surface_word_entry_evidence",
                accepted_kinds=(
                    "written_evidence",
                    "acoustic_evidence",
                    "licensed_transcription_evidence",
                ),
            ),
        ),
        required_identity=(
            IdentityRequirement(requirement_id="trace_identity_required", identity_kind="TraceIdentity"),
            IdentityRequirement(requirement_id="surface_word_identity_required", identity_kind="SurfaceWordIdentity"),
        ),
    ),
    MinimumClosureContract(
        carrier_kind="FormalShapeCandidate",
        required_fields=("formal_shape_id", "trace_ref", "rank", "residuals"),
        required_evidence=(
            EvidenceRequirement(
                requirement_id="morphological_evidence_required",
                accepted_kinds=("morphological_evidence",),
            ),
        ),
        required_identity=(
            IdentityRequirement(requirement_id="trace_identity_required", identity_kind="TraceIdentity"),
            IdentityRequirement(requirement_id="surface_word_identity_required", identity_kind="SurfaceWordIdentity"),
        ),
    ),
    MinimumClosureContract(
        carrier_kind="RootReadinessCandidate",
        required_fields=("root_readiness_id", "trace_ref", "rank", "residuals"),
        required_evidence=(
            EvidenceRequirement(
                requirement_id="morphological_evidence_required",
                accepted_kinds=("morphological_evidence",),
            ),
            EvidenceRequirement(
                requirement_id="lexical_attestation_required",
                accepted_kinds=("lexical_attestation",),
            ),
        ),
        required_identity=(
            IdentityRequirement(requirement_id="trace_identity_required", identity_kind="TraceIdentity"),
            IdentityRequirement(requirement_id="surface_word_identity_required", identity_kind="SurfaceWordIdentity"),
            IdentityRequirement(
                requirement_id="root_candidate_identity_required",
                identity_kind="RootCandidateIdentity",
            ),
            IdentityRequirement(
                requirement_id="origin_alternative_identity_required",
                identity_kind="OriginAlternativeIdentity",
            ),
        ),
    ),
    MinimumClosureContract(
        carrier_kind="WeightReadinessCandidate",
        required_fields=("weight_readiness_id", "trace_ref", "rank", "residuals"),
        required_evidence=(
            EvidenceRequirement(
                requirement_id="morphological_evidence_required",
                accepted_kinds=("morphological_evidence",),
            ),
        ),
        required_identity=(
            IdentityRequirement(requirement_id="trace_identity_required", identity_kind="TraceIdentity"),
            IdentityRequirement(
                requirement_id="pattern_candidate_identity_required",
                identity_kind="PatternCandidateIdentity",
            ),
        ),
    ),
    MinimumClosureContract(
        carrier_kind="VerbalSignifiedCandidate",
        required_fields=("verbal_signified_id", "trace_ref", "rank", "residuals"),
        required_evidence=(
            EvidenceRequirement(
                requirement_id="formal_binding_evidence_required",
                accepted_kinds=("formal_binding_evidence",),
            ),
            EvidenceRequirement(
                requirement_id="ordered_unit_evidence_required",
                accepted_kinds=("ordered_unit_evidence",),
            ),
            EvidenceRequirement(
                requirement_id="licensed_lafz_boundary_evidence_required",
                accepted_kinds=("licensed_lafz_boundary_evidence",),
            ),
            EvidenceRequirement(
                requirement_id="lexical_reality_evidence_required",
                accepted_kinds=("lexical_reality_evidence",),
            ),
        ),
        required_identity=(
            IdentityRequirement(requirement_id="trace_identity_required", identity_kind="TraceIdentity"),
            IdentityRequirement(requirement_id="lexical_identity_required", identity_kind="LexicalIdentity"),
        ),
    ),
    MinimumClosureContract(
        carrier_kind="LexicalSenseCandidate",
        required_fields=("lexical_sense_id", "trace_ref", "rank", "residuals"),
        required_evidence=(
            EvidenceRequirement(
                requirement_id="lexical_attestation_required",
                accepted_kinds=("lexical_attestation",),
            ),
            EvidenceRequirement(
                requirement_id="contextual_evidence_required",
                accepted_kinds=("contextual_evidence",),
            ),
        ),
        required_identity=(
            IdentityRequirement(requirement_id="trace_identity_required", identity_kind="TraceIdentity"),
            IdentityRequirement(requirement_id="lexical_identity_required", identity_kind="LexicalIdentity"),
        ),
    ),
    MinimumClosureContract(
        carrier_kind="ContractableLexicalUnit",
        required_fields=("contractable_unit_id", "trace_ref", "rank", "residuals"),
        required_evidence=(
            EvidenceRequirement(
                requirement_id="composition_entry_evidence_required",
                accepted_kinds=("composition_entry_evidence",),
            ),
            EvidenceRequirement(
                requirement_id="slot_schema_evidence_required",
                accepted_kinds=("slot_schema_evidence",),
            ),
            EvidenceRequirement(
                requirement_id="lexical_organization_evidence_required",
                accepted_kinds=("lexical_organization_evidence",),
            ),
            EvidenceRequirement(
                requirement_id="path_resolution_evidence_required",
                accepted_kinds=("path_resolution_evidence",),
            ),
        ),
        required_identity=(
            IdentityRequirement(requirement_id="trace_identity_required", identity_kind="TraceIdentity"),
            IdentityRequirement(requirement_id="lexical_identity_required", identity_kind="LexicalIdentity"),
        ),
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


def issue_mrk_proof(
    contract: MinimumClosureContract,
    audit_result: MinimumClosureAuditResult,
    probe: MinimumClosureProbe,
) -> MRKProof:
    """Issue audit-only MRKProof from a successful minimum closure audit result."""
    if audit_result.status != "MINIMUM_CLOSURE_MET":
        raise ValueError(FailureCode.M_00_22.value)
    if contract.carrier_kind != probe.carrier_kind or audit_result.carrier_kind != contract.carrier_kind:
        raise ValueError(FailureCode.M_CX_02.value)
    if audit_result.contract_id != contract.contract_id or audit_result.contract_version != contract.contract_version:
        raise ValueError(FailureCode.M_00_22.value)
    if audit_result.trace_ref != probe.trace_ref:
        raise ValueError(FailureCode.M_01_14.value)
    if audit_result.rank != probe.rank:
        raise ValueError(FailureCode.M_01_16.value)

    evidence_refs = tuple(
        evidence_ref
        for proof in probe.evidence_proofs
        if proof.domain_id == probe.carrier_id
        and proof.trace_ref == probe.trace_ref
        and proof.trace.trace_ref == probe.trace_ref
        for evidence_ref in proof.evidence_refs
    )
    if not evidence_refs:
        raise ValueError(FailureCode.M_00_22.value)

    trace = ProofTrace(
        trace_id=f"trace::{probe.carrier_id}::{contract.contract_id}@{contract.contract_version}",
        trace_ref=probe.trace_ref,
        steps=(f"audit::{contract.carrier_kind}",),
        evidence_refs=evidence_refs,
        residuals=audit_result.residuals,
    )
    return MRKProof(
        proof_id=f"mrk::{probe.carrier_id}::{contract.contract_id}@{contract.contract_version}",
        proof_kind=contract.contract_id,
        domain_id=probe.carrier_id,
        checked_gate_ids=(f"{contract.contract_id}@{contract.contract_version}",),
        checked_bridge_ids=(contract.constitutional_source,),
        preserved_identity_refs=tuple(
            ref
            for proof in probe.identity_proofs
            if proof.domain_id == probe.carrier_id
            and proof.trace_ref == probe.trace_ref
            and proof.trace.trace_ref == probe.trace_ref
            for ref in proof.preserved_identity_refs
        ),
        forbidden_outputs_checked=("runtime_authority", "layer_opening"),
        evidence_refs=evidence_refs,
        residual_codes=tuple(sorted(audit_result.residuals)),
        failure_codes=tuple(code.value for code in audit_result.failure_codes),
        trace=trace,
        trace_ref=probe.trace_ref,
        residuals=audit_result.residuals,
    )


__all__ = [
    "CarrierKind",
    "EvidenceRequirement",
    "IdentityRequirement",
    "MINIMUM_CLOSURE_CARRIERS",
    "MINIMUM_CLOSURE_CONTRACT_BY_CARRIER",
    "MINIMUM_CLOSURE_CONTRACTS",
    "MINIMUM_CLOSURE_CONSTITUTIONAL_SOURCE",
    "MINIMUM_CLOSURE_CONTRACT_ID",
    "MINIMUM_CLOSURE_CONTRACT_VERSION",
    "MINIMUM_CLOSURE_EFFECTIVE_FROM",
    "MINIMUM_CLOSURE_TRACE_REF",
    "MinimumClosureAuditResult",
    "MinimumClosureContract",
    "MinimumClosureProbe",
    "MinimumClosureRank",
    "MinimumClosureStatus",
    "audit_minimum_closure",
    "audit_minimum_closure_for_carrier",
    "issue_mrk_proof",
]
