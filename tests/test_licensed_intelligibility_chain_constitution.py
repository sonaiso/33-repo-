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
    """trace_ref: docs/21 §0 Constitutional Status."""
    content = _content()

    assert "Runtime status: AUDIT_ONLY" in content
    assert "L0 is closed." in content
    assert "L1 is contract/audit bounded." in content
    assert "L2 remains locked." in content
    assert "L3 remains locked." in content
    assert "Runtime embargo remains active." in content
    assert "Audit-only constitutional chain." in content


def test_non_scope_blocks_runtime_kernel_decision_engine() -> None:
    """trace_ref: docs/21 §0 Non-scope."""
    content = _content()

    for phrase in (
        "No runtime.",
        "No kernel.",
        "No decision engine.",
        "No coverage matrix.",
        "No predicates.",
        "No translators.",
        "No domain opening.",
        "No rank promotion.",
        "No hukm.",
        "No yaqīn.",
        "No truth certification.",
        "binding_kernel.py",
        "decision_engine.py",
        "coverage_matrix_v0.1.yaml",
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
        "docs/18_RUNTIME_EMBARGO_LIFT_PROTOCOL.md",
        "docs/20_AGENT_AUTONOMY_RUNBOOK.md",
        "docs/58_DAL_ALONE_ATOMIC_CLOSURE_LAW.md",
        "docs/58_SUPREME_TASAWWUR_REALITY_LAW.md",
        "docs/60_PATH_CARD_LICENSED_DERIVATION_LAW.md",
        "docs/61_INDEPENDENT_IFADAH_MODEL_LAW.md",
        "docs/62_HALLUCINATION_LEAP_BARRIER_LAW.md",
    ):
        assert authority in content, f"missing authority: {authority}"


def test_supreme_law_states_no_substitution_and_universal_guard() -> None:
    """trace_ref: docs/21 §1 Supreme Law."""
    content = _content()

    for phrase in (
        "لا تقوم طبقة مقام طبقة أخرى.",
        "كل طبقة تحفظ ما قبلها ولا تدّعي ما بعدها.",
        "المعقولية المرخّصة حارس كل انتقال، لا مرحلة تنتهي.",
        "No layer substitutes for another layer.",
        "Licensed intelligibility is a universal guard over every transition",
        "LicensedTransition(A → B) iff",
        "Identity(A) ⊆ Identity(B)",
        "ReverseTest(B → A) does not break origin",
    ):
        assert phrase in content, f"missing supreme-law phrase: {phrase!r}"


def test_transition_audit_fields_are_complete() -> None:
    """trace_ref: docs/21 §0 transition fields."""
    content = _content()

    for field in (
        "Origin",
        "Branch",
        "Sabab",
        "Condition",
        "Mani",
        "EffectiveAttribute",
        "QadihDifferenceCheck",
        "IdentityPreservation",
        "ResidualPolicy",
        "ProofTrace",
        "ReverseTest",
    ):
        assert field in content, f"missing transition audit field: {field}"


def test_full_s0_to_s13_chain_is_enumerated_in_order() -> None:
    """trace_ref: docs/21 §2 The Atomic Chain."""
    content = _content()

    stages = (
        ("S0", "SpeechCarrier", "حامل القول"),
        ("S1", "DalOnly", "الدال وحده"),
        ("S2", "InternalDalRelations", "نسب الدال وحده"),
        ("S3", "LafziForm", "الصورة اللفظية"),
        ("S4", "LexicalMadlul", "المدلول الوضعي المعجمي"),
        ("S5", "InternalMadlulRelations", "نسب داخل المدلول وحده"),
        ("S6", "DalMadlulCoupling", "نسبة الدال إلى المدلول"),
        ("S7", "Maqam", "المقام"),
        ("S8", "CandidateQawliRelation", "النسبة القولية المرشحة"),
        ("S9", "LicensedQawliRelation", "النسبة القولية المرخّصة"),
        ("S10", "QawlDirection", "جهة القول"),
        ("S11", "Ifadah", "الإفادة"),
        ("S12", "MantooqIntelligible", "معقول المنطوق"),
        ("S13", "Mafhoom", "المفهوم"),
    )

    for stage_id, english, arabic in stages:
        assert stage_id in content, f"missing stage id: {stage_id}"
        assert english in content, f"missing english stage name: {english}"
        assert arabic in content, f"missing arabic stage name: {arabic}"
    # Strict ordering across S0..S13 in the document:
    indices = [content.find(f"\n{stage_id} ") for stage_id, _, _ in stages]
    for i, idx in enumerate(indices):
        assert idx != -1, f"stage {stages[i][0]} not found as a chain line"
    assert indices == sorted(indices), "S0..S13 must appear in strict order"


