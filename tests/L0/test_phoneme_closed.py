"""
Tests for PhoneticPattern and PhonemeUnit — L0 closure.
Origin: docs/00_MAQOOL_CONSTITUTION.md §3 (MCE-1); docs/01_L0_PHONETIC_BOUNDARY.md BL-L0-02
"""
import pytest

from tests.conftest import ConstitutionalChainTestCase
from taaqqul_slot_geometry.L0.phoneme import PhonemeUnit, PhoneticPattern
from taaqqul_slot_geometry.constitution.failure_taxonomy import FailureCode


class TestPhonemeClosed(ConstitutionalChainTestCase):
    """Origin: docs/00_MAQOOL_CONSTITUTION.md §3 (MCE-1)"""

    def test_eight_patterns_closed(self):
        """MCE-1: The 8 phonetic patterns are closed — no 9th may exist."""
        patterns = list(PhoneticPattern)
        assert len(patterns) == 8

    def test_all_eight_pattern_values(self):
        """All 8 pattern values are present."""
        values = {p.value for p in PhoneticPattern}
        assert "Ca" in values
        assert "Cu" in values
        assert "Ci" in values
        assert "C∅" in values
        assert "Caa" in values
        assert "Cuu" in values
        assert "Cii" in values
        assert "CVC∅" in values

    def test_phoneme_unit_valid(self):
        """A valid PhonemeUnit can be constructed."""
        unit = PhonemeUnit(consonant="k", pattern=PhoneticPattern.C_FATHA)
        assert unit.consonant == "k"
        assert unit.pattern == PhoneticPattern.C_FATHA

    def test_phoneme_unit_trace_ref_present(self):
        """Rule 2: trace_ref must be present."""
        unit = PhonemeUnit(consonant="k", pattern=PhoneticPattern.C_FATHA)
        assert unit.trace_ref
        assert "MAQOOL_CONSTITUTION" in unit.trace_ref

    def test_phoneme_unit_rank_is_candidate(self):
        """Rule 2: rank must be CANDIDATE."""
        unit = PhonemeUnit(consonant="k", pattern=PhoneticPattern.C_FATHA)
        assert unit.rank == "CANDIDATE"

    def test_phoneme_unit_residuals_present(self):
        """Rule 2: residuals field must be present (may be empty)."""
        unit = PhonemeUnit(consonant="k", pattern=PhoneticPattern.C_FATHA)
        assert isinstance(unit.residuals, frozenset)

    def test_phoneme_unit_frozen(self):
        """Rule 3: PhonemeUnit must be frozen (immutable)."""
        unit = PhonemeUnit(consonant="k", pattern=PhoneticPattern.C_FATHA)
        with pytest.raises((AttributeError, TypeError)):
            unit.consonant = "x"  # type: ignore[misc]

    def test_no_invalid_pattern(self):
        """M-00-02: Invalid pattern string must be rejected."""
        with pytest.raises((ValueError, TypeError)):
            PhonemeUnit(consonant="k", pattern="INVALID")

    def test_empty_consonant_rejected(self):
        """M-00-14: Empty consonant must be rejected."""
        with pytest.raises(ValueError) as exc_info:
            PhonemeUnit(consonant="", pattern=PhoneticPattern.C_FATHA)
        assert FailureCode.M_00_14.value in str(exc_info.value)

    def test_multi_char_consonant_rejected(self):
        """M-00-15: Consonant symbol longer than 4 chars must be rejected."""
        with pytest.raises(ValueError) as exc_info:
            PhonemeUnit(consonant="kabcde", pattern=PhoneticPattern.C_FATHA)
        assert FailureCode.M_00_15.value in str(exc_info.value)

    def test_identity_preservation_cv(self):
        """CV = C+a must preserve C and pattern."""
        unit = PhonemeUnit(consonant="k", pattern=PhoneticPattern.C_FATHA)
        assert unit.consonant == "k"
        assert unit.pattern == PhoneticPattern.C_FATHA

    def test_all_patterns_constructable(self):
        """Every one of the 8 patterns can produce a valid PhonemeUnit."""
        for pat in PhoneticPattern:
            unit = PhonemeUnit(consonant="k", pattern=pat)
            assert unit.pattern == pat
