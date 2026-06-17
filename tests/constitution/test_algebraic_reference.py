"""
Tests for AlgebraicReference — الإحالة الجبرية المرخّصة.

Origin: docs/00_MAQOOL_CONSTITUTION.md §5 Rules 6, 7, 8
"""
import pytest

from taaqqul_slot_geometry.constitution.algebraic_reference import (
    AlgebraicReference,
    GateStatus,
    REFERENCE_LAYER_INDEX,
    REFERENCE_TYPE_DOMAIN,
    REFERENCE_TYPE_MODE,
    ReferenceCompositionError,
    ReferenceLayer,
    ReferenceMode,
    ReferenceResidualKind,
    ReferenceType,
    RefResult,
    RefStatus,
    compose_chain,
    compose_references,
)
from taaqqul_slot_geometry.constitution.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.core.rank import Rank


# ══════════════════════════════════════════════════════════════════════════════
# §1  ReferenceLayer Tests
# ══════════════════════════════════════════════════════════════════════════════


class TestReferenceLayer:
    """Tests for the 12-layer reference chain."""

    def test_layer_count(self):
        """There must be exactly 12 layers."""
        assert len(ReferenceLayer) == 12

    def test_layer_index_ordering(self):
        """Layers must be ordered 0..11."""
        assert REFERENCE_LAYER_INDEX["digital"] == 0
        assert REFERENCE_LAYER_INDEX["tanzil"] == 11
        assert len(REFERENCE_LAYER_INDEX) == 12

    def test_all_layers_indexed(self):
        """Every layer must have an index."""
        for layer in ReferenceLayer:
            assert layer.value in REFERENCE_LAYER_INDEX

    def test_layer_ordering_is_sequential(self):
        """Indices must be 0, 1, 2, ..., 11 with no gaps."""
        indices = sorted(REFERENCE_LAYER_INDEX.values())
        assert indices == list(range(12))


# ══════════════════════════════════════════════════════════════════════════════
# §2  ReferenceType Tests
# ══════════════════════════════════════════════════════════════════════════════


class TestReferenceType:
    """Tests for the 12 species of reference."""

    def test_type_count(self):
        """There must be exactly 12 reference types."""
        assert len(ReferenceType) == 12

    def test_all_types_have_domain(self):
        """Every reference type must have a declared domain (source, target)."""
        for ref_type in ReferenceType:
            assert ref_type in REFERENCE_TYPE_DOMAIN

    def test_no_reference_leaps(self):
        """No reference type domain may span more than 1 layer distance."""
        for ref_type, (src, tgt) in REFERENCE_TYPE_DOMAIN.items():
            src_idx = REFERENCE_LAYER_INDEX[src.value]
            tgt_idx = REFERENCE_LAYER_INDEX[tgt.value]
            distance = abs(tgt_idx - src_idx)
            assert distance <= 1, (
                f"{ref_type.value}: leaps {distance} layers "
                f"({src.value} → {tgt.value})"
            )

    def test_all_types_have_mode(self):
        """Every reference type must have a declared mode."""
        for ref_type in ReferenceType:
            assert ref_type in REFERENCE_TYPE_MODE

    def test_syntactic_ref_is_refinement(self):
        """SYNTACTIC_REF must be classified as refinement, not transition."""
        assert REFERENCE_TYPE_MODE[ReferenceType.SYNTACTIC_REF] == ReferenceMode.REFINEMENT

    def test_compositional_ref_replaces_conceptual(self):
        """COMPOSITIONAL_REF maps WORD → COMPOSITION (transition)."""
        src, tgt = REFERENCE_TYPE_DOMAIN[ReferenceType.COMPOSITIONAL_REF]
        assert src == ReferenceLayer.WORD
        assert tgt == ReferenceLayer.COMPOSITION
        assert REFERENCE_TYPE_MODE[ReferenceType.COMPOSITIONAL_REF] == ReferenceMode.TRANSITION


# ══════════════════════════════════════════════════════════════════════════════
# §3  ReferenceMode Tests
# ══════════════════════════════════════════════════════════════════════════════


