# Hallucination Leap Barrier Law — `docs/62`

## Authority

- `docs/00_MAQOOL_CONSTITUTION.md`
- `docs/00A_CONSTITUTIONAL_PROGRAMMING_AMENDMENT.md`
- `docs/12_RUNTIME_EMBARGO_CONSTITUTION.md`
- `docs/13_FAILURE_ALIGNMENT_CONSTITUTION.md`
- `docs/14_EUCLIDEAN_LEARNING_DOMAIN_BOUNDARY.md`
- `docs/15_PROJECT_ROADMAP.md`
- `docs/20_AGENT_AUTONOMY_RUNBOOK.md`
- `docs/54_GPT_ANSWER_REASONABLENESS_OBJECTIVE_LAW.md`
- `docs/55_KNOWLEDGE_ORIGINS_FOR_GPT_REASONABLENESS_LAW.md`
- `docs/56_REASONABLENESS_PROOF_OBJECT_BOUNDARY_LAW.md`
- `docs/57_TRANSPARENT_BARRIER_ARCHITECTURE_LAW.md`
- `docs/58_SUPREME_TASAWWUR_REALITY_LAW.md`
- `docs/61_INDEPENDENT_IFADAH_MODEL_LAW.md`

## Constitutional Status

This law is an audit-only barrier map.

```text
Runtime status: AUDIT_ONLY
L0 is closed.
L1 is contract/audit bounded.
L2 remains locked.
L3 remains locked.
Runtime embargo remains active.
```

## Scope

This document records the constitutional definition of hallucination as an
unlicensed leap in the verification chain for GPT-answer reasonableness.

It maps the barrier points that prevent a statistical or linguistic candidate
from being promoted into `SlotFill`, `Ifādah`, `Hukm`, or `Yaqīn` without the
required slot, license, blocker check, residual visibility, and trace.

## Non-scope

This document does not:

- create a hallucination detector;
- create a runtime predicate;
- create a runtime translator;
- create a decision engine;
- create a runtime kernel;
- create a coverage matrix;
- create or accept a computed verdict;
- open `L2`;
- open `L3`;
- open any runtime domain;
- issue hukm;
- create yaqīn;
- certify truth.

## One Auditable Claim

Hallucination, for this audit law, is not the mere presence of a candidate.

```text
A candidate is not hallucination while declared as candidate.
Hallucination begins when an open candidate is written, named, or treated as
closed without the license required by its constitutional layer.
```

The prohibited promotion chain is:

```text
StatisticalCandidate
  → LicensedSlotFill
  → Ifādah
  → Hukm
  → Yaqīn
```

Every arrow in the chain requires a declared slot, a license condition, a
blocker check, a visible residual policy, and a trace. If any arrow is closed
by probability, context alone, evidence list alone, or silence about residuals,
the closure is a hallucination leap.

## Ten Hallucination Leap Barriers

| ID | Hallucination type | Required slot | License condition | Blocker | Residual required | Forbidden promotion phrase | FailureCode family |
|----|--------------------|---------------|-------------------|---------|-------------------|-----------------------------|--------------------|
| HLB-01 | Candidate without slot — مرشح بلا خانة | named slot with domain and trace | slot declared by question need or licensed origin | no slot is available | `SLOT_UNDECLARED` | `candidate therefore fills the slot` | `M_CX` / `M_R0` |
| HLB-02 | Invented slot — خانة مخترعة | slot from an authorized contract | roadmap or contract license names the slot | slot created only to fit the answer | `SLOT_LICENSE_MISSING` | `context creates a new slot` | `M_CX` / `M_TBA` |
| HLB-03 | Answer misses question focus — جواب لا يسد بؤرة السؤال | question focus and answer focus | answer satisfies the demanded focus | answer is complete only in isolation | `QUESTION_FOCUS_UNSATISFIED` | `complete report therefore complete answer` | `M_R0` / `M_TBA` |
| HLB-04 | Reference without referent — إحالة بلا مرجع | referent with trace | discourse or pre-conceptual reference license | unresolved required reference | `REFERENCE_UNRESOLVED` | `pronoun therefore resolved` | `M_K0` / `M_RPO` |
| HLB-05 | Deletion without qarīnah — حذف بلا قرينة | deleted part and its role | prior expression, question, usage, structural need, or maqam license | mental possibility alone supplies the deleted part | `ELLIPSIS_UNLICENSED` | `possible completion therefore licensed ellipsis` | `M_R0` / `M_RPO` |
| HLB-06 | Maqam creates from nothing — مقام يخلق من العدم | visible carrier or gap | maqam closes a licensed gap already carried by expression, prior question, visible situation, usage custom, apparent relation, or trace | no carrier exists for the proposed closure | `MAQAM_CARRIER_MISSING` | `context creates meaning from nothing` | `M_TBA` / `M_R0` |
| HLB-07 | Ifādah equals truth — إفادة = صدق | speech-function completion | minimal utterance function completes in maqam | truth, evidence, or reality is being smuggled into ifādah | `TRUTH_NOT_PROVEN` | `ifādah therefore true` | `M_RPO` / `M_TBA` |
| HLB-08 | Probability equals yaqīn — احتمال = يقين | modality slot | certainty licensed by the required domain and evidence standard | probability, dominance, or suggestion is renamed certainty | `CERTAINTY_UNLICENSED` | `probable therefore certain` | `M_RPO` / `M_CX` |
| HLB-09 | Domain crossing without bridge — عبور مجال بلا جسر | source domain, target domain, bridge | bridge preserves invariant and records residuals | candidate crosses domain by analogy or label only | `BRIDGE_UNLICENSED` | `candidate therefore valid in the new domain` | `M_CX` / `M_TBA` |
| HLB-10 | Hidden residual — بقية مخفية | residual type and scope | all residuals remain visible until lawfully discharged | residual is omitted to make closure appear complete | `HIDDEN_RESIDUAL` | `no residuals mentioned therefore closed` | `M_RPO` / `M_TBA` |

