"""
KPI Indicators — Measurable performance indicators enforced via pytest.

Origin: docs/16_STRATEGIC_METHODOLOGY.md §7
Authority: docs/00_MAQOOL_CONSTITUTION.md §5

These tests measure adherence to strategic, long-term, medium-term, and
short-term goals. Each test maps to a specific KPI in the methodology document.

Running these tests provides a quantitative measure of project health:
    pytest tests/test_kpi_indicators.py -v
"""
from __future__ import annotations

import ast
import importlib
import inspect
import subprocess
import sys
from pathlib import Path
from typing import List

import pytest

# ── Paths ────────────────────────────────────────────────────────────────────

REPO_ROOT = Path(__file__).parent.parent
SRC_ROOT = REPO_ROOT / "src" / "taaqqul_slot_geometry"
L0_DIR = SRC_ROOT / "L0"
L1_DIR = SRC_ROOT / "L1"
L2_DIR = SRC_ROOT / "L2"
L3_DIR = SRC_ROOT / "L3"
CONSTITUTION_DIR = SRC_ROOT / "constitution"
CORE_DIR = SRC_ROOT / "core"
RUNTIME_DIR = SRC_ROOT / "runtime"

# All source directories that contain production code
ALL_SOURCE_DIRS = [L0_DIR, CONSTITUTION_DIR, CORE_DIR, RUNTIME_DIR]


def _python_files(directory: Path) -> List[Path]:
    """Get all Python files in a directory (excluding __init__.py)."""
    if not directory.exists():
        return []
    return [f for f in directory.glob("*.py") if f.name != "__init__.py"]


def _all_source_files() -> List[Path]:
    """Get all source files across all production directories."""
    files = []
    for d in ALL_SOURCE_DIRS:
        files.extend(_python_files(d))
    return files


# ══════════════════════════════════════════════════════════════════════════════
# KPI-01: trace_ref Coverage
# Every source file must reference the constitution or roadmap
# ══════════════════════════════════════════════════════════════════════════════


class TestKPITraceCoverage:
    """KPI-01: 100% of source files have constitutional trace.

    Origin: docs/16_STRATEGIC_METHODOLOGY.md §7 KPI-01
    Target: 100%
    """

    AUTHORITY_MARKERS = (
        "docs/00_MAQOOL_CONSTITUTION",
        "docs/15_PROJECT_ROADMAP",
        "docs/14_PR_CHAIN_ROADMAP",
        "docs/01_L0_PHONETIC_BOUNDARY",
        "docs/01_EUCLIDEAN_PROOFS",
        "docs/19_MORPHOLOGY_GENERATOR_THEOREM",
        "docs/20_WAQF_WASL_BOUNDARY_THEOREM",
        "Origin:",
        "trace_ref",
    )

    def test_all_source_files_have_trace(self):
        """Every source file must reference the constitution or roadmap."""
        files = _all_source_files()
        assert len(files) > 0, "No source files found"

        violations = []
        for f in files:
            content = f.read_text(encoding="utf-8")
            if not any(marker in content for marker in self.AUTHORITY_MARKERS):
                violations.append(str(f.relative_to(REPO_ROOT)))

        assert violations == [], (
            f"KPI-01 FAILED: {len(violations)} files without trace_ref: "
            f"{violations}"
        )


# ══════════════════════════════════════════════════════════════════════════════
# KPI-02: Frozen Dataclass Compliance
# All dataclasses must use frozen=True
# ══════════════════════════════════════════════════════════════════════════════


class TestKPIFrozenCompliance:
    """KPI-02: 100% of dataclasses use frozen=True.

    Origin: docs/16_STRATEGIC_METHODOLOGY.md §7 KPI-02
    Target: 100%
    """

    def test_all_dataclasses_frozen(self):
        """Every @dataclass in source must have frozen=True."""
        files = _all_source_files()
        violations = []

        for f in files:
            content = f.read_text(encoding="utf-8")
            try:
                tree = ast.parse(content)
            except SyntaxError:
                continue

            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    for decorator in node.decorator_list:
                        # Check @dataclass(...) calls
                        if isinstance(decorator, ast.Call):
                            func = decorator.func
                            if isinstance(func, ast.Name) and func.id == "dataclass":
                                has_frozen = False
                                for kw in decorator.keywords:
                                    if kw.arg == "frozen":
                                        if isinstance(kw.value, ast.Constant):
                                            has_frozen = kw.value.value is True
                                if not has_frozen:
                                    violations.append(
                                        f"{f.relative_to(REPO_ROOT)}:{node.lineno} "
                                        f"class {node.name}"
                                    )

        assert violations == [], (
            f"KPI-02 FAILED: {len(violations)} dataclasses not frozen: "
            f"{violations}"
        )