def test_each_stage_has_a_section_heading() -> None:
    """trace_ref: docs/21 §3..§16."""
    content = _content()

    for heading in (
        "## 3. S0 — SpeechCarrier",
        "## 4. S1 — DalOnly",
        "## 5. S2 — InternalDalRelations",
        "## 6. S3 — LafziForm",
        "## 7. S4 — LexicalMadlul",
        "## 8. S5 — InternalMadlulRelations",
        "## 9. S6 — DalMadlulCoupling",
        "## 10. S7 — Maqam",
        "## 11. S8 — CandidateQawliRelation",
        "## 12. S9 — LicensedQawliRelation",
        "## 13. S10 — QawlDirection",
        "## 14. S11 — Ifadah",
        "## 15. S12 — MantooqIntelligible",
        "## 16. S13 — Mafhoom",
    ):
        assert heading in content, f"missing stage section heading: {heading!r}"


def test_mutabaqah_tadammun_iltizam_section_blocks_hukm() -> None:
    """trace_ref: docs/21 §9 DalMadlulCoupling."""
    content = _content()

    for phrase in (
        "Mutabaqah (المطابقة)",
        "Tadammun (التضمن)",
        "Iltizam (الالتزام)",
        "المطابقة والتضمن والالتزام شروط إمكان للفهم الدلالي.",
        "وليست موجبات للحكم.",
        "فهم تمام ما وضع له اللفظ.",
        "فهم الجزء الداخل في الموضوع له.",
        "فهم لازم مرخّص خارج الموضوع له.",
        "المطابقة لا تعني الصدق.",
        "المطابقة لا تعني الحكم.",
        "التضمن لا يستخرج جزءًا موهومًا.",
        "الالتزام لا يولّد حكمًا بلا دليل.",
        "ولا يساوي يقينًا.",
    ):
        assert phrase in content, f"missing coupling phrase: {phrase!r}"


def test_maqam_laws_forbid_truth_and_creation_from_nothing() -> None:
    """trace_ref: docs/21 §10 Maqam."""
    content = _content()

    for phrase in (
        "المقام لا يخلق الدلالة من العدم.",
        "المقام يشغّل دلالة محفوظة.",
        "المقام لا ينتج الصدق.",
        "المقام لا يغلق بقايا غير مرخّصة.",
    ):
        assert phrase in content, f"missing maqam law: {phrase!r}"


def test_candidate_and_licensed_qawli_relation_are_separated() -> None:
    """trace_ref: docs/21 §11, §12."""
    content = _content()

    for phrase in (
        "النسبة المرشحة احتمال منضبط.",
        "وليست إفادة.",
        "ولا حكم.",
        "لا تتحول النسبة المرشحة إلى مرخّصة إلا بوصف مؤثر وانتفاء مانع.",
        "candidate_relation",
        "completed_required_parties",
        "effective_attribute",
        "maqam_preserved",
        "no_blocking_residual",
        "no_qadih_difference",
        "proof_trace",
    ):
        assert phrase in content, f"missing qawli phrase: {phrase!r}"


def test_qawl_direction_precedes_ifadah() -> None:
    """trace_ref: docs/21 §13 QawlDirection."""
    content = _content()

    for phrase in (
        "لا جهة قول بلا نسبة مرخّصة.",
        "ولا إفادة قبل تعيين الجهة.",
    ):
        assert phrase in content, f"missing direction law: {phrase!r}"


