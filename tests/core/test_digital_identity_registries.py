"""
Tests for the Arabic Digital Identity registries (LetterRegistry, MarkRegistry, TransitionRegistry).

Origin: docs/59_ARABIC_DIGITAL_IDENTITY_LAW.md
"""
import pytest

from tests.conftest import ConstitutionalChainTestCase
from taaqqul_slot_geometry.constitution.failure_taxonomy import FailureCode
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


# ══════════════════════════════════════════════════════════════════════════════
# LetterRegistry Tests
# ══════════════════════════════════════════════════════════════════════════════


class TestLetterRegistry(ConstitutionalChainTestCase):
    """Origin: docs/59_ARABIC_DIGITAL_IDENTITY_LAW.md §LetterRegistry"""

    def test_exactly_28_letters(self):
        """Registry must contain exactly 28 Arabic letters."""
        assert len(LETTER_REGISTRY) == 28

    def test_all_letter_ids_unique(self):
        """All letter_ids must be unique."""
        ids = [lt.letter_id for lt in LETTER_REGISTRY]
        assert len(ids) == len(set(ids))

    def test_all_glyphs_unique(self):
        """All glyphs must be unique."""
        glyphs = [lt.glyph for lt in LETTER_REGISTRY]
        assert len(glyphs) == len(set(glyphs))

    def test_all_codepoints_unique(self):
        """All Unicode codepoints must be unique."""
        cps = [lt.unicode_codepoint for lt in LETTER_REGISTRY]
        assert len(cps) == len(set(cps))

    def test_lookup_by_id(self):
        """get_letter_by_id returns correct letter."""
        ba = get_letter_by_id("BA")
        assert ba.glyph == "ب"
        assert ba.unicode_codepoint == "U+0628"

    def test_lookup_by_glyph(self):
        """get_letter_by_glyph returns correct letter."""
        meem = get_letter_by_glyph("م")
        assert meem.letter_id == "MEEM"

    def test_lookup_by_codepoint(self):
        """get_letter_by_codepoint returns correct letter."""
        noon = get_letter_by_codepoint("U+0646")
        assert noon.letter_id == "NOON"

    def test_unknown_id_rejected(self):
        """Unknown letter_id must raise ValueError with FailureCode."""
        with pytest.raises(ValueError) as exc_info:
            get_letter_by_id("UNKNOWN")
        assert FailureCode.M_00_03.value in str(exc_info.value)

    def test_unknown_glyph_rejected(self):
        """Unknown glyph must raise ValueError."""
        with pytest.raises(ValueError) as exc_info:
            get_letter_by_glyph("X")
        assert FailureCode.M_00_03.value in str(exc_info.value)

    def test_all_letters_have_trace_ref(self):
        """Every letter must have a non-empty trace_ref."""
        for lt in LETTER_REGISTRY:
            assert lt.trace_ref, f"Missing trace_ref on {lt.letter_id}"

    def test_all_letters_rank_candidate(self):
        """Every letter must have rank CANDIDATE."""
        for lt in LETTER_REGISTRY:
            assert lt.rank == "CANDIDATE", f"Wrong rank on {lt.letter_id}"

    def test_all_letters_have_residuals(self):
        """Every letter must have a frozenset residuals field."""
        for lt in LETTER_REGISTRY:
            assert isinstance(lt.residuals, frozenset)

    def test_letters_are_frozen(self):
        """LetterIdentity must be frozen (immutable)."""
        ba = get_letter_by_id("BA")
        with pytest.raises((AttributeError, TypeError)):
            ba.letter_id = "CHANGED"  # type: ignore[misc]

    def test_waw_ya_have_ambiguity_residual(self):
        """Waw and Ya carry madd_or_consonant_ambiguity residual."""
        waw = get_letter_by_id("WAW")
        ya = get_letter_by_id("YA")
        assert "madd_or_consonant_ambiguity" in waw.residuals
        assert "madd_or_consonant_ambiguity" in ya.residuals

    def test_consonantal_letters_accept_all(self):
        """All consonantal letters accept haraka, sukun, and shadda."""
        for lt in LETTER_REGISTRY:
            if lt.genus == LetterGenus.CONSONANTAL:
                assert lt.accepts_haraka
                assert lt.accepts_sukun
                assert lt.accepts_shadda

    def test_empty_letter_id_rejected(self):
        """Empty letter_id must be rejected at construction."""
        with pytest.raises(ValueError) as exc_info:
            LetterIdentity(
                letter_id="",
                unicode_codepoint="U+0000",
                glyph="?",
                genus=LetterGenus.CONSONANTAL,
                essence="test",
                accepts_haraka=True,
                accepts_sukun=True,
                accepts_shadda=True,
                connects_right=True,
                connects_left=True,
            )
        assert FailureCode.M_00_03.value in str(exc_info.value)


# ══════════════════════════════════════════════════════════════════════════════
# MarkRegistry Tests
# ══════════════════════════════════════════════════════════════════════════════


