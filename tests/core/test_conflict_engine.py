"""
Tests for PR #41 conflict engine contracts.

Origin: docs/00_MAQOOL_CONSTITUTION.md §5 Rule 1
Authority: docs/15_PROJECT_ROADMAP.md Phase 1 (L1 open)
"""
from __future__ import annotations

import pytest

from taaqqul_slot_geometry.constitution.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.core.closure_kernel import (
    CONFLICT_MSG_BLOCKER_RESIDUAL,
    CONFLICT_MSG_NASKH_NO_CHRONOLOGY,
    CONFLICT_MSG_TARJIH_BLOCKED,
    CONFLICT_MSG_UNRESOLVED_SUSPENDED,
    ConflictClaim,
    Residual,
    Trace,
    make_closure_certificate,
    resolve_closure_conflicts,
)


def _trace(trace_id: str, layer: str = "L1_Atom", evidence: tuple[str, ...] = ("e1",)) -> Trace:
    return Trace(trace_id=trace_id, source_layer=layer, evidence=evidence)


def _closed_cert(layer: str, trace_id: str) -> object:
    return make_closure_certificate(
        layer=layer,
        identity_preserved=True,
        boundary_declared=True,
        trace=_trace(trace_id, layer),
        residual_entries=(),
        next_permissions=("L2_Syllable",) if layer != "L12_Irab" else (),
        requires_next_permission=layer != "L12_Irab",
    )


def _blocked_cert(layer: str, trace_id: str) -> object:
    return make_closure_certificate(
        layer=layer,
        identity_preserved=True,
        boundary_declared=True,
        trace=_trace(trace_id, layer),
        residual_entries=(
            Residual(
                family="path",
                severity="blocker",
                message="synthetic_blocker_for_conflict_test",
                remediation_hint="clear blocker before transition",
            ),
        ),
        next_permissions=("L2_Syllable",) if layer != "L12_Irab" else (),
        requires_next_permission=layer != "L12_Irab",
    )


def test_conflict_engine_prefers_domain_separation_before_blocking():
    blocked = _blocked_cert("L1_Atom", "t-block")
    closed = _closed_cert("L1_Atom", "t-ok")
    result = resolve_closure_conflicts(
        claims=(
            ConflictClaim(certificate=blocked, domain_scope="past-event"),
            ConflictClaim(certificate=closed, domain_scope="tool-reference"),
        )
    )
    assert result.status == "separated"
    assert result.blocked_transition is False


def test_blocker_residual_prevents_transition():
    blocked = _blocked_cert("L1_Atom", "t-block")
    closed = _closed_cert("L1_Atom", "t-ok")
    result = resolve_closure_conflicts(
        claims=(
            ConflictClaim(certificate=blocked, domain_scope="same-domain"),
            ConflictClaim(certificate=closed, domain_scope="same-domain"),
        )
    )
    assert result.status == "blocked"
    assert result.blocked_transition is True
    assert any(item.message == CONFLICT_MSG_BLOCKER_RESIDUAL for item in result.residual_entries)


def test_unresolved_conflict_returns_suspended_certificate():
    c1 = _closed_cert("L1_Atom", "t-1")
    c2 = _closed_cert("L2_Syllable", "t-2")
    result = resolve_closure_conflicts(
        claims=(
            ConflictClaim(certificate=c1, domain_scope="same-domain"),
            ConflictClaim(certificate=c2, domain_scope="same-domain"),
        )
    )
    assert result.status == "suspended"
    assert any(
        item.message == CONFLICT_MSG_UNRESOLVED_SUSPENDED for item in result.residual_entries
    )


def test_tarjih_is_blocked_unless_jam_fails():
    c1 = _closed_cert("L1_Atom", "t-1")
    c2 = _closed_cert("L2_Syllable", "t-2")
    result = resolve_closure_conflicts(
        claims=(
            ConflictClaim(certificate=c1, domain_scope="same-domain", coexistence_permitted=True),
            ConflictClaim(certificate=c2, domain_scope="same-domain", coexistence_permitted=True),
        ),
        attempt_tarjih=True,
    )
    assert result.status == "suspended"
    assert any(
        item.message == CONFLICT_MSG_TARJIH_BLOCKED for item in result.residual_entries
    )


def test_no_naskh_like_behavior_without_chronology_evidence():
    c1 = _closed_cert("L1_Atom", "t-1")
    c2 = _closed_cert("L2_Syllable", "t-2")
    result = resolve_closure_conflicts(
        claims=(
            ConflictClaim(certificate=c1, domain_scope="same-domain", naskh_like_claim=True),
            ConflictClaim(certificate=c2, domain_scope="same-domain"),
        )
    )
    assert result.status == "suspended"
    assert any(
        item.message == CONFLICT_MSG_NASKH_NO_CHRONOLOGY
        for item in result.residual_entries
    )


def test_conflict_certificates_preserve_trace_ids():
    c1 = _closed_cert("L1_Atom", "trace-a")
    c2 = _closed_cert("L2_Syllable", "trace-b")
    result = resolve_closure_conflicts(
        claims=(
            ConflictClaim(certificate=c1, domain_scope="same-domain"),
            ConflictClaim(certificate=c2, domain_scope="same-domain"),
        )
    )
    assert result.candidate_trace_ids == ("trace-a", "trace-b")


def test_conflict_engine_rejects_empty_claim_set():
    with pytest.raises(ValueError, match=FailureCode.M_CX_08.value):
        resolve_closure_conflicts(claims=())
