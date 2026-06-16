# Reasonableness Proof Object Boundary Law — `docs/56`

## Authority
`docs/00_MAQOOL_CONSTITUTION.md §5 Rule 1` (Layered Implementation Order).
`docs/54_GPT_ANSWER_REASONABLENESS_OBJECTIVE_LAW.md` (Operational Goal).
`docs/55_KNOWLEDGE_ORIGINS_FOR_GPT_REASONABLENESS_LAW.md` (Knowledge Origins).

## Phase
GPT-RPO — Reasonableness Proof Object Boundary Law.

---

## Declaration

> The output of the Taaqol-GPT system is NOT a truth certificate.
> It is a **Reasonableness Proof Object (RPO)**: a traceable, evidence-bound,
> rank-limited, residual-visible record that proves the verdict about
> the answer's reasonableness is **procedurally justified** under declared conditions.

---

## Constitutional Prohibition

The following terms are **constitutionally forbidden** as names for the system's output:

| Forbidden Term | Why | FailureCode |
|----------------|-----|-------------|
| `TruthCertificate` | System does not certify absolute truth | `M_RPO_01` |
| `EuclideanProof` (of reality) | System does not prove real-world facts geometrically | `M_RPO_02` |
| `FinalCertificate` | No output is final; all carry rank and residuals | `M_RPO_03` |
| `AuthorityCertificate` | Audit ≠ Authority; verification ≠ execution | `M_RPO_04` |
| `AbsoluteAcceptance` | No `⊤` (top element) exists; all acceptance is scoped | `M_RPO_05` |

---

## What the RPO Proves

The RPO does NOT prove:

```text
The world is as GPT said.
```

The RPO proves:

```text
Given this question,
given this answer,
given these extracted claims,
given these origins,
given this evidence,
given these gates,
given these residuals,

the verdict REASONABLE / UNREASONABLE / MU'ALLAQ
is procedurally valid under the declared rules.
```

That is: **the RPO proves that the verdict followed the rules, not that reality matches the claim.**

---

## RPO Structure

```text
ReasonablenessProofObject = (
    question_ref,
    answer_ref,
    maqam_gpt,
    mantuq_gpt,
    mafhum_gpt,
    origin_bindings,
    evidence_support,
    gates,
    rank,
    residuals,
    trace_graph,
    verdict
)
```

### Field Definitions

| Field | Type | Description |
|-------|------|-------------|
| `question_ref` | `str` | Pointer to the user's question |
| `answer_ref` | `str` | Pointer to the GPT answer being verified |
| `maqam_gpt` | `MaqamGPT` | Context: domain, constraints, risk, evidence need |
| `mantuq_gpt` | `FrozenSet[MantuqClaim]` | Extracted explicit claims |
| `mafhum_gpt` | `FrozenSet[MafhumImplication]` | Derived implicit commitments |
| `origin_bindings` | `FrozenSet[OriginBinding]` | Claims bound to knowledge origins |
| `evidence_support` | `FrozenSet[EvidenceEntry]` | Evidence supporting/contradicting claims |
| `gates` | `FrozenSet[GateResult]` | Results of all 10 reasonableness gates |
| `rank` | `str` | Always `"CANDIDATE"` — never promoted without amendment |
| `residuals` | `FrozenSet[TypedResidual]` | Visible, typed, non-numeric residuals |
| `trace_graph` | `TraceGraph` | Full trace from question to verdict |
| `verdict` | `ReasonablenessVerdict` | The final verdict with scope declaration |

---

## Verdict States (expanded from docs/54)

```text
verdict ∈ {
    REASONABLE,
    PARTIALLY_REASONABLE,
    UNREASONABLE,
    MU'ALLAQ,
    OFF_MAQAM,
    UNSUPPORTED,
    CONTRADICTORY,
    OVERCLAIMED,
    ORIGIN_CONTRADICTION,
    FORBIDDEN_LEAP,
    RESIDUAL_BLOCKED,
    NEEDS_CLARIFICATION
}
```

**Critical**: Even `REASONABLE` carries scope:

```text
REASONABLE = reasonable WITHIN declared scope, origins, evidence, rank, and trace.
```

There is no absolute acceptance. There is no `⊤`.

---

## Two Types of Verification in the RPO

### a. Formal/Procedural Verification (machine-checkable)

These can be proven formally within the system:

| Check | Question |
|-------|----------|
| Trace completeness | Does every claim have trace to its origin? |
| Gate passage | Did all required gates execute? |
| Residual visibility | Are all residuals declared, not hidden? |
| Rank compliance | Is rank bounded correctly? |
| No-leap check | Does no transition skip a layer? |
| Origin binding | Is every factual claim bound to an origin? |
| NeedGate compliance | Was no layer opened without justification? |

