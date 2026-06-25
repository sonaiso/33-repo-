# Computed Coverage Schema Constitution — `docs/18_COMPUTED_COVERAGE_SCHEMA_CONSTITUTION.md`

## Scope
Schema-only constitutional contract for future coverage cases under Runtime Embargo.
Fixture-manifest quarantine for coverage corpus classification (valid vs invalid).

## Non-scope
No runtime kernel.
No decision engine.
No `coverage_matrix_v0.1.yaml`.
No runtime predicates/translators.
No runtime domain opening.
No computed verdict execution.

## Authority docs
- `docs/00_MAQOOL_CONSTITUTION.md`
- `docs/00A_CONSTITUTIONAL_PROGRAMMING_AMENDMENT.md`
- `docs/12_RUNTIME_EMBARGO_CONSTITUTION.md`
- `docs/13_FAILURE_ALIGNMENT_CONSTITUTION.md`
- `docs/15_REJECTED_RUNTIME_PATTERNS.md`

## Files changed
- `docs/18_COMPUTED_COVERAGE_SCHEMA_CONSTITUTION.md`
- `schemas/coverage_case.schema.json`
- `tests/test_computed_coverage_schema.py`
- `tests/fixtures/coverage_cases/manifest.json`
- `tests/test_coverage_fixture_manifest.py`
- `tests/fixtures/coverage_cases/valid_blocked_ifadah_case.json`
- `tests/fixtures/coverage_cases/valid_accepted_candidate_lafzi_case.json`
- `tests/fixtures/coverage_cases/valid_proof_required_hukm_case.json`
- `tests/fixtures/coverage_cases/valid_bridge_required_dal_only_case.json`
- `tests/fixtures/coverage_cases/valid_bridge_required_lafzi_form_case.json`
- `tests/fixtures/coverage_cases/valid_bridge_required_lexical_madlul_case.json`
- `tests/fixtures/coverage_cases/valid_bridge_required_tanzil_case.json`
- `tests/fixtures/coverage_cases/valid_residual_relation_case.json`
- `tests/fixtures/coverage_cases/invalid_accepted_ifadah_case.json`
- `tests/fixtures/coverage_cases/invalid_boolean_proof_case.json`
- `tests/fixtures/coverage_cases/invalid_computed_verdict_case.json`
- `tests/fixtures/coverage_cases/invalid_mrk_defaults_case.json`
- `tests/fixtures/coverage_cases/invalid_rank_certificate_case.json`
- `tests/fixtures/coverage_cases/valid_matrix_*.json`
- `tests/fixtures/coverage_cases/invalid_matrix_*.json`

## Schema contract
Allowed fields:
- `case_id`
- `input_text`
- `input_domain`
- `expected_verdict`
- `required_contracts`
- `required_bridges`
- `expected_failure_family`
- `expected_residual_policy`
- `trace_ref` (must equal `docs/18_COMPUTED_COVERAGE_SCHEMA_CONSTITUTION.md`)

Conditional requirements:
- `EXPECTED_BLOCKED` requires `expected_failure_family`.
- `EXPECTED_PROOF_REQUIRED` requires `expected_failure_family`.
- `EXPECTED_RESIDUAL` requires `expected_residual_policy`.
- `EXPECTED_BRIDGE_REQUIRED` requires non-empty `required_bridges`.
- Outcome-specific fields are exclusive declarations:
  - `expected_failure_family` is allowed only for `EXPECTED_BLOCKED` and `EXPECTED_PROOF_REQUIRED`.
  - `expected_residual_policy` is allowed only for `EXPECTED_RESIDUAL`.
  - `required_bridges` is allowed only for `EXPECTED_BRIDGE_REQUIRED`.

Forbidden fields/claims:
- `computed_verdict`
- `manual_dashboard`
- `mrk_defaults`
- `domain_proved`
- `unit_proved`
- `identity_preserved`
- `trace_preserved`
- `gate_passed`
- `is_preserved`
- `rank = CERTIFICATE`
- `rank = REJECTED`
- `Rank.CERTIFICATE`
- `Rank.REJECTED`
- `coverage_matrix_v0.1.yaml`

## Fixture manifest quarantine contract
- Manifest path: `tests/fixtures/coverage_cases/manifest.json`.
- Fixture case files referenced by the manifest are the PR #81 locked-domain fixture corpus carried forward unchanged in this PR.
- Every coverage fixture in `tests/fixtures/coverage_cases/*.json` (except `manifest.json`) must be listed exactly once.
- `valid_fixtures` entries must start with `valid_` and pass `schemas/coverage_case.schema.json`.
- `invalid_fixtures` entries must start with `invalid_` and fail `schemas/coverage_case.schema.json`.
- Locked domains `D5_IFADAH`, `D6_HUKM`, `D7_TANZIL` remain embargoed from `EXPECTED_ACCEPTED_CANDIDATE`.
- Forbidden-pattern fixtures (`computed_verdict`, `mrk_defaults`, `rank=CERTIFICATE` or `Rank.CERTIFICATE`) must remain quarantined under `invalid_fixtures`.
- Manifest coverage completeness is mandatory for all schema verdict classes (`EXPECTED_ACCEPTED_CANDIDATE`, `EXPECTED_BLOCKED`, `EXPECTED_PROOF_REQUIRED`, `EXPECTED_BRIDGE_REQUIRED`, `EXPECTED_RESIDUAL`).
- Invalid fixtures must include explicit anti-pattern quarantine reasons for `COMPUTED_VERDICT_FORBIDDEN`, `MRK_DEFAULTS_FORBIDDEN`, `BOOLEAN_PROOF_FORBIDDEN`, and `RANK_CERTIFICATE_FORBIDDEN`.
- Bridge-required coverage must include audit fixtures for `D1_DAL_ONLY → D2_LAFZI_FORM`, `D2_LAFZI_FORM → D3_LEXICAL_MADLUL`, and `D3_LEXICAL_MADLUL → D4_RELATION` with declared bridge requirements.
- Residual coverage must include at least one fixture with `EXPECTED_RESIDUAL` and explicit `expected_residual_policy`.

## Verdict fixture matrix contract
- Each schema `expected_verdict` class must have a positive `VERDICT_POSITIVE` fixture.
- Positive verdict matrix fixtures must include only the outcome-specific fields required for that verdict.
- Each schema `expected_verdict` class must have negative `VERDICT_NEGATIVE` fixtures for every unrelated outcome-specific field.
- Each schema `expected_verdict` class must have a negative `VERDICT_NEGATIVE` fixture proving `computed_verdict` remains forbidden.
- Verdict fixture matrix entries are declarative schema cases only; they do not compute, execute, or authorize runtime verdicts.

## Tests run
Required before finish:
- `pytest tests/`
- `pytest tests/test_kpi_indicators.py -v`
- `python -m ci.constitutional_guard --source-dir src`

## Constitutional invariants preserved
- Runtime Embargo remains active.
- Schema is declarative-only.
- No kernel/decision authority is introduced.
- No runtime artifact is introduced.
- No boolean-as-proof fields are authorized.
