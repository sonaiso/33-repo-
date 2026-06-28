"""Audit-only guard tests for the Licensed Intelligibility Chain Constitution.

Origin: docs/21_LICENSED_INTELLIGIBILITY_CHAIN_CONSTITUTION.md
"""

from pathlib import Path


REPO_ROOT = Path(__file__).parent.parent
CHAIN_DOC = (
    REPO_ROOT / "docs" / "21_LICENSED_INTELLIGIBILITY_CHAIN_CONSTITUTION.md"
)
SRC_ROOT = REPO_ROOT / "src" / "taaqqul_slot_geometry"


def _content() -> str:
    return CHAIN_DOC.read_text(encoding="utf-8")


def test_licensed_intelligibility_chain_is_audit_only() -> None:
    """trace_ref: docs/21 §Constitutional Status."""
    content = _content()

    assert "Runtime status: AUDIT_ONLY" in content
    assert "L0 is closed." in content
    assert "L1 is contract/audit bounded." in content
    assert "L2 remains locked." in content
    assert "L3 remains locked." in content
    assert "Runtime embargo remains active." in content


def test_licensed_intelligibility_chain_preserves_non_scope() -> None:
    """trace_ref: docs/21 §Non-scope."""
    content = _content()

    for phrase in (
        "create an intelligibility runtime engine",
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
        "promote any candidate beyond `CANDIDATE`",
    ):
        assert phrase in content, f"missing non-scope phrase: {phrase!r}"


def test_authority_chain_includes_required_documents() -> None:
    """trace_ref: docs/21 §Authority."""
    content = _content()

    for authority in (
        "docs/00_MAQOOL_CONSTITUTION.md",
        "docs/00A_CONSTITUTIONAL_PROGRAMMING_AMENDMENT.md",
        "docs/12_RUNTIME_EMBARGO_CONSTITUTION.md",
        "docs/13_FAILURE_ALIGNMENT_CONSTITUTION.md",
        "docs/14_EUCLIDEAN_LEARNING_DOMAIN_BOUNDARY.md",
        "docs/15_PROJECT_ROADMAP.md",
        "docs/20_AGENT_AUTONOMY_RUNBOOK.md",
        "docs/58_SUPREME_TASAWWUR_REALITY_LAW.md",
        "docs/61_INDEPENDENT_IFADAH_MODEL_LAW.md",
        "docs/62_HALLUCINATION_LEAP_BARRIER_LAW.md",
    ):
        assert authority in content, f"missing authority: {authority}"


def test_fourteen_licensed_layers_are_enumerated() -> None:
    """trace_ref: docs/21 §The Fourteen Licensed Layers."""
    content = _content()

    layers = (
        ("UtteranceCarrier", "حامل القول"),
        ("SignifierAlone", "الدال وحده"),
        ("SignifierAloneRelation", "نسب الدال وحده"),
        ("LiteralSignified", "المدلول اللفظي"),
        ("LexicalPositedSignified", "المدلول الوضعي المعجمي"),
        ("SignifiedAloneRelation", "نسب المدلول وحده"),
        ("SignifierSignifiedCoupling", "نسبة الدال إلى المدلول"),
        ("Maqam", "المقام"),
        ("CandidateQawliRelation", "النسبة القولية المرشحة"),
        ("LicensedQawliRelation", "النسبة القولية المرخّصة"),
        ("QawlDirection", "جهة القول"),
        ("Ifadah", "الإفادة"),
        ("MantooqIntelligible", "معقول المنطوق"),
        ("MafhoomCandidate", "المفهوم"),
    )

    for english, arabic in layers:
        assert english in content, f"missing layer name: {english}"
        assert arabic in content, f"missing arabic layer name: {arabic}"

    for lic_id in (
        "LIC-01",
        "LIC-02",
        "LIC-03",
        "LIC-04",
        "LIC-05",
        "LIC-06",
        "LIC-07",
        "LIC-08",
        "LIC-09",
        "LIC-10",
        "LIC-11",
        "LIC-12",
        "LIC-13",
        "LIC-14",
    ):
        assert lic_id in content, f"missing layer card id: {lic_id}"


