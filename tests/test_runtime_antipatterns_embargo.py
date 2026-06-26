"""Rejected runtime anti-pattern guardrails for PR #63 (docs + tests only).

Embargo drift mappings use exact phrases from the Runtime Embargo Constitution
as keys and tuples of corresponding audit guardrail markers as values. The
values must appear in the rejected-pattern document or audit-only registries.
"""

from __future__ import annotations

import io
import json
import re
import tokenize
from bisect import bisect_right
from pathlib import Path

import pytest

from tests.forbidden_runtime_artifacts import load_forbidden_runtime_artifact_paths
from tests.forbidden_runtime_patterns import (
    CANONICAL_FORBIDDEN_RUNTIME_PATTERNS_PATH,
    ForbiddenRuntimePattern,
    allowed_forbidden_runtime_pattern_paths,
    compile_forbidden_runtime_patterns,
    load_forbidden_runtime_patterns,
)
from tests.test_forbidden_runtime_pattern_fixtures import (
    ALLOWED_CONTEXT_NEGATIVE_FIXTURES,
    PATTERN_FIXTURES,
)

REPO_ROOT = Path(__file__).parent.parent
GUARD_DOC = REPO_ROOT / "docs" / "15_REJECTED_RUNTIME_PATTERNS.md"

FORBIDDEN_RUNTIME_ARTIFACT_PATHS = load_forbidden_runtime_artifact_paths()
FORBIDDEN_CANONICAL_RUNTIME_ARTIFACTS = tuple(
    REPO_ROOT / artifact for artifact in FORBIDDEN_RUNTIME_ARTIFACT_PATHS
)
RUNTIME_EMBARGO_DOC = REPO_ROOT / "docs" / "12_RUNTIME_EMBARGO_CONSTITUTION.md"
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
    "RUNTIME_PREDICATE_CLASS_FORBIDDEN",
    "RUNTIME_TRANSLATOR_CLASS_FORBIDDEN",
    "RUNTIME_PREDICATE_FIELD_FORBIDDEN",
    "RUNTIME_TRANSLATOR_FIELD_FORBIDDEN",
    "RUNTIME_DOMAIN_OPENING_CLASS_FORBIDDEN",
    "OPEN_RUNTIME_DOMAIN_CALL_FORBIDDEN",
    "COMPUTED_VERDICT_CLASS_FORBIDDEN",
    "COMPUTED_VERDICT_FIELD_FORBIDDEN",
    "MRK_DEFAULTS_FIELD_FORBIDDEN",
    "MANUAL_DASHBOARD_FIELD_FORBIDDEN",
    "EVIDENCE_LIST_AS_PROOF_PHRASE_FORBIDDEN",
    "MRK_BOOLEAN_DEFAULTS_PHRASE_FORBIDDEN",
    "DAL_ONLY_FORBIDDEN_OUTPUT_CONTRACT_FORBIDDEN",
    "LAFZI_FORM_FORBIDDEN_OUTPUT_CONTRACT_FORBIDDEN",
    "TRANSFORM_PASS_INLINE_FORBIDDEN",
    "TRANSFORM_PASS_ANNOTATED_FORBIDDEN",
    "TRANSFORM_PASS_MULTILINE_ANNOTATED_FORBIDDEN",
}

REQUIRED_DOC_PHRASES = [
    "Rejected Runtime Anti-Patterns",
    "This document records rejected patterns only.",
    "It is audit-only.",
    "The rejected artifacts and anti-patterns listed here are not future roadmap items.",
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
    "RuntimePredicate",
    "RuntimeTranslator",
    "runtime_predicate:",
    "runtime_translator:",
    "RuntimeDomainOpening",
    "open_runtime_domain(",
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
    "DAL_ONLY to produce root, weight, word, tool, meaning, isnad, ifadah, hukm, or tanzil.",
    "LAFZI_FORM to produce lexical meaning, usage, isnad, ifadah, hukm, or tanzil.",
]

