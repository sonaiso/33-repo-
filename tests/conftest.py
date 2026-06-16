"""
Shared test infrastructure for Taaqol-GPT constitutional tests.
Origin: docs/00_MAQOOL_CONSTITUTION.md (all sections)
"""
from __future__ import annotations

from dataclasses import dataclass, field

import pytest


# ── Structural Case Descriptors ──────────────────────────────────────────────
# These frozen dataclasses provide typed, structural traceability for test cases.
# They can be used for test parameterization and constitutional origin tracking.


@dataclass(frozen=True)
class ConstitutionalTestCase:
    """Case descriptor for constitutional tests.

    Used as a structural record for test parameterization and traceability.

    Parameters
    ----------
    origin_law : str
        The constitutional law/rule being tested (e.g. "Rule 3").
    origin_law_ref : str
        Full document reference (e.g. "docs/00_MAQOOL_CONSTITUTION.md §5 Rule 3").
    branch_of_origin : str
        The constitutional branch (e.g. "L0_PHONETICS", "CONSTITUTION").
    description : str
        Human-readable description of what this test case verifies.
    """

    origin_law: str
    origin_law_ref: str
    branch_of_origin: str
    description: str = ""


@dataclass(frozen=True)
class ConstitutionalChainCase(ConstitutionalTestCase):
    """Extended case descriptor for chain/transition tests.

    Adds chain-specific metadata for tests that verify layer transitions,
    identity preservation, and no-leap axioms.

    Parameters
    ----------
    chain_position : str
        Position in the constitutional chain (e.g. "L0->L1").
    forbidden_shortcut_assertions : tuple[str, ...]
        Assertions that must NOT be bypassed.
    """

    chain_position: str = ""
    forbidden_shortcut_assertions: tuple[str, ...] = ()


# ── Test Base Class ──────────────────────────────────────────────────────────
# All test classes inherit from this. It carries structural origin metadata.


class ConstitutionalChainTestCase:
    """Base class for all constitutional chain tests.

    Every subclass MUST declare its constitutional origin in its docstring
    (format: ``Origin: <doc> <section>``).

    Every test method MUST:
    1. Declare its constitutional origin in its docstring.
    2. Test rejection with a named FailureCode where applicable.
    3. Test that ``trace_ref`` is present.
    4. Test that ``rank`` is ``"CANDIDATE"``.

    Subclasses SHOULD set these class-level attributes for structural traceability:
    - origin_law: str — the constitutional rule being tested
    - origin_law_ref: str — full document reference
    - branch_of_origin: str — constitutional branch (e.g. "L0_PHONETICS")
    """

    origin_law: str = ""
    origin_law_ref: str = ""
    branch_of_origin: str = ""
