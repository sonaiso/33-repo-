"""
L1 package — Formal Description layer.
Origin: docs/00_MAQOOL_CONSTITUTION.md §5 Rule 1; §6 L1
Authority: docs/15_PROJECT_ROADMAP.md Phase 1 PR-10, PR-11
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
from taaqqul_slot_geometry.L1.postulate import (
    POSTULATE_BY_ID,
    POSTULATE_P1,
    POSTULATE_P2,
    POSTULATE_P3,
    POSTULATE_P4,
    POSTULATE_P5,
    POSTULATES,
    Postulate,
    PostulateCategory,
    get_postulate,
    postulates_by_category,
    total_postulate_count,
    verify_postulate_coverage,
)

__all__ = [
    "BoundaryCondition",
    "DEFINITION_BY_TERM",
    "DefinitionCategory",
    "FORMAL_DEFINITIONS",
    "FormalDefinition",
    "POSTULATE_BY_ID",
    "POSTULATE_P1",
    "POSTULATE_P2",
    "POSTULATE_P3",
    "POSTULATE_P4",
    "POSTULATE_P5",
    "POSTULATES",
    "Postulate",
    "PostulateCategory",
    "definitions_by_category",
    "get_definition",
    "get_postulate",
    "postulates_by_category",
    "total_definition_count",
    "total_postulate_count",
    "verify_identity_preservation",
    "verify_postulate_coverage",
]
