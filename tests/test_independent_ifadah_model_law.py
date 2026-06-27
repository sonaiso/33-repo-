"""Audit-only boundary checks for the independent ifadah model law.

Origin: docs/61_INDEPENDENT_IFADAH_MODEL_LAW.md
"""
from pathlib import Path


REPO_ROOT = Path(__file__).parent.parent
IFADAH_DOC = REPO_ROOT / "docs" / "61_INDEPENDENT_IFADAH_MODEL_LAW.md"
SRC_ROOT = REPO_ROOT / "src" / "taaqqul_slot_geometry"


def _content() -> str:
    return IFADAH_DOC.read_text(encoding="utf-8")


def test_independent_ifadah_model_is_audit_only_boundary() -> None:
    """trace_ref: docs/61_INDEPENDENT_IFADAH_MODEL_LAW.md §Constitutional Status."""
    content = _content()

    assert "Runtime status: AUDIT_ONLY" in content
    assert "D5_IFADAH boundary guidance only" in content
    assert "L2 remains locked." in content
    assert "L3 remains locked." in content
    assert "Runtime embargo remains active." in content


def test_ifadah_model_preserves_non_scope_boundaries() -> None:
    """trace_ref: docs/61_INDEPENDENT_IFADAH_MODEL_LAW.md §Non-scope."""
    content = _content()

    for phrase in (
        "prove truth",
        "issue hukm",
        "issue tanzil",
        "create yaqīn",
        "certify reality",
        "create a decision engine",
        "create runtime predicates",
        "create runtime translators",
        "open `D5_IFADAH` as a runtime domain",
        "open `L2` or `L3`",
    ):
        assert phrase in content


def test_eight_initial_utterance_types_are_recorded() -> None:
    """trace_ref: docs/61_INDEPENDENT_IFADAH_MODEL_LAW.md §Eight Initial Utterance Types."""
    content = _content()

    for arabic_type in ("خبر", "طلب", "سؤال", "نداء", "شرط", "جواب", "دعاء", "زجر"):
        assert arabic_type in content


def test_four_ifadah_audit_outcomes_are_non_runtime_labels() -> None:
    """trace_ref: docs/61_INDEPENDENT_IFADAH_MODEL_LAW.md §Four Ifadah Audit Outcomes."""
    content = _content()

    for outcome in (
        "COMPLETE_IFADAH",
        "MAQAMI_COMPLETE_IFADAH",
        "SUSPENDED_IFADAH",
        "NO_IFADAH",
    ):
        assert outcome in content

    assert "These labels are audit outcomes only." in content
    assert "not computed verdicts" in content
    assert "not authorize a runtime evaluator" in content


def test_acceptance_and_rejection_examples_cover_required_guardrails() -> None:
    """trace_ref: docs/61_INDEPENDENT_IFADAH_MODEL_LAW.md §Acceptance and Rejection Examples."""
    content = _content()

    for phrase in (
        "Condition without answer",
        "Address without addressee",
        "Unknown reference",
        "Answer that misses the question",
        "Mental possibility alone is not a license.",
        "The maqam does not create ifadah from nothing.",
    ):
        assert phrase in content


def test_ifadah_model_does_not_create_locked_layer_source() -> None:
    """trace_ref: docs/20_AGENT_AUTONOMY_RUNBOOK.md §Stop conditions."""
    assert not (SRC_ROOT / "L2" / "ifadah_model.py").exists()
    assert not (SRC_ROOT / "L3" / "ifadah_model.py").exists()
