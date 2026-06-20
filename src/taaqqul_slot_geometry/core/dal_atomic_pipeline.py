"""
DAL Atomic Pipeline — DAL_ONLY surface production without role/meaning claims.

Origin: docs/00_MAQOOL_CONSTITUTION.md §5 Rule 1; docs/06_DOMAIN_SLOT_GEOMETRY_CONSTITUTION.md
Authority: docs/15_PROJECT_ROADMAP.md Phase 1 (No leap across layers)
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, unique
from typing import FrozenSet, Literal, Tuple

from taaqqul_slot_geometry.constitution.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.core.letter_registry import LetterGenus
from taaqqul_slot_geometry.core.transition_registry import TransitionVerdict
from taaqqul_slot_geometry.core.vocalized_parser import ParsedUnit, parse_vocalized


_DAL_TRACE_REF = "docs/06_DOMAIN_SLOT_GEOMETRY_CONSTITUTION.md §DAL_ONLY"
_DAL_FORBIDDEN_OUTPUTS = (
    "ROOT_FORM",
    "PATTERN_FORM",
    "TOOL_FORM",
    "MABNI_FORM",
    "LEXICAL_MEANING",
    "ISNAD",
    "IFADAH",
    "HUKM",
)


@unique
class CarrierOperationProfile(str, Enum):
    """Operational profile of a carrier inside DAL_ONLY."""

    CONSONANT_CARRIER = "CONSONANT_CARRIER"
    MADD_CARRIER = "MADD_CARRIER"
    HAMZA_OR_SEAT_CARRIER = "HAMZA_OR_SEAT_CARRIER"


@unique
class HarakaOperation(str, Enum):
    """Outgoing operation produced by a mark attached to a carrier."""

    OPEN_A = "OPEN_A"
    OPEN_U = "OPEN_U"
    OPEN_I = "OPEN_I"
    CLOSE = "CLOSE"
    COMPRESS = "COMPRESS"
    NASALIZE = "NASALIZE"
    LENGTHEN = "LENGTHEN"
    UNRESOLVED = "UNRESOLVED"


@unique
class SurfaceSkeletonStatus(str, Enum):
    """DAL-only status for a surface skeleton candidate."""

    DAL_SKELETON_LICENSED = "DAL_SKELETON_LICENSED"
    DAL_SUSPENDED_MISSING_MARK = "DAL_SUSPENDED_MISSING_MARK"
    DAL_BLOCKED_INITIAL_SUKUN = "DAL_BLOCKED_INITIAL_SUKUN"
    DAL_BRIDGE_REQUIRED_TO_LAFZI = "DAL_BRIDGE_REQUIRED_TO_LAFZI"


@dataclass(frozen=True)
class DalProofObject:
    """Proof bundle for DAL-only candidates."""

    proof_id: str
    domain_id: Literal["DAL_ONLY"]
    checked_gates: Tuple[str, ...]
    preserved_identity: Tuple[str, ...]
    failure_codes: Tuple[str, ...]
    trace: Tuple[str, ...]
    trace_ref: str = _DAL_TRACE_REF
    rank: str = "CANDIDATE"
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if not self.proof_id:
            raise ValueError(FailureCode.M_00_22.value)
        if not self.checked_gates:
            raise ValueError(FailureCode.M_00_22.value)
        if not self.trace_ref:
            raise ValueError(FailureCode.M_00_11.value)
        if self.rank != "CANDIDATE":
            raise ValueError(FailureCode.M_00_10.value)


@dataclass(frozen=True)
class CarrierIdentityProfile:
    """Carrier identity profile in DAL_ONLY."""

    carrier_id: str
    glyph: str
    position_index: int
    profile: CarrierOperationProfile
    allowed_operations: Tuple[str, ...]
    forbidden_outputs: Tuple[str, ...] = _DAL_FORBIDDEN_OUTPUTS
    trace_ref: str = _DAL_TRACE_REF
    rank: str = "CANDIDATE"
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if not self.carrier_id or not self.glyph:
            raise ValueError(FailureCode.M_00_14.value)
        if self.position_index < 0:
            raise ValueError(FailureCode.M_00_22.value)
        if not isinstance(self.profile, CarrierOperationProfile):
            raise ValueError(FailureCode.M_00_22.value)
        if not self.allowed_operations:
            raise ValueError(FailureCode.M_00_22.value)
        if not self.trace_ref:
            raise ValueError(FailureCode.M_00_11.value)
        if self.rank != "CANDIDATE":
            raise ValueError(FailureCode.M_00_10.value)


@dataclass(frozen=True)
class HarakaFunctionSlot:
    """Haraka function attached to a carrier (never independent)."""

    slot_id: str
    carrier_ref: str
    mark_id: str
    outgoing_operation: HarakaOperation
    incoming_edge: str
    outgoing_edge: str
    next_layer_markers: Tuple[str, ...]
    forbidden_outputs: Tuple[str, ...] = _DAL_FORBIDDEN_OUTPUTS
    trace_ref: str = _DAL_TRACE_REF
    rank: str = "CANDIDATE"
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if not self.slot_id or not self.carrier_ref:
            raise ValueError(FailureCode.M_00_22.value)
        if not self.mark_id:
            raise ValueError(FailureCode.M_00_04.value)
        if not isinstance(self.outgoing_operation, HarakaOperation):
            raise ValueError(FailureCode.M_00_22.value)
        if not self.incoming_edge or not self.outgoing_edge:
            raise ValueError(FailureCode.M_00_22.value)
        if not self.trace_ref:
            raise ValueError(FailureCode.M_00_11.value)
        if self.rank != "CANDIDATE":
            raise ValueError(FailureCode.M_00_10.value)


@dataclass(frozen=True)
class SurfaceSkeletonCandidate:
    """DAL-only surface skeleton candidate."""

    skeleton_id: str
    carriers: Tuple[CarrierIdentityProfile, ...]
    haraka_slots: Tuple[HarakaFunctionSlot, ...]
    edge_signature: Tuple[str, ...]
    status: SurfaceSkeletonStatus
    proof: DalProofObject
    forbidden_outputs: Tuple[str, ...] = _DAL_FORBIDDEN_OUTPUTS
    trace_ref: str = _DAL_TRACE_REF
    rank: str = "CANDIDATE"
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if not self.skeleton_id:
            raise ValueError(FailureCode.M_00_22.value)
        if not self.carriers or not self.haraka_slots:
            raise ValueError(FailureCode.M_00_22.value)
        if len(self.carriers) != len(self.haraka_slots):
            raise ValueError(FailureCode.M_00_22.value)
        if not isinstance(self.status, SurfaceSkeletonStatus):
            raise ValueError(FailureCode.M_00_22.value)
        if not self.trace_ref:
            raise ValueError(FailureCode.M_00_11.value)
        if self.rank != "CANDIDATE":
            raise ValueError(FailureCode.M_00_10.value)


@dataclass(frozen=True)
class BridgeRequiredMarker:
    """Marker that DAL candidate needs DalToLafziBridge before role eligibility."""

    marker_id: str
    source_domain: Literal["DAL_ONLY"]
    target_domain: Literal["LAFZI_FORM"]
    required_bridge: Literal["DalToLafziBridge"]
    status: Literal["BRIDGE_REQUIRED"]
    reason: str
    trace_ref: str = _DAL_TRACE_REF
    rank: str = "CANDIDATE"
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if not self.marker_id or not self.reason:
            raise ValueError(FailureCode.M_00_22.value)
        if not self.trace_ref:
            raise ValueError(FailureCode.M_00_11.value)
        if self.rank != "CANDIDATE":
            raise ValueError(FailureCode.M_00_10.value)


@dataclass(frozen=True)
class DalAtomicArtifacts:
    """Aggregated DAL-only outputs for one vocalized surface."""

    carrier_profiles: Tuple[CarrierIdentityProfile, ...]
    haraka_slots: Tuple[HarakaFunctionSlot, ...]
    surface_skeleton: SurfaceSkeletonCandidate
    bridge_required_marker: BridgeRequiredMarker
    trace_ref: str = _DAL_TRACE_REF
    rank: str = "CANDIDATE"
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if not self.carrier_profiles:
            raise ValueError(FailureCode.M_00_22.value)
        if len(self.carrier_profiles) != len(self.haraka_slots):
            raise ValueError(FailureCode.M_00_22.value)
        if not self.trace_ref:
            raise ValueError(FailureCode.M_00_11.value)
        if self.rank != "CANDIDATE":
            raise ValueError(FailureCode.M_00_10.value)


def _profile_for_parsed_unit(unit: ParsedUnit) -> CarrierOperationProfile:
    """Infer DAL carrier operation profile from parsed unit."""
    if unit.letter is None or unit.raw_letter in {"ء", "أ", "إ", "ؤ", "ئ"}:
        return CarrierOperationProfile.HAMZA_OR_SEAT_CARRIER
    if unit.letter is not None and unit.letter.genus == LetterGenus.LONG_VOWEL:
        return CarrierOperationProfile.MADD_CARRIER
    return CarrierOperationProfile.CONSONANT_CARRIER


def _operation_for_mark(mark_id: str) -> HarakaOperation:
    """Map mark identity into DAL haraka operation."""
    mapping = {
        "FATHA": HarakaOperation.OPEN_A,
        "DAMMA": HarakaOperation.OPEN_U,
        "KASRA": HarakaOperation.OPEN_I,
        "SUKUN": HarakaOperation.CLOSE,
        # Specialized marks are preserved as DAL residuals until bridged.
        "SHADDA": HarakaOperation.UNRESOLVED,
        "FATHATAN": HarakaOperation.UNRESOLVED,
        "DAMMATAN": HarakaOperation.UNRESOLVED,
        "KASRATAN": HarakaOperation.UNRESOLVED,
        "MADDAH": HarakaOperation.UNRESOLVED,
        "SUPERSCRIPT_ALIF": HarakaOperation.UNRESOLVED,
        "MISSING": HarakaOperation.UNRESOLVED,
    }
    return mapping.get(mark_id, HarakaOperation.UNRESOLVED)


def _edge_signature(index: int, total: int, operation: HarakaOperation) -> Tuple[str, str]:
    """Build incoming/outgoing edge labels."""
    incoming = "START" if index == 0 else "INTERNAL_WASL"
    outgoing = "FINAL_WAQF" if index == total - 1 else operation.value
    return incoming, outgoing


def build_dal_atomic_artifacts(text: str) -> DalAtomicArtifacts:
    """Generate DAL-only artifacts from vocalized input text."""
    parsed = parse_vocalized(text)
    if not parsed.units:
        raise ValueError(FailureCode.M_00_06.value)

    carriers: list[CarrierIdentityProfile] = []
    harakat: list[HarakaFunctionSlot] = []
    edge_states: list[str] = ["E0"]
    all_residuals: set[str] = set(parsed.residuals)

    for idx, unit in enumerate(parsed.units):
        profile = _profile_for_parsed_unit(unit)
        carrier_id = f"C{idx + 1}"
        carriers.append(
            CarrierIdentityProfile(
                carrier_id=carrier_id,
                glyph=unit.raw_letter,
                position_index=idx,
                profile=profile,
                allowed_operations=(
                    "IDENTIFY_CARRIER",
                    "ATTACH_HARAKA",
                    "COMPUTE_INCOMING_EDGE",
                    "COMPUTE_OUTGOING_EDGE",
                    "LINK_CARRIERS",
                    "PROJECT_WAQF_WASL",
                ),
                residuals=unit.residuals,
            )
        )

        mark_id = unit.mark.mark_id if unit.mark is not None else "MISSING"
        operation = _operation_for_mark(mark_id)
        incoming_edge, outgoing_edge = _edge_signature(idx, len(parsed.units), operation)
        edge_states.append(f"E{idx + 1}")

        slot_residuals = set(unit.residuals)
        if mark_id == "MISSING":
            slot_residuals.add("missing_harakat")
        if mark_id == "SHADDA":
            slot_residuals.add("shadda_requires_identity_expansion_proof")
        if mark_id in {"FATHATAN", "DAMMATAN", "KASRATAN"}:
            slot_residuals.add("tanwin_requires_word_layer")
        if mark_id in {"MADDAH", "SUPERSCRIPT_ALIF"}:
            slot_residuals.add("madd_requires_carrier_compatibility_proof")

        harakat.append(
            HarakaFunctionSlot(
                slot_id=f"H{idx + 1}",
                carrier_ref=carrier_id,
                mark_id=mark_id,
                outgoing_operation=operation,
                incoming_edge=incoming_edge,
                outgoing_edge=outgoing_edge,
                next_layer_markers=(
                    "BRIDGE_REQUIRED_TO_LAFZI",
                    "ROLE_ELIGIBILITY_LOCKED_IN_DAL",
                    "NO_DIRECT_LEXICAL_OR_RELATION_CLAIM",
                ),
                residuals=frozenset(slot_residuals),
            )
        )
        all_residuals |= slot_residuals

    has_initial_sukun = harakat[0].outgoing_operation == HarakaOperation.CLOSE
    has_missing_marks = any(slot.mark_id == "MISSING" for slot in harakat)

    status = SurfaceSkeletonStatus.DAL_SKELETON_LICENSED
    failure_codes: Tuple[str, ...] = ()
    if has_initial_sukun:
        status = SurfaceSkeletonStatus.DAL_BLOCKED_INITIAL_SUKUN
        failure_codes = (FailureCode.M_00_22.value,)
        all_residuals.add("initial_sukun_requires_repair_gate")
        if has_missing_marks:
            all_residuals.add("missing_harakat")
    elif has_missing_marks:
        status = SurfaceSkeletonStatus.DAL_SUSPENDED_MISSING_MARK
    else:
        status = SurfaceSkeletonStatus.DAL_BRIDGE_REQUIRED_TO_LAFZI

    proof = DalProofObject(
        proof_id="DAL-PROOF-1",
        domain_id="DAL_ONLY",
        checked_gates=(
            "NO_INDEPENDENT_MARK",
            "INITIAL_CLOSURE_GATE",
            "WAQF_WASL_PROJECTION_GATE",
        ),
        preserved_identity=tuple(c.glyph for c in carriers),
        failure_codes=failure_codes,
        trace=(_DAL_TRACE_REF, "docs/00_MAQOOL_CONSTITUTION.md §5 Rule 1"),
        residuals=frozenset(all_residuals),
    )

    skeleton = SurfaceSkeletonCandidate(
        skeleton_id="DAL-SKEL-1",
        carriers=tuple(carriers),
        haraka_slots=tuple(harakat),
        edge_signature=tuple(edge_states),
        status=status,
        proof=proof,
        residuals=frozenset(all_residuals),
    )

    bridge_marker = BridgeRequiredMarker(
        marker_id="DAL-BRIDGE-1",
        source_domain="DAL_ONLY",
        target_domain="LAFZI_FORM",
        required_bridge="DalToLafziBridge",
        status="BRIDGE_REQUIRED",
        reason="RoleEligibilityOperations are forbidden before DalToLafziBridge.",
        residuals=frozenset({"bridge_required_to_open_role_eligibility"}),
    )

    return DalAtomicArtifacts(
        carrier_profiles=tuple(carriers),
        haraka_slots=tuple(harakat),
        surface_skeleton=skeleton,
        bridge_required_marker=bridge_marker,
        residuals=frozenset(all_residuals | {"bridge_required_to_open_role_eligibility"}),
    )


def open_role_eligibility_operations(
    bridge_marker: BridgeRequiredMarker,
    bridge_verdict: TransitionVerdict,
) -> Literal["ROLE_ELIGIBILITY_OPEN"]:
    """Open role eligibility only after a licensed DalToLafziBridge."""
    if bridge_marker.required_bridge != "DalToLafziBridge":
        raise ValueError(FailureCode.M_00_09.value)
    if bridge_verdict != TransitionVerdict.LICENSED:
        raise ValueError(
            f"{FailureCode.M_00_09.value}: DalToLafziBridge must be licensed first"
        )
    return "ROLE_ELIGIBILITY_OPEN"