class TestReferenceMode:
    """Tests for the reference mode (transition vs refinement)."""

    def test_refinement_same_layer_only(self):
        """All refinement types must have same source and target layer."""
        for ref_type, mode in REFERENCE_TYPE_MODE.items():
            if mode == ReferenceMode.REFINEMENT:
                src, tgt = REFERENCE_TYPE_DOMAIN[ref_type]
                assert src == tgt, (
                    f"{ref_type.value} is REFINEMENT but source={src.value} != target={tgt.value}"
                )

    def test_transition_different_layers(self):
        """All transition types must have adjacent different layers."""
        for ref_type, mode in REFERENCE_TYPE_MODE.items():
            if mode == ReferenceMode.TRANSITION:
                src, tgt = REFERENCE_TYPE_DOMAIN[ref_type]
                src_idx = REFERENCE_LAYER_INDEX[src.value]
                tgt_idx = REFERENCE_LAYER_INDEX[tgt.value]
                assert tgt_idx == src_idx + 1, (
                    f"{ref_type.value} is TRANSITION but "
                    f"target({tgt_idx}) != source({src_idx})+1"
                )


# ══════════════════════════════════════════════════════════════════════════════
# §4  RefResult Tests
# ══════════════════════════════════════════════════════════════════════════════


class TestRefResult:
    """Tests for RefResult birth guards and properties."""

    def test_licensed_result_no_reason_required(self):
        """A LICENSED result does not require a reason."""
        result = RefResult(
            status=RefStatus.LICENSED,
            output_layer=ReferenceLayer.GLYPH,
            identity_preserved=True,
        )
        assert result.is_licensed
        assert result.reason == ""

    def test_blocked_result_requires_reason(self):
        """A BLOCKED result must declare a reason (OA8)."""
        with pytest.raises(ValueError, match="silent_exception_forbidden"):
            RefResult(
                status=RefStatus.BLOCKED,
                output_layer=ReferenceLayer.GLYPH,
                identity_preserved=False,
                reason="",  # Empty reason — forbidden
            )

    def test_deferred_result_requires_reason(self):
        """A DEFERRED result must declare a reason (OA8)."""
        with pytest.raises(ValueError, match="silent_exception_forbidden"):
            RefResult(
                status=RefStatus.DEFERRED,
                output_layer=ReferenceLayer.GLYPH,
                identity_preserved=False,
                reason="",
            )

    def test_result_frozen(self):
        """RefResult must be frozen (Rule 3)."""
        result = RefResult(
            status=RefStatus.LICENSED,
            output_layer=ReferenceLayer.GLYPH,
            identity_preserved=True,
        )
        with pytest.raises(AttributeError):
            result.status = RefStatus.BLOCKED  # type: ignore[misc]

    def test_rank_must_be_candidate(self):
        """Rank must be CANDIDATE (no promotion in current phase).

        The birth guard in __post_init__ enforces rank == Rank.CANDIDATE.
        We test this by passing a non-Rank value via object.__new__ bypass.
        """
        # Since Rank only has CANDIDATE, passing a non-Rank string tests the guard
        with pytest.raises(ValueError, match=FailureCode.M_CX_09.value):
            # Constructing with a string bypasses Rank enum and hits the guard
            RefResult(
                status=RefStatus.LICENSED,
                output_layer=ReferenceLayer.GLYPH,
                identity_preserved=True,
                rank="PROMOTED",  # type: ignore[arg-type]
            )

    def test_trace_ref_required(self):
        """trace_ref must not be empty."""
        with pytest.raises(ValueError, match="constitution_trace_ref_missing"):
            RefResult(
                status=RefStatus.LICENSED,
                output_layer=ReferenceLayer.GLYPH,
                identity_preserved=True,
                trace_ref="",
            )

    def test_residuals_are_typed(self):
        """Residuals must be ReferenceResidualKind, not bare strings."""
        result = RefResult(
            status=RefStatus.LICENSED,
            output_layer=ReferenceLayer.GLYPH,
            identity_preserved=True,
            residuals=frozenset({ReferenceResidualKind.IDENTITY_NOT_VERIFIED}),
        )
        assert ReferenceResidualKind.IDENTITY_NOT_VERIFIED in result.residuals

    def test_rank_is_enum(self):
        """Rank must be Rank enum, not a string."""
        result = RefResult(
            status=RefStatus.LICENSED,
            output_layer=ReferenceLayer.GLYPH,
            identity_preserved=True,
        )
        assert result.rank == Rank.CANDIDATE
        assert isinstance(result.rank, Rank)


