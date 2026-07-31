"""Audit-only particle lexicon and MCC registry guards.

trace_ref: docs/21_LICENSED_INTELLIGIBILITY_CHAIN_CONSTITUTION.md; docs/12_RUNTIME_EMBARGO_CONSTITUTION.md
"""

from __future__ import annotations

import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = REPO_ROOT / "data" / "particle_lexicon_mcc_registry.json"
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
    "runtime_authorized",
}


def _registry() -> dict[str, object]:
    return json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))


def test_registry_exists_and_declares_audit_only_scope() -> None:
    assert REGISTRY_PATH.exists()
    registry = _registry()
    assert registry["scope"] == "AUDIT_ONLY_PARTICLE_LEXICON_MCC_REGISTRY"
    assert registry["registry_status"] == "AUDIT_SANDBOX_ONLY"
    assert registry["particle_lexicon"]["status"] == "candidate_only"
    assert registry["particle_lexicon"]["execution_mode"] == "AUDIT_REFERENCE_ONLY"
    assert registry["mcc_contract"]["status"] == "candidate_only"
    assert registry["mcc_contract"]["execution_mode"] == "AUDIT_REFERENCE_ONLY"
    assert registry["runtime_policy"] == {
        "particle_runtime_resolution": "EMBARGOED",
        "mcc_runtime_execution": "EMBARGOED",
        "binding_kernel": "EMBARGOED",
        "decision_engine": "EMBARGOED",
    }


def test_particle_lexicon_categories_are_complete_and_non_executable() -> None:
    categories = _registry()["particle_lexicon"]["categories"]
    assert isinstance(categories, list)
    assert len(categories) == 11
    category_ids = {cat["category_id"] for cat in categories}
    assert category_ids == {f"3.{i}" for i in range(1, 12)}

    has_min = False
    has_thumma = False
    has_hal = False
    has_inn = False
    for category in categories:
        assert isinstance(category["title_ar"], str) and category["title_ar"].strip()
        entries = category["entries"]
        assert isinstance(entries, list)
        assert entries
        for entry in entries:
            assert isinstance(entry["particle"], str) and entry["particle"].strip()
            assert isinstance(entry["meaning"], str) and entry["meaning"].strip()
            assert entry["evidence"] == "معجمي"
            assert not (FORBIDDEN_FIELDS & set(entry.keys()))
            has_min = has_min or entry["particle"] == "مِنْ"
            has_thumma = has_thumma or entry["particle"] == "ثُمَّ"
            has_hal = has_hal or entry["particle"] == "هَلْ"
            has_inn = has_inn or entry["particle"] == "إِنْ"

    assert has_min
    assert has_thumma
    assert has_hal
    assert has_inn


def test_mcc_contract_baseline_is_present() -> None:
    mcc = _registry()["mcc_contract"]
    requirements = mcc["core_requirements"]
    assert isinstance(requirements, list)
    assert len(requirements) == 9
    requirement_ids = {item["requirement_id"] for item in requirements}
    assert requirement_ids == {f"mcc-0{i}" for i in range(1, 10)}

    patterns = mcc["factor_patterns"]
    assert isinstance(patterns, list)
    assert len(patterns) >= 8
    for item in patterns:
        assert isinstance(item["factor_type"], str) and item["factor_type"].strip()
        assert isinstance(item["example"], str) and item["example"].strip()
        assert isinstance(item["opens_slots"], list)
        assert item["opens_slots"]

    models = mcc["applied_models"]
    assert isinstance(models, list)
    assert len(models) == 5
    for model in models:
        assert isinstance(model["model_id"], str) and model["model_id"].strip()
        assert isinstance(model["example_text"], str) and model["example_text"].strip()


def test_registry_references_and_embargo_paths_are_guarded() -> None:
    registry = _registry()
    refs = registry["registry_test_refs"]
    assert refs == ["tests/test_particle_lexicon_mcc_registry.py"]
    for ref in refs:
        assert (REPO_ROOT / ref).exists()

    forbidden_paths = registry["forbidden_runtime_artifacts"]
    assert isinstance(forbidden_paths, list)
    assert set(forbidden_paths) == REQUIRED_FORBIDDEN_RUNTIME_ARTIFACTS
    assert all(not (REPO_ROOT / rel_path).exists() for rel_path in forbidden_paths)
