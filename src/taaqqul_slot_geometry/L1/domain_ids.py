"""
Canonical L1 Domain IDs.

Origin: docs/05_DOMAIN_REGISTRY_CONSTITUTION.md Canonical L1 Domain IDs
Authority: docs/15_PROJECT_ROADMAP.md Phase 1 PR-34
"""
from __future__ import annotations

from enum import Enum, unique
from typing import Tuple


@unique
class DomainID(str, Enum):
    """Canonical domain identifiers for L1 constitutional programming."""

    D0_TRACE = "D0_TRACE"
    D1_DAL_ONLY = "D1_DAL_ONLY"
    D2_LAFZI_FORM = "D2_LAFZI_FORM"
    D3_LEXICAL_MADLUL = "D3_LEXICAL_MADLUL"
    D4_RELATION = "D4_RELATION"
    D5_IFADAH = "D5_IFADAH"
    D6_HUKM = "D6_HUKM"
    D7_TANZIL = "D7_TANZIL"


CANONICAL_DOMAIN_IDS: Tuple[DomainID, ...] = (
    DomainID.D0_TRACE,
    DomainID.D1_DAL_ONLY,
    DomainID.D2_LAFZI_FORM,
    DomainID.D3_LEXICAL_MADLUL,
    DomainID.D4_RELATION,
    DomainID.D5_IFADAH,
    DomainID.D6_HUKM,
    DomainID.D7_TANZIL,
)


__all__ = [
    "CANONICAL_DOMAIN_IDS",
    "DomainID",
]
