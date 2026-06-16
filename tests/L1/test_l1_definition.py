"""
Test L1 Formal Definitions — test_l1_definition.py

Origin: docs/15_PROJECT_ROADMAP.md Phase 1 PR-10
Authority: docs/00_MAQOOL_CONSTITUTION.md §6 L1

Verifies:
1. All 13 L0 entities have formal definitions
2. Every definition is frozen with proper birth guards
3. Every definition carries trace_ref, rank=CANDIDATE, residuals
4. Identity preservation: Identity(L0) ⊆ Identity(L1)
5. Category coverage: all 4 categories have definitions
6. Boundary conditions are well-formed
7. Registry functions work correctly
"""
from __future__ import annotations

import pytest

from taaqqul_slot_geometry.constitution.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.L1.definition import (
    DEF_GRAPHEME,
    DEF_HARF_MAANI,
    DEF_JAMID,
    DEF_PHONEME,
    DEF_SIGNIFICATION,
    DEF_SIGNIFIED,
    DEF_SIGNIFIER,
    DEF_SYLLABLE,
    DEF_UNION,
    DEF_UTTERANCE,
    DEF_VOWEL,
    DEF_WAQF_WASL,
    DEF_WEIGHT,
    DEFINITION_BY_TERM,
    FORMAL_DEFINITIONS,
    BoundaryCondition,
    DefinitionCategory,
    FormalDefinition,
    definitions_by_category,
    get_definition,
    total_definition_count,
    verify_identity_preservation,
)


# ══════════════════════════════════════════════════════════════════════════════
# Test: Registry Completeness
# ══════════════════════════════════════════════════════════════════════════════


class TestRegistryCompleteness:
    """All 13 L0 entities must have corresponding L1 formal definitions."""

    EXPECTED_TERMS = [
        "PhonemeUnit",
        "Grapheme",
        "Vowel",
        "Syllable",
        "Utterance",
        "Signifier",
        "LinguisticSignified",
        "Union",
        "Signification",
        "JamidAnchor",
        "HarfMaani",
        "WeightUnit",
        "WaqfWaslProfile",
    ]

    def test_exactly_13_definitions(self):
        """Registry must contain exactly 13 formal definitions."""
        assert total_definition_count() == 13

    def test_all_expected_terms_present(self):
        """All expected L0 entity terms must have definitions."""
        actual_terms = {d.term for d in FORMAL_DEFINITIONS}
        expected = set(self.EXPECTED_TERMS)
        missing = expected - actual_terms
        assert missing == set(), f"Missing definitions for: {missing}"

    def test_no_duplicate_terms(self):
        """No two definitions may share the same term name."""
        terms = [d.term for d in FORMAL_DEFINITIONS]
        assert len(terms) == len(set(terms)), "Duplicate terms found"

    def test_definition_by_term_dict_consistent(self):
        """DEFINITION_BY_TERM must match FORMAL_DEFINITIONS tuple."""
        assert len(DEFINITION_BY_TERM) == len(FORMAL_DEFINITIONS)
        for d in FORMAL_DEFINITIONS:
            assert d.term in DEFINITION_BY_TERM
            assert DEFINITION_BY_TERM[d.term] is d


# ══════════════════════════════════════════════════════════════════════════════
# Test: Constitutional Compliance (Frozen, trace_ref, rank, residuals)
# ══════════════════════════════════════════════════════════════════════════════


class TestConstitutionalCompliance:
    """Every formal definition must comply with constitutional rules."""

    @pytest.mark.parametrize("definition", FORMAL_DEFINITIONS)
    def test_definition_is_frozen(self, definition: FormalDefinition):
        """Every FormalDefinition must be immutable (Rule 3)."""
        with pytest.raises(AttributeError):
            definition.term = "mutated"  # type: ignore[misc]

    @pytest.mark.parametrize("definition", FORMAL_DEFINITIONS)
    def test_has_trace_ref(self, definition: FormalDefinition):
        """Every definition must carry a non-empty trace_ref."""
        assert definition.trace_ref
        assert "docs/" in definition.trace_ref

    @pytest.mark.parametrize("definition", FORMAL_DEFINITIONS)
    def test_rank_is_candidate(self, definition: FormalDefinition):
        """Every definition must have rank='CANDIDATE'."""
        assert definition.rank == "CANDIDATE"

    @pytest.mark.parametrize("definition", FORMAL_DEFINITIONS)
    def test_has_residuals(self, definition: FormalDefinition):
        """Every definition must carry a residuals field (FrozenSet)."""
        assert isinstance(definition.residuals, frozenset)

    @pytest.mark.parametrize("definition", FORMAL_DEFINITIONS)
    def test_has_constitution_ref(self, definition: FormalDefinition):
        """Every definition must reference the constitution."""
        assert definition.constitution_ref
        assert "docs/" in definition.constitution_ref

    @pytest.mark.parametrize("definition", FORMAL_DEFINITIONS)
    def test_has_l0_source_ref(self, definition: FormalDefinition):
        """Every definition must reference its L0 source."""
        assert definition.l0_source_ref
        assert "L0/" in definition.l0_source_ref