FORBIDDEN_PATTERN_RECORDS = load_forbidden_runtime_patterns()
FORBIDDEN_PATTERN_RECORDS_BY_ID = {
    record.id: record for record in FORBIDDEN_PATTERN_RECORDS
}
FORBIDDEN_PATTERNS = compile_forbidden_runtime_patterns(FORBIDDEN_PATTERN_RECORDS)
FORBIDDEN_PATTERNS_BY_ID = {pattern.id: pattern for pattern in FORBIDDEN_PATTERNS}
# Essential subset of canonical artifact prohibitions for
# docs/12_RUNTIME_EMBARGO_CONSTITUTION.md Explicit Prohibitions.
ESSENTIAL_FORBIDDEN_ARTIFACT_NAMES = frozenset(
    {"binding_kernel.py", "decision_engine.py", "coverage_matrix_v0.1.yaml"}
)
# Keys are exact phrases from docs/12_RUNTIME_EMBARGO_CONSTITUTION.md; values
# are the corresponding audit guardrail markers in docs/15 or the registries.
EMBARGO_TO_REJECTED_PATTERN_MARKERS = {
    "binding_kernel.py": ("binding_kernel.py",),
    "decision_engine.py": ("decision_engine.py",),
    "coverage_matrix_v0.1.yaml": ("coverage_matrix_v0.1.yaml",),
    "Runtime predicates": ("RuntimePredicate", "runtime_predicate:"),
    "runtime translators": ("RuntimeTranslator", "runtime_translator:"),
    "Rank.CERTIFICATE": ("Rank.CERTIFICATE",),
    "manual computed verdict": ("ComputedVerdict", "computed_verdict"),
}
TRANSFORM_ANTIPATTERN_PATTERNS = tuple(
    pattern
    for pattern in FORBIDDEN_PATTERNS
    if pattern.id.startswith("TRANSFORM_PASS_")
)

ALLOWED_SUFFIXES = {".py", ".toml", ".yaml", ".yml"}
ALLOWED_EXCEPTION_PATHS = allowed_forbidden_runtime_pattern_paths(
    FORBIDDEN_PATTERN_RECORDS
)


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
        path for path in targets if path.is_file() and path not in ALLOWED_EXCEPTION_PATHS
    )


def path_matches_allowed_in(path: Path, allowed_in: tuple[str, ...]) -> bool:
    """Return whether a repository path is a registered allowed audit context."""
    try:
        relative_path = path.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        # Paths outside this repository are never registered allowed contexts.
        return False
    return relative_path in allowed_in


def pattern_violations_for_text(
    path: Path,
    text: str,
    patterns=FORBIDDEN_PATTERNS,
    records_by_id=FORBIDDEN_PATTERN_RECORDS_BY_ID,
) -> list[str]:
    """Return forbidden pattern violations for text outside allowed contexts."""
    if not patterns:
        raise ValueError("patterns must not be empty")
    if not records_by_id:
        raise ValueError("records_by_id must not be empty")
    violations: list[str] = []
    offsets = line_starts(text)
    for pattern in patterns:
        record = records_by_id[pattern.id]
        if path_matches_allowed_in(path, record.allowed_in):
            continue
        for match in pattern.matcher.finditer(text):
            line_number = line_number_at(offsets, match.start())
            matched_text = match.group(0)
            violations.append(
                f"pattern {pattern.id} matched '{matched_text}' at line {line_number}"
            )
    return violations


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


def line_starts(text: str) -> tuple[int, ...]:
    """Return zero-based offsets for the first character of each scan-text line."""
    offsets = [0]
    for idx, char in enumerate(text):
        if char == "\n":
            offsets.append(idx + 1)
    return tuple(offsets)


def line_number_at(offsets: tuple[int, ...], position: int) -> int:
    """Return the one-based line number where a zero-based text position occurs."""
    # The number of line starts less than or equal to position is the
    # corresponding one-based line number.
    return bisect_right(offsets, position)


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
    assert GUARD_DOC in ALLOWED_EXCEPTION_PATHS


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
        if "transform" in record.description.lower():
            assert record.id.startswith("TRANSFORM_PASS_")
        for allowed_path in record.allowed_in:
            assert not allowed_path.startswith(("/", "./", "../"))
            assert "\\" not in allowed_path
            assert "//" not in allowed_path
            assert not allowed_path.endswith("/")
            assert "/./" not in allowed_path
            assert "/../" not in allowed_path
    assert ALLOWED_EXCEPTION_PATHS == {GUARD_DOC}


