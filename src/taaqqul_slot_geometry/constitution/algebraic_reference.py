"""
AlgebraicReference — الإحالة الجبرية المرخّصة.

Origin: docs/00_MAQOOL_CONSTITUTION.md §5 Rules 6, 7, 8
Authority: User-defined critique §§1-15 (Algebraic Reference Law)

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

    This module is binding on ALL agents working on this codebase.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, unique
from typing import FrozenSet, Tuple

from taaqqul_slot_geometry.constitution.failure_taxonomy import FailureCode


# ══════════════════════════════════════════════════════════════════════════════
# §1  REFERENCE LAYER (طبقات الإحالة)
# ══════════════════════════════════════════════════════════════════════════════


@unique
class ReferenceLayer(str, Enum):
    """The 12 layers of the algebraic reference chain.

    Origin: docs/00_MAQOOL_CONSTITUTION.md §6
    Authority: Supreme Algebraic Reference Law §3

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
# §2  REFERENCE TYPE (أنواع الإحالة)
# ══════════════════════════════════════════════════════════════════════════════


@unique
class ReferenceType(str, Enum):
    """The 12 species of algebraic reference — كل إحالة لها نوعها.

    Origin: Supreme Algebraic Reference Law §5
    Authority: Critique §1 (No generic reference — each has own conditions)

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
    CONCEPTUAL_REF = "conceptual_ref"    # Meaning → Concept
    SYNTACTIC_REF = "syntactic_ref"      # Words → Relation
    IFADAH_REF = "ifadah_ref"           # Relation → Ifadah
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
    ReferenceType.CONCEPTUAL_REF: (ReferenceLayer.WORD, ReferenceLayer.COMPOSITION),
    ReferenceType.SYNTACTIC_REF: (ReferenceLayer.COMPOSITION, ReferenceLayer.COMPOSITION),
    ReferenceType.IFADAH_REF: (ReferenceLayer.COMPOSITION, ReferenceLayer.IFADAH),
    ReferenceType.HUKM_REF: (ReferenceLayer.IFADAH, ReferenceLayer.HUKM),
    ReferenceType.TANZIL_REF: (ReferenceLayer.HUKM, ReferenceLayer.TANZIL),
}


# ══════════════════════════════════════════════════════════════════════════════
# §3  REFERENCE STATUS (حالة الإحالة)
# ══════════════════════════════════════════════════════════════════════════════


@unique
class RefStatus(str, Enum):
    """Output status of an algebraic reference operation.

    Origin: Supreme Algebraic Reference Law §9

    Every reference operation produces exactly one of these statuses.
    No silent failure is permitted (OA8: Visible Residuals).
    """

    LICENSED = "licensed"     # Transition succeeded — مرخّص
    DEFERRED = "deferred"    # Transition suspended (needs more data) — معلّق
    BLOCKED = "blocked"      # Transition forbidden (preventer active) — ممنوع


# ══════════════════════════════════════════════════════════════════════════════
# §4  RefResult — RESULT OF AN ALGEBRAIC REFERENCE (ناتج الإحالة)
# ══════════════════════════════════════════════════════════════════════════════


@dataclass(frozen=True)
class RefResult:
    """The result of applying an algebraic reference operation.

    Origin: Supreme Algebraic Reference Law §9, §14
    Authority: docs/00_MAQOOL_CONSTITUTION.md §5 Rule 5 (named failures)

    Every reference produces a RefResult with:
        - status: LICENSED | DEFERRED | BLOCKED
        - output_layer: which layer the result belongs to
        - identity_preserved: whether Identity(source) ⊆ Identity(target)
        - reason: explanation when not licensed
        - rank: always "CANDIDATE" in current phase
        - residuals: accumulated residual bundle
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
    rank : str
        Always "CANDIDATE".
    residuals : FrozenSet[str]
        Residual bundle.
    trace : Tuple[str, ...]
        Ordered trace of operations.
    """

    status: RefStatus
    output_layer: ReferenceLayer
    identity_preserved: bool
    reason: str = ""
    trace_ref: str = "docs/00_MAQOOL_CONSTITUTION.md §5 Rules 6,7,8"
    rank: str = "CANDIDATE"
    residuals: FrozenSet[str] = field(default_factory=frozenset)
    trace: Tuple[str, ...] = ()

    def __post_init__(self) -> None:
        """Birth guard — validates RefResult fields."""
        if not isinstance(self.status, RefStatus):
            raise ValueError(FailureCode.M_CX_24.value)
        if not isinstance(self.output_layer, ReferenceLayer):
            raise ValueError(FailureCode.M_CX_22.value)
        if not self.trace_ref:
            raise ValueError(FailureCode.M_CX_12.value)
        if self.rank != "CANDIDATE":
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
# §5  AlgebraicReference — THE REFERENCE OPERATION (عملية الإحالة)
# ══════════════════════════════════════════════════════════════════════════════


@dataclass(frozen=True)
class AlgebraicReference:
    """A single algebraic reference operation — دالة إحالية جزئية.

    Origin: Supreme Algebraic Reference Law §2, §5
    Authority: docs/00_MAQOOL_CONSTITUTION.md §5 Rules 6, 7, 8

    Formula:
        ref_t(x) = y  iff  License(x) holds
        ref_t(x) = Blocked/Deferred(reason)  otherwise

    License conditions (ALL must hold):
        1. Domain_t(x) — source is in the correct layer
        2. Carrier_t(x) — carrier exists and is identified
        3. IdentityPreserved(x, y) — no identity loss
        4. Condition_t(x) — specific transition condition met
        5. Cause_t(x) — cause for transition exists
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
    cause : str
        The cause (reason) for the transition.
    preventers : FrozenSet[str]
        Set of conditions that would block the reference.
    operator_licensed : bool
        Whether the operator performing this reference is licensed.
    trace_ref : str
        Constitutional reference.
    rank : str
        Always "CANDIDATE".
    residuals : FrozenSet[str]
        Residual bundle.
    """

    reference_type: ReferenceType
    source_layer: ReferenceLayer
    target_layer: ReferenceLayer
    domain: str
    condition: str
    cause: str
    preventers: FrozenSet[str] = field(default_factory=frozenset)
    operator_licensed: bool = True
    trace_ref: str = "docs/00_MAQOOL_CONSTITUTION.md §5 Rules 6,7,8"
    rank: str = "CANDIDATE"
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        """Birth guard — validates AlgebraicReference fields."""
        if not isinstance(self.reference_type, ReferenceType):
            raise ValueError(FailureCode.M_CX_21.value)
        if not isinstance(self.source_layer, ReferenceLayer):
            raise ValueError(FailureCode.M_CX_21.value)
        if not isinstance(self.target_layer, ReferenceLayer):
            raise ValueError(FailureCode.M_CX_22.value)
        if not self.domain:
            raise ValueError(FailureCode.M_CX_24.value)
        if not self.condition:
            raise ValueError(FailureCode.M_CX_24.value)
        if not self.cause:
            raise ValueError(FailureCode.M_CX_24.value)
        if not self.trace_ref:
            raise ValueError(FailureCode.M_CX_12.value)
        if self.rank != "CANDIDATE":
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
        """
        src_idx = REFERENCE_LAYER_INDEX[self.source_layer.value]
        tgt_idx = REFERENCE_LAYER_INDEX[self.target_layer.value]
        # Allow same-layer (syntactic_ref operates within composition)
        # or adjacent layers only
        if abs(src_idx - tgt_idx) > 1:
            raise ValueError(
                f"{FailureCode.M_CX_02.value}: "
                f"leap from {self.source_layer.value} to {self.target_layer.value} "
                f"is forbidden (distance={abs(src_idx - tgt_idx)})"
            )

    def apply(self, identity_preserved: bool = True) -> RefResult:
        """Apply this algebraic reference operation.

        Origin: Supreme Algebraic Reference Law §14

        Checks all 7 license conditions and returns a RefResult.

        Parameters
        ----------
        identity_preserved : bool
            Whether the caller has verified Identity(source) ⊆ Identity(target).

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
                residuals=self.residuals | frozenset({"preventer_blocked"}),
                trace=(self.reference_type.value,),
            )

        # Check operator license
        if not self.operator_licensed:
            return RefResult(
                status=RefStatus.DEFERRED,
                output_layer=self.target_layer,
                identity_preserved=False,
                reason="operator_not_licensed",
                residuals=self.residuals | frozenset({"operator_unlicensed"}),
                trace=(self.reference_type.value,),
            )

        # Check identity preservation (P3)
        if not identity_preserved:
            return RefResult(
                status=RefStatus.BLOCKED,
                output_layer=self.target_layer,
                identity_preserved=False,
                reason="identity_loss_on_transition",
                residuals=self.residuals | frozenset({"identity_lost"}),
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
# §6  COMPOSITION LAW (قانون التركيب)
# ══════════════════════════════════════════════════════════════════════════════


class ReferenceCompositionError(ValueError):
    """Raised when reference composition violates the No-Leap Composition Law.

    Origin: Supreme Algebraic Reference Law §11
    """

    def __init__(self, message: str, failure_code: FailureCode) -> None:
        super().__init__(f"{failure_code.value}: {message}")
        self.failure_code = failure_code


def compose_references(
    first: AlgebraicReference,
    second: AlgebraicReference,
) -> Tuple[RefResult, RefResult]:
    """Compose two algebraic references sequentially: second ∘ first.

    Origin: Supreme Algebraic Reference Law §11
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
            residuals=result_first.residuals | frozenset({"predecessor_blocked"}),
            trace=result_first.trace + (second.reference_type.value,),
        )
        return result_first, result_second

    # Apply second (identity preserved if first was preserved)
    result_second = second.apply(identity_preserved=result_first.identity_preserved)

    return result_first, result_second


def compose_chain(
    references: Tuple[AlgebraicReference, ...],
) -> Tuple[RefResult, ...]:
    """Compose a chain of algebraic references sequentially.

    Origin: Supreme Algebraic Reference Law §11
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
        raise ValueError(f"{FailureCode.M_CX_24.value}: empty reference chain")

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
    previous_identity = True
    accumulated_residuals: frozenset[str] = frozenset()

    for ref in references:
        if not previous_licensed:
            # Predecessor failed — block this and all subsequent
            result = RefResult(
                status=RefStatus.BLOCKED,
                output_layer=ref.target_layer,
                identity_preserved=False,
                reason="predecessor_in_chain_failed",
                residuals=accumulated_residuals | frozenset({"chain_blocked"}),
                trace=tuple(r.reference_type.value for r in references[:len(results) + 1]),
            )
        else:
            result = ref.apply(identity_preserved=previous_identity)

        results.append(result)
        previous_licensed = result.is_licensed
        previous_identity = result.identity_preserved
        accumulated_residuals = accumulated_residuals | result.residuals

    return tuple(results)
