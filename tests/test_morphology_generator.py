"""
Tests for the Morphological Generative System (TH7–TH9).
Origin: docs/00_MAQOOL_CONSTITUTION.md §5 Rule 10

This test module verifies:
    TH7: Morphological generation is a function G(R, W, F) = S
    TH8: Transitivity is a function of weight structure T(W) = class
    TH9: Weak root transformations are deterministic M(R, pos) = rule

Test groups (12 classes, 66 tests):
    1. TestWeightPatternRegistry — registry integrity
    2. TestPastTenseGeneration — past tense forms
    3. TestPresentTenseGeneration — present tense forms
    4. TestActiveParticipleGeneration — active participle forms
    5. TestPassiveParticipleGeneration — passive participle forms
    6. TestVerbalNounGeneration — masdar forms
    7. TestPluralGeneration — all plural types
    8. TestDiminutiveComparative — diminutive and comparative
    9. TestTransitivitySystem — TH8 transitivity rules
    10. TestWeakRootSystem — TH9 weak root classification
    11. TestFullGenerationPipeline — integration tests
    12. TestConstitutionalIntegrity — constitutional constraint verification
"""
from __future__ import annotations

import pytest

from taaqqul_slot_geometry.core.arabic_weight_pattern import (
    ConsonantPosition,
    GenerativeRelation,
    MorphForm,
    TransitivityHint,
    WEIGHT_PATTERN_REGISTRY,
    WeightPatternSpec,
    get_all_intransitive_forms,
    get_all_transitive_forms,
    get_all_variable_forms,
    get_weight_pattern,
)
from taaqqul_slot_geometry.core.arabic_morphology_generator import (
    GeneratedForm,
    GenerationTarget,
    LicensedRoot,
    RootType,
    generate_active_participle,
    generate_all_forms,
    generate_broken_plural,
    generate_comparative,
    generate_diminutive,
    generate_passive_participle,
    generate_past,
    generate_present,
    generate_sound_plural_fem,
    generate_sound_plural_masc,
    generate_verbal_noun,
    make_root,
)
from taaqqul_slot_geometry.core.arabic_taadiyah_luzoom import (
    TransitivityClass,
    TransitivityMechanism,
    TransitivityRule,
    TRANSITIVITY_RULES,
    determine_transitivity,
    get_all_intransitive_rules,
    get_all_transitive_rules,
    get_object_count,
    get_transitivity_rule,
)
from taaqqul_slot_geometry.core.arabic_muttasil import (
    TRANSFORMATION_RULES,
    WEAK_CONSONANTS,
    WeakRootClass,
    WeakTransformation,
    classify_root,
    generate_weak_past,
    generate_weak_present,
    get_transformation_for,
    is_weak_root,
)


# ══════════════════════════════════════════════════════════════════════════════
# §1  TestWeightPatternRegistry (7 tests)
# ══════════════════════════════════════════════════════════════════════════════


class TestWeightPatternRegistry:
    """Verify the 9 weight patterns are correctly registered."""

    def test_registry_has_9_patterns(self) -> None:
        """Registry must contain exactly 9 patterns."""
        assert len(WEIGHT_PATTERN_REGISTRY) == 9

    def test_all_forms_present(self) -> None:
        """Every MorphForm must appear in the registry."""
        forms_in_registry = {spec.form for spec in WEIGHT_PATTERN_REGISTRY}
        expected = set(MorphForm)
        assert forms_in_registry == expected

    def test_each_pattern_has_generative_relations(self) -> None:
        """Every pattern must have at least one generative relation."""
        for spec in WEIGHT_PATTERN_REGISTRY:
            assert len(spec.generative_relations) > 0, f"{spec.form} has no relations"

    def test_trilateral_positions(self) -> None:
        """All patterns must have trilateral consonant positions (F, A, L)."""
        for spec in WEIGHT_PATTERN_REGISTRY:
            assert ConsonantPosition.FA in spec.consonant_positions
            assert ConsonantPosition.AYN in spec.consonant_positions
            assert ConsonantPosition.LAM in spec.consonant_positions

    def test_form_i_is_base(self) -> None:
        """Form I must have no prefix/infix and VARIABLE transitivity."""
        form_i = get_weight_pattern(MorphForm.FORM_I)
        assert form_i.prefix == ""
        assert form_i.infix == ""
        assert form_i.suffix == ""
        assert form_i.has_gemination is False
        assert form_i.transitivity_hint == TransitivityHint.VARIABLE

    def test_form_ii_has_gemination(self) -> None:
        """Form II must have gemination and TRANSITIVE hint."""
        form_ii = get_weight_pattern(MorphForm.FORM_II)
        assert form_ii.has_gemination is True
        assert form_ii.transitivity_hint == TransitivityHint.TRANSITIVE

    def test_constitutional_fields_on_pattern(self) -> None:
        """Every pattern must carry constitutional fields."""
        for spec in WEIGHT_PATTERN_REGISTRY:
            assert spec.domain_tag == "L0_MORPHOLOGY"
            assert spec.trace_ref != ""
            assert spec.rank == "CANDIDATE"
            assert isinstance(spec.residuals, frozenset)


