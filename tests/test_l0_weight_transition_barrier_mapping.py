"""Audit-only checks for L0 weight-to-transition barrier mapping.

Origin: docs/64_L0_WEIGHT_TRANSITION_BARRIER_MAPPING_LAW.md
"""

from pathlib import Path


REPO_ROOT = Path(__file__).parent.parent
LAW_DOC = REPO_ROOT / "docs" / "64_L0_WEIGHT_TRANSITION_BARRIER_MAPPING_LAW.md"
SRC_ROOT = REPO_ROOT / "src" / "taaqqul_slot_geometry"
TRANSITION_REGISTRY_SRC = SRC_ROOT / "core" / "transition_registry.py"


def _content() -> str:
    return LAW_DOC.read_text(encoding="utf-8")


def _transition_registry_source() -> str:
    return TRANSITION_REGISTRY_SRC.read_text(encoding="utf-8")


def test_weight_transition_mapping_law_exists_and_is_audit_only() -> None:
    """trace_ref: docs/64_L0_WEIGHT_TRANSITION_BARRIER_MAPPING_LAW.md §Constitutional status."""
    content = _content()

    assert LAW_DOC.exists()
    assert "Runtime status: `AUDIT_ONLY`." in content
    assert "L0 is closed." in content
    assert "L1 is contract/audit bounded." in content
    assert "L2 remains locked." in content
    assert "L3 remains locked." in content
    assert "Runtime embargo remains active." in content


def test_mapping_law_declares_current_weight_sources_and_barriers() -> None:
    """trace_ref: docs/64_L0_WEIGHT_TRANSITION_BARRIER_MAPPING_LAW.md §Official mapping."""
    content = _content()

    for phrase in (
        "src/taaqqul_slot_geometry/L0/weight.py",
        "src/taaqqul_slot_geometry/core/arabic_weight_pattern.py",
        "src/taaqqul_slot_geometry/core/transition_registry.py",
        "Weight ⇏ Hukm",
        "Ifadah ⇏ Truth",
    ):
        assert phrase in content


def test_transition_registry_stops_at_mufrad_without_semantic_runtime_outputs() -> None:
    """trace_ref: docs/64_L0_WEIGHT_TRANSITION_BARRIER_MAPPING_LAW.md §One auditable claim."""
    source = _transition_registry_source().lower()
    assert "mufrad" in source

    for token in ("ifadah", "hukm", "tanzil", "truth", "yaqin"):
        assert token not in source


def test_source_tree_rejects_nonexistent_external_track_names_without_amendment() -> None:
    """trace_ref: docs/64_L0_WEIGHT_TRANSITION_BARRIER_MAPPING_LAW.md §Forbidden drift under this law."""

    forbidden_name_tokens = ("LAFZI-D6", "coupled_dalalah", "x0r")
    python_files = list(SRC_ROOT.rglob("*.py"))
    assert python_files

    for path in python_files:
        content = path.read_text(encoding="utf-8")
        for token in forbidden_name_tokens:
            assert token not in content
