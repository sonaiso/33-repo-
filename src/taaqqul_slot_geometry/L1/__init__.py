"""
L1 package — Formal Description layer.
Origin: docs/00_MAQOOL_CONSTITUTION.md §5 Rule 1; §6 L1
Authority: docs/15_PROJECT_ROADMAP.md Phase 1 PR-10
"""
from taaqqul_slot_geometry.L1.definition import (
    DEFINITION_BY_TERM,
    FORMAL_DEFINITIONS,
    BoundaryCondition,
    DefinitionCategory,
    FormalDefinition,
    definitions_by_category,
    get_definition,
    total_definition_count,
    verify_identity_preservation,
)

__all__ = [
    "BoundaryCondition",
    "DEFINITION_BY_TERM",
    "DefinitionCategory",
    "FORMAL_DEFINITIONS",
    "FormalDefinition",
    "definitions_by_category",
    "get_definition",
    "total_definition_count",
    "verify_identity_preservation",
]
