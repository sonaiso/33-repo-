"""
Integration test: vocalized Arabic words through the full L0 pipeline.

Tests the complete chain:
  Unicode → Letter/Mark → VocalizedUnit → Syllable → LafzCandidate

Each test case validates:
- Correct letter/mark parsing
- Correct syllable pattern formation
- Lafz closure (phonetically complete)
- NO morphological assertions (root, weight, word class are FORBIDDEN in L0)

Origin: docs/59_ARABIC_DIGITAL_IDENTITY_LAW.md §VocalizedParser
trace_ref: docs/15_PROJECT_ROADMAP.md Phase 0 — L0 Closure (PR-9)
"""
from __future__ import annotations

import pytest
from typing import FrozenSet

from taaqqul_slot_geometry.core.vocalized_parser import parse_vocalized, ParseResult
from taaqqul_slot_geometry.core.vocalized_unit_builder import build_vocalized_units
from taaqqul_slot_geometry.core.syllabifier import syllabify
from taaqqul_slot_geometry.core.lafz_closure import close_lafz, LafzCandidate
from taaqqul_slot_geometry.core.transition_registry import TransitionVerdict


# ══════════════════════════════════════════════════════════════════════════════
# Helper: run the full L0 pipeline on a vocalized word
# ══════════════════════════════════════════════════════════════════════════════

def _run_l0_pipeline(text: str) -> LafzCandidate:
    """Run the full L0 pipeline: parse → build units → syllabify → close lafz."""
    parsed = parse_vocalized(text)
    units = build_vocalized_units(parsed)
    syllabified = syllabify(units)
    return close_lafz(syllabified)


# ══════════════════════════════════════════════════════════════════════════════
# Test case definitions — what L0 MUST produce and what it MUST NOT assert
# ══════════════════════════════════════════════════════════════════════════════

# IMPORTANT: These tests verify ONLY phonetic/orthographic pipeline correctness.
# The downstream_hint is documentary ONLY — it is NEVER asserted in L0.
# must_not_assert_in_L0 lists what is FORBIDDEN to extract in this layer.

VOCALIZED_CASES = [
    {
        "input": "كَتَبَ",
        "description": "kataba — 3 CV syllables",
        "expected_syllable_pattern": "CV-CV-CV",
        "expected_lafz_closed": True,
        "expected_residuals": frozenset(),
        "downstream_hint": {"possible_weight": "فَعَلَ", "possible_word_class": "verb"},
        "must_not_assert_in_L0": ["root", "weight", "past_tense", "transitivity", "source"],
    },
    {
        "input": "كُتِبَ",
        "description": "kutiba — 3 CV syllables (passive, but L0 doesn't know that)",
        "expected_syllable_pattern": "CV-CV-CV",
        "expected_lafz_closed": True,
        "expected_residuals": frozenset(),  # NO agent_suppressed in L0!
        "downstream_hint": {"possible_weight": "فُعِلَ", "possible_word_class": "verb"},
        "must_not_assert_in_L0": ["root", "weight", "passive_voice", "agent_suppressed"],
    },
    {
        "input": "عِلْمٌ",
        "description": "ilmun — CVC + CV with tanwin",
        "expected_syllable_pattern": "CVC-CV",
        "expected_lafz_closed": True,
        "expected_residuals": frozenset({"tanwin_requires_word_layer"}),
        "downstream_hint": {"possible_weight": "فِعْل", "possible_word_class": "noun"},
        "must_not_assert_in_L0": ["root", "weight", "noun_type", "masdar"],
    },
]


# ══════════════════════════════════════════════════════════════════════════════
# Core integration tests
# ══════════════════════════════════════════════════════════════════════════════

