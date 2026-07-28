"""Audit-only integration gap registry guards.

trace_ref: docs/67_IMPLEMENTATION_GAP_ANALYSIS_TAAQOL_GPT_TO_33_REPO.md; docs/12_RUNTIME_EMBARGO_CONSTITUTION.md
"""

from __future__ import annotations

import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = REPO_ROOT / "data" / "integration_gap_registry.json"
DOC_PATH = REPO_ROOT / "docs" / "67_IMPLEMENTATION_GAP_ANALYSIS_TAAQOL_GPT_TO_33_REPO.md"
ALLOWED_PRIORITIES = {"P0", "P1", "P2"}
ALLOWED_STATUSES = {"NOW", "DEFER", "BLOCKED"}
REQUIRED_FORBIDDEN_RUNTIME_ARTIFACTS = {
    "src/taaqqul_slot_geometry/runtime/binding_kernel.py",
    "src/taaqqul_slot_geometry/runtime/decision_engine.py",
    "coverage_matrix_v0.1.yaml",
}


def _registry() -> dict[str, object]:
    return json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))


def test_registry_exists_and_declares_audit_only_embargoed_scope() -> None:
    assert REGISTRY_PATH.exists()
    assert DOC_PATH.exists()
    registry = _registry()
    assert registry["scope"] == "AUDIT_ONLY_INTEGRATION_GAP_REGISTRY"
    assert registry["selected_safe_queue_item"] == 9
    assert registry["runtime_status"] == "EMBARGOED"
    trace_ref = registry["trace_ref"]
    assert isinstance(trace_ref, str)
    assert "docs/67_IMPLEMENTATION_GAP_ANALYSIS_TAAQOL_GPT_TO_33_REPO.md" in trace_ref
    assert "docs/12_RUNTIME_EMBARGO_CONSTITUTION.md" in trace_ref


def test_registry_priorities_have_closed_status_set_and_are_non_empty() -> None:
    priorities = _registry()["priorities"]
    assert isinstance(priorities, list)
    assert priorities
    for entry in priorities:
        assert isinstance(entry, dict)
        assert entry["priority"] in ALLOWED_PRIORITIES
        assert entry["status"] in ALLOWED_STATUSES
        assert isinstance(entry["capability_group"], str)
        assert entry["capability_group"].strip()
        assert isinstance(entry["target_scope"], str)
        assert entry["target_scope"].strip()
        assert isinstance(entry["execution_mode"], str)
        assert entry["execution_mode"].strip()
        assert isinstance(entry["reason"], str)
        assert entry["reason"].strip()


def test_registry_contains_expected_now_defer_blocked_distribution() -> None:
    priorities = _registry()["priorities"]
    statuses = [entry["status"] for entry in priorities]
    assert statuses.count("NOW") == 3
    assert statuses.count("DEFER") == 2
    assert statuses.count("BLOCKED") == 2


def test_blocked_entries_require_explicit_authorization_and_no_runtime_unlock_claim() -> None:
    blocked = [entry for entry in _registry()["priorities"] if entry["status"] == "BLOCKED"]
    assert blocked
    for entry in blocked:
        assert entry["requires_explicit_constitutional_authorization"] is True
        assert entry["execution_mode"] == "BLOCKED_UNTIL_AUTHORIZED"
        reason = str(entry["reason"]).lower()
        assert ("locked" in reason) or ("embargo" in reason)


def test_registry_keeps_forbidden_runtime_artifacts_absent() -> None:
    forbidden_paths = _registry()["forbidden_runtime_artifacts"]
    assert isinstance(forbidden_paths, list)
    assert set(forbidden_paths) == REQUIRED_FORBIDDEN_RUNTIME_ARTIFACTS
    assert all(not (REPO_ROOT / rel_path).exists() for rel_path in forbidden_paths)


def test_registry_declares_existing_test_reference() -> None:
    refs = _registry()["registry_test_refs"]
    assert refs == ["tests/test_integration_gap_registry.py"]
    for ref in refs:
        assert (REPO_ROOT / ref).exists()
