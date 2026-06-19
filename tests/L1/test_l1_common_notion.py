"""
Test L1 Common Notions — test_l1_common_notion.py

Origin: docs/15_PROJECT_ROADMAP.md Phase 1 PR-12
Authority: docs/00_MAQOOL_CONSTITUTION.md §6 L1

Verifies:
1. All 4 common notions are registered
2. Every common notion is frozen with proper birth guards
3. Every common notion carries trace_ref, rank=CANDIDATE, residuals
4. Domain coverage: all domains have common notions
5. Registry functions work correctly
6. Birth guards reject invalid constructions
7. Content matches constitutional specification
"""
from __future__ import annotations

import pytest

from taaqqul_slot_geometry.constitution.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.L1.common_notion import (
    COMMON_NOTION_BY_ID,
    COMMON_NOTION_CN1,
    COMMON_NOTION_CN2,
    COMMON_NOTION_CN3,
    COMMON_NOTION_CN4,
    COMMON_NOTIONS,
    CommonNotion,
    CommonNotionDomain,
    common_notions_by_domain,
    get_common_notion,
    total_common_notion_count,
    verify_common_notion_coverage,
)


# ══════════════════════════════════════════════════════════════════════════════
# Test: Registry Completeness
# ══════════════════════════════════════════════════════════════════════════════


class TestRegistryCompleteness:
    """All 4 common notions must be registered."""

    EXPECTED_IDS = ["CN1", "CN2", "CN3", "CN4"]

    def test_exactly_4_common_notions(self):
        """Registry must contain exactly 4 common notions."""
        assert total_common_notion_count() == 4

    def test_all_ids_present(self):
        """All expected common notion IDs must be present."""
        actual_ids = {cn.notion_id for cn in COMMON_NOTIONS}
        expected = set(self.EXPECTED_IDS)
        missing = expected - actual_ids
        assert missing == set(), f"Missing common notions: {missing}"

    def test_no_duplicate_ids(self):
        """No two common notions may share the same ID."""
        ids = [cn.notion_id for cn in COMMON_NOTIONS]
        assert len(ids) == len(set(ids)), "Duplicate IDs found"

    def test_common_notion_by_id_dict_consistent(self):
        """COMMON_NOTION_BY_ID must match COMMON_NOTIONS tuple."""
        assert len(COMMON_NOTION_BY_ID) == len(COMMON_NOTIONS)
        for cn in COMMON_NOTIONS:
            assert cn.notion_id in COMMON_NOTION_BY_ID
            assert COMMON_NOTION_BY_ID[cn.notion_id] is cn

    def test_constants_match_registry(self):
        """Named constants must be in the registry at correct positions."""
        assert COMMON_NOTION_CN1 is COMMON_NOTIONS[0]
        assert COMMON_NOTION_CN2 is COMMON_NOTIONS[1]
        assert COMMON_NOTION_CN3 is COMMON_NOTIONS[2]
        assert COMMON_NOTION_CN4 is COMMON_NOTIONS[3]


# ══════════════════════════════════════════════════════════════════════════════
# Test: Constitutional Compliance (Frozen, trace_ref, rank, residuals)
# ══════════════════════════════════════════════════════════════════════════════