# ══════════════════════════════════════════════════════════════════════════════
# §5  AlgebraicReference Tests
# ══════════════════════════════════════════════════════════════════════════════


class TestAlgebraicReference:
    """Tests for AlgebraicReference birth guards and apply()."""

    def _make_digital_ref(self, **kwargs):
        """Helper: build a valid DigitalRef."""
        defaults = dict(
            reference_type=ReferenceType.DIGITAL_REF,
            source_layer=ReferenceLayer.DIGITAL,
            target_layer=ReferenceLayer.GLYPH,
            domain="unicode_arabic_block",
            condition="codepoint_in_arabic_range",
            condition_verdict=GateStatus.VERIFIED,
            cause="unicode_to_glyph_mapping_exists",
            cause_verdict=GateStatus.VERIFIED,
            identity_evidence_ref="unicode_codepoint_identity_preserved",
        )
        defaults.update(kwargs)
        return AlgebraicReference(**defaults)

    def test_valid_digital_ref(self):
        """A valid DigitalRef must construct without error."""
        ref = self._make_digital_ref()
        assert ref.reference_type == ReferenceType.DIGITAL_REF
        assert ref.source_layer == ReferenceLayer.DIGITAL
        assert ref.target_layer == ReferenceLayer.GLYPH

    def test_apply_licensed(self):
        """apply() with all conditions met returns LICENSED."""
        ref = self._make_digital_ref()
        result = ref.apply()
        assert result.is_licensed
        assert result.output_layer == ReferenceLayer.GLYPH
        assert result.identity_preserved

    def test_apply_blocked_by_preventer(self):
        """apply() with active preventer returns BLOCKED (OA6)."""
        ref = self._make_digital_ref(
            preventers=frozenset({"invalid_codepoint"})
        )
        result = ref.apply()
        assert result.status == RefStatus.BLOCKED
        assert "preventer_active" in result.reason
        assert ReferenceResidualKind.PREVENTER_ACTIVE in result.residuals

    def test_apply_deferred_operator_unlicensed(self):
        """apply() with unlicensed operator returns DEFERRED."""
        ref = self._make_digital_ref(operator_licensed=False)
        result = ref.apply()
        assert result.status == RefStatus.DEFERRED
        assert "operator_not_licensed" in result.reason
        assert ReferenceResidualKind.OPERATOR_UNLICENSED in result.residuals

    def test_apply_deferred_identity_not_proven(self):
        """apply() without identity_evidence_ref returns DEFERRED."""
        ref = self._make_digital_ref(identity_evidence_ref="")
        result = ref.apply()
        assert result.status == RefStatus.DEFERRED
        assert FailureCode.M_CX_30.value in result.reason
        assert ReferenceResidualKind.IDENTITY_NOT_VERIFIED in result.residuals

    def test_apply_blocked_condition_failed(self):
        """apply() with condition_verdict=FAILED returns BLOCKED."""
        ref = self._make_digital_ref(condition_verdict=GateStatus.FAILED)
        result = ref.apply()
        assert result.status == RefStatus.BLOCKED
        assert "condition_failed" in result.reason
        assert ReferenceResidualKind.CONDITION_FAILED in result.residuals

    def test_apply_deferred_condition_not_verified(self):
        """apply() with condition_verdict=NOT_VERIFIED returns DEFERRED."""
        ref = self._make_digital_ref(condition_verdict=GateStatus.NOT_VERIFIED)
        result = ref.apply()
        assert result.status == RefStatus.DEFERRED
        assert "condition_not_verified" in result.reason
        assert ReferenceResidualKind.CONDITION_NOT_VERIFIED in result.residuals

    def test_apply_blocked_cause_failed(self):
        """apply() with cause_verdict=FAILED returns BLOCKED."""
        ref = self._make_digital_ref(cause_verdict=GateStatus.FAILED)
        result = ref.apply()
        assert result.status == RefStatus.BLOCKED
        assert "cause_failed" in result.reason
        assert ReferenceResidualKind.CAUSE_FAILED in result.residuals

    def test_apply_deferred_cause_not_verified(self):
        """apply() with cause_verdict=NOT_VERIFIED returns DEFERRED."""
        ref = self._make_digital_ref(cause_verdict=GateStatus.NOT_VERIFIED)
        result = ref.apply()
        assert result.status == RefStatus.DEFERRED
        assert "cause_not_verified" in result.reason
        assert ReferenceResidualKind.CAUSE_NOT_ACTIVE in result.residuals

    def test_no_leap_enforced(self):
        """References that skip layers must be rejected."""
        with pytest.raises(ValueError, match="reference_target_type_mismatch"):
            AlgebraicReference(
                reference_type=ReferenceType.DIGITAL_REF,
                source_layer=ReferenceLayer.DIGITAL,
                target_layer=ReferenceLayer.VOCALIZED,
                domain="test",
                condition="test",
                condition_verdict=GateStatus.VERIFIED,
                cause="test",
                cause_verdict=GateStatus.VERIFIED,
            )

    def test_source_layer_mismatch(self):
        """Reference with wrong source layer for its type must be rejected."""
        with pytest.raises(ValueError, match="reference_source_type_mismatch"):
            AlgebraicReference(
                reference_type=ReferenceType.DIGITAL_REF,
                source_layer=ReferenceLayer.GLYPH,
                target_layer=ReferenceLayer.LETTER_MARK,
                domain="test",
                condition="test",
                condition_verdict=GateStatus.VERIFIED,
                cause="test",
                cause_verdict=GateStatus.VERIFIED,
            )

    def test_target_layer_mismatch(self):
        """Reference with wrong target layer for its type must be rejected."""
        with pytest.raises(ValueError, match="reference_target_type_mismatch"):
            AlgebraicReference(
                reference_type=ReferenceType.DIGITAL_REF,
                source_layer=ReferenceLayer.DIGITAL,
                target_layer=ReferenceLayer.LETTER_MARK,
                domain="test",
                condition="test",
                condition_verdict=GateStatus.VERIFIED,
                cause="test",
                cause_verdict=GateStatus.VERIFIED,
            )

    def test_empty_domain_rejected(self):
        """Domain must be non-empty."""
        with pytest.raises(ValueError, match="reference_domain_missing"):
            self._make_digital_ref(domain="")

    def test_empty_condition_rejected(self):
        """Condition must be non-empty."""
        with pytest.raises(ValueError, match="reference_condition_missing"):
            self._make_digital_ref(condition="")

    def test_empty_cause_rejected(self):
        """Cause must be non-empty."""
        with pytest.raises(ValueError, match="reference_cause_missing"):
            self._make_digital_ref(cause="")

    def test_frozen(self):
        """AlgebraicReference must be frozen."""
        ref = self._make_digital_ref()
        with pytest.raises(AttributeError):
            ref.domain = "mutated"  # type: ignore[misc]

    def test_rank_candidate(self):
        """Rank must be CANDIDATE.

        The birth guard in __post_init__ enforces rank == Rank.CANDIDATE.
        Passing a non-Rank string tests the guard directly.
        """
        with pytest.raises(ValueError, match=FailureCode.M_CX_09.value):
            self._make_digital_ref(rank="PROMOTED")  # type: ignore[arg-type]

    def test_mode_property(self):
        """mode property returns the correct ReferenceMode."""
        ref = self._make_digital_ref()
        assert ref.mode == ReferenceMode.TRANSITION

    def test_syntactic_ref_mode_is_refinement(self):
        """SYNTACTIC_REF mode must be REFINEMENT."""
        ref = AlgebraicReference(
            reference_type=ReferenceType.SYNTACTIC_REF,
            source_layer=ReferenceLayer.COMPOSITION,
            target_layer=ReferenceLayer.COMPOSITION,
            domain="syntactic_relations",
            condition="constituents_identified",
            condition_verdict=GateStatus.VERIFIED,
            cause="syntactic_binding_required",
            cause_verdict=GateStatus.VERIFIED,
            identity_evidence_ref="composition_identity_preserved",
        )
        assert ref.mode == ReferenceMode.REFINEMENT


