"""Rejected runtime anti-pattern guardrails for PR #63 (docs + tests only)."""

from __future__ import annotations

import io
import json
import re
import tokenize
from pathlib import Path

import pytest

from tests.forbidden_runtime_artifacts import load_forbidden_runtime_artifact_paths
from tests.forbidden_runtime_patterns import (
    CANONICAL_FORBIDDEN_RUNTIME_PATTERNS_PATH,
    ForbiddenRuntimePattern,
    compile_forbidden_runtime_patterns,
    load_forbidden_runtime_patterns,
)

REPO_ROOT = Path(__file__).parent.parent
GUARD_DOC = REPO_ROOT / "docs" / "15_REJECTED_RUNTIME_PATTERNS.md"

FORBIDDEN_RUNTIME_ARTIFACT_PATHS = load_forbidden_runtime_artifact_paths()
FORBIDDEN_CANONICAL_RUNTIME_ARTIFACTS = tuple(
    REPO_ROOT / artifact for artifact in FORBIDDEN_RUNTIME_ARTIFACT_PATHS
)
CLASS_FIELD_LOOKAHEAD_LIMIT = 400
RETURN_TYPE_LOOKAHEAD_LIMIT = 120
REQUIRED_PATTERN_IDS = {
    "BINDING_DECISION_ENGINE_FORBIDDEN",
    "RANK_CERTIFICATE_FORBIDDEN",
    "RANK_REJECTED_FORBIDDEN",
    "EXECUTION_RANK_CERTIFIED_FORBIDDEN",
    "MRK_BOOLEAN_DEFAULT_DOMAIN_PROVED",
    "MRK_BOOLEAN_DEFAULT_UNIT_PROVED",
    "MRK_BOOLEAN_DEFAULT_IDENTITY_PRESERVED",
    "MRK_BOOLEAN_DEFAULT_TRACE_PRESERVED",
    "MRK_BOOLEAN_DEFAULT_GATE_PASSED",
    "IS_PRESERVED_TRUE_FIELD_FORBIDDEN",
    "IDENTITY_PRESERVED_TRUE_FIELD_FORBIDDEN",
    "EVIDENCE_LIST_INLINE_LICENSE_FORBIDDEN",
    "EVIDENCE_LIST_MULTILINE_LICENSE_FORBIDDEN",
    "TEXT_ONLY_BRIDGE_TRANSLATOR_FORBIDDEN",
    "TEXT_ONLY_GATE_CONDITION_FORBIDDEN",
    "COMPUTED_VERDICT_CLASS_FORBIDDEN",
    "COMPUTED_VERDICT_FIELD_FORBIDDEN",
    "MRK_DEFAULTS_FIELD_FORBIDDEN",
    "MANUAL_DASHBOARD_FIELD_FORBIDDEN",
    "EVIDENCE_LIST_AS_PROOF_PHRASE_FORBIDDEN",
    "MRK_BOOLEAN_DEFAULTS_PHRASE_FORBIDDEN",
    "TRANSFORM_PASS_INLINE_FORBIDDEN",
    "TRANSFORM_PASS_ANNOTATED_FORBIDDEN",
    "TRANSFORM_PASS_MULTILINE_ANNOTATED_FORBIDDEN",
}

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
    "Canonical forbidden-path source of truth: `data/forbidden_runtime_artifacts.json` (audit-only).",
    "Canonical forbidden-pattern source of truth: `data/forbidden_runtime_patterns.json` (audit-only).",
    "Path-normalization variants are rejected before any forbidden artifact can be authorized.",
    "The guard scanner must detect both single-line and multi-line forms of rejected evidence and transform anti-patterns.",
]

FORBIDDEN_PATTERN_RECORDS = load_forbidden_runtime_patterns()
FORBIDDEN_PATTERNS = compile_forbidden_runtime_patterns(FORBIDDEN_PATTERN_RECORDS)
TRANSFORM_ANTIPATTERN_PATTERNS = tuple(
    pattern
    for pattern in FORBIDDEN_PATTERNS
    if pattern.id.startswith("TRANSFORM_PASS_")
)

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


def test_forbidden_runtime_pattern_registry_is_canonical_and_valid():
    """trace_ref: docs/12_RUNTIME_EMBARGO_CONSTITUTION.md Embargo Rule."""
    assert CANONICAL_FORBIDDEN_RUNTIME_PATTERNS_PATH.exists()
    records = FORBIDDEN_PATTERN_RECORDS
    assert records, "forbidden runtime pattern registry must not be empty"
    assert {record.id for record in records}.issuperset(REQUIRED_PATTERN_IDS)
    assert len({record.id for record in records}) == len(records)
    assert len({(record.mode, record.pattern) for record in records}) == len(records)

    for record in records:
        assert record.mode in {"regex", "literal"}
        assert record.description
        assert record.allowed_in
        for allowed_path in record.allowed_in:
            assert not allowed_path.startswith(("/", "./", "../"))
            assert "\\" not in allowed_path
            assert "//" not in allowed_path
            assert not allowed_path.endswith("/")
            assert "/./" not in allowed_path
            assert "/../" not in allowed_path