class TestConstitutionalCompliance:
    """Every common notion must comply with constitutional rules."""

    @pytest.mark.parametrize("notion", COMMON_NOTIONS)
    def test_notion_is_frozen(self, notion: CommonNotion):
        """Every CommonNotion must be immutable (Rule 3)."""
        with pytest.raises(AttributeError):
            notion.name = "mutated"  # type: ignore[misc]

    @pytest.mark.parametrize("notion", COMMON_NOTIONS)
    def test_has_trace_ref(self, notion: CommonNotion):
        """Every common notion must carry a non-empty trace_ref."""
        assert notion.trace_ref
        assert "docs/" in notion.trace_ref

    @pytest.mark.parametrize("notion", COMMON_NOTIONS)
    def test_rank_is_candidate(self, notion: CommonNotion):
        """Every common notion must have rank='CANDIDATE'."""
        assert notion.rank == "CANDIDATE"

    @pytest.mark.parametrize("notion", COMMON_NOTIONS)
    def test_has_residuals(self, notion: CommonNotion):
        """Every common notion must carry a residuals field (FrozenSet)."""
        assert isinstance(notion.residuals, frozenset)

    @pytest.mark.parametrize("notion", COMMON_NOTIONS)
    def test_has_constitution_ref(self, notion: CommonNotion):
        """Every common notion must reference the constitution."""
        assert notion.constitution_ref
        assert "docs/" in notion.constitution_ref

    @pytest.mark.parametrize("notion", COMMON_NOTIONS)
    def test_has_notion_id(self, notion: CommonNotion):
        """Every common notion must have a non-empty ID."""
        assert notion.notion_id

    @pytest.mark.parametrize("notion", COMMON_NOTIONS)
    def test_has_name(self, notion: CommonNotion):
        """Every common notion must have a non-empty name."""
        assert notion.name

    @pytest.mark.parametrize("notion", COMMON_NOTIONS)
    def test_has_name_ar(self, notion: CommonNotion):
        """Every common notion must have a non-empty Arabic name."""
        assert notion.name_ar

    @pytest.mark.parametrize("notion", COMMON_NOTIONS)
    def test_has_statement(self, notion: CommonNotion):
        """Every common notion must have a non-empty statement."""
        assert notion.statement

    @pytest.mark.parametrize("notion", COMMON_NOTIONS)
    def test_has_formal_expression(self, notion: CommonNotion):
        """Every common notion must have a non-empty formal expression."""
        assert notion.formal_expression


# ══════════════════════════════════════════════════════════════════════════════
# Test: Common Notion Content Verification
# ══════════════════════════════════════════════════════════════════════════════


class TestCommonNotionContent:
    """Verify the content of each common notion matches the constitution."""

    def test_cn1_self_equality(self):
        """CN1 must assert self-equality."""
        assert COMMON_NOTION_CN1.notion_id == "CN1"
        assert COMMON_NOTION_CN1.name == "Self-Equality"
        assert COMMON_NOTION_CN1.name_ar == "المساواة الذاتية"
        assert COMMON_NOTION_CN1.statement == "Every entity is equal to itself."
        assert COMMON_NOTION_CN1.domain == CommonNotionDomain.EQUALITY
        assert COMMON_NOTION_CN1.formal_expression == "A=A"
        assert COMMON_NOTION_CN1.order == 1

    def test_cn2_whole_greater_than_part(self):
        """CN2 must assert whole-greater-than-part."""
        assert COMMON_NOTION_CN2.notion_id == "CN2"
        assert COMMON_NOTION_CN2.name == "Whole Greater Than Part"
        assert COMMON_NOTION_CN2.name_ar == "الكل أكبر من الجزء"
        assert COMMON_NOTION_CN2.statement == "If A contains B and B is not empty, then A is greater than B."
        assert COMMON_NOTION_CN2.domain == CommonNotionDomain.ORDER
        assert COMMON_NOTION_CN2.formal_expression == "B⊂A ∧ B≠∅ → A>B"
        assert COMMON_NOTION_CN2.order == 2

    def test_cn3_substitution(self):
        """CN3 must assert substitution."""
        assert COMMON_NOTION_CN3.notion_id == "CN3"
        assert COMMON_NOTION_CN3.name == "Substitution"
        assert COMMON_NOTION_CN3.name_ar == "الاستبدال"
        assert COMMON_NOTION_CN3.statement == "If A = B and B = C, then A = C."
        assert COMMON_NOTION_CN3.domain == CommonNotionDomain.EQUALITY
        assert COMMON_NOTION_CN3.formal_expression == "A=B ∧ B=C → A=C"
        assert COMMON_NOTION_CN3.order == 3

    def test_cn4_transitivity_of_subsumption(self):
        """CN4 must assert transitivity of subsumption."""
        assert COMMON_NOTION_CN4.notion_id == "CN4"
        assert COMMON_NOTION_CN4.name == "Transitivity of Subsumption"
        assert COMMON_NOTION_CN4.name_ar == "تعدّي الاشتمال"
        assert COMMON_NOTION_CN4.statement == (
            "If Identity(a) ⊆ Identity(b) and Identity(b) ⊆ Identity(c), "
            "then Identity(a) ⊆ Identity(c)."
        )
        assert COMMON_NOTION_CN4.domain == CommonNotionDomain.ORDER
        assert COMMON_NOTION_CN4.formal_expression == (
            "Identity(a) ⊆ Identity(b) ∧ Identity(b) ⊆ Identity(c) → Identity(a) ⊆ Identity(c)"
        )
        assert COMMON_NOTION_CN4.order == 4