class TestVocalizedParsing:
    """Test the parsing stage: Unicode → (letter, mark) pairs."""

    def test_kataba_parse(self) -> None:
        """كَتَبَ parses into 3 letter+mark pairs."""
        result = parse_vocalized("كَتَبَ")
        assert len(result.units) == 3
        assert result.is_fully_vocalized is True
        assert result.rank == "CANDIDATE"

        # Verify letter identities
        assert result.units[0].letter is not None
        assert result.units[0].letter.letter_id == "KAF"
        assert result.units[0].mark is not None
        assert result.units[0].mark.mark_id == "FATHA"

        assert result.units[1].letter is not None
        assert result.units[1].letter.letter_id == "TA"
        assert result.units[1].mark is not None
        assert result.units[1].mark.mark_id == "FATHA"

        assert result.units[2].letter is not None
        assert result.units[2].letter.letter_id == "BA"
        assert result.units[2].mark is not None
        assert result.units[2].mark.mark_id == "FATHA"

    def test_kutiba_parse(self) -> None:
        """كُتِبَ parses into 3 letter+mark pairs."""
        result = parse_vocalized("كُتِبَ")
        assert len(result.units) == 3
        assert result.is_fully_vocalized is True

        assert result.units[0].mark.mark_id == "DAMMA"
        assert result.units[1].mark.mark_id == "KASRA"
        assert result.units[2].mark.mark_id == "FATHA"

    def test_ilmun_parse(self) -> None:
        """عِلْمٌ parses into letter+mark pairs with sukun and tanwin."""
        result = parse_vocalized("عِلْمٌ")
        assert len(result.units) == 3
        assert result.is_fully_vocalized is True

        # ع + kasra
        assert result.units[0].letter.letter_id == "AIN"
        assert result.units[0].mark.mark_id == "KASRA"

        # ل + sukun
        assert result.units[1].letter.letter_id == "LAM"
        assert result.units[1].mark.mark_id == "SUKUN"

        # م + dammatan (tanwin)
        assert result.units[2].letter.letter_id == "MEEM"
        assert result.units[2].mark.mark_id == "DAMMATAN"

    def test_unvocalized_deferred(self) -> None:
        """كتب without harakat produces rank='deferred'."""
        result = parse_vocalized("كتب")
        assert result.rank == "deferred"
        assert "missing_harakat" in result.residuals

    def test_empty_input_raises(self) -> None:
        """Empty input raises ValueError with FailureCode."""
        with pytest.raises(ValueError, match="utterance_empty"):
            parse_vocalized("")

    def test_orphaned_mark_raises(self) -> None:
        """A mark without preceding letter raises ValueError."""
        with pytest.raises(ValueError, match="grapheme_not_in_28"):
            parse_vocalized("\u064E")  # bare fatha


class TestVocalizedUnitBuilding:
    """Test the unit building stage: (letter, mark) → VocalizedUnit."""

    def test_kataba_units(self) -> None:
        """كَتَبَ produces 3 vocalized units with CV patterns."""
        parsed = parse_vocalized("كَتَبَ")
        units = build_vocalized_units(parsed)
        assert len(units) == 3

        # All should be LICENSED
        for u in units:
            assert u.transition_verdict == TransitionVerdict.LICENSED

        # All should be C_FATHA pattern
        from taaqqul_slot_geometry.L0.phoneme import PhoneticPattern
        for u in units:
            assert u.phoneme.pattern == PhoneticPattern.C_FATHA

    def test_tanwin_unit_has_residual(self) -> None:
        """Tanwin mark produces tanwin_requires_word_layer residual."""
        parsed = parse_vocalized("عِلْمٌ")
        units = build_vocalized_units(parsed)
        # Last unit (meem + dammatan) should have tanwin residual
        assert "tanwin_requires_word_layer" in units[2].residuals
        assert units[2].is_tanwin is True


class TestSyllabification:
    """Test the syllabification stage: VocalizedUnits → Syllables."""

    def test_kataba_syllables(self) -> None:
        """كَتَبَ produces CV-CV-CV syllable pattern."""
        parsed = parse_vocalized("كَتَبَ")
        units = build_vocalized_units(parsed)
        result = syllabify(units)

        assert len(result.syllables) == 3
        from taaqqul_slot_geometry.L0.syllable import SyllableType
        assert result.syllable_types == (SyllableType.CV, SyllableType.CV, SyllableType.CV)

    def test_ilmun_syllables(self) -> None:
        """عِلْمٌ produces CVC-CV syllable pattern.

        عِلْ = عِ (onset + kasra) + لْ (coda sukun) → CVC
        مٌ  = م + dammatan (tanwin acts as short vowel at L0) → CV
        """
        parsed = parse_vocalized("عِلْمٌ")
        units = build_vocalized_units(parsed)
        result = syllabify(units)

        assert len(result.syllables) == 2
        from taaqqul_slot_geometry.L0.syllable import SyllableType
        assert result.syllable_types == (SyllableType.CVC, SyllableType.CV)