# ══════════════════════════════════════════════════════════════════════════════
# Test: Definition Structure (Genus + Differentia)
# ══════════════════════════════════════════════════════════════════════════════


class TestDefinitionStructure:
    """Every definition must follow the حد = جنس + فصل pattern."""

    @pytest.mark.parametrize("definition", FORMAL_DEFINITIONS)
    def test_has_genus(self, definition: FormalDefinition):
        """Every definition must have a non-empty genus (الجنس)."""
        assert definition.genus

    @pytest.mark.parametrize("definition", FORMAL_DEFINITIONS)
    def test_has_differentia(self, definition: FormalDefinition):
        """Every definition must have a non-empty differentia (الفصل)."""
        assert definition.differentia

    @pytest.mark.parametrize("definition", FORMAL_DEFINITIONS)
    def test_has_boundary_conditions(self, definition: FormalDefinition):
        """Every definition must have at least one boundary condition."""
        assert len(definition.boundary_conditions) >= 1

    @pytest.mark.parametrize("definition", FORMAL_DEFINITIONS)
    def test_has_identity_fields(self, definition: FormalDefinition):
        """Every definition must declare identity fields for preservation."""
        assert len(definition.identity_fields) >= 1
        # Must always include the mandatory fields
        assert "trace_ref" in definition.identity_fields
        assert "rank" in definition.identity_fields
        assert "residuals" in definition.identity_fields


# ══════════════════════════════════════════════════════════════════════════════
# Test: Category Coverage
# ══════════════════════════════════════════════════════════════════════════════


class TestCategoryCoverage:
    """All 4 definition categories must be populated."""

    def test_phonological_category_has_definitions(self):
        """PHONOLOGICAL category must have definitions."""
        defs = definitions_by_category(DefinitionCategory.PHONOLOGICAL)
        assert len(defs) == 4  # phoneme, grapheme, vowel, syllable

    def test_compositional_category_has_definitions(self):
        """COMPOSITIONAL category must have definitions."""
        defs = definitions_by_category(DefinitionCategory.COMPOSITIONAL)
        assert len(defs) == 4  # utterance, signifier, signified, union

    def test_semantic_category_has_definitions(self):
        """SEMANTIC category must have definitions."""
        defs = definitions_by_category(DefinitionCategory.SEMANTIC)
        assert len(defs) == 3  # signification, jamid, harf_maani

    def test_structural_category_has_definitions(self):
        """STRUCTURAL category must have definitions."""
        defs = definitions_by_category(DefinitionCategory.STRUCTURAL)
        assert len(defs) == 2  # weight, waqf_wasl

    def test_categories_sum_to_13(self):
        """Sum of all category counts must equal 13."""
        total = sum(
            len(definitions_by_category(c))
            for c in DefinitionCategory
        )
        assert total == 13


# ══════════════════════════════════════════════════════════════════════════════
# Test: Boundary Conditions
# ══════════════════════════════════════════════════════════════════════════════


