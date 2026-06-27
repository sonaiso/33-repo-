"""Audit-only barrier checks for hallucination leap law.

Origin: docs/62_HALLUCINATION_LEAP_BARRIER_LAW.md
"""

from pathlib import Path


REPO_ROOT = Path(__file__).parent.parent
HALLUCINATION_DOC = REPO_ROOT / "docs" / "62_HALLUCINATION_LEAP_BARRIER_LAW.md"
SRC_ROOT = REPO_ROOT / "src" / "taaqqul_slot_geometry"


def _content() -> str:
    return HALLUCINATION_DOC.read_text(encoding="utf-8")


def test_hallucination_leap_barrier_is_audit_only() -> None:
    """trace_ref: docs/62_HALLUCINATION_LEAP_BARRIER_LAW.md §Constitutional Status."""
    content = _content()

    assert "Runtime status: AUDIT_ONLY" in content
    assert "L0 is closed." in content
    assert "L1 is contract/audit bounded." in content
    assert "L2 remains locked." in content
    assert "L3 remains locked." in content
    assert "Runtime embargo remains active." in content


def test_hallucination_leap_barrier_preserves_non_scope() -> None:
    """trace_ref: docs/62_HALLUCINATION_LEAP_BARRIER_LAW.md §Non-scope."""
    content = _content()

    for phrase in (
        "create a hallucination detector",
        "create a runtime predicate",
        "create a runtime translator",
        "create a decision engine",
        "create a runtime kernel",
        "create a coverage matrix",
        "create or accept a computed verdict",
        "open `L2`",
        "open `L3`",
        "open any runtime domain",
        "issue hukm",
        "create yaqīn",
        "certify truth",
    ):
        assert phrase in content


def test_prohibited_promotion_chain_is_recorded() -> None:
    """trace_ref: docs/62_HALLUCINATION_LEAP_BARRIER_LAW.md §One Auditable Claim."""
    content = _content()

    for phrase in (
        "A candidate is not hallucination while declared as candidate.",
        "StatisticalCandidate",
        "LicensedSlotFill",
        "Ifādah",
        "Hukm",
        "Yaqīn",
        "Every arrow in the chain requires a declared slot",
    ):
        assert phrase in content


def test_ten_hallucination_leap_barriers_are_mapped() -> None:
    """trace_ref: docs/62_HALLUCINATION_LEAP_BARRIER_LAW.md §Ten Hallucination Leap Barriers."""
    content = _content()

    for barrier_id in (
        "HLB-01",
        "HLB-02",
        "HLB-03",
        "HLB-04",
        "HLB-05",
        "HLB-06",
        "HLB-07",
        "HLB-08",
        "HLB-09",
        "HLB-10",
    ):
        assert barrier_id in content

    for phrase in (
        "Candidate without slot",
        "Invented slot",
        "Answer misses question focus",
        "Reference without referent",
        "Deletion without qarīnah",
        "Maqam creates from nothing",
        "Ifādah equals truth",
        "Probability equals yaqīn",
        "Domain crossing without bridge",
        "Hidden residual",
        "Required slot",
        "License condition",
        "Blocker",
        "Residual required",
        "Forbidden promotion phrase",
        "FailureCode family",
    ):
        assert phrase in content


def test_acceptance_rejection_examples_cover_required_guardrails() -> None:
    """trace_ref: docs/62_HALLUCINATION_LEAP_BARRIER_LAW.md §Acceptance and Rejection Examples."""
    content = _content()

    for phrase in (
        "This is not hallucination while the candidate remains openly ranked as a",
        "Ifādah ≠ Truth.",
        "Ifādah is not hukm.",
        "Ifādah is not yaqīn.",
        "Probability ≠ Yaqīn.",
        "Maqam closes licensed gap, does not create from nothing.",
        "A hidden residual is breach independent of the evidential weakness",
    ):
        assert phrase in content


def test_rank_label_drift_guardrails_are_explicit() -> None:
    """trace_ref: docs/62_HALLUCINATION_LEAP_BARRIER_LAW.md §Rank Label Clarification."""
    content = _content()

    for phrase in (
        "Audit labels such as `LICENSED` may appear only as local audit vocabulary",
        "does not mean truth, hukm, yaqīn",
        "`candidate` must not drift into `licensed` unless the license is named",
        "`probable` must not drift into `certain`",
        "`context suggests` must not drift into `context proves`",
        "`evidence list exists` must not drift into `evidence proves`",
        "`ifādah` must not drift into `truth`",
        "a missing residual must not be treated as closure",
    ):
        assert phrase in content


def test_hallucination_barrier_law_does_not_create_locked_layer_source() -> None:
    """trace_ref: docs/20_AGENT_AUTONOMY_RUNBOOK.md §Stop conditions."""
    assert not (SRC_ROOT / "L2" / "hallucination_detector.py").exists()
    assert not (SRC_ROOT / "L3" / "hallucination_detector.py").exists()
    assert not (SRC_ROOT / "runtime" / "hallucination_detector.py").exists()