def test_allowed_in_paths_are_existing_audit_document_contexts():
    """trace_ref: docs/12_RUNTIME_EMBARGO_CONSTITUTION.md Embargo Rule."""
    assert ALLOWED_EXCEPTION_PATHS
    for allowed_path in ALLOWED_EXCEPTION_PATHS:
        assert allowed_path.exists()
        assert allowed_path.is_file()
        assert allowed_path.is_relative_to(REPO_ROOT / "docs")
        assert allowed_path.suffix == ".md"


def test_forbidden_runtime_artifact_registry_covers_essential_antipattern_names():
    """trace_ref: docs/12_RUNTIME_EMBARGO_CONSTITUTION.md Explicit Prohibitions."""
    artifact_paths = load_forbidden_runtime_artifact_paths()
    names_by_path = {Path(artifact_path).name for artifact_path in artifact_paths}

    assert ESSENTIAL_FORBIDDEN_ARTIFACT_NAMES <= names_by_path
    assert all(not path.startswith(("/", "./", "../")) for path in artifact_paths)


def test_forbidden_runtime_artifact_registry_is_reflected_in_rejected_patterns_doc():
    """trace_ref: docs/12_RUNTIME_EMBARGO_CONSTITUTION.md Explicit Prohibitions."""
    content = GUARD_DOC.read_text(encoding="utf-8")
    artifact_paths = load_forbidden_runtime_artifact_paths()

    for artifact_path in artifact_paths:
        assert artifact_path in content
    for artifact_name in ESSENTIAL_FORBIDDEN_ARTIFACT_NAMES:
        assert artifact_name in content


def test_runtime_embargo_explicit_prohibitions_are_reflected_in_audit_guardrails():
    """trace_ref: docs/12_RUNTIME_EMBARGO_CONSTITUTION.md Explicit Prohibitions."""
    embargo_content = RUNTIME_EMBARGO_DOC.read_text(encoding="utf-8")
    rejected_content = GUARD_DOC.read_text(encoding="utf-8")
    artifact_registry_text = "\n".join(load_forbidden_runtime_artifact_paths())
    pattern_registry_text = "\n".join(
        f"{record.id}\n{record.pattern}\n{record.description}"
        for record in FORBIDDEN_PATTERN_RECORDS
    )
    audit_guardrail_text = "\n".join(
        (rejected_content, artifact_registry_text, pattern_registry_text)
    )

    for embargo_marker, guardrail_markers in EMBARGO_TO_REJECTED_PATTERN_MARKERS.items():
        assert embargo_marker in embargo_content
        assert any(marker in audit_guardrail_text for marker in guardrail_markers), (
            f"Runtime embargo marker must be reflected in audit guardrails: {embargo_marker}"
        )


def test_allowed_context_paths_are_audit_only_documentation():
    """trace_ref: docs/12_RUNTIME_EMBARGO_CONSTITUTION.md Embargo Rule."""
    for allowed_path in ALLOWED_EXCEPTION_PATHS:
        relative_path = allowed_path.relative_to(REPO_ROOT).as_posix()
        content = allowed_path.read_text(encoding="utf-8").casefold()

        assert relative_path.startswith("docs/")
        assert relative_path.endswith(".md")
        assert not allowed_path.is_relative_to(REPO_ROOT / "src")
        assert not allowed_path.is_relative_to(REPO_ROOT / "schemas")
        assert not allowed_path.is_relative_to(REPO_ROOT / "ci")
        assert not allowed_path.is_relative_to(REPO_ROOT / "tests")
        assert re.search(r"\baudit[-\s]+only\b", content)
        assert re.search(r"\bquoted[-\s]+anti-patterns?\b", content)


def test_registered_allowed_contexts_do_not_report_registered_antipattern_text():
    """trace_ref: docs/12_RUNTIME_EMBARGO_CONSTITUTION.md Embargo Rule."""
    for pattern_id, sample in ALLOWED_CONTEXT_NEGATIVE_FIXTURES.items():
        record = FORBIDDEN_PATTERN_RECORDS_BY_ID[pattern_id]
        assert FORBIDDEN_PATTERNS_BY_ID[pattern_id].matcher.search(sample)
        for allowed_path in record.allowed_in:
            path = REPO_ROOT / allowed_path
            assert not pattern_violations_for_text(path, sample), pattern_id


