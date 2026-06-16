"""
L0 package — phonological layer (Object Language).
Origin: docs/00_MAQOOL_CONSTITUTION.md §6 L0
"""
from taaqqul_slot_geometry.L0.grapheme import GRAPHEME_TABLE, Grapheme, get_grapheme
from taaqqul_slot_geometry.L0.harf_maani import HARF_MAANI_TABLE, HarfMaani, get_harf
from taaqqul_slot_geometry.L0.jamid import (
    ALL_ANCHORS,
    BINARY_ANCHORS,
    TERNARY_ANCHORS,
    JamidAnchor,
    JamidAnchorType,
)
from taaqqul_slot_geometry.L0.phoneme import PhonemeUnit, PhoneticPattern
from taaqqul_slot_geometry.L0.signification import Signification, SignificationType
from taaqqul_slot_geometry.L0.signified import ConventionalSignified, LinguisticSignified
from taaqqul_slot_geometry.L0.signifier import Signifier
from taaqqul_slot_geometry.L0.syllable import Syllable, SyllableType, make_syllable
from taaqqul_slot_geometry.L0.union import Union
from taaqqul_slot_geometry.L0.utterance import Utterance
from taaqqul_slot_geometry.L0.vowel import (
    MADD_VOWELS,
    SHORT_VOWELS,
    Vowel,
    assert_valid_vowel,
    is_madd,
    is_short,
)
from taaqqul_slot_geometry.L0.waqf_wasl import (
    CANONICAL_PROFILES,
    BoundaryLevel,
    BoundaryTest,
    WaqfStatus,
    WaqfWaslProfile,
    WordPath,
    can_stop,
    must_join,
)
from taaqqul_slot_geometry.L0.weight import WeightPattern, WeightUnit

__all__ = [
    "GRAPHEME_TABLE",
    "Grapheme",
    "get_grapheme",
    "HARF_MAANI_TABLE",
    "HarfMaani",
    "get_harf",
    "ALL_ANCHORS",
    "BINARY_ANCHORS",
    "TERNARY_ANCHORS",
    "JamidAnchor",
    "JamidAnchorType",
    "PhonemeUnit",
    "PhoneticPattern",
    "Signification",
    "SignificationType",
    "ConventionalSignified",
    "LinguisticSignified",
    "Signifier",
    "Syllable",
    "SyllableType",
    "make_syllable",
    "Union",
    "Utterance",
    "MADD_VOWELS",
    "SHORT_VOWELS",
    "Vowel",
    "assert_valid_vowel",
    "is_madd",
    "is_short",
    "CANONICAL_PROFILES",
    "BoundaryLevel",
    "BoundaryTest",
    "WaqfStatus",
    "WaqfWaslProfile",
    "WordPath",
    "can_stop",
    "must_join",
    "WeightPattern",
    "WeightUnit",
]
