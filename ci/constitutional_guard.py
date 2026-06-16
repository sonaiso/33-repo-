"""
Constitutional Guard — CI/CD gate that rejects PRs violating the constitution.

Origin: docs/00_MAQOOL_CONSTITUTION.md (all sections)

Usage:
    python -m ci.constitutional_guard --pr-number <N> --branch <branch-name>

Condition: Every PR must satisfy constitutional constraints.
Cause: The constitution is the root authority.
Barrier: Any violation produces a named REJECTED verdict.
Motive: No unconstitutional code enters the main branch.
"""
from __future__ import annotations

import argparse
import ast
import sys
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import FrozenSet, List


# ── Verdict ──────────────────────────────────────────────────────────────────


class Verdict(str, Enum):
    """Constitutional guard verdict."""

    PASSED = "PASSED"
    REJECTED = "REJECTED"


@dataclass(frozen=True)
class Violation:
    """A single constitutional violation found in a file.

    Parameters
    ----------
    file_path : str
        Path to the violating file.
    line_number : int
        Line number of the violation.
    rule : str
        The constitutional rule violated.
    description : str
        Human-readable description.
    failure_code : str
        The applicable FailureCode value.
    """

    file_path: str
    line_number: int
    rule: str
    description: str
    failure_code: str


@dataclass(frozen=True)
class GuardReport:
    """The full constitutional guard report.

    Parameters
    ----------
    pr_number : int
        The PR being checked.
    branch : str
        The branch being checked.
    verdict : Verdict
        PASSED or REJECTED.
    violations : tuple
        All violations found.
    checks_performed : int
        Number of checks performed.
    trace_ref : str
        Constitutional reference.
    rank : str
        Always "CANDIDATE".
    residuals : FrozenSet[str]
        Residual bundle.
    """

    pr_number: int
    branch: str
    verdict: Verdict
    violations: tuple
    checks_performed: int
    trace_ref: str = "docs/00_MAQOOL_CONSTITUTION.md"
    rank: str = "CANDIDATE"
    residuals: FrozenSet[str] = field(default_factory=frozenset)


# ── Checks ───────────────────────────────────────────────────────────────────


def check_trace_ref_present(file_path: Path) -> List[Violation]:
    """Check that Python source files contain trace_ref references.

    Condition: Every source file must reference the constitution.
    Cause: Rule 2 requires trace_ref on all entities.
    Barrier: Missing trace_ref → violation.
    Motive: Traceability to constitutional authority.
    """
    violations: List[Violation] = []
    if not file_path.suffix == ".py":
        return violations
    try:
        content = file_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return violations

    if not content.strip():
        return violations

    # Skip __init__.py files that are just package markers
    if file_path.name == "__init__.py" and len(content.strip()) < 100:
        return violations

    # Check for trace_ref or Origin or constitutional reference
    has_trace = (
        "trace_ref" in content
        or "Origin:" in content
        or "docs/00_MAQOOL_CONSTITUTION" in content
        or "docs/01_L0_PHONETIC_BOUNDARY" in content
    )
    if not has_trace:
        violations.append(Violation(
            file_path=str(file_path),
            line_number=1,
            rule="Rule 2 (trace_ref)",
            description="File has no constitutional trace reference",
            failure_code="M_00_11",
        ))
    return violations


def check_frozen_dataclasses(file_path: Path) -> List[Violation]:
    """Check that all dataclasses use frozen=True.

    Condition: Every dataclass must be frozen.
    Cause: Rule 3 requires immutability.
    Barrier: Non-frozen dataclass → violation.
    Motive: Prevent mutation of constitutional entities.
    """
    violations: List[Violation] = []
    if not file_path.suffix == ".py":
        return violations
    try:
        content = file_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return violations

    if "@dataclass" not in content:
        return violations

    try:
        tree = ast.parse(content)
    except SyntaxError:
        return violations

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            for decorator in node.decorator_list:
                # Bare @dataclass without parentheses (always mutable)
                if isinstance(decorator, ast.Name) and decorator.id == "dataclass":
                    violations.append(Violation(
                        file_path=str(file_path),
                        line_number=node.lineno,
                        rule="Rule 3 (frozen dataclass)",
                        description=(
                            f"Class {node.name!r} uses bare @dataclass "
                            f"without frozen=True"
                        ),
                        failure_code="M_CX_06",
                    ))
                # @dataclass(...) call form — check for frozen=True
                elif isinstance(decorator, ast.Call):
                    func = decorator.func
                    if isinstance(func, ast.Name) and func.id == "dataclass":
                        has_frozen = False
                        for keyword in decorator.keywords:
                            if keyword.arg == "frozen":
                                if isinstance(keyword.value, ast.Constant):
                                    has_frozen = keyword.value.value is True
                        if not has_frozen:
                            violations.append(Violation(
                                file_path=str(file_path),
                                line_number=node.lineno,
                                rule="Rule 3 (frozen dataclass)",
                                description=(
                                    f"Class {node.name!r} uses @dataclass "
                                    f"without frozen=True"
                                ),
                                failure_code="M_CX_06",
                            ))
    return violations


