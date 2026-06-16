"""
Tests for Waqf-Wasl Boundary Economy Theorem (TH6.5).
Origin: docs/20_WAQF_WASL_BOUNDARY_THEOREM.md
"""
import pytest

from taaqqul_slot_geometry.constitution.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.L0.waqf_wasl import (
    CANONICAL_PROFILES,
    PROFILE_HADHA,
    PROFILE_KANA,
    PROFILE_KATABA,
    PROFILE_MIN,
    PROFILE_RAJUL,
    BoundaryLevel,
    BoundaryTest,
    WaqfStatus,
    WaqfWaslProfile,
    WordPath,
    can_stop,
    guard_harf_has_operand,
    guard_incomplete_verb_has_complement,
    guard_no_semantic_without_relation,
    guard_no_weight_before_word,
    guard_no_word_before_syllable,
    guard_phonetic_stop_not_meaning,
    guard_structural_stop_not_ifadah,
    guard_sub_ternary_not_in_weight,
    must_join,
    required_complement_at,
)


# ══════════════════════════════════════════════════════════════════════════════
# §1  BoundaryTest entity tests
# ══════════════════════════════════════════════════════════════════════════════


class TestBoundaryTest:
    """Test BoundaryTest entity construction and guards."""

    def test_closed_boundary_no_complement(self):
        """A closed boundary needs no complement."""
        bt = BoundaryTest(
            level=BoundaryLevel.PHONETIC,
            status=WaqfStatus.CLOSED,
        )
        assert bt.level == BoundaryLevel.PHONETIC
        assert bt.status == WaqfStatus.CLOSED
        assert bt.required_complement == ""
        assert bt.rank == "CANDIDATE"

    def test_open_boundary_requires_complement(self):
        """An open boundary must declare its required complement."""
        bt = BoundaryTest(
            level=BoundaryLevel.FUNCTIONAL,
            status=WaqfStatus.OPEN,
            required_complement="majrur",
        )
        assert bt.status == WaqfStatus.OPEN
        assert bt.required_complement == "majrur"

    def test_open_boundary_without_complement_fails(self):
        """Opening a boundary without declaring complement violates M_WW_04."""
        with pytest.raises(ValueError, match=FailureCode.M_WW_04.value):
            BoundaryTest(
                level=BoundaryLevel.FUNCTIONAL,
                status=WaqfStatus.OPEN,
                required_complement="",
            )

    def test_missing_trace_ref_fails(self):
        """Missing trace_ref violates M_00_11."""
        with pytest.raises(ValueError, match=FailureCode.M_00_11.value):
            BoundaryTest(
                level=BoundaryLevel.PHONETIC,
                status=WaqfStatus.CLOSED,
                trace_ref="",
            )

    def test_rank_promotion_fails(self):
        """Rank != CANDIDATE violates M_00_10."""
        with pytest.raises(ValueError, match=FailureCode.M_00_10.value):
            BoundaryTest(
                level=BoundaryLevel.PHONETIC,
                status=WaqfStatus.CLOSED,
                rank="PROMOTED",
            )

    def test_frozen(self):
        """BoundaryTest must be frozen (Rule 3)."""
        bt = BoundaryTest(
            level=BoundaryLevel.PHONETIC,
            status=WaqfStatus.CLOSED,
        )
        with pytest.raises(Exception):
            bt.status = WaqfStatus.OPEN  # type: ignore[misc]


# ══════════════════════════════════════════════════════════════════════════════
# §2  WaqfWaslProfile entity tests
# ══════════════════════════════════════════════════════════════════════════════