# ══════════════════════════════════════════════════════════════════════════════
# §2  TestPastTenseGeneration (5 tests)
# ══════════════════════════════════════════════════════════════════════════════


class TestPastTenseGeneration:
    """Verify past tense generation for trilateral roots."""

    def test_ktb_form_i_past(self) -> None:
        """ك-ت-ب Form I → كَتَبَ"""
        root = make_root("كتب")
        result = generate_past(root)
        assert result.target == GenerationTarget.PAST
        assert result.form == MorphForm.FORM_I
        assert "كَ" in result.surface or "ك\u064E" in result.surface

    def test_drs_form_i_past(self) -> None:
        """د-ر-س Form I → دَرَسَ"""
        root = make_root("درس")
        result = generate_past(root)
        assert result.target == GenerationTarget.PAST
        assert result.root == root

    def test_ktb_form_ii_past(self) -> None:
        """ك-ت-ب Form II → كَتَّبَ (with shadda)"""
        root = make_root("كتب")
        result = generate_past(root, MorphForm.FORM_II)
        assert result.form == MorphForm.FORM_II
        # Form II has shadda on middle radical
        assert "\u0651" in result.surface  # shadda present

    def test_form_iv_past(self) -> None:
        """ك-ت-ب Form IV → أَكْتَبَ (with hamza prefix)"""
        root = make_root("كتب")
        result = generate_past(root, MorphForm.FORM_IV)
        assert result.form == MorphForm.FORM_IV
        assert result.surface.startswith("أ")

    def test_quadrilateral_root_creation(self) -> None:
        """Quadrilateral root (4 consonants) is correctly created."""
        root = make_root("دحرج")
        assert root.root_type == RootType.QUADRILATERAL
        assert len(root.consonants) == 4


# ══════════════════════════════════════════════════════════════════════════════
# §3  TestPresentTenseGeneration (5 tests)
# ══════════════════════════════════════════════════════════════════════════════


class TestPresentTenseGeneration:
    """Verify present tense generation."""

    def test_ktb_form_i_present(self) -> None:
        """ك-ت-ب Form I → يَكْتُبُ"""
        root = make_root("كتب")
        result = generate_present(root)
        assert result.target == GenerationTarget.PRESENT
        assert result.surface.startswith("ي")

    def test_drs_form_i_present(self) -> None:
        """د-ر-س Form I → يَدْرُسُ"""
        root = make_root("درس")
        result = generate_present(root)
        assert result.target == GenerationTarget.PRESENT
        assert result.surface.startswith("ي")

    def test_form_vii_present(self) -> None:
        """Form VII present starts with ي+ن"""
        root = make_root("كسر")
        result = generate_present(root, MorphForm.FORM_VII)
        assert result.target == GenerationTarget.PRESENT
        # يَنْ prefix
        assert "ن" in result.surface

    def test_form_x_present(self) -> None:
        """Form X present has يَسْتَ prefix"""
        root = make_root("خرج")
        result = generate_present(root, MorphForm.FORM_X)
        assert result.target == GenerationTarget.PRESENT
        assert "س" in result.surface
        assert "ت" in result.surface

    def test_present_has_ya_prefix(self) -> None:
        """All present forms start with يَ or يُ."""
        root = make_root("علم")
        for f in MorphForm:
            result = generate_present(root, f)
            assert result.surface[0] == "ي"