def test_ifadah_is_not_truth_hukm_tanzil_yaqin() -> None:
    """trace_ref: docs/21 §14 Ifadah."""
    content = _content()

    for phrase in (
        "الإفادة اكتمال وظيفة القول.",
        "لا ثبوت صدقه.",
        "truth",
        "hukm",
        "tanzīl",
        "yaqīn",
    ):
        assert phrase in content, f"missing ifadah phrase: {phrase!r}"


def test_mantooq_must_be_preserved_before_mafhoom() -> None:
    """trace_ref: docs/21 §15, §16."""
    content = _content()

    for phrase in (
        "معقول المنطوق هو ما ثبت من القول بعد الإفادة.",
        "لا ما استُخرج منه لاحقًا.",
        "لا مفهوم بلا منطوق محفوظ.",
        "ولا مفهوم يعلو على منطوقه.",
        "ولا مفهوم يعارض منطوقه.",
        "mafhoom muwāfaqah",
        "mafhoom mukhālafah",
        "mafhoom iqtiḍāʾ",
        "mafhoom ishārah",
        "mafhoom tanbīh",
    ):
        assert phrase in content, f"missing mantooq/mafhoom phrase: {phrase!r}"


def test_transitions_table_covers_every_arrow() -> None:
    """trace_ref: docs/21 §17 Atomic Transitions Table."""
    content = _content()

    transitions = (
        ("S0 → S1", "CarrierToDalGate"),
        ("S1 → S2", "InternalDalGate"),
        ("S2 → S3", "DalToLafziFormBridge"),
        ("S3 → S4", "LafziToLexicalBridge"),
        ("S4 → S5", "InternalMadlulGate"),
        ("S5 → S6", "DalMadlulCouplingGate"),
        ("S6 → S7", "MaqamActivationGate"),
        ("S7 → S8", "QawliCandidateGate"),
        ("S8 → S9", "QawliLicenseGate"),
        ("S9 → S10", "QawlDirectionGate"),
        ("S10 → S11", "IfadahGate"),
        ("S11 → S12", "MantooqGate"),
        ("S12 → S13", "MafhoomGate"),
    )
    for arrow, gate in transitions:
        assert arrow in content, f"missing transition arrow: {arrow}"
        assert gate in content, f"missing gate name: {gate}"


def test_nine_chain_guards_are_recorded() -> None:
    """trace_ref: docs/21 §18 Chain Guards."""
    content = _content()

    for guard in (
        "OriginGuard:",
        "BoundaryGuard:",
        "LicenseGuard:",
        "TraceGuard:",
        "IdentityGuard:",
        "ResidualGuard:",
        "RankGuard:",
        "ReverseTestGuard:",
        "NoSubstitutionGuard:",
    ):
        assert guard in content, f"missing chain guard: {guard}"

    for phrase in (
        "لا دخول بلا أصل محفوظ.",
        "لا عبور بلا حد.",
        "لا انتقال بلا رخصة.",
        "لا خروج بلا أثر.",
        "لا حفظ بلا هوية.",
        "لا بقايا مخفية.",
        "لا رتبة فوق CANDIDATE.",
        "لا نتيجة بلا رجوع إلى الأصل.",
        "لا طبقة تقوم مقام طبقة.",
    ):
        assert phrase in content, f"missing guard law: {phrase!r}"


def test_reverse_test_chain_is_complete_and_backward() -> None:
    """trace_ref: docs/21 §19 Reverse Test Law."""
    content = _content()

    for phrase in (
        "Mafhoom\n  must return to Mantooq",
        "Mantooq\n  must return to Ifadah",
        "Ifadah\n  must return to QawlDirection + LicensedQawliRelation",
        "LicensedQawliRelation\n  must return to CandidateQawliRelation + Maqam",
        "Maqam\n  must return to DalMadlulCoupling",
        "DalMadlulCoupling\n  must return to LexicalMadlul + Dal",
        "LexicalMadlul\n  must return to LafziForm",
        "LafziForm\n  must return to DalOnly",
        "DalOnly\n  must return to SpeechCarrier",
        "لا نتيجة بلا رجوع إلى الأصل.",
    ):
        assert phrase in content, f"missing reverse-test entry: {phrase!r}"


