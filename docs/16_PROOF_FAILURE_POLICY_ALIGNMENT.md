# ProofObject Failure-Policy Alignment — `docs/16_PROOF_FAILURE_POLICY_ALIGNMENT.md`

## Scope
Define audit-only failure-policy alignment metadata for required L1 ProofObject kinds.

## Non-scope
No runtime kernel, no executable policy engine, no runtime predicates, no runtime translators, and no domain opening.

## Authority docs
- `docs/00_MAQOOL_CONSTITUTION.md`
- `docs/00A_CONSTITUTIONAL_PROGRAMMING_AMENDMENT.md`
- `docs/08_PROOF_OBJECT_CONSTITUTION.md`
- `docs/12_RUNTIME_EMBARGO_CONSTITUTION.md`
- `docs/13_FAILURE_ALIGNMENT_CONSTITUTION.md`
- `docs/15_REJECTED_RUNTIME_PATTERNS.md`

## Files changed
- `docs/16_PROOF_FAILURE_POLICY_ALIGNMENT.md`
- `tests/test_proof_failure_policy_alignment.py`

## Tests run
- `pytest tests/test_proof_failure_policy_alignment.py -v`
- `pytest tests/`
- `pytest tests/test_kpi_indicators.py -v`
- `python -m ci.constitutional_guard --source-dir src`

## Constitutional invariants preserved
- Runtime embargo remains active.
- No policy is executable before embargo lift.
- No ProofObject policy may emit `ComputedVerdict`.
- No policy introduces `Rank.CERTIFICATE` or `Rank.REJECTED`.
- `rank_ceiling` remains `CANDIDATE`.
- FailureCode remains canonical and is not replaced.

## Central law
No ProofObject failure policy is executable before runtime embargo lift.
Failure policies are audit-only alignment metadata.
No proof policy may emit ComputedVerdict.
No proof policy may raise rank above CANDIDATE.
No proof policy may replace FailureCode.

## Audit-only alignment matrix

| proof_kind | missing_policy | broken_policy | canonical_family | proof_obligation | runtime_status | is_executable | preserves_failure_code | rank_ceiling |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MRKProof | MRK_PROOF_MISSING | MRK_PROOF_INCOMPLETE | PROOF/MRK | PROOF_MRK_REQUIRED | AUDIT_ONLY | false | true | CANDIDATE |
| DomainProof | DOMAIN_PROOF_MISSING | DOMAIN_ORIGIN_UNPROVED | DOMAIN | PROOF_DOMAIN_REQUIRED | AUDIT_ONLY | false | true | CANDIDATE |
| IdentityProof | IDENTITY_PROOF_MISSING | IDENTITY_BROKEN | IDENTITY | PROOF_IDENTITY_REQUIRED | AUDIT_ONLY | false | true | CANDIDATE |
| GateProof | GATE_PROOF_MISSING | GATE_FAILED | GATE | PROOF_GATE_REQUIRED | AUDIT_ONLY | false | true | CANDIDATE |
| BridgeProof | BRIDGE_PROOF_MISSING | BRIDGE_IDENTITY_NOT_PRESERVED | BRIDGE | PROOF_BRIDGE_REQUIRED | AUDIT_ONLY | false | true | CANDIDATE |
| EvidenceProof | EVIDENCE_PROOF_MISSING | EVIDENCE_SCOPE_INVALID | EVIDENCE | PROOF_EVIDENCE_REQUIRED | AUDIT_ONLY | false | true | CANDIDATE |
| CoverageProof | COVERAGE_PROOF_MISSING | COVERAGE_INCOMPLETE | COVERAGE | PROOF_COVERAGE_REQUIRED | AUDIT_ONLY | false | true | CANDIDATE |
