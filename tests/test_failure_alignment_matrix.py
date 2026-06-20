"""Failure-alignment audit-only matrix checks for PR #38."""
from __future__ import annotations

import csv
from pathlib import Path

import pytest

from taaqqul_slot_geometry.constitution.failure_taxonomy import FailureCode


REPO_ROOT = Path(__file__).parent.parent
ALIGNMENT_DOC = REPO_ROOT / "docs" / "13_FAILURE_ALIGNMENT_CONSTITUTION.md"
ALIGNMENT_CSV = REPO_ROOT / "data" / "failure_alignment.csv"

AUDIT_ONLY_MARKER = "AUDIT_ONLY"

REQUIRED_COLUMNS = {
    "row_id",
    "audit_scope",
    "legacy_label",
    "primary_canonical_code",
    "secondary_canonical_codes",
    "is_executable_row",
    "executable_mapping",
    "notes",
}


def _parse_bool_string(value: str) -> bool:
    """Parse CSV boolean text values such as true/false into bool."""
    return (value or "").strip().lower() == "true"


@pytest.fixture(scope="module")
def alignment_rows() -> list[dict[str, str]]:
    with ALIGNMENT_CSV.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        assert reader.fieldnames is not None
        missing = REQUIRED_COLUMNS - set(reader.fieldnames)
        assert not missing, f"failure_alignment.csv missing columns: {sorted(missing)}"
        return list(reader)


def test_failure_alignment_document_declares_audit_only_status():
    """trace_ref: docs/00_MAQOOL_CONSTITUTION.md Rule 5 (named failures)."""
    assert ALIGNMENT_DOC.exists()
    content = ALIGNMENT_DOC.read_text(encoding="utf-8")
    assert "FailureAlignment is audit-only." in content
    assert "FailureAlignment does not replace FailureCode." in content
    assert "FailureAlignment does not open runtime." in content


def test_failure_alignment_csv_exists_and_non_empty(alignment_rows: list[dict[str, str]]):
    """trace_ref: docs/13_FAILURE_ALIGNMENT_CONSTITUTION.md Alignment Constraints."""
    assert ALIGNMENT_CSV.exists()
    assert alignment_rows, "failure_alignment.csv must contain at least one audit row"


def test_every_row_has_primary_canonical_code(alignment_rows: list[dict[str, str]]):
    """trace_ref: docs/13_FAILURE_ALIGNMENT_CONSTITUTION.md Alignment Constraints."""
    for row in alignment_rows:
        primary = (row["primary_canonical_code"] or "").strip()
        assert primary, f"row {row['row_id']} is missing primary_canonical_code"
        assert primary.upper() != "NONE", f"row {row['row_id']} cannot use NONE as primary"


def test_alignment_covers_all_failure_codes(alignment_rows: list[dict[str, str]]):
    """trace_ref: docs/13_FAILURE_ALIGNMENT_CONSTITUTION.md Audit-Only Law (PR #38)."""
    expected = {failure_code.name for failure_code in FailureCode}
    actual = {(row["primary_canonical_code"] or "").strip() for row in alignment_rows}
    assert expected <= actual, (
        "failure_alignment.csv must include an audit row for every canonical FailureCode"
    )


def test_alignment_primary_codes_are_unique(alignment_rows: list[dict[str, str]]):
    """trace_ref: docs/13_FAILURE_ALIGNMENT_CONSTITUTION.md Alignment Constraints."""
    expected = {failure_code.name for failure_code in FailureCode}
    seen: set[str] = set()
    for row in alignment_rows:
        primary = (row["primary_canonical_code"] or "").strip()
        assert primary in expected, f"row {row['row_id']} has unknown primary code: {primary}"
        assert primary not in seen, f"primary_canonical_code duplicated: {primary}"
        seen.add(primary)


def test_executable_rows_require_non_none_mapping(alignment_rows: list[dict[str, str]]):
    """trace_ref: docs/13_FAILURE_ALIGNMENT_CONSTITUTION.md Alignment Constraints."""
    for row in alignment_rows:
        is_executable = _parse_bool_string(row["is_executable_row"])
        mapping = (row["executable_mapping"] or "").strip().upper()
        if is_executable:
            assert mapping not in {"", "NONE"}, (
                f"row {row['row_id']} is executable and cannot map to NONE"
            )


def test_all_rows_stay_non_executable_while_embargoed(
    alignment_rows: list[dict[str, str]],
):
    """trace_ref: docs/12_RUNTIME_EMBARGO_CONSTITUTION.md Embargo Rule (PR #38)."""
    for row in alignment_rows:
        assert not _parse_bool_string(row["is_executable_row"]), (
            f"row {row['row_id']} cannot become executable before runtime embargo lift"
        )


def test_audit_rows_remain_non_executable(alignment_rows: list[dict[str, str]]):
    """trace_ref: docs/13_FAILURE_ALIGNMENT_CONSTITUTION.md Audit-Only Law (PR #38)."""
    for row in alignment_rows:
        is_executable = _parse_bool_string(row["is_executable_row"])
        mapping = (row["executable_mapping"] or "").strip().upper()
        if not is_executable:
            assert mapping == AUDIT_ONLY_MARKER, (
                f"row {row['row_id']} must stay AUDIT_ONLY while runtime is embargoed"
            )
