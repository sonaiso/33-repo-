"""
Arabic Weight Pattern Registry — 9 generative weight patterns (TH7).
Origin: docs/00_MAQOOL_CONSTITUTION.md §5 Rule 10; docs/01_EUCLIDEAN_PROOFS.md §5

Each weight pattern carries generative relations that define
how consonant positions (F=فاء, A=عين, L=لام) interact with
prefixes, infixes, and suffixes to produce licensed word forms.

Mathematical basis:
    ∀W ∈ WeightPattern: W = (positions, prefix, infix, suffix, transitivity_hint)
    positions ∈ {F, A, L} for trilateral; {F, A, L, L2} for quadrilateral
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, unique
from typing import FrozenSet, Optional, Tuple

from taaqqul_slot_geometry.constitution.failure_taxonomy import FailureCode


# ══════════════════════════════════════════════════════════════════════════════
# §1  ENUMERATIONS
# ══════════════════════════════════════════════════════════════════════════════


@unique
class MorphForm(str, Enum):
    """Morphological form identifiers (الأبواب الصرفية).

    These are the 9 canonical Arabic verb forms plus the base root.
    """

    FORM_I = "fa3ala"          # فَعَلَ — Form I (base)
    FORM_II = "fa33ala"        # فَعَّلَ — Form II (intensive/causative)
    FORM_III = "faa3ala"       # فَاعَلَ — Form III (reciprocal)
    FORM_IV = "af3ala"         # أَفْعَلَ — Form IV (causative)
    FORM_V = "tafa33ala"       # تَفَعَّلَ — Form V (reflexive of II)
    FORM_VI = "tafaa3ala"      # تَفَاعَلَ — Form VI (reciprocal reflexive)
    FORM_VII = "infa3ala"      # اِنْفَعَلَ — Form VII (passive/reflexive)
    FORM_VIII = "ifta3ala"     # اِفْتَعَلَ — Form VIII (reflexive)
    FORM_X = "istaf3ala"       # اِسْتَفْعَلَ — Form X (requestative)


@unique
class ConsonantPosition(str, Enum):
    """Root consonant positions in the Arabic morphological template."""

    FA = "F"    # فاء الكلمة — first radical
    AYN = "A"   # عين الكلمة — second radical
    LAM = "L"   # لام الكلمة — third radical
    LAM2 = "L2"  # لام ثانية — fourth radical (quadrilateral only)


@unique
class TransitivityHint(str, Enum):
    """Structural transitivity indicator derived from weight form.

    This is a HINT from the weight structure, not a semantic determination.
    Actual transitivity requires L1+ analysis (TH8).
    """

    TRANSITIVE = "transitive"           # متعدٍ
    INTRANSITIVE = "intransitive"       # لازم
    VARIABLE = "variable"               # لازم/متعدٍ (context-dependent)


# ══════════════════════════════════════════════════════════════════════════════
# §2  CORE ENTITIES
# ══════════════════════════════════════════════════════════════════════════════


@dataclass(frozen=True)
class GenerativeRelation:
    """A single generative relation within a weight pattern.

    Describes how a morphological element (prefix, infix, suffix, or
    consonant gemination) participates in word generation.

    Parameters
    ----------
    element : str
        The morphological element (e.g. "أ" for Form IV prefix).
    position : str
        Where the element appears ("prefix", "infix", "suffix", "gemination").
    function : str
        The morphological function (e.g. "causation", "reciprocity").
    """

    element: str
    position: str
    function: str
    domain_tag: str = "L0_MORPHOLOGY"
    trace_ref: str = "docs/00_MAQOOL_CONSTITUTION.md §5 Rule 10"
    rank: str = "CANDIDATE"
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if not self.element:
            raise ValueError(FailureCode.M_00_22.value)
        if not self.position:
            raise ValueError(FailureCode.M_00_22.value)
        if not self.function:
            raise ValueError(FailureCode.M_00_22.value)
        if not self.trace_ref:
            raise ValueError(FailureCode.M_00_11.value)
        if self.rank != "CANDIDATE":
            raise ValueError(FailureCode.M_00_10.value)


@dataclass(frozen=True)
class WeightPatternSpec:
    """A complete weight pattern specification with generative relations.

    Each pattern defines:
    - The consonant template (which positions are radicals)
    - Prefix/infix/suffix elements
    - Transitivity hint (structural, not semantic)
    - Generative relations that produce word forms

    Parameters
    ----------
    form : MorphForm
        The morphological form identifier.
    arabic_label : str
        Arabic name of the pattern (e.g. "فَعَلَ").
    consonant_positions : Tuple[ConsonantPosition, ...]
        The radical consonant positions in this pattern.
    prefix : str
        Prefix element (empty string if none).
    infix : str
        Infix element (empty string if none).
    suffix : str
        Suffix element (empty string if none).
    has_gemination : bool
        Whether the pattern involves consonant doubling (تشديد).
    transitivity_hint : TransitivityHint
        Structural transitivity indicator.
    generative_relations : Tuple[GenerativeRelation, ...]
        The set of generative relations for this pattern.
    """

    form: MorphForm
    arabic_label: str
    consonant_positions: Tuple[ConsonantPosition, ...]
    prefix: str
    infix: str
    suffix: str
    has_gemination: bool
    transitivity_hint: TransitivityHint
    generative_relations: Tuple[GenerativeRelation, ...]
    domain_tag: str = "L0_MORPHOLOGY"
    trace_ref: str = "docs/00_MAQOOL_CONSTITUTION.md §5 Rule 10"
    rank: str = "CANDIDATE"
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if not self.arabic_label:
            raise ValueError(FailureCode.M_00_22.value)
        if not self.consonant_positions:
            raise ValueError(FailureCode.M_00_22.value)
        if not isinstance(self.form, MorphForm):
            raise ValueError(FailureCode.M_00_22.value)
        if not isinstance(self.transitivity_hint, TransitivityHint):
            raise ValueError(FailureCode.M_00_22.value)
        if not self.trace_ref:
            raise ValueError(FailureCode.M_00_11.value)
        if self.rank != "CANDIDATE":
            raise ValueError(FailureCode.M_00_10.value)


# ══════════════════════════════════════════════════════════════════════════════
# §3  WEIGHT PATTERN REGISTRY (9 patterns)
# ══════════════════════════════════════════════════════════════════════════════

_TRI = (ConsonantPosition.FA, ConsonantPosition.AYN, ConsonantPosition.LAM)
_QUAD = (
    ConsonantPosition.FA,
    ConsonantPosition.AYN,
    ConsonantPosition.LAM,
    ConsonantPosition.LAM2,
)


def _build_registry() -> Tuple[WeightPatternSpec, ...]:
    """Build the immutable registry of 9 weight patterns.

    Returns a frozen tuple (immutable) of all canonical forms.
    """
    return (
        # ── Form I: فَعَلَ ─────────────────────────────────────────────────
        WeightPatternSpec(
            form=MorphForm.FORM_I,
            arabic_label="فَعَلَ",
            consonant_positions=_TRI,
            prefix="",
            infix="",
            suffix="",
            has_gemination=False,
            transitivity_hint=TransitivityHint.VARIABLE,
            generative_relations=(
                GenerativeRelation(
                    element="َ",
                    position="vowel_F",
                    function="base_active",
                ),
                GenerativeRelation(
                    element="َ",
                    position="vowel_A",
                    function="base_active",
                ),
                GenerativeRelation(
                    element="َ",
                    position="vowel_L",
                    function="base_active",
                ),
            ),
        ),
        # ── Form II: فَعَّلَ ────────────────────────────────────────────────
        WeightPatternSpec(
            form=MorphForm.FORM_II,
            arabic_label="فَعَّلَ",
            consonant_positions=_TRI,
            prefix="",
            infix="",
            suffix="",
            has_gemination=True,
            transitivity_hint=TransitivityHint.TRANSITIVE,
            generative_relations=(
                GenerativeRelation(
                    element="ّ",
                    position="gemination_A",
                    function="intensification",
                ),
                GenerativeRelation(
                    element="ّ",
                    position="gemination_A",
                    function="causation",
                ),
            ),
        ),
        # ── Form III: فَاعَلَ ───────────────────────────────────────────────
        WeightPatternSpec(
            form=MorphForm.FORM_III,
            arabic_label="فَاعَلَ",
            consonant_positions=_TRI,
            prefix="",
            infix="ا",
            suffix="",
            has_gemination=False,
            transitivity_hint=TransitivityHint.TRANSITIVE,
            generative_relations=(
                GenerativeRelation(
                    element="ا",
                    position="infix_after_F",
                    function="reciprocity",
                ),
            ),
        ),
        # ── Form IV: أَفْعَلَ ───────────────────────────────────────────────
        WeightPatternSpec(
            form=MorphForm.FORM_IV,
            arabic_label="أَفْعَلَ",
            consonant_positions=_TRI,
            prefix="أ",
            infix="",
            suffix="",
            has_gemination=False,
            transitivity_hint=TransitivityHint.TRANSITIVE,
            generative_relations=(
                GenerativeRelation(
                    element="أ",
                    position="prefix",
                    function="causation",
                ),
            ),
        ),
        # ── Form V: تَفَعَّلَ ───────────────────────────────────────────────
        WeightPatternSpec(
            form=MorphForm.FORM_V,
            arabic_label="تَفَعَّلَ",
            consonant_positions=_TRI,
            prefix="ت",
            infix="",
            suffix="",
            has_gemination=True,
            transitivity_hint=TransitivityHint.VARIABLE,
            generative_relations=(
                GenerativeRelation(
                    element="ت",
                    position="prefix",
                    function="reflexivity",
                ),
                GenerativeRelation(
                    element="ّ",
                    position="gemination_A",
                    function="intensification",
                ),
            ),
        ),
        # ── Form VI: تَفَاعَلَ ──────────────────────────────────────────────
        WeightPatternSpec(
            form=MorphForm.FORM_VI,
            arabic_label="تَفَاعَلَ",
            consonant_positions=_TRI,
            prefix="ت",
            infix="ا",
            suffix="",
            has_gemination=False,
            transitivity_hint=TransitivityHint.VARIABLE,
            generative_relations=(
                GenerativeRelation(
                    element="ت",
                    position="prefix",
                    function="reflexivity",
                ),
                GenerativeRelation(
                    element="ا",
                    position="infix_after_F",
                    function="reciprocity",
                ),
            ),
        ),
        # ── Form VII: اِنْفَعَلَ ────────────────────────────────────────────
        WeightPatternSpec(
            form=MorphForm.FORM_VII,
            arabic_label="اِنْفَعَلَ",
            consonant_positions=_TRI,
            prefix="ان",
            infix="",
            suffix="",
            has_gemination=False,
            transitivity_hint=TransitivityHint.INTRANSITIVE,
            generative_relations=(
                GenerativeRelation(
                    element="ان",
                    position="prefix",
                    function="passivity",
                ),
            ),
        ),
        # ── Form VIII: اِفْتَعَلَ ───────────────────────────────────────────
        WeightPatternSpec(
            form=MorphForm.FORM_VIII,
            arabic_label="اِفْتَعَلَ",
            consonant_positions=_TRI,
            prefix="ا",
            infix="ت",
            suffix="",
            has_gemination=False,
            transitivity_hint=TransitivityHint.VARIABLE,
            generative_relations=(
                GenerativeRelation(
                    element="ا",
                    position="prefix",
                    function="reflexivity",
                ),
                GenerativeRelation(
                    element="ت",
                    position="infix_after_F",
                    function="reflexivity",
                ),
            ),
        ),
        # ── Form X: اِسْتَفْعَلَ ────────────────────────────────────────────
        WeightPatternSpec(
            form=MorphForm.FORM_X,
            arabic_label="اِسْتَفْعَلَ",
            consonant_positions=_TRI,
            prefix="است",
            infix="",
            suffix="",
            has_gemination=False,
            transitivity_hint=TransitivityHint.TRANSITIVE,
            generative_relations=(
                GenerativeRelation(
                    element="است",
                    position="prefix",
                    function="requestative",
                ),
            ),
        ),
    )


# ══════════════════════════════════════════════════════════════════════════════
# §4  PUBLIC API
# ══════════════════════════════════════════════════════════════════════════════

WEIGHT_PATTERN_REGISTRY: Tuple[WeightPatternSpec, ...] = _build_registry()
"""Immutable registry of 9 canonical weight patterns."""


def get_weight_pattern(form: MorphForm) -> WeightPatternSpec:
    """Look up a weight pattern by its form identifier.

    Parameters
    ----------
    form : MorphForm
        The form to look up.

    Returns
    -------
    WeightPatternSpec
        The corresponding weight pattern specification.

    Raises
    ------
    ValueError
        If the form is not found (should never happen with valid MorphForm).
    """
    for spec in WEIGHT_PATTERN_REGISTRY:
        if spec.form == form:
            return spec
    raise ValueError(f"{FailureCode.M_00_22.value}: form {form} not in registry")


def get_all_transitive_forms() -> Tuple[WeightPatternSpec, ...]:
    """Return all forms with TRANSITIVE transitivity hint.

    Pure function — no side effects.
    """
    return tuple(
        spec
        for spec in WEIGHT_PATTERN_REGISTRY
        if spec.transitivity_hint == TransitivityHint.TRANSITIVE
    )


def get_all_intransitive_forms() -> Tuple[WeightPatternSpec, ...]:
    """Return all forms with INTRANSITIVE transitivity hint.

    Pure function — no side effects.
    """
    return tuple(
        spec
        for spec in WEIGHT_PATTERN_REGISTRY
        if spec.transitivity_hint == TransitivityHint.INTRANSITIVE
    )


def get_all_variable_forms() -> Tuple[WeightPatternSpec, ...]:
    """Return all forms with VARIABLE transitivity hint.

    Pure function — no side effects.
    """
    return tuple(
        spec
        for spec in WEIGHT_PATTERN_REGISTRY
        if spec.transitivity_hint == TransitivityHint.VARIABLE
    )