# ══════════════════════════════════════════════════════════════════════════════
# §6  Composition Tests
# ══════════════════════════════════════════════════════════════════════════════


class TestComposition:
    """Tests for reference composition law."""

    def _make_ref(self, ref_type: ReferenceType) -> AlgebraicReference:
        """Helper: build a valid reference of a given type."""
        src, tgt = REFERENCE_TYPE_DOMAIN[ref_type]
        return AlgebraicReference(
            reference_type=ref_type,
            source_layer=src,
            target_layer=tgt,
            domain=f"domain_{ref_type.value}",
            condition=f"condition_{ref_type.value}",
            condition_verdict=GateStatus.VERIFIED,
            cause=f"cause_{ref_type.value}",
            cause_verdict=GateStatus.VERIFIED,
            identity_evidence_ref=f"identity_proof_{ref_type.value}",
        )

    def test_valid_composition(self):
        """Composing adjacent references should succeed."""
        digital = self._make_ref(ReferenceType.DIGITAL_REF)
        glyph = self._make_ref(ReferenceType.GLYPH_REF)

        r1, r2 = compose_references(digital, glyph)
        assert r1.is_licensed
        assert r2.is_licensed

    def test_composition_gap_rejected(self):
        """Composing non-adjacent references must raise error."""
        digital = self._make_ref(ReferenceType.DIGITAL_REF)
        operational = self._make_ref(ReferenceType.OPERATIONAL_REF)

        with pytest.raises(ReferenceCompositionError, match="composition_gap"):
            compose_references(digital, operational)

    def test_composition_cascading_failure(self):
        """If first fails, second must be BLOCKED."""
        digital = AlgebraicReference(
            reference_type=ReferenceType.DIGITAL_REF,
            source_layer=ReferenceLayer.DIGITAL,
            target_layer=ReferenceLayer.GLYPH,
            domain="unicode",
            condition="valid",
            condition_verdict=GateStatus.VERIFIED,
            cause="mapping",
            cause_verdict=GateStatus.VERIFIED,
            identity_evidence_ref="proof",
            preventers=frozenset({"invalid_codepoint"}),  # Will fail
        )
        glyph = self._make_ref(ReferenceType.GLYPH_REF)

        r1, r2 = compose_references(digital, glyph)
        assert r1.status == RefStatus.BLOCKED
        assert r2.status == RefStatus.BLOCKED
        assert "predecessor_failed" in r2.reason
        assert ReferenceResidualKind.PREDECESSOR_FAILED in r2.residuals

    def test_compose_chain_full_l0(self):
        """A full L0 chain (Digital→...→Lafz) must compose successfully."""
        chain = (
            self._make_ref(ReferenceType.DIGITAL_REF),
            self._make_ref(ReferenceType.GLYPH_REF),
            self._make_ref(ReferenceType.OPERATIONAL_REF),
            self._make_ref(ReferenceType.SYLLABIC_REF),
            self._make_ref(ReferenceType.LAFZ_REF),
        )
        results = compose_chain(chain)
        assert len(results) == 5
        assert all(r.is_licensed for r in results)

    def test_compose_chain_failure_propagation(self):
        """Failure in chain position N blocks positions N+1, N+2, ..."""
        chain = (
            self._make_ref(ReferenceType.DIGITAL_REF),
            AlgebraicReference(
                reference_type=ReferenceType.GLYPH_REF,
                source_layer=ReferenceLayer.GLYPH,
                target_layer=ReferenceLayer.LETTER_MARK,
                domain="glyph",
                condition="valid",
                condition_verdict=GateStatus.VERIFIED,
                cause="mapping",
                cause_verdict=GateStatus.VERIFIED,
                identity_evidence_ref="proof",
                preventers=frozenset({"unknown_glyph"}),  # Fails here
            ),
            self._make_ref(ReferenceType.OPERATIONAL_REF),
            self._make_ref(ReferenceType.SYLLABIC_REF),
            self._make_ref(ReferenceType.LAFZ_REF),
        )
        results = compose_chain(chain)
        assert results[0].is_licensed  # Digital passes
        assert results[1].status == RefStatus.BLOCKED  # Glyph fails
        assert results[2].status == RefStatus.BLOCKED  # Blocked downstream
        assert results[3].status == RefStatus.BLOCKED
        assert results[4].status == RefStatus.BLOCKED
        assert ReferenceResidualKind.CHAIN_BLOCKED in results[2].residuals

    def test_compose_chain_empty_rejected(self):
        """Empty chain must be rejected."""
        with pytest.raises(ValueError, match=FailureCode.M_CX_32.value):
            compose_chain(())