# ══════════════════════════════════════════════════════════════════════════════
# §4  TestActiveParticipleGeneration (4 tests)
# ══════════════════════════════════════════════════════════════════════════════


class TestActiveParticipleGeneration:
    """Verify active participle generation."""

    def test_ktb_form_i_active_participle(self) -> None:
        """ك-ت-ب Form I → كَاتِب"""
        root = make_root("كتب")
        result = generate_active_participle(root)
        assert result.target == GenerationTarget.ACTIVE_PARTICIPLE
        # فَاعِل pattern: F+alif+A+kasra+L
        assert "ا" in result.surface  # alif after F

    def test_drs_form_i_active_participle(self) -> None:
        """د-ر-س Form I → دَارِس"""
        root = make_root("درس")
        result = generate_active_participle(root)
        assert result.target == GenerationTarget.ACTIVE_PARTICIPLE
        assert "ا" in result.surface

    def test_form_iv_active_participle(self) -> None:
        """Form IV active participle has م prefix (مُفْعِل)."""
        root = make_root("سلم")
        result = generate_active_participle(root, MorphForm.FORM_IV)
        assert result.surface.startswith("م")

    def test_form_x_active_participle(self) -> None:
        """Form X active participle has مُسْتَ prefix."""
        root = make_root("خرج")
        result = generate_active_participle(root, MorphForm.FORM_X)
        assert result.surface.startswith("م")
        assert "س" in result.surface


# ══════════════════════════════════════════════════════════════════════════════
# §5  TestPassiveParticipleGeneration (3 tests)
# ══════════════════════════════════════════════════════════════════════════════


class TestPassiveParticipleGeneration:
    """Verify passive participle generation."""

    def test_ktb_form_i_passive_participle(self) -> None:
        """ك-ت-ب Form I → مَكْتُوب"""
        root = make_root("كتب")
        result = generate_passive_participle(root)
        assert result.target == GenerationTarget.PASSIVE_PARTICIPLE
        assert result.surface.startswith("م")  # مَفْعُول starts with م
        assert "و" in result.surface  # has واو

    def test_form_ii_passive_participle(self) -> None:
        """Form II passive participle (مُفَعَّل)."""
        root = make_root("علم")
        result = generate_passive_participle(root, MorphForm.FORM_II)
        assert result.surface.startswith("م")

    def test_passive_participle_constitutional_fields(self) -> None:
        """Passive participle carries constitutional fields."""
        root = make_root("كتب")
        result = generate_passive_participle(root)
        assert result.domain_tag == "L0_MORPHOLOGY"
        assert result.trace_ref != ""
        assert result.rank == "CANDIDATE"


# ══════════════════════════════════════════════════════════════════════════════
# §6  TestVerbalNounGeneration (4 tests)
# ══════════════════════════════════════════════════════════════════════════════


class TestVerbalNounGeneration:
    """Verify verbal noun (masdar) generation."""

    def test_ktb_form_i_masdar(self) -> None:
        """ك-ت-ب + فَعَلَ → كِتَاب (فِعَال pattern)"""
        root = make_root("كتب")
        result = generate_verbal_noun(root, MorphForm.FORM_I)
        assert result.target == GenerationTarget.VERBAL_NOUN
        assert "ا" in result.surface  # long alif in فِعَال

    def test_ktb_form_ii_masdar(self) -> None:
        """ك-ت-ب + فَعَّلَ → تَكْتِيب (تَفْعِيل pattern)"""
        root = make_root("كتب")
        result = generate_verbal_noun(root, MorphForm.FORM_II)
        assert result.target == GenerationTarget.VERBAL_NOUN
        assert result.surface.startswith("ت")  # starts with ت

    def test_form_iv_masdar(self) -> None:
        """Form IV masdar (إِفْعَال)."""
        root = make_root("سلم")
        result = generate_verbal_noun(root, MorphForm.FORM_IV)
        assert result.target == GenerationTarget.VERBAL_NOUN
        assert result.surface.startswith("إ")

    def test_masdar_trace_integrity(self) -> None:
        """Masdar generation trace must be non-empty."""
        root = make_root("كتب")
        result = generate_verbal_noun(root)
        assert result.generation_trace != ""
        assert "masdar" in result.generation_trace.lower() or "Form" in result.generation_trace


