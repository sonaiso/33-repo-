"""
Tests for FailureCode — all 100 constitutional prohibitions enumerated.
Origin: docs/00_MAQOOL_CONSTITUTION.md §7
"""
import pytest

from tests.conftest import ConstitutionalChainTestCase
from taaqqul_slot_geometry.constitution.failure_taxonomy import FailureCode


class TestFailureCodes(ConstitutionalChainTestCase):
    """Origin: docs/00_MAQOOL_CONSTITUTION.md §7"""

    def test_at_least_100_codes(self):
        """Constitution requires 100 failure codes."""
        codes = list(FailureCode)
        assert len(codes) >= 100

    def test_l0_codes_present(self):
        """L0 failure codes (M_00_xx) are present."""
        l0_codes = [c for c in FailureCode if c.name.startswith("M_00_")]
        assert len(l0_codes) >= 10

    def test_l1_codes_present(self):
        """L1 failure codes (M_01_xx) are present."""
        l1_codes = [c for c in FailureCode if c.name.startswith("M_01_")]
        assert len(l1_codes) >= 10

    def test_l2_codes_present(self):
        """L2 failure codes (M_02_xx) are present."""
        l2_codes = [c for c in FailureCode if c.name.startswith("M_02_")]
        assert len(l2_codes) >= 10

    def test_l3_codes_present(self):
        """L3 failure codes (M_03_xx) are present."""
        l3_codes = [c for c in FailureCode if c.name.startswith("M_03_")]
        assert len(l3_codes) >= 10

    def test_cx_codes_present(self):
        """Cross-cutting failure codes (M_CX_xx) are present."""
        cx_codes = [c for c in FailureCode if c.name.startswith("M_CX_")]
        assert len(cx_codes) >= 10

    def test_no_ninth_pattern_code_present(self):
        """M_00_01 no_signifier_before_sound is the first L0 code."""
        assert FailureCode.M_00_01.value == "no_signifier_before_sound"

    def test_no_leap_code_present(self):
        """M_00_09 no_leap_between_layers is present."""
        assert FailureCode.M_00_09.value == "no_leap_between_layers"

    def test_identity_loss_code_present(self):
        """M_CX_01 identity_loss_on_transition is present."""
        assert FailureCode.M_CX_01.value == "identity_loss_on_transition"

    def test_all_codes_are_strings(self):
        """All failure code values are strings."""
        for code in FailureCode:
            assert isinstance(code.value, str), f"Non-string value for {code.name}"

    def test_codes_unique(self):
        """All failure code values are unique."""
        values = [c.value for c in FailureCode]
        assert len(values) == len(set(values))