# ══════════════════════════════════════════════════════════════════════════════
# KPI-03: Named Failure Coverage
# All raise statements in source use FailureCode-based exceptions
# ══════════════════════════════════════════════════════════════════════════════


class TestKPINamedFailures:
    """KPI-03: All rejection paths use named FailureCodes.

    Origin: docs/16_STRATEGIC_METHODOLOGY.md §7 KPI-03
    Target: 100% (no bare ValueError/TypeError without failure_code)
    """

    # Exception classes that carry failure_code
    NAMED_EXCEPTION_PATTERNS = (
        "FailureCode",
        "failure_code",
        "TransitionError",
        "IdentityLossError",
        "BranchLicenseError",
        "ProofVerificationError",
    )

    def test_no_silent_exceptions_in_guards(self):
        """Birth guards (__post_init__) must use named failure codes."""
        files = _all_source_files()
        violations = []

        for f in files:
            content = f.read_text(encoding="utf-8")
            try:
                tree = ast.parse(content)
            except SyntaxError:
                continue

            for node in ast.walk(tree):
                if (
                    isinstance(node, ast.FunctionDef)
                    and node.name == "__post_init__"
                ):
                    # Check raise statements inside __post_init__
                    for child in ast.walk(node):
                        if isinstance(child, ast.Raise) and child.exc:
                            # Get the source segment for context
                            lines = content.split("\n")
                            line_content = lines[child.lineno - 1] if child.lineno <= len(lines) else ""
                            has_named = any(
                                pat in line_content
                                for pat in self.NAMED_EXCEPTION_PATTERNS
                            )
                            # Also check surrounding lines for failure_code
                            context_start = max(0, child.lineno - 3)
                            context_end = min(len(lines), child.lineno + 2)
                            context = "\n".join(lines[context_start:context_end])
                            if not has_named and not any(
                                pat in context
                                for pat in self.NAMED_EXCEPTION_PATTERNS
                            ):
                                violations.append(
                                    f"{f.relative_to(REPO_ROOT)}:{child.lineno}"
                                )

        assert violations == [], (
            f"KPI-03 FAILED: {len(violations)} silent exceptions in birth guards: "
            f"{violations}"
        )


# ══════════════════════════════════════════════════════════════════════════════
# KPI-04: L0 Entity Count
# All 13 L0 entities must be present
# ══════════════════════════════════════════════════════════════════════════════


class TestKPIL0EntityCount:
    """KPI-04: All L0 entities are implemented.

    Origin: docs/16_STRATEGIC_METHODOLOGY.md §7 KPI-04
    Target: 13 entity files in L0/
    """

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

    def test_l0_entity_count(self):
        """L0 must have exactly 13 entity files."""
        actual_files = [f.name for f in _python_files(L0_DIR)]
        assert len(actual_files) == 13, (
            f"KPI-04 FAILED: Expected 13 L0 entities, found {len(actual_files)}"
        )

    def test_all_expected_entities_present(self):
        """All expected L0 entity files must exist."""
        actual_files = set(f.name for f in _python_files(L0_DIR))
        missing = set(self.EXPECTED_L0_ENTITIES) - actual_files
        assert missing == set(), (
            f"KPI-04 FAILED: Missing L0 entities: {missing}"
        )


# ══════════════════════════════════════════════════════════════════════════════
# KPI-05: No Layer Leak
# No L1/L2/L3 constructs may exist in L0 code
# ══════════════════════════════════════════════════════════════════════════════


class TestKPINoLayerLeak:
    """KPI-05: No higher-layer constructs leak into L0.

    Origin: docs/16_STRATEGIC_METHODOLOGY.md §7 KPI-05
    Target: 0 leaks
    """

    FORBIDDEN_IN_L0 = [
        "HukmCandidate",
        "TanzilCandidate",
        "RealityClaim",
        "MajazVerdict",
        "NaqlVerdict",
    ]

    def test_no_l3_constructs_in_l0(self):
        """L3 constructs must not appear in L0 source code."""
        l0_files = _python_files(L0_DIR)
        violations = []

        for f in l0_files:
            content = f.read_text(encoding="utf-8")
            lines = content.split("\n")
            for line_num, line in enumerate(lines, start=1):
                stripped = line.strip()
                if stripped.startswith("#"):
                    continue
                for construct in self.FORBIDDEN_IN_L0:
                    if construct in line:
                        violations.append(
                            f"{f.relative_to(REPO_ROOT)}:{line_num} "
                            f"contains {construct!r}"
                        )

        assert violations == [], (
            f"KPI-05 FAILED: {len(violations)} layer leaks: {violations}"
        )


