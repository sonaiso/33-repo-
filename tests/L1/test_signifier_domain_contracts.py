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
    DomainCertificate,
    INDEPENDENT_ENTRY_DOMAINS,
    ManiCheck,
    MotionDomainCertificate,
    SIGNIFIER_DOMAIN_ORDER,
    SIGNIFIER_DOMAIN_TRANSITIONS,
    SignifierDomain,
    WaqfWaslDomainCertificate,
    domain_relation,
    license_domain,
    next_signifier_domains,
    previous_signifier_domains,
    previous_signifier_domain,
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


def test_signifier_domain_transition_registry_is_complete():
    assert set(SIGNIFIER_DOMAIN_TRANSITIONS) == set(SIGNIFIER_DOMAIN_ORDER)


def test_previous_and_next_domain_links():
    assert previous_signifier_domain("weight") == "minimal_mujarrad"
    assert previous_signifier_domain("syllable") == "phonetic_atom"
    assert previous_signifier_domains("root_stem") == ("syllable", "waqf_wasl")
    assert previous_signifier_domain("root_stem") is None
    assert next_signifier_domains("weight") == ("jamid_anchor", "event_path")
    assert next_signifier_domains("irab_ready") == tuple()


def test_mabni_tool_is_formally_independent_entry_domain():
    assert "mabni_tool" in INDEPENDENT_ENTRY_DOMAINS
    assert previous_signifier_domains("mabni_tool") == tuple()


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


def test_license_domain_blocks_when_origin_missing():
    cert = license_domain(
        domain="motion",
        origin_certificate="",
        sabab="carrier-licensed",
        mani_checks=tuple(),
        trace=("x",),
    )
    assert cert.status == "blocked"
    assert cert.status_reason == "blocked_origin_missing"
    assert cert.allowed_next_domains == tuple()


def test_license_domain_blocks_when_origin_is_whitespace_only():
    cert = license_domain(
        domain="motion",
        origin_certificate="   ",
        sabab="carrier-licensed",
        mani_checks=tuple(),
        trace=("x",),
    )
    assert cert.status == "blocked"
    assert cert.status_reason == "blocked_origin_missing"
    assert cert.allowed_next_domains == tuple()


def test_license_domain_blocks_when_sabab_missing():
    cert = license_domain(
        domain="motion",
        origin_certificate="origin:letter",
        sabab="",
        mani_checks=tuple(),
        trace=("x",),
    )
    assert cert.status == "blocked"
    assert cert.status_reason == "blocked_domain_without_sabab"
    assert cert.allowed_next_domains == tuple()


def test_license_domain_blocks_when_sabab_is_whitespace_only():
    cert = license_domain(
        domain="motion",
        origin_certificate="origin:letter",
        sabab="   ",
        mani_checks=tuple(),
        trace=("x",),
    )
    assert cert.status == "blocked"
    assert cert.status_reason == "blocked_domain_without_sabab"
    assert cert.allowed_next_domains == tuple()


def test_license_domain_blocks_when_mani_blocker_exists():
    cert = license_domain(
        domain="weight",
        origin_certificate="origin:root",
        sabab="licensed-root-to-pattern",
        mani_checks=(
            ManiCheck(residual_code="mani_weight_without_root", severity="blocker", trace=("x",)),
        ),
        trace=("x",),
    )
    assert cert.status == "blocked"
    assert cert.status_reason == "blocked_by_mani"
    assert cert.allowed_next_domains == tuple()


def test_license_domain_provisional_with_warning_residuals():
    cert = license_domain(
        domain="root_stem",
        origin_certificate="origin:syllable",
        sabab="licensed-carrier-order",
        mani_checks=(
            ManiCheck(
                residual_code="mani_weak_letter_review",
                severity="warning",
                trace=("x",),
            ),
        ),
        trace=("x",),
    )
    assert cert.status == "provisional"
    assert cert.status_reason == "none"
    assert cert.allowed_next_domains == ("minimal_mujarrad", "proper_name", "loanword")


def test_license_domain_closed_links_previous_and_next_relations():
    cert = license_domain(
        domain="weight",
        origin_certificate="origin:minimal-mujarrad",
        sabab="licensed-root-pattern-projection",
        mani_checks=tuple(),
        trace=("x",),
    )
    assert isinstance(cert, DomainCertificate)
    assert cert.status == "closed"
    assert cert.relation.previous_domains == ("minimal_mujarrad",)
    assert cert.relation.next_domains == ("jamid_anchor", "event_path")
    assert cert.relation.relation_previous_to_next == (
        "minimal_mujarrad_to_jamid_anchor_via_weight",
        "minimal_mujarrad_to_event_path_via_weight",
    )


def test_domain_certificate_rejects_blocked_with_next_permissions():
    with pytest.raises(ValueError, match=FailureCode.M_CX_04.value):
        DomainCertificate(
            domain="motion",
            origin_certificate="origin:letter",
            sabab="licensed-motion",
            mani_residuals=tuple(),
            boundary_declared=True,
            relation=domain_relation(domain="motion", trace=("x",)),
            trace=("x",),
            status="blocked",
            status_reason="blocked_by_mani",
            allowed_next_domains=("phonetic_atom",),
        )


def test_domain_certificate_rejects_closed_with_blank_origin_or_sabab():
    with pytest.raises(ValueError, match=FailureCode.M_00_22.value):
        DomainCertificate(
            domain="motion",
            origin_certificate="   ",
            sabab="licensed-motion",
            mani_residuals=tuple(),
            boundary_declared=True,
            relation=domain_relation(domain="motion", trace=("x",)),
            trace=("x",),
            status="closed",
            status_reason="none",
            allowed_next_domains=("phonetic_atom",),
        )
    with pytest.raises(ValueError, match=FailureCode.M_00_22.value):
        DomainCertificate(
            domain="motion",
            origin_certificate="origin:letter",
            sabab="   ",
            mani_residuals=tuple(),
            boundary_declared=True,
            relation=domain_relation(domain="motion", trace=("x",)),
            trace=("x",),
            status="provisional",
            status_reason="none",
            allowed_next_domains=("phonetic_atom",),
        )


def test_domain_certificate_requires_none_status_reason_when_non_blocked():
    with pytest.raises(ValueError, match=FailureCode.M_CX_04.value):
        DomainCertificate(
            domain="motion",
            origin_certificate="origin:letter",
            sabab="licensed-motion",
            mani_residuals=tuple(),
            boundary_declared=True,
            relation=domain_relation(domain="motion", trace=("x",)),
            trace=("x",),
            status="closed",
            status_reason="blocked_by_mani",
            allowed_next_domains=("phonetic_atom",),
        )
