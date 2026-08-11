"""Audit-only claim-preserving bounded-transfer contract checks (docs + tests only)."""

from pathlib import Path


REPO_ROOT = Path(__file__).parent.parent
CONTRACT_DOC = REPO_ROOT / "docs" / "68_CLAIM_PRESERVING_BOUNDED_TRANSFER_CONTRACT.md"
EMBARGO_DOC = REPO_ROOT / "docs" / "12_RUNTIME_EMBARGO_CONSTITUTION.md"

REQUIRED_SECTION_MARKERS = [
    "## Constitutional claim (single-goal scope)",
    "## Selected next-safe-step queue item",
    "## Current constitutional bounds",
    "## Scope",
    "## Non-scope",
    "## Authority docs",
    "## Files changed",
    "## Tests run",
    "## Constitutional invariants preserved",
    "## Why this is audit-only",
]

REQUIRED_BOUNDARY_MARKERS = [
    "`Model != Realization != Context != IntendedClass`",
    "`MC_n`",
    "`RA_{n,psi}`",
    "`CandComp_U`",
    "`CtxComp_Gamma`",
    "`ChkSound`",
    "`ChkComp`",
    "`SCM_{psi,tau}(N)`",
    "Finite stability is evidence, not cutoff proof.",
    "Finite quotient count alone is insufficient; finite representatives are also required.",
    "Refutation needs one intended countermodel.",
    "Finite verification of a universal claim needs representation adequacy (`RA_{n,psi}`).",
]

REQUIRED_NON_SCOPE_PROHIBITIONS = [
    "No `binding_kernel.py`, `decision_engine.py`, or `coverage_matrix_v0.1.yaml` changes.",
    "No runtime predicates/translators.",
    "No computed-verdict runtime.",
    "No domain opening and no locked-layer opening.",
]

FORBIDDEN_AUTHORIZATION_PHRASES = [
    "runtime authorized",
    "embargo lifted",
    "kernel activated",
    "decision authority granted",
    "domain opening authorized",
]


def test_claim_preserving_contract_document_exists():
    """trace_ref: docs/15_PROJECT_ROADMAP.md next-safe-step queue."""
    assert CONTRACT_DOC.exists(), "Missing bounded transfer contract document"


def test_claim_preserving_contract_has_required_sections():
    """trace_ref: docs/20_AGENT_AUTONOMY_RUNBOOK.md Required Output Shape."""
    content = CONTRACT_DOC.read_text(encoding="utf-8")
    for marker in REQUIRED_SECTION_MARKERS:
        assert marker in content, f"Missing required section marker: {marker}"


def test_claim_preserving_contract_declares_required_boundaries():
    """trace_ref: docs/00_MAQOOL_CONSTITUTION.md proof-boundary discipline."""
    content = CONTRACT_DOC.read_text(encoding="utf-8")
    for marker in REQUIRED_BOUNDARY_MARKERS:
        assert marker in content, f"Missing bounded-transfer marker: {marker}"


def test_claim_preserving_contract_keeps_runtime_non_scope_explicit():
    """trace_ref: docs/12_RUNTIME_EMBARGO_CONSTITUTION.md Embargo Rule."""
    content = CONTRACT_DOC.read_text(encoding="utf-8")
    for marker in REQUIRED_NON_SCOPE_PROHIBITIONS:
        assert marker in content, f"Missing runtime non-scope marker: {marker}"


def test_claim_preserving_contract_does_not_claim_runtime_authorization():
    """trace_ref: docs/12_RUNTIME_EMBARGO_CONSTITUTION.md Explicit Prohibitions."""
    folded = CONTRACT_DOC.read_text(encoding="utf-8").casefold()
    for phrase in FORBIDDEN_AUTHORIZATION_PHRASES:
        assert phrase not in folded, f"Forbidden runtime authorization phrase found: {phrase}"


def test_runtime_embargo_doc_still_declares_embargo_active():
    """trace_ref: docs/12_RUNTIME_EMBARGO_CONSTITUTION.md Embargo Rule."""
    content = EMBARGO_DOC.read_text(encoding="utf-8")
    assert "Runtime remains embargoed" in content
