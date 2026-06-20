"""
Tests for L1 DAL atomic contracts.

Origin: docs/10_DAL_ATOMIC_CONSTITUTION.md
Authority: docs/15_PROJECT_ROADMAP.md Phase 1 PR-35
"""
from __future__ import annotations

import pytest

from taaqqul_slot_geometry.constitution.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.L1.dal_atomic import (
    DAL_ONLY_FORBIDDEN_OUTPUTS,
    BridgeRequiredMarker,
    CarrierIdentitySlot,
    ClosureCell,
    EdgeState,
    HarakaFunctionSlot,
    SurfaceSkeletonCandidate,
)
from taaqqul_slot_geometry.L1.domain_ids import DomainID


def _carrier_payload() -> dict:
    return {
        "slot_id": "carrier-1",
        "carrier_symbol": "ب",
        "carrier_index": 0,
        "edge_state_ref": "edge-1",
        "proof_object_ref": "proof:carrier-1",
        "trace_ref": "docs/10_DAL_ATOMIC_CONSTITUTION.md",
    }


def _haraka_payload() -> dict:
    return {
        "slot_id": "haraka-1",
        "carrier_slot_ref": "carrier-1",
        "haraka_mark": "FATHA",
        "incoming_edge_ref": "edge-start",
        "outgoing_edge_ref": "edge-1",
        "proof_object_ref": "proof:haraka-1",
        "trace_ref": "docs/10_DAL_ATOMIC_CONSTITUTION.md",
    }


def _edge_payload() -> dict:
    return {
        "edge_id": "edge-1",
        "from_slot_ref": "carrier-1",
        "to_slot_ref": "carrier-2",
        "transition_label": "WASL",
        "proof_trace_ref": "trace:edge-1",
        "trace_ref": "docs/10_DAL_ATOMIC_CONSTITUTION.md",
    }


def _closure_payload() -> dict:
    return {
        "cell_id": "closure-1",
        "carrier_slot_refs": ("carrier-1",),
        "haraka_slot_refs": ("haraka-1",),
        "edge_state_refs": ("edge-1",),
        "waqf_wasl_projection_ref": "projection:ww-1",
        "proof_trace_ref": "trace:closure-1",
        "trace_ref": "docs/10_DAL_ATOMIC_CONSTITUTION.md",
    }


def _surface_payload() -> dict:
    return {
        "candidate_id": "surface-1",
        "closure_cell_ref": "closure-1",
        "carrier_slot_refs": ("carrier-1",),
        "haraka_slot_refs": ("haraka-1",),
        "waqf_wasl_projection_ref": "projection:ww-1",
        "proof_object_ref": "proof:surface-1",
        "trace_ref": "docs/10_DAL_ATOMIC_CONSTITUTION.md",
    }


def _bridge_marker_payload() -> dict:
    return {
        "marker_id": "bridge-required-1",
        "source_domain_id": DomainID.D1_DAL_ONLY,
        "target_domain_id": DomainID.D2_LAFZI_FORM,
        "required_bridge_id": "DalToLafziBridgeSpec",
        "reason": "DAL_ONLY cannot open LAFZI_FORM directly.",
        "proof_object_ref": "proof:bridge-required-1",
        "trace_ref": "docs/10_DAL_ATOMIC_CONSTITUTION.md",
    }


@pytest.mark.parametrize("entity_cls,payload_factory", [
    (CarrierIdentitySlot, _carrier_payload),
    (HarakaFunctionSlot, _haraka_payload),
    (EdgeState, _edge_payload),
    (ClosureCell, _closure_payload),
    (SurfaceSkeletonCandidate, _surface_payload),
    (BridgeRequiredMarker, _bridge_marker_payload),
])
def test_dal_entities_keep_candidate_rank(entity_cls, payload_factory):
    """trace_ref: docs/00A_CONSTITUTIONAL_PROGRAMMING_AMENDMENT.md L1 Output Envelope."""
    entity = entity_cls(**payload_factory())
    assert entity.rank == "CANDIDATE"


@pytest.mark.parametrize("entity_cls,payload_factory", [
    (CarrierIdentitySlot, _carrier_payload),
    (HarakaFunctionSlot, _haraka_payload),
    (EdgeState, _edge_payload),
    (ClosureCell, _closure_payload),
    (SurfaceSkeletonCandidate, _surface_payload),
    (BridgeRequiredMarker, _bridge_marker_payload),
])
def test_dal_entities_reject_rank_promotion(entity_cls, payload_factory):
    """trace_ref: docs/00A_CONSTITUTIONAL_PROGRAMMING_AMENDMENT.md L1 Output Envelope."""
    with pytest.raises(ValueError, match=FailureCode.M_01_16.value):
        entity_cls(**payload_factory(), rank="CERTIFICATE")  # type: ignore[arg-type]