class TestWaqfWaslProfile:
    """Test WaqfWaslProfile entity construction and properties."""

    def test_valid_profile_construction(self):
        """A valid profile with all 4 levels passes."""
        profile = WaqfWaslProfile(
            unit_label="test",
            word_path=WordPath.ISM_MUTAMAKKIN,
            tests=(
                BoundaryTest(level=BoundaryLevel.PHONETIC, status=WaqfStatus.CLOSED),
                BoundaryTest(level=BoundaryLevel.STRUCTURAL, status=WaqfStatus.CLOSED),
                BoundaryTest(level=BoundaryLevel.FUNCTIONAL, status=WaqfStatus.CLOSED),
                BoundaryTest(
                    level=BoundaryLevel.SEMANTIC,
                    status=WaqfStatus.OPEN,
                    required_complement="tarkib",
                ),
            ),
        )
        assert profile.unit_label == "test"
        assert profile.word_path == WordPath.ISM_MUTAMAKKIN

    def test_missing_level_fails(self):
        """Profile missing a boundary level fails."""
        with pytest.raises(ValueError, match="missing_boundary_levels"):
            WaqfWaslProfile(
                unit_label="incomplete",
                word_path=WordPath.HARF,
                tests=(
                    BoundaryTest(level=BoundaryLevel.PHONETIC, status=WaqfStatus.CLOSED),
                    BoundaryTest(level=BoundaryLevel.STRUCTURAL, status=WaqfStatus.CLOSED),
                    BoundaryTest(
                        level=BoundaryLevel.FUNCTIONAL,
                        status=WaqfStatus.OPEN,
                        required_complement="x",
                    ),
                    # SEMANTIC missing!
                ),
            )

    def test_empty_label_fails(self):
        """Empty unit_label fails."""
        with pytest.raises(ValueError, match="unit_label_empty"):
            WaqfWaslProfile(
                unit_label="",
                word_path=WordPath.HARF,
                tests=(
                    BoundaryTest(level=BoundaryLevel.PHONETIC, status=WaqfStatus.CLOSED),
                    BoundaryTest(level=BoundaryLevel.STRUCTURAL, status=WaqfStatus.CLOSED),
                    BoundaryTest(
                        level=BoundaryLevel.FUNCTIONAL,
                        status=WaqfStatus.OPEN,
                        required_complement="x",
                    ),
                    BoundaryTest(
                        level=BoundaryLevel.SEMANTIC,
                        status=WaqfStatus.OPEN,
                        required_complement="y",
                    ),
                ),
            )

    def test_frozen(self):
        """WaqfWaslProfile must be frozen (Rule 3)."""
        with pytest.raises(Exception):
            PROFILE_MIN.unit_label = "changed"  # type: ignore[misc]


# ══════════════════════════════════════════════════════════════════════════════
# §3  Canonical profile tests (TH6.5 §5 examples)
# ══════════════════════════════════════════════════════════════════════════════


class TestCanonicalProfiles:
    """Test canonical profiles match the theorem's declarations."""

    def test_min_is_harf(self):
        """'min' is classified as harf (particle)."""
        assert PROFILE_MIN.word_path == WordPath.HARF

    def test_min_phonetic_closed(self):
        """'min' can stop phonetically (it is pronounceable)."""
        assert PROFILE_MIN.can_stop_phonetic is True

    def test_min_structural_closed(self):
        """'min' is structurally complete as a particle."""
        assert PROFILE_MIN.can_stop_structural is True

    def test_min_functional_open(self):
        """'min' cannot stop functionally — it needs a majrur."""
        assert PROFILE_MIN.can_stop_functional is False

    def test_min_semantic_open(self):
        """'min' cannot achieve meaning alone — it needs connection."""
        assert PROFILE_MIN.can_stop_semantic is False

    def test_rajul_all_closed_except_semantic(self):
        """'rajul' is independent lexically but not for ifadah."""
        assert PROFILE_RAJUL.can_stop_phonetic is True
        assert PROFILE_RAJUL.can_stop_structural is True
        assert PROFILE_RAJUL.can_stop_functional is True
        assert PROFILE_RAJUL.can_stop_semantic is False

    def test_kataba_needs_fa_il(self):
        """'kataba' (complete verb) needs a subject."""
        assert PROFILE_KATABA.can_stop_phonetic is True
        assert PROFILE_KATABA.can_stop_structural is True
        assert PROFILE_KATABA.can_stop_functional is False
        assert PROFILE_KATABA.can_stop_semantic is False

    def test_kana_incomplete_verb(self):
        """'kana' (incomplete verb) needs ism and khabar."""
        assert PROFILE_KANA.word_path == WordPath.FI_L_NAQIS
        assert PROFILE_KANA.can_stop_functional is False
        assert PROFILE_KANA.can_stop_semantic is False

    def test_hadha_mabni(self):
        """'hadha' (demonstrative) is built but referentially open."""
        assert PROFILE_HADHA.word_path == WordPath.ISM_MABNI
        assert PROFILE_HADHA.can_stop_phonetic is True
        assert PROFILE_HADHA.can_stop_structural is True
        assert PROFILE_HADHA.can_stop_functional is False
        assert PROFILE_HADHA.can_stop_semantic is False

    def test_all_canonical_profiles_have_trace_ref(self):
        """All canonical profiles carry trace_ref (Rule 2)."""
        for profile in CANONICAL_PROFILES:
            assert profile.trace_ref != ""

    def test_all_canonical_profiles_are_candidates(self):
        """All canonical profiles have rank CANDIDATE (Rule 2)."""
        for profile in CANONICAL_PROFILES:
            assert profile.rank == "CANDIDATE"

    def test_canonical_profiles_count(self):
        """There are exactly 5 canonical profiles."""
        assert len(CANONICAL_PROFILES) == 5