def test_forbidden_shortcuts_are_recorded_as_antipatterns() -> None:
    """trace_ref: docs/21 §20 Forbidden Shortcuts."""
    content = _content()

    for shortcut in (
        "SpeechCarrier → LexicalMeaning",
        "DalOnly → LexicalMadlul",
        "LafziForm → Relation",
        "LexicalMadlul → Ifadah",
        "Maqam → Truth",
        "Mutabaqah → Hukm",
        "Tadammun → Hukm",
        "Iltizam → Hukm",
        "CandidateQawliRelation → Ifadah",
        "Ifadah → Hukm",
        "Ifadah → Truth",
        "Mantooq → Mafhoom without preservation",
        "Mafhoom > Mantooq",
        "Probability → Yaqin",
        "StatisticalCandidate → LicensedSlotFill",
    ):
        assert shortcut in content, f"missing forbidden shortcut: {shortcut!r}"

    assert "These shortcuts are not implementation plans." in content
    assert "anti-patterns" in content


def test_drift_guardrail_blocks_stage_collapses() -> None:
    """trace_ref: docs/21 §21 Drift Guardrail."""
    content = _content()

    for phrase in (
        "`SpeechCarrier` must not drift into `DalOnly`",
        "`DalOnly` must not drift into `LexicalMadlul`",
        "`LafziForm` must not drift into `Relation`",
        "`LexicalMadlul` must not drift into `Ifadah`",
        "`Maqam` must not drift into `Truth`",
        "`Mutabaqah` must not drift into `Hukm`",
        "`Tadammun` must not drift into `Hukm`",
        "`Iltizam` must not drift into `Hukm`",
        "`CandidateQawliRelation` must not drift into `Ifadah`",
        "`Ifadah` must not drift into `Truth`",
        "`Ifadah` must not drift into `Hukm`",
        "`Mantooq` must not drift into `Mafhoom` without preservation",
        "`Mafhoom` must not outrank `Mantooq`",
    ):
        assert phrase in content, f"missing drift guardrail: {phrase!r}"


def test_final_boundary_preserves_entity_invariants() -> None:
    """trace_ref: docs/21 §23 Final Boundary Law."""
    content = _content()

    for phrase in (
        "trace_ref",
        'rank = "CANDIDATE"',
        "named FailureCode on rejection",
        "frozen dataclass status in source",
        "visible residuals",
    ):
        assert phrase in content, f"missing entity invariant: {phrase!r}"


def test_chain_law_does_not_create_runtime_or_locked_layer_source() -> None:
    """trace_ref: docs/20_AGENT_AUTONOMY_RUNBOOK.md §Stop conditions."""
    forbidden = (
        SRC_ROOT / "L2" / "licensed_intelligibility_chain.py",
        SRC_ROOT / "L3" / "licensed_intelligibility_chain.py",
        SRC_ROOT / "runtime" / "licensed_intelligibility_chain.py",
        SRC_ROOT / "runtime" / "mafhoom_engine.py",
        SRC_ROOT / "runtime" / "mantooq_engine.py",
        SRC_ROOT / "runtime" / "ifadah_engine.py",
        SRC_ROOT / "runtime" / "maqam_engine.py",
        SRC_ROOT / "runtime" / "qawli_relation_engine.py",
        SRC_ROOT / "runtime" / "binding_kernel.py",
        SRC_ROOT / "runtime" / "decision_engine.py",
        REPO_ROOT / "data" / "coverage_matrix_v0.1.yaml",
    )
    for path in forbidden:
        assert not path.exists(), f"forbidden runtime artifact present: {path}"
