"""
Tests for canonical L1 Domain IDs.

Origin: docs/05_DOMAIN_REGISTRY_CONSTITUTION.md Canonical L1 Domain IDs
Authority: docs/15_PROJECT_ROADMAP.md Phase 1 PR-34
"""
from __future__ import annotations

import pytest

from taaqqul_slot_geometry.L1.domain_ids import CANONICAL_DOMAIN_IDS, DomainID


def test_domain_ids_are_canonical_and_complete():
    """trace_ref: docs/05_DOMAIN_REGISTRY_CONSTITUTION.md Canonical L1 Domain IDs."""
    assert CANONICAL_DOMAIN_IDS == (
        DomainID.D0_TRACE,
        DomainID.D1_DAL_ONLY,
        DomainID.D2_LAFZI_FORM,
        DomainID.D3_LEXICAL_MADLUL,
        DomainID.D4_RELATION,
        DomainID.D5_IFADAH,
        DomainID.D6_HUKM,
        DomainID.D7_TANZIL,
    )


def test_d2_lafzi_form_is_canonical():
    """trace_ref: docs/05_DOMAIN_REGISTRY_CONSTITUTION.md ### D2_LAFZI_FORM."""
    assert DomainID.D2_LAFZI_FORM.value == "D2_LAFZI_FORM"


def test_legacy_d2_name_is_rejected():
    """trace_ref: docs/05_DOMAIN_REGISTRY_CONSTITUTION.md Canonical L1 Domain IDs."""
    with pytest.raises(ValueError):
        DomainID("D2_LAFZI_MADLUL_ONLY")