class TestMarkRegistry(ConstitutionalChainTestCase):
    """Origin: docs/59_ARABIC_DIGITAL_IDENTITY_LAW.md §MarkRegistry"""

    def test_registry_not_empty(self):
        """Mark registry must contain entries."""
        assert len(MARK_REGISTRY) >= 10

    def test_all_mark_ids_unique(self):
        """All mark_ids must be unique."""
        ids = [m.mark_id for m in MARK_REGISTRY]
        assert len(ids) == len(set(ids))

    def test_all_codepoints_unique(self):
        """All Unicode codepoints must be unique."""
        cps = [m.unicode_codepoint for m in MARK_REGISTRY]
        assert len(cps) == len(set(cps))

    def test_lookup_fatha(self):
        """FATHA mark has correct properties."""
        fatha = get_mark_by_id("FATHA")
        assert fatha.unicode_codepoint == "U+064E"
        assert fatha.genus == MarkGenus.SHORT_VOWEL
        assert fatha.function == MarkFunction.VOWEL_OPEN

    def test_lookup_sukun(self):
        """SUKUN mark has correct properties."""
        sukun = get_mark_by_id("SUKUN")
        assert sukun.genus == MarkGenus.SUKUN
        assert sukun.function == MarkFunction.CLOSE_LETTER

    def test_lookup_shadda(self):
        """SHADDA mark has correct properties."""
        shadda = get_mark_by_id("SHADDA")
        assert shadda.genus == MarkGenus.SHADDA
        assert shadda.function == MarkFunction.GEMINATE

    def test_lookup_by_codepoint(self):
        """get_mark_by_codepoint works correctly."""
        damma = get_mark_by_codepoint("U+064F")
        assert damma.mark_id == "DAMMA"

    def test_unknown_mark_rejected(self):
        """Unknown mark_id must raise ValueError."""
        with pytest.raises(ValueError) as exc_info:
            get_mark_by_id("UNKNOWN")
        assert FailureCode.M_00_04.value in str(exc_info.value)

    def test_all_marks_have_trace_ref(self):
        """Every mark must have non-empty trace_ref."""
        for m in MARK_REGISTRY:
            assert m.trace_ref, f"Missing trace_ref on {m.mark_id}"

    def test_all_marks_rank_candidate(self):
        """Every mark must have rank CANDIDATE."""
        for m in MARK_REGISTRY:
            assert m.rank == "CANDIDATE", f"Wrong rank on {m.mark_id}"

    def test_all_marks_have_preventers(self):
        """Every mark must have a frozenset preventers field."""
        for m in MARK_REGISTRY:
            assert isinstance(m.preventers, frozenset)

    def test_marks_are_frozen(self):
        """MarkIdentity must be frozen."""
        fatha = get_mark_by_id("FATHA")
        with pytest.raises((AttributeError, TypeError)):
            fatha.mark_id = "CHANGED"  # type: ignore[misc]

    def test_short_vowels_prevent_conflicts(self):
        """Short vowel marks must list conflicting_short_vowel as preventer."""
        for m in MARK_REGISTRY:
            if m.genus == MarkGenus.SHORT_VOWEL:
                assert "conflicting_short_vowel" in m.preventers

    def test_empty_mark_id_rejected(self):
        """Empty mark_id must be rejected at construction."""
        with pytest.raises(ValueError) as exc_info:
            MarkIdentity(
                mark_id="",
                unicode_codepoint="U+0000",
                glyph="?",
                genus=MarkGenus.SHORT_VOWEL,
                function=MarkFunction.VOWEL_OPEN,
                attaches_to="letter",
                opens_next_layer="test",
                preventers=frozenset(),
            )
        assert FailureCode.M_00_04.value in str(exc_info.value)


# ══════════════════════════════════════════════════════════════════════════════
# TransitionRegistry Tests
# ══════════════════════════════════════════════════════════════════════════════


