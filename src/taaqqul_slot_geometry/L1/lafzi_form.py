"""
L1 LAFZI_FORM contracts (D2_LAFZI_FORM).

Origin: docs/11_LAFZI_FORM_CONSTITUTION.md
Authority: docs/15_PROJECT_ROADMAP.md Phase 1 PR-36
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import FrozenSet, Tuple

from taaqqul_slot_geometry.constitution.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.core.rank import Rank
from taaqqul_slot_geometry.L1.domain_ids import DomainID

LAFZI_FORM_FORBIDDEN_OUTPUTS: Tuple[str, ...] = (
    "LEXICAL_MEANING",
    "LEXICAL_ROOT",
    "USAGE",
    "RELATION",
    "TOOL_MEANING",
    "MASDAR_MEANING",
    "TRANSITIVITY",
    "ISNAD",
    "IFADAH",
    "HUKM",
    "TANZIL",
)
LAFZI_FORM_FORBIDDEN_OUTPUTS_SET = frozenset(LAFZI_FORM_FORBIDDEN_OUTPUTS)
TRACE_REF = "docs/11_LAFZI_FORM_CONSTITUTION.md §LAFZI-C2 Contract Refinement"
SOURCE_CONTRACT_REF = "SurfaceSkeletonCandidate"
FORM_CONTRACT_STAGE = "LAFZI_C2"
FORM_ONLY_STATUS = "FORM_ONLY"
NO_ADDITION = "NO_ADDITION"


def _validate_common(
    *,
    trace_ref: str,
    rank: Rank,
    domain_id: DomainID,
    source_domain_id: DomainID,
    source_surface_ref: str,
    source_contract_ref: str,
    required_bridge_ref: str,
    form_contract_stage: str,
    form_only_status: str,
    forbidden_outputs: Tuple[str, ...],
    proof_object_ref: str,
    proof_trace_ref: str,
) -> None:
    if not trace_ref:
        raise ValueError(FailureCode.M_01_14.value)
    if rank != Rank.CANDIDATE:
        raise ValueError(FailureCode.M_01_16.value)
    if domain_id != DomainID.D2_LAFZI_FORM:
        raise ValueError(FailureCode.M_00_22.value)
    if source_domain_id != DomainID.D1_DAL_ONLY:
        raise ValueError(FailureCode.M_00_09.value)
    if not source_surface_ref:
        raise ValueError(FailureCode.M_00_22.value)
    if source_contract_ref != SOURCE_CONTRACT_REF:
        raise ValueError(FailureCode.M_00_22.value)
    if required_bridge_ref != "DalToLafziBridgeSpec":
        raise ValueError(FailureCode.M_00_22.value)
    if form_contract_stage != FORM_CONTRACT_STAGE:
        raise ValueError(FailureCode.M_00_22.value)
    if form_only_status != FORM_ONLY_STATUS:
        raise ValueError(FailureCode.M_00_22.value)
    if not forbidden_outputs:
        raise ValueError(FailureCode.M_00_22.value)
    if not set(forbidden_outputs).issuperset(LAFZI_FORM_FORBIDDEN_OUTPUTS_SET):
        raise ValueError(FailureCode.M_00_22.value)
    if not proof_object_ref and not proof_trace_ref:
        raise ValueError(FailureCode.M_00_22.value)


def _validate_arity(arity: int, allowed: FrozenSet[int]) -> None:
    if arity not in allowed:
        raise ValueError(FailureCode.M_00_22.value)


def _validate_no_addition(addition_status: str) -> None:
    if addition_status != NO_ADDITION:
        raise ValueError(FailureCode.M_00_22.value)


@dataclass(frozen=True)
class RootFormCandidate:
    candidate_id: str
    root_form: str
    source_surface_ref: str
    lexical_root_ref: str = ""
    proof_object_ref: str = ""
    proof_trace_ref: str = ""
    source_contract_ref: str = SOURCE_CONTRACT_REF
    required_bridge_ref: str = "DalToLafziBridgeSpec"
    form_contract_stage: str = FORM_CONTRACT_STAGE
    form_only_status: str = FORM_ONLY_STATUS
    arity: int = 3
    source_domain_id: DomainID = DomainID.D1_DAL_ONLY
    domain_id: DomainID = DomainID.D2_LAFZI_FORM
    forbidden_outputs: Tuple[str, ...] = LAFZI_FORM_FORBIDDEN_OUTPUTS
    trace_ref: str = TRACE_REF
    rank: Rank = Rank.CANDIDATE
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if not self.candidate_id or not self.root_form:
            raise ValueError(FailureCode.M_00_22.value)
        if self.lexical_root_ref:
            raise ValueError(FailureCode.M_00_22.value)
        _validate_arity(self.arity, frozenset({3, 4}))
        _validate_common(
            trace_ref=self.trace_ref,
            rank=self.rank,
            domain_id=self.domain_id,
            source_domain_id=self.source_domain_id,
            source_surface_ref=self.source_surface_ref,
            source_contract_ref=self.source_contract_ref,
            required_bridge_ref=self.required_bridge_ref,
            form_contract_stage=self.form_contract_stage,
            form_only_status=self.form_only_status,
            forbidden_outputs=self.forbidden_outputs,
            proof_object_ref=self.proof_object_ref,
            proof_trace_ref=self.proof_trace_ref,
        )


@dataclass(frozen=True)
class PatternFormCandidate:
    candidate_id: str
    pattern_form: str
    source_surface_ref: str
    lexical_meaning_ref: str = ""
    proof_object_ref: str = ""
    proof_trace_ref: str = ""
    source_contract_ref: str = SOURCE_CONTRACT_REF
    required_bridge_ref: str = "DalToLafziBridgeSpec"
    form_contract_stage: str = FORM_CONTRACT_STAGE
    form_only_status: str = FORM_ONLY_STATUS
    source_domain_id: DomainID = DomainID.D1_DAL_ONLY
    domain_id: DomainID = DomainID.D2_LAFZI_FORM
    forbidden_outputs: Tuple[str, ...] = LAFZI_FORM_FORBIDDEN_OUTPUTS
    trace_ref: str = TRACE_REF
    rank: Rank = Rank.CANDIDATE
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if not self.candidate_id or not self.pattern_form:
            raise ValueError(FailureCode.M_00_22.value)
        if self.lexical_meaning_ref:
            raise ValueError(FailureCode.M_00_22.value)
        _validate_common(
            trace_ref=self.trace_ref,
            rank=self.rank,
            domain_id=self.domain_id,
            source_domain_id=self.source_domain_id,
            source_surface_ref=self.source_surface_ref,
            source_contract_ref=self.source_contract_ref,
            required_bridge_ref=self.required_bridge_ref,
            form_contract_stage=self.form_contract_stage,
            form_only_status=self.form_only_status,
            forbidden_outputs=self.forbidden_outputs,
            proof_object_ref=self.proof_object_ref,
            proof_trace_ref=self.proof_trace_ref,
        )


@dataclass(frozen=True)
class WordFormCandidate:
    candidate_id: str
    word_form: str
    source_surface_ref: str
    proof_object_ref: str = ""
    proof_trace_ref: str = ""
    source_contract_ref: str = SOURCE_CONTRACT_REF
    required_bridge_ref: str = "DalToLafziBridgeSpec"
    form_contract_stage: str = FORM_CONTRACT_STAGE
    form_only_status: str = FORM_ONLY_STATUS
    source_domain_id: DomainID = DomainID.D1_DAL_ONLY
    domain_id: DomainID = DomainID.D2_LAFZI_FORM
    forbidden_outputs: Tuple[str, ...] = LAFZI_FORM_FORBIDDEN_OUTPUTS
    trace_ref: str = TRACE_REF
    rank: Rank = Rank.CANDIDATE
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if not self.candidate_id or not self.word_form:
            raise ValueError(FailureCode.M_00_22.value)
        _validate_common(
            trace_ref=self.trace_ref,
            rank=self.rank,
            domain_id=self.domain_id,
            source_domain_id=self.source_domain_id,
            source_surface_ref=self.source_surface_ref,
            source_contract_ref=self.source_contract_ref,
            required_bridge_ref=self.required_bridge_ref,
            form_contract_stage=self.form_contract_stage,
            form_only_status=self.form_only_status,
            forbidden_outputs=self.forbidden_outputs,
            proof_object_ref=self.proof_object_ref,
            proof_trace_ref=self.proof_trace_ref,
        )


@dataclass(frozen=True)
class BareTriliteralVerbFormCandidate:
    candidate_id: str
    consonant_skeleton: str
    source_surface_ref: str
    transitivity_profile_ref: str = ""
    isnad_ref: str = ""
    proof_object_ref: str = ""
    proof_trace_ref: str = ""
    addition_status: str = NO_ADDITION
    source_contract_ref: str = SOURCE_CONTRACT_REF
    required_bridge_ref: str = "DalToLafziBridgeSpec"
    form_contract_stage: str = FORM_CONTRACT_STAGE
    form_only_status: str = FORM_ONLY_STATUS
    arity: int = 3
    source_domain_id: DomainID = DomainID.D1_DAL_ONLY
    domain_id: DomainID = DomainID.D2_LAFZI_FORM
    forbidden_outputs: Tuple[str, ...] = LAFZI_FORM_FORBIDDEN_OUTPUTS
    trace_ref: str = TRACE_REF
    rank: Rank = Rank.CANDIDATE
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if not self.candidate_id or not self.consonant_skeleton:
            raise ValueError(FailureCode.M_00_22.value)
        if self.transitivity_profile_ref or self.isnad_ref:
            raise ValueError(FailureCode.M_00_22.value)
        _validate_arity(self.arity, frozenset({3}))
        _validate_no_addition(self.addition_status)
        _validate_common(
            trace_ref=self.trace_ref,
            rank=self.rank,
            domain_id=self.domain_id,
            source_domain_id=self.source_domain_id,
            source_surface_ref=self.source_surface_ref,
            source_contract_ref=self.source_contract_ref,
            required_bridge_ref=self.required_bridge_ref,
            form_contract_stage=self.form_contract_stage,
            form_only_status=self.form_only_status,
            forbidden_outputs=self.forbidden_outputs,
            proof_object_ref=self.proof_object_ref,
            proof_trace_ref=self.proof_trace_ref,
        )


@dataclass(frozen=True)
class BareQuadriliteralVerbFormCandidate:
    candidate_id: str
    consonant_skeleton: str
    source_surface_ref: str
    transitivity_profile_ref: str = ""
    isnad_ref: str = ""
    proof_object_ref: str = ""
    proof_trace_ref: str = ""
    addition_status: str = NO_ADDITION
    source_contract_ref: str = SOURCE_CONTRACT_REF
    required_bridge_ref: str = "DalToLafziBridgeSpec"
    form_contract_stage: str = FORM_CONTRACT_STAGE
    form_only_status: str = FORM_ONLY_STATUS
    arity: int = 4
    source_domain_id: DomainID = DomainID.D1_DAL_ONLY
    domain_id: DomainID = DomainID.D2_LAFZI_FORM
    forbidden_outputs: Tuple[str, ...] = LAFZI_FORM_FORBIDDEN_OUTPUTS
    trace_ref: str = TRACE_REF
    rank: Rank = Rank.CANDIDATE
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if not self.candidate_id or not self.consonant_skeleton:
            raise ValueError(FailureCode.M_00_22.value)
        if self.transitivity_profile_ref or self.isnad_ref:
            raise ValueError(FailureCode.M_00_22.value)
        _validate_arity(self.arity, frozenset({4}))
        _validate_no_addition(self.addition_status)
        _validate_common(
            trace_ref=self.trace_ref,
            rank=self.rank,
            domain_id=self.domain_id,
            source_domain_id=self.source_domain_id,
            source_surface_ref=self.source_surface_ref,
            source_contract_ref=self.source_contract_ref,
            required_bridge_ref=self.required_bridge_ref,
            form_contract_stage=self.form_contract_stage,
            form_only_status=self.form_only_status,
            forbidden_outputs=self.forbidden_outputs,
            proof_object_ref=self.proof_object_ref,
            proof_trace_ref=self.proof_trace_ref,
        )


@dataclass(frozen=True)
class TriliteralJamidFormCandidate:
    candidate_id: str
    jamid_form: str
    source_surface_ref: str
    proof_object_ref: str = ""
    proof_trace_ref: str = ""
    addition_status: str = NO_ADDITION
    source_contract_ref: str = SOURCE_CONTRACT_REF
    required_bridge_ref: str = "DalToLafziBridgeSpec"
    form_contract_stage: str = FORM_CONTRACT_STAGE
    form_only_status: str = FORM_ONLY_STATUS
    arity: int = 3
    source_domain_id: DomainID = DomainID.D1_DAL_ONLY
    domain_id: DomainID = DomainID.D2_LAFZI_FORM
    forbidden_outputs: Tuple[str, ...] = LAFZI_FORM_FORBIDDEN_OUTPUTS
    trace_ref: str = TRACE_REF
    rank: Rank = Rank.CANDIDATE
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if not self.candidate_id or not self.jamid_form:
            raise ValueError(FailureCode.M_00_22.value)
        _validate_arity(self.arity, frozenset({3}))
        _validate_no_addition(self.addition_status)
        _validate_common(
            trace_ref=self.trace_ref,
            rank=self.rank,
            domain_id=self.domain_id,
            source_domain_id=self.source_domain_id,
            source_surface_ref=self.source_surface_ref,
            source_contract_ref=self.source_contract_ref,
            required_bridge_ref=self.required_bridge_ref,
            form_contract_stage=self.form_contract_stage,
            form_only_status=self.form_only_status,
            forbidden_outputs=self.forbidden_outputs,
            proof_object_ref=self.proof_object_ref,
            proof_trace_ref=self.proof_trace_ref,
        )


@dataclass(frozen=True)
class QuadriliteralJamidFormCandidate:
    candidate_id: str
    jamid_form: str
    source_surface_ref: str
    proof_object_ref: str = ""
    proof_trace_ref: str = ""
    addition_status: str = NO_ADDITION
    source_contract_ref: str = SOURCE_CONTRACT_REF
    required_bridge_ref: str = "DalToLafziBridgeSpec"
    form_contract_stage: str = FORM_CONTRACT_STAGE
    form_only_status: str = FORM_ONLY_STATUS
    arity: int = 4
    source_domain_id: DomainID = DomainID.D1_DAL_ONLY
    domain_id: DomainID = DomainID.D2_LAFZI_FORM
    forbidden_outputs: Tuple[str, ...] = LAFZI_FORM_FORBIDDEN_OUTPUTS
    trace_ref: str = TRACE_REF
    rank: Rank = Rank.CANDIDATE
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if not self.candidate_id or not self.jamid_form:
            raise ValueError(FailureCode.M_00_22.value)
        _validate_arity(self.arity, frozenset({4}))
        _validate_no_addition(self.addition_status)
        _validate_common(
            trace_ref=self.trace_ref,
            rank=self.rank,
            domain_id=self.domain_id,
            source_domain_id=self.source_domain_id,
            source_surface_ref=self.source_surface_ref,
            source_contract_ref=self.source_contract_ref,
            required_bridge_ref=self.required_bridge_ref,
            form_contract_stage=self.form_contract_stage,
            form_only_status=self.form_only_status,
            forbidden_outputs=self.forbidden_outputs,
            proof_object_ref=self.proof_object_ref,
            proof_trace_ref=self.proof_trace_ref,
        )


@dataclass(frozen=True)
class MasdarFormCandidate:
    candidate_id: str
    masdar_form: str
    source_surface_ref: str
    masdar_meaning_ref: str = ""
    proof_object_ref: str = ""
    proof_trace_ref: str = ""
    source_contract_ref: str = SOURCE_CONTRACT_REF
    required_bridge_ref: str = "DalToLafziBridgeSpec"
    form_contract_stage: str = FORM_CONTRACT_STAGE
    form_only_status: str = FORM_ONLY_STATUS
    source_domain_id: DomainID = DomainID.D1_DAL_ONLY
    domain_id: DomainID = DomainID.D2_LAFZI_FORM
    forbidden_outputs: Tuple[str, ...] = LAFZI_FORM_FORBIDDEN_OUTPUTS
    trace_ref: str = TRACE_REF
    rank: Rank = Rank.CANDIDATE
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if not self.candidate_id or not self.masdar_form:
            raise ValueError(FailureCode.M_00_22.value)
        if self.masdar_meaning_ref:
            raise ValueError(FailureCode.M_00_22.value)
        _validate_common(
            trace_ref=self.trace_ref,
            rank=self.rank,
            domain_id=self.domain_id,
            source_domain_id=self.source_domain_id,
            source_surface_ref=self.source_surface_ref,
            source_contract_ref=self.source_contract_ref,
            required_bridge_ref=self.required_bridge_ref,
            form_contract_stage=self.form_contract_stage,
            form_only_status=self.form_only_status,
            forbidden_outputs=self.forbidden_outputs,
            proof_object_ref=self.proof_object_ref,
            proof_trace_ref=self.proof_trace_ref,
        )


@dataclass(frozen=True)
class ToolFormCandidate:
    candidate_id: str
    tool_form: str
    source_surface_ref: str
    tool_meaning_ref: str = ""
    proof_object_ref: str = ""
    proof_trace_ref: str = ""
    source_contract_ref: str = SOURCE_CONTRACT_REF
    required_bridge_ref: str = "DalToLafziBridgeSpec"
    form_contract_stage: str = FORM_CONTRACT_STAGE
    form_only_status: str = FORM_ONLY_STATUS
    source_domain_id: DomainID = DomainID.D1_DAL_ONLY
    domain_id: DomainID = DomainID.D2_LAFZI_FORM
    forbidden_outputs: Tuple[str, ...] = LAFZI_FORM_FORBIDDEN_OUTPUTS
    trace_ref: str = TRACE_REF
    rank: Rank = Rank.CANDIDATE
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if not self.candidate_id or not self.tool_form:
            raise ValueError(FailureCode.M_00_22.value)
        if self.tool_meaning_ref:
            raise ValueError(FailureCode.M_00_22.value)
        _validate_common(
            trace_ref=self.trace_ref,
            rank=self.rank,
            domain_id=self.domain_id,
            source_domain_id=self.source_domain_id,
            source_surface_ref=self.source_surface_ref,
            source_contract_ref=self.source_contract_ref,
            required_bridge_ref=self.required_bridge_ref,
            form_contract_stage=self.form_contract_stage,
            form_only_status=self.form_only_status,
            forbidden_outputs=self.forbidden_outputs,
            proof_object_ref=self.proof_object_ref,
            proof_trace_ref=self.proof_trace_ref,
        )


@dataclass(frozen=True)
class MabniNounFormCandidate:
    candidate_id: str
    mabni_form: str
    source_surface_ref: str
    proof_object_ref: str = ""
    proof_trace_ref: str = ""
    source_contract_ref: str = SOURCE_CONTRACT_REF
    required_bridge_ref: str = "DalToLafziBridgeSpec"
    form_contract_stage: str = FORM_CONTRACT_STAGE
    form_only_status: str = FORM_ONLY_STATUS
    source_domain_id: DomainID = DomainID.D1_DAL_ONLY
    domain_id: DomainID = DomainID.D2_LAFZI_FORM
    forbidden_outputs: Tuple[str, ...] = LAFZI_FORM_FORBIDDEN_OUTPUTS
    trace_ref: str = TRACE_REF
    rank: Rank = Rank.CANDIDATE
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if not self.candidate_id or not self.mabni_form:
            raise ValueError(FailureCode.M_00_22.value)
        _validate_common(
            trace_ref=self.trace_ref,
            rank=self.rank,
            domain_id=self.domain_id,
            source_domain_id=self.source_domain_id,
            source_surface_ref=self.source_surface_ref,
            source_contract_ref=self.source_contract_ref,
            required_bridge_ref=self.required_bridge_ref,
            form_contract_stage=self.form_contract_stage,
            form_only_status=self.form_only_status,
            forbidden_outputs=self.forbidden_outputs,
            proof_object_ref=self.proof_object_ref,
            proof_trace_ref=self.proof_trace_ref,
        )


__all__ = [
    "BareQuadriliteralVerbFormCandidate",
    "BareTriliteralVerbFormCandidate",
    "FORM_CONTRACT_STAGE",
    "FORM_ONLY_STATUS",
    "LAFZI_FORM_FORBIDDEN_OUTPUTS",
    "MabniNounFormCandidate",
    "MasdarFormCandidate",
    "NO_ADDITION",
    "PatternFormCandidate",
    "QuadriliteralJamidFormCandidate",
    "RootFormCandidate",
    "SOURCE_CONTRACT_REF",
    "ToolFormCandidate",
    "TriliteralJamidFormCandidate",
    "WordFormCandidate",
]
