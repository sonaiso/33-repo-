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
    "## Current hardening baseline",
    "## Highest-priority safe gap queue",
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
    "Why this is audit-only",
)

ARABIC_NEXT_SAFE_STEP_PROMPT = (
    "إذا أردت، أبدأ الآن بالخطوة التالية الضيقة الآمنة (PR واحد فقط) وفق خيارك التالي."
)

CURRENT_BASELINE_MARKERS = (
    "PR #103",
    "PR #105",
    "expected_verdict fixture matrix",
    "Computed coverage is schema/fixture based only",
    "`computed_verdict` cannot be supplied by fixture data",
    "all `computed_verdict` examples remain invalid",
    "do not regress it",
)

SAFE_GAP_QUEUE_MARKERS = (
    "After PR #105",
    "Closed by PR #105: computed coverage verdict fixture tests are strengthened",
    "allowed-context negative fixture coverage exists",
    "schema tests prove `computed_verdict` is rejected for every verdict fixture type",
    "computed_verdict rejection fixture",
    "canonical_family",
    "forbidden_runtime_use",
    "Current transition: keep agent autonomy instructions/runbook synchronized",
    "anti-pattern regression guards",
)


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _normalized(text: str) -> str:
    return text.casefold()


def _post_pr_105_segment(text: str) -> str:
    marker = "post-pr #105"
    normalized = _normalized(text)
    assert marker in normalized
    return normalized.split(marker, maxsplit=1)[1]


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


def test_agent_autonomy_runbook_declares_current_computed_coverage_baseline():
    """trace_ref: docs/00B_AGENT_BINDING_CONSTITUTION.md Role Boundaries."""
    content = _read_text(AGENT_AUTONOMY_RUNBOOK)

    for marker in CURRENT_BASELINE_MARKERS:
        assert marker in content


def test_agent_autonomy_runbook_declares_safe_gap_queue_after_pr_105():
    """trace_ref: docs/12_RUNTIME_EMBARGO_CONSTITUTION.md Embargo Rule."""
    content = _read_text(AGENT_AUTONOMY_RUNBOOK)

    for marker in SAFE_GAP_QUEUE_MARKERS:
        assert marker in content


def test_copilot_instructions_declare_current_pr_105_baseline():
    """trace_ref: docs/00B_AGENT_BINDING_CONSTITUTION.md Role Boundaries."""
    content = _read_text(COPILOT_INSTRUCTIONS)

    assert "PR #105" in content
    for marker in CURRENT_BASELINE_MARKERS:
        assert marker in content


def test_schema_only_boundary_preserved_after_pr_105():
    """trace_ref: docs/12_RUNTIME_EMBARGO_CONSTITUTION.md Embargo Rule."""
    for path in (AGENT_AUTONOMY_RUNBOOK, COPILOT_INSTRUCTIONS):
        content = _read_text(path)
        post_pr_105_segment = _post_pr_105_segment(content)

        assert "schema/fixture based only" in _normalized(content)
        assert "coverage runner" not in post_pr_105_segment
        assert "runtime readiness" not in post_pr_105_segment


def test_agent_autonomy_runbook_declares_stop_conditions():
    """trace_ref: docs/12_RUNTIME_EMBARGO_CONSTITUTION.md Explicit Prohibitions."""
    content = _normalized(_read_text(AGENT_AUTONOMY_RUNBOOK))

    assert "## stop conditions" in content
    assert "blocked" in content
    assert "runtime authorization" in content
    assert "rank promotion" in content


def test_agent_autonomy_runbook_includes_explicit_arabic_next_safe_step_prompt():
    """trace_ref: docs/00B_AGENT_BINDING_CONSTITUTION.md Role Boundaries."""
    content = _read_text(AGENT_AUTONOMY_RUNBOOK)
    assert ARABIC_NEXT_SAFE_STEP_PROMPT in content
