"""Failure-alignment audit-only matrix checks for PR #55."""
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
    "canonical_family",
    "domain_scope",
    "proof_obligation",
    "residual_policy",
    "forbidden_runtime_use",
    "is_executable_row",
    "executable_mapping",
    "notes",
}

CANONICAL_FAMILIES = {
    "TRACE",
    "RANK",
    "IDENTITY",
    "LAYER_LEAP",
    "MEANING_LEAK",
    "IFADAH_LEAK",
    "RELATION_PREREQUISITE",
    "HUKM_PREREQUISITE",
    "TANZIL_PREREQUISITE",
    "L0_SPECIFIC",
    "L1_SPECIFIC",
    "L2_SPECIFIC",
    "L3_SPECIFIC",
    "SCHEMA",
    "BRIDGE",
    "PURITY",
    "BRANCH_GOVERNANCE",
    "REFERENCE_ALGEBRA",
    "EVIDENCE",
    "MANAT",
}

TRACE_CODES = {"M_01_14", "M_00_11", "M_CX_12", "M_02_11", "M_03_07"}
RANK_CODES = {"M_01_16", "M_CX_09", "M_00_10", "M_00_12", "M_01_15", "M_02_12", "M_03_08"}

REQUIRED_FAMILY_BY_CODE = {
    "M_02_19": "MEANING_LEAK",
    "M_WW_07": "MEANING_LEAK",
    "M_WW_08": "IFADAH_LEAK",
    "M_WW_03": "RELATION_PREREQUISITE",
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


@pytest.fixture(scope="module")
def rows_by_code(alignment_rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    return {(row["primary_canonical_code"] or "").strip(): row for row in alignment_rows}


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


def test_every_row_has_canonical_family_in_closed_set(alignment_rows: list[dict[str, str]]):
    """trace_ref: docs/13_FAILURE_ALIGNMENT_CONSTITUTION.md Canonical Family Set."""
    for row in alignment_rows:
        family = (row["canonical_family"] or "").strip()
        assert family, f"row {row['row_id']} is missing canonical_family"
        assert family in CANONICAL_FAMILIES, (
            f"row {row['row_id']} uses non-closed canonical_family: {family}"
        )


def test_every_row_has_domain_scope(alignment_rows: list[dict[str, str]]):
    """trace_ref: docs/13_FAILURE_ALIGNMENT_CONSTITUTION.md Alignment Constraints."""
    for row in alignment_rows:
        domain_scope = (row["domain_scope"] or "").strip()
        assert domain_scope, f"row {row['row_id']} is missing domain_scope"


def test_every_row_has_proof_obligation_or_audit_only_local(
    alignment_rows: list[dict[str, str]],
):
    """trace_ref: docs/13_FAILURE_ALIGNMENT_CONSTITUTION.md Alignment Constraints."""
    for row in alignment_rows:
        obligation = (row["proof_obligation"] or "").strip()
        assert obligation, f"row {row['row_id']} is missing proof_obligation"
        assert obligation == "AUDIT_ONLY_LOCAL" or obligation.startswith("PROOF_"), (
            f"row {row['row_id']} has unsupported proof_obligation: {obligation}"
        )


def test_forbidden_runtime_use_is_true_while_embargoed(alignment_rows: list[dict[str, str]]):
    """trace_ref: docs/12_RUNTIME_EMBARGO_CONSTITUTION.md Embargo Rule."""
    for row in alignment_rows:
        assert _parse_bool_string(row["forbidden_runtime_use"]), (
            f"row {row['row_id']} must set forbidden_runtime_use=true while embargoed"
        )


def test_all_rows_stay_non_executable_and_audit_only(alignment_rows: list[dict[str, str]]):
    """trace_ref: docs/13_FAILURE_ALIGNMENT_CONSTITUTION.md Audit-Only Law."""
    for row in alignment_rows:
        is_executable = _parse_bool_string(row["is_executable_row"])
        mapping = (row["executable_mapping"] or "").strip().upper()
        assert not is_executable, (
            f"row {row['row_id']} cannot become executable before runtime embargo lift"
        )
        assert mapping == AUDIT_ONLY_MARKER, (
            f"row {row['row_id']} must stay AUDIT_ONLY while runtime is embargoed"
        )


@pytest.mark.parametrize("code,expected_family", REQUIRED_FAMILY_BY_CODE.items())
def test_required_code_family_assignments(
    rows_by_code: dict[str, dict[str, str]],
    code: str,
    expected_family: str,
):
    """trace_ref: docs/13_FAILURE_ALIGNMENT_CONSTITUTION.md Canonical Family Set."""
    assert code in rows_by_code, f"missing required canonical code in matrix: {code}"
    family = (rows_by_code[code]["canonical_family"] or "").strip()
    assert family == expected_family


def test_trace_related_codes_map_to_trace(rows_by_code: dict[str, dict[str, str]]):
    """trace_ref: docs/13_FAILURE_ALIGNMENT_CONSTITUTION.md Canonical Family Set."""
    for code in TRACE_CODES:
        assert code in rows_by_code, f"missing trace-related canonical code: {code}"
        family = (rows_by_code[code]["canonical_family"] or "").strip()
        assert family == "TRACE", f"{code} must map to TRACE"


def test_rank_related_codes_map_to_rank(rows_by_code: dict[str, dict[str, str]]):
    """trace_ref: docs/13_FAILURE_ALIGNMENT_CONSTITUTION.md Canonical Family Set."""
    for code in RANK_CODES:
        assert code in rows_by_code, f"missing rank-related canonical code: {code}"
        family = (rows_by_code[code]["canonical_family"] or "").strip()
        assert family == "RANK", f"{code} must map to RANK"
