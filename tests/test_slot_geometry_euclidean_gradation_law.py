"""Audit-only checks for Slot Geometry Euclidean Gradation law.

Origin: docs/63_SLOT_GEOMETRY_EUCLIDEAN_GRADATION_LAW.md
"""

from pathlib import Path


REPO_ROOT = Path(__file__).parent.parent
LAW_DOC = REPO_ROOT / "docs" / "63_SLOT_GEOMETRY_EUCLIDEAN_GRADATION_LAW.md"
SRC_ROOT = REPO_ROOT / "src" / "taaqqul_slot_geometry"


def _content() -> str:
    return LAW_DOC.read_text(encoding="utf-8")


def test_slot_geometry_gradation_law_exists_and_is_audit_only() -> None:
    """trace_ref: docs/63_SLOT_GEOMETRY_EUCLIDEAN_GRADATION_LAW.md §Constitutional Status."""
    content = _content()

    assert LAW_DOC.exists()
    assert "Runtime status: AUDIT_ONLY" in content
    assert "L0 is closed." in content
    assert "L1 is contract/audit bounded." in content
    assert "L2 remains locked." in content
    assert "L3 remains locked." in content
    assert "Runtime embargo remains active." in content


def test_slot_geometry_is_layered_contract_not_table() -> None:
    """trace_ref: docs/63_SLOT_GEOMETRY_EUCLIDEAN_GRADATION_LAW.md §One Auditable Claim."""
    content = _content()

    for phrase in (
        "Slot Geometry is not a table of static slots.",
        "It is a layered contract system",
        "GPT-answer reasonableness verification",
        "Linguistic analysis is therefore a condition of possibility",
        "It is not an independent final objective.",
    ):
        assert phrase in content


def test_eight_contract_questions_are_required() -> None:
    """trace_ref: docs/63_SLOT_GEOMETRY_EUCLIDEAN_GRADATION_LAW.md §The Eight Contract Questions."""
    content = _content()

    for phrase in (
        "ConditionOfPossibility",
        "MinimumCompleteLimit",
        "Opening",
        "Demand",
        "IdentityPreservation",
        "Closure",
        "Residual",
        "LicensedTransition",
        "شرط الإمكان",
        "الحد الأدنى المكتمل",
        "حفظ الهوية",
        "الانتقال المرخّص",
    ):
        assert phrase in content


def test_non_scope_preserves_runtime_embargo_and_locked_layers() -> None:
    """trace_ref: docs/63_SLOT_GEOMETRY_EUCLIDEAN_GRADATION_LAW.md §Non-scope."""
    content = _content()

    for phrase in (
        "create a runtime engine",
        "create a decision engine",
        "create a runtime kernel",
        "create a coverage matrix",
        "create a runtime predicate",
        "create a runtime translator",
        "compute verdicts",
        "open `L2`",
        "open `L3`",
        "open any runtime domain",
        "issue hukm",
        "certify truth",
        "create yaqīn",
        "promote rank above `CANDIDATE`",
    ):
        assert phrase in content


def test_chains_are_recorded_without_opening_later_layers() -> None:
    """trace_ref: docs/63_SLOT_GEOMETRY_EUCLIDEAN_GRADATION_LAW.md §Foundational chains."""
    content = _content()

    for phrase in (
        "LetterWithVowel",
        "WaqfWasl",
        "Syllable",
        "RootOrAugmentCandidate",
        "WeightCandidate",
        "GenusCandidate",
        "SentenceCandidate",
        "RelationCandidate",
        "IfadahCandidate",
        "HukmCandidate",
        "TruthCandidate",
        "YaqinCandidate",
        "The chain above does not open L2, L3, or runtime.",
    ):
        assert phrase in content


def test_needgate_boundary_is_explicit() -> None:
    """trace_ref: docs/63_SLOT_GEOMETRY_EUCLIDEAN_GRADATION_LAW.md §NeedGate Boundary."""
    content = _content()

    for phrase in (
        "No morphology, syntax, semantics, relation analysis",
        "Each opening requires a verification need",
        "specific GPT claim under review",
        "Analysis is demand-driven by the verification need, not exhaustive.",
    ):
        assert phrase in content


def test_antipromotion_rules_are_explicit() -> None:
    """trace_ref: docs/63_SLOT_GEOMETRY_EUCLIDEAN_GRADATION_LAW.md §Anti-promotion Rules."""
    content = _content()

    for phrase in (
        "LetterWithVowel ⇏ Word",
        "Syllable ⇏ Meaning",
        "Weight ⇏ Hukm",
        "Ifadah ⇏ Truth",
        "Information ⇏ Truth",
        "Probability ⇏ Yaqin",
        "Context ⇏ Proof",
        "EvidenceList ⇏ Proof",
        "HiddenResidual ⇏ Closure",
        "Candidate ⇏ LicensedTransition",
    ):
        assert phrase in content


def test_slot_geometry_law_does_not_create_locked_layer_or_runtime_source() -> None:
    """trace_ref: docs/20_AGENT_AUTONOMY_RUNBOOK.md §Stop conditions."""
    forbidden_paths = (
        SRC_ROOT / "L2" / "slot_geometry.py",
        SRC_ROOT / "L3" / "slot_geometry.py",
        SRC_ROOT / "runtime" / "slot_geometry.py",
        SRC_ROOT / "runtime" / "decision_engine.py",
        SRC_ROOT / "runtime" / "binding_kernel.py",
    )

    for path in forbidden_paths:
        assert not path.exists()