class TestLafzClosure:
    """Test the lafz closure stage: Syllables → LafzCandidate."""

    def test_kataba_lafz_closed(self) -> None:
        """كَتَبَ produces a closed LafzCandidate."""
        lafz = _run_l0_pipeline("كَتَبَ")
        assert lafz.lafz_closed is True
        assert lafz.identity_preserved is True
        assert lafz.syllable_pattern == "CV-CV-CV"
        assert lafz.rank == "CANDIDATE"
        assert lafz.transition_verdict == TransitionVerdict.LICENSED

    def test_kutiba_lafz_closed(self) -> None:
        """كُتِبَ produces a closed LafzCandidate with NO agent_suppressed."""
        lafz = _run_l0_pipeline("كُتِبَ")
        assert lafz.lafz_closed is True
        assert lafz.syllable_pattern == "CV-CV-CV"
        # CRITICAL: agent_suppressed must NOT be in L0 residuals
        assert "agent_suppressed" not in lafz.residuals

    def test_ilmun_lafz_closed_with_tanwin_residual(self) -> None:
        """عِلْمٌ produces a closed lafz with tanwin_requires_word_layer residual."""
        lafz = _run_l0_pipeline("عِلْمٌ")
        assert lafz.lafz_closed is True
        assert lafz.syllable_pattern == "CVC-CV"
        assert "tanwin_requires_word_layer" in lafz.residuals

    def test_unvocalized_lafz_not_closed(self) -> None:
        """كتب (unvocalized) produces a non-closed lafz with missing_harakat."""
        lafz = _run_l0_pipeline("كتب")
        assert lafz.lafz_closed is False
        assert "missing_harakat" in lafz.residuals


class TestL0BoundaryEnforcement:
    """Verify that L0 does NOT produce any morphological information.

    These tests ensure the No-Leap Axiom is respected:
    L0 produces ONLY phonetic/orthographic identity closure.
    """

    def test_no_root_in_l0(self) -> None:
        """LafzCandidate has no root field."""
        lafz = _run_l0_pipeline("كَتَبَ")
        assert not hasattr(lafz, "root")
        assert not hasattr(lafz, "root_consonants")

    def test_no_weight_in_l0(self) -> None:
        """LafzCandidate has no weight field."""
        lafz = _run_l0_pipeline("كَتَبَ")
        assert not hasattr(lafz, "weight")
        assert not hasattr(lafz, "weight_pattern")
        assert not hasattr(lafz, "weight_witness")

    def test_no_word_class_in_l0(self) -> None:
        """LafzCandidate has no word_class/noun/verb field."""
        lafz = _run_l0_pipeline("كَتَبَ")
        assert not hasattr(lafz, "word_class")
        assert not hasattr(lafz, "is_verb")
        assert not hasattr(lafz, "is_noun")
        assert not hasattr(lafz, "is_particle")

    def test_no_tense_in_l0(self) -> None:
        """LafzCandidate has no tense field."""
        lafz = _run_l0_pipeline("كَتَبَ")
        assert not hasattr(lafz, "tense")
        assert not hasattr(lafz, "past")
        assert not hasattr(lafz, "present")

    def test_no_transitivity_in_l0(self) -> None:
        """LafzCandidate has no transitivity field."""
        lafz = _run_l0_pipeline("كَتَبَ")
        assert not hasattr(lafz, "transitivity")
        assert not hasattr(lafz, "transitive")
        assert not hasattr(lafz, "intransitive")

    def test_no_agent_suppressed_in_l0(self) -> None:
        """agent_suppressed is a morphological residual, NOT an L0 residual."""
        lafz = _run_l0_pipeline("كُتِبَ")
        assert "agent_suppressed" not in lafz.residuals

    def test_rank_always_candidate(self) -> None:
        """All L0 outputs must be rank='CANDIDATE', never promoted."""
        for case in VOCALIZED_CASES:
            if case["expected_lafz_closed"]:
                lafz = _run_l0_pipeline(case["input"])
                assert lafz.rank == "CANDIDATE", (
                    f"Rank promotion forbidden in L0 for {case['input']}"
                )
