"""
AlgebraicReference — الإحالة الجبرية المرخّصة.

Origin: docs/00_MAQOOL_CONSTITUTION.md §5 Rules 6, 7, 8
Authority: docs/00_MAQOOL_CONSTITUTION.md §6 (Layer Order)

Architecture:
    الإحالة الجبرية هي دالة جزئية مرخّصة بين طبقتين:
        ref_t : A_i ⇀ A_{i+1}
    تحفظ هوية الحامل، وتمنع القفز، وتنتج إما:
        مرشّحًا (Licensed)، أو معلّقًا (Deferred)، أو ممنوعًا (Blocked).

    Every algebraic reference must satisfy:
        1. Domain declared (عيّن المجال)
        2. Carrier identified (عيّن الحامل)
        3. Identity preserved (حُفظت الهوية)
        4. Condition holds (تحقّق الشرط)
        5. Cause exists (قام السبب)
        6. Preventer absent (انتفى المانع)
        7. Rank preserved (حُفظت الرتبة)
        8. Residuals declared (سُجّلت البقايا)

    Composition law:
        g ∘ f is valid iff target(f) == source(g) AND both licensed.
        No-Leap: cannot skip intermediate layers.

    Same-layer refinement:
        Some reference types operate within the same layer (e.g., syntactic
        relations within COMPOSITION). These are classified as REFINEMENT,
        not TRANSITION, and are subject to different constraints.

    This module is binding on ALL agents working on this codebase.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, unique
from typing import FrozenSet, Tuple

from taaqqul_slot_geometry.constitution.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.core.rank import Rank


# ══════════════════════════════════════════════════════════════════════════════
# §1  REFERENCE LAYER (طبقات الإحالة)
# ══════════════════════════════════════════════════════════════════════════════


@unique
class ReferenceLayer(str, Enum):
    """The 12 layers of the algebraic reference chain.

    Origin: docs/00_MAQOOL_CONSTITUTION.md §6

    Each layer is a type domain. References are partial functions
    between adjacent layers only (No-Leap Axiom).
    """

    DIGITAL = "digital"          # A0: Unicode codepoints
    GLYPH = "glyph"             # A1: Visual glyphs
    LETTER_MARK = "letter_mark"  # A2: Letters and diacritical marks
    VOCALIZED = "vocalized"      # A3: Vocalized units (letter + haraka)
    SYLLABLE = "syllable"        # A4: Syllable patterns
    LAFZ = "lafz"               # A5: Closed lafz (phonological word)
    MUFRAD = "mufrad"           # A6: Classified mufrad (word candidate)
    WORD = "word"               # A7: Contractually-ready word
    COMPOSITION = "composition"  # A8: Syntactic composition
    IFADAH = "ifadah"           # A9: Benefit/utterance
    HUKM = "hukm"              # A10: Judgment with evidence
    TANZIL = "tanzil"           # A11: Application to reality


# Canonical layer ordering for adjacency verification
REFERENCE_LAYER_INDEX: dict[str, int] = {layer.value: i for i, layer in enumerate(ReferenceLayer)}


# ══════════════════════════════════════════════════════════════════════════════
# §2  REFERENCE MODE (نمط الإحالة: انتقال أو تنقيح)
# ══════════════════════════════════════════════════════════════════════════════


@unique
class ReferenceMode(str, Enum):
    """Distinguishes transition references from same-layer refinement.

    Origin: docs/00_MAQOOL_CONSTITUTION.md §5 Rule 8

    TRANSITION: source_layer → target_layer (adjacent, different layers)
    REFINEMENT: source_layer → source_layer (same layer, restructuring)
    """

    TRANSITION = "transition"    # Cross-layer: A_i → A_{i+1}
    REFINEMENT = "refinement"    # Same-layer: A_i → A_i (restructuring)


# ══════════════════════════════════════════════════════════════════════════════
# §3  REFERENCE TYPE (أنواع الإحالة)
# ══════════════════════════════════════════════════════════════════════════════


@unique
class ReferenceType(str, Enum):
    """The 12 species of algebraic reference — كل إحالة لها نوعها.

    Origin: docs/00_MAQOOL_CONSTITUTION.md §5 Rules 6, 7, 8

    No reference may cross its layer boundary.
    Each type has its own conditions, preventers, and residuals.
    """

    DIGITAL_REF = "digital_ref"          # Unicode → Glyph
    GLYPH_REF = "glyph_ref"             # Glyph → Letter/Mark
    OPERATIONAL_REF = "operational_ref"   # Letter × Haraka → VocalizedUnit
    SYLLABIC_REF = "syllabic_ref"        # Units → Syllable
    LAFZ_REF = "lafz_ref"               # Syllables → Lafz
    MORPHOLOGICAL_REF = "morphological_ref"  # Lafz → Mufrad
    CONVENTIONAL_REF = "conventional_ref"    # Mufrad → ConventionalMeaning
    COMPOSITIONAL_REF = "compositional_ref"  # Word → Composition (transition)
    SYNTACTIC_REF = "syntactic_ref"      # Composition → Composition (refinement)
    IFADAH_REF = "ifadah_ref"           # Composition → Ifadah
    HUKM_REF = "hukm_ref"              # Ifadah × Evidence → Hukm
    TANZIL_REF = "tanzil_ref"           # Hukm × Manat → Tanzil


# Mapping from ReferenceType to (source_layer, target_layer)
REFERENCE_TYPE_DOMAIN: dict[ReferenceType, tuple[ReferenceLayer, ReferenceLayer]] = {
    ReferenceType.DIGITAL_REF: (ReferenceLayer.DIGITAL, ReferenceLayer.GLYPH),
    ReferenceType.GLYPH_REF: (ReferenceLayer.GLYPH, ReferenceLayer.LETTER_MARK),
    ReferenceType.OPERATIONAL_REF: (ReferenceLayer.LETTER_MARK, ReferenceLayer.VOCALIZED),
    ReferenceType.SYLLABIC_REF: (ReferenceLayer.VOCALIZED, ReferenceLayer.SYLLABLE),
    ReferenceType.LAFZ_REF: (ReferenceLayer.SYLLABLE, ReferenceLayer.LAFZ),
    ReferenceType.MORPHOLOGICAL_REF: (ReferenceLayer.LAFZ, ReferenceLayer.MUFRAD),
    ReferenceType.CONVENTIONAL_REF: (ReferenceLayer.MUFRAD, ReferenceLayer.WORD),
    ReferenceType.COMPOSITIONAL_REF: (ReferenceLayer.WORD, ReferenceLayer.COMPOSITION),
    ReferenceType.SYNTACTIC_REF: (ReferenceLayer.COMPOSITION, ReferenceLayer.COMPOSITION),
    ReferenceType.IFADAH_REF: (ReferenceLayer.COMPOSITION, ReferenceLayer.IFADAH),
    ReferenceType.HUKM_REF: (ReferenceLayer.IFADAH, ReferenceLayer.HUKM),
    ReferenceType.TANZIL_REF: (ReferenceLayer.HUKM, ReferenceLayer.TANZIL),
}

# Mapping from ReferenceType to its mode (transition or refinement)
REFERENCE_TYPE_MODE: dict[ReferenceType, ReferenceMode] = {
    ReferenceType.DIGITAL_REF: ReferenceMode.TRANSITION,
    ReferenceType.GLYPH_REF: ReferenceMode.TRANSITION,
    ReferenceType.OPERATIONAL_REF: ReferenceMode.TRANSITION,
    ReferenceType.SYLLABIC_REF: ReferenceMode.TRANSITION,
    ReferenceType.LAFZ_REF: ReferenceMode.TRANSITION,
    ReferenceType.MORPHOLOGICAL_REF: ReferenceMode.TRANSITION,
    ReferenceType.CONVENTIONAL_REF: ReferenceMode.TRANSITION,
    ReferenceType.COMPOSITIONAL_REF: ReferenceMode.TRANSITION,
    ReferenceType.SYNTACTIC_REF: ReferenceMode.REFINEMENT,
    ReferenceType.IFADAH_REF: ReferenceMode.TRANSITION,
    ReferenceType.HUKM_REF: ReferenceMode.TRANSITION,
    ReferenceType.TANZIL_REF: ReferenceMode.TRANSITION,
}


# ══════════════════════════════════════════════════════════════════════════════
# §4  REFERENCE RESIDUAL (أنواع البقايا المرجعية)
# ══════════════════════════════════════════════════════════════════════════════


@unique
class ReferenceResidualKind(str, Enum):
    """Typed residuals for algebraic references.

    Origin: docs/00_MAQOOL_CONSTITUTION.md §5 Rule 2 (residuals field)

    Residuals must be typed, visible, and rank-affecting.
    No untyped string residuals are permitted.
    """

    IDENTITY_NOT_VERIFIED = "identity_not_verified"
    CONDITION_NOT_VERIFIED = "condition_not_verified"
    CONDITION_FAILED = "condition_failed"
    CAUSE_NOT_ACTIVE = "cause_not_active"
    CAUSE_FAILED = "cause_failed"
    PREVENTER_ACTIVE = "preventer_active"
    OPERATOR_UNLICENSED = "operator_unlicensed"
    COMPOSITION_GAP = "composition_gap"
    PREDECESSOR_FAILED = "predecessor_failed"
    CHAIN_BLOCKED = "chain_blocked"


# ══════════════════════════════════════════════════════════════════════════════
# §5  GATE STATUS (حالة البوابة)
# ══════════════════════════════════════════════════════════════════════════════


@unique
class GateStatus(str, Enum):
    """Verdict status for condition/cause gates.

    Origin: docs/00_MAQOOL_CONSTITUTION.md §5 Rule 5 (named failures)

    Each condition and cause must have an explicit verdict:
    - VERIFIED: condition/cause confirmed to hold
    - NOT_VERIFIED: condition/cause not yet confirmed (defers)
    - FAILED: condition/cause confirmed NOT to hold (blocks)
    """

    VERIFIED = "verified"
    NOT_VERIFIED = "not_verified"
    FAILED = "failed"


# ══════════════════════════════════════════════════════════════════════════════
# §6  REFERENCE STATUS (حالة الإحالة)
# ══════════════════════════════════════════════════════════════════════════════


@unique
class RefStatus(str, Enum):
    """Output status of an algebraic reference operation.

    Origin: docs/00_MAQOOL_CONSTITUTION.md §5 Rules 6, 7, 8

    Every reference operation produces exactly one of these statuses.
    No silent failure is permitted (OA8: Visible Residuals).
    """

    LICENSED = "licensed"     # Transition succeeded — مرخّص
    DEFERRED = "deferred"    # Transition suspended (needs more data) — معلّق
    BLOCKED = "blocked"      # Transition forbidden (preventer active) — ممنوع


# ══════════════════════════════════════════════════════════════════════════════
# §7  RefResult — RESULT OF AN ALGEBRAIC REFERENCE (ناتج الإحالة)
# ══════════════════════════════════════════════════════════════════════════════


@dataclass(frozen=True)
class RefResult:
    """The result of applying an algebraic reference operation.

    Origin: docs/00_MAQOOL_CONSTITUTION.md §5 Rules 6, 7, 8

    Every reference produces a RefResult with:
        - status: LICENSED | DEFERRED | BLOCKED
        - output_layer: which layer the result belongs to
        - identity_preserved: whether Identity(source) ⊆ Identity(target)
        - reason: explanation when not licensed
        - rank: always Rank.CANDIDATE in current phase
        - residuals: accumulated typed residual bundle
        - trace: ordered trace of operations that produced this result

    Parameters
    ----------
    status : RefStatus
        The outcome of the reference operation.
    output_layer : ReferenceLayer
        The target layer of the reference.
    identity_preserved : bool
        Whether identity was preserved (Rule 7).
    reason : str
        Explanation (empty if LICENSED, non-empty otherwise).
    trace_ref : str
        Constitutional reference.
    rank : Rank
        Always Rank.CANDIDATE.
    residuals : FrozenSet[ReferenceResidualKind]
        Typed residual bundle.
    trace : Tuple[str, ...]
        Ordered trace of operations.
    """

    status: RefStatus
    output_layer: ReferenceLayer
    identity_preserved: bool
    reason: str = ""
    trace_ref: str = "docs/00_MAQOOL_CONSTITUTION.md §5 Rules 6,7,8"
    rank: Rank = Rank.CANDIDATE
    residuals: FrozenSet[ReferenceResidualKind] = field(default_factory=frozenset)
    trace: Tuple[str, ...] = ()

    def __post_init__(self) -> None:
        """Birth guard — validates RefResult fields."""
        if not isinstance(self.status, RefStatus):
            raise ValueError(FailureCode.M_CX_33.value)
        if not isinstance(self.output_layer, ReferenceLayer):
            raise ValueError(FailureCode.M_CX_22.value)
        if not self.trace_ref:
            raise ValueError(FailureCode.M_CX_12.value)
        if self.rank != Rank.CANDIDATE:
            raise ValueError(FailureCode.M_CX_09.value)
        if self.status != RefStatus.LICENSED and not self.reason:
            raise ValueError(
                f"{FailureCode.M_CX_08.value}: "
                "non-licensed RefResult must declare a reason (OA8)"
            )

    @property
    def is_licensed(self) -> bool:
        """Whether this result represents a successful reference."""
        return self.status == RefStatus.LICENSED


# ══════════════════════════════════════════════════════════════════════════════
# §8  AlgebraicReference — THE REFERENCE OPERATION (عملية الإحالة)
# ══════════════════════════════════════════════════════════════════════════════


@dataclass(frozen=True)
class AlgebraicReference:
    """A single algebraic reference operation — دالة إحالية جزئية.

    Origin: docs/00_MAQOOL_CONSTITUTION.md §5 Rules 6, 7, 8

    Formula:
        ref_t(x) = y  iff  License(x) holds
        ref_t(x) = Blocked/Deferred(reason)  otherwise

    License conditions (ALL must hold):
        1. Domain_t(x) — source is in the correct layer
        2. Carrier_t(x) — carrier exists and is identified
        3. IdentityPreserved(x, y) — no identity loss (must be proven)
        4. Condition_t(x) — specific transition condition verified
        5. Cause_t(x) — cause for transition verified active
        6. ¬Preventer_t(x) — no active preventer
        7. ResidualsDeclared(x, y) — residuals tracked

    Parameters
    ----------
    reference_type : ReferenceType
        Which species of reference this is.
    source_layer : ReferenceLayer
        The source domain.
    target_layer : ReferenceLayer
        The target domain.
    domain : str
        Domain declaration (what domain is this reference operating in).
    condition : str
        The condition that must hold for licensing.
    condition_verdict : GateStatus
        Whether the condition has been verified to hold.
    cause : str
        The cause (reason) for the transition.
    cause_verdict : GateStatus
        Whether the cause has been verified as active.
    preventers : FrozenSet[str]
        Set of conditions that would block the reference.
    operator_licensed : bool
        Whether the operator performing this reference is licensed.
    identity_evidence_ref : str
        Reference to identity preservation proof. Empty means not proven.
    trace_ref : str
        Constitutional reference.
    rank : Rank
        Always Rank.CANDIDATE.
    residuals : FrozenSet[ReferenceResidualKind]
        Typed residual bundle.
    """

    reference_type: ReferenceType
    source_layer: ReferenceLayer
    target_layer: ReferenceLayer
    domain: str
    condition: str
    condition_verdict: GateStatus
    cause: str
    cause_verdict: GateStatus
    preventers: FrozenSet[str] = field(default_factory=frozenset)
    operator_licensed: bool = True
    identity_evidence_ref: str = ""
    trace_ref: str = "docs/00_MAQOOL_CONSTITUTION.md §5 Rules 6,7,8"
    rank: Rank = Rank.CANDIDATE
    residuals: FrozenSet[ReferenceResidualKind] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        """Birth guard — validates AlgebraicReference fields."""
        if not isinstance(self.reference_type, ReferenceType):
            raise ValueError(FailureCode.M_CX_21.value)
        if not isinstance(self.source_layer, ReferenceLayer):
            raise ValueError(FailureCode.M_CX_21.value)
        if not isinstance(self.target_layer, ReferenceLayer):
            raise ValueError(FailureCode.M_CX_22.value)
        if not self.domain:
            raise ValueError(FailureCode.M_CX_26.value)
        if not self.condition:
            raise ValueError(FailureCode.M_CX_27.value)
        if not self.cause:
            raise ValueError(FailureCode.M_CX_28.value)
        if not isinstance(self.condition_verdict, GateStatus):
            raise ValueError(FailureCode.M_CX_31.value)
        if not isinstance(self.cause_verdict, GateStatus):
            raise ValueError(FailureCode.M_CX_31.value)
        if not self.trace_ref:
            raise ValueError(FailureCode.M_CX_12.value)
        if self.rank != Rank.CANDIDATE:
            raise ValueError(FailureCode.M_CX_09.value)
        # Validate that reference_type matches declared layers
        expected = REFERENCE_TYPE_DOMAIN.get(self.reference_type)
        if expected is not None:
            exp_src, exp_tgt = expected
            if self.source_layer != exp_src:
                raise ValueError(
                    f"{FailureCode.M_CX_21.value}: "
                    f"{self.reference_type.value} requires source={exp_src.value}, "
                    f"got {self.source_layer.value}"
                )
            if self.target_layer != exp_tgt:
                raise ValueError(
                    f"{FailureCode.M_CX_22.value}: "
                    f"{self.reference_type.value} requires target={exp_tgt.value}, "
                    f"got {self.target_layer.value}"
                )
        # Validate adjacency (No-Leap Axiom)
        self._check_adjacency()

    def _check_adjacency(self) -> None:
        """Enforce No-Leap Axiom: source and target must be adjacent or same.

        Origin: docs/00_MAQOOL_CONSTITUTION.md §5 Rule 8

        Same-layer references are only valid for REFINEMENT-mode types.
        """
        src_idx = REFERENCE_LAYER_INDEX[self.source_layer.value]
        tgt_idx = REFERENCE_LAYER_INDEX[self.target_layer.value]
        distance = abs(src_idx - tgt_idx)
        mode = REFERENCE_TYPE_MODE.get(self.reference_type, ReferenceMode.TRANSITION)

        if mode == ReferenceMode.REFINEMENT:
            # Refinement must be same-layer
            if distance != 0:
                raise ValueError(
                    f"{FailureCode.M_CX_29.value}: "
                    f"refinement reference {self.reference_type.value} must be same-layer, "
                    f"got {self.source_layer.value} → {self.target_layer.value}"
                )
        else:
            # Transition must be to adjacent layer (distance == 1 exactly)
            if distance != 1:
                raise ValueError(
                    f"{FailureCode.M_CX_29.value}: "
                    f"transition from {self.source_layer.value} to {self.target_layer.value} "
                    f"requires distance=1, got distance={distance}"
                )

    @property
    def mode(self) -> ReferenceMode:
        """The mode of this reference (transition or refinement)."""
        return REFERENCE_TYPE_MODE.get(self.reference_type, ReferenceMode.TRANSITION)

    def apply(self) -> RefResult:
        """Apply this algebraic reference operation.

        Origin: docs/00_MAQOOL_CONSTITUTION.md §5 Rules 6, 7, 8

        Checks all license conditions and returns a RefResult.
        Identity preservation is no longer assumed — it must be proven
        via identity_evidence_ref. If not proven, result is DEFERRED.

        Returns
        -------
        RefResult
            The result of the reference operation.
        """
        # Check preventer (OA6: Preventer Blocks Transition)
        if self.preventers:
            return RefResult(
                status=RefStatus.BLOCKED,
                output_layer=self.target_layer,
                identity_preserved=False,
                reason=f"preventer_active: {', '.join(sorted(self.preventers))}",
                residuals=self.residuals | frozenset({ReferenceResidualKind.PREVENTER_ACTIVE}),
                trace=(self.reference_type.value,),
            )

        # Check operator license
        if not self.operator_licensed:
            return RefResult(
                status=RefStatus.DEFERRED,
                output_layer=self.target_layer,
                identity_preserved=False,
                reason="operator_not_licensed",
                residuals=self.residuals | frozenset({ReferenceResidualKind.OPERATOR_UNLICENSED}),
                trace=(self.reference_type.value,),
            )

        # Check condition verdict
        if self.condition_verdict == GateStatus.FAILED:
            return RefResult(
                status=RefStatus.BLOCKED,
                output_layer=self.target_layer,
                identity_preserved=False,
                reason=f"condition_failed: {self.condition}",
                residuals=self.residuals | frozenset({ReferenceResidualKind.CONDITION_FAILED}),
                trace=(self.reference_type.value,),
            )
        if self.condition_verdict == GateStatus.NOT_VERIFIED:
            return RefResult(
                status=RefStatus.DEFERRED,
                output_layer=self.target_layer,
                identity_preserved=False,
                reason=f"condition_not_verified: {self.condition}",
                residuals=self.residuals | frozenset({ReferenceResidualKind.CONDITION_NOT_VERIFIED}),
                trace=(self.reference_type.value,),
            )

        # Check cause verdict
        if self.cause_verdict == GateStatus.FAILED:
            return RefResult(
                status=RefStatus.BLOCKED,
                output_layer=self.target_layer,
                identity_preserved=False,
                reason=f"cause_failed: {self.cause}",
                residuals=self.residuals | frozenset({ReferenceResidualKind.CAUSE_FAILED}),
                trace=(self.reference_type.value,),
            )
        if self.cause_verdict == GateStatus.NOT_VERIFIED:
            return RefResult(
                status=RefStatus.DEFERRED,
                output_layer=self.target_layer,
                identity_preserved=False,
                reason=f"cause_not_verified: {self.cause}",
                residuals=self.residuals | frozenset({ReferenceResidualKind.CAUSE_NOT_ACTIVE}),
                trace=(self.reference_type.value,),
            )

        # Check identity preservation — must be explicitly proven
        if not self.identity_evidence_ref:
            return RefResult(
                status=RefStatus.DEFERRED,
                output_layer=self.target_layer,
                identity_preserved=False,
                reason=f"{FailureCode.M_CX_30.value}: no identity_evidence_ref provided",
                residuals=self.residuals | frozenset({ReferenceResidualKind.IDENTITY_NOT_VERIFIED}),
                trace=(self.reference_type.value,),
            )

        # All conditions met — licensed
        return RefResult(
            status=RefStatus.LICENSED,
            output_layer=self.target_layer,
            identity_preserved=True,
            residuals=self.residuals,
            trace=(self.reference_type.value,),
        )


# ══════════════════════════════════════════════════════════════════════════════
# §9  COMPOSITION LAW (قانون التركيب)
# ══════════════════════════════════════════════════════════════════════════════


class ReferenceCompositionError(ValueError):
    """Raised when reference composition violates the No-Leap Composition Law.

    Origin: docs/00_MAQOOL_CONSTITUTION.md §5 Rule 8
    """

    def __init__(self, message: str, failure_code: FailureCode) -> None:
        super().__init__(f"{failure_code.value}: {message}")
        self.failure_code = failure_code


def compose_references(
    first: AlgebraicReference,
    second: AlgebraicReference,
) -> Tuple[RefResult, RefResult]:
    """Compose two algebraic references sequentially: second ∘ first.

    Origin: docs/00_MAQOOL_CONSTITUTION.md §5 Rule 8
    Authority: No-Leap Composition Law

    Conditions for valid composition:
        1. target(first) == source(second) — types must connect
        2. first must be licensed — cannot compose on failed reference
        3. second must be licensed — cannot compose on failed reference

    Parameters
    ----------
    first : AlgebraicReference
        The first reference to apply (inner function).
    second : AlgebraicReference
        The second reference to apply (outer function).

    Returns
    -------
    Tuple[RefResult, RefResult]
        Results of (first.apply(), second.apply()).

    Raises
    ------
    ReferenceCompositionError
        If composition gap exists (target(first) != source(second)).
    """
    # Verify composition is valid: target(first) == source(second)
    if first.target_layer != second.source_layer:
        raise ReferenceCompositionError(
            f"composition gap: target({first.reference_type.value})="
            f"{first.target_layer.value} != source({second.reference_type.value})="
            f"{second.source_layer.value}",
            FailureCode.M_CX_23,
        )

    # Apply first
    result_first = first.apply()

    # If first failed, second cannot proceed
    if not result_first.is_licensed:
        result_second = RefResult(
            status=RefStatus.BLOCKED,
            output_layer=second.target_layer,
            identity_preserved=False,
            reason=f"predecessor_failed: {result_first.reason}",
            residuals=result_first.residuals | frozenset({ReferenceResidualKind.PREDECESSOR_FAILED}),
            trace=result_first.trace + (second.reference_type.value,),
        )
        return result_first, result_second

    # Apply second
    result_second = second.apply()

    return result_first, result_second


def compose_chain(
    references: Tuple[AlgebraicReference, ...],
) -> Tuple[RefResult, ...]:
    """Compose a chain of algebraic references sequentially.

    Origin: docs/00_MAQOOL_CONSTITUTION.md §5 Rule 8
    Authority: No-Leap Composition Law

    The chain must be ordered such that target(refs[i]) == source(refs[i+1]).
    If any reference in the chain fails, all subsequent references are blocked.

    Parameters
    ----------
    references : Tuple[AlgebraicReference, ...]
        Ordered chain of references to compose.

    Returns
    -------
    Tuple[RefResult, ...]
        Results for each reference in the chain.

    Raises
    ------
    ReferenceCompositionError
        If any adjacent pair has a composition gap.
    ValueError
        If the chain is empty.
    """
    if not references:
        raise ValueError(f"{FailureCode.M_CX_32.value}: empty reference chain")

    # Verify all adjacent pairs are composable
    for i in range(len(references) - 1):
        if references[i].target_layer != references[i + 1].source_layer:
            raise ReferenceCompositionError(
                f"composition gap at position {i}→{i+1}: "
                f"target({references[i].reference_type.value})="
                f"{references[i].target_layer.value} != "
                f"source({references[i+1].reference_type.value})="
                f"{references[i+1].source_layer.value}",
                FailureCode.M_CX_23,
            )

    results: list[RefResult] = []
    previous_licensed = True
    accumulated_residuals: frozenset[ReferenceResidualKind] = frozenset()

    for ref in references:
        if not previous_licensed:
            # Predecessor failed — block this and all subsequent
            result = RefResult(
                status=RefStatus.BLOCKED,
                output_layer=ref.target_layer,
                identity_preserved=False,
                reason="predecessor_in_chain_failed",
                residuals=accumulated_residuals | frozenset({ReferenceResidualKind.CHAIN_BLOCKED}),
                trace=tuple(r.reference_type.value for r in references[:len(results) + 1]),
            )
        else:
            result = ref.apply()

        results.append(result)
        previous_licensed = result.is_licensed
        accumulated_residuals = accumulated_residuals | result.residuals

    return tuple(results)
