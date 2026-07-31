"""Audit-only Wadai lexicon inventory registry guards.

trace_ref: docs/21_LICENSED_INTELLIGIBILITY_CHAIN_CONSTITUTION.md; docs/12_RUNTIME_EMBARGO_CONSTITUTION.md
"""

from __future__ import annotations

import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = REPO_ROOT / "data" / "wadai_lexicon_inventory_registry.json"
ALLOWED_STATUS = {"candidate_only"}
ALLOWED_EXECUTION_MODE = {"AUDIT_REFERENCE_ONLY"}
REQUIRED_FORBIDDEN_RUNTIME_ARTIFACTS = {
    "src/taaqqul_slot_geometry/runtime/binding_kernel.py",
    "src/taaqqul_slot_geometry/runtime/decision_engine.py",
    "coverage_matrix_v0.1.yaml",
}
FORBIDDEN_FIELDS = {
    "computed_verdict",
    "hukm",
    "tanzil",
    "decision",
    "rank",
    "is_certified",
}


def _registry() -> dict[str, object]:
    return json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))


def test_registry_exists_and_is_audit_only() -> None:
    assert REGISTRY_PATH.exists()
    registry = _registry()
    assert registry["scope"] == "AUDIT_ONLY_WADAI_LEXICON_INVENTORY"
    assert registry["inventory_status"] == "AUDIT_SANDBOX_ONLY"
    runtime_policy = registry["runtime_policy"]
    assert runtime_policy == {
        "lexicon_lookup_runtime": "EMBARGOED",
        "binding_kernel": "EMBARGOED",
        "decision_engine": "EMBARGOED",
    }
    trace_ref = registry["trace_ref"]
    assert isinstance(trace_ref, str)
    assert "docs/21_LICENSED_INTELLIGIBILITY_CHAIN_CONSTITUTION.md" in trace_ref
    assert "docs/12_RUNTIME_EMBARGO_CONSTITUTION.md" in trace_ref


def test_inventory_entries_are_non_executable_candidates() -> None:
    entries = _registry()["entries"]
    assert isinstance(entries, list)
    assert entries
    seen_ids: set[str] = set()
    for entry in entries:
        assert isinstance(entry["entry_id"], str) and entry["entry_id"].strip()
        assert entry["entry_id"] not in seen_ids
        seen_ids.add(entry["entry_id"])
        assert isinstance(entry["surface_form"], str) and entry["surface_form"].strip()
        assert isinstance(entry["lexical_sense_label"], str) and entry["lexical_sense_label"].strip()
        assert isinstance(entry["source_ref"], str) and entry["source_ref"].strip()
        assert entry["status"] in ALLOWED_STATUS
        assert entry["execution_mode"] in ALLOWED_EXECUTION_MODE
        assert entry["forbidden_runtime_use"] is True
        assert not (FORBIDDEN_FIELDS & set(entry.keys()))


def test_registry_references_and_runtime_artifact_embargo_are_kept() -> None:
    registry = _registry()
    refs = registry["registry_test_refs"]
    assert refs == ["tests/test_wadai_lexicon_inventory_registry.py"]
    for ref in refs:
        assert (REPO_ROOT / ref).exists()

    forbidden_paths = registry["forbidden_runtime_artifacts"]
    assert isinstance(forbidden_paths, list)
    assert set(forbidden_paths) == REQUIRED_FORBIDDEN_RUNTIME_ARTIFACTS
    assert all(not (REPO_ROOT / rel_path).exists() for rel_path in forbidden_paths)