# ══════════════════════════════════════════════════════════════════════════════
# §4  Pure function tests (can_stop, must_join)
# ══════════════════════════════════════════════════════════════════════════════


class TestPureFunctions:
    """Test pure boundary query functions."""

    def test_can_stop_true(self):
        """can_stop returns True for closed levels."""
        assert can_stop(PROFILE_RAJUL, BoundaryLevel.PHONETIC) is True

    def test_can_stop_false(self):
        """can_stop returns False for open levels."""
        assert can_stop(PROFILE_MIN, BoundaryLevel.FUNCTIONAL) is False

    def test_must_join_true(self):
        """must_join returns True for open levels."""
        assert must_join(PROFILE_MIN, BoundaryLevel.FUNCTIONAL) is True

    def test_must_join_false(self):
        """must_join returns False for closed levels."""
        assert must_join(PROFILE_RAJUL, BoundaryLevel.STRUCTURAL) is False

    def test_required_complement_for_open(self):
        """Required complement is returned for open levels."""
        complement = required_complement_at(PROFILE_MIN, BoundaryLevel.FUNCTIONAL)
        assert complement == "majrur (مجرور)"

    def test_required_complement_for_closed(self):
        """Required complement is empty string for closed levels."""
        complement = required_complement_at(PROFILE_RAJUL, BoundaryLevel.PHONETIC)
        assert complement == ""

    def test_must_join_levels(self):
        """must_join_levels returns all open levels."""
        levels = PROFILE_MIN.must_join_levels
        assert BoundaryLevel.FUNCTIONAL in levels
        assert BoundaryLevel.SEMANTIC in levels
        assert BoundaryLevel.PHONETIC not in levels


# ══════════════════════════════════════════════════════════════════════════════
# §5  Economy guard function tests
# ══════════════════════════════════════════════════════════════════════════════


