"""
Test L1 Postulates — test_l1_postulate.py

Origin: docs/15_PROJECT_ROADMAP.md Phase 1 PR-11
Authority: docs/00_MAQOOL_CONSTITUTION.md §8

Verifies:
1. All 5 postulates are registered
2. Every postulate is frozen with proper birth guards
3. Every postulate carries trace_ref, rank=CANDIDATE, residuals
4. Category coverage: all 4 categories have postulates
5. Registry functions work correctly
6. Birth guards reject invalid constructions
"""
from __future__ import annotations

import pytest

from taaqqul_slot_geometry.constitution.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.L1.postulate import (
    POSTULATE_BY_ID,
    POSTULATE_P1,
    POSTULATE_P2,
    POSTULATE_P3,
    POSTULATE_P4,
    POSTULATE_P5,
    POSTULATES,
    Postulate,
    PostulateCategory,
    get_postulate,
    postulates_by_category,
    total_postulate_count,
    verify_postulate_coverage,
)


# ══════════════════════════════════════════════════════════════════════════════
# Test: Registry Completeness
# ══════════════════════════════════════════════════════════════════════════════


class TestRegistryCompleteness:
    """All 5 postulates must be registered."""

    EXPECTED_IDS = ["P1", "P2", "P3", "P4", "P5"]

    def test_exactly_5_postulates(self):
        """Registry must contain exactly 5 postulates."""
        assert total_postulate_count() == 5

    def test_all_expected_ids_present(self):
        """All expected postulate IDs must be present."""
        actual_ids = {p.postulate_id for p in POSTULATES}
        expected = set(self.EXPECTED_IDS)
        missing = expected - actual_ids
        assert missing == set(), f"Missing postulates: {missing}"

    def test_no_duplicate_ids(self):
        """No two postulates may share the same ID."""
        ids = [p.postulate_id for p in POSTULATES]
        assert len(ids) == len(set(ids)), "Duplicate IDs found"

    def test_postulate_by_id_dict_consistent(self):
        """POSTULATE_BY_ID must match POSTULATES tuple."""
        assert len(POSTULATE_BY_ID) == len(POSTULATES)
        for p in POSTULATES:
            assert p.postulate_id in POSTULATE_BY_ID
            assert POSTULATE_BY_ID[p.postulate_id] is p

    def test_constants_match_registry(self):
        """Named constants must be in the registry."""
        assert POSTULATE_P1 is POSTULATES[0]
        assert POSTULATE_P2 is POSTULATES[1]
        assert POSTULATE_P3 is POSTULATES[2]
        assert POSTULATE_P4 is POSTULATES[3]
        assert POSTULATE_P5 is POSTULATES[4]


# ══════════════════════════════════════════════════════════════════════════════
# Test: Constitutional Compliance (Frozen, trace_ref, rank, residuals)
# ══════════════════════════════════════════════════════════════════════════════


class TestConstitutionalCompliance:
    """Every postulate must comply with constitutional rules."""

    @pytest.mark.parametrize("postulate", POSTULATES)
    def test_postulate_is_frozen(self, postulate: Postulate):
        """Every Postulate must be immutable (Rule 3)."""
        with pytest.raises(AttributeError):
            postulate.name = "mutated"  # type: ignore[misc]

    @pytest.mark.parametrize("postulate", POSTULATES)
    def test_has_trace_ref(self, postulate: Postulate):
        """Every postulate must carry a non-empty trace_ref."""
        assert postulate.trace_ref
        assert "docs/" in postulate.trace_ref

    @pytest.mark.parametrize("postulate", POSTULATES)
    def test_rank_is_candidate(self, postulate: Postulate):
        """Every postulate must have rank='CANDIDATE'."""
        assert postulate.rank == "CANDIDATE"

    @pytest.mark.parametrize("postulate", POSTULATES)
    def test_has_residuals(self, postulate: Postulate):
        """Every postulate must carry a residuals field (FrozenSet)."""
        assert isinstance(postulate.residuals, frozenset)

    @pytest.mark.parametrize("postulate", POSTULATES)
    def test_has_constitution_ref(self, postulate: Postulate):
        """Every postulate must reference the constitution."""
        assert postulate.constitution_ref
        assert "docs/" in postulate.constitution_ref

    @pytest.mark.parametrize("postulate", POSTULATES)
    def test_has_postulate_id(self, postulate: Postulate):
        """Every postulate must have a non-empty ID."""
        assert postulate.postulate_id
        assert postulate.postulate_id.startswith("P")

    @pytest.mark.parametrize("postulate", POSTULATES)
    def test_has_name(self, postulate: Postulate):
        """Every postulate must have a non-empty name."""
        assert postulate.name

    @pytest.mark.parametrize("postulate", POSTULATES)
    def test_has_name_ar(self, postulate: Postulate):
        """Every postulate must have a non-empty Arabic name."""
        assert postulate.name_ar

    @pytest.mark.parametrize("postulate", POSTULATES)
    def test_has_statement(self, postulate: Postulate):
        """Every postulate must have a non-empty statement."""
        assert postulate.statement


