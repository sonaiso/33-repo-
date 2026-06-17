"""
Core package — SlotGraph, Rank, ResidualBundle, TraceRef, Morphological Generator.
Origin: docs/00_MAQOOL_CONSTITUTION.md §2 Category 1
"""
from taaqqul_slot_geometry.core.rank import Rank, RankLattice
from taaqqul_slot_geometry.core.residual import ResidualBundle
from taaqqul_slot_geometry.core.slot_graph import SlotGraph
from taaqqul_slot_geometry.core.trace import TraceRef
from taaqqul_slot_geometry.core.arabic_weight_pattern import (
    ConsonantPosition,
    GenerativeRelation,
    MorphForm,
    TransitivityHint,
    WEIGHT_PATTERN_REGISTRY,
    WeightPatternSpec,
    get_weight_pattern,
)
from taaqqul_slot_geometry.core.arabic_morphology_generator import (
    GeneratedForm,
    GenerationTarget,
    LicensedRoot,
    RootType,
    generate_all_forms,
    generate_past,
    generate_present,
    generate_active_participle,
    generate_passive_participle,
    generate_verbal_noun,
    generate_sound_plural_masc,
    generate_sound_plural_fem,
    generate_broken_plural,
    generate_diminutive,
    generate_comparative,
    make_root,
)
from taaqqul_slot_geometry.core.arabic_taadiyah_luzoom import (
    TransitivityClass,
    TransitivityMechanism,
    TransitivityRule,
    TransitivityVerdict,
    TRANSITIVITY_RULES,
    determine_transitivity,
)
from taaqqul_slot_geometry.core.arabic_muttasil import (
    WEAK_CONSONANTS,
    WeakRootClass,
    WeakTransformation,
    WeakRootAnalysis,
    WeakTransformationRule,
    TRANSFORMATION_RULES,
    classify_root,
    is_weak_root,
    generate_weak_past,
    generate_weak_present,
)
from taaqqul_slot_geometry.core.letter_registry import (
    LETTER_BY_CODEPOINT,
    LETTER_BY_GLYPH,
    LETTER_BY_ID,
    LETTER_REGISTRY,
    LetterGenus,
    LetterIdentity,
    get_letter_by_codepoint,
    get_letter_by_glyph,
    get_letter_by_id,
)
from taaqqul_slot_geometry.core.mark_registry import (
    MARK_BY_CODEPOINT,
    MARK_BY_ID,
    MARK_REGISTRY,
    MarkFunction,
    MarkGenus,
    MarkIdentity,
    get_mark_by_codepoint,
    get_mark_by_id,
)
from taaqqul_slot_geometry.core.transition_registry import (
    TRANSITION_BY_ID,
    TRANSITION_REGISTRY,
    TransitionLayer,
    TransitionLaw,
    TransitionVerdict,
    check_transition_licensed,
    get_transition_law,
)

__all__ = [
    "Rank",
    "RankLattice",
    "ResidualBundle",
    "SlotGraph",
    "TraceRef",
    # Weight Pattern Registry (TH7)
    "ConsonantPosition",
    "GenerativeRelation",
    "MorphForm",
    "TransitivityHint",
    "WEIGHT_PATTERN_REGISTRY",
    "WeightPatternSpec",
    "get_weight_pattern",
    # Morphology Generator (TH7)
    "GeneratedForm",
    "GenerationTarget",
    "LicensedRoot",
    "RootType",
    "generate_all_forms",
    "generate_past",
    "generate_present",
    "generate_active_participle",
    "generate_passive_participle",
    "generate_verbal_noun",
    "generate_sound_plural_masc",
    "generate_sound_plural_fem",
    "generate_broken_plural",
    "generate_diminutive",
    "generate_comparative",
    "make_root",
    # Transitivity System (TH8)
    "TransitivityClass",
    "TransitivityMechanism",
    "TransitivityRule",
    "TransitivityVerdict",
    "TRANSITIVITY_RULES",
    "determine_transitivity",
    # Weak Root System (TH9)
    "WEAK_CONSONANTS",
    "WeakRootClass",
    "WeakTransformation",
    "WeakRootAnalysis",
    "WeakTransformationRule",
    "TRANSFORMATION_RULES",
    "classify_root",
    "is_weak_root",
    "generate_weak_past",
    "generate_weak_present",
    # Letter Registry (docs/59)
    "LETTER_BY_CODEPOINT",
    "LETTER_BY_GLYPH",
    "LETTER_BY_ID",
    "LETTER_REGISTRY",
    "LetterGenus",
    "LetterIdentity",
    "get_letter_by_codepoint",
    "get_letter_by_glyph",
    "get_letter_by_id",
    # Mark Registry (docs/59)
    "MARK_BY_CODEPOINT",
    "MARK_BY_ID",
    "MARK_REGISTRY",
    "MarkFunction",
    "MarkGenus",
    "MarkIdentity",
    "get_mark_by_codepoint",
    "get_mark_by_id",
    # Transition Registry (docs/59)
    "TRANSITION_BY_ID",
    "TRANSITION_REGISTRY",
    "TransitionLayer",
    "TransitionLaw",
    "TransitionVerdict",
    "check_transition_licensed",
    "get_transition_law",
]
