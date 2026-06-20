"""
Declarative DAL_ONLY -> LAFZI_FORM bridge specs.

Origin: docs/07_GATE_BRIDGE_CONSTITUTION.md
Authority: docs/15_PROJECT_ROADMAP.md Phase 1 PR-37
"""
from __future__ import annotations

from typing import FrozenSet, Tuple

from taaqqul_slot_geometry.constitution.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.L1.domain_bridge_gate import BridgeSpec, GateSpec, OperationSpec
from taaqqul_slot_geometry.L1.domain_ids import DomainID
from taaqqul_slot_geometry.L1.lafzi_form import LAFZI_FORM_FORBIDDEN_OUTPUTS

DAL_TO_LAFZI_BRIDGE_ID = "DalToLafziBridgeSpec"
DAL_SURFACE_TO_LAFZI_GATE_ID = "DalSurfaceToLafziEntryGate"
DAL_SURFACE_TO_LAFZI_OPERATION_ID = "DalSurfaceToLafziOperation"

PERMITTED_DOMAIN_PATHS: FrozenSet[Tuple[DomainID, DomainID]] = frozenset(
    [(DomainID.D1_DAL_ONLY, DomainID.D2_LAFZI_FORM)]
)

DAL_SURFACE_TO_LAFZI_OPERATION_SPEC = OperationSpec(
    operation_id=DAL_SURFACE_TO_LAFZI_OPERATION_ID,
    source_domain_id=DomainID.D1_DAL_ONLY,
    target_domain_id=DomainID.D2_LAFZI_FORM,
    operation_kind="dal_surface_to_lafzi_form",
    input_contract_refs=("docs/10_DAL_ATOMIC_CONSTITUTION.md",),
    output_contract_refs=("docs/11_LAFZI_FORM_CONSTITUTION.md",),
    forbidden_outputs=LAFZI_FORM_FORBIDDEN_OUTPUTS,
    required_gate_ids=(DAL_SURFACE_TO_LAFZI_GATE_ID,),
    trace_ref="docs/07_GATE_BRIDGE_CONSTITUTION.md §Gate declaration",
)

DAL_SURFACE_TO_LAFZI_ENTRY_GATE = GateSpec(
    gate_id=DAL_SURFACE_TO_LAFZI_GATE_ID,
    source_domain_id=DomainID.D1_DAL_ONLY,
    input_contract_ref="docs/10_DAL_ATOMIC_CONSTITUTION.md",
    predicate_ref="declarative:DalSurfaceToLafziEntryGate",
    failure_code=FailureCode.M_00_09,
    residual_code="dal_to_lafzi_gate_requires_declared_bridge",
    forbidden_outputs=LAFZI_FORM_FORBIDDEN_OUTPUTS,
    trace_ref="docs/07_GATE_BRIDGE_CONSTITUTION.md §Gate declaration",
)

DAL_TO_LAFZI_BRIDGE_SPEC = BridgeSpec(
    bridge_id=DAL_TO_LAFZI_BRIDGE_ID,
    source_domain_id=DomainID.D1_DAL_ONLY,
    target_domain_id=DomainID.D2_LAFZI_FORM,
    source_contract_ref="docs/10_DAL_ATOMIC_CONSTITUTION.md",
    target_contract_ref="docs/11_LAFZI_FORM_CONSTITUTION.md",
    translator_ref="declarative:DalToLafziTranslator",
    invariant_policy_ref="docs/07_GATE_BRIDGE_CONSTITUTION.md §Identity policy",
    required_proof_kinds=("IdentityProof", "BridgeProof", "DomainProof"),
    forbidden_outputs=LAFZI_FORM_FORBIDDEN_OUTPUTS,
    trace_ref="docs/07_GATE_BRIDGE_CONSTITUTION.md §Bridge declaration",
)

__all__ = [
    "DAL_SURFACE_TO_LAFZI_ENTRY_GATE",
    "DAL_SURFACE_TO_LAFZI_GATE_ID",
    "DAL_SURFACE_TO_LAFZI_OPERATION_ID",
    "DAL_SURFACE_TO_LAFZI_OPERATION_SPEC",
    "DAL_TO_LAFZI_BRIDGE_ID",
    "DAL_TO_LAFZI_BRIDGE_SPEC",
    "PERMITTED_DOMAIN_PATHS",
]