class TestBoundaryConditions:
    """Boundary conditions must be well-formed."""

    @pytest.mark.parametrize("definition", FORMAL_DEFINITIONS)
    def test_all_conditions_are_frozen(self, definition: FormalDefinition):
        """Every boundary condition must be immutable."""
        for bc in definition.boundary_conditions:
            with pytest.raises(AttributeError):
                bc.description = "mutated"  # type: ignore[misc]

    @pytest.mark.parametrize("definition", FORMAL_DEFINITIONS)
    def test_all_conditions_have_ids(self, definition: FormalDefinition):
        """Every boundary condition must have a unique ID."""
        ids = [bc.condition_id for bc in definition.boundary_conditions]
        assert len(ids) == len(set(ids)), "Duplicate condition IDs"

    @pytest.mark.parametrize("definition", FORMAL_DEFINITIONS)
    def test_at_least_one_necessary_condition(self, definition: FormalDefinition):
        """Every definition must have at least one necessary condition."""
        has_necessary = any(
            bc.is_necessary for bc in definition.boundary_conditions
        )
        assert has_necessary

    @pytest.mark.parametrize("definition", FORMAL_DEFINITIONS)
    def test_at_least_one_sufficient_condition(self, definition: FormalDefinition):
        """Every definition must have at least one sufficient condition."""
        has_sufficient = any(
            bc.is_sufficient for bc in definition.boundary_conditions
        )
        assert has_sufficient

    def test_boundary_condition_birth_guard_rejects_empty_id(self):
        """BoundaryCondition must reject empty condition_id."""
        with pytest.raises(ValueError, match=FailureCode.M_01_08.value):
            BoundaryCondition(
                condition_id="",
                description="test",
                is_necessary=True,
                is_sufficient=False,
            )

    def test_boundary_condition_birth_guard_rejects_empty_description(self):
        """BoundaryCondition must reject empty description."""
        with pytest.raises(ValueError, match=FailureCode.M_01_08.value):
            BoundaryCondition(
                condition_id="BC-TEST-01",
                description="",
                is_necessary=True,
                is_sufficient=False,
            )

    def test_boundary_condition_rejects_rank_promotion(self):
        """BoundaryCondition must reject rank != CANDIDATE."""
        with pytest.raises(ValueError, match=FailureCode.M_01_16.value):
            BoundaryCondition(
                condition_id="BC-TEST-01",
                description="test",
                is_necessary=True,
                is_sufficient=False,
                rank="PROMOTED",
            )


# ══════════════════════════════════════════════════════════════════════════════
# Test: Identity Preservation
# ══════════════════════════════════════════════════════════════════════════════


class TestIdentityPreservation:
    """Identity(L0) must be a subset of Identity(L1) for every definition."""

    def test_identity_preserved_when_subset(self):
        """verify_identity_preservation returns True for valid subsets."""
        l0_fields = frozenset({"consonant", "pattern", "trace_ref", "rank", "residuals"})
        result = verify_identity_preservation(DEF_PHONEME, l0_fields)
        assert result is True

    def test_identity_fails_when_not_subset(self):
        """verify_identity_preservation raises on identity loss."""
        l0_fields = frozenset({"consonant", "pattern", "trace_ref", "rank", "residuals", "extra_field"})
        with pytest.raises(ValueError, match=FailureCode.M_01_20.value):
            verify_identity_preservation(DEF_PHONEME, l0_fields)

    @pytest.mark.parametrize("definition", FORMAL_DEFINITIONS)
    def test_mandatory_identity_fields_preserved(self, definition: FormalDefinition):
        """Mandatory fields (trace_ref, rank, residuals) are always in identity_fields."""
        mandatory = frozenset({"trace_ref", "rank", "residuals"})
        result = verify_identity_preservation(definition, mandatory)
        assert result is True


# ══════════════════════════════════════════════════════════════════════════════
# Test: Birth Guards (FormalDefinition)
# ══════════════════════════════════════════════════════════════════════════════


