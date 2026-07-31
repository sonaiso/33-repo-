"""Audit-only verb lexicon inventory registry guards.

trace_ref: docs/21_LICENSED_INTELLIGIBILITY_CHAIN_CONSTITUTION.md; docs/12_RUNTIME_EMBARGO_CONSTITUTION.md
"""

from __future__ import annotations

import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = REPO_ROOT / "data" / "verb_lexicon_inventory_registry.json"
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


def test_registry_exists_and_is_audit_only() -> None:
    assert REGISTRY_PATH.exists()
    registry = _registry()
    assert registry["scope"] == "AUDIT_ONLY_VERB_LEXICON_INVENTORY"
    assert registry["registry_status"] == "AUDIT_SANDBOX_ONLY"
    assert registry["verb_lexicon"]["status"] == "candidate_only"
    assert registry["verb_lexicon"]["execution_mode"] == "AUDIT_REFERENCE_ONLY"
    assert registry["runtime_policy"] == {
        "verb_runtime_resolution": "EMBARGOED",
        "binding_kernel": "EMBARGOED",
        "decision_engine": "EMBARGOED",
    }


def test_sections_exist_and_cover_baseline_examples() -> None:
    lexicon = _registry()["verb_lexicon"]
    past = lexicon["past_tense_built"]
    present = lexicon["present_tense_declined"]
    imperative = lexicon["imperative_built"]
    assert isinstance(past, list) and past
    assert isinstance(present, list) and present
    assert isinstance(imperative, list) and imperative

    past_verbs = {entry["verb"] for entry in past}
    present_verbs = {entry["verb"] for entry in present}
    imperative_verbs = {entry["imperative"] for entry in imperative}
    assert {"كَتَبَ", "ذَهَبَ", "افْتَرَى"} <= past_verbs
    assert {"يَكْتُبُ", "يَنْصَرِفُ", "يَفْتَرِي"} <= present_verbs
    assert {"اُكْتُبْ", "انْصَرِفْ", "افْتَرِ"} <= imperative_verbs


def test_entries_keep_audit_contract_shape() -> None:
    lexicon = _registry()["verb_lexicon"]
    for entry in lexicon["past_tense_built"]:
        assert isinstance(entry["verb"], str) and entry["verb"].strip()
        assert isinstance(entry["meaning"], str) and entry["meaning"].strip()
        assert isinstance(entry["transitivity"], str) and entry["transitivity"].strip()
        assert isinstance(entry["health"], str) and entry["health"].strip()
        assert isinstance(entry["construction"], str) and entry["construction"].strip()
        assert isinstance(entry["pattern"], str) and entry["pattern"].strip()
        assert isinstance(entry["residuals"], str) and entry["residuals"].strip()
        assert entry["evidence"] == "معجمي"
        assert not (FORBIDDEN_FIELDS & set(entry.keys()))

    for entry in lexicon["present_tense_declined"]:
        assert isinstance(entry["verb"], str) and entry["verb"].strip()
        assert isinstance(entry["source"], str) and entry["source"].strip()
        assert isinstance(entry["base_state"], str) and entry["base_state"].strip()
        assert isinstance(entry["pattern"], str) and entry["pattern"].strip()
        assert str(entry["evidence"]).startswith("اشتقاقي")
        assert not (FORBIDDEN_FIELDS & set(entry.keys()))

    for entry in lexicon["imperative_built"]:
        assert isinstance(entry["imperative"], str) and entry["imperative"].strip()
        assert isinstance(entry["from_verb"], str) and entry["from_verb"].strip()
        assert isinstance(entry["construction"], str) and entry["construction"].strip()
        assert isinstance(entry["pattern"], str) and entry["pattern"].strip()
        assert str(entry["evidence"]).startswith("اشتقاقي")
        assert not (FORBIDDEN_FIELDS & set(entry.keys()))


def test_registry_references_and_embargo_paths_are_guarded() -> None:
    registry = _registry()
    refs = registry["registry_test_refs"]
    assert refs == ["tests/test_verb_lexicon_inventory_registry.py"]
    for ref in refs:
        assert (REPO_ROOT / ref).exists()

    forbidden_paths = registry["forbidden_runtime_artifacts"]
    assert isinstance(forbidden_paths, list)
    assert set(forbidden_paths) == REQUIRED_FORBIDDEN_RUNTIME_ARTIFACTS
    assert all(not (REPO_ROOT / rel_path).exists() for rel_path in forbidden_paths)