def test_guard_document_itself_is_allowed_audit_context_for_quoted_patterns():
    """trace_ref: docs/12_RUNTIME_EMBARGO_CONSTITUTION.md Embargo Rule."""
    content = GUARD_DOC.read_text(encoding="utf-8")
    assert not pattern_violations_for_text(GUARD_DOC, content)


def test_guard_document_quoted_patterns_fail_outside_allowed_context(
    tmp_path: Path,
):
    """trace_ref: docs/12_RUNTIME_EMBARGO_CONSTITUTION.md Embargo Rule."""
    copied_doc = tmp_path / "copied_rejected_runtime_patterns.md"
    content = GUARD_DOC.read_text(encoding="utf-8")

    violations = pattern_violations_for_text(copied_doc, content)

    assert violations
    assert any("Rank.CERTIFICATE" in violation for violation in violations)
    assert any("evidence list as proof" in violation for violation in violations)


def test_registered_antipattern_text_still_fails_outside_allowed_contexts(
    tmp_path: Path,
):
    """trace_ref: docs/12_RUNTIME_EMBARGO_CONSTITUTION.md Embargo Rule."""
    outside_path = tmp_path / "synthetic_runtime_antipattern.py"
    for pattern_id, sample in PATTERN_FIXTURES.items():
        violations = pattern_violations_for_text(outside_path, sample)
        assert any(f"pattern {pattern_id} " in violation for violation in violations)


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
        (
            "missing-allowed-in",
            [
                {
                    "id": "MISSING_ALLOWED_IN",
                    "pattern": "x",
                    "mode": "literal",
                    "description": "missing allowed paths",
                }
            ],
        ),
        (
            "empty-allowed-in",
            [
                {
                    "id": "EMPTY_ALLOWED_IN",
                    "pattern": "x",
                    "mode": "literal",
                    "description": "empty allowed paths",
                    "allowed_in": [],
                }
            ],
        ),
        (
            "non-string-allowed-in",
            [
                {
                    "id": "NON_STRING_ALLOWED_IN",
                    "pattern": "x",
                    "mode": "literal",
                    "description": "non-string allowed path",
                    "allowed_in": [1],
                }
            ],
        ),
        (
            "empty-string-allowed-in",
            [
                {
                    "id": "EMPTY_STRING_ALLOWED_IN",
                    "pattern": "x",
                    "mode": "literal",
                    "description": "empty-string allowed path",
                    "allowed_in": [""],
                }
            ],
        ),
        (
            "absolute-allowed-in",
            [
                {
                    "id": "ABSOLUTE_ALLOWED_IN",
                    "pattern": "x",
                    "mode": "literal",
                    "description": "absolute allowed path",
                    "allowed_in": ["/docs/15_REJECTED_RUNTIME_PATTERNS.md"],
                }
            ],
        ),
        (
            "relative-dot-allowed-in",
            [
                {
                    "id": "RELATIVE_DOT_ALLOWED_IN",
                    "pattern": "x",
                    "mode": "literal",
                    "description": "relative dot allowed path",
                    "allowed_in": ["./docs/15_REJECTED_RUNTIME_PATTERNS.md"],
                }
            ],
        ),
        (
            "relative-parent-allowed-in",
            [
                {
                    "id": "RELATIVE_PARENT_ALLOWED_IN",
                    "pattern": "x",
                    "mode": "literal",
                    "description": "relative parent allowed path",
                    "allowed_in": ["../docs/15_REJECTED_RUNTIME_PATTERNS.md"],
                }
            ],
        ),
        (
            "backslash-allowed-in",
            [
                {
                    "id": "BACKSLASH_ALLOWED_IN",
                    "pattern": "x",
                    "mode": "literal",
                    "description": "backslash allowed path",
                    "allowed_in": ["docs\\15_REJECTED_RUNTIME_PATTERNS.md"],
                }
            ],
        ),
        (
            "double-slash-allowed-in",
            [
                {
                    "id": "DOUBLE_SLASH_ALLOWED_IN",
                    "pattern": "x",
                    "mode": "literal",
                    "description": "double slash allowed path",
                    "allowed_in": ["docs//15_REJECTED_RUNTIME_PATTERNS.md"],
                }
            ],
        ),
        (
            "trailing-slash-allowed-in",
            [
                {
                    "id": "TRAILING_SLASH_ALLOWED_IN",
                    "pattern": "x",
                    "mode": "literal",
                    "description": "trailing slash allowed path",
                    "allowed_in": ["docs/15_REJECTED_RUNTIME_PATTERNS.md/"],
                }
            ],
        ),
        (
            "dot-segment-allowed-in",
            [
                {
                    "id": "DOT_SEGMENT_ALLOWED_IN",
                    "pattern": "x",
                    "mode": "literal",
                    "description": "dot segment allowed path",
                    "allowed_in": ["docs/./15_REJECTED_RUNTIME_PATTERNS.md"],
                }
            ],
        ),
        (
            "parent-segment-allowed-in",
            [
                {
                    "id": "PARENT_SEGMENT_ALLOWED_IN",
                    "pattern": "x",
                    "mode": "literal",
                    "description": "parent segment allowed path",
                    "allowed_in": ["docs/../docs/15_REJECTED_RUNTIME_PATTERNS.md"],
                }
            ],
        ),
        (
            "directory-wide-allowed-in",
            [
                {
                    "id": "DIRECTORY_WIDE_ALLOWED_IN",
                    "pattern": "x",
                    "mode": "literal",
                    "description": "directory allowed path",
                    "allowed_in": ["docs"],
                }
            ],
        ),
        (
            "stale-allowed-in",
            [
                {
                    "id": "STALE_ALLOWED_IN",
                    "pattern": "x",
                    "mode": "literal",
                    "description": "stale allowed path",
                    "allowed_in": ["docs/DOES_NOT_EXIST.md"],
                }
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
        file_violations = pattern_violations_for_text(path, scanned_text(path))
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
        "DAL_ONLY produces root",
        "LAFZI_FORM outputs lexical meaning",
        "def transform(self, operation: str): pass",
        "def transform(self, operation: str) -> \"SlotGeometry\":\n    pass",
        "def transform(self, operation: str):\n    pass",
        "def transform(self, operation: str) -> (\n    SlotGeometry\n):\n    pass",
        "class RuntimePredicate:\n    pass",
        "class RuntimeTranslator:\n    pass",
        "runtime_predicate: contract",
        "runtime_translator: contract",
        "RuntimeDomainOpening",
        "open_runtime_domain(DomainID.D3_LEXICAL_MADLUL)",
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


def test_line_number_lookup_handles_line_starts_and_mid_line_positions():
    """trace_ref: docs/12_RUNTIME_EMBARGO_CONSTITUTION.md Embargo Rule."""
    offsets = line_starts("a\nbc\ndef")
    assert offsets == (0, 2, 5)
    assert line_number_at(offsets, 0) == 1
    assert line_number_at(offsets, 1) == 1
    assert line_number_at(offsets, 2) == 2
    assert line_number_at(offsets, 4) == 2
    assert line_number_at(offsets, 5) == 3


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


def test_runtime_authority_antipatterns_match_representative_variants():
    compiled_by_id = {pattern.id: pattern.matcher for pattern in FORBIDDEN_PATTERNS}
    samples = {
        "RUNTIME_PREDICATE_CLASS_FORBIDDEN": "class RuntimePredicate:\n    pass",
        "RUNTIME_TRANSLATOR_CLASS_FORBIDDEN": "class RuntimeTranslator:\n    pass",
        "RUNTIME_PREDICATE_FIELD_FORBIDDEN": "runtime_predicate: contract",
        "RUNTIME_TRANSLATOR_FIELD_FORBIDDEN": "runtime_translator: contract",
        "RUNTIME_DOMAIN_OPENING_CLASS_FORBIDDEN": "RuntimeDomainOpening",
        "OPEN_RUNTIME_DOMAIN_CALL_FORBIDDEN": (
            "open_runtime_domain(DomainID.D3_LEXICAL_MADLUL)"
        ),
    }
    for pattern_id, sample in samples.items():
        assert compiled_by_id[pattern_id].search(sample), pattern_id