class TestEconomyGuards:
    """Test economy guard functions enforce WW laws."""

    # WW-03: No weight before word boundary
    def test_guard_weight_before_word_raises(self):
        """Weight before word boundary raises M_WW_01."""
        with pytest.raises(ValueError, match=FailureCode.M_WW_01.value):
            guard_no_weight_before_word(
                has_word_boundary=False, attempting_weight=True
            )

    def test_guard_weight_after_word_passes(self):
        """Weight after word boundary is fine."""
        guard_no_weight_before_word(has_word_boundary=True, attempting_weight=True)

    # WW-04: No word before syllable license
    def test_guard_word_before_syllable_raises(self):
        """Word before syllable license raises M_WW_02."""
        with pytest.raises(ValueError, match=FailureCode.M_WW_02.value):
            guard_no_word_before_syllable(
                has_syllable_license=False, attempting_word=True
            )

    def test_guard_word_after_syllable_passes(self):
        """Word after syllable license is fine."""
        guard_no_word_before_syllable(has_syllable_license=True, attempting_word=True)

    # WW-14/P38: No semantic closure without relation
    def test_guard_semantic_without_relation_raises(self):
        """Claiming meaning without relation raises M_WW_03."""
        with pytest.raises(ValueError, match=FailureCode.M_WW_03.value):
            guard_no_semantic_without_relation(
                claiming_complete_meaning=True, has_licensed_relation=False
            )

    def test_guard_semantic_with_relation_passes(self):
        """Claiming meaning with relation is fine."""
        guard_no_semantic_without_relation(
            claiming_complete_meaning=True, has_licensed_relation=True
        )

    # WW-10: Harf must have operand
    def test_guard_harf_without_operand_raises(self):
        """Harf without operand raises M_WW_04."""
        with pytest.raises(ValueError, match=FailureCode.M_WW_04.value):
            guard_harf_has_operand(word_path=WordPath.HARF, has_operand=False)

    def test_guard_harf_with_operand_passes(self):
        """Harf with operand is fine."""
        guard_harf_has_operand(word_path=WordPath.HARF, has_operand=True)

    def test_guard_non_harf_without_operand_passes(self):
        """Non-harf doesn't need operand check."""
        guard_harf_has_operand(word_path=WordPath.ISM_MUTAMAKKIN, has_operand=False)

    # WW-09: Incomplete verb must have complement
    def test_guard_incomplete_verb_without_complement_raises(self):
        """Incomplete verb without complement raises M_WW_05."""
        with pytest.raises(ValueError, match=FailureCode.M_WW_05.value):
            guard_incomplete_verb_has_complement(
                word_path=WordPath.FI_L_NAQIS, has_complement=False
            )

    def test_guard_incomplete_verb_with_complement_passes(self):
        """Incomplete verb with complement is fine."""
        guard_incomplete_verb_has_complement(
            word_path=WordPath.FI_L_NAQIS, has_complement=True
        )

    # WW-15: Sub-ternary not in derivational weight
    def test_guard_sub_ternary_in_weight_raises(self):
        """Sub-ternary attempting weight raises M_WW_06."""
        with pytest.raises(ValueError, match=FailureCode.M_WW_06.value):
            guard_sub_ternary_not_in_weight(
                consonant_count=2, attempting_derivational_weight=True
            )

    def test_guard_ternary_in_weight_passes(self):
        """Ternary or above in weight is fine."""
        guard_sub_ternary_not_in_weight(
            consonant_count=3, attempting_derivational_weight=True
        )

    # WW-01/WW-07: Phonetic stop != meaning
    def test_guard_phonetic_stop_as_meaning_raises(self):
        """Claiming meaning from phonetic stop raises M_WW_07."""
        with pytest.raises(ValueError, match=FailureCode.M_WW_07.value):
            guard_phonetic_stop_not_meaning(
                can_stop_phonetic=True, claiming_meaning_from_stop=True
            )

    # WW-01/WW-08: Structural stop != ifadah
    def test_guard_structural_stop_as_ifadah_raises(self):
        """Claiming ifadah from structural stop raises M_WW_08."""
        with pytest.raises(ValueError, match=FailureCode.M_WW_08.value):
            guard_structural_stop_not_ifadah(
                can_stop_structural=True, claiming_ifadah_from_structure=True
            )


# ══════════════════════════════════════════════════════════════════════════════
# §6  Theorem invariant tests
# ══════════════════════════════════════════════════════════════════════════════


class TestTheoremInvariants:
    """Test the core invariants declared by TH6.5."""

    def test_phonetic_stop_does_not_imply_structural(self):
        """WW-01: Phonetic stop ≠ structural stop. (Step 5 of proof)"""
        # All canonical profiles are phonetically closed
        for profile in CANONICAL_PROFILES:
            assert profile.can_stop_phonetic is True
        # But not all are functionally/semantically closed
        assert PROFILE_MIN.can_stop_functional is False

    def test_structural_stop_does_not_imply_semantic(self):
        """WW-01: Structural stop ≠ semantic stop. (Step 6 of proof)"""
        # rajul is structurally closed but semantically open
        assert PROFILE_RAJUL.can_stop_structural is True
        assert PROFILE_RAJUL.can_stop_semantic is False

    def test_no_single_word_achieves_ifadah(self):
        """WW-06/P38: No single word achieves complete meaning alone."""
        for profile in CANONICAL_PROFILES:
            assert profile.can_stop_semantic is False

    def test_harf_is_always_functionally_open(self):
        """WW-10: Harf (particle) must join at functional level."""
        assert must_join(PROFILE_MIN, BoundaryLevel.FUNCTIONAL) is True

    def test_incomplete_verb_is_functionally_open(self):
        """WW-09: Incomplete verb must join at functional level."""
        assert must_join(PROFILE_KANA, BoundaryLevel.FUNCTIONAL) is True

    def test_ism_mutamakkin_lexically_independent(self):
        """WW-07: Full noun is functionally closed but semantically open."""
        assert PROFILE_RAJUL.can_stop_functional is True
        assert PROFILE_RAJUL.can_stop_semantic is False
