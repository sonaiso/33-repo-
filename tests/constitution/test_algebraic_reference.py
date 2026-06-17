"""
Tests for AlgebraicReference — الإحالة الجبرية المرخّصة.

Origin: docs/00_MAQOOL_CONSTITUTION.md §5 Rules 6, 7, 8
Authority: Supreme Algebraic Reference Law
"""
import pytest

from taaqqul_slot_geometry.constitution.algebraic_reference import (
    AlgebraicReference,
    REFERENCE_LAYER_INDEX,
    REFERENCE_TYPE_DOMAIN,
    ReferenceCompositionError,
    ReferenceLayer,
    ReferenceType,
    RefResult,
    RefStatus,
    compose_chain,
    compose_references,
)
from taaqqul_slot_geometry.constitution.failure_taxonomy import FailureCode


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


# ══════════════════════════════════════════════════════════════════════════════
# §3  RefResult Tests
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
        """Rank must be CANDIDATE (no promotion in current phase)."""
        with pytest.raises(ValueError, match="rank_ceiling_exceeded"):
            RefResult(
                status=RefStatus.LICENSED,
                output_layer=ReferenceLayer.GLYPH,
                identity_preserved=True,
                rank="LICENSED",
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


# ══════════════════════════════════════════════════════════════════════════════
# §4  AlgebraicReference Tests
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
            cause="unicode_to_glyph_mapping_exists",
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
        assert "preventer_blocked" in result.residuals

    def test_apply_deferred_operator_unlicensed(self):
        """apply() with unlicensed operator returns DEFERRED."""
        ref = self._make_digital_ref(operator_licensed=False)
        result = ref.apply()
        assert result.status == RefStatus.DEFERRED
        assert "operator_not_licensed" in result.reason

    def test_apply_blocked_identity_loss(self):
        """apply(identity_preserved=False) returns BLOCKED (P3)."""
        ref = self._make_digital_ref()
        result = ref.apply(identity_preserved=False)
        assert result.status == RefStatus.BLOCKED
        assert "identity_loss" in result.reason

    def test_no_leap_enforced(self):
        """References that skip layers must be rejected.

        Note: The type-domain check fires before adjacency check,
        so we use a type that doesn't have a fixed domain mapping
        to test pure adjacency. Instead, we verify that the type-domain
        check itself prevents leaps by rejecting mismatched targets.
        """
        # Using DIGITAL_REF with wrong target triggers type mismatch
        # (which is the correct constitutional guard — type binds to layer)
        with pytest.raises(ValueError, match="reference_target_type_mismatch"):
            AlgebraicReference(
                reference_type=ReferenceType.DIGITAL_REF,
                source_layer=ReferenceLayer.DIGITAL,
                target_layer=ReferenceLayer.VOCALIZED,  # Skips glyph + letter_mark
                domain="test",
                condition="test",
                cause="test",
            )

    def test_source_layer_mismatch(self):
        """Reference with wrong source layer for its type must be rejected."""
        with pytest.raises(ValueError, match="reference_source_type_mismatch"):
            AlgebraicReference(
                reference_type=ReferenceType.DIGITAL_REF,
                source_layer=ReferenceLayer.GLYPH,  # Wrong! Should be DIGITAL
                target_layer=ReferenceLayer.LETTER_MARK,
                domain="test",
                condition="test",
                cause="test",
            )

    def test_target_layer_mismatch(self):
        """Reference with wrong target layer for its type must be rejected."""
        with pytest.raises(ValueError, match="reference_target_type_mismatch"):
            AlgebraicReference(
                reference_type=ReferenceType.DIGITAL_REF,
                source_layer=ReferenceLayer.DIGITAL,
                target_layer=ReferenceLayer.LETTER_MARK,  # Wrong! Should be GLYPH
                domain="test",
                condition="test",
                cause="test",
            )

    def test_empty_domain_rejected(self):
        """Domain must be non-empty."""
        with pytest.raises(ValueError, match="reference_condition_failed"):
            self._make_digital_ref(domain="")

    def test_empty_condition_rejected(self):
        """Condition must be non-empty."""
        with pytest.raises(ValueError, match="reference_condition_failed"):
            self._make_digital_ref(condition="")

    def test_empty_cause_rejected(self):
        """Cause must be non-empty."""
        with pytest.raises(ValueError, match="reference_condition_failed"):
            self._make_digital_ref(cause="")

    def test_frozen(self):
        """AlgebraicReference must be frozen."""
        ref = self._make_digital_ref()
        with pytest.raises(AttributeError):
            ref.domain = "mutated"  # type: ignore[misc]

    def test_rank_candidate(self):
        """Rank must be CANDIDATE."""
        with pytest.raises(ValueError, match="rank_ceiling_exceeded"):
            self._make_digital_ref(rank="LICENSED")


# ══════════════════════════════════════════════════════════════════════════════
# §5  Composition Tests
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
            cause=f"cause_{ref_type.value}",
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
            cause="mapping",
            preventers=frozenset({"invalid_codepoint"}),  # Will fail
        )
        glyph = self._make_ref(ReferenceType.GLYPH_REF)

        r1, r2 = compose_references(digital, glyph)
        assert r1.status == RefStatus.BLOCKED
        assert r2.status == RefStatus.BLOCKED
        assert "predecessor_failed" in r2.reason

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
                cause="mapping",
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

    def test_compose_chain_empty_rejected(self):
        """Empty chain must be rejected."""
        with pytest.raises(ValueError, match="reference_condition_failed"):
            compose_chain(())


# ══════════════════════════════════════════════════════════════════════════════
# §6  Agent-Binding Constitutional Tests
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
            cause="mapping",
        )
        assert ref.trace_ref != ""
        assert ref.rank == "CANDIDATE"
        assert isinstance(ref.residuals, frozenset)

    def test_weight_does_not_cross_to_meaning(self):
        """Morphological reference stays within Lafz→Mufrad (no meaning)."""
        src, tgt = REFERENCE_TYPE_DOMAIN[ReferenceType.MORPHOLOGICAL_REF]
        assert src == ReferenceLayer.LAFZ
        assert tgt == ReferenceLayer.MUFRAD
        # Mufrad is NOT meaning — it's classification candidate only

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
