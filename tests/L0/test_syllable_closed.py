"""
Tests for SyllableType and Syllable — L0 closure.
Origin: docs/00_MAQOOL_CONSTITUTION.md §4 (MCE-2); docs/01_L0_PHONETIC_BOUNDARY.md BL-L0-04
"""
import pytest

from tests.conftest import ConstitutionalChainTestCase
from taaqqul_slot_geometry.L0.phoneme import PhonemeUnit, PhoneticPattern
from taaqqul_slot_geometry.L0.syllable import Syllable, SyllableType, make_syllable
from taaqqul_slot_geometry.constitution.failure_taxonomy import FailureCode


def _cv() -> PhonemeUnit:
    return PhonemeUnit(consonant="k", pattern=PhoneticPattern.C_FATHA)


def _cvc() -> PhonemeUnit:
    return PhonemeUnit(consonant="k", pattern=PhoneticPattern.CVC_SUKUN)


def _cvv() -> PhonemeUnit:
    return PhonemeUnit(consonant="k", pattern=PhoneticPattern.C_FATHA_MADD)


class TestSyllableClosed(ConstitutionalChainTestCase):
    """Origin: docs/00_MAQOOL_CONSTITUTION.md §4 (MCE-2)"""

    def test_four_syllable_types_closed(self):
        """MCE-2: Exactly 4 syllable types exist."""
        assert len(list(SyllableType)) == 4

    def test_all_four_type_values_present(self):
        """All 4 syllable type values are present."""
        values = {s.value for s in SyllableType}
        assert "CV" in values
        assert "CVC" in values
        assert "CVV" in values
        assert "CVCC" in values

    def test_make_cv_syllable(self):
        """A CV syllable can be constructed from a C_FATHA phoneme."""
        syl = make_syllable((_cv(),))
        assert syl.syllable_type == SyllableType.CV

    def test_make_cvc_syllable(self):
        """A CVC syllable can be constructed from a CVC∅ phoneme."""
        syl = make_syllable((_cvc(),))
        assert syl.syllable_type == SyllableType.CVC

    def test_make_cvv_syllable(self):
        """A CVV syllable can be constructed from a C_FATHA_MADD phoneme."""
        syl = make_syllable((_cvv(),))
        assert syl.syllable_type == SyllableType.CVV

    def test_make_cvcc_syllable(self):
        """A CVCC syllable requires two CVC∅ phonemes."""
        syl = make_syllable((_cvc(), _cvc()))
        assert syl.syllable_type == SyllableType.CVCC

    def test_syllable_trace_ref_present(self):
        """Rule 2: trace_ref present."""
        syl = make_syllable((_cv(),))
        assert syl.trace_ref

    def test_syllable_rank_is_candidate(self):
        """Rule 2: rank is CANDIDATE."""
        syl = make_syllable((_cv(),))
        assert syl.rank == "CANDIDATE"

    def test_syllable_residuals_present(self):
        """Rule 2: residuals is frozenset."""
        syl = make_syllable((_cv(),))
        assert isinstance(syl.residuals, frozenset)

    def test_syllable_frozen(self):
        """Rule 3: Syllable must be frozen."""
        syl = make_syllable((_cv(),))
        with pytest.raises((AttributeError, TypeError)):
            syl.syllable_type = SyllableType.CVC  # type: ignore[misc]

    def test_empty_phoneme_sequence_rejected(self):
        """M-00-16: Empty phoneme sequence must be rejected."""
        with pytest.raises(ValueError) as exc_info:
            Syllable(phonemes=(), syllable_type=SyllableType.CV)
        assert FailureCode.M_00_16.value in str(exc_info.value)

    def test_mismatched_type_rejected(self):
        """M-00-17: Mismatched declared type must be rejected."""
        with pytest.raises(ValueError) as exc_info:
            Syllable(
                phonemes=(_cv(),),
                syllable_type=SyllableType.CVC,  # wrong
            )
        assert FailureCode.M_00_17.value in str(exc_info.value)
