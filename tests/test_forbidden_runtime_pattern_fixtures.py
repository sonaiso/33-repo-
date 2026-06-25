"""Positive fixture coverage for canonical forbidden runtime patterns.

trace_ref: docs/12_RUNTIME_EMBARGO_CONSTITUTION.md
"""

from __future__ import annotations

from tests.forbidden_runtime_patterns import (
    compile_forbidden_runtime_patterns,
    load_forbidden_runtime_patterns,
)


PATTERN_FIXTURES = {
    "BINDING_DECISION_ENGINE_FORBIDDEN": "engine = BindingDecisionEngine()",
    "RANK_CERTIFICATE_FORBIDDEN": "rank = Rank.CERTIFICATE",
    "RANK_REJECTED_FORBIDDEN": "rank = Rank.REJECTED",
    "EXECUTION_RANK_CERTIFIED_FORBIDDEN": "rank = ExecutionRank.CERTIFIED",
    "MRK_BOOLEAN_DEFAULT_DOMAIN_PROVED": "domain_proved: true",
    "MRK_BOOLEAN_DEFAULT_UNIT_PROVED": "unit_proved: TRUE",
    "MRK_BOOLEAN_DEFAULT_IDENTITY_PRESERVED": "identity_preserved: True",
    "MRK_BOOLEAN_DEFAULT_TRACE_PRESERVED": "trace_preserved: TrUe",
    "MRK_BOOLEAN_DEFAULT_GATE_PASSED": "gate_passed: tRuE",
    "IS_PRESERVED_TRUE_FIELD_FORBIDDEN": "is_preserved: bool = true",
    "IDENTITY_PRESERVED_TRUE_FIELD_FORBIDDEN": (
        "identity_preserved: bool = TRUE"
    ),
    "EVIDENCE_LIST_INLINE_LICENSE_FORBIDDEN": (
        "if self.evidence: self.licensed = true"
    ),
    "EVIDENCE_LIST_MULTILINE_LICENSE_FORBIDDEN": (
        "if self.evidence:\n    self.licensed = TRUE"
    ),
    "TEXT_ONLY_BRIDGE_TRANSLATOR_FORBIDDEN": (
        "class Bridge:\n    translator: str"
    ),
    "TEXT_ONLY_GATE_CONDITION_FORBIDDEN": "class Gate:\n    condition: str",
    "COMPUTED_VERDICT_CLASS_FORBIDDEN": "result = ComputedVerdict()",
    "COMPUTED_VERDICT_FIELD_FORBIDDEN": "computed_verdict: MUALLAQ",
    "MRK_DEFAULTS_FIELD_FORBIDDEN": "mrk_defaults: {}",
    "MANUAL_DASHBOARD_FIELD_FORBIDDEN": "manual_dashboard: totals",
    "EVIDENCE_LIST_AS_PROOF_PHRASE_FORBIDDEN": "evidence list as proof",
    "MRK_BOOLEAN_DEFAULTS_PHRASE_FORBIDDEN": "MRK boolean defaults",
    "TRANSFORM_PASS_INLINE_FORBIDDEN": (
        "def transform(self, operation: str): pass"
    ),
    "TRANSFORM_PASS_ANNOTATED_FORBIDDEN": (
        "def transform(self, operation: str) -> SlotGeometry:\n    pass"
    ),
    "TRANSFORM_PASS_MULTILINE_ANNOTATED_FORBIDDEN": (
        "def transform(self, operation: str) -> (\n    SlotGeometry\n):\n    pass"
    ),
}


def test_forbidden_runtime_pattern_fixtures_cover_every_registry_id():
    """trace_ref: docs/12_RUNTIME_EMBARGO_CONSTITUTION.md Embargo Rule."""
    registry_ids = {record.id for record in load_forbidden_runtime_patterns()}
    fixture_ids = set(PATTERN_FIXTURES)

    assert fixture_ids == registry_ids


def test_forbidden_runtime_pattern_fixtures_match_canonical_patterns():
    """trace_ref: docs/12_RUNTIME_EMBARGO_CONSTITUTION.md Embargo Rule."""
    compiled_by_id = {
        pattern.id: pattern.matcher
        for pattern in compile_forbidden_runtime_patterns(
            load_forbidden_runtime_patterns()
        )
    }

    for pattern_id, sample in PATTERN_FIXTURES.items():
        assert compiled_by_id[pattern_id].search(sample), pattern_id

