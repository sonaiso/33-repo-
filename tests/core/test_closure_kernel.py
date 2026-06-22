"""
Tests for closure_kernel minimal closure nucleus.

Origin: docs/00_MAQOOL_CONSTITUTION.md §5 Rule 1
Authority: docs/15_PROJECT_ROADMAP.md Phase 1 (L1 open)
"""
from __future__ import annotations

import pytest

from taaqqul_slot_geometry.constitution.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.core.closure_kernel import (
    CoverageCaseRow,
    CoverageMatrix,
    ClosureCertificate,
    Residual,
    Trace,
    close_l10_derivation_family,
    close_l11_mabni_tool_reference,
    close_l12_i3rab_relation,
    close_l3_root_stem,
    close_l4_minimal_mujarrad,
    close_l5_jamid_anchor,
    close_l6_past_mujarrad_event,
    close_l7_augmented,
    close_l8_imperfect_event,
    close_l9_imperative_event,
    hamzat_wasl_gate,
    issue_provisional_certificate,
    madd_gate,
    make_closure_certificate,
    should_block_transition,
)


def _trace(layer: str = "L1_Atom") -> Trace:
    return Trace(trace_id="t-1", source_layer=layer, evidence=("e1",))


def _l3() -> ClosureCertificate:
    return close_l3_root_stem(
        radicals=("ق", "ت", "ل"),
        positions=("فاء", "عين", "لام"),
        trace=_trace("L3_RootStem"),
    )


def _l4_event() -> ClosureCertificate:
    return close_l4_minimal_mujarrad(
        path="event",
        pattern="فَعَلَ",
        lower_certificate=_l3(),
        trace=_trace("L4_MinimalMujarrad"),
    )


def test_trace_rejects_unknown_layer():
    with pytest.raises(ValueError, match=FailureCode.M_CX_13.value):
        Trace(trace_id="t-1", source_layer="L99", evidence=("e1",))


def test_closure_certificate_closed_when_no_residuals():
    cert = make_closure_certificate(
        layer="L1_Atom",
        identity_preserved=True,
        boundary_declared=True,
        trace=_trace(),
        residual_entries=(),
        next_permissions=("L2_Syllable",),
    )
    assert isinstance(cert, ClosureCertificate)
    assert cert.status == "closed"
    assert not should_block_transition(cert)


def test_l3_root_stem_produces_provisional_on_weak_letter():
    cert = close_l3_root_stem(
        radicals=("ق", "و", "ل"),
        positions=("فاء", "عين", "لام"),
        trace=_trace("L3_RootStem"),
    )
    assert cert.layer == "L3_RootStem"
    assert cert.status == "provisional"
    assert any("weak_letter" in item.message for item in cert.residual_entries)


def test_l3_root_stem_blocks_on_missing_radicals():
    cert = close_l3_root_stem(
        radicals=("ق", "و"),
        positions=("فاء", "عين"),
        trace=_trace("L3_RootStem"),
    )
    assert cert.status == "blocked"
    assert should_block_transition(cert)


def test_l6_past_mujarrad_requires_fa_il_slot():
    cert = close_l6_past_mujarrad_event(
        pattern="فَعَلَ",
        has_fa_il_slot=False,
        lower_certificate=_l4_event(),
        trace=_trace("L6_PastMujarradEvent"),
    )
    assert cert.status == "blocked"
    assert any("fa_il" in item.message for item in cert.residual_entries)


def test_l6_past_mujarrad_blocks_without_l4_certificate():
    cert = close_l6_past_mujarrad_event(
        pattern="فَعَلَ",
        has_fa_il_slot=True,
        lower_certificate=None,
        trace=_trace("L6_PastMujarradEvent"),
    )
    assert cert.status == "blocked"
    assert any(item.message == "past_event_without_minimal_mujarrad_closure" for item in cert.residual_entries)


def test_l7_augmented_requires_prior_minimal_closure_certificate():
    cert = close_l7_augmented(
        augmentation_pattern="أفعل",
        lower_certificate=None,
        trace=_trace("L7_Augmented"),
    )
    assert cert.status == "blocked"
    assert any(item.message == "augmentation_before_mujarrad" for item in cert.residual_entries)


def test_hamzat_wasl_gate_blocks_when_connection_rule_missing():
    ok, residuals = hamzat_wasl_gate(appears_in_start=True, drops_in_connection=False)
    assert not ok
    assert any(item.severity == "blocker" for item in residuals)


def test_madd_gate_blocks_on_sukun_extension():
    ok, residuals = madd_gate(motion="سكون", extended=True)
    assert not ok
    assert residuals[0].message == "madd_without_short_motion"


