"""Guard repository-level Copilot autonomy instructions.

trace_ref: docs/00B_AGENT_BINDING_CONSTITUTION.md; docs/12_RUNTIME_EMBARGO_CONSTITUTION.md
"""

from __future__ import annotations

from pathlib import Path


REPO_ROOT = Path(__file__).parent.parent
COPILOT_INSTRUCTIONS = REPO_ROOT / ".github" / "copilot-instructions.md"
AGENT_AUTONOMY_RUNBOOK = REPO_ROOT / "docs" / "20_AGENT_AUTONOMY_RUNBOOK.md"


COMMON_CONSTITUTIONAL_MARKERS = (
    "runtime",
    "embargo",
    "kernel",
    "decision_engine.py",
    "coverage_matrix_v0.1.yaml",
    "rank",
    "boolean",
    "euclidean learning",
    "audit",
    "failurealignment",
    "one narrow pr",
    "domain opening",
)

RUNBOOK_REQUIRED_SECTIONS = (
    "## Scope",
    "## Non-scope",
    "## Authority docs",
    "## Required PR body shape",
    "## Required validation",
    "## Constitutional invariants preserved",
)

PR_BODY_FIELDS = (
    "Scope",
    "Non-scope",
    "Authority docs",
    "Files changed",
    "Tests run",
    "Constitutional invariants preserved",
)


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _normalized(text: str) -> str:
    return text.casefold()


def test_copilot_instruction_files_exist():
    """trace_ref: docs/00B_AGENT_BINDING_CONSTITUTION.md Role Boundaries."""
    assert COPILOT_INSTRUCTIONS.exists()
    assert AGENT_AUTONOMY_RUNBOOK.exists()


def test_copilot_instructions_preserve_constitutional_markers():
    """trace_ref: docs/12_RUNTIME_EMBARGO_CONSTITUTION.md Embargo Rule."""
    content = _normalized(_read_text(COPILOT_INSTRUCTIONS))

    for marker in COMMON_CONSTITUTIONAL_MARKERS:
        assert marker in content


def test_agent_autonomy_runbook_preserves_constitutional_markers():
    """trace_ref: docs/12_RUNTIME_EMBARGO_CONSTITUTION.md Embargo Rule."""
    content = _normalized(_read_text(AGENT_AUTONOMY_RUNBOOK))

    for marker in COMMON_CONSTITUTIONAL_MARKERS:
        assert marker in content


def test_agent_autonomy_runbook_has_required_sections_and_pr_fields():
    """trace_ref: docs/00B_AGENT_BINDING_CONSTITUTION.md Role Boundaries."""
    content = _read_text(AGENT_AUTONOMY_RUNBOOK)
    required_pr_body = content.split("## Required PR body shape", maxsplit=1)[1]

    for section in RUNBOOK_REQUIRED_SECTIONS:
        assert section in content
    for field in PR_BODY_FIELDS:
        assert field in required_pr_body


def test_agent_autonomy_runbook_declares_stop_conditions():
    """trace_ref: docs/12_RUNTIME_EMBARGO_CONSTITUTION.md Explicit Prohibitions."""
    content = _normalized(_read_text(AGENT_AUTONOMY_RUNBOOK))

    assert "## stop conditions" in content
    assert "blocked" in content
    assert "runtime authorization" in content
    assert "rank promotion" in content
