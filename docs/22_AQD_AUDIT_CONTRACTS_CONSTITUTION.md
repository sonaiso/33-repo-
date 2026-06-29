# Aqd Audit Contracts Constitution

Origin: docs/00_MAQOOL_CONSTITUTION.md §5; docs/12_RUNTIME_EMBARGO_CONSTITUTION.md
Authority: docs/00A_CONSTITUTIONAL_PROGRAMMING_AMENDMENT.md; docs/13_FAILURE_ALIGNMENT_CONSTITUTION.md; docs/14_EUCLIDEAN_LEARNING_DOMAIN_BOUNDARY.md; docs/15_PROJECT_ROADMAP.md; docs/20_AGENT_AUTONOMY_RUNBOOK.md

## Scope

This document authorizes an L1 audit-only contract layer for the Aqd concept. Aqd is treated here as a proof-bearing contract vocabulary for shape, guardrails, residuals, and proof references.

## Non-scope

Aqd is not a runtime language in this phase. This document does not authorize execution, parser construction, interpreter construction, semantic lookup, relation runtime, ifadah runtime, hukm, tanzil, result emission, or any Runtime Embargo lift.

## Contract law

Every Aqd contract is an audit-only candidate:

- `rank` remains `CANDIDATE`.
- `trace_ref` is required.
- `proof_object_ref` or `proof_trace_ref` is required.
- `forbidden_outputs` is required and must preserve the Aqd forbidden-output set.
- `authoritative` is always `False`.
- `runtime_authorized` is always `False`.
- `residuals` remain audit labels only.

The contract layer describes shape and guardrails only. It never emits a runtime result and never decides final meaning, relation authority, ifadah, hukm, tanzil, or yaqin.

## Proof references

Aqd contracts carry references to ProofObject or ProofTrace records. A reference is not itself runtime authority. No Boolean field may replace a proof object or proof trace.

## Residual labels

EnergyLeak and EnergyMismatch may appear only as residual labels in audit output. They are not exceptions, not runtime events, and not execution failures.

## Runtime embargo status

Runtime remains embargoed. The Aqd audit contracts do not lift the embargo, do not open locked layers, and do not produce operational authority.