def check_no_io_in_source(file_path: Path) -> List[Violation]:
    """Check that source files do not perform I/O operations.

    Condition: No I/O in pure context.
    Cause: Rule 4 requires pure functions.
    Barrier: I/O calls → violation.
    Motive: Purity guarantee for constitutional entities.
    """
    violations: List[Violation] = []
    if not file_path.suffix == ".py":
        return violations
    try:
        content = file_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return violations

    # Skip the CI guard itself and test files
    if "ci/" in str(file_path) or "test_" in file_path.name:
        return violations

    # Check for forbidden I/O patterns in source
    forbidden_patterns = [
        ("open(", "M_CX_10"),
        ("requests.", "M_CX_11"),
        ("urllib", "M_CX_11"),
        ("socket.", "M_CX_11"),
        ("subprocess.", "M_CX_10"),
    ]
    lines = content.split("\n")
    for line_num, line in enumerate(lines, start=1):
        stripped = line.strip()
        if stripped.startswith("#"):
            continue
        for pattern, code in forbidden_patterns:
            if pattern in line:
                violations.append(Violation(
                    file_path=str(file_path),
                    line_number=line_num,
                    rule="Rule 4 (pure function)",
                    description=f"I/O pattern {pattern!r} found",
                    failure_code=code,
                ))
    return violations


def check_rank_not_promoted(file_path: Path) -> List[Violation]:
    """Check that no rank promotion occurs beyond CANDIDATE.

    Condition: rank must always be "CANDIDATE" in L0.
    Cause: Rule 2 ceiling.
    Barrier: Any promotion → violation.
    Motive: Prevent premature authority escalation.
    """
    violations: List[Violation] = []
    if not file_path.suffix == ".py":
        return violations
    try:
        content = file_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return violations

    # Skip test files
    if "test_" in file_path.name:
        return violations

    lines = content.split("\n")
    forbidden_ranks = ["PROVEN", "LICENSED", "FINAL", "PROMOTED"]
    for line_num, line in enumerate(lines, start=1):
        stripped = line.strip()
        if stripped.startswith("#"):
            continue
        for rank in forbidden_ranks:
            if f'rank = "{rank}"' in line or f"rank = '{rank}'" in line:
                violations.append(Violation(
                    file_path=str(file_path),
                    line_number=line_num,
                    rule="Rule 2 (rank ceiling)",
                    description=f"Rank promotion to {rank!r} forbidden in L0",
                    failure_code="M_CX_09",
                ))
    return violations


def check_no_l3_in_l0(file_path: Path) -> List[Violation]:
    """Check that L3 constructs do not appear in L0 code.

    Condition: L3 entities are forbidden in L0.
    Cause: Layer lock (Rule 6).
    Barrier: L3 construct in L0 → violation.
    Motive: Enforce layer discipline.
    """
    violations: List[Violation] = []
    if not file_path.suffix == ".py":
        return violations
    try:
        content = file_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return violations

    # Only check L0 source files
    if "/L0/" not in str(file_path):
        return violations

    forbidden_constructs = [
        ("HukmCandidate", "M_03_09"),
        ("TanzilCandidate", "M_03_10"),
        ("RealityClaim", "M_03_11"),
        ("MajazVerdict", "M_03_12"),
        ("NaqlVerdict", "M_03_13"),
    ]
    lines = content.split("\n")
    for line_num, line in enumerate(lines, start=1):
        stripped = line.strip()
        if stripped.startswith("#"):
            continue
        for construct, code in forbidden_constructs:
            if construct in line:
                violations.append(Violation(
                    file_path=str(file_path),
                    line_number=line_num,
                    rule="L3 forbidden in L0",
                    description=f"L3 construct {construct!r} found in L0",
                    failure_code=code,
                ))
    return violations


