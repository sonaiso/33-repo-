"""
Arabic Weak Root System (المعتل) — TH9.
Origin: docs/00_MAQOOL_CONSTITUTION.md §5 Rule 10

TH9: Weak roots follow deterministic generative rules.
    M(R, position) = transformation_rule

A "weak root" (جذر معتل) contains one or more weak consonants
(و waw, ي ya, أ/ء hamza) in specific positions. The behavior
of the weak consonant is NOT exceptional — it follows rules
determined by its position in the root.

Classifications:
    - مثال (mithal): weak first radical (واو or ياء in F position)
    - أجوف (ajwaf): weak second radical (واو or ياء in A position)
    - ناقص (naqis): weak third radical (واو or ياء in L position)
    - لفيف مفروق (lafif mafruq): weak first AND third (F + L)
    - لفيف مقرون (lafif maqrun): weak second AND third (A + L)
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, unique
from typing import FrozenSet, Optional, Tuple

from taaqqul_slot_geometry.constitution.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.core.arabic_morphology_generator import (
    GeneratedForm,
    GenerationTarget,
    LicensedRoot,
    RootType,
    apply_alif_madd,
    apply_damma,
    apply_fatha,
    apply_kasra,
    apply_sukun,
)
from taaqqul_slot_geometry.core.arabic_weight_pattern import MorphForm


# ══════════════════════════════════════════════════════════════════════════════
# §1  ENUMERATIONS
# ══════════════════════════════════════════════════════════════════════════════

WEAK_CONSONANTS: FrozenSet[str] = frozenset({"و", "ي", "ء", "أ", "ؤ", "ئ"})
"""The set of weak consonants (حروف العلة) in Arabic."""


@unique
class WeakRootClass(str, Enum):
    """Classification of weak roots by position of weak consonant."""

    MITHAL = "mithal"             # مثال — weak first radical
    AJWAF = "ajwaf"              # أجوف — weak second radical
    NAQIS = "naqis"             # ناقص — weak third radical
    LAFIF_MAFRUQ = "lafif_mafruq"  # لفيف مفروق — weak first + third
    LAFIF_MAQRUN = "lafif_maqrun"  # لفيف مقرون — weak second + third
    SAHIH = "sahih"             # صحيح — sound root (no weak consonants)


@unique
class WeakTransformation(str, Enum):
    """Types of phonological transformation applied to weak consonants."""

    DELETION = "deletion"       # حذف — consonant is deleted
    MUTATION_TO_ALIF = "to_alif"  # قلب إلى ألف
    MUTATION_TO_YA = "to_ya"    # قلب إلى ياء
    MUTATION_TO_WAW = "to_waw"  # قلب إلى واو
    HAMZA_PREFIX = "hamza_prefix"  # إضافة همزة
    VOWEL_CHANGE = "vowel_change"  # تغيير الحركة
    NO_CHANGE = "no_change"     # لا تغيير


# ══════════════════════════════════════════════════════════════════════════════
# §2  CORE ENTITIES
# ══════════════════════════════════════════════════════════════════════════════


@dataclass(frozen=True)
class WeakRootAnalysis:
    """Analysis of a root's weak consonant classification.

    Parameters
    ----------
    root : LicensedRoot
        The root being analyzed.
    classification : WeakRootClass
        The weak root classification.
    weak_positions : Tuple[int, ...]
        Indices of weak consonants (0-based: 0=F, 1=A, 2=L).
    weak_consonants_found : Tuple[str, ...]
        The actual weak consonants found at those positions.
    """

    root: LicensedRoot
    classification: WeakRootClass
    weak_positions: Tuple[int, ...]
    weak_consonants_found: Tuple[str, ...]
    domain_tag: str = "L0_MORPHOLOGY"
    trace_ref: str = "docs/00_MAQOOL_CONSTITUTION.md §5 Rule 10"
    rank: str = "CANDIDATE"
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if not isinstance(self.root, LicensedRoot):
            raise ValueError(FailureCode.M_00_22.value)
        if not isinstance(self.classification, WeakRootClass):
            raise ValueError(FailureCode.M_00_22.value)
        if not self.trace_ref:
            raise ValueError(FailureCode.M_00_11.value)
        if self.rank != "CANDIDATE":
            raise ValueError(FailureCode.M_00_10.value)


@dataclass(frozen=True)
class WeakTransformationRule:
    """A rule for transforming a weak consonant in a specific context.

    Parameters
    ----------
    weak_class : WeakRootClass
        The weak root class this rule applies to.
    target_form : GenerationTarget
        Which generated form triggers this rule.
    transformation : WeakTransformation
        What happens to the weak consonant.
    condition : str
        Human-readable condition for the transformation.
    example_root : str
        Example root demonstrating this rule.
    example_result : str
        Expected result of applying the rule.
    """

    weak_class: WeakRootClass
    target_form: GenerationTarget
    transformation: WeakTransformation
    condition: str
    example_root: str
    example_result: str
    domain_tag: str = "L0_MORPHOLOGY"
    trace_ref: str = "docs/00_MAQOOL_CONSTITUTION.md §5 Rule 10"
    rank: str = "CANDIDATE"
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if not isinstance(self.weak_class, WeakRootClass):
            raise ValueError(FailureCode.M_00_22.value)
        if not isinstance(self.target_form, GenerationTarget):
            raise ValueError(FailureCode.M_00_22.value)
        if not isinstance(self.transformation, WeakTransformation):
            raise ValueError(FailureCode.M_00_22.value)
        if not self.condition:
            raise ValueError(FailureCode.M_00_22.value)
        if not self.trace_ref:
            raise ValueError(FailureCode.M_00_11.value)
        if self.rank != "CANDIDATE":
            raise ValueError(FailureCode.M_00_10.value)


# ══════════════════════════════════════════════════════════════════════════════
# §3  CLASSIFICATION (pure functions)
# ══════════════════════════════════════════════════════════════════════════════


def classify_root(root: LicensedRoot) -> WeakRootAnalysis:
    """Classify a root by its weak consonant position(s).

    TH9: Classification is deterministic — a function of consonant identity
    and position.

    Parameters
    ----------
    root : LicensedRoot
        The root to classify.

    Returns
    -------
    WeakRootAnalysis
        The classification result.
    """
    weak_pos: list[int] = []
    weak_cons: list[str] = []

    for i, c in enumerate(root.consonants):
        if c in WEAK_CONSONANTS:
            weak_pos.append(i)
            weak_cons.append(c)

    positions = tuple(weak_pos)
    consonants = tuple(weak_cons)

    if not positions:
        classification = WeakRootClass.SAHIH
    elif positions == (0,):
        classification = WeakRootClass.MITHAL
    elif positions == (1,):
        classification = WeakRootClass.AJWAF
    elif positions == (2,):
        classification = WeakRootClass.NAQIS
    elif 0 in positions and 2 in positions and 1 not in positions:
        classification = WeakRootClass.LAFIF_MAFRUQ
    elif 1 in positions and 2 in positions:
        classification = WeakRootClass.LAFIF_MAQRUN
    else:
        # Fallback for unusual combinations
        classification = WeakRootClass.SAHIH

    return WeakRootAnalysis(
        root=root,
        classification=classification,
        weak_positions=positions,
        weak_consonants_found=consonants,
    )


def is_weak_root(root: LicensedRoot) -> bool:
    """Check if a root contains any weak consonants.

    Pure function.
    """
    analysis = classify_root(root)
    return bool(analysis.weak_positions)


# ══════════════════════════════════════════════════════════════════════════════
# §4  TRANSFORMATION RULES TABLE
# ══════════════════════════════════════════════════════════════════════════════


def _build_transformation_rules() -> Tuple[WeakTransformationRule, ...]:
    """Build the immutable transformation rules for weak roots.

    Each rule specifies what happens to the weak consonant in a specific
    morphological context.
    """
    return (
        # ── مثال (Mithal) rules ──────────────────────────────────────────
        WeakTransformationRule(
            weak_class=WeakRootClass.MITHAL,
            target_form=GenerationTarget.PAST,
            transformation=WeakTransformation.HAMZA_PREFIX,
            condition="واو في موقع الفاء + باب أَفْعَلَ",
            example_root="وصل",
            example_result="أَوْصَلَ",
        ),
        WeakTransformationRule(
            weak_class=WeakRootClass.MITHAL,
            target_form=GenerationTarget.PRESENT,
            transformation=WeakTransformation.DELETION,
            condition="واو في موقع الفاء + المضارع",
            example_root="وصل",
            example_result="يَصِلُ",
        ),
        # ── أجوف (Ajwaf) rules ───────────────────────────────────────────
        WeakTransformationRule(
            weak_class=WeakRootClass.AJWAF,
            target_form=GenerationTarget.PAST,
            transformation=WeakTransformation.MUTATION_TO_ALIF,
            condition="واو أو ياء في موقع العين + الماضي",
            example_root="قول",
            example_result="قَالَ",
        ),
        WeakTransformationRule(
            weak_class=WeakRootClass.AJWAF,
            target_form=GenerationTarget.PRESENT,
            transformation=WeakTransformation.MUTATION_TO_WAW,
            condition="واو في موقع العين + المضارع",
            example_root="قول",
            example_result="يَقُولُ",
        ),
        # ── ناقص (Naqis) rules ───────────────────────────────────────────
        WeakTransformationRule(
            weak_class=WeakRootClass.NAQIS,
            target_form=GenerationTarget.PAST,
            transformation=WeakTransformation.VOWEL_CHANGE,
            condition="ياء في موقع اللام + الماضي",
            example_root="رمي",
            example_result="رَمَى",
        ),
        WeakTransformationRule(
            weak_class=WeakRootClass.NAQIS,
            target_form=GenerationTarget.PRESENT,
            transformation=WeakTransformation.MUTATION_TO_YA,
            condition="ياء في موقع اللام + المضارع",
            example_root="رمي",
            example_result="يَرْمِي",
        ),
        # ── لفيف مقرون (Lafif Maqrun) rules ──────────────────────────────
        WeakTransformationRule(
            weak_class=WeakRootClass.LAFIF_MAQRUN,
            target_form=GenerationTarget.PAST,
            transformation=WeakTransformation.VOWEL_CHANGE,
            condition="حرفا علة في العين واللام + الماضي",
            example_root="سوي",
            example_result="سَوَى",
        ),
        WeakTransformationRule(
            weak_class=WeakRootClass.LAFIF_MAQRUN,
            target_form=GenerationTarget.PRESENT,
            transformation=WeakTransformation.MUTATION_TO_YA,
            condition="حرفا علة في العين واللام + المضارع",
            example_root="روي",
            example_result="يَرْوِي",
        ),
    )


TRANSFORMATION_RULES: Tuple[WeakTransformationRule, ...] = _build_transformation_rules()
"""Immutable table of weak root transformation rules."""


# ══════════════════════════════════════════════════════════════════════════════
# §5  GENERATION WITH WEAK ROOT HANDLING
# ══════════════════════════════════════════════════════════════════════════════


def generate_weak_past(root: LicensedRoot, form: MorphForm = MorphForm.FORM_I) -> GeneratedForm:
    """Generate past tense for a weak root with appropriate transformations.

    TH9: Weak consonants undergo deterministic transformations.

    Parameters
    ----------
    root : LicensedRoot
        A weak root.
    form : MorphForm
        The morphological form.

    Returns
    -------
    GeneratedForm
        The generated form with weak root transformations applied.
    """
    analysis = classify_root(root)
    f, a, l = root.consonants[0], root.consonants[1], root.consonants[2]

    if analysis.classification == WeakRootClass.MITHAL and form == MorphForm.FORM_IV:
        # مثال + أَفْعَلَ: و-ص-ل → أَوْصَلَ
        surface = apply_fatha("أ") + apply_sukun(f) + apply_fatha(a) + apply_fatha(l)
        trace = f"Mithal Form IV: أ+َ + {f}+ْ + {a}+َ + {l}+َ (hamza prefix for weak-first)"

    elif analysis.classification == WeakRootClass.AJWAF:
        # أجوف: ق-و-ل → قَالَ (واو → ألف)
        surface = apply_fatha(f) + apply_alif_madd() + apply_fatha(l)
        trace = f"Ajwaf past: {f}+َ + ا (← {a}) + {l}+َ (weak-middle → alif)"

    elif analysis.classification == WeakRootClass.NAQIS:
        # ناقص: ر-م-ي → رَمَى
        surface = apply_fatha(f) + apply_fatha(a) + "ى"
        trace = f"Naqis past: {f}+َ + {a}+َ + ى (← {l}) (weak-final → alif maqsura)"

    elif analysis.classification == WeakRootClass.LAFIF_MAQRUN:
        # لفيف مقرون: س-و-ي → سَوَى
        surface = apply_fatha(f) + apply_fatha(a) + "ى"
        trace = f"Lafif maqrun past: {f}+َ + {a}+َ + ى (weak second+third)"

    else:
        # Default: regular past tense generation
        surface = apply_fatha(f) + apply_fatha(a) + apply_fatha(l)
        trace = f"Regular past: {f}+َ + {a}+َ + {l}+َ"

    return GeneratedForm(
        surface=surface,
        root=root,
        form=form,
        target=GenerationTarget.PAST,
        generation_trace=trace,
    )


def generate_weak_present(root: LicensedRoot, form: MorphForm = MorphForm.FORM_I) -> GeneratedForm:
    """Generate present tense for a weak root with appropriate transformations.

    TH9: Weak consonants undergo deterministic transformations.

    Parameters
    ----------
    root : LicensedRoot
        A weak root.
    form : MorphForm
        The morphological form.

    Returns
    -------
    GeneratedForm
        The generated form with weak root transformations applied.
    """
    analysis = classify_root(root)
    f, a, l = root.consonants[0], root.consonants[1], root.consonants[2]

    if analysis.classification == WeakRootClass.MITHAL:
        # مثال: و-ص-ل → يَصِلُ (واو deleted)
        surface = apply_fatha("ي") + apply_kasra(a) + apply_damma(l)
        trace = f"Mithal present: ي+َ + {a}+ِ + {l}+ُ (weak-first deleted)"

    elif analysis.classification == WeakRootClass.AJWAF:
        # أجوف: ق-و-ل → يَقُولُ (واو preserved as long vowel)
        surface = apply_fatha("ي") + apply_damma(f) + "و" + apply_damma(l)
        trace = f"Ajwaf present: ي+َ + {f}+ُ + و + {l}+ُ (weak-middle as long vowel)"

    elif analysis.classification == WeakRootClass.NAQIS:
        # ناقص: ر-م-ي → يَرْمِي
        surface = apply_fatha("ي") + apply_sukun(f) + apply_kasra(a) + "ي"
        trace = f"Naqis present: ي+َ + {f}+ْ + {a}+ِ + ي (weak-final → ya)"

    elif analysis.classification == WeakRootClass.LAFIF_MAQRUN:
        # لفيف مقرون: ر-و-ي → يَرْوِي
        surface = apply_fatha("ي") + apply_sukun(f) + apply_kasra(a) + l
        trace = f"Lafif maqrun present: ي+َ + {f}+ْ + {a}+ِ + {l} (weak second+third)"

    else:
        # Default: regular present tense
        surface = apply_fatha("ي") + apply_sukun(f) + apply_damma(a) + apply_damma(l)
        trace = f"Regular present: ي+َ + {f}+ْ + {a}+ُ + {l}+ُ"

    return GeneratedForm(
        surface=surface,
        root=root,
        form=form,
        target=GenerationTarget.PRESENT,
        generation_trace=trace,
    )


def get_transformation_for(
    weak_class: WeakRootClass, target: GenerationTarget
) -> Optional[WeakTransformationRule]:
    """Look up the transformation rule for a given class and target.

    Parameters
    ----------
    weak_class : WeakRootClass
        The weak root classification.
    target : GenerationTarget
        The target form.

    Returns
    -------
    Optional[WeakTransformationRule]
        The rule if found, None otherwise.
    """
    for rule in TRANSFORMATION_RULES:
        if rule.weak_class == weak_class and rule.target_form == target:
            return rule
    return None