class TestFormalDefinitionBirthGuards:
    """FormalDefinition birth guards must reject invalid constructions."""

    def _valid_kwargs(self) -> dict:
        """Baseline valid kwargs for FormalDefinition."""
        return {
            "term": "TestEntity",
            "genus": "test genus",
            "differentia": "test differentia",
            "category": DefinitionCategory.PHONOLOGICAL,
            "l0_source_ref": "L0/test.py",
            "constitution_ref": "docs/00_MAQOOL_CONSTITUTION.md §1",
            "boundary_conditions": (
                BoundaryCondition(
                    condition_id="BC-TEST-01",
                    description="test condition",
                    is_necessary=True,
                    is_sufficient=True,
                ),
            ),
            "identity_fields": frozenset({"trace_ref", "rank", "residuals"}),
        }

    def test_rejects_empty_term(self):
        """Empty term must be rejected (M_01_02)."""
        kwargs = self._valid_kwargs()
        kwargs["term"] = ""
        with pytest.raises(ValueError, match=FailureCode.M_01_02.value):
            FormalDefinition(**kwargs)

    def test_rejects_empty_genus(self):
        """Empty genus must be rejected (M_01_08)."""
        kwargs = self._valid_kwargs()
        kwargs["genus"] = ""
        with pytest.raises(ValueError, match=FailureCode.M_01_08.value):
            FormalDefinition(**kwargs)

    def test_rejects_empty_differentia(self):
        """Empty differentia must be rejected (M_01_08)."""
        kwargs = self._valid_kwargs()
        kwargs["differentia"] = ""
        with pytest.raises(ValueError, match=FailureCode.M_01_08.value):
            FormalDefinition(**kwargs)

    def test_rejects_empty_l0_source_ref(self):
        """Empty l0_source_ref must be rejected (M_01_02)."""
        kwargs = self._valid_kwargs()
        kwargs["l0_source_ref"] = ""
        with pytest.raises(ValueError, match=FailureCode.M_01_02.value):
            FormalDefinition(**kwargs)

    def test_rejects_empty_constitution_ref(self):
        """Empty constitution_ref must be rejected (M_01_03)."""
        kwargs = self._valid_kwargs()
        kwargs["constitution_ref"] = ""
        with pytest.raises(ValueError, match=FailureCode.M_01_03.value):
            FormalDefinition(**kwargs)

    def test_rejects_empty_identity_fields(self):
        """Empty identity_fields must be rejected (M_01_08)."""
        kwargs = self._valid_kwargs()
        kwargs["identity_fields"] = frozenset()
        with pytest.raises(ValueError, match=FailureCode.M_01_08.value):
            FormalDefinition(**kwargs)

    def test_rejects_rank_promotion(self):
        """Rank promotion must be rejected (M_01_16)."""
        kwargs = self._valid_kwargs()
        kwargs["rank"] = "PROMOTED"
        with pytest.raises(ValueError, match=FailureCode.M_01_16.value):
            FormalDefinition(**kwargs)

    def test_rejects_empty_trace_ref(self):
        """Empty trace_ref must be rejected (M_01_14)."""
        kwargs = self._valid_kwargs()
        kwargs["trace_ref"] = ""
        with pytest.raises(ValueError, match=FailureCode.M_01_14.value):
            FormalDefinition(**kwargs)

    def test_rejects_negative_closed_set_size(self):
        """Negative closed_set_size must be rejected."""
        kwargs = self._valid_kwargs()
        kwargs["closed_set_size"] = -1
        with pytest.raises(ValueError, match=FailureCode.M_01_08.value):
            FormalDefinition(**kwargs)


# ══════════════════════════════════════════════════════════════════════════════
# Test: Lookup Functions
# ══════════════════════════════════════════════════════════════════════════════


class TestLookupFunctions:
    """Registry lookup functions must work correctly."""

    def test_get_definition_valid_term(self):
        """get_definition must return the correct definition for valid terms."""
        d = get_definition("PhonemeUnit")
        assert d is DEF_PHONEME

    def test_get_definition_invalid_term(self):
        """get_definition must raise for unknown terms."""
        with pytest.raises(ValueError, match=FailureCode.M_01_02.value):
            get_definition("NonExistentEntity")

    def test_definitions_by_category_returns_correct_count(self):
        """definitions_by_category must return correct counts."""
        phonological = definitions_by_category(DefinitionCategory.PHONOLOGICAL)
        assert len(phonological) == 4

    def test_total_definition_count(self):
        """total_definition_count must return 13."""
        assert total_definition_count() == 13


# ══════════════════════════════════════════════════════════════════════════════
# Test: Closed Set Documentation
# ══════════════════════════════════════════════════════════════════════════════


class TestClosedSets:
    """Definitions for closed-set entities must document the set size."""

    CLOSED_SET_EXPECTATIONS = {
        "PhonemeUnit": 8,
        "Grapheme": 28,
        "Vowel": 7,
        "Syllable": 4,
        "Signification": 5,
        "JamidAnchor": 7,
        "HarfMaani": 20,
        "WeightUnit": 9,
        "WaqfWaslProfile": 4,
    }

    @pytest.mark.parametrize(
        "term,expected_size",
        list(CLOSED_SET_EXPECTATIONS.items()),
    )
    def test_closed_set_size_correct(self, term: str, expected_size: int):
        """Definitions for closed sets must document the correct size."""
        d = get_definition(term)
        assert d.closed_set_size == expected_size

    def test_non_closed_set_entities_have_zero_size(self):
        """Non-closed-set entities must have closed_set_size=0."""
        non_closed = {"Utterance", "Signifier", "LinguisticSignified", "Union"}
        for term in non_closed:
            d = get_definition(term)
            assert d.closed_set_size == 0, f"{term} should have closed_set_size=0"
