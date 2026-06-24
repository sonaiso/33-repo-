"""Rejected runtime anti-pattern guardrails for PR #63 (docs + tests only)."""

from __future__ import annotations

import io
import re
import tokenize
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).parent.parent
GUARD_DOC = REPO_ROOT / "docs" / "15_REJECTED_RUNTIME_PATTERNS.md"

FORBIDDEN_RUNTIME_ARTIFACT_PATHS = (
    # Repo-relative forbidden artifact paths under the runtime embargo.
    # FORBIDDEN_CANONICAL_RUNTIME_ARTIFACTS prepends REPO_ROOT to these paths.
    "src/taaqqul_slot_geometry/L1/binding_kernel.py",
    "src/taaqqul_slot_geometry/L1/decision_engine.py",
    "src/taaqqul_slot_geometry/runtime/binding_kernel.py",
    "src/taaqqul_slot_geometry/runtime/decision_engine.py",
    "src/taaqqul_slot_geometry/core/binding_kernel.py",
    "src/taaqqul_slot_geometry/core/decision_engine.py",
    "coverage_matrix_v0.1.yaml",
    "docs/coverage_matrix_v0.1.yaml",
    "data/coverage_matrix_v0.1.yaml",
    "schemas/coverage_matrix_v0.1.yaml",
    "tests/test_binding_constraints.py",
    "l_protocol/contracts/binding_instructions.py",
    "l_protocol/engine/binding_kernel.py",
    "l_protocol/engine/decision_engine.py",
    "l_protocol/coverage_matrix_v0.1.yaml",
    "l_protocol/tests/test_binding_constraints.py",
)
FORBIDDEN_CANONICAL_RUNTIME_ARTIFACTS = tuple(
    REPO_ROOT / artifact for artifact in FORBIDDEN_RUNTIME_ARTIFACT_PATHS
)
CLASS_FIELD_LOOKAHEAD_LIMIT = 400
RETURN_TYPE_LOOKAHEAD_LIMIT = 120

REQUIRED_DOC_PHRASES = [
    "Rejected Runtime Anti-Patterns",
    "This document records rejected patterns only.",
    "It is audit-only.",
    # Canonical forbidden artifact paths — derived from FORBIDDEN_CANONICAL_RUNTIME_ARTIFACTS
    # so that this check stays in sync with the enforced canonical path list.
    # All paths in FORBIDDEN_CANONICAL_RUNTIME_ARTIFACTS are constructed as
    # REPO_ROOT / <subpath>, so .relative_to(REPO_ROOT) is always valid here.
    *(
        str(p.relative_to(REPO_ROOT)).replace("\\", "/")
        for p in FORBIDDEN_CANONICAL_RUNTIME_ARTIFACTS
    ),
    # Generic forbidden artifact names — required because the guard document
    # names these runtime artifacts without path qualification as well.
    *(
        p.name
        for p in FORBIDDEN_CANONICAL_RUNTIME_ARTIFACTS
        if p.name in {"binding_kernel.py", "decision_engine.py"}
    ),
    "MRK boolean defaults",
    "domain_proved: true",
    "unit_proved: true",
    "identity_preserved: true",
    "trace_preserved: true",
    "gate_passed: true",
    "identity_preserved: bool = True",
    "is_preserved: bool = True",
    "Rank.CERTIFICATE",
    "Rank.REJECTED",
    "ExecutionRank.CERTIFIED as runtime authority",
    "MRKProof",
    "IdentityProof",
    "GateProof",
    "BridgeProof",
    "EvidenceProof",
    "CoverageProof",
    "evidence list as proof",
    "if self.evidence: self.licensed = True",
    "def transform(self, operation: str): pass",
    "condition: str",
    "translator: str",
    "ComputedVerdict",
    "computed_verdict",
    "mrk_defaults",
    "YAML granting proof",
    "dashboard manual totals",
    "manual_dashboard",
    "expected_verdict",
    "computed verdict only after explicit runtime authorization",
    "All outputs are audit-only.",
    "Runtime embargo remains active.",
    "No runtime kernel.",
    "No runtime predicates.",
    "No runtime translators.",
    "No coverage runner.",
    "No runtime domain opening.",
    "Forbidden artifact lists must remain schema/test/doc consistent.",
    "Path-normalization variants are rejected before any forbidden artifact can be authorized.",
    "The guard scanner must detect both single-line and multi-line forms of rejected evidence and transform anti-patterns.",
]