def test_provisional_certificate_drops_next_steps_when_blocker_exists():
    cert_ok = make_closure_certificate(
        layer="L1_Atom",
        identity_preserved=True,
        boundary_declared=True,
        trace=_trace(),
        next_permissions=("L2_Syllable",),
    )
    cert_blocked = close_l6_past_mujarrad_event(
        pattern="فَعَلَ",
        has_fa_il_slot=False,
        lower_certificate=_l4_event(),
        trace=_trace("L6_PastMujarradEvent"),
    )
    provisional = issue_provisional_certificate((cert_ok, cert_blocked))
    assert "L6_PastMujarradEvent" in provisional.blocked_layers
    assert provisional.allowed_next_steps == ()


def test_l8_imperfect_blocked_without_event_origin():
    l6 = close_l6_past_mujarrad_event(
        pattern="فَعَلَ",
        has_fa_il_slot=True,
        lower_certificate=_l4_event(),
        trace=_trace("L6_PastMujarradEvent"),
    )
    cert = close_l8_imperfect_event(
        has_event_origin=False,
        lower_certificate=l6,
        trace=_trace("L8_Imperfect"),
    )
    assert cert.status == "blocked"
    assert any(item.message == "imperfect_without_event_origin" for item in cert.residual_entries)


def test_l9_imperative_blocked_without_addressee_or_force_slot():
    l6 = close_l6_past_mujarrad_event(
        pattern="فَعَلَ",
        has_fa_il_slot=True,
        lower_certificate=_l4_event(),
        trace=_trace("L6_PastMujarradEvent"),
    )
    l8 = close_l8_imperfect_event(
        has_event_origin=True,
        lower_certificate=l6,
        trace=_trace("L8_Imperfect"),
    )
    cert = close_l9_imperative_event(
        has_addressee_slot=False,
        has_force_slot=False,
        lower_certificate=l8,
        trace=_trace("L9_Imperative"),
    )
    assert cert.status == "blocked"
    assert any(item.message == "imperative_without_addressee_slot" for item in cert.residual_entries)
    assert any(item.message == "imperative_without_force_slot" for item in cert.residual_entries)


def test_l10_derivation_blocked_without_mujarrad_or_event_origin():
    l4 = _l4_event()
    l7 = close_l7_augmented(
        augmentation_pattern="أفعل",
        lower_certificate=l4,
        trace=_trace("L7_Augmented"),
    )
    cert = close_l10_derivation_family(
        has_mujarrad_origin=False,
        has_event_origin=False,
        lower_certificate=l7,
        trace=_trace("L10_Derivation"),
    )
    assert cert.status == "blocked"
    assert any(item.message == "derivation_without_mujarrad_origin" for item in cert.residual_entries)
    assert any(item.message == "derivation_without_event_origin" for item in cert.residual_entries)


def test_l11_mabni_tool_blocked_when_forced_into_root_weight_path():
    l4 = _l4_event()
    l7 = close_l7_augmented(
        augmentation_pattern="أفعل",
        lower_certificate=l4,
        trace=_trace("L7_Augmented"),
    )
    l10 = close_l10_derivation_family(
        has_mujarrad_origin=True,
        has_event_origin=True,
        lower_certificate=l7,
        trace=_trace("L10_Derivation"),
    )
    cert = close_l11_mabni_tool_reference(
        forced_into_root_weight_path=True,
        functional_identity_licensed=True,
        lower_certificate=l10,
        trace=_trace("L11_MabniTool"),
    )
    assert cert.status == "blocked"
    assert any(item.message == "mabni_tool_forced_into_root_weight_path" for item in cert.residual_entries)


def test_l12_i3rab_blocked_without_syntactic_relation_or_factor():
    l4 = _l4_event()
    l7 = close_l7_augmented(
        augmentation_pattern="أفعل",
        lower_certificate=l4,
        trace=_trace("L7_Augmented"),
    )
    l10 = close_l10_derivation_family(
        has_mujarrad_origin=True,
        has_event_origin=True,
        lower_certificate=l7,
        trace=_trace("L10_Derivation"),
    )
    l11 = close_l11_mabni_tool_reference(
        forced_into_root_weight_path=False,
        functional_identity_licensed=True,
        lower_certificate=l10,
        trace=_trace("L11_MabniTool"),
    )
    cert = close_l12_i3rab_relation(
        has_syntactic_relation=False,
        has_governing_factor=False,
        carrier_certificate=l11,
        trace=_trace("L12_Irab"),
    )
    assert cert.status == "blocked"
    assert any(item.message == "i3rab_without_syntactic_relation" for item in cert.residual_entries)
    assert any(item.message == "i3rab_without_governing_factor" for item in cert.residual_entries)


