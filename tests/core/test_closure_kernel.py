"""
Tests for closure_kernel minimal closure nucleus.

Origin: docs/00_MAQOOL_CONSTITUTION.md §5 Rule 1
Authority: docs/15_PROJECT_ROADMAP.md Phase 1 (L1 open)
"""
from __future__ import annotations

import pytest

from taaqqul_slot_geometry.constitution.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.core.closure_kernel import (
    ClosureCertificate,
    Trace,
    close_l3_root_stem,
    close_l6_past_mujarrad_event,
    close_l7_augmented,
    hamzat_wasl_gate,
    issue_provisional_certificate,
    madd_gate,
    make_closure_certificate,
    should_block_transition,
)


def _trace(layer: str = "L1_Atom") -> Trace:
    return Trace(trace_id="t-1", source_layer=layer, evidence=("e1",))


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
        trace=_trace("L6_PastMujarradEvent"),
    )
    assert cert.status == "blocked"
    assert any("fa_il" in item.message for item in cert.residual_entries)


def test_l7_augmented_requires_prior_minimal_closure():
    cert = close_l7_augmented(
        augmentation_pattern="أفعل",
        minimal_mujarrad_closed=False,
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
        trace=_trace("L6_PastMujarradEvent"),
    )
    provisional = issue_provisional_certificate((cert_ok, cert_blocked))
    assert "L6_PastMujarradEvent" in provisional.blocked_layers
    assert provisional.allowed_next_steps == ()