# ══════════════════════════════════════════════════════════════════════════════
# Test: Postulate Content Verification
# ══════════════════════════════════════════════════════════════════════════════


class TestPostulateContent:
    """Verify the content of each postulate matches the constitution."""

    def test_p1_sound_primacy(self):
        """P1 must assert sound primacy."""
        assert POSTULATE_P1.postulate_id == "P1"
        assert POSTULATE_P1.name == "Sound Primacy"
        assert POSTULATE_P1.name_ar == "أولوية الصوت"
        assert "signifier" in POSTULATE_P1.statement
        assert "phonological" in POSTULATE_P1.statement
        assert POSTULATE_P1.category == PostulateCategory.GROUNDING

    def test_p2_closure(self):
        """P2 must assert layer closure."""
        assert POSTULATE_P2.postulate_id == "P2"
        assert POSTULATE_P2.name == "Closure"
        assert POSTULATE_P2.name_ar == "الإغلاق"
        assert "closed" in POSTULATE_P2.statement
        assert POSTULATE_P2.category == PostulateCategory.STRUCTURAL

    def test_p3_identity_preservation(self):
        """P3 must assert identity preservation."""
        assert POSTULATE_P3.postulate_id == "P3"
        assert POSTULATE_P3.name == "Identity Preservation"
        assert POSTULATE_P3.name_ar == "ثبات الهوية"
        assert "Identity" in POSTULATE_P3.statement
        assert POSTULATE_P3.category == PostulateCategory.PRESERVATION

    def test_p4_no_meaning_from_weight(self):
        """P4 must assert no meaning from weight."""
        assert POSTULATE_P4.postulate_id == "P4"
        assert POSTULATE_P4.name == "No Meaning from Weight"
        assert POSTULATE_P4.name_ar == "لا معنى من الوزن"
        assert "weight" in POSTULATE_P4.statement.lower()
        assert "meaning" in POSTULATE_P4.statement.lower()
        assert POSTULATE_P4.category == PostulateCategory.CONSTRAINT

    def test_p5_exhaustiveness(self):
        """P5 must assert exhaustiveness."""
        assert POSTULATE_P5.postulate_id == "P5"
        assert POSTULATE_P5.name == "Exhaustiveness"
        assert POSTULATE_P5.name_ar == "الاستيعاب"
        assert "8" in POSTULATE_P5.statement
        assert "4" in POSTULATE_P5.statement
        assert "28" in POSTULATE_P5.statement
        assert POSTULATE_P5.category == PostulateCategory.STRUCTURAL


# ══════════════════════════════════════════════════════════════════════════════
# Test: Category Coverage
# ══════════════════════════════════════════════════════════════════════════════


class TestCategoryCoverage:
    """All 4 postulate categories must be populated."""

    def test_grounding_category_has_postulates(self):
        """GROUNDING category must have postulates."""
        posts = postulates_by_category(PostulateCategory.GROUNDING)
        assert len(posts) == 1  # P1

    def test_structural_category_has_postulates(self):
        """STRUCTURAL category must have postulates."""
        posts = postulates_by_category(PostulateCategory.STRUCTURAL)
        assert len(posts) == 2  # P2, P5

    def test_preservation_category_has_postulates(self):
        """PRESERVATION category must have postulates."""
        posts = postulates_by_category(PostulateCategory.PRESERVATION)
        assert len(posts) == 1  # P3

    def test_constraint_category_has_postulates(self):
        """CONSTRAINT category must have postulates."""
        posts = postulates_by_category(PostulateCategory.CONSTRAINT)
        assert len(posts) == 1  # P4

    def test_categories_sum_to_5(self):
        """Sum of all category counts must equal 5."""
        total = sum(
            len(postulates_by_category(c))
            for c in PostulateCategory
        )
        assert total == 5

    def test_verify_postulate_coverage_passes(self):
        """verify_postulate_coverage must return True."""
        assert verify_postulate_coverage() is True


# ══════════════════════════════════════════════════════════════════════════════
# Test: Related Failure Codes
# ══════════════════════════════════════════════════════════════════════════════


