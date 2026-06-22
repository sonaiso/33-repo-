"""
Tests for L1 signifier domain contracts.

Origin: docs/00_MAQOOL_CONSTITUTION.md §5 Rule 1
Authority: docs/15_PROJECT_ROADMAP.md Phase 1 (L1 open)
"""
from __future__ import annotations

from typing import get_args

import pytest

from taaqqul_slot_geometry.constitution.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.L1.signifier_domain import (
    AdditiveLetterDomainCertificate,
    MotionDomainCertificate,
    SIGNIFIER_DOMAIN_ORDER,
    SignifierDomain,
    WaqfWaslDomainCertificate,
)


def test_signifier_domain_literal_order_is_complete():
    assert SIGNIFIER_DOMAIN_ORDER == (
        "trace",
        "letter",
        "motion",
        "phonetic_atom",
        "syllable",
        "waqf_wasl",
        "additive_letter",
        "root_stem",
        "minimal_mujarrad",
        "weight",
        "jamid_anchor",
        "event_path",
        "mabni_tool",
        "reference",
        "proper_name",
        "loanword",
        "irab_ready",
    )
    assert get_args(SignifierDomain) == SIGNIFIER_DOMAIN_ORDER


def test_motion_domain_certificate_contract():
    cert = MotionDomainCertificate(
        carrier_letter="ك",
        motion_state="FATHA",
        function="opening",
        trace=("docs/00_MAQOOL_CONSTITUTION.md §5 Rule 2",),
    )
    assert cert.rank == "CANDIDATE"
    assert cert.domain == "motion"


def test_additive_letter_domain_certificate_contract():
    cert = AdditiveLetterDomainCertificate(
        candidate_letter="أ",
        position=0,
        additive_function="hamzat_ziyadah",
        required_origin_certificate="origin:ktb",
        blocked_until_mujarrad_closure=True,
        trace=("docs/00_MAQOOL_CONSTITUTION.md §5 Rule 2",),
    )
    assert cert.rank == "CANDIDATE"
    assert cert.domain == "additive_letter"


def test_waqf_wasl_domain_certificate_contract():
    cert = WaqfWaslDomainCertificate(
        unit="كَتَبْ",
        can_pause=True,
        must_connect=False,
        pause_effect="incidental_sukun",
        connection_effect="restore_motion",
        closure_type="nominal_closure",
        trace=("docs/00_MAQOOL_CONSTITUTION.md §5 Rule 2",),
    )
    assert cert.rank == "CANDIDATE"
    assert cert.domain == "waqf_wasl"


@pytest.mark.parametrize(
    "factory",
    [
        lambda: MotionDomainCertificate(
            carrier_letter="ك",
            motion_state="FATHA",
            function="opening",
            trace=("x",),
            rank="CERTIFIED",  # type: ignore[arg-type]
        ),
        lambda: AdditiveLetterDomainCertificate(
            candidate_letter="أ",
            position=0,
            additive_function="hamzat_ziyadah",
            required_origin_certificate="origin:ktb",
            blocked_until_mujarrad_closure=True,
            trace=("x",),
            rank="CERTIFIED",  # type: ignore[arg-type]
        ),
        lambda: WaqfWaslDomainCertificate(
            unit="كَتَبْ",
            can_pause=True,
            must_connect=False,
            pause_effect="incidental_sukun",
            connection_effect="restore_motion",
            closure_type="nominal_closure",
            trace=("x",),
            rank="CERTIFIED",  # type: ignore[arg-type]
        ),
    ],
)
def test_signifier_certificates_reject_rank_promotion(factory):
    with pytest.raises(ValueError, match=FailureCode.M_01_16.value):
        factory()


def test_additive_letter_requires_mujarrad_closure_gate():
    with pytest.raises(ValueError, match=FailureCode.M_00_22.value):
        AdditiveLetterDomainCertificate(
            candidate_letter="أ",
            position=0,
            additive_function="hamzat_ziyadah",
            required_origin_certificate="origin:ktb",
            blocked_until_mujarrad_closure=False,
            trace=("x",),
        )


def test_waqf_wasl_requires_pause_or_connection():
    with pytest.raises(ValueError, match=FailureCode.M_00_22.value):
        WaqfWaslDomainCertificate(
            unit="كَتَبْ",
            can_pause=False,
            must_connect=False,
            pause_effect="none",
            connection_effect="none",
            closure_type="undetermined",
            trace=("x",),
        )
