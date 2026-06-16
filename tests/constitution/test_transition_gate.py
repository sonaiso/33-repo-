"""
Tests for TransitionGate — combined gate tests.
Origin: docs/00_MAQOOL_CONSTITUTION.md §5 Rules 6, 7, 8
"""
import pytest

from tests.conftest import ConstitutionalChainTestCase
from taaqqul_slot_geometry.constitution.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.constitution.transition_gate import (
    LAYER_INDEX,
    TransitionError,
    TransitionGate,
)


class TestTransitionGateClosed(ConstitutionalChainTestCase):
    """Origin: docs/00_MAQOOL_CONSTITUTION.md §5 Rules 6, 7, 8"""

    def test_layer_index_has_four_layers(self):
        """Four layer indices are defined."""
        assert set(LAYER_INDEX.keys()) == {"L0", "L1", "L2", "L3"}
        assert LAYER_INDEX["L0"] == 0
        assert LAYER_INDEX["L3"] == 3

    def test_valid_l1_to_l2(self):
        """L1→L2 transition is adjacent."""
        gate = TransitionGate(
            source_layer="L1",
            target_layer="L2",
            bridge_license_ref="ref",
        )
        assert gate.source_layer == "L1"

    def test_valid_l2_to_l3(self):
        """L2→L3 transition is adjacent."""
        gate = TransitionGate(
            source_layer="L2",
            target_layer="L3",
            bridge_license_ref="ref",
        )
        assert gate.target_layer == "L3"

    def test_l0_to_l2_leap_rejected(self):
        """M_CX_02: L0→L2 is a leap and must be rejected."""
        with pytest.raises(TransitionError) as exc_info:
            TransitionGate(
                source_layer="L0",
                target_layer="L2",
                bridge_license_ref="ref",
            )
        assert exc_info.value.failure_code == FailureCode.M_CX_02

    def test_l0_to_l3_leap_rejected(self):
        """M_CX_02: L0→L3 is an even greater leap and must be rejected."""
        with pytest.raises(TransitionError) as exc_info:
            TransitionGate(
                source_layer="L0",
                target_layer="L3",
                bridge_license_ref="ref",
            )
        assert exc_info.value.failure_code == FailureCode.M_CX_02

    def test_gate_trace_ref_present(self):
        """Rule 2: trace_ref present."""
        gate = TransitionGate(
            source_layer="L0",
            target_layer="L1",
            bridge_license_ref="ref",
        )
        assert gate.trace_ref

    def test_gate_rank_is_candidate(self):
        """Rule 2: rank is CANDIDATE."""
        gate = TransitionGate(
            source_layer="L0",
            target_layer="L1",
            bridge_license_ref="ref",
        )
        assert gate.rank == "CANDIDATE"
