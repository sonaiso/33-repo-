"""
Tests for declarative DAL_ONLY -> LAFZI_FORM bridge specs.

Origin: docs/07_GATE_BRIDGE_CONSTITUTION.md
Authority: docs/15_PROJECT_ROADMAP.md Phase 1 PR-37
"""
from __future__ import annotations

import pytest

from taaqqul_slot_geometry.L1.dal_to_lafzi_bridge import (
    DAL_SURFACE_TO_LAFZI_ENTRY_GATE,
    DAL_SURFACE_TO_LAFZI_OPERATION_SPEC,
    DAL_TO_LAFZI_BRIDGE_ID,
    DAL_TO_LAFZI_BRIDGE_SPEC,
    PERMITTED_DOMAIN_PATHS,
)
from taaqqul_slot_geometry.L1.domain_ids import DomainID


def test_operation_spec_declares_only_dal_to_lafzi():
    """trace_ref: docs/07_GATE_BRIDGE_CONSTITUTION.md Gate/Bridge Contract Law."""
    assert DAL_SURFACE_TO_LAFZI_OPERATION_SPEC.source_domain_id == DomainID.D1_DAL_ONLY
    assert DAL_SURFACE_TO_LAFZI_OPERATION_SPEC.target_domain_id == DomainID.D2_LAFZI_FORM


def test_gate_spec_is_bound_to_dal_only():
    """trace_ref: docs/07_GATE_BRIDGE_CONSTITUTION.md Gate/Bridge Contract Law."""
    assert DAL_SURFACE_TO_LAFZI_ENTRY_GATE.source_domain_id == DomainID.D1_DAL_ONLY


def test_bridge_spec_declares_dal_to_lafzi_only():
    """trace_ref: docs/07_GATE_BRIDGE_CONSTITUTION.md Gate/Bridge Contract Law."""
    assert DAL_TO_LAFZI_BRIDGE_SPEC.bridge_id == DAL_TO_LAFZI_BRIDGE_ID
    assert DAL_TO_LAFZI_BRIDGE_SPEC.source_domain_id == DomainID.D1_DAL_ONLY
    assert DAL_TO_LAFZI_BRIDGE_SPEC.target_domain_id == DomainID.D2_LAFZI_FORM


@pytest.mark.parametrize(
    "source,target",
    [
        (DomainID.D1_DAL_ONLY, DomainID.D3_LEXICAL_MADLUL),
        (DomainID.D1_DAL_ONLY, DomainID.D4_RELATION),
        (DomainID.D2_LAFZI_FORM, DomainID.D3_LEXICAL_MADLUL),
        (DomainID.D2_LAFZI_FORM, DomainID.D4_RELATION),
    ],
)
def test_forbidden_paths_are_not_permitted(source: DomainID, target: DomainID):
    """trace_ref: docs/11_LAFZI_FORM_CONSTITUTION.md Domain separation constraints."""
    assert (source, target) not in PERMITTED_DOMAIN_PATHS


def test_only_one_permitted_path_exists():
    """trace_ref: docs/11_LAFZI_FORM_CONSTITUTION.md Entry constraints."""
    assert PERMITTED_DOMAIN_PATHS == frozenset(
        {(DomainID.D1_DAL_ONLY, DomainID.D2_LAFZI_FORM)}
    )
