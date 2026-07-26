"""Audit-only checks for the formal epistemic system specification.

Origin: docs/66_FORMAL_EPISTEMIC_SYSTEM_SPECIFICATION.md
"""

from pathlib import Path


REPO_ROOT = Path(__file__).parent.parent
SPEC_DOC = REPO_ROOT / "docs" / "66_FORMAL_EPISTEMIC_SYSTEM_SPECIFICATION.md"


def _content() -> str:
    return SPEC_DOC.read_text(encoding="utf-8")


def test_formal_epistemic_spec_exists_and_is_audit_only() -> None:
    """trace_ref: docs/66_FORMAL_EPISTEMIC_SYSTEM_SPECIFICATION.md §Constitutional Status."""
    content = _content()

    assert SPEC_DOC.exists()
    for phrase in (
        "Runtime status: AUDIT_ONLY",
        "L0 is closed.",
        "L1 is contract/audit bounded.",
        "L2 remains locked.",
        "L3 remains locked.",
        "Runtime embargo remains active.",
    ):
        assert phrase in content


def test_spec_separates_theory_system_from_macro_jrc() -> None:
    """trace_ref: docs/66_FORMAL_EPISTEMIC_SYSTEM_SPECIFICATION.md §One Auditable Claim."""
    content = _content()

    for phrase in (
        "`TheorySystem` is a structured epistemic object.",
        "`Macro-JRC` is a readiness predicate over that object.",
        "Internal closure is not external match.",
    ):
        assert phrase in content


def test_spec_declares_core_signatures_relations_and_transitions() -> None:
    """trace_ref: docs/66_FORMAL_EPISTEMIC_SYSTEM_SPECIFICATION.md §Signature and Sorts; §Licensed Transition Functions."""
    content = _content()

    for phrase in (
        "ValidationMode",
        "ValidationResult",
        "MatchResult",
        "LicensedRel(p_i, p_j, r)",
        "InternallyClosed(N)",
        "f_8 : J × J × M_R ⇀ N",
        "f_9 : N × AxiomSet × I × D × O ⇀ T",
        "f_10 : T → {TRUE, FALSE} × Residuals × Trace",
        "f_11 : T × ValidationMode × EvidenceSet → MatchResult",
    ):
        assert phrase in content


def test_spec_preserves_no_leap_identity_and_residual_contracts() -> None:
    """trace_ref: docs/66_FORMAL_EPISTEMIC_SYSTEM_SPECIFICATION.md §Formal Objects; §Licensed Transition Functions; §Anti-Pattern Laws."""
    content = _content()

    for phrase in (
        "Identity(p) = id_p",
        "RoleWithinTheory(p, τ) is relation metadata, not proposition identity.",
        "Residuals(f_8(...)) = Ω_p1 ∪ Ω_p2 ∪ Ω_r",
        "Order(p_1, p_2) ⇏ ENTAILS(p_1, p_2)",
        "Macro-JRC(τ) ⇏ Match(τ, E, D)",
    ):
        assert phrase in content


def test_spec_non_scope_preserves_runtime_embargo_boundaries() -> None:
    """trace_ref: docs/66_FORMAL_EPISTEMIC_SYSTEM_SPECIFICATION.md §Non-scope."""
    content = _content()

    for phrase in (
        "create a runtime kernel",
        "create a decision engine",
        "create a coverage matrix runtime",
        "create runtime predicates or translators",
        "compute runtime verdict authority",
        "open `L2`",
        "open `L3`",
        "open any runtime domain",
        "promote rank above `CANDIDATE`",
    ):
        assert phrase in content

    for forbidden_phrase in (
        "runtime_lift_authorized=True",
        "Rank.CERTIFICATE",
        "ExecutionRank.CERTIFIED",
    ):
        assert forbidden_phrase not in content
