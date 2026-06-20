"""
Tests for DAL atomic pipeline outputs and bridge gating.
Origin: docs/06_DOMAIN_SLOT_GEOMETRY_CONSTITUTION.md
"""
from __future__ import annotations

import pytest

from taaqqul_slot_geometry.constitution.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.core.dal_atomic_pipeline import (
    HarakaOperation,
    SurfaceSkeletonStatus,
    build_dal_atomic_artifacts,
    open_role_eligibility_operations,
)
from taaqqul_slot_geometry.core.transition_registry import TransitionVerdict


class TestDalAtomicOutputs:
    """DAL_ONLY must emit only DAL artifacts, not role/meaning outputs."""

    def test_generates_requested_dal_artifacts(self) -> None:
        artifacts = build_dal_atomic_artifacts("بَ")
        assert len(artifacts.carrier_profiles) == 1
        assert len(artifacts.haraka_slots) == 1
        assert artifacts.surface_skeleton.status == SurfaceSkeletonStatus.DAL_BRIDGE_REQUIRED_TO_LAFZI
        assert artifacts.bridge_required_marker.required_bridge == "DalToLafziBridge"
        assert "ROOT_FORM" in artifacts.carrier_profiles[0].forbidden_outputs
        assert "LEXICAL_MEANING" in artifacts.haraka_slots[0].forbidden_outputs

    def test_missing_mark_suspends_surface(self) -> None:
        artifacts = build_dal_atomic_artifacts("ب")
        assert artifacts.haraka_slots[0].mark_id == "MISSING"
        assert artifacts.haraka_slots[0].outgoing_operation == HarakaOperation.UNRESOLVED
        assert artifacts.surface_skeleton.status == SurfaceSkeletonStatus.DAL_SUSPENDED_MISSING_MARK
        assert "missing_harakat" in artifacts.surface_skeleton.residuals

    def test_initial_sukun_is_blocked(self) -> None:
        artifacts = build_dal_atomic_artifacts("بْ")
        assert artifacts.haraka_slots[0].outgoing_operation == HarakaOperation.CLOSE
        assert artifacts.surface_skeleton.status == SurfaceSkeletonStatus.DAL_BLOCKED_INITIAL_SUKUN
        assert "initial_sukun_requires_repair_gate" in artifacts.surface_skeleton.residuals

    def test_specialized_marks_stay_unresolved_in_dal(self) -> None:
        artifacts = build_dal_atomic_artifacts("بً")
        assert artifacts.haraka_slots[0].outgoing_operation == HarakaOperation.UNRESOLVED
        assert "tanwin_requires_word_layer" in artifacts.haraka_slots[0].residuals


class TestRoleEligibilityGate:
    """Role eligibility opens only after DalToLafziBridge is licensed."""

    def test_requires_licensed_bridge(self) -> None:
        artifacts = build_dal_atomic_artifacts("بَ")
        with pytest.raises(ValueError, match=FailureCode.M_00_09.value):
            open_role_eligibility_operations(
                artifacts.bridge_required_marker,
                TransitionVerdict.DEFERRED,
            )

    def test_opens_after_bridge(self) -> None:
        artifacts = build_dal_atomic_artifacts("بَ")
        result = open_role_eligibility_operations(
            artifacts.bridge_required_marker,
            TransitionVerdict.LICENSED,
        )
        assert result == "ROLE_ELIGIBILITY_OPEN"