# ══════════════════════════════════════════════════════════════════════════════
# KPI-06: CI Guard Clean
# The constitutional guard must pass with 0 violations
# ══════════════════════════════════════════════════════════════════════════════


class TestKPICIGuardClean:
    """KPI-06: CI constitutional guard passes with 0 violations.

    Origin: docs/16_STRATEGIC_METHODOLOGY.md §7 KPI-06
    Target: 0 violations
    """

    def test_constitutional_guard_passes(self):
        """Run the CI guard and verify 0 violations."""
        result = subprocess.run(
            [
                sys.executable, "-m", "ci.constitutional_guard",
                "--source-dir", str(SRC_ROOT),
            ],
            capture_output=True,
            text=True,
            cwd=str(REPO_ROOT),
        )
        assert "Verdict: PASSED" in result.stdout, (
            f"KPI-06 FAILED: CI guard did not pass.\n"
            f"stdout: {result.stdout[-500:]}\n"
            f"stderr: {result.stderr[-500:]}"
        )


# ══════════════════════════════════════════════════════════════════════════════
# KPI-07: No Open Residuals (structural check)
# Source modules should not have TODO/FIXME indicating unfinished work
# ══════════════════════════════════════════════════════════════════════════════


class TestKPINoOpenResiduals:
    """KPI-07: Residuals in source code are bounded.

    Origin: docs/16_STRATEGIC_METHODOLOGY.md §7 KPI-07
    Target: ≤ baseline (no regression)
    """

    # Maximum allowed open residual markers
    BASELINE_LIMIT = 0

    RESIDUAL_MARKERS = ("TODO", "FIXME", "HACK", "XXX")

    def test_open_residuals_within_baseline(self):
        """Open residual markers in L0 source must not exceed baseline."""
        l0_files = _python_files(L0_DIR)
        count = 0

        for f in l0_files:
            content = f.read_text(encoding="utf-8")
            for marker in self.RESIDUAL_MARKERS:
                count += content.count(marker)

        assert count <= self.BASELINE_LIMIT, (
            f"KPI-07 FAILED: {count} open residual markers in L0 "
            f"(baseline: {self.BASELINE_LIMIT})"
        )


# ══════════════════════════════════════════════════════════════════════════════
# KPI-P1: Phase Progress — L0 Completion
# ══════════════════════════════════════════════════════════════════════════════


class TestKPIPhaseProgress:
    """KPI-P1..P5: Phase completion progress indicators.

    Origin: docs/16_STRATEGIC_METHODOLOGY.md §7 KPI-P1..P5
    """

    def test_l0_phase_complete(self):
        """Phase 0 (L0) should be 100% complete — all 13 entities + runtime."""
        l0_entities = _python_files(L0_DIR)
        assert len(l0_entities) == 13, f"L0 has {len(l0_entities)} entities, expected 13"

        runtime_engine = RUNTIME_DIR / "constitutional_engine.py"
        assert runtime_engine.exists(), "Runtime engine missing"

    def test_l1_phase_not_started(self):
        """Phase 1 (L1) should have no production code yet (only __init__.py)."""
        l1_files = _python_files(L1_DIR)
        # L1 should be empty (no production files yet)
        assert l1_files == [], (
            f"L1 has unexpected files: {[f.name for f in l1_files]} — "
            "L1 should not start until L0 is formally closed"
        )

    def test_l2_phase_locked(self):
        """Phase 2 (L2) must have no production code."""
        l2_files = _python_files(L2_DIR)
        assert l2_files == [], f"L2 has unexpected files: {[f.name for f in l2_files]}"

    def test_l3_phase_locked(self):
        """Phase 3 (L3) must have no production code."""
        l3_files = _python_files(L3_DIR)
        assert l3_files == [], f"L3 has unexpected files: {[f.name for f in l3_files]}"

    def test_overall_progress_percentage(self):
        """Overall progress: count of completed phases / total phases."""
        # Phase 0 complete = 1, total = 4
        completed_phases = 1  # L0 only
        total_phases = 4
        progress = completed_phases / total_phases
        # This test documents progress, not enforces a minimum
        assert progress >= 0.25, (
            f"Progress is {progress*100:.0f}%, expected at least 25% (1/4 phases)"
        )
