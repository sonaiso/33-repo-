"""Audit-only K0/W0/R0 alignment registry guards.

trace_ref: docs/54_GPT_ANSWER_REASONABLENESS_OBJECTIVE_LAW.md; docs/55_KNOWLEDGE_ORIGINS_FOR_GPT_REASONABLENESS_LAW.md; docs/20_AGENT_AUTONOMY_RUNBOOK.md
"""

from __future__ import annotations

import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = REPO_ROOT / "data" / "k0_w0_r0_alignment_registry.json"
ALLOWED_STATUSES = {"present", "partial", "missing"}


def _registry() -> dict[str, object]:
    return json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))


def test_registry_exists_with_audit_only_scope() -> None:
    registry = _registry()
    assert REGISTRY_PATH.exists()
    assert registry["scope"] == "AUDIT_ONLY_ALIGNMENT_REGISTRY"
    assert registry["runtime_status"] == "EMBARGOED"
    trace_ref = registry["trace_ref"]
    assert isinstance(trace_ref, str)
    assert "docs/54_GPT_ANSWER_REASONABLENESS_OBJECTIVE_LAW.md" in trace_ref
    assert "docs/55_KNOWLEDGE_ORIGINS_FOR_GPT_REASONABLENESS_LAW.md" in trace_ref


def test_registry_declares_exactly_k0_w0_r0_statuses() -> None:
    statuses = _registry()["statuses"]
    assert isinstance(statuses, dict)
    assert set(statuses.keys()) == {"K0", "W0", "R0"}
    for key in ("K0", "W0", "R0"):
        status = statuses[key]["status"]
        assert status in ALLOWED_STATUSES


def test_k0_r0_w0_current_alignment_state() -> None:
    statuses = _registry()["statuses"]
    k0 = statuses["K0"]
    r0 = statuses["R0"]
    w0 = statuses["W0"]

    assert k0["status"] == "partial"
    assert k0["law_doc"] == "docs/55_KNOWLEDGE_ORIGINS_FOR_GPT_REASONABLENESS_LAW.md"
    assert "src/taaqqul_slot_geometry/L1/postulate.py" in k0["implementation_refs"]

    assert r0["status"] == "partial"
    assert r0["law_doc"] == "docs/54_GPT_ANSWER_REASONABLENESS_OBJECTIVE_LAW.md"

    assert w0["status"] == "missing"
    assert w0["law_doc"] == ""
    assert w0["implementation_refs"] == []
    assert w0["test_refs"] == []


def test_registry_file_references_exist_when_declared() -> None:
    statuses = _registry()["statuses"]
    for entry in statuses.values():
        law_doc = entry["law_doc"]
        if law_doc:
            assert (REPO_ROOT / law_doc).exists()
        for rel_path in [*entry["implementation_refs"], *entry["test_refs"]]:
            assert (REPO_ROOT / rel_path).exists()


def test_registry_keeps_forbidden_runtime_artifacts_absent() -> None:
    forbidden_paths = _registry()["forbidden_runtime_artifacts"]
    assert isinstance(forbidden_paths, list)
    assert all(not (REPO_ROOT / rel_path).exists() for rel_path in forbidden_paths)
