"""TraceStep identity proof backing contract checks for PR #66."""

from pathlib import Path


REPO_ROOT = Path(__file__).parent.parent
CONTRACT_DOC = REPO_ROOT / "docs" / "18_TRACESTEP_IDENTITY_PROOF_CONTRACT.md"

FORBIDDEN_CANONICAL_RUNTIME_ARTIFACT_PATHS = (
    REPO_ROOT / "src" / "taaqqul_slot_geometry" / "L1" / "binding_kernel.py",
    REPO_ROOT / "src" / "taaqqul_slot_geometry" / "L1" / "decision_engine.py",
    REPO_ROOT / "coverage_matrix_v0.1.yaml",
    REPO_ROOT / "docs" / "coverage_matrix_v0.1.yaml",
    REPO_ROOT / "data" / "coverage_matrix_v0.1.yaml",
)


def _contract_content() -> str:
    return CONTRACT_DOC.read_text(encoding="utf-8")


def test_tracestep_identity_proof_contract_doc_exists():
    """trace_ref: docs/08_PROOF_OBJECT_CONSTITUTION.md Core Law."""
    assert CONTRACT_DOC.exists(), "Missing TraceStep identity proof contract"


def test_contract_requires_proof_object_or_identity_proof_reference():
    """trace_ref: docs/08_PROOF_OBJECT_CONSTITUTION.md Core Law."""
    content = _contract_content()
    assert "TraceStepIdentityProofRequirement" in content
    assert "contract term only" in content
    assert "`IdentityProof` reference" in content
    assert "`ProofObject` reference" in content
    assert "preserved_identity_refs" in content


def test_contract_rejects_boolean_as_tracestep_identity_proof():
    """trace_ref: docs/08_PROOF_OBJECT_CONSTITUTION.md Forbidden substitutions."""
    content = _contract_content()
    assert "TraceStep identity cannot be proven by Boolean fields." in content
    assert "`identity_preserved=True` cannot prove identity preservation." in content
    assert "`is_preserved=True` cannot prove identity preservation." in content
    assert "Implicit identity preservation is forbidden." in content


def test_contract_keeps_ledger_partial_until_implementation():
    """trace_ref: docs/17_RUNTIME_EMBARGO_READINESS_LEDGER.md Readiness table."""
    content = _contract_content()
    assert "TraceStep identity ProofObject-backed | PARTIAL | explicit bool only" in content
    assert "Missing `IdentityProof` or `ProofObject` reference" in content
    assert "This PR does not update the runtime ledger to DONE." in content


def test_contract_declares_runtime_embargo_active():
    """trace_ref: docs/12_RUNTIME_EMBARGO_CONSTITUTION.md Embargo Rule."""
    content = _contract_content()
    assert "Runtime Embargo remains active." in content
    assert "Kernel is not authorized." in content
    assert "Decision engine is not authorized." in content
    assert "Coverage matrix runtime is not authorized." in content


def test_forbidden_runtime_artifacts_absent_from_canonical_paths():
    """trace_ref: docs/12_RUNTIME_EMBARGO_CONSTITUTION.md Explicit Prohibitions."""
    matches = [
        path
        for path in FORBIDDEN_CANONICAL_RUNTIME_ARTIFACT_PATHS
        if path.exists()
    ]

    assert not matches, "Forbidden runtime artifacts exist:\n" + "\n".join(
        str(path.relative_to(REPO_ROOT)) for path in matches
    )