def check_roadmap_binding(file_path: Path) -> List[Violation]:
    """Check that new source files reference the project roadmap.

    Condition: Every source file must trace to the roadmap or constitution.
    Cause: Branching governance requires roadmap traceability (M_CX_16).
    Barrier: No roadmap or constitution reference → violation.
    Motive: Prevent unplanned work that fragments the project.
    """
    violations: List[Violation] = []
    if not file_path.suffix == ".py":
        return violations
    try:
        content = file_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return violations

    if not content.strip():
        return violations

    # Skip __init__.py, test files, and CI files
    if file_path.name == "__init__.py" and len(content.strip()) < 200:
        return violations
    if "test_" in file_path.name or "conftest" in file_path.name:
        return violations
    if "ci" in file_path.parts:
        return violations

    # Must reference either the constitution OR the roadmap
    has_authority_ref = (
        "docs/00_MAQOOL_CONSTITUTION" in content
        or "docs/15_PROJECT_ROADMAP" in content
        or "docs/14_PR_CHAIN_ROADMAP" in content
        or "docs/01_L0_PHONETIC_BOUNDARY" in content
        or "docs/01_EUCLIDEAN_PROOFS" in content
        or "docs/19_MORPHOLOGY_GENERATOR_THEOREM" in content
        or "docs/20_WAQF_WASL_BOUNDARY_THEOREM" in content
        or "Origin:" in content
        or "trace_ref" in content
    )
    if not has_authority_ref:
        violations.append(Violation(
            file_path=str(file_path),
            line_number=1,
            rule="Branching governance (roadmap binding)",
            description=(
                "File has no reference to roadmap or constitution — "
                "all code must trace to an authorized plan"
            ),
            failure_code="M_CX_16",
        ))
    return violations


# ── Guard Runner ─────────────────────────────────────────────────────────────


ALL_CHECKS = [
    check_trace_ref_present,
    check_frozen_dataclasses,
    check_no_io_in_source,
    check_rank_not_promoted,
    check_no_l3_in_l0,
    check_roadmap_binding,
]


def run_guard(
    source_dir: Path,
    pr_number: int = 0,
    branch: str = "",
) -> GuardReport:
    """Run all constitutional checks on a source directory.

    Condition: source_dir must contain Python source files.
    Cause: CI/CD must enforce constitutional compliance.
    Barrier: Any violation produces REJECTED verdict.
    Motive: Gate-keep the constitutional boundary.

    Parameters
    ----------
    source_dir : Path
        Root directory to scan.
    pr_number : int
        The PR number being checked.
    branch : str
        The branch name being checked.

    Returns
    -------
    GuardReport
        The full report with verdict.
    """
    all_violations: List[Violation] = []
    checks_performed = 0

    python_files = list(source_dir.rglob("*.py"))
    for py_file in python_files:
        for check_fn in ALL_CHECKS:
            violations = check_fn(py_file)
            all_violations.extend(violations)
            checks_performed += 1

    verdict = Verdict.PASSED if not all_violations else Verdict.REJECTED

    return GuardReport(
        pr_number=pr_number,
        branch=branch,
        verdict=verdict,
        violations=tuple(all_violations),
        checks_performed=checks_performed,
    )


def print_report(report: GuardReport) -> None:
    """Print the guard report to stdout.

    This is the ONLY I/O function in the guard — intentionally separated
    from the pure check logic.
    """
    print(f"\n{'='*60}")
    print(f"  CONSTITUTIONAL GUARD REPORT")
    print(f"{'='*60}")
    print(f"  PR: #{report.pr_number}")
    print(f"  Branch: {report.branch}")
    print(f"  Checks performed: {report.checks_performed}")
    print(f"  Violations: {len(report.violations)}")
    print(f"  Verdict: {report.verdict.value}")
    print(f"{'='*60}")

    if report.violations:
        print("\n  VIOLATIONS:")
        for i, v in enumerate(report.violations, 1):
            print(f"\n  [{i}] {v.rule}")
            print(f"      File: {v.file_path}:{v.line_number}")
            print(f"      Code: {v.failure_code}")
            print(f"      Desc: {v.description}")

    print(f"\n{'='*60}")
    if report.verdict == Verdict.PASSED:
        print("  ✓ CONSTITUTIONAL COMPLIANCE: PASSED")
    else:
        print("  ✗ CONSTITUTIONAL COMPLIANCE: REJECTED")
    print(f"{'='*60}\n")


# ── CLI Entry Point ──────────────────────────────────────────────────────────


def main() -> None:
    """CLI entry point for the constitutional guard."""
    parser = argparse.ArgumentParser(
        description="Constitutional Guard — rejects PRs violating the constitution"
    )
    parser.add_argument(
        "--pr-number", type=int, default=0,
        help="PR number being checked",
    )
    parser.add_argument(
        "--branch", type=str, default="",
        help="Branch name being checked",
    )
    parser.add_argument(
        "--source-dir", type=str, default="src",
        help="Source directory to scan (default: src)",
    )
    args = parser.parse_args()

    source_dir = Path(args.source_dir)
    if not source_dir.exists():
        print(f"ERROR: source directory {source_dir} does not exist")
        sys.exit(2)

    report = run_guard(
        source_dir=source_dir,
        pr_number=args.pr_number,
        branch=args.branch,
    )

    print_report(report)

    if report.verdict == Verdict.REJECTED:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
