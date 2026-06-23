"""Rejected runtime anti-pattern guardrails for PR #56 (docs + tests only)."""

from __future__ import annotations

import re
from pathlib import Path


REPO_ROOT = Path(__file__).parent.parent
GUARD_DOC = REPO_ROOT / "docs" / "15_REJECTED_RUNTIME_PATTERNS.md"

FORBIDDEN_FILES = [
    REPO_ROOT / "src" / "taaqqul_slot_geometry" / "L1" / "binding_kernel.py",
    REPO_ROOT / "src" / "taaqqul_slot_geometry" / "L1" / "decision_engine.py",
    REPO_ROOT / "coverage_matrix_v0.1.yaml",
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
    r"\bdomain_proved\s*:\s*true\b",
    r"\bunit_proved\s*:\s*true\b",
    r"\bidentity_preserved\s*:\s*true\b",
    r"\btrace_preserved\s*:\s*true\b",
    r"\bgate_passed\s*:\s*true\b",
    r"\bis_preserved\s*:\s*bool\s*=\s*True\b",
    r"\btransform\(operation:\s*str\):\s*pass\b",
    r"\bevidence\s+list\s+as\s+proof\b",
    r"\bMRK\s+boolean\s+defaults\b",
]

FORBIDDEN_PLAIN_TOKENS = [
    "binding_kernel.py",
    "decision_engine.py",
    "coverage_matrix_v0.1.yaml",
]


def _scan_targets() -> list[Path]:
    """Collect source/config files where pre-runtime anti-patterns are forbidden."""
    targets: set[Path] = set()
    targets.update((REPO_ROOT / "src").rglob("*.py"))
    targets.update((REPO_ROOT / "ci").rglob("*.py"))

    for pattern in ("*.toml", "*.yaml", "*.yml"):
        targets.update(REPO_ROOT.glob(pattern))
        targets.update((REPO_ROOT / "ci").rglob(pattern))

    return sorted(path for path in targets if path.is_file())


def test_rejected_runtime_patterns_doc_exists_with_required_markers():
    """trace_ref: docs/12_RUNTIME_EMBARGO_CONSTITUTION.md Explicit Prohibitions."""
    assert GUARD_DOC.exists(), "Missing rejected runtime anti-pattern guard document"
    content = GUARD_DOC.read_text(encoding="utf-8")
    for phrase in REQUIRED_DOC_PHRASES:
        assert phrase in content, f"Missing required rejected-pattern phrase: {phrase}"


def test_forbidden_runtime_files_are_absent():
    """trace_ref: docs/12_RUNTIME_EMBARGO_CONSTITUTION.md Explicit Prohibitions."""
    for path in FORBIDDEN_FILES:
        assert not path.exists(), f"Forbidden pre-runtime artifact exists: {path}"


def test_source_and_config_files_block_rejected_runtime_antipatterns():
    """trace_ref: docs/12_RUNTIME_EMBARGO_CONSTITUTION.md Embargo Rule."""
    violations: list[str] = []
    for path in _scan_targets():
        text = path.read_text(encoding="utf-8")
        for token in FORBIDDEN_PLAIN_TOKENS:
            if token in text:
                violations.append(f"{path}: plain token '{token}'")
        for regex in FORBIDDEN_REGEXES:
            if re.search(regex, text):
                violations.append(f"{path}: regex '{regex}'")

    assert not violations, "\n" + "\n".join(violations)