def test_forbidden_runtime_pattern_loader_reports_missing_file(tmp_path: Path):
    """trace_ref: docs/12_RUNTIME_EMBARGO_CONSTITUTION.md Embargo Rule."""
    missing = tmp_path / "missing.json"
    with pytest.raises(RuntimeError, match="Missing canonical forbidden runtime pattern list"):
        load_forbidden_runtime_patterns(missing)


def test_forbidden_runtime_pattern_loader_reports_invalid_json(tmp_path: Path):
    """trace_ref: docs/12_RUNTIME_EMBARGO_CONSTITUTION.md Embargo Rule."""
    invalid = tmp_path / "patterns.json"
    invalid.write_text("{", encoding="utf-8")
    with pytest.raises(RuntimeError, match="Invalid JSON in canonical forbidden runtime pattern list"):
        load_forbidden_runtime_patterns(invalid)


def test_forbidden_runtime_pattern_loader_rejects_invalid_payloads(tmp_path: Path):
    """trace_ref: docs/12_RUNTIME_EMBARGO_CONSTITUTION.md Embargo Rule."""
    invalid_payloads = [
        ("not-a-list", {"id": "X"}),
        ("not-an-object", ["X"]),
        ("missing-field", [{"id": "X"}]),
        (
            "invalid-mode",
            [
                {
                    "id": "INVALID_MODE",
                    "pattern": "x",
                    "mode": "glob",
                    "description": "invalid mode",
                    "allowed_in": ["docs/15_REJECTED_RUNTIME_PATTERNS.md"],
                }
            ],
        ),
        (
            "invalid-regex",
            [
                {
                    "id": "INVALID_REGEX",
                    "pattern": "[",
                    "mode": "regex",
                    "description": "invalid regex",
                    "allowed_in": ["docs/15_REJECTED_RUNTIME_PATTERNS.md"],
                }
            ],
        ),
        (
            "duplicate-allowed-in",
            [
                {
                    "id": "DUPLICATE_ALLOWED_IN",
                    "pattern": "x",
                    "mode": "literal",
                    "description": "duplicate allowed paths",
                    "allowed_in": [
                        "docs/15_REJECTED_RUNTIME_PATTERNS.md",
                        "docs/15_REJECTED_RUNTIME_PATTERNS.md",
                    ],
                }
            ],
        ),
        (
            "duplicate-id",
            [
                {
                    "id": "DUPLICATE_ID",
                    "pattern": "x",
                    "mode": "literal",
                    "description": "first",
                    "allowed_in": ["docs/15_REJECTED_RUNTIME_PATTERNS.md"],
                },
                {
                    "id": "DUPLICATE_ID",
                    "pattern": "y",
                    "mode": "literal",
                    "description": "second",
                    "allowed_in": ["docs/15_REJECTED_RUNTIME_PATTERNS.md"],
                },
            ],
        ),
        (
            "duplicate-pattern-mode",
            [
                {
                    "id": "DUPLICATE_PATTERN_A",
                    "pattern": "x",
                    "mode": "literal",
                    "description": "first",
                    "allowed_in": ["docs/15_REJECTED_RUNTIME_PATTERNS.md"],
                },
                {
                    "id": "DUPLICATE_PATTERN_B",
                    "pattern": "x",
                    "mode": "literal",
                    "description": "second",
                    "allowed_in": ["docs/15_REJECTED_RUNTIME_PATTERNS.md"],
                },
            ],
        ),
    ]

    for name, payload in invalid_payloads:
        path = tmp_path / f"{name}.json"
        path.write_text(json.dumps(payload), encoding="utf-8")
        with pytest.raises((RuntimeError, ValueError)):
            load_forbidden_runtime_patterns(path)


def test_forbidden_runtime_pattern_loader_supports_literal_mode():
    """trace_ref: docs/12_RUNTIME_EMBARGO_CONSTITUTION.md Embargo Rule."""
    compiled = compile_forbidden_runtime_patterns(
        (
            ForbiddenRuntimePattern(
                id="LITERAL_DOT_PATTERN",
                pattern="Rank.CERTIFICATE",
                mode="literal",
                description="literal matching escapes regex metacharacters",
                allowed_in=("docs/15_REJECTED_RUNTIME_PATTERNS.md",),
            ),
        )
    )
    assert compiled[0].matcher.search("Rank.CERTIFICATE")
    assert not compiled[0].matcher.search("RankXCERTIFICATE")


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
            for match in pattern.matcher.finditer(text):
                line_number = text.count("\n", 0, match.start()) + 1
                matched_text = match.group(0)
                file_violations.append(
                    f"pattern {pattern.id} matched '{matched_text}' at line {line_number}"
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
        assert any(pattern.matcher.search(sample) for pattern in FORBIDDEN_PATTERNS)


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
        assert any(
            pattern.matcher.search(sample)
            for pattern in TRANSFORM_ANTIPATTERN_PATTERNS
        )
