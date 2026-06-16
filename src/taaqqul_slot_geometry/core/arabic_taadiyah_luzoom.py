"""
Arabic Transitivity & Intransitivity (التعدي واللزوم) — TH8.
Origin: docs/00_MAQOOL_CONSTITUTION.md §5 Rule 10

TH8: Transitivity is a generative function of weight structure.
    T(W) = transitivity_class

The transitivity of a verb is NOT arbitrary — it is determined by the
structural features of its morphological form (الوزن).

Key principle: Morphological augmentation (زيادة) creates transitivity.
    - Gemination (تشديد) → intensification → transitivity
    - Medial alif (ألف وسطية) → reciprocity → transitivity
    - Initial hamza (همزة بادئة) → causation → transitivity
    - Initial nun (نون بادئة) → passivity → intransitivity
    - Initial sin-ta (سين+تاء) → requestative → transitivity
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, unique
from typing import FrozenSet, Tuple

from taaqqul_slot_geometry.constitution.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.core.arabic_weight_pattern import (
    MorphForm,
    TransitivityHint,
    WeightPatternSpec,
    get_weight_pattern,
)


# ══════════════════════════════════════════════════════════════════════════════
# §1  ENUMERATIONS
# ══════════════════════════════════════════════════════════════════════════════


@unique
class TransitivityClass(str, Enum):
    """Formal transitivity classification."""

    LAZIM = "lazim"             # لازم — intransitive
    MUTAADDI_1 = "mutaaddi_1"  # متعدٍ لمفعول واحد
    MUTAADDI_2 = "mutaaddi_2"  # متعدٍ لمفعولين
    MUTAADDI_3 = "mutaaddi_3"  # متعدٍ لثلاثة مفاعيل
    VARIABLE = "variable"      # لازم/متعدٍ حسب السياق


@unique
class TransitivityMechanism(str, Enum):
    """The structural mechanism that determines transitivity."""

    NONE = "none"                   # no augmentation (Form I base)
    GEMINATION = "gemination"       # تشديد (Form II)
    MEDIAL_ALIF = "medial_alif"    # ألف وسطية (Form III)
    INITIAL_HAMZA = "initial_hamza"  # همزة بادئة (Form IV)
    TA_PREFIX = "ta_prefix"         # تاء بادئة (Form V, VI)
    NUN_PREFIX = "nun_prefix"       # نون بادئة (Form VII)
    TA_INFIX = "ta_infix"          # تاء داخلية (Form VIII)
    SIN_TA = "sin_ta"              # سين + تاء (Form X)


# ══════════════════════════════════════════════════════════════════════════════
# §2  CORE ENTITIES
# ══════════════════════════════════════════════════════════════════════════════


@dataclass(frozen=True)
class TransitivityRule:
    """A single transitivity rule derived from weight structure.

    Maps a morphological form to its transitivity class through
    a structural mechanism.

    Parameters
    ----------
    form : MorphForm
        The morphological form this rule applies to.
    transitivity_class : TransitivityClass
        The resulting transitivity classification.
    mechanism : TransitivityMechanism
        The structural feature that determines transitivity.
    explanation : str
        Arabic/linguistic explanation of why this mechanism works.
    object_count : int
        Number of objects the verb can take (0 for intransitive).
    """

    form: MorphForm
    transitivity_class: TransitivityClass
    mechanism: TransitivityMechanism
    explanation: str
    object_count: int
    domain_tag: str = "L0_MORPHOLOGY"
    trace_ref: str = "docs/00_MAQOOL_CONSTITUTION.md §5 Rule 10"
    rank: str = "CANDIDATE"
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if not isinstance(self.form, MorphForm):
            raise ValueError(FailureCode.M_00_22.value)
        if not isinstance(self.transitivity_class, TransitivityClass):
            raise ValueError(FailureCode.M_00_22.value)
        if not isinstance(self.mechanism, TransitivityMechanism):
            raise ValueError(FailureCode.M_00_22.value)
        if not self.explanation:
            raise ValueError(FailureCode.M_00_22.value)
        if self.object_count < 0:
            raise ValueError(FailureCode.M_00_22.value)
        if not self.trace_ref:
            raise ValueError(FailureCode.M_00_11.value)
        if self.rank != "CANDIDATE":
            raise ValueError(FailureCode.M_00_10.value)


@dataclass(frozen=True)
class TransitivityVerdict:
    """Result of transitivity analysis for a specific form.

    Parameters
    ----------
    form : MorphForm
        The analyzed form.
    is_transitive : bool
        Whether the form is transitive.
    is_intransitive : bool
        Whether the form is intransitive.
    is_variable : bool
        Whether transitivity depends on context.
    object_count : int
        Number of objects the verb takes.
    mechanism : TransitivityMechanism
        The determining mechanism.
    """

    form: MorphForm
    is_transitive: bool
    is_intransitive: bool
    is_variable: bool
    object_count: int
    mechanism: TransitivityMechanism
    domain_tag: str = "L0_MORPHOLOGY"
    trace_ref: str = "docs/00_MAQOOL_CONSTITUTION.md §5 Rule 10"
    rank: str = "CANDIDATE"
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if not isinstance(self.form, MorphForm):
            raise ValueError(FailureCode.M_00_22.value)
        if not self.trace_ref:
            raise ValueError(FailureCode.M_00_11.value)
        if self.rank != "CANDIDATE":
            raise ValueError(FailureCode.M_00_10.value)


# ══════════════════════════════════════════════════════════════════════════════
# §3  TRANSITIVITY RULE TABLE (TH8)
# ══════════════════════════════════════════════════════════════════════════════


def _build_transitivity_rules() -> Tuple[TransitivityRule, ...]:
    """Build the immutable transitivity rule table.

    TH8: Each form's transitivity is determined by its structural features.
    """
    return (
        # Form I: فَعَلَ — base form, transitivity varies
        TransitivityRule(
            form=MorphForm.FORM_I,
            transitivity_class=TransitivityClass.VARIABLE,
            mechanism=TransitivityMechanism.NONE,
            explanation="الفعل المجرد لا علامة له — التعدي واللزوم يُحدَّدان بالسماع",
            object_count=1,
        ),
        # Form II: فَعَّلَ — gemination → intensification → transitive
        TransitivityRule(
            form=MorphForm.FORM_II,
            transitivity_class=TransitivityClass.MUTAADDI_1,
            mechanism=TransitivityMechanism.GEMINATION,
            explanation="التشديد = تكثيف = تعدي. التكرار يُحدث تأثيراً خارجياً",
            object_count=1,
        ),
        # Form III: فَاعَلَ — medial alif → reciprocity → transitive
        TransitivityRule(
            form=MorphForm.FORM_III,
            transitivity_class=TransitivityClass.MUTAADDI_1,
            mechanism=TransitivityMechanism.MEDIAL_ALIF,
            explanation="الألف الوسطية = تبادل = تعدي. المبادلة تتطلب مفعولاً",
            object_count=1,
        ),
        # Form IV: أَفْعَلَ — initial hamza → causation → transitive
        TransitivityRule(
            form=MorphForm.FORM_IV,
            transitivity_class=TransitivityClass.MUTAADDI_1,
            mechanism=TransitivityMechanism.INITIAL_HAMZA,
            explanation="الهمزة البادئة = تسبيب = تعدي. السبب يتطلب مسبَّباً",
            object_count=1,
        ),
        # Form V: تَفَعَّلَ — ta prefix + gemination → reflexive of II → variable
        TransitivityRule(
            form=MorphForm.FORM_V,
            transitivity_class=TransitivityClass.VARIABLE,
            mechanism=TransitivityMechanism.TA_PREFIX,
            explanation="التاء = انعكاس. مطاوعة فَعَّلَ — قد يكون لازماً أو متعدياً",
            object_count=1,
        ),
        # Form VI: تَفَاعَلَ — ta prefix + alif → reciprocal reflexive → variable
        TransitivityRule(
            form=MorphForm.FORM_VI,
            transitivity_class=TransitivityClass.VARIABLE,
            mechanism=TransitivityMechanism.TA_PREFIX,
            explanation="التاء + الألف = تبادل منعكس. قد يكون لازماً أو متعدياً",
            object_count=0,
        ),
        # Form VII: اِنْفَعَلَ — nun prefix → passivity → intransitive
        TransitivityRule(
            form=MorphForm.FORM_VII,
            transitivity_class=TransitivityClass.LAZIM,
            mechanism=TransitivityMechanism.NUN_PREFIX,
            explanation="النون = انفعال = لزوم. المطاوعة تجعل الفعل لازماً حتماً",
            object_count=0,
        ),
        # Form VIII: اِفْتَعَلَ — ta infix → reflexive → variable
        TransitivityRule(
            form=MorphForm.FORM_VIII,
            transitivity_class=TransitivityClass.VARIABLE,
            mechanism=TransitivityMechanism.TA_INFIX,
            explanation="التاء الداخلية = انعكاس. قد يكون لازماً أو متعدياً",
            object_count=1,
        ),
        # Form X: اِسْتَفْعَلَ — sin+ta → requestative → transitive
        TransitivityRule(
            form=MorphForm.FORM_X,
            transitivity_class=TransitivityClass.MUTAADDI_1,
            mechanism=TransitivityMechanism.SIN_TA,
            explanation="السين+التاء = طلب = تعدي. الطلب يتطلب مطلوباً",
            object_count=1,
        ),
    )


TRANSITIVITY_RULES: Tuple[TransitivityRule, ...] = _build_transitivity_rules()
"""Immutable table of transitivity rules for all 9 forms."""


# ══════════════════════════════════════════════════════════════════════════════
# §4  PUBLIC API (pure functions)
# ══════════════════════════════════════════════════════════════════════════════


def determine_transitivity(form: MorphForm) -> TransitivityVerdict:
    """Determine transitivity class from morphological form (TH8).

    This is the implementation of the theorem:
        T(W) = transitivity_class
    Transitivity is a FUNCTION of weight structure, not arbitrary.

    Parameters
    ----------
    form : MorphForm
        The morphological form to analyze.

    Returns
    -------
    TransitivityVerdict
        The transitivity verdict for this form.

    Raises
    ------
    ValueError
        If the form is not recognized.
    """
    for rule in TRANSITIVITY_RULES:
        if rule.form == form:
            is_trans = rule.transitivity_class in (
                TransitivityClass.MUTAADDI_1,
                TransitivityClass.MUTAADDI_2,
                TransitivityClass.MUTAADDI_3,
            )
            is_intrans = rule.transitivity_class == TransitivityClass.LAZIM
            is_var = rule.transitivity_class == TransitivityClass.VARIABLE

            return TransitivityVerdict(
                form=form,
                is_transitive=is_trans,
                is_intransitive=is_intrans,
                is_variable=is_var,
                object_count=rule.object_count,
                mechanism=rule.mechanism,
            )

    raise ValueError(f"{FailureCode.M_00_22.value}: form {form} not in transitivity rules")


def get_transitivity_rule(form: MorphForm) -> TransitivityRule:
    """Look up the transitivity rule for a specific form.

    Parameters
    ----------
    form : MorphForm
        The form to look up.

    Returns
    -------
    TransitivityRule
        The corresponding rule.
    """
    for rule in TRANSITIVITY_RULES:
        if rule.form == form:
            return rule
    raise ValueError(f"{FailureCode.M_00_22.value}: form {form} not in transitivity rules")


def get_all_transitive_rules() -> Tuple[TransitivityRule, ...]:
    """Return all rules that produce transitive forms.

    Pure function.
    """
    return tuple(
        rule
        for rule in TRANSITIVITY_RULES
        if rule.transitivity_class
        in (
            TransitivityClass.MUTAADDI_1,
            TransitivityClass.MUTAADDI_2,
            TransitivityClass.MUTAADDI_3,
        )
    )


def get_all_intransitive_rules() -> Tuple[TransitivityRule, ...]:
    """Return all rules that produce intransitive forms.

    Pure function.
    """
    return tuple(
        rule
        for rule in TRANSITIVITY_RULES
        if rule.transitivity_class == TransitivityClass.LAZIM
    )


def get_object_count(form: MorphForm) -> int:
    """Return the number of objects a form can take.

    Parameters
    ----------
    form : MorphForm
        The morphological form.

    Returns
    -------
    int
        Maximum number of objects this form can take (0 for intransitive).
        Check determine_transitivity(form).is_variable to distinguish
        VARIABLE forms from fixed counts.
    """
    verdict = determine_transitivity(form)
    return verdict.object_count