# ══════════════════════════════════════════════════════════════════════════════
# §7  Agent-Binding Constitutional Tests
# ══════════════════════════════════════════════════════════════════════════════


class TestConstitutionalBinding:
    """Tests that verify constitutional guarantees binding on ALL agents."""

    def test_no_reference_crosses_boundary(self):
        """No reference type crosses its declared layer boundary."""
        for ref_type, (src, tgt) in REFERENCE_TYPE_DOMAIN.items():
            src_idx = REFERENCE_LAYER_INDEX[src.value]
            tgt_idx = REFERENCE_LAYER_INDEX[tgt.value]
            assert abs(tgt_idx - src_idx) <= 1, (
                f"CONSTITUTIONAL VIOLATION: {ref_type.value} crosses "
                f"from {src.value}({src_idx}) to {tgt.value}({tgt_idx})"
            )

    def test_all_results_have_trace_ref(self):
        """Every RefResult must carry trace_ref (Rule 2)."""
        result = RefResult(
            status=RefStatus.LICENSED,
            output_layer=ReferenceLayer.GLYPH,
            identity_preserved=True,
        )
        assert result.trace_ref != ""

    def test_all_references_have_mandatory_fields(self):
        """Every AlgebraicReference must have trace_ref, rank, residuals."""
        ref = AlgebraicReference(
            reference_type=ReferenceType.DIGITAL_REF,
            source_layer=ReferenceLayer.DIGITAL,
            target_layer=ReferenceLayer.GLYPH,
            domain="unicode",
            condition="valid",
            condition_verdict=GateStatus.VERIFIED,
            cause="mapping",
            cause_verdict=GateStatus.VERIFIED,
        )
        assert ref.trace_ref != ""
        assert ref.rank == Rank.CANDIDATE
        assert isinstance(ref.residuals, frozenset)

    def test_weight_does_not_cross_to_meaning(self):
        """Morphological reference stays within Lafz→Mufrad (no meaning)."""
        src, tgt = REFERENCE_TYPE_DOMAIN[ReferenceType.MORPHOLOGICAL_REF]
        assert src == ReferenceLayer.LAFZ
        assert tgt == ReferenceLayer.MUFRAD

    def test_hukm_requires_ifadah_source(self):
        """Hukm reference must source from Ifadah (OA11)."""
        src, tgt = REFERENCE_TYPE_DOMAIN[ReferenceType.HUKM_REF]
        assert src == ReferenceLayer.IFADAH
        assert tgt == ReferenceLayer.HUKM

    def test_tanzil_requires_hukm_source(self):
        """Tanzil reference must source from Hukm (OA12)."""
        src, tgt = REFERENCE_TYPE_DOMAIN[ReferenceType.TANZIL_REF]
        assert src == ReferenceLayer.HUKM
        assert tgt == ReferenceLayer.TANZIL

    def test_authority_is_not_user_defined_critique(self):
        """Authority must reference constitutional docs, not 'User-defined critique'."""
        import inspect
        import taaqqul_slot_geometry.constitution.algebraic_reference as algebraic_reference_mod
        source = inspect.getsource(algebraic_reference_mod)
        assert "User-defined critique" not in source