def test_blocker_residual_in_lower_closure_prevents_next_transition():
    l6_blocked = close_l6_past_mujarrad_event(
        pattern="فَعَلَ",
        has_fa_il_slot=False,
        lower_certificate=_l4_event(),
        trace=_trace("L6_PastMujarradEvent"),
    )
    cert = close_l8_imperfect_event(
        has_event_origin=True,
        lower_certificate=l6_blocked,
        trace=_trace("L8_Imperfect"),
    )
    assert cert.status == "blocked"
    assert any(item.message == "required_lower_closure_blocked" for item in cert.residual_entries)


def test_provisional_certificate_records_allowed_and_blocked_transitions():
    cert_ok = make_closure_certificate(
        layer="L1_Atom",
        identity_preserved=True,
        boundary_declared=True,
        trace=_trace(),
        residual_entries=(),
        next_permissions=("L2_Syllable",),
    )
    cert_warn = make_closure_certificate(
        layer="L2_Syllable",
        identity_preserved=True,
        boundary_declared=True,
        trace=_trace("L2_Syllable"),
        residual_entries=(
            Residual(
                family="path",
                severity="warning",
                message="non_blocking_warning",
                remediation_hint="record warning only",
            ),
        ),
        next_permissions=("L3_RootStem",),
    )
    cert_blocked = close_l6_past_mujarrad_event(
        pattern="فَعَلَ",
        has_fa_il_slot=False,
        lower_certificate=_l4_event(),
        trace=_trace("L6_PastMujarradEvent"),
    )
    provisional = issue_provisional_certificate((cert_ok, cert_warn, cert_blocked))
    assert "L6_PastMujarradEvent" in provisional.blocked_layers
    assert "L2_Syllable" in provisional.provisional_layers
    assert provisional.allowed_next_steps == ()


def test_coverage_matrix_registers_rows_without_full_coverage_claim():
    matrix = CoverageMatrix()
    row = CoverageCaseRow(
        case_id="C-001",
        layer="L8_Imperfect",
        gate_name="close_l8_imperfect_event",
        expected_status="blocked",
        observed_status="blocked",
    )
    updated = matrix.register_case_row(row)
    assert len(updated.rows) == 1
    assert updated.rows[0].case_id == "C-001"
    assert updated.claimed_exhaustive is False


def test_l7_augmented_blocks_when_lower_certificate_is_blocked():
    l6_blocked = close_l6_past_mujarrad_event(
        pattern="فَعَلَ",
        has_fa_il_slot=False,
        lower_certificate=_l4_event(),
        trace=_trace("L6_PastMujarradEvent"),
    )
    cert = close_l7_augmented(
        augmentation_pattern="أفعل",
        lower_certificate=l6_blocked,
        trace=_trace("L7_Augmented"),
    )
    assert cert.status == "blocked"
    assert any(item.message == "required_lower_closure_blocked" for item in cert.residual_entries)


def test_l11_mabni_tool_can_close_without_l10_when_functional_identity_is_licensed():
    cert = close_l11_mabni_tool_reference(
        forced_into_root_weight_path=False,
        functional_identity_licensed=True,
        lower_certificate=None,
        trace=_trace("L11_MabniTool"),
    )
    assert cert.status == "closed"


def test_l12_i3rab_accepts_non_l11_carrier_certificate():
    l4 = _l4_event()
    l6 = close_l6_past_mujarrad_event(
        pattern="فَعَلَ",
        has_fa_il_slot=True,
        lower_certificate=l4,
        trace=_trace("L6_PastMujarradEvent"),
    )
    cert = close_l12_i3rab_relation(
        has_syntactic_relation=True,
        has_governing_factor=True,
        carrier_certificate=l6,
        trace=_trace("L12_Irab"),
    )
    assert cert.status == "closed"


def test_l5_jamid_anchor_blocks_outside_closed_set():
    cert = close_l5_jamid_anchor(
        anchor_type="quad",
        lower_certificate=close_l4_minimal_mujarrad(
            path="jamid",
            pattern=None,
            lower_certificate=_l3(),
            trace=_trace("L4_MinimalMujarrad"),
        ),
        trace=_trace("L5_Jamid"),
    )
    assert cert.status == "blocked"
    assert any(item.message == "jamid_anchor_outside_closed_set" for item in cert.residual_entries)
