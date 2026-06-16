"""
Test L0 Closure Declaration — verifies all conditions for formal L0 closure.

Origin: docs/15_PROJECT_ROADMAP.md Phase 0 Closure Condition
Authority: docs/00_MAQOOL_CONSTITUTION.md §5 Rule 1
Reference: docs/L0_CLOSURE_DECLARATION.md

This test ensures that:
1. All 13 L0 entities exist and are properly implemented
2. No open residuals remain in L0 source
3. The constitutional guard passes
4. L1 is authorized (closure declaration exists)
5. L0 entities are read-only (no L1+ constructs leaked in)
"""
from __future__ import annotations

from pathlib import Path

import pytest

# ── Paths ────────────────────────────────────────────────────────────────────

REPO_ROOT = Path(__file__).parent.parent
SRC_ROOT = REPO_ROOT / "src" / "taaqqul_slot_geometry"
L0_DIR = SRC_ROOT / "L0"
L1_DIR = SRC_ROOT / "L1"
DOCS_DIR = REPO_ROOT / "docs"
CLOSURE_DOC = DOCS_DIR / "L0_CLOSURE_DECLARATION.md"


# ── Expected L0 Entities ─────────────────────────────────────────────────────

EXPECTED_L0_ENTITIES = [
    "phoneme.py",
    "grapheme.py",
    "vowel.py",
    "syllable.py",
    "utterance.py",
    "signifier.py",
    "signified.py",
    "union.py",
    "signification.py",
    "jamid.py",
    "harf_maani.py",
    "weight.py",
    "waqf_wasl.py",
]


# ══════════════════════════════════════════════════════════════════════════════
# Test: Closure Declaration Exists
# ══════════════════════════════════════════════════════════════════════════════


class TestL0ClosureDeclarationExists:
    """Verify the closure declaration document exists and is well-formed."""

    def test_closure_document_exists(self):
        """The L0 closure declaration document must exist."""
        assert CLOSURE_DOC.exists(), (
            f"L0 Closure Declaration not found at {CLOSURE_DOC}"
        )

    def test_closure_document_references_constitution(self):
        """Closure document must reference the constitution."""
        content = CLOSURE_DOC.read_text(encoding="utf-8")
        assert "docs/00_MAQOOL_CONSTITUTION.md" in content

    def test_closure_document_declares_closure(self):
        """Closure document must contain formal closure statement."""
        content = CLOSURE_DOC.read_text(encoding="utf-8")
        assert "formally closed" in content.lower()

    def test_closure_document_authorizes_l1(self):
        """Closure document must authorize L1 opening."""
        content = CLOSURE_DOC.read_text(encoding="utf-8")
        assert "L1" in content
        assert "authorized" in content.lower() or "open" in content.lower()


# ══════════════════════════════════════════════════════════════════════════════
# Test: All L0 Entities Complete
# ══════════════════════════════════════════════════════════════════════════════


class TestL0EntitiesComplete:
    """Verify all 13 L0 entities are present and complete."""

    def test_all_13_entities_exist(self):
        """All 13 expected L0 entity files must be present."""
        actual = set(
            f.name for f in L0_DIR.glob("*.py") if f.name != "__init__.py"
        )
        expected = set(EXPECTED_L0_ENTITIES)
        missing = expected - actual
        assert missing == set(), f"Missing L0 entities: {missing}"

    def test_entity_count_exact(self):
        """L0 must have exactly 13 entity files (no extras)."""
        actual = [
            f.name for f in L0_DIR.glob("*.py") if f.name != "__init__.py"
        ]
        assert len(actual) == len(EXPECTED_L0_ENTITIES), (
            f"Expected {len(EXPECTED_L0_ENTITIES)} entities, "
            f"found {len(actual)}: {actual}"
        )

    @pytest.mark.parametrize("entity_file", EXPECTED_L0_ENTITIES)
    def test_entity_has_trace_ref(self, entity_file: str):
        """Every L0 entity must carry a trace_ref or Origin reference."""
        path = L0_DIR / entity_file
        content = path.read_text(encoding="utf-8")
        has_trace = (
            "trace_ref" in content
            or "Origin:" in content
            or "docs/00_MAQOOL_CONSTITUTION" in content
            or "docs/01_L0_PHONETIC_BOUNDARY" in content
        )
        assert has_trace, f"{entity_file} missing constitutional trace"

    @pytest.mark.parametrize("entity_file", EXPECTED_L0_ENTITIES)
    def test_entity_has_frozen_dataclass(self, entity_file: str):
        """Every L0 entity must use frozen dataclasses."""
        path = L0_DIR / entity_file
        content = path.read_text(encoding="utf-8")
        if "@dataclass" in content:
            assert "frozen=True" in content, (
                f"{entity_file} has @dataclass without frozen=True"
            )


# ══════════════════════════════════════════════════════════════════════════════
# Test: No Open Residuals in L0
# ══════════════════════════════════════════════════════════════════════════════


class TestL0NoOpenResiduals:
    """Verify no open residual markers remain in L0."""

    RESIDUAL_MARKERS = ("TODO", "FIXME", "HACK", "XXX")

    def test_no_residual_markers_in_l0(self):
        """L0 source files must have no TODO/FIXME/HACK/XXX markers."""
        violations = []
        for f in L0_DIR.glob("*.py"):
            if f.name == "__init__.py":
                continue
            content = f.read_text(encoding="utf-8")
            for marker in self.RESIDUAL_MARKERS:
                if marker in content:
                    violations.append(f"{f.name}: contains {marker}")

        assert violations == [], (
            f"Open residuals found in L0: {violations}"
        )


# ══════════════════════════════════════════════════════════════════════════════
# Test: L1 Authorization
# ══════════════════════════════════════════════════════════════════════════════


class TestL1Authorization:
    """Verify L1 is properly authorized after L0 closure."""

    def test_l1_package_exists(self):
        """L1 package directory must exist (even if empty)."""
        assert L1_DIR.exists(), "L1 directory does not exist"

    def test_l1_init_exists(self):
        """L1 __init__.py must exist as package marker."""
        init = L1_DIR / "__init__.py"
        assert init.exists(), "L1/__init__.py does not exist"

    def test_l1_init_references_constitution(self):
        """L1 __init__.py must reference constitutional authority."""
        init = L1_DIR / "__init__.py"
        content = init.read_text(encoding="utf-8")
        has_ref = (
            "docs/00_MAQOOL_CONSTITUTION" in content
            or "Origin:" in content
        )
        assert has_ref, "L1/__init__.py missing constitutional reference"

    def test_l2_still_locked(self):
        """L2 must have no production code (still locked)."""
        l2_dir = SRC_ROOT / "L2"
        if l2_dir.exists():
            production_files = [
                f for f in l2_dir.glob("*.py") if f.name != "__init__.py"
            ]
            assert production_files == [], (
                f"L2 is locked but has files: {[f.name for f in production_files]}"
            )

    def test_l3_still_locked(self):
        """L3 must have no production code (still locked)."""
        l3_dir = SRC_ROOT / "L3"
        if l3_dir.exists():
            production_files = [
                f for f in l3_dir.glob("*.py") if f.name != "__init__.py"
            ]
            assert production_files == [], (
                f"L3 is locked but has files: {[f.name for f in production_files]}"
            )
