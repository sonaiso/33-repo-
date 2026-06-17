"""
Test L1 Postulates — test_l1_postulate.py

Origin: docs/15_PROJECT_ROADMAP.md Phase 1 PR-11
Authority: docs/00_MAQOOL_CONSTITUTION.md §8

Verifies:
1. All 5 structural postulates are registered
2. All 12 operational axioms are registered
3. Every postulate/axiom is frozen with proper birth guards
4. Every postulate/axiom carries trace_ref, rank=CANDIDATE, residuals
5. Category coverage: all 5 categories have postulates/axioms
6. Registry functions work correctly
7. Birth guards reject invalid constructions
"""
from __future__ import annotations

import pytest

from taaqqul_slot_geometry.constitution.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.L1.postulate import (
    ALL_POSTULATES_AND_AXIOMS,
    AXIOM_OA1,
    AXIOM_OA2,
    AXIOM_OA3,
    AXIOM_OA4,
    AXIOM_OA5,
    AXIOM_OA6,
    AXIOM_OA7,
    AXIOM_OA8,
    AXIOM_OA9,
    AXIOM_OA10,
    AXIOM_OA11,
    AXIOM_OA12,
    OPERATIONAL_AXIOMS,
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
    total_axiom_count,
    total_combined_count,
    total_postulate_count,
    verify_postulate_coverage,
)


# ══════════════════════════════════════════════════════════════════════════════
# Test: Registry Completeness
# ══════════════════════════════════════════════════════════════════════════════


class TestRegistryCompleteness:
    """All 5 structural postulates and 12 operational axioms must be registered."""

    EXPECTED_STRUCTURAL_IDS = ["P1", "P2", "P3", "P4", "P5"]
    EXPECTED_AXIOM_IDS = [
        "OA1", "OA2", "OA3", "OA4", "OA5", "OA6",
        "OA7", "OA8", "OA9", "OA10", "OA11", "OA12",
    ]

    def test_exactly_5_postulates(self):
        """Registry must contain exactly 5 structural postulates."""
        assert total_postulate_count() == 5

    def test_exactly_12_axioms(self):
        """Registry must contain exactly 12 operational axioms."""
        assert total_axiom_count() == 12

    def test_exactly_17_combined(self):
        """Combined registry must have 17 total (5 + 12)."""
        assert total_combined_count() == 17

    def test_all_structural_ids_present(self):
        """All expected structural postulate IDs must be present."""
        actual_ids = {p.postulate_id for p in POSTULATES}
        expected = set(self.EXPECTED_STRUCTURAL_IDS)
        missing = expected - actual_ids
        assert missing == set(), f"Missing postulates: {missing}"

    def test_all_axiom_ids_present(self):
        """All expected operational axiom IDs must be present."""
        actual_ids = {a.postulate_id for a in OPERATIONAL_AXIOMS}
        expected = set(self.EXPECTED_AXIOM_IDS)
        missing = expected - actual_ids
        assert missing == set(), f"Missing axioms: {missing}"

    def test_no_duplicate_ids(self):
        """No two postulates/axioms may share the same ID."""
        ids = [p.postulate_id for p in ALL_POSTULATES_AND_AXIOMS]
        assert len(ids) == len(set(ids)), "Duplicate IDs found"

    def test_postulate_by_id_dict_consistent(self):
        """POSTULATE_BY_ID must match ALL_POSTULATES_AND_AXIOMS tuple."""
        assert len(POSTULATE_BY_ID) == len(ALL_POSTULATES_AND_AXIOMS)
        for p in ALL_POSTULATES_AND_AXIOMS:
            assert p.postulate_id in POSTULATE_BY_ID
            assert POSTULATE_BY_ID[p.postulate_id] is p

    def test_structural_constants_match_registry(self):
        """Named structural constants must be in the registry."""
        assert POSTULATE_P1 is POSTULATES[0]
        assert POSTULATE_P2 is POSTULATES[1]
        assert POSTULATE_P3 is POSTULATES[2]
        assert POSTULATE_P4 is POSTULATES[3]
        assert POSTULATE_P5 is POSTULATES[4]

    def test_axiom_constants_match_registry(self):
        """Named axiom constants must be in the registry."""
        assert AXIOM_OA1 is OPERATIONAL_AXIOMS[0]
        assert AXIOM_OA2 is OPERATIONAL_AXIOMS[1]
        assert AXIOM_OA3 is OPERATIONAL_AXIOMS[2]
        assert AXIOM_OA4 is OPERATIONAL_AXIOMS[3]
        assert AXIOM_OA5 is OPERATIONAL_AXIOMS[4]
        assert AXIOM_OA6 is OPERATIONAL_AXIOMS[5]
        assert AXIOM_OA7 is OPERATIONAL_AXIOMS[6]
        assert AXIOM_OA8 is OPERATIONAL_AXIOMS[7]
        assert AXIOM_OA9 is OPERATIONAL_AXIOMS[8]
        assert AXIOM_OA10 is OPERATIONAL_AXIOMS[9]
        assert AXIOM_OA11 is OPERATIONAL_AXIOMS[10]
        assert AXIOM_OA12 is OPERATIONAL_AXIOMS[11]


