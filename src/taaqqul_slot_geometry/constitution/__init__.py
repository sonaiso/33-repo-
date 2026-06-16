"""
Constitution package — root authority for Taaqol-GPT.
Origin: docs/00_MAQOOL_CONSTITUTION.md
"""
from taaqqul_slot_geometry.constitution.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.constitution.identity_preservation import (
    IdentityLossError,
    IdentityPreservation,
)
from taaqqul_slot_geometry.constitution.maqool_constitution import (
    CONSTITUTION,
    MaqoolConstitution,
)
from taaqqul_slot_geometry.constitution.transition_gate import (
    TransitionError,
    TransitionGate,
)

__all__ = [
    "FailureCode",
    "IdentityLossError",
    "IdentityPreservation",
    "MaqoolConstitution",
    "CONSTITUTION",
    "TransitionError",
    "TransitionGate",
]
