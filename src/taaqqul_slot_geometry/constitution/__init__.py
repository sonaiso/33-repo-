"""
Constitution package — root authority for Taaqol-GPT.
Origin: docs/00_MAQOOL_CONSTITUTION.md
"""
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
from taaqqul_slot_geometry.constitution.branch_license import (
    BranchLicense,
    BranchLicenseError,
)
from taaqqul_slot_geometry.constitution.euclidean_axioms import (
    ALL_DEFINITIONS,
    ALL_POSTULATES,
    ALL_THEOREMS,
    DefinitionId,
    EuclideanDefinition,
    EuclideanPostulate,
    EuclideanTheorem,
    PostulateId,
    ProofStep,
    ProofVerificationError,
    ProofVerifier,
    SYSTEM_HASH,
    TheoremId,
)
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
    "ALL_DEFINITIONS",
    "ALL_POSTULATES",
    "ALL_THEOREMS",
    "AlgebraicReference",
    "BranchLicense",
    "BranchLicenseError",
    "CONSTITUTION",
    "DefinitionId",
    "EuclideanDefinition",
    "EuclideanPostulate",
    "EuclideanTheorem",
    "FailureCode",
    "IdentityLossError",
    "IdentityPreservation",
    "MaqoolConstitution",
    "PostulateId",
    "ProofStep",
    "ProofVerificationError",
    "ProofVerifier",
    "REFERENCE_LAYER_INDEX",
    "REFERENCE_TYPE_DOMAIN",
    "ReferenceCompositionError",
    "ReferenceLayer",
    "ReferenceType",
    "RefResult",
    "RefStatus",
    "SYSTEM_HASH",
    "TheoremId",
    "TransitionError",
    "TransitionGate",
    "compose_chain",
    "compose_references",
]