# ══════════════════════════════════════════════════════════════════════════════
# Test: Constitutional Compliance (Frozen, trace_ref, rank, residuals)
# ══════════════════════════════════════════════════════════════════════════════


class TestConstitutionalCompliance:
    """Every postulate/axiom must comply with constitutional rules."""

    @pytest.mark.parametrize("postulate", ALL_POSTULATES_AND_AXIOMS)
    def test_postulate_is_frozen(self, postulate: Postulate):
        """Every Postulate must be immutable (Rule 3)."""
        with pytest.raises(AttributeError):
            postulate.name = "mutated"  # type: ignore[misc]

    @pytest.mark.parametrize("postulate", ALL_POSTULATES_AND_AXIOMS)
    def test_has_trace_ref(self, postulate: Postulate):
        """Every postulate/axiom must carry a non-empty trace_ref."""
        assert postulate.trace_ref
        assert "docs/" in postulate.trace_ref

    @pytest.mark.parametrize("postulate", ALL_POSTULATES_AND_AXIOMS)
    def test_rank_is_candidate(self, postulate: Postulate):
        """Every postulate/axiom must have rank='CANDIDATE'."""
        assert postulate.rank == "CANDIDATE"

    @pytest.mark.parametrize("postulate", ALL_POSTULATES_AND_AXIOMS)
    def test_has_residuals(self, postulate: Postulate):
        """Every postulate/axiom must carry a residuals field (FrozenSet)."""
        assert isinstance(postulate.residuals, frozenset)

    @pytest.mark.parametrize("postulate", ALL_POSTULATES_AND_AXIOMS)
    def test_has_constitution_ref(self, postulate: Postulate):
        """Every postulate/axiom must reference the constitution."""
        assert postulate.constitution_ref
        assert "docs/" in postulate.constitution_ref

    @pytest.mark.parametrize("postulate", ALL_POSTULATES_AND_AXIOMS)
    def test_has_postulate_id(self, postulate: Postulate):
        """Every postulate/axiom must have a non-empty ID."""
        assert postulate.postulate_id

    @pytest.mark.parametrize("postulate", ALL_POSTULATES_AND_AXIOMS)
    def test_has_name(self, postulate: Postulate):
        """Every postulate/axiom must have a non-empty name."""
        assert postulate.name

    @pytest.mark.parametrize("postulate", ALL_POSTULATES_AND_AXIOMS)
    def test_has_name_ar(self, postulate: Postulate):
        """Every postulate/axiom must have a non-empty Arabic name."""
        assert postulate.name_ar

    @pytest.mark.parametrize("postulate", ALL_POSTULATES_AND_AXIOMS)
    def test_has_statement(self, postulate: Postulate):
        """Every postulate/axiom must have a non-empty statement."""
        assert postulate.statement


# ══════════════════════════════════════════════════════════════════════════════
# Test: Structural Postulate Content Verification
# ══════════════════════════════════════════════════════════════════════════════


class TestPostulateContent:
    """Verify the content of each structural postulate matches the constitution."""

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
# Test: Operational Axiom Content Verification
# ══════════════════════════════════════════════════════════════════════════════


