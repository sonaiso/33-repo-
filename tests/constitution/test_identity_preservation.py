"""
Tests for IdentityPreservation and TransitionGate.
Origin: docs/00_MAQOOL_CONSTITUTION.md §5 Rules 6, 7, 8
"""
import pytest

from tests.conftest import ConstitutionalChainTestCase
from taaqqul_slot_geometry.constitution.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.constitution.identity_preservation import (
    IdentityLossError,
    IdentityPreservation,
)
from taaqqul_slot_geometry.constitution.transition_gate import (
    TransitionError,
    TransitionGate,
)


class TestIdentityPreservation(ConstitutionalChainTestCase):
    """Origin: docs/00_MAQOOL_CONSTITUTION.md §5 Rule 7"""

    def test_valid_preservation(self):
        """Identity is preserved when source ⊆ preserved."""
        ip = IdentityPreservation(
            source_identity=frozenset({"a", "b"}),
            added_attributes=frozenset({"c"}),
            preserved=frozenset({"a", "b"}),
        )
        assert ip.target_identity == frozenset({"a", "b", "c"})

    def test_identity_loss_raises(self):
        """Rule 7: IdentityLossError must be raised when identity is lost."""
        with pytest.raises(IdentityLossError) as exc_info:
            IdentityPreservation(
                source_identity=frozenset({"a", "b", "c"}),
                added_attributes=frozenset(),
                preserved=frozenset({"a"}),  # b and c are lost
            )
        assert exc_info.value.failure_code == FailureCode.M_CX_01

    def test_trace_ref_present(self):
        """Rule 2: trace_ref must be present."""
        ip = IdentityPreservation(
            source_identity=frozenset({"x"}),
            added_attributes=frozenset(),
            preserved=frozenset({"x"}),
        )
        assert ip.trace_ref

    def test_rank_is_candidate(self):
        """Rule 2: rank is CANDIDATE."""
        ip = IdentityPreservation(
            source_identity=frozenset({"x"}),
            added_attributes=frozenset(),
            preserved=frozenset({"x"}),
        )
        assert ip.rank == "CANDIDATE"

    def test_frozen(self):
        """Rule 3: IdentityPreservation must be frozen."""
        ip = IdentityPreservation(
            source_identity=frozenset({"x"}),
            added_attributes=frozenset(),
            preserved=frozenset({"x"}),
        )
        with pytest.raises((AttributeError, TypeError)):
            ip.rank = "VERDICT"  # type: ignore[misc]


class TestTransitionGate(ConstitutionalChainTestCase):
    """Origin: docs/00_MAQOOL_CONSTITUTION.md §5 Rules 6, 8"""

    def test_valid_l0_to_l1_gate(self):
        """A valid L0→L1 gate can be created."""
        gate = TransitionGate(
            source_layer="L0",
            target_layer="L1",
            bridge_license_ref="test_bridge_L0_L1",
        )
        assert gate.source_layer == "L0"
        assert gate.target_layer == "L1"

    def test_leap_forbidden(self):
        """Rule 8: No-leap axiom — skipping a layer is rejected."""
        with pytest.raises(TransitionError) as exc_info:
            TransitionGate(
                source_layer="L0",
                target_layer="L2",
                bridge_license_ref="test_ref",
            )
        assert exc_info.value.failure_code == FailureCode.M_CX_02

    def test_empty_bridge_ref_rejected(self):
        """M_CX_03: Empty bridge_license_ref must be rejected."""
        with pytest.raises(TransitionError) as exc_info:
            TransitionGate(
                source_layer="L0",
                target_layer="L1",
                bridge_license_ref="",
            )
        assert exc_info.value.failure_code == FailureCode.M_CX_03

    def test_unknown_layer_rejected(self):
        """M_CX_13: Unknown layer name must be rejected."""
        with pytest.raises(TransitionError) as exc_info:
            TransitionGate(
                source_layer="L0",
                target_layer="L99",
                bridge_license_ref="test_ref",
            )
        assert exc_info.value.failure_code == FailureCode.M_CX_13

    def test_prove_transition_valid(self):
        """prove_transition returns IdentityPreservation for valid transition."""
        gate = TransitionGate(
            source_layer="L0",
            target_layer="L1",
            bridge_license_ref="bridge_ref",
        )
        proof = gate.prove_transition(
            source_identity=frozenset({"consonant", "pattern"}),
            target_identity=frozenset({"consonant", "pattern", "definition"}),
        )
        assert isinstance(proof, IdentityPreservation)
        assert frozenset({"consonant", "pattern"}).issubset(proof.preserved)

    def test_prove_transition_identity_loss_raises(self):
        """prove_transition raises IdentityLossError when source identity is lost."""
        gate = TransitionGate(
            source_layer="L0",
            target_layer="L1",
            bridge_license_ref="bridge_ref",
        )
        with pytest.raises(IdentityLossError):
            gate.prove_transition(
                source_identity=frozenset({"consonant", "pattern", "lost_attr"}),
                target_identity=frozenset({"consonant"}),  # pattern and lost_attr gone
            )

    def test_gate_frozen(self):
        """Rule 3: TransitionGate must be frozen."""
        gate = TransitionGate(
            source_layer="L0",
            target_layer="L1",
            bridge_license_ref="test_ref",
        )
        with pytest.raises((AttributeError, TypeError)):
            gate.source_layer = "L1"  # type: ignore[misc]