class TestRelatedFailureCodes:
    """Postulates must reference their related failure codes."""

    def test_p1_has_related_failure_codes(self):
        """P1 must reference sound-related failure codes."""
        assert len(POSTULATE_P1.related_failure_codes) >= 1
        assert FailureCode.M_00_01.value in POSTULATE_P1.related_failure_codes

    def test_p2_has_related_failure_codes(self):
        """P2 must reference layer-crossing failure codes."""
        assert len(POSTULATE_P2.related_failure_codes) >= 1
        assert FailureCode.M_CX_02.value in POSTULATE_P2.related_failure_codes

    def test_p3_has_related_failure_codes(self):
        """P3 must reference identity-loss failure codes."""
        assert len(POSTULATE_P3.related_failure_codes) >= 1
        assert FailureCode.M_CX_01.value in POSTULATE_P3.related_failure_codes

    def test_p4_has_related_failure_codes(self):
        """P4 must reference weight-meaning failure codes."""
        assert len(POSTULATE_P4.related_failure_codes) >= 1
        assert FailureCode.M_02_19.value in POSTULATE_P4.related_failure_codes

    def test_p5_has_related_failure_codes(self):
        """P5 must reference closed-set violation failure codes."""
        assert len(POSTULATE_P5.related_failure_codes) >= 1
        assert FailureCode.M_00_02.value in POSTULATE_P5.related_failure_codes


# ══════════════════════════════════════════════════════════════════════════════
# Test: Birth Guards
# ══════════════════════════════════════════════════════════════════════════════


class TestPostulateBirthGuards:
    """Postulate birth guards must reject invalid constructions."""

    def _valid_kwargs(self) -> dict:
        """Baseline valid kwargs for Postulate."""
        return {
            "postulate_id": "P-TEST",
            "name": "Test Postulate",
            "name_ar": "مسلّمة اختبارية",
            "statement": "This is a test statement.",
            "category": PostulateCategory.GROUNDING,
            "constitution_ref": "docs/00_MAQOOL_CONSTITUTION.md §8",
        }

    def test_rejects_empty_postulate_id(self):
        """Empty postulate_id must be rejected (M_01_09)."""
        kwargs = self._valid_kwargs()
        kwargs["postulate_id"] = ""
        with pytest.raises(ValueError, match=FailureCode.M_01_09.value):
            Postulate(**kwargs)

    def test_rejects_empty_name(self):
        """Empty name must be rejected (M_01_09)."""
        kwargs = self._valid_kwargs()
        kwargs["name"] = ""
        with pytest.raises(ValueError, match=FailureCode.M_01_09.value):
            Postulate(**kwargs)

    def test_rejects_empty_name_ar(self):
        """Empty name_ar must be rejected (M_01_09)."""
        kwargs = self._valid_kwargs()
        kwargs["name_ar"] = ""
        with pytest.raises(ValueError, match=FailureCode.M_01_09.value):
            Postulate(**kwargs)

    def test_rejects_empty_statement(self):
        """Empty statement must be rejected (M_01_09)."""
        kwargs = self._valid_kwargs()
        kwargs["statement"] = ""
        with pytest.raises(ValueError, match=FailureCode.M_01_09.value):
            Postulate(**kwargs)

    def test_rejects_invalid_category(self):
        """Invalid category must be rejected (M_01_19)."""
        kwargs = self._valid_kwargs()
        kwargs["category"] = "not_a_category"
        with pytest.raises(ValueError, match=FailureCode.M_01_19.value):
            Postulate(**kwargs)

    def test_rejects_empty_constitution_ref(self):
        """Empty constitution_ref must be rejected (M_01_03)."""
        kwargs = self._valid_kwargs()
        kwargs["constitution_ref"] = ""
        with pytest.raises(ValueError, match=FailureCode.M_01_03.value):
            Postulate(**kwargs)

    def test_rejects_empty_trace_ref(self):
        """Empty trace_ref must be rejected (M_01_14)."""
        kwargs = self._valid_kwargs()
        kwargs["trace_ref"] = ""
        with pytest.raises(ValueError, match=FailureCode.M_01_14.value):
            Postulate(**kwargs)

    def test_rejects_rank_promotion(self):
        """Rank promotion must be rejected (M_01_16)."""
        kwargs = self._valid_kwargs()
        kwargs["rank"] = "PROMOTED"
        with pytest.raises(ValueError, match=FailureCode.M_01_16.value):
            Postulate(**kwargs)


# ══════════════════════════════════════════════════════════════════════════════
# Test: Lookup Functions
# ══════════════════════════════════════════════════════════════════════════════


class TestLookupFunctions:
    """Registry lookup functions must work correctly."""

    def test_get_postulate_valid_id(self):
        """get_postulate must return the correct postulate for valid IDs."""
        p = get_postulate("P1")
        assert p is POSTULATE_P1

    def test_get_postulate_all_ids(self):
        """get_postulate must work for all 5 IDs."""
        for pid in ["P1", "P2", "P3", "P4", "P5"]:
            p = get_postulate(pid)
            assert p.postulate_id == pid

    def test_get_postulate_invalid_id(self):
        """get_postulate must raise for unknown IDs."""
        with pytest.raises(ValueError, match=FailureCode.M_01_09.value):
            get_postulate("P99")

    def test_postulates_by_category_returns_correct_count(self):
        """postulates_by_category must return correct counts."""
        structural = postulates_by_category(PostulateCategory.STRUCTURAL)
        assert len(structural) == 2

    def test_total_postulate_count(self):
        """total_postulate_count must return 5."""
        assert total_postulate_count() == 5
