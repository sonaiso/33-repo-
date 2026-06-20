"""Runtime embargo guardrails for PR #38 (docs + tests only)."""
from io import StringIO
from pathlib import Path
import tokenize


REPO_ROOT = Path(__file__).parent.parent
EMBARGO_DOC = REPO_ROOT / "docs" / "12_RUNTIME_EMBARGO_CONSTITUTION.md"
L1_SOURCE = REPO_ROOT / "src" / "taaqqul_slot_geometry" / "L1"

FORBIDDEN_FILES = [
    REPO_ROOT / "src" / "taaqqul_slot_geometry" / "L1" / "binding_kernel.py",
    REPO_ROOT / "src" / "taaqqul_slot_geometry" / "L1" / "decision_engine.py",
    REPO_ROOT / "coverage_matrix_v0.1.yaml",
]

RANK_PATTERNS = [
    "Rank.CERTIFICATE",
    "Rank.REJECTED",
]

RUNTIME_PATTERNS = [
    "computed_verdict:",
    "mrk_defaults:",
]

BOOLEAN_PROOF_REGEXES = [
    r"\bdomain_proved\s*:\s*bool\b",
    r"\bidentity_preserved\s*:\s*bool\b",
    r"\bgate_passed\s*:\s*bool\b",
]


REQUIRED_EMBARGO_PHRASES = [
    "Runtime remains embargoed",
    "D1_DAL_ONLY contracts are frozen.",
    "D2_LAFZI_FORM contracts are frozen.",
    "DalToLafziBridgeSpec is declared.",
    "FailureAlignment is audit-clean.",
    "ProofObject references have stable failure policies.",
    "No Boolean-as-proof remains in proposed runtime specs.",
    "No Rank.CERTIFICATE exists in L1.",
    "No manual computed verdict exists.",
    "binding_kernel.py is forbidden before embargo lift.",
    "coverage_matrix_v0.1.yaml is forbidden before computed coverage schema.",
]




def _code_without_comments_or_strings(path: Path) -> str:
    """Return source tokens without comments/strings for executable-pattern checks."""
    source = path.read_text(encoding="utf-8")
    tokens = tokenize.generate_tokens(StringIO(source).readline)
    parts: list[str] = []
    for token in tokens:
        if token.type in {tokenize.COMMENT, tokenize.STRING}:
            continue
        parts.append(token.string)
    return " ".join(parts)


def test_runtime_embargo_document_exists_and_declares_authority():
    """trace_ref: docs/00_MAQOOL_CONSTITUTION.md Rule 5 (named failures)."""
    assert EMBARGO_DOC.exists()
    content = EMBARGO_DOC.read_text(encoding="utf-8")
    for phrase in REQUIRED_EMBARGO_PHRASES:
        assert phrase in content, f"Missing embargo phrase: {phrase}"


def test_runtime_embargo_forbidden_files_absent():
    """trace_ref: docs/12_RUNTIME_EMBARGO_CONSTITUTION.md Explicit Prohibitions."""
    for forbidden in FORBIDDEN_FILES:
        assert not forbidden.exists(), f"Forbidden pre-embargo artifact exists: {forbidden}"


def test_runtime_embargo_forbidden_tokens_absent_in_l1_source_only():
    """trace_ref: docs/12_RUNTIME_EMBARGO_CONSTITUTION.md Embargo Rule (PR #38)."""
    import re

    for path in L1_SOURCE.glob("*.py"):
        source = _code_without_comments_or_strings(path)
        for pattern in RANK_PATTERNS:
            assert pattern not in source, f"Forbidden token '{pattern}' found in {path}"
        for regex in BOOLEAN_PROOF_REGEXES:
            assert not re.search(regex, source), f"Forbidden boolean-proof field found in {path}"
        for pattern in RUNTIME_PATTERNS:
            assert pattern not in source, f"Forbidden token '{pattern}' found in {path}"
