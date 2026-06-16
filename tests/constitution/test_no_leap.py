"""
Tests for No-Leap Axiom — Rule 8.
Origin: docs/00_MAQOOL_CONSTITUTION.md §5 Rule 8
"""
import pytest

from tests.conftest import ConstitutionalChainTestCase
from taaqqul_slot_geometry.constitution.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.constitution.transition_gate import (
    TransitionError,
    TransitionGate,
)


class TestNoLeapAxiom(ConstitutionalChainTestCase):
    """Origin: docs/00_MAQOOL_CONSTITUTION.md §5 Rule 8"""

    @pytest.mark.parametrize("src,tgt", [
        ("L0", "L2"),
        ("L0", "L3"),
        ("L1", "L3"),
        ("L2", "L0"),
        ("L3", "L1"),
        ("L3", "L0"),
    ])
    def test_leap_rejected(self, src, tgt):
        """Every non-adjacent pair (abs diff > 1) must be rejected."""
        with pytest.raises(TransitionError) as exc_info:
            TransitionGate(
                source_layer=src,
                target_layer=tgt,
                bridge_license_ref="test_ref",
            )
        assert exc_info.value.failure_code == FailureCode.M_CX_02

    @pytest.mark.parametrize("src,tgt", [
        ("L0", "L1"),
        ("L1", "L2"),
        ("L2", "L3"),
        ("L1", "L0"),
        ("L2", "L1"),
        ("L3", "L2"),
    ])
    def test_adjacent_allowed(self, src, tgt):
        """Adjacent layer transitions are allowed."""
        gate = TransitionGate(
            source_layer=src,
            target_layer=tgt,
            bridge_license_ref="test_ref",
        )
        assert gate.source_layer == src
        assert gate.target_layer == tgt
