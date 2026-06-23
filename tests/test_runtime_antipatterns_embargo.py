"""Rejected runtime anti-pattern guardrails for PR #56 (docs + tests only)."""

from __future__ import annotations

import re
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).parent.parent
GUARD_DOC = REPO_ROOT / "docs" / "15_REJECTED_RUNTIME_PATTERNS.md"

FORBIDDEN_FILE_NAMES = [
    "binding_kernel.py",
    "decision_engine.py",
    "coverage_matrix_v0.1.yaml",
]

REQUIRED_DOC_PHRASES = [
    "Rejected Runtime Anti-Patterns",
    "binding_kernel.py",
    "decision_engine.py",
    "coverage_matrix_v0.1.yaml",
    "BindingDecisionEngine",
    "MRK boolean defaults",
    "domain_proved: true",
    "unit_proved: true",
    "identity_preserved: true",
    "trace_preserved: true",
    "gate_passed: true",
    "is_preserved: bool = True",
    "Rank.CERTIFICATE",
    "Rank.REJECTED",
    "evidence list as proof",
    "transform(operation: str): pass",
    "All rows remain audit-only.",
    "Runtime embargo remains active.",
    "No kernel.",
    "No predicates.",
    "No translators.",
    "No coverage runtime.",
]

FORBIDDEN_REGEXES = [
    r"\bBindingDecisionEngine\b",
    r"\bRank\.CERTIFICATE\b",
    r"\bRank\.REJECTED\b",
    r"\bdomain_proved\s*:\s*(?:true|True)\b",
    r"\bunit_proved\s*:\s*(?:true|True)\b",
    r"\bidentity_preserved\s*:\s*(?:true|True)\b",
    r"\btrace_preserved\s*:\s*(?:true|True)\b",
    r"\bgate_passed\s*:\s*(?:true|True)\b",
    r"\bis_preserved\s*:\s*bool\s*=\s*(?:true|True)\b",
    r"\btransform\(operation:\s*str\):\s*pass\b",
    r"\bevidence\s+list\s+as\s+proof\b",
    r"\bMRK\s+boolean\s+defaults\b",
]

ALLOWED_SUFFIXES = {".py", ".toml", ".yaml", ".yml"}


def scan_targets() -> list[Path]:
    """Collect source/config files where pre-runtime anti-patterns are forbidden."""
    targets: set[Path] = set()
    targets.update((REPO_ROOT / "src").rglob("*.py"))
    targets.update((REPO_ROOT / "ci").rglob("*.py"))

    for pattern in ("*.toml", "*.yaml", "*.yml"):
        targets.update(REPO_ROOT.glob(pattern))
        targets.update((REPO_ROOT / "ci").rglob(pattern))

    return sorted(path for path in targets if path.is_file())


def forbidden_runtime_files() -> list[Path]:
    """Return forbidden runtime file artifacts if they exist anywhere in the repo."""
    paths: list[Path] = []
    for name in FORBIDDEN_FILE_NAMES:
        paths.extend(path for path in REPO_ROOT.rglob(name) if path.is_file())
    return sorted(set(paths))


@pytest.fixture(scope="module")
def scanned_targets() -> list[Path]:
    return scan_targets()


def test_scanned_targets_are_source_and_config_files_only(scanned_targets: list[Path]):
    """trace_ref: docs/12_RUNTIME_EMBARGO_CONSTITUTION.md Embargo Rule."""
    targets = scanned_targets
    assert targets, "scan targets must not be empty"
    assert all(path.is_file() for path in targets)
    assert all(path.suffix in ALLOWED_SUFFIXES for path in targets)
    assert any(path.is_relative_to(REPO_ROOT / "src") for path in targets)
    assert any(path.is_relative_to(REPO_ROOT / "ci") for path in targets)
    assert REPO_ROOT / "pyproject.toml" in targets


def test_rejected_runtime_patterns_doc_exists_with_required_markers():
    """trace_ref: docs/12_RUNTIME_EMBARGO_CONSTITUTION.md Explicit Prohibitions."""
    assert GUARD_DOC.exists(), "Missing rejected runtime anti-pattern guard document"
    content = GUARD_DOC.read_text(encoding="utf-8")
    for phrase in REQUIRED_DOC_PHRASES:
        assert phrase in content, f"Missing required rejected-pattern phrase: {phrase}"


def test_forbidden_runtime_files_are_absent():
    """trace_ref: docs/12_RUNTIME_EMBARGO_CONSTITUTION.md Explicit Prohibitions."""
    matches = forbidden_runtime_files()
    assert not matches, "Forbidden pre-runtime artifacts exist:\n" + "\n".join(
        str(path) for path in matches
    )


def test_source_and_config_files_block_rejected_runtime_anti_patterns(
    scanned_targets: list[Path],
):
    """trace_ref: docs/12_RUNTIME_EMBARGO_CONSTITUTION.md Embargo Rule."""
    violations: list[str] = []
    for path in scanned_targets:
        text = path.read_text(encoding="utf-8")
        file_violations: list[str] = []
        for regex in FORBIDDEN_REGEXES:
            for match in re.finditer(regex, text):
                line_number = text.count("\n", 0, match.start()) + 1
                matched_text = match.group(0)
                file_violations.append(
                    f"regex '{regex}' matched '{matched_text}' at line {line_number}"
                )
        if file_violations:
            violations.append(f"{path}: " + ", ".join(file_violations))

    assert not violations, "\n" + "\n".join(violations)
