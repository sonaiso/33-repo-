"""Runtime Embargo Readiness Ledger guardrails for PR #65 (docs + tests only)."""

from pathlib import Path


REPO_ROOT = Path(__file__).parent.parent
LEDGER_DOC = REPO_ROOT / "docs" / "17_RUNTIME_EMBARGO_READINESS_LEDGER.md"

REQUIRED_PHRASES = [
    "Runtime Embargo remains active.",
    "Kernel is not authorized.",
    "Decision engine is not authorized.",
    "Coverage matrix runtime is not authorized.",
    "Euclidean Learning remains `AUDIT_SANDBOX_ONLY`.",
    "## Chain state through PR #74",
    "DONE in this ledger means the named prerequisite is complete as audit/schema/contract readiness only.",
    "DONE does not lift Runtime Embargo.",
    "DONE does not authorize `binding_kernel.py`, `decision_engine.py`, `coverage_matrix_v0.1.yaml`, runtime predicates, runtime translators, or computed verdict runtime.",
    "Only an explicit Runtime Embargo Lift PR may authorize runtime.",
    "### DONE",
    "### PARTIAL",
    "### BLOCKED",
    "DAL_ONLY contracts.",
    "LAFZI_FORM contracts.",
    "DalToLafziBridgeSpec declarative-only.",
    "Runtime Embargo Constitution.",
    "FailureAlignment full coverage.",
    "FailureAlignment canonical families / proof policy normalization.",
    "Rejected Runtime Patterns guard.",
    "Canonical runtime artifact blocking.",
    "Legacy `l_protocol` relocation blocked.",
    "Euclidean Learning contained as `AUDIT_SANDBOX_ONLY`.",
    "Euclidean Layer to Domain map audit-only.",
    "TraceStep identity ProofObject-backed.",
    "ProofObject references stable failure policies.",
    "Computed Coverage schema readiness.",
    "`binding_kernel.py`.",
    "`decision_engine.py`.",
    "`coverage_matrix_v0.1.yaml`.",
    "Runtime predicates/translators.",
    "Runtime domain opening.",
    "Kernel/decision authority.",
    "Anti-pattern guard green",
    "| Anti-pattern guard green | DONE |",
    "| Coverage schema readiness | DONE |",
    "| Rejected Runtime Patterns guard | DONE |",
    "| Canonical runtime artifact blocking | DONE |",
    "| Legacy l_protocol relocation blocked | DONE |",
    "| Euclidean Learning containment | DONE |",
    "| Euclidean Layer to Domain map | DONE |",
    "| TraceStep identity ProofObject-backed | PARTIAL |",
    "explicit bool only",
    "| Runtime kernel allowed | NOT AUTHORIZED |",
    "| decision_engine.py allowed | NOT AUTHORIZED |",
    "| coverage_matrix_v0.1.yaml allowed | NOT AUTHORIZED |",
    "| l_protocol runtime relocation allowed | NOT AUTHORIZED |",
    "| runtime predicates/translators allowed | NOT AUTHORIZED |",
    "| runtime domain opening allowed | NOT AUTHORIZED |",
    "Next authorized work is one of:",
    "Computed Coverage Schema Only.",
    "LAFZI-C2 Contract Refinement.",
]

FORBIDDEN_PHRASES = [
    "embargo lifted",
    "runtime authorized",
    "kernel activated",
    "embargo removed",
]

FORBIDDEN_AUTHORIZATION_ROWS = [
    "| Runtime kernel allowed | AUTHORIZED |",
    "| decision_engine.py allowed | AUTHORIZED |",
    "| coverage_matrix_v0.1.yaml allowed | AUTHORIZED |",
    "| l_protocol runtime relocation allowed | AUTHORIZED |",
    "| runtime predicates/translators allowed | AUTHORIZED |",
    "| runtime domain opening allowed | AUTHORIZED |",
]


def test_runtime_embargo_readiness_ledger_exists():
    """trace_ref: docs/12_RUNTIME_EMBARGO_CONSTITUTION.md Embargo Rule."""
    assert LEDGER_DOC.exists(), "Missing runtime embargo readiness ledger document"


def test_runtime_embargo_readiness_ledger_has_required_claims():
    """trace_ref: docs/12_RUNTIME_EMBARGO_CONSTITUTION.md Explicit Prohibitions."""
    content = LEDGER_DOC.read_text(encoding="utf-8")
    for phrase in REQUIRED_PHRASES:
        assert phrase in content, f"Missing required readiness phrase: {phrase}"


def test_runtime_embargo_readiness_ledger_does_not_claim_embargo_lifted():
    """trace_ref: docs/12_RUNTIME_EMBARGO_CONSTITUTION.md Embargo Rule."""
    content = LEDGER_DOC.read_text(encoding="utf-8").casefold()
    for phrase in FORBIDDEN_PHRASES:
        assert phrase.casefold() not in content, (
            f"Forbidden phrase found in readiness ledger: {phrase}"
        )


def test_runtime_embargo_readiness_ledger_does_not_authorize_blocked_runtime_rows():
    """trace_ref: docs/12_RUNTIME_EMBARGO_CONSTITUTION.md Explicit Prohibitions."""
    content = LEDGER_DOC.read_text(encoding="utf-8")
    for row in FORBIDDEN_AUTHORIZATION_ROWS:
        assert row not in content, f"Forbidden authorization row found: {row}"