FORBIDDEN_PATTERNS = [
    re.compile(r"\bBindingDecisionEngine\b"),
    re.compile(r"\bRank\.CERTIFICATE\b"),
    re.compile(r"\bRank\.REJECTED\b"),
    re.compile(r"\bExecutionRank\.CERTIFIED\b"),
    re.compile(r"\bdomain_proved\s*:\s*true\b", re.IGNORECASE),
    re.compile(r"\bunit_proved\s*:\s*true\b", re.IGNORECASE),
    re.compile(r"\bidentity_preserved\s*:\s*true\b", re.IGNORECASE),
    re.compile(r"\btrace_preserved\s*:\s*true\b", re.IGNORECASE),
    re.compile(r"\bgate_passed\s*:\s*true\b", re.IGNORECASE),
    re.compile(r"\bis_preserved\s*:\s*bool\s*=\s*true\b", re.IGNORECASE),
    re.compile(r"\bidentity_preserved\s*:\s*bool\s*=\s*true\b", re.IGNORECASE),
    re.compile(r"\bif\s+self\.evidence\s*:\s*self\.licensed\s*=\s*true\b", re.IGNORECASE),
    re.compile(
        r"\bif\s+self\.evidence\s*:\s*(?:\r?\n[ \t]*)+self\.licensed\s*=\s*true\b",
        re.IGNORECASE,
    ),
    re.compile(
        rf"\bclass\s+Bridge\b[\s\S]{{0,{CLASS_FIELD_LOOKAHEAD_LIMIT}}}\btranslator\s*:\s*str\b"
    ),
    re.compile(
        rf"\bclass\s+Gate\b[\s\S]{{0,{CLASS_FIELD_LOOKAHEAD_LIMIT}}}\bcondition\s*:\s*str\b"
    ),
    re.compile(r"\bComputedVerdict\b"),
    re.compile(r"\bcomputed_verdict\s*:"),
    re.compile(r"\bmrk_defaults\s*:"),
    re.compile(r"\bmanual_dashboard\s*:"),
    re.compile(r"\bevidence\s+list\s+as\s+proof\b"),
    re.compile(r"\bMRK\s+boolean\s+defaults\b"),
]

TRANSFORM_ANTIPATTERN_PATTERNS = [
    re.compile(
        r"\bdef\s+transform\s*\(\s*self\s*,\s*operation\s*:\s*str\s*\)\s*:\s*"
        r"(?:\r?\n[ \t]*)*pass\b"
    ),
    re.compile(
        r"\bdef\s+transform\s*\(\s*self\s*,\s*operation\s*:\s*str\s*\)\s*->\s*"
        r"[^:\n]+\s*:\s*(?:\r?\n[ \t]*)*pass\b"
    ),
    re.compile(
        r"\bdef\s+transform\s*\(\s*self\s*,\s*operation\s*:\s*str\s*\)\s*->\s*"
        rf"\([\s\S]{{0,{RETURN_TYPE_LOOKAHEAD_LIMIT}}}?\)\s*:\s*(?:\r?\n[ \t]*)*pass\b"
    ),
]

FORBIDDEN_PATTERNS.extend(TRANSFORM_ANTIPATTERN_PATTERNS)

ALLOWED_SUFFIXES = {".py", ".toml", ".yaml", ".yml"}
ALLOWED_EXCEPTION_PATH = GUARD_DOC


def scan_targets() -> list[Path]:
    """Collect paths where pre-runtime anti-patterns are forbidden."""
    targets: set[Path] = set()
    targets.update((REPO_ROOT / "src").rglob("*.py"))
    targets.update((REPO_ROOT / "schemas").rglob("*"))
    targets.update((REPO_ROOT / "tests").rglob("*.py"))
    targets.update((REPO_ROOT / "ci").rglob("*.py"))

    for pattern in ("*.toml", "*.yaml", "*.yml"):
        targets.update(REPO_ROOT.glob(pattern))
        targets.update((REPO_ROOT / "schemas").rglob(pattern))
        targets.update((REPO_ROOT / "ci").rglob(pattern))

    return sorted(
        path for path in targets if path.is_file() and path != ALLOWED_EXCEPTION_PATH
    )


def forbidden_runtime_files() -> list[Path]:
    """Return forbidden canonical runtime artifacts if they exist."""
    return [
        path
        for path in FORBIDDEN_CANONICAL_RUNTIME_ARTIFACTS
        if path.exists()
    ]


