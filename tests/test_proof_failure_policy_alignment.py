"""Audit-only ProofObject failure-policy alignment checks for PR #61."""

from __future__ import annotations

from pathlib import Path
import re

import pytest


REPO_ROOT = Path(__file__).parent.parent
ALIGNMENT_DOC = REPO_ROOT / "docs" / "16_PROOF_FAILURE_POLICY_ALIGNMENT.md"
EMBARGO_DOC = REPO_ROOT / "docs" / "12_RUNTIME_EMBARGO_CONSTITUTION.md"

REQUIRED_PROOF_KINDS = {
    "MRKProof": "PROOF_MRK",
    "DomainProof": "DOMAIN",
    "IdentityProof": "IDENTITY",
    "GateProof": "GATE",
    "BridgeProof": "BRIDGE",
    "EvidenceProof": "EVIDENCE",
    "CoverageProof": "COVERAGE",
}

FORBIDDEN_TOKENS = (
    "ComputedVerdict",
    "Rank.CERTIFICATE",
    "Rank.REJECTED",
)


SAFE_CANONICAL_FAMILY_PATTERN = re.compile(r"^[A-Z][A-Z0-9_]*$")

REQUIRED_COLUMNS = (
    "proof_kind",
    "missing_policy",
    "broken_policy",
    "canonical_family",
    "proof_obligation",
    "runtime_status",
    "is_executable",
    "preserves_failure_code",
    "rank_ceiling",
)



def _is_markdown_separator_row(columns: list[str]) -> bool:
    normalized = [cell.replace(" ", "") for cell in columns]
    return all(
        cell
        and "-" in cell
        and all(symbol in {"-", ":"} for symbol in cell)
        for cell in normalized
    )


def parse_alignment_rows() -> list[dict[str, str]]:
    content = ALIGNMENT_DOC.read_text(encoding="utf-8")
    lines = content.splitlines()

    rows: list[dict[str, str]] = []
    seen_table_header = False
    for line in lines:
        if not line.startswith("|"):
            continue

        cols = [part.strip() for part in line.strip().strip("|").split("|")]
        if tuple(cols) == REQUIRED_COLUMNS:
            seen_table_header = True
            continue
        if seen_table_header and _is_markdown_separator_row(cols):
            continue

        if seen_table_header and len(cols) == len(REQUIRED_COLUMNS):
            rows.append(dict(zip(REQUIRED_COLUMNS, cols)))

    return rows


@pytest.fixture(scope="module")
def rows() -> list[dict[str, str]]:
    assert ALIGNMENT_DOC.exists(), "Alignment document must exist"
    parsed_rows = parse_alignment_rows()
    assert parsed_rows, "Alignment matrix must have audit rows"
    return parsed_rows


@pytest.fixture(scope="module")
def row_by_kind(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    return {row["proof_kind"]: row for row in rows}



def test_alignment_doc_declares_audit_only_failure_policy_law():
    """trace_ref: docs/12_RUNTIME_EMBARGO_CONSTITUTION.md Embargo Rule."""
    content = ALIGNMENT_DOC.read_text(encoding="utf-8")
    assert "No ProofObject failure policy is executable before runtime embargo lift." in content
    assert "Failure policies are audit-only alignment metadata." in content
    assert "No proof policy may replace FailureCode." in content



def test_all_required_proof_kinds_present(row_by_kind: dict[str, dict[str, str]]):
    """trace_ref: docs/08_PROOF_OBJECT_CONSTITUTION.md Required proof objects."""
    assert set(REQUIRED_PROOF_KINDS) <= set(row_by_kind)



def test_each_row_has_required_policy_fields(rows: list[dict[str, str]]):
    """trace_ref: docs/13_FAILURE_ALIGNMENT_CONSTITUTION.md Alignment Constraints."""
    for row in rows:
        assert row["proof_kind"]
        assert row["missing_policy"]
        assert row["broken_policy"]
        assert row["canonical_family"]
        assert row["proof_obligation"]



def test_all_rows_stay_audit_only_non_executable(rows: list[dict[str, str]]):
    """trace_ref: docs/12_RUNTIME_EMBARGO_CONSTITUTION.md Embargo Rule."""
    for row in rows:
        assert row["runtime_status"] == "AUDIT_ONLY"
        assert row["is_executable"].lower() == "false"



def test_all_rows_preserve_failure_code_and_candidate_ceiling(rows: list[dict[str, str]]):
    """trace_ref: docs/00A_CONSTITUTIONAL_PROGRAMMING_AMENDMENT.md L1 Output Envelope."""
    for row in rows:
        assert row["preserves_failure_code"].lower() == "true"
        assert row["rank_ceiling"] == "CANDIDATE"



def test_no_forbidden_runtime_verdict_or_rank_tokens_in_alignment_doc():
    """trace_ref: docs/15_REJECTED_RUNTIME_PATTERNS.md Rejected patterns."""
    row_text = "\n".join(
        " | ".join(row[column] for column in REQUIRED_COLUMNS) for row in parse_alignment_rows()
    )
    for token in FORBIDDEN_TOKENS:
        assert token not in row_text



def test_required_family_mappings(row_by_kind: dict[str, dict[str, str]]):
    """trace_ref: docs/13_FAILURE_ALIGNMENT_CONSTITUTION.md Canonical Family Set."""
    for proof_kind, expected_family in REQUIRED_PROOF_KINDS.items():
        assert row_by_kind[proof_kind]["canonical_family"] == expected_family


def test_canonical_family_values_are_schema_safe(rows: list[dict[str, str]]):
    """trace_ref: docs/13_FAILURE_ALIGNMENT_CONSTITUTION.md Canonical Family Set."""
    for row in rows:
        family = row["canonical_family"]
        assert SAFE_CANONICAL_FAMILY_PATTERN.fullmatch(family), (
            f"canonical_family must be schema-safe, got: {family}"
        )


def test_runtime_embargo_doc_still_declares_embargo_active():
    """trace_ref: docs/12_RUNTIME_EMBARGO_CONSTITUTION.md Embargo Rule."""
    content = EMBARGO_DOC.read_text(encoding="utf-8")
    assert "Runtime remains embargoed" in content