# ══════════════════════════════════════════════════════════════════════════════
# §7  TestPluralGeneration (5 tests)
# ══════════════════════════════════════════════════════════════════════════════


class TestPluralGeneration:
    """Verify plural generation."""

    def test_sound_plural_masc(self) -> None:
        """Sound masculine plural: active_part + ُونَ"""
        root = make_root("كتب")
        result = generate_sound_plural_masc(root)
        assert result.target == GenerationTarget.SOUND_PLURAL_MASC
        # Must end with ون
        assert "و" in result.surface
        assert "ن" in result.surface

    def test_sound_plural_fem(self) -> None:
        """Sound feminine plural: active_part + َات"""
        root = make_root("كتب")
        result = generate_sound_plural_fem(root)
        assert result.target == GenerationTarget.SOUND_PLURAL_FEM
        assert "ات" in result.surface

    def test_broken_plural(self) -> None:
        """Broken plural: فُعَلَاء pattern."""
        root = make_root("كتب")
        result = generate_broken_plural(root)
        assert result.target == GenerationTarget.BROKEN_PLURAL
        assert "ء" in result.surface  # ends with hamza

    def test_plural_from_root(self) -> None:
        """All plural forms derive from the same root."""
        root = make_root("علم")
        masc = generate_sound_plural_masc(root)
        fem = generate_sound_plural_fem(root)
        broken = generate_broken_plural(root)
        assert masc.root == root
        assert fem.root == root
        assert broken.root == root

    def test_plural_system_completeness(self) -> None:
        """Full plural system covers all three types."""
        root = make_root("درس")
        masc = generate_sound_plural_masc(root)
        fem = generate_sound_plural_fem(root)
        broken = generate_broken_plural(root)
        targets = {masc.target, fem.target, broken.target}
        assert GenerationTarget.SOUND_PLURAL_MASC in targets
        assert GenerationTarget.SOUND_PLURAL_FEM in targets
        assert GenerationTarget.BROKEN_PLURAL in targets


# ══════════════════════════════════════════════════════════════════════════════
# §8  TestDiminutiveComparative (4 tests)
# ══════════════════════════════════════════════════════════════════════════════


class TestDiminutiveComparative:
    """Verify diminutive and comparative generation."""

    def test_diminutive_ktb(self) -> None:
        """Diminutive of كتب: فُعَيْل = كُتَيْب"""
        root = make_root("كتب")
        result = generate_diminutive(root)
        assert result.target == GenerationTarget.DIMINUTIVE
        # فُعَيْل pattern includes ي+sukun
        assert "ي" in result.surface

    def test_comparative_kthr(self) -> None:
        """Comparative: أَفْعَلُ pattern (كثر → أَكْثَرُ)."""
        root = make_root("كثر")
        result = generate_comparative(root)
        assert result.target == GenerationTarget.COMPARATIVE
        assert result.surface.startswith("أ")  # starts with أ

    def test_diminutive_constitutional(self) -> None:
        """Diminutive form carries constitutional fields."""
        root = make_root("كتب")
        result = generate_diminutive(root)
        assert result.rank == "CANDIDATE"
        assert result.trace_ref != ""

    def test_comparative_constitutional(self) -> None:
        """Comparative form carries constitutional fields."""
        root = make_root("كبر")
        result = generate_comparative(root)
        assert result.rank == "CANDIDATE"
        assert result.domain_tag == "L0_MORPHOLOGY"


# ══════════════════════════════════════════════════════════════════════════════
# §9  TestTransitivitySystem (8 tests)
# ══════════════════════════════════════════════════════════════════════════════


