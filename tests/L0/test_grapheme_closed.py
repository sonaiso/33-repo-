"""
Tests for Grapheme — L0 closure of 28 Arabic letters.
Origin: docs/00_MAQOOL_CONSTITUTION.md §2 Category 2 (Grapheme); docs/01_L0_PHONETIC_BOUNDARY.md BL-L0-03
"""
import pytest

from tests.conftest import ConstitutionalChainTestCase
from taaqqul_slot_geometry.L0.grapheme import (
    GRAPHEME_BY_SYMBOL,
    GRAPHEME_TABLE,
    Grapheme,
    get_grapheme,
)
from taaqqul_slot_geometry.constitution.failure_taxonomy import FailureCode


class TestGraphemeClosed(ConstitutionalChainTestCase):
    """Origin: docs/00_MAQOOL_CONSTITUTION.md §2 Category 2 (Grapheme)"""

    def test_exactly_28_graphemes(self):
        """BL-L0-03: exactly 28 Arabic graphemes exist."""
        assert len(GRAPHEME_TABLE) == 28

    def test_grapheme_table_symbols_unique(self):
        """All grapheme symbols are unique."""
        symbols = [g.symbol for g in GRAPHEME_TABLE]
        assert len(symbols) == len(set(symbols))

    def test_get_grapheme_returns_correct(self):
        """Pure lookup returns the grapheme for a known symbol."""
        g = get_grapheme("b")
        assert g.symbol == "b"
        assert g.arabic_letter == "ب"

    def test_get_grapheme_unknown_rejected(self):
        """M-00-03: Unknown symbol must be rejected."""
        with pytest.raises(ValueError) as exc_info:
            get_grapheme("UNKNOWN")
        assert FailureCode.M_00_03.value in str(exc_info.value)

    def test_grapheme_trace_ref_present(self):
        """Rule 2: trace_ref present on every grapheme."""
        for g in GRAPHEME_TABLE:
            assert g.trace_ref, f"Missing trace_ref on grapheme {g.symbol!r}"

    def test_grapheme_rank_is_candidate(self):
        """Rule 2: rank is CANDIDATE on every grapheme."""
        for g in GRAPHEME_TABLE:
            assert g.rank == "CANDIDATE", f"Wrong rank on grapheme {g.symbol!r}"

    def test_grapheme_residuals_present(self):
        """Rule 2: residuals field is frozenset on every grapheme."""
        for g in GRAPHEME_TABLE:
            assert isinstance(g.residuals, frozenset)

    def test_grapheme_frozen(self):
        """Rule 3: Grapheme must be frozen."""
        g = get_grapheme("k")
        with pytest.raises((AttributeError, TypeError)):
            g.symbol = "x"  # type: ignore[misc]

    def test_invalid_symbol_constructor_rejected(self):
        """M-00-03: Grapheme with unknown symbol must be rejected at construction."""
        with pytest.raises(ValueError) as exc_info:
            Grapheme(
                symbol="Z",
                arabic_letter="?",
                articulation_point="halq_aqsa",
                articulation_manner="hams",
                phoneme_symbol="Z",
            )
        assert FailureCode.M_00_03.value in str(exc_info.value)

    def test_all_graphemes_have_articulation_point(self):
        """Every grapheme has a non-empty articulation_point."""
        for g in GRAPHEME_TABLE:
            assert g.articulation_point, f"Missing articulation_point on {g.symbol!r}"

    def test_all_graphemes_have_articulation_manner(self):
        """Every grapheme has a non-empty articulation_manner."""
        for g in GRAPHEME_TABLE:
            assert g.articulation_manner, f"Missing articulation_manner on {g.symbol!r}"