# ══════════════════════════════════════════════════════════════════════════════
# Test: Domain Coverage
# ══════════════════════════════════════════════════════════════════════════════


class TestDomainCoverage:
    """All common notion domains must be populated."""

    def test_equality_domain_has_notions(self):
        """EQUALITY domain must have common notions."""
        notions = common_notions_by_domain(CommonNotionDomain.EQUALITY)
        assert len(notions) == 2  # CN1, CN3

    def test_order_domain_has_notions(self):
        """ORDER domain must have common notions."""
        notions = common_notions_by_domain(CommonNotionDomain.ORDER)
        assert len(notions) == 2  # CN2, CN4

    def test_domains_sum_to_4(self):
        """Sum of all domain counts must equal 4."""
        total = sum(
            len(common_notions_by_domain(d))
            for d in CommonNotionDomain
        )
        assert total == 4

    def test_verify_common_notion_coverage_passes(self):
        """verify_common_notion_coverage must return True."""
        assert verify_common_notion_coverage() is True


# ══════════════════════════════════════════════════════════════════════════════
# Test: Related Failure Codes
# ══════════════════════════════════════════════════════════════════════════════


class TestRelatedFailureCodes:
    """Common notions must reference their related failure codes."""

    def test_cn1_has_self_equality_failure_code(self):
        """CN1 must reference self-equality failure code."""
        assert len(COMMON_NOTION_CN1.related_failure_codes) >= 1
        assert FailureCode.M_01_10.value in COMMON_NOTION_CN1.related_failure_codes

    def test_cn2_has_whole_part_failure_code(self):
        """CN2 must reference whole-greater-than-part failure code."""
        assert len(COMMON_NOTION_CN2.related_failure_codes) >= 1
        assert FailureCode.M_01_11.value in COMMON_NOTION_CN2.related_failure_codes

    def test_cn3_has_substitution_failure_code(self):
        """CN3 must reference substitution failure code."""
        assert len(COMMON_NOTION_CN3.related_failure_codes) >= 1
        assert FailureCode.M_01_12.value in COMMON_NOTION_CN3.related_failure_codes

    def test_cn4_has_transitivity_failure_code(self):
        """CN4 must reference transitivity-of-subsumption failure code."""
        assert len(COMMON_NOTION_CN4.related_failure_codes) >= 1
        assert FailureCode.M_01_13.value in COMMON_NOTION_CN4.related_failure_codes

    @pytest.mark.parametrize("notion", COMMON_NOTIONS)
    def test_all_notions_have_failure_codes(self, notion: CommonNotion):
        """Every common notion must reference at least one failure code."""
        assert len(notion.related_failure_codes) >= 1


# ══════════════════════════════════════════════════════════════════════════════
# Test: Birth Guards
# ══════════════════════════════════════════════════════════════════════════════


