"""
Tests for JamidAnchor — binary/ternary lexical anchors.
Origin: docs/01_L0_PHONETIC_BOUNDARY.md BL-L0-05
"""
import pytest

from tests.conftest import ConstitutionalChainTestCase
from taaqqul_slot_geometry.L0.jamid import (
    ALL_ANCHORS,
    BINARY_ANCHORS,
    TERNARY_ANCHORS,
    JamidAnchor,
    JamidAnchorType,
)
from taaqqul_slot_geometry.L0.phoneme import PhonemeUnit, PhoneticPattern
from taaqqul_slot_geometry.constitution.failure_taxonomy import FailureCode


class TestJamidClosed(ConstitutionalChainTestCase):
    """Origin: docs/01_L0_PHONETIC_BOUNDARY.md BL-L0-05"""

    def test_four_binary_anchors(self):
        """Exactly 4 binary jamid anchors exist (yd, dm, xd, fm)."""
        assert len(BINARY_ANCHORS) == 4

    def test_three_ternary_anchors(self):
        """Exactly 3 ternary jamid anchors exist (hjr, byt, bab)."""
        assert len(TERNARY_ANCHORS) == 3

    def test_all_anchors_count(self):
        """Total anchors = 7."""
        assert len(ALL_ANCHORS) == 7

    def test_binary_anchor_forms(self):
        """Binary anchors have the expected forms."""
        forms = {a.form for a in BINARY_ANCHORS}
        assert forms == {"yd", "dm", "xd", "fm"}

    def test_ternary_anchor_forms(self):
        """Ternary anchors have the expected forms."""
        forms = {a.form for a in TERNARY_ANCHORS}
        assert forms == {"hjr", "byt", "bab"}

    def test_binary_not_derivational_root(self):
        """BL-L0-05: Binary jamid anchors must NOT be derivational roots."""
        for anchor in BINARY_ANCHORS:
            assert anchor.is_derivational_root is False

    def test_ternary_not_derivational_root(self):
        """BL-L0-05: Ternary jamid anchors must also not be derivational roots."""
        for anchor in TERNARY_ANCHORS:
            assert anchor.is_derivational_root is False

    def test_is_derivational_root_true_rejected(self):
        """M-00-07: is_derivational_root=True must be rejected."""
        with pytest.raises(ValueError) as exc_info:
            JamidAnchor(
                form="yd",
                anchor_type=JamidAnchorType.BINARY,
                phonemes=(
                    PhonemeUnit(consonant="j", pattern=PhoneticPattern.C_FATHA),
                    PhonemeUnit(consonant="d", pattern=PhoneticPattern.C_SUKUN),
                ),
                is_derivational_root=True,
            )
        assert FailureCode.M_00_07.value in str(exc_info.value)

    def test_anchor_trace_ref_present(self):
        """Rule 2: trace_ref present on every anchor."""
        for anchor in ALL_ANCHORS:
            assert anchor.trace_ref

    def test_anchor_rank_is_candidate(self):
        """Rule 2: rank is CANDIDATE."""
        for anchor in ALL_ANCHORS:
            assert anchor.rank == "CANDIDATE"

    def test_anchor_frozen(self):
        """Rule 3: JamidAnchor must be frozen."""
        anchor = BINARY_ANCHORS[0]
        with pytest.raises((AttributeError, TypeError)):
            anchor.form = "zz"  # type: ignore[misc]

    def test_unknown_binary_form_rejected(self):
        """M-00-23: Unknown binary form must be rejected."""
        with pytest.raises(ValueError) as exc_info:
            JamidAnchor(
                form="zz",
                anchor_type=JamidAnchorType.BINARY,
                phonemes=(
                    PhonemeUnit(consonant="z", pattern=PhoneticPattern.C_FATHA),
                    PhonemeUnit(consonant="z", pattern=PhoneticPattern.C_SUKUN),
                ),
            )
        assert FailureCode.M_00_23.value in str(exc_info.value)

    def test_unknown_ternary_form_rejected(self):
        """M-00-24: Unknown ternary form must be rejected."""
        with pytest.raises(ValueError) as exc_info:
            JamidAnchor(
                form="zzz",
                anchor_type=JamidAnchorType.TERNARY,
                phonemes=(
                    PhonemeUnit(consonant="z", pattern=PhoneticPattern.C_FATHA),
                    PhonemeUnit(consonant="z", pattern=PhoneticPattern.C_FATHA),
                    PhonemeUnit(consonant="z", pattern=PhoneticPattern.C_SUKUN),
                ),
            )
        assert FailureCode.M_00_24.value in str(exc_info.value)