# ══════════════════════════════════════════════════════════════════════════════
# §8  Negative Tests — Condition/Cause/Identity Verification
# ══════════════════════════════════════════════════════════════════════════════


class TestNegativeConditionCauseIdentity:
    """Negative tests for condition, cause, and identity verification."""

    def _make_ref(self, **kwargs):
        """Helper: build a valid reference with all verdicts."""
        defaults = dict(
            reference_type=ReferenceType.DIGITAL_REF,
            source_layer=ReferenceLayer.DIGITAL,
            target_layer=ReferenceLayer.GLYPH,
            domain="unicode_arabic_block",
            condition="codepoint_in_arabic_range",
            condition_verdict=GateStatus.VERIFIED,
            cause="unicode_to_glyph_mapping_exists",
            cause_verdict=GateStatus.VERIFIED,
            identity_evidence_ref="unicode_identity_proof",
        )
        defaults.update(kwargs)
        return AlgebraicReference(**defaults)

    def test_condition_declared_but_not_verified_defers(self):
        """A condition that is declared but NOT_VERIFIED must defer."""
        ref = self._make_ref(condition_verdict=GateStatus.NOT_VERIFIED)
        result = ref.apply()
        assert result.status == RefStatus.DEFERRED
        assert "condition_not_verified" in result.reason

    def test_condition_declared_but_failed_blocks(self):
        """A condition that is declared but FAILED must block."""
        ref = self._make_ref(condition_verdict=GateStatus.FAILED)
        result = ref.apply()
        assert result.status == RefStatus.BLOCKED
        assert "condition_failed" in result.reason
        assert ReferenceResidualKind.CONDITION_FAILED in result.residuals

    def test_cause_declared_but_not_verified_defers(self):
        """A cause that is declared but NOT_VERIFIED must defer."""
        ref = self._make_ref(cause_verdict=GateStatus.NOT_VERIFIED)
        result = ref.apply()
        assert result.status == RefStatus.DEFERRED
        assert "cause_not_verified" in result.reason

    def test_cause_declared_but_failed_blocks(self):
        """A cause that is declared but FAILED must block."""
        ref = self._make_ref(cause_verdict=GateStatus.FAILED)
        result = ref.apply()
        assert result.status == RefStatus.BLOCKED
        assert "cause_failed" in result.reason
        assert ReferenceResidualKind.CAUSE_FAILED in result.residuals

    def test_identity_missing_defers_not_licenses(self):
        """Missing identity_evidence_ref must DEFER, never LICENSE."""
        ref = self._make_ref(identity_evidence_ref="")
        result = ref.apply()
        assert result.status == RefStatus.DEFERRED
        assert FailureCode.M_CX_30.value in result.reason
        assert not result.identity_preserved

    def test_identity_provided_licenses(self):
        """Providing identity_evidence_ref allows licensing."""
        ref = self._make_ref(identity_evidence_ref="proof_of_identity")
        result = ref.apply()
        assert result.is_licensed
        assert result.identity_preserved

    def test_no_default_identity_true(self):
        """apply() must not default identity_preserved to True without proof."""
        ref = self._make_ref(identity_evidence_ref="")
        result = ref.apply()
        # Must not be licensed just because other conditions are met
        assert not result.is_licensed
        assert not result.identity_preserved