class TestTransitionRegistry(ConstitutionalChainTestCase):
    """Origin: docs/59_ARABIC_DIGITAL_IDENTITY_LAW.md §TransitionRegistry"""

    def test_registry_has_expected_laws(self):
        """Registry must have all 9 transition laws."""
        assert len(TRANSITION_REGISTRY) == 9

    def test_all_law_ids_unique(self):
        """All law_ids must be unique."""
        ids = [t.law_id for t in TRANSITION_REGISTRY]
        assert len(ids) == len(set(ids))

    def test_lookup_letter_haraka_link(self):
        """LETTER_HARAKA_LINK law exists with correct layers."""
        law = get_transition_law("LETTER_HARAKA_LINK")
        assert law.source_layer == TransitionLayer.LETTER
        assert law.target_layer == TransitionLayer.VOCALIZED_UNIT

    def test_lookup_syllable_to_lafz(self):
        """SYLLABLE_TO_LAFZ law exists with correct layers."""
        law = get_transition_law("SYLLABLE_TO_LAFZ")
        assert law.source_layer == TransitionLayer.SYLLABLE
        assert law.target_layer == TransitionLayer.LAFZ

    def test_unknown_law_rejected(self):
        """Unknown law_id must raise ValueError."""
        with pytest.raises(ValueError) as exc_info:
            get_transition_law("NONEXISTENT")
        assert FailureCode.M_CX_02.value in str(exc_info.value)

    def test_all_laws_have_trace_ref(self):
        """Every law must have non-empty trace_ref."""
        for t in TRANSITION_REGISTRY:
            assert t.trace_ref, f"Missing trace_ref on {t.law_id}"

    def test_all_laws_rank_candidate(self):
        """Every law must have rank CANDIDATE."""
        for t in TRANSITION_REGISTRY:
            assert t.rank == "CANDIDATE", f"Wrong rank on {t.law_id}"

    def test_all_laws_have_preventers(self):
        """Every law must have a frozenset preventers field."""
        for t in TRANSITION_REGISTRY:
            assert isinstance(t.preventers, frozenset)

    def test_laws_are_frozen(self):
        """TransitionLaw must be frozen."""
        law = get_transition_law("UNICODE_TO_GLYPH")
        with pytest.raises((AttributeError, TypeError)):
            law.law_id = "CHANGED"  # type: ignore[misc]

    def test_no_leap_between_layers(self):
        """Transition laws must follow the adjacency graph (No-Leap Axiom).

        The layer graph is NOT purely linear — it has branching:
          UNICODE → GLYPH → {LETTER, MARK} → VOCALIZED_UNIT → SYLLABLE → LAFZ → MUFRAD

        LETTER and MARK are sibling outputs of GLYPH, and both feed into VOCALIZED_UNIT.
        So valid edges include: LETTER→VOCALIZED_UNIT, MARK→(combined with letter).
        """
        # Define the valid adjacency graph (directed edges)
        VALID_EDGES = {
            (TransitionLayer.UNICODE, TransitionLayer.GLYPH),
            (TransitionLayer.GLYPH, TransitionLayer.LETTER),
            (TransitionLayer.GLYPH, TransitionLayer.MARK),
            (TransitionLayer.LETTER, TransitionLayer.VOCALIZED_UNIT),
            (TransitionLayer.MARK, TransitionLayer.VOCALIZED_UNIT),
            (TransitionLayer.VOCALIZED_UNIT, TransitionLayer.SYLLABLE),
            (TransitionLayer.SYLLABLE, TransitionLayer.LAFZ),
            (TransitionLayer.LAFZ, TransitionLayer.MUFRAD),
        }
        for t in TRANSITION_REGISTRY:
            pair = (t.source_layer, t.target_layer)
            assert pair in VALID_EDGES, (
                f"Law {t.law_id} uses edge {t.source_layer.value}→{t.target_layer.value} "
                f"which is not in the valid adjacency graph"
            )

    def test_check_transition_licensed_all_pass(self):
        """When all conditions pass, verdict is LICENSED."""
        verdict = check_transition_licensed(
            law_id="LETTER_HARAKA_LINK",
            carrier_exists=True,
            domain_declared=True,
            identity_preserved=True,
            condition_holds=True,
            cause_exists=True,
            preventer_active=False,
        )
        assert verdict == TransitionVerdict.LICENSED

    def test_check_transition_blocked_by_preventer(self):
        """When preventer is active, verdict is the law's failure verdict."""
        verdict = check_transition_licensed(
            law_id="LETTER_HARAKA_LINK",
            carrier_exists=True,
            domain_declared=True,
            identity_preserved=True,
            condition_holds=True,
            cause_exists=True,
            preventer_active=True,
        )
        assert verdict == TransitionVerdict.RESIDUAL

    def test_check_transition_missing_carrier(self):
        """When carrier is missing, transition fails."""
        verdict = check_transition_licensed(
            law_id="UNICODE_TO_GLYPH",
            carrier_exists=False,
            domain_declared=True,
            identity_preserved=True,
            condition_holds=True,
            cause_exists=True,
            preventer_active=False,
        )
        assert verdict == TransitionVerdict.BLOCKED

    def test_check_transition_missing_condition(self):
        """When condition fails, transition fails."""
        verdict = check_transition_licensed(
            law_id="VOCALIZED_UNIT_TO_SYLLABLE",
            carrier_exists=True,
            domain_declared=True,
            identity_preserved=True,
            condition_holds=False,
            cause_exists=True,
            preventer_active=False,
        )
        assert verdict == TransitionVerdict.DEFERRED

    def test_lafz_to_mufrad_has_context_residual(self):
        """LAFZ_TO_MUFRAD carries classification_may_require_context residual."""
        law = get_transition_law("LAFZ_TO_MUFRAD")
        assert "classification_may_require_context" in law.residuals
