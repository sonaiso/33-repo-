"""Failure-alignment audit-only matrix checks for PR #38."""
from __future__ import annotations

import csv
from pathlib import Path


REPO_ROOT = Path(__file__).parent.parent
ALIGNMENT_DOC = REPO_ROOT / "docs" / "13_FAILURE_ALIGNMENT_CONSTITUTION.md"
ALIGNMENT_CSV = REPO_ROOT / "data" / "failure_alignment.csv"

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


def _read_rows() -> list[dict[str, str]]:
    with ALIGNMENT_CSV.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        assert reader.fieldnames is not None
        missing = REQUIRED_COLUMNS - set(reader.fieldnames)
        assert not missing, f"failure_alignment.csv missing columns: {sorted(missing)}"
        return list(reader)


def test_failure_alignment_document_declares_audit_only_status():
    """trace_ref: docs/00_MAQOOL_CONSTITUTION.md §5."""
    assert ALIGNMENT_DOC.exists()
    content = ALIGNMENT_DOC.read_text(encoding="utf-8")
    assert "FailureAlignment is audit-only." in content
    assert "FailureAlignment does not replace FailureCode." in content
    assert "FailureAlignment does not open runtime." in content


def test_failure_alignment_csv_exists_and_non_empty():
    """trace_ref: docs/13_FAILURE_ALIGNMENT_CONSTITUTION.md Alignment Constraints."""
    assert ALIGNMENT_CSV.exists()
    rows = _read_rows()
    assert rows, "failure_alignment.csv must contain at least one audit row"


def test_every_row_has_primary_canonical_code():
    """trace_ref: docs/13_FAILURE_ALIGNMENT_CONSTITUTION.md Alignment Constraints."""
    for row in _read_rows():
        primary = (row["primary_canonical_code"] or "").strip()
        assert primary, f"row {row['row_id']} is missing primary_canonical_code"
        assert primary.upper() != "NONE", f"row {row['row_id']} cannot use NONE as primary"


def test_executable_rows_cannot_use_none_mapping_and_audit_rows_stay_non_executable():
    """trace_ref: docs/13_FAILURE_ALIGNMENT_CONSTITUTION.md Audit-Only Law (PR #38)."""
    for row in _read_rows():
        is_executable = (row["is_executable_row"] or "").strip().lower() == "true"
        mapping = (row["executable_mapping"] or "").strip().upper()
        if is_executable:
            assert mapping not in {"", "NONE"}, (
                f"row {row['row_id']} is executable and cannot map to NONE"
            )
        else:
            assert mapping == "AUDIT_ONLY", (
                f"row {row['row_id']} must stay AUDIT_ONLY while runtime is embargoed"
            )