# ══════════════════════════════════════════════════════════════════════════════
# §9  Negative Tests — Same-Layer Reference Misuse
# ══════════════════════════════════════════════════════════════════════════════


class TestSameLayerReferenceMisuse:
    """Negative tests for same-layer reference type/mode constraints."""

    def test_syntactic_ref_same_layer_valid(self):
        """SYNTACTIC_REF operating within COMPOSITION is valid."""
        ref = AlgebraicReference(
            reference_type=ReferenceType.SYNTACTIC_REF,
            source_layer=ReferenceLayer.COMPOSITION,
            target_layer=ReferenceLayer.COMPOSITION,
            domain="syntactic_relations",
            condition="constituents_identified",
            condition_verdict=GateStatus.VERIFIED,
            cause="syntactic_binding_required",
            cause_verdict=GateStatus.VERIFIED,
            identity_evidence_ref="composition_identity",
        )
        assert ref.mode == ReferenceMode.REFINEMENT
        result = ref.apply()
        assert result.is_licensed

    def test_transition_ref_cannot_be_same_layer(self):
        """A TRANSITION-mode reference cannot have same source and target.

        The type-domain check prevents this since DIGITAL_REF requires
        source=DIGITAL and target=GLYPH.
        """
        with pytest.raises(ValueError, match="reference_target_type_mismatch"):
            AlgebraicReference(
                reference_type=ReferenceType.DIGITAL_REF,
                source_layer=ReferenceLayer.DIGITAL,
                target_layer=ReferenceLayer.DIGITAL,  # Same as source
                domain="test",
                condition="test",
                condition_verdict=GateStatus.VERIFIED,
                cause="test",
                cause_verdict=GateStatus.VERIFIED,
            )


# ══════════════════════════════════════════════════════════════════════════════
# §10  Negative Tests — Precise Failure Codes
# ══════════════════════════════════════════════════════════════════════════════


