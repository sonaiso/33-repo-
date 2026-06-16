"""
Tests for HarfMaani — Arabic particles.
Origin: docs/01_L0_PHONETIC_BOUNDARY.md BL-L0-07
"""
import pytest

from tests.conftest import ConstitutionalChainTestCase
from taaqqul_slot_geometry.L0.harf_maani import (
    HARF_MAANI_TABLE,
    HarfMaani,
    get_harf,
)
from taaqqul_slot_geometry.constitution.failure_taxonomy import FailureCode


class TestHarfMaaniClosed(ConstitutionalChainTestCase):
    """Origin: docs/01_L0_PHONETIC_BOUNDARY.md BL-L0-07"""

    def test_particle_table_nonempty(self):
        """Particle table contains at least the canonical particles."""
        assert len(HARF_MAANI_TABLE) >= 10

    def test_get_harf_wa(self):
        """'wa' particle can be retrieved."""
        h = get_harf("wa")
        assert h.name == "wa"

    def test_get_harf_unknown_rejected(self):
        """M-00-08: Unknown particle name must be rejected."""
        with pytest.raises(ValueError) as exc_info:
            get_harf("UNKNOWN_PARTICLE")
        assert FailureCode.M_00_08.value in str(exc_info.value)

    def test_harf_trace_ref_present(self):
        """Rule 2: trace_ref present on every particle."""
        for h in HARF_MAANI_TABLE:
            assert h.trace_ref, f"Missing trace_ref on particle {h.name!r}"

    def test_harf_rank_is_candidate(self):
        """Rule 2: rank is CANDIDATE on every particle."""
        for h in HARF_MAANI_TABLE:
            assert h.rank == "CANDIDATE", f"Wrong rank on particle {h.name!r}"

    def test_harf_residuals_present(self):
        """Rule 2: residuals is frozenset on every particle."""
        for h in HARF_MAANI_TABLE:
            assert isinstance(h.residuals, frozenset)

    def test_harf_frozen(self):
        """Rule 3: HarfMaani must be frozen."""
        h = get_harf("wa")
        with pytest.raises((AttributeError, TypeError)):
            h.name = "x"  # type: ignore[misc]

    def test_sukun_particles(self):
        """BL-L0-07: Most particles are built on sukun."""
        sukun_particles = [h for h in HARF_MAANI_TABLE if h.is_built_on_sukun]
        assert len(sukun_particles) >= 5

    def test_empty_phonetic_form_rejected(self):
        """M-00-25: Empty phonetic_form must be rejected."""
        with pytest.raises(ValueError) as exc_info:
            HarfMaani(
                name="wa",
                arabic_form="وَ",
                phonetic_form="",
                function="conjunction",
            )
        assert FailureCode.M_00_25.value in str(exc_info.value)

    def test_empty_function_rejected(self):
        """M-00-08: Empty function must be rejected."""
        with pytest.raises(ValueError) as exc_info:
            HarfMaani(
                name="wa",
                arabic_form="وَ",
                phonetic_form="wa",
                function="",
            )
        assert FailureCode.M_00_08.value in str(exc_info.value)

    def test_canonical_particles_present(self):
        """Canonical particles wa, fa, bi, li, min are all present."""
        by_name = {h.name for h in HARF_MAANI_TABLE}
        for expected in ("wa", "fa", "bi", "li", "min"):
            assert expected in by_name, f"Missing canonical particle {expected!r}"