@pytest.mark.parametrize("entity_cls,payload_factory", [
    (CarrierIdentitySlot, _carrier_payload),
    (HarakaFunctionSlot, _haraka_payload),
    (EdgeState, _edge_payload),
    (ClosureCell, _closure_payload),
    (SurfaceSkeletonCandidate, _surface_payload),
    (BridgeRequiredMarker, _bridge_marker_payload),
])
def test_dal_entities_require_trace_ref(entity_cls, payload_factory):
    """trace_ref: docs/00_MAQOOL_CONSTITUTION.md §5 Rule 2."""
    payload = payload_factory()
    payload["trace_ref"] = ""
    with pytest.raises(ValueError, match=FailureCode.M_01_14.value):
        entity_cls(**payload)


@pytest.mark.parametrize("entity_cls,payload_factory", [
    (CarrierIdentitySlot, _carrier_payload),
    (HarakaFunctionSlot, _haraka_payload),
    (EdgeState, _edge_payload),
    (ClosureCell, _closure_payload),
    (SurfaceSkeletonCandidate, _surface_payload),
    (BridgeRequiredMarker, _bridge_marker_payload),
])
def test_dal_entities_require_non_empty_forbidden_outputs(entity_cls, payload_factory):
    """trace_ref: docs/10_DAL_ATOMIC_CONSTITUTION.md DAL_ONLY Scope."""
    payload = payload_factory()
    payload["forbidden_outputs"] = ()
    with pytest.raises(ValueError, match=FailureCode.M_00_22.value):
        entity_cls(**payload)


@pytest.mark.parametrize("entity_cls,payload_factory", [
    (CarrierIdentitySlot, _carrier_payload),
    (HarakaFunctionSlot, _haraka_payload),
    (EdgeState, _edge_payload),
    (ClosureCell, _closure_payload),
    (SurfaceSkeletonCandidate, _surface_payload),
    (BridgeRequiredMarker, _bridge_marker_payload),
])
def test_dal_entities_require_proof_object_or_trace_ref(entity_cls, payload_factory):
    """trace_ref: docs/08_PROOF_OBJECT_CONSTITUTION.md Core Law."""
    payload = payload_factory()
    payload["proof_object_ref"] = ""
    payload["proof_trace_ref"] = ""
    with pytest.raises(ValueError, match=FailureCode.M_00_22.value):
        entity_cls(**payload)


def test_no_haraka_without_carrier():
    """trace_ref: docs/10_DAL_ATOMIC_CONSTITUTION.md Central Atomic Laws."""
    payload = _haraka_payload()
    payload["carrier_slot_ref"] = ""
    with pytest.raises(ValueError, match=FailureCode.M_00_22.value):
        HarakaFunctionSlot(**payload)


def test_no_surface_without_waqf_wasl_projection():
    """trace_ref: docs/10_DAL_ATOMIC_CONSTITUTION.md Central Atomic Laws."""
    payload = _surface_payload()
    payload["waqf_wasl_projection_ref"] = ""
    with pytest.raises(ValueError, match=FailureCode.M_00_22.value):
        SurfaceSkeletonCandidate(**payload)


def test_bridge_required_marker_rejects_non_dal_source():
    """trace_ref: docs/10_DAL_ATOMIC_CONSTITUTION.md DAL_ONLY Scope."""
    payload = _bridge_marker_payload()
    payload["source_domain_id"] = DomainID.D2_LAFZI_FORM
    with pytest.raises(ValueError, match=FailureCode.M_00_22.value):
        BridgeRequiredMarker(**payload)


def test_bridge_required_marker_rejects_non_lafzi_target():
    """trace_ref: docs/10_DAL_ATOMIC_CONSTITUTION.md DAL_ONLY Scope."""
    payload = _bridge_marker_payload()
    payload["target_domain_id"] = DomainID.D3_LEXICAL_MADLUL
    with pytest.raises(ValueError, match=FailureCode.M_00_22.value):
        BridgeRequiredMarker(**payload)


def test_dal_forbidden_outputs_cover_blocked_higher_layers():
    """trace_ref: docs/10_DAL_ATOMIC_CONSTITUTION.md DAL_ONLY Scope."""
    required = {
        "ROOT_FORM",
        "PATTERN_FORM",
        "WORD_FORM",
        "TOOL_FORM",
        "MABNI_FORM",
        "LEXICAL_MEANING",
        "ISNAD",
        "IFADAH",
        "HUKM",
        "TANZIL",
    }
    assert required.issubset(set(DAL_ONLY_FORBIDDEN_OUTPUTS))