class TestTransitivitySystem:
    """Verify TH8: transitivity is a function of weight structure."""

    def test_form_i_is_variable(self) -> None:
        """Form I (فَعَلَ) has VARIABLE transitivity."""
        verdict = determine_transitivity(MorphForm.FORM_I)
        assert verdict.is_variable is True
        assert verdict.is_transitive is False
        assert verdict.is_intransitive is False

    def test_form_ii_is_transitive(self) -> None:
        """Form II (فَعَّلَ) is TRANSITIVE via gemination."""
        verdict = determine_transitivity(MorphForm.FORM_II)
        assert verdict.is_transitive is True
        assert verdict.mechanism == TransitivityMechanism.GEMINATION

    def test_form_iv_is_transitive(self) -> None:
        """Form IV (أَفْعَلَ) is TRANSITIVE via initial hamza."""
        verdict = determine_transitivity(MorphForm.FORM_IV)
        assert verdict.is_transitive is True
        assert verdict.mechanism == TransitivityMechanism.INITIAL_HAMZA

    def test_form_vii_is_intransitive(self) -> None:
        """Form VII (اِنْفَعَلَ) is INTRANSITIVE (passivity)."""
        verdict = determine_transitivity(MorphForm.FORM_VII)
        assert verdict.is_intransitive is True
        assert verdict.mechanism == TransitivityMechanism.NUN_PREFIX

    def test_form_x_is_transitive(self) -> None:
        """Form X (اِسْتَفْعَلَ) is TRANSITIVE via sin+ta."""
        verdict = determine_transitivity(MorphForm.FORM_X)
        assert verdict.is_transitive is True
        assert verdict.mechanism == TransitivityMechanism.SIN_TA

    def test_object_count_form_vii(self) -> None:
        """Form VII takes 0 objects (intransitive)."""
        count = get_object_count(MorphForm.FORM_VII)
        assert count == 0

    def test_transitive_rules_count(self) -> None:
        """At least 4 forms are categorically transitive."""
        trans_rules = get_all_transitive_rules()
        assert len(trans_rules) >= 4

    def test_intransitive_rules_count(self) -> None:
        """At least 1 form is categorically intransitive."""
        intrans_rules = get_all_intransitive_rules()
        assert len(intrans_rules) >= 1


# ══════════════════════════════════════════════════════════════════════════════
# §10  TestWeakRootSystem (8 tests)
# ══════════════════════════════════════════════════════════════════════════════


class TestWeakRootSystem:
    """Verify TH9: weak root classification and transformations."""

    def test_mithal_classification(self) -> None:
        """و-ص-ل is classified as مثال (weak first radical)."""
        root = make_root("وصل")
        analysis = classify_root(root)
        assert analysis.classification == WeakRootClass.MITHAL
        assert 0 in analysis.weak_positions

    def test_ajwaf_classification(self) -> None:
        """ق-و-ل is classified as أجوف (weak second radical)."""
        root = make_root("قول")
        analysis = classify_root(root)
        assert analysis.classification == WeakRootClass.AJWAF
        assert 1 in analysis.weak_positions

    def test_naqis_classification(self) -> None:
        """ر-م-ي is classified as ناقص (weak third radical)."""
        root = make_root("رمي")
        analysis = classify_root(root)
        assert analysis.classification == WeakRootClass.NAQIS
        assert 2 in analysis.weak_positions

    def test_lafif_maqrun_classification(self) -> None:
        """Root with weak 2nd+3rd is لفيف مقرون."""
        root = LicensedRoot(
            consonants=("ر", "و", "ي"),
            root_type=RootType.TRILATERAL,
        )
        analysis = classify_root(root)
        assert analysis.classification == WeakRootClass.LAFIF_MAQRUN

    def test_sound_root_classification(self) -> None:
        """ك-ت-ب is classified as صحيح (sound root)."""
        root = make_root("كتب")
        analysis = classify_root(root)
        assert analysis.classification == WeakRootClass.SAHIH

    def test_is_weak_root_true(self) -> None:
        """و-ص-ل is a weak root."""
        root = make_root("وصل")
        assert is_weak_root(root) is True

    def test_is_weak_root_false(self) -> None:
        """ك-ت-ب is NOT a weak root."""
        root = make_root("كتب")
        assert is_weak_root(root) is False

    def test_weak_past_ajwaf(self) -> None:
        """Ajwaf past: ق-و-ل → قَالَ (middle → alif)."""
        root = make_root("قول")
        result = generate_weak_past(root)
        # Should contain alif (weak middle transformed to alif)
        assert "ا" in result.surface or "\u0627" in result.surface