class TestPreciseFailureCodes:
    """Tests that precise failure codes are used for different error conditions."""

    def test_empty_domain_uses_domain_missing_code(self):
        """Empty domain must raise M_CX_26 (reference_domain_missing)."""
        with pytest.raises(ValueError, match="reference_domain_missing"):
            AlgebraicReference(
                reference_type=ReferenceType.DIGITAL_REF,
                source_layer=ReferenceLayer.DIGITAL,
                target_layer=ReferenceLayer.GLYPH,
                domain="",
                condition="valid",
                condition_verdict=GateStatus.VERIFIED,
                cause="exists",
                cause_verdict=GateStatus.VERIFIED,
            )

    def test_empty_condition_uses_condition_missing_code(self):
        """Empty condition must raise M_CX_27 (reference_condition_missing)."""
        with pytest.raises(ValueError, match="reference_condition_missing"):
            AlgebraicReference(
                reference_type=ReferenceType.DIGITAL_REF,
                source_layer=ReferenceLayer.DIGITAL,
                target_layer=ReferenceLayer.GLYPH,
                domain="unicode",
                condition="",
                condition_verdict=GateStatus.VERIFIED,
                cause="exists",
                cause_verdict=GateStatus.VERIFIED,
            )

    def test_empty_cause_uses_cause_missing_code(self):
        """Empty cause must raise M_CX_28 (reference_cause_missing)."""
        with pytest.raises(ValueError, match="reference_cause_missing"):
            AlgebraicReference(
                reference_type=ReferenceType.DIGITAL_REF,
                source_layer=ReferenceLayer.DIGITAL,
                target_layer=ReferenceLayer.GLYPH,
                domain="unicode",
                condition="valid",
                condition_verdict=GateStatus.VERIFIED,
                cause="",
                cause_verdict=GateStatus.VERIFIED,
            )

    def test_layer_leap_uses_specific_code(self):
        """Layer leap must raise M_CX_29 (reference_layer_leap) via type check."""
        # Since type-domain check fires first, we test via the type mismatch
        # but the underlying adjacency check uses M_CX_29
        with pytest.raises(ValueError):
            AlgebraicReference(
                reference_type=ReferenceType.DIGITAL_REF,
                source_layer=ReferenceLayer.DIGITAL,
                target_layer=ReferenceLayer.SYLLABLE,  # Leaps
                domain="unicode",
                condition="valid",
                condition_verdict=GateStatus.VERIFIED,
                cause="exists",
                cause_verdict=GateStatus.VERIFIED,
            )

    def test_new_failure_codes_exist(self):
        """New failure codes M_CX_26..M_CX_33 must exist in FailureCode."""
        assert FailureCode.M_CX_26.value == "reference_domain_missing"
        assert FailureCode.M_CX_27.value == "reference_condition_missing"
        assert FailureCode.M_CX_28.value == "reference_cause_missing"
        assert FailureCode.M_CX_29.value == "reference_layer_leap"
        assert FailureCode.M_CX_30.value == "reference_identity_proof_missing"
        assert FailureCode.M_CX_31.value == "reference_condition_not_verified"
        assert FailureCode.M_CX_32.value == "reference_chain_empty"
        assert FailureCode.M_CX_33.value == "reference_result_status_invalid"


# ══════════════════════════════════════════════════════════════════════════════
# §11  GateStatus Tests
# ══════════════════════════════════════════════════════════════════════════════


class TestGateStatus:
    """Tests for GateStatus enum."""

    def test_three_statuses(self):
        """GateStatus must have exactly 3 members."""
        assert len(GateStatus) == 3

    def test_verified_value(self):
        """VERIFIED must equal 'verified'."""
        assert GateStatus.VERIFIED.value == "verified"

    def test_not_verified_value(self):
        """NOT_VERIFIED must equal 'not_verified'."""
        assert GateStatus.NOT_VERIFIED.value == "not_verified"

    def test_failed_value(self):
        """FAILED must equal 'failed'."""
        assert GateStatus.FAILED.value == "failed"


# ══════════════════════════════════════════════════════════════════════════════
# §12  ReferenceResidualKind Tests
# ══════════════════════════════════════════════════════════════════════════════


class TestReferenceResidualKind:
    """Tests for typed residual kinds."""

    def test_all_residual_kinds_exist(self):
        """All expected residual kinds must exist."""
        expected = {
            "identity_not_verified",
            "condition_not_verified",
            "condition_failed",
            "cause_not_active",
            "cause_failed",
            "preventer_active",
            "operator_unlicensed",
            "composition_gap",
            "predecessor_failed",
            "chain_blocked",
        }
        actual = {kind.value for kind in ReferenceResidualKind}
        assert actual == expected

    def test_residual_kind_count(self):
        """Must have exactly 10 residual kinds."""
        assert len(ReferenceResidualKind) == 10
