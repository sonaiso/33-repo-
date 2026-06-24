"""Runtime Embargo Lift Protocol guardrails (docs + tests only)."""

from pathlib import Path


REPO_ROOT = Path(__file__).parent.parent
PROTOCOL_DOC = REPO_ROOT / "docs" / "18_RUNTIME_EMBARGO_LIFT_PROTOCOL.md"

REQUIRED_PHRASES = [
    "Readiness is not lift.",
    "DONE in readiness ledger is not lift.",
    "Only explicit Runtime Embargo Lift PR may authorize runtime.",
    "Implicit lift is forbidden.",
    "Partial/blanket lift is forbidden.",
    "Lift PR must name exact authorized artifacts/files.",
    "Lift PR must include rollback plan.",
    "Lift PR must include negative tests.",
    "Lift does not auto-open LEXICAL_MADLUL/RELATION/IFADAH/HUKM/TANZIL.",
    "Runtime Embargo remains active.",
    "This PR defines authorization protocol only; it does not grant runtime execution authority.",
    "`binding_kernel.py` remains forbidden unless explicitly authorized by a Runtime Embargo Lift PR.",
    "`Rank.CERTIFICATE`",
    "`Rank.REJECTED`",
    "`domain_proved: true`",
    "`unit_proved: true`",
    "`identity_preserved: true`",
    "`trace_preserved: true`",
    "`gate_passed: true`",
    "`is_preserved: true`",
    "evidence list as proof",
    "domain opening without bridge",
]

FORBIDDEN_PHRASES = [
    "runtime embargo is lifted",
    "runtime embargo lifted now",
    "binding_kernel.py is authorized",
    "decision_engine.py is authorized",
    "coverage_matrix_v0.1.yaml is authorized",
]


def test_runtime_embargo_lift_protocol_doc_exists():
    """trace_ref: docs/12_RUNTIME_EMBARGO_CONSTITUTION.md Embargo Rule."""
    assert PROTOCOL_DOC.exists(), "Missing runtime embargo lift protocol document"


def test_runtime_embargo_lift_protocol_required_phrases():
    """trace_ref: docs/12_RUNTIME_EMBARGO_CONSTITUTION.md Explicit Prohibitions."""
    content = PROTOCOL_DOC.read_text(encoding="utf-8")
    for phrase in REQUIRED_PHRASES:
        assert phrase in content, f"Missing required protocol phrase: {phrase}"


def test_runtime_embargo_lift_protocol_forbidden_phrases_absent():
    """trace_ref: docs/12_RUNTIME_EMBARGO_CONSTITUTION.md Embargo Rule."""
    content = PROTOCOL_DOC.read_text(encoding="utf-8").casefold()
    for phrase in FORBIDDEN_PHRASES:
        assert phrase.casefold() not in content, f"Forbidden phrase found: {phrase}"