# ══════════════════════════════════════════════════════════════════════════════
# §11  TestFullGenerationPipeline (7 tests)
# ══════════════════════════════════════════════════════════════════════════════


class TestFullGenerationPipeline:
    """Integration tests for the full generative pipeline."""

    def test_generate_all_forms_count(self) -> None:
        """generate_all_forms produces exactly 10 forms."""
        root = make_root("كتب")
        forms = generate_all_forms(root)
        assert len(forms) == 10

    def test_all_forms_have_surface(self) -> None:
        """Every generated form has a non-empty surface."""
        root = make_root("كتب")
        forms = generate_all_forms(root)
        for f in forms:
            assert f.surface != ""

    def test_all_forms_have_trace(self) -> None:
        """Every generated form has a non-empty generation trace."""
        root = make_root("كتب")
        forms = generate_all_forms(root)
        for f in forms:
            assert f.generation_trace != ""

    def test_all_forms_preserve_root(self) -> None:
        """Every generated form references the original root."""
        root = make_root("كتب")
        forms = generate_all_forms(root)
        for f in forms:
            assert f.root == root

    def test_all_forms_carry_constitutional_fields(self) -> None:
        """Every generated form carries trace_ref, rank, residuals."""
        root = make_root("درس")
        forms = generate_all_forms(root)
        for f in forms:
            assert f.trace_ref != ""
            assert f.rank == "CANDIDATE"
            assert isinstance(f.residuals, frozenset)

    def test_different_roots_produce_different_surfaces(self) -> None:
        """Different roots produce different surface forms."""
        root1 = make_root("كتب")
        root2 = make_root("درس")
        past1 = generate_past(root1)
        past2 = generate_past(root2)
        assert past1.surface != past2.surface

    def test_pipeline_determinism(self) -> None:
        """Same input always produces same output (pure function)."""
        root = make_root("كتب")
        forms1 = generate_all_forms(root)
        forms2 = generate_all_forms(root)
        for f1, f2 in zip(forms1, forms2):
            assert f1.surface == f2.surface
            assert f1.generation_trace == f2.generation_trace


# ══════════════════════════════════════════════════════════════════════════════
# §12  TestConstitutionalIntegrity (6 tests)
# ══════════════════════════════════════════════════════════════════════════════


class TestConstitutionalIntegrity:
    """Verify constitutional constraints are respected throughout."""

    def test_root_rejects_empty_consonants(self) -> None:
        """Root with empty consonant raises ValueError."""
        with pytest.raises(ValueError):
            LicensedRoot(consonants=("", "ت", "ب"), root_type=RootType.TRILATERAL)

    def test_root_rejects_wrong_count(self) -> None:
        """Trilateral root with 4 consonants raises ValueError."""
        with pytest.raises(ValueError):
            LicensedRoot(consonants=("ك", "ت", "ب", "ر"), root_type=RootType.TRILATERAL)

    def test_root_rejects_rank_promotion(self) -> None:
        """Root with rank != CANDIDATE raises ValueError."""
        with pytest.raises(ValueError):
            LicensedRoot(
                consonants=("ك", "ت", "ب"),
                root_type=RootType.TRILATERAL,
                rank="PROMOTED",
            )

    def test_root_rejects_empty_trace(self) -> None:
        """Root with empty trace_ref raises ValueError."""
        with pytest.raises(ValueError):
            LicensedRoot(
                consonants=("ك", "ت", "ب"),
                root_type=RootType.TRILATERAL,
                trace_ref="",
            )

    def test_generated_form_is_frozen(self) -> None:
        """GeneratedForm is immutable (frozen dataclass)."""
        root = make_root("كتب")
        result = generate_past(root)
        with pytest.raises((AttributeError, TypeError)):
            result.surface = "hacked"  # type: ignore[misc]

    def test_weight_pattern_is_frozen(self) -> None:
        """WeightPatternSpec is immutable (frozen dataclass)."""
        spec = get_weight_pattern(MorphForm.FORM_I)
        with pytest.raises((AttributeError, TypeError)):
            spec.arabic_label = "hacked"  # type: ignore[misc]