def test_seven_non_substitution_laws_are_recorded() -> None:
    """trace_ref: docs/21 §Non-Substitution Laws."""
    content = _content()

    for law_id in (
        "LIC-LAW-01",
        "LIC-LAW-02",
        "LIC-LAW-03",
        "LIC-LAW-04",
        "LIC-LAW-05",
        "LIC-LAW-06",
        "LIC-LAW-07",
    ):
        assert law_id in content, f"missing non-substitution law id: {law_id}"

    for arabic in (
        "لا طبقة تقوم مقام طبقة.",
        "لا حامل يغني عن الدال.",
        "لا دال ينتج المعجم وحده.",
        "لا مدلول لفظي يساوي الوضع.",
        "لا مقام ينتج الصدق.",
        "لا إفادة تكفي للحكم.",
        "لا مفهوم بلا منطوق محفوظ.",
    ):
        assert arabic in content, f"missing arabic law statement: {arabic}"

    for english in (
        "No layer substitutes for another layer.",
        "No carrier substitutes for a signifier.",
        "No signifier alone produces the lexicon.",
        "No literal signified equals the lexical positing.",
        "No maqam produces truth.",
        "No ifādah suffices for hukm.",
        "No mafhoom exists without a preserved mantooq.",
    ):
        assert english in content, f"missing english law gloss: {english}"


def test_mafhoom_preservation_sub_law_is_recorded() -> None:
    """trace_ref: docs/21 §Mafhoom Preservation Sub-Law."""
    content = _content()

    for phrase in (
        "No mafhoom without preserved mantooq.",
        "No mafhoom contradicts its mantooq.",
        "No mafhoom overrides its mantooq.",
        "مفهوم موافقة",
        "مفهوم مخالفة",
        "مفهوم اقتضاء",
        "مفهوم إشارة",
    ):
        assert phrase in content, f"missing mafhoom phrase: {phrase!r}"


def test_acceptance_and_rejection_examples_cover_required_substitutions() -> None:
    """trace_ref: docs/21 §Acceptance and Rejection Examples."""
    content = _content()

    for phrase in (
        "Carrier does not substitute for signifier",
        "Signifier alone does not produce the lexicon",
        "Literal signified does not equal the lexical positing",
        "Maqam does not produce truth",
        "Ifādah does not suffice for hukm",
        "Mafhoom does not exist without preserved mantooq",
    ):
        assert phrase in content, f"missing example heading: {phrase!r}"


def test_drift_guardrail_blocks_layer_collapses() -> None:
    """trace_ref: docs/21 §Drift Guardrail."""
    content = _content()

    for phrase in (
        "`carrier` must not drift into `signifier`",
        "`signifier` must not drift into `lexicon`",
        "`literal signified` must not drift into `lexical positing`",
        "`lexical positing` must not drift into `usage proves positing`",
        "`coupling` must not drift into `hukm`",
        "`maqam` must not drift into `truth`",
        "`qawli relation candidate` must not drift into `licensed qawli relation`",
        "`licensed qawli relation` must not drift into `ifādah`",
        "`qawl direction` must not drift into `ifādah`",
        "`ifādah` must not drift into `hukm`",
        "`mantooq` must not drift into `mafhoom`",
        "`mafhoom` must not override `mantooq`",
    ):
        assert phrase in content, f"missing drift guardrail: {phrase!r}"


def test_cross_reference_map_binds_prior_laws() -> None:
    """trace_ref: docs/21 §Cross-Reference Map."""
    content = _content()

    for phrase in (
        "docs/58_DAL_ALONE_ATOMIC_CLOSURE_LAW.md",
        "docs/11_LAFZI_FORM_CONSTITUTION.md",
        "docs/60_PATH_CARD_LICENSED_DERIVATION_LAW.md",
        "docs/61_INDEPENDENT_IFADAH_MODEL_LAW.md",
        "docs/62_HALLUCINATION_LEAP_BARRIER_LAW.md",
        "docs/58_SUPREME_TASAWWUR_REALITY_LAW.md",
        "docs/18_RUNTIME_EMBARGO_LIFT_PROTOCOL.md",
    ):
        assert phrase in content, f"missing cross-reference: {phrase}"


def test_final_boundary_preserves_entity_invariants() -> None:
    """trace_ref: docs/21 §Final Boundary Law."""
    content = _content()

    for phrase in (
        "trace_ref",
        'rank = "CANDIDATE"',
        "FailureCode",
        "frozen dataclass",
        "visible residuals",
    ):
        assert phrase in content, f"missing entity invariant: {phrase!r}"


def test_chain_law_does_not_create_locked_layer_source() -> None:
    """trace_ref: docs/20_AGENT_AUTONOMY_RUNBOOK.md §Stop conditions."""
    forbidden = (
        SRC_ROOT / "L2" / "licensed_intelligibility_chain.py",
        SRC_ROOT / "L3" / "licensed_intelligibility_chain.py",
        SRC_ROOT / "runtime" / "licensed_intelligibility_chain.py",
        SRC_ROOT / "runtime" / "mafhoom_engine.py",
        SRC_ROOT / "runtime" / "mantooq_engine.py",
        SRC_ROOT / "runtime" / "ifadah_engine.py",
    )
    for path in forbidden:
        assert not path.exists(), f"forbidden runtime artifact present: {path}"