class TestOperationalAxiomContent:
    """Verify the content of each operational axiom."""

    def test_oa1_origin_precedes_branch(self):
        """OA1 must assert origin precedes branch."""
        assert AXIOM_OA1.postulate_id == "OA1"
        assert AXIOM_OA1.name == "Origin Precedes Branch"
        assert "origin" in AXIOM_OA1.statement.lower()
        assert "branch" in AXIOM_OA1.statement.lower()
        assert AXIOM_OA1.category == PostulateCategory.OPERATIONAL

    def test_oa2_no_weight_without_origin(self):
        """OA2 must assert no weight without origin."""
        assert AXIOM_OA2.postulate_id == "OA2"
        assert AXIOM_OA2.name == "No Weight Without Origin"
        assert "weight" in AXIOM_OA2.statement.lower()
        assert "origin" in AXIOM_OA2.statement.lower()
        assert AXIOM_OA2.category == PostulateCategory.OPERATIONAL

    def test_oa3_no_origin_without_prior_knowledge(self):
        """OA3 must assert no origin without prior knowledge."""
        assert AXIOM_OA3.postulate_id == "OA3"
        assert AXIOM_OA3.name == "No Origin Without Prior Knowledge"
        assert "prior" in AXIOM_OA3.statement.lower()
        assert "knowledge" in AXIOM_OA3.statement.lower()
        assert AXIOM_OA3.category == PostulateCategory.OPERATIONAL

    def test_oa4_no_branch_without_shared_illah(self):
        """OA4 must assert no branch without shared illah."""
        assert AXIOM_OA4.postulate_id == "OA4"
        assert AXIOM_OA4.name == "No Branch Without Shared Illah"
        assert "illah" in AXIOM_OA4.statement.lower()
        assert AXIOM_OA4.category == PostulateCategory.OPERATIONAL

    def test_oa5_no_illah_without_attribute(self):
        """OA5 must assert no illah without effective attribute."""
        assert AXIOM_OA5.postulate_id == "OA5"
        assert AXIOM_OA5.name == "No Illah Without Effective Attribute"
        assert "attribute" in AXIOM_OA5.statement.lower()
        assert AXIOM_OA5.category == PostulateCategory.OPERATIONAL

    def test_oa6_preventer_blocks_transition(self):
        """OA6 must assert preventer blocks transition."""
        assert AXIOM_OA6.postulate_id == "OA6"
        assert AXIOM_OA6.name == "Preventer Blocks Transition"
        assert "preventer" in AXIOM_OA6.statement.lower()
        assert AXIOM_OA6.category == PostulateCategory.OPERATIONAL

    def test_oa7_invalidating_difference(self):
        """OA7 must assert invalidating difference blocks or lowers rank."""
        assert AXIOM_OA7.postulate_id == "OA7"
        assert AXIOM_OA7.name == "Invalidating Difference"
        assert "invalidating" in AXIOM_OA7.statement.lower()
        assert AXIOM_OA7.category == PostulateCategory.OPERATIONAL

    def test_oa8_visible_residuals(self):
        """OA8 must assert residuals are always visible."""
        assert AXIOM_OA8.postulate_id == "OA8"
        assert AXIOM_OA8.name == "Visible Residuals"
        assert "residual" in AXIOM_OA8.statement.lower()
        assert AXIOM_OA8.category == PostulateCategory.OPERATIONAL

    def test_oa9_morphology_does_not_produce_hukm(self):
        """OA9 must assert morphology does not produce hukm."""
        assert AXIOM_OA9.postulate_id == "OA9"
        assert AXIOM_OA9.name == "Morphology Does Not Produce Hukm"
        assert "judgment" in AXIOM_OA9.statement.lower()
        assert AXIOM_OA9.category == PostulateCategory.OPERATIONAL

    def test_oa10_syntax_does_not_produce_reality(self):
        """OA10 must assert syntax does not produce reality."""
        assert AXIOM_OA10.postulate_id == "OA10"
        assert AXIOM_OA10.name == "Syntax Does Not Produce Reality"
        assert "reality" in AXIOM_OA10.statement.lower()
        assert AXIOM_OA10.category == PostulateCategory.OPERATIONAL

    def test_oa11_ifadah_requires_evidence(self):
        """OA11 must assert ifadah requires evidence."""
        assert AXIOM_OA11.postulate_id == "OA11"
        assert AXIOM_OA11.name == "Ifadah Requires Evidence"
        assert "evidence" in AXIOM_OA11.statement.lower()
        assert AXIOM_OA11.category == PostulateCategory.OPERATIONAL

    def test_oa12_evidence_requires_tahqiq(self):
        """OA12 must assert evidence requires tahqiq al-manat."""
        assert AXIOM_OA12.postulate_id == "OA12"
        assert AXIOM_OA12.name == "Evidence Requires Tahqiq al-Manat"
        assert "tahqiq" in AXIOM_OA12.statement.lower()
        assert AXIOM_OA12.category == PostulateCategory.OPERATIONAL


# ══════════════════════════════════════════════════════════════════════════════
# Test: Category Coverage
# ══════════════════════════════════════════════════════════════════════════════


class TestCategoryCoverage:
    """All 5 postulate categories must be populated."""

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

    def test_operational_category_has_axioms(self):
        """OPERATIONAL category must have 12 axioms."""
        posts = postulates_by_category(PostulateCategory.OPERATIONAL)
        assert len(posts) == 12

    def test_categories_sum_to_17(self):
        """Sum of all category counts must equal 17."""
        total = sum(
            len(postulates_by_category(c))
            for c in PostulateCategory
        )
        assert total == 17

    def test_verify_postulate_coverage_passes(self):
        """verify_postulate_coverage must return True."""
        assert verify_postulate_coverage() is True


# ══════════════════════════════════════════════════════════════════════════════
# Test: Related Failure Codes
# ══════════════════════════════════════════════════════════════════════════════


class TestRelatedFailureCodes:
    """Postulates/axioms must reference their related failure codes."""

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

    @pytest.mark.parametrize("axiom", OPERATIONAL_AXIOMS)
    def test_operational_axioms_have_failure_codes(self, axiom: Postulate):
        """Every operational axiom must reference at least one failure code."""
        assert len(axiom.related_failure_codes) >= 1


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

    def test_get_postulate_all_structural_ids(self):
        """get_postulate must work for all 5 structural IDs."""
        for pid in ["P1", "P2", "P3", "P4", "P5"]:
            p = get_postulate(pid)
            assert p.postulate_id == pid

    def test_get_postulate_all_axiom_ids(self):
        """get_postulate must work for all 12 operational axiom IDs."""
        for oa_id in [f"OA{i}" for i in range(1, 13)]:
            a = get_postulate(oa_id)
            assert a.postulate_id == oa_id

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

    def test_total_axiom_count(self):
        """total_axiom_count must return 12."""
        assert total_axiom_count() == 12

    def test_total_combined_count(self):
        """total_combined_count must return 17."""
        assert total_combined_count() == 17
