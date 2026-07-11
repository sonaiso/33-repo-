"""Audit-only K0/W0/R0 alignment registry guards.

trace_ref: docs/54_GPT_ANSWER_REASONABLENESS_OBJECTIVE_LAW.md; docs/55_KNOWLEDGE_ORIGINS_FOR_GPT_REASONABLENESS_LAW.md; docs/20_AGENT_AUTONOMY_RUNBOOK.md
"""

from __future__ import annotations

import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = REPO_ROOT / "data" / "k0_w0_r0_alignment_registry.json"
ALLOWED_STATUSES = {"present", "partial", "missing"}
ALLOWED_RUNTIME_STATUSES = {"embargoed", "missing", "partial", "present"}
ALLOWED_CLOSURE_STATUSES = {"closed", "candidate", "unproven"}
REQUIRED_FORBIDDEN_RUNTIME_ARTIFACTS = {
    "src/taaqqul_slot_geometry/runtime/binding_kernel.py",
    "src/taaqqul_slot_geometry/runtime/decision_engine.py",
    "coverage_matrix_v0.1.yaml",
}


def _registry() -> dict[str, object]:
    return json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))


def test_registry_exists_with_audit_only_scope() -> None:
    assert REGISTRY_PATH.exists()
    registry = _registry()
    assert registry["scope"] == "AUDIT_ONLY_ALIGNMENT_REGISTRY"
    runtime_policy = registry["runtime_policy"]
    assert runtime_policy == {
        "existing_l0_pipeline": "ACTIVE_LEGACY_LIMITED",
        "binding_kernel": "EMBARGOED",
        "decision_kernel": "EMBARGOED",
        "w0_runtime": "EMBARGOED",
    }
    trace_ref = registry["trace_ref"]
    assert isinstance(trace_ref, str)
    assert "docs/54_GPT_ANSWER_REASONABLENESS_OBJECTIVE_LAW.md" in trace_ref
    assert "docs/55_KNOWLEDGE_ORIGINS_FOR_GPT_REASONABLENESS_LAW.md" in trace_ref


def test_registry_declares_exactly_k0_w0_r0_statuses() -> None:
    statuses = _registry()["statuses"]
    assert isinstance(statuses, dict)
    assert set(statuses.keys()) == {"K0", "W0", "R0"}
    for entry in statuses.values():
        assert entry["law_status"] in ALLOWED_STATUSES
        assert entry["contract_status"] in ALLOWED_STATUSES
        assert entry["runtime_status"] in ALLOWED_RUNTIME_STATUSES
        assert entry["test_status"] in ALLOWED_STATUSES
        assert entry["closure_status"] in ALLOWED_CLOSURE_STATUSES
        assert isinstance(entry["completion_criteria"], list)
        assert entry["completion_criteria"]
        assert all(isinstance(item, str) and item.strip() for item in entry["completion_criteria"])
        assert isinstance(entry["known_gaps"], list)
        assert entry["known_gaps"]
        assert all(isinstance(item, str) and item.strip() for item in entry["known_gaps"])
        assert isinstance(entry["evidence_refs"], list)
        assert entry["evidence_refs"]


def test_k0_r0_w0_current_alignment_state() -> None:
    statuses = _registry()["statuses"]
    k0 = statuses["K0"]
    r0 = statuses["R0"]
    w0 = statuses["W0"]

    assert k0["law_status"] == "partial"
    assert k0["contract_status"] == "partial"
    assert k0["runtime_status"] == "embargoed"
    assert k0["test_status"] == "partial"
    assert k0["closure_status"] == "unproven"
    assert k0["law_doc"] == "docs/55_KNOWLEDGE_ORIGINS_FOR_GPT_REASONABLENESS_LAW.md"
    assert "src/taaqqul_slot_geometry/L1/postulate.py" in k0["implementation_refs"]
    assert "tests/L1/test_l1_postulate.py" in k0["test_refs"]

    assert r0["law_status"] == "partial"
    assert r0["contract_status"] == "partial"
    assert r0["runtime_status"] == "missing"
    assert r0["test_status"] == "partial"
    assert r0["closure_status"] == "unproven"
    assert r0["law_doc"] == "docs/54_GPT_ANSWER_REASONABLENESS_OBJECTIVE_LAW.md"
    assert "src/taaqqul_slot_geometry/L1/postulate.py" in r0["implementation_refs"]
    assert "tests/L1/test_l1_postulate.py" in r0["test_refs"]

    assert w0["law_status"] == "missing"
    assert w0["contract_status"] == "missing"
    assert w0["runtime_status"] == "embargoed"
    assert w0["test_status"] == "missing"
    assert w0["closure_status"] == "unproven"
    assert w0["law_doc"] == ""
    assert w0["evidence_refs"] == []
    assert w0["contract_refs"] == []
    assert w0["runtime_refs"] == []
    assert w0["behavioral_test_refs"] == []
    assert "tests/test_k0_w0_r0_alignment_registry.py" in w0["registry_test_refs"]


def test_registry_file_references_exist_when_declared() -> None:
    statuses = _registry()["statuses"]
    for entry in statuses.values():
        law_doc = entry["law_doc"]
        if law_doc:
            assert (REPO_ROOT / law_doc).exists()
        for rel_path in [*entry["evidence_refs"], *entry["implementation_refs"], *entry["test_refs"]]:
        for rel_path in [
            *entry["evidence_refs"],
            *entry["contract_refs"],
            *entry["runtime_refs"],
            *entry["behavioral_test_refs"],
            *entry["registry_test_refs"],
        ]:
            assert (REPO_ROOT / rel_path).exists()


def test_registry_separates_evidence_contract_runtime_and_tests() -> None:
    statuses = _registry()["statuses"]
    for entry in statuses.values():
        assert isinstance(entry["evidence_refs"], list)
        assert isinstance(entry["contract_refs"], list)
        assert isinstance(entry["runtime_refs"], list)
        assert isinstance(entry["behavioral_test_refs"], list)
        assert isinstance(entry["registry_test_refs"], list)


def test_registry_keeps_forbidden_runtime_artifacts_absent() -> None:
    forbidden_paths = _registry()["forbidden_runtime_artifacts"]
    assert isinstance(forbidden_paths, list)
    assert forbidden_paths
    assert set(forbidden_paths) == REQUIRED_FORBIDDEN_RUNTIME_ARTIFACTS
    assert all(not (REPO_ROOT / rel_path).exists() for rel_path in forbidden_paths)