def scanned_text(path: Path) -> str:
    """Return scan text for a path, stripping Python comments and string literals."""
    text = path.read_text(encoding="utf-8")
    if path.suffix != ".py":
        return text

    tokens: list[tuple[int, str]] = []
    try:
        for token in tokenize.generate_tokens(io.StringIO(text).readline):
            if token.type in {tokenize.COMMENT, tokenize.STRING}:
                continue
            tokens.append((token.type, token.string))
    except tokenize.TokenError:
        return text

    return tokenize.untokenize(tokens)


@pytest.fixture(scope="module")
def scanned_targets() -> list[Path]:
    return scan_targets()


def test_scanned_targets_are_expected_embargo_scope(scanned_targets: list[Path]):
    """trace_ref: docs/12_RUNTIME_EMBARGO_CONSTITUTION.md Embargo Rule."""
    targets = scanned_targets
    assert targets, "scan targets must not be empty"
    assert all(path.is_file() for path in targets)
    assert all(
        path.suffix in ALLOWED_SUFFIXES or path.is_relative_to(REPO_ROOT / "schemas")
        for path in targets
    )
    assert any(path.is_relative_to(REPO_ROOT / "src") for path in targets)
    assert any(path.is_relative_to(REPO_ROOT / "schemas") for path in targets)
    assert any(path.is_relative_to(REPO_ROOT / "tests") for path in targets)
    assert any(path.is_relative_to(REPO_ROOT / "ci") for path in targets)
    assert REPO_ROOT / "pyproject.toml" in targets
    assert GUARD_DOC not in targets


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
        str(path.relative_to(REPO_ROOT)) for path in matches
    )


def test_source_and_config_files_block_rejected_runtime_anti_patterns(
    scanned_targets: list[Path],
):
    """trace_ref: docs/12_RUNTIME_EMBARGO_CONSTITUTION.md Embargo Rule."""
    violations: list[str] = []
    for path in scanned_targets:
        text = scanned_text(path)
        file_violations: list[str] = []
        for pattern in FORBIDDEN_PATTERNS:
            for match in pattern.finditer(text):
                line_number = text.count("\n", 0, match.start()) + 1
                matched_text = match.group(0)
                file_violations.append(
                    f"pattern '{pattern.pattern}' matched '{matched_text}' at line {line_number}"
                )
        if file_violations:
            violations.append(f"{path}: " + ", ".join(file_violations))

    assert not violations, "\n" + "\n".join(violations)


def test_antipattern_regexes_match_case_and_multiline_variants():
    samples = [
        "domain_proved: TRUE",
        "unit_proved: TrUe",
        "identity_preserved: true",
        "trace_preserved: True",
        "gate_passed: tRuE",
        "identity_preserved: bool = TRUE",
        "is_preserved: bool = TRUE",
        "if self.evidence: self.licensed = TRUE",
        "if self.evidence:\n    self.licensed = TRUE",
        "if self.evidence:\n\n    self.licensed = TRUE",
        "ExecutionRank.CERTIFIED",
        "def transform(self, operation: str): pass",
        "def transform(self, operation: str) -> \"SlotGeometry\":\n    pass",
        "def transform(self, operation: str):\n    pass",
        "def transform(self, operation: str) -> (\n    SlotGeometry\n):\n    pass",
    ]
    for sample in samples:
        assert any(pattern.search(sample) for pattern in FORBIDDEN_PATTERNS)


def test_python_comments_and_strings_are_ignored_for_antipattern_scan(tmp_path: Path):
    path = tmp_path / "example.py"
    path.write_text(
        (
            "# domain_proved: TRUE\n"
            "\"\"\"Rank.CERTIFICATE appears only in doc text.\"\"\"\n"
            "msg = \"identity_preserved: true\"\n"
            "safe_value = 1\n"
        ),
        encoding="utf-8",
    )
    stripped = scanned_text(path)
    assert "domain_proved" not in stripped
    assert "Rank.CERTIFICATE" not in stripped
    assert "identity_preserved" not in stripped


def test_transform_antipattern_regexes_cover_annotation_variants():
    samples = [
        "def transform(self, operation: str): pass",
        "def transform(self, operation: str):\n    pass",
        "def transform(self, operation: str) -> \"SlotGeometry\":\n    pass",
        "def transform(self, operation: str) -> (\n    SlotGeometry\n):\n    pass",
    ]
    for sample in samples:
        assert any(pattern.search(sample) for pattern in TRANSFORM_ANTIPATTERN_PATTERNS)