class TestCommonNotionBirthGuards:
    """CommonNotion birth guards must reject invalid constructions."""

    def _valid_kwargs(self) -> dict:
        """Baseline valid kwargs for CommonNotion."""
        return {
            "notion_id": "CN-TEST",
            "name": "Test Notion",
            "name_ar": "فكرة اختبارية",
            "statement": "This is a test statement.",
            "formal_expression": "A=B",
            "order": 1,
            "domain": CommonNotionDomain.EQUALITY,
            "constitution_ref": "docs/00_MAQOOL_CONSTITUTION.md §9 CN1",
        }

    def test_rejects_empty_notion_id(self):
        """Empty notion_id must be rejected (M_01_04)."""
        kwargs = self._valid_kwargs()
        kwargs["notion_id"] = ""
        with pytest.raises(ValueError, match=FailureCode.M_01_04.value):
            CommonNotion(**kwargs)

    def test_rejects_empty_name(self):
        """Empty name must be rejected (M_01_04)."""
        kwargs = self._valid_kwargs()
        kwargs["name"] = ""
        with pytest.raises(ValueError, match=FailureCode.M_01_04.value):
            CommonNotion(**kwargs)

    def test_rejects_empty_name_ar(self):
        """Empty name_ar must be rejected (M_01_04)."""
        kwargs = self._valid_kwargs()
        kwargs["name_ar"] = ""
        with pytest.raises(ValueError, match=FailureCode.M_01_04.value):
            CommonNotion(**kwargs)

    def test_rejects_empty_statement(self):
        """Empty statement must be rejected (M_01_04)."""
        kwargs = self._valid_kwargs()
        kwargs["statement"] = ""
        with pytest.raises(ValueError, match=FailureCode.M_01_04.value):
            CommonNotion(**kwargs)

    def test_rejects_empty_formal_expression(self):
        """Empty formal_expression must be rejected (M_01_04)."""
        kwargs = self._valid_kwargs()
        kwargs["formal_expression"] = ""
        with pytest.raises(ValueError, match=FailureCode.M_01_04.value):
            CommonNotion(**kwargs)

    def test_rejects_invalid_domain(self):
        """Invalid domain must be rejected (M_01_04)."""
        kwargs = self._valid_kwargs()
        kwargs["domain"] = "not_a_domain"
        with pytest.raises(ValueError, match=FailureCode.M_01_04.value):
            CommonNotion(**kwargs)

    def test_rejects_invalid_order(self):
        """Order outside CN1..CN4 must be rejected (M_01_04)."""
        kwargs = self._valid_kwargs()
        kwargs["order"] = 5
        with pytest.raises(ValueError, match=FailureCode.M_01_04.value):
            CommonNotion(**kwargs)

    def test_rejects_empty_constitution_ref(self):
        """Empty constitution_ref must be rejected (M_01_03)."""
        kwargs = self._valid_kwargs()
        kwargs["constitution_ref"] = ""
        with pytest.raises(ValueError, match=FailureCode.M_01_03.value):
            CommonNotion(**kwargs)

    def test_rejects_empty_trace_ref(self):
        """Empty trace_ref must be rejected (M_01_14)."""
        kwargs = self._valid_kwargs()
        kwargs["trace_ref"] = ""
        with pytest.raises(ValueError, match=FailureCode.M_01_14.value):
            CommonNotion(**kwargs)

    def test_rejects_rank_promotion(self):
        """Rank promotion must be rejected (M_01_16)."""
        kwargs = self._valid_kwargs()
        kwargs["rank"] = "PROMOTED"
        with pytest.raises(ValueError, match=FailureCode.M_01_16.value):
            CommonNotion(**kwargs)


# ══════════════════════════════════════════════════════════════════════════════
# Test: Lookup Functions
# ══════════════════════════════════════════════════════════════════════════════


class TestLookupFunctions:
    """Registry lookup functions must work correctly."""

    def test_get_common_notion_valid_id(self):
        """get_common_notion must return the correct notion for valid IDs."""
        cn = get_common_notion("CN1")
        assert cn is COMMON_NOTION_CN1

    def test_get_common_notion_all_ids(self):
        """get_common_notion must work for all 4 IDs."""
        for cn_id in ["CN1", "CN2", "CN3", "CN4"]:
            cn = get_common_notion(cn_id)
            assert cn.notion_id == cn_id

    def test_get_common_notion_invalid_id(self):
        """get_common_notion must raise for unknown IDs."""
        with pytest.raises(ValueError, match=FailureCode.M_01_04.value):
            get_common_notion("CN99")

    def test_common_notions_by_domain_returns_correct_count(self):
        """common_notions_by_domain must return correct counts."""
        equality = common_notions_by_domain(CommonNotionDomain.EQUALITY)
        assert len(equality) == 2

    def test_total_common_notion_count(self):
        """total_common_notion_count must return 4."""
        assert total_common_notion_count() == 4
