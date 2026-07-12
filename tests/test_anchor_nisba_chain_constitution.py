"""Audit-only guard tests for the anchor-nisba constitutional chain.

Origin: docs/65_ANCHOR_NISBA_CHAIN_CONSTITUTION.md
"""

from pathlib import Path


REPO_ROOT = Path(__file__).parent.parent
DOC = REPO_ROOT / "docs" / "65_ANCHOR_NISBA_CHAIN_CONSTITUTION.md"
SRC_ROOT = REPO_ROOT / "src" / "taaqqul_slot_geometry"


def _content() -> str:
    return DOC.read_text(encoding="utf-8")


def test_anchor_nisba_doc_is_audit_only_and_locked_layer_safe() -> None:
    """trace_ref: docs/65 §Constitutional Status."""
    content = _content()

    for phrase in (
        "Runtime status: AUDIT_ONLY",
        "L0 is closed.",
        "L1 is contract/audit bounded.",
        "L2 remains locked.",
        "L3 remains locked.",
        "Runtime embargo remains active.",
    ):
        assert phrase in content


def test_corrected_chain_includes_anchor_and_nisba_sequence() -> None:
    """trace_ref: docs/65 §Corrected Chain."""
    content = _content()
    section = content.split("## Corrected Chain", maxsplit=1)[1]
    chain_block = section.split("```text", maxsplit=1)[1].split("```", maxsplit=1)[0]

    stages = (
        "WADI-L0",
        "ANCHOR-L0",
        "LEXEME-L0",
        "PRECOMP-L0",
        "NISBA-K0",
        "NISBA-C1",
        "NISBA-G1",
        "COMP-L0",
        "CASE-L0",
        "IFADAH-L0",
        "MAQAM-L0",
        "SPEECH-ACT-L0",
    )
    chain_lines = [line.strip() for line in chain_block.splitlines()]
    indices = [chain_lines.index(stage) for stage in stages]
    assert indices == sorted(indices)


def test_boundary_separation_law_is_explicit() -> None:
    """trace_ref: docs/65 §Boundary Separation Law."""
    content = _content()

    for phrase in (
        "النسبة ليست العامل",
        "والعامل ليس الطرف",
        "والعلامة الإعرابية ليست المقام",
        "None of these layers substitutes for another layer.",
    ):
        assert phrase in content


def test_anchor_types_and_nisba_gates_are_recorded() -> None:
    """trace_ref: docs/65 §Anchor Law and §Nisba Kernel Law."""
    content = _content()

    for phrase in (
        "GenusAnchor",
        "SourceAttributeAnchor",
        "RelationInterfaceAnchor",
        "ReferenceInterfaceAnchor",
        "NisbahKernel",
        "NisbahPossible is not NisbahEstablished.",
    ):
        assert phrase in content


def test_precomp_to_comp_direct_jump_is_prohibited() -> None:
    """trace_ref: docs/65 §No-Leap Requirement."""
    content = _content()

    assert "PRECOMP-L0 -> COMP-L0" in content
    for gate in ("NISBA-K0", "NISBA-C1", "NISBA-G1"):
        assert gate in content
    assert "anti-patterns" in content


def test_anchor_nisba_law_does_not_authorize_runtime_artifacts() -> None:
    """trace_ref: docs/65 §Final Boundary Law."""
    forbidden = (
        SRC_ROOT / "runtime" / "binding_kernel.py",
        SRC_ROOT / "runtime" / "decision_engine.py",
        SRC_ROOT / "runtime" / "nisba_engine.py",
        REPO_ROOT / "data" / "coverage_matrix_v0.1.yaml",
    )
    for path in forbidden:
        assert not path.exists(), f"forbidden runtime artifact present: {path}"