These are **formal proofs within the system's rules**.

### b. Evidential Verification (domain-dependent)

These cannot be proven formally — they are supported by evidence:

| Check | Question |
|-------|----------|
| Origin accuracy | Is the knowledge origin itself correct? |
| Evidence reliability | Is the cited evidence trustworthy? |
| Real-world truth | Does the claim match reality? |
| Temporal validity | Is the evidence still current? |

These are **evidential judgments**, not formal proofs.

**The RPO is therefore**:

```text
Formal + Evidential Verification Object
```

Not:

```text
Pure Euclidean Proof
```

---

## Typed Residuals (not numeric)

Residuals in the RPO are **typed and ordered**, not a number between 0 and 1.

### Residual Types

| Type | Meaning | Severity |
|------|---------|----------|
| `EXPLANATORY` | Additional context could strengthen the verdict | LOW |
| `DEFERRED` | Verification possible but postponed | LOW |
| `EVIDENCE_MISSING` | Factual claim lacks supporting evidence | MEDIUM |
| `ORIGIN_UNBOUND` | Claim not yet bound to a knowledge origin | MEDIUM |
| `DOMAIN_AMBIGUOUS` | Domain classification unclear | MEDIUM |
| `REFERENCE_UNRESOLVED` | A pronoun/reference affects verdict but is ambiguous | HIGH |
| `BLOCKING` | Prevents verdict issuance entirely | CRITICAL |
| `HIDDEN_FORBIDDEN` | A residual was concealed (constitutional breach) | FATAL |

### Residual Ordering

```text
FATAL > CRITICAL > HIGH > MEDIUM > LOW
```

**Rule RPO-RES-1**: No numeric residual score (`Res(C) → [0,1]`) is permitted
without a calibration dataset and validation methodology.

**FailureCode**: `M_RPO_06`

---

## RPO Composition (Partial, Non-commutative)

When combining multiple RPOs (e.g., multi-claim answers):

### What is NOT assumed

| Property | Status | Reason |
|----------|--------|--------|
| Commutativity | **NOT ASSUMED** | Order of claims may affect verdict |
| Associativity | **NOT ASSUMED** | Grouping may reveal contradictions |
| Identity element (`⊤`) | **FORBIDDEN** | No absolute acceptance exists |
| Absorption | **NOT ASSUMED** | Combining RPOs may produce refusal |

### What IS defined

```text
compose(RPO_1, RPO_2) ⇀ RPO_3 | Refusal(reason)
```

Composition is:
- **Partial**: may produce `Refusal` if claims contradict
- **Typed**: respects domain and scope constraints
- **Non-commutative by default**: order matters until proven otherwise
- **Trace-preserving**: composed RPO carries traces from both sources

**Rule RPO-ALG-1**: No algebraic property (commutativity, associativity, etc.)
may be asserted without formal proof of its conditions.

**FailureCode**: `M_RPO_07`

---

## What This Law Forbids

| Forbidden action | FailureCode |
|------------------|-------------|
| Calling system output a "truth certificate" | `M_RPO_01` |
| Claiming system produces "Euclidean proof of reality" | `M_RPO_02` |
| Treating any output as final/non-revisable | `M_RPO_03` |
| Equating audit with authority | `M_RPO_04` |
| Using absolute acceptance (`⊤`) | `M_RPO_05` |
| Using numeric residual score without calibration | `M_RPO_06` |
| Asserting algebraic properties without proof | `M_RPO_07` |
| Claiming to reveal internal model mechanisms | `M_RPO_08` |
| Issuing RPO without all mandatory fields | `M_RPO_09` |
| Issuing RPO without scope declaration on verdict | `M_RPO_10` |

---

## Relationship to Existing Documents

| Document | Relationship |
|----------|-------------|
| `docs/54` | Defines the goal; RPO is the output that achieves it |
| `docs/55` | Defines origins; RPO binds claims to them |
| `docs/56` (this) | Defines what the output IS and what it is NOT |
| `docs/57` (next) | Defines the architectural barrier that produces RPOs |

---

## Summary Statement

```text
The Reasonableness Proof Object proves not that the answer is absolutely true,
but that the verdict about its reasonableness is procedurally justified
under declared origins, evidence, gates, rank, residuals, and trace.
```

```text
وثيقة تحقق المعقولية تثبت صحة مسار الحكم،
لا حقيقة الدعوى المطلقة.
```

---

*End of Reasonableness Proof Object Boundary Law*