## Acceptance and Rejection Examples

### Candidate remains candidate

Accepted audit wording:

```text
This is a probable candidate. The required slot is not yet licensed.
Residual: SLOT_LICENSE_MISSING.
```

This is not hallucination while the candidate remains openly ranked as a
candidate and the residual remains visible.

Rejected wording:

```text
This is probable, so it fills the required slot.
```

Probability does not close the slot.

### Ifādah is not truth

Accepted audit wording:

```text
The utterance may complete a speech function in maqam. Truth, hukm, and yaqīn
remain outside this audit result.
```

Rejected wording:

```text
The utterance has ifādah, therefore the claim is true.
```

Ifādah ≠ Truth. Ifādah is not hukm. Ifādah is not yaqīn.

### Probability is not yaqīn

Accepted audit wording:

```text
The evidence suggests a candidate with visible uncertainty residuals.
```

Rejected wording:

```text
The evidence suggests it, therefore it is certain.
```

Probability ≠ Yaqīn.

### Maqam closes licensed gap only

Accepted audit wording:

```text
The maqam closes a licensed gap already carried by the prior question.
```

Rejected wording:

```text
The maqam creates the missing meaning from nothing.
```

Maqam closes licensed gap, does not create from nothing.

### Hidden residual is independent breach

Accepted audit wording:

```text
The answer remains suspended because REFERENCE_UNRESOLVED is visible.
```

Rejected wording:

```text
The answer is closed; no residuals are mentioned.
```

A hidden residual is breach independent of the evidential weakness that caused
the residual. Concealing the blocker is itself constitutionally forbidden.

## Rank Label Clarification

Audit labels such as `LICENSED` may appear only as local audit vocabulary for a
specific contract condition. Such a label does not mean truth, hukm, yaqīn,
runtime authority, or domain opening.

```text
LICENSED in audit context = a scoped condition was recorded.
LICENSED in audit context ≠ truth.
LICENSED in audit context ≠ hukm.
LICENSED in audit context ≠ yaqīn.
```

## Drift Guardrail

Future documentation, schemas, or fixtures must not convert open language into
closure language. In particular:

- `candidate` must not drift into `licensed` unless the license is named;
- `probable` must not drift into `certain`;
- `context suggests` must not drift into `context proves`;
- `evidence list exists` must not drift into `evidence proves`;
- `ifādah` must not drift into `truth`;
- a missing residual must not be treated as closure.

## Final Boundary Law

No `StatisticalCandidate` may be promoted to `LicensedSlotFill`, no slot fill to
`Ifādah`, no ifādah to `Hukm`, and no hukm to `Yaqīn` unless the layer-specific
slot, license, blocker absence, trace, and residual policy are explicit.

This law records audit-only barriers. It authorizes no runtime detector, no
predicate, no translator, no computed verdict, no hukm, no yaqīn, and no locked
layer opening.

---

*End of Hallucination Leap Barrier Law.*
