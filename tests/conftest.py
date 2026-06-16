"""
Shared test infrastructure for Taaqol-GPT constitutional tests.
Origin: docs/00_MAQOOL_CONSTITUTION.md (all sections)
"""
from __future__ import annotations

import pytest


class ConstitutionalChainTestCase:
    """Base class for all constitutional chain tests.

    Every subclass MUST declare its constitutional origin in its docstring
    (format: ``Origin: <doc> <section>``).

    Every test method MUST:
    1. Declare its constitutional origin in its docstring.
    2. Test rejection with a named FailureCode where applicable.
    3. Test that ``trace_ref`` is present.
    4. Test that ``rank`` is ``"CANDIDATE"``.
    """
