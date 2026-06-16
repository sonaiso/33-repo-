# Transparent Barrier Architecture Law — `docs/57`

## Authority
`docs/00_MAQOOL_CONSTITUTION.md §5 Rule 1` (Layered Implementation Order).
`docs/54_GPT_ANSWER_REASONABLENESS_OBJECTIVE_LAW.md` (Operational Goal).
`docs/55_KNOWLEDGE_ORIGINS_FOR_GPT_REASONABLENESS_LAW.md` (Knowledge Origins).
`docs/56_REASONABLENESS_PROOF_OBJECT_BOUNDARY_LAW.md` (Proof Object Definition).

## Phase
GPT-TBA — Transparent Barrier Architecture Law.

---

## Declaration

> Taaqol-GPT is a **Transparent Reasonableness Barrier**:
> a boundary architecture around black-box LLMs that transforms
> their external answers into traceable, evidence-bound,
> rank-limited, residual-visible reasonableness proof objects.
>
> It does not open the black box.
> It does not trust the black box.
> It surrounds the black box with a verifiable boundary.

---

## The Three Axioms of the Barrier

### Axiom TBA-1 — Non-Intrusion

```text
The barrier does NOT access, inspect, or reverse-engineer
the internal mechanisms of the language model.
```

We do not claim to know:
- How the model generated the answer
- What chain-of-thought occurred internally
- What weights activated
- Why the model chose specific words

We claim to know only:
- What the model **said** (external output)
- What that output **commits to** (entailments)
- What that output **assumes** (hidden premises)
- What **evidence** supports or contradicts it
- What **residuals** remain unverified

**FailureCode for violation**: `M_TBA_01`

---

### Axiom TBA-2 — Non-Trust

```text
The barrier does NOT treat the LLM output as true by default.
Every claim is a CANDIDATE until verified.
```

| Input state | System treatment |
|-------------|-----------------|
| GPT answer arrives | Status: `UNVERIFIED_CANDIDATE` |
| After MantuqGPT extraction | Status: `CLAIMS_EXTRACTED` |
| After OriginBinding | Status: `BOUND_CANDIDATE` |
| After all gates pass | Status: `REASONABLE` (within scope) |

At no point does the system assert:

```text
This answer is TRUE.
```

It asserts:

```text
This answer is REASONABLE under declared conditions.
```

**FailureCode for violation**: `M_TBA_02`

---

### Axiom TBA-3 — Transparency

```text
Every step from input to verdict is traceable,
every rejection is named,
every residual is visible,
and every scope limitation is declared.
```

Nothing is hidden:
- No silent skip of a verification step
- No unnamed rejection
- No invisible residual
- No undeclared scope limitation
- No pretense of completeness

**FailureCode for violation**: `M_TBA_03`

---

## The Barrier Pipeline

### Mandatory Sequence (every GPT answer)

```text
UserQuestion
  │
  ▼
MaqamGPT ─────────────── (What was asked? Domain? Risk? Constraints?)
  │
  ▼
MantuqGPT ────────────── (What did GPT explicitly claim?)
  │
  ▼
MafhumGPT ────────────── (What does the answer implicitly commit to?)
  │
  ▼
OriginBinding ────────── (Do claims match known origins?)
  │
  ▼
EvidenceSupport ──────── (Is there evidence? What kind? How reliable?)
  │
  ▼
ReasonablenessGates ──── (10 gates: all must pass)
  │
  ▼
ReasonablenessVerdict ── (REASONABLE / UNREASONABLE / MU'ALLAQ / ...)
  │
  ▼
AuditRecord ──────────── (RPO emitted with full trace)
```

### MaqamGPT Comes FIRST (not last)

**Constitutional rule**: The context of the user's question (MaqamGPT) is determined
BEFORE any analysis of the answer. This ensures:

- The answer is judged against what was ASKED, not in isolation
- Domain-appropriate evidence standards are applied
- Risk level determines verification depth

Placing MaqamGPT after verification is a constitutional breach.

**FailureCode**: `M_TBA_04`

---

## Arabic Linguistic Layers: Callable Infrastructure, Not Mandatory Pipeline

### The NeedGate Principle (from docs/54)

```text
Arabic analysis layers (L0–L7) are NOT a mandatory pipeline.
They are callable infrastructure invoked ONLY when needed.
```

| Layer | Invoked when... |
|-------|----------------|
| Morphology (صرف) | A claim's meaning depends on derivational form |
| Syntax (نحو) | A claim's relation structure is ambiguous |
| Semantics (دلالة) | A claim's truth/metaphor status is disputed |
| Pragmatics (تداول) | A claim's force (report vs. command) is unclear |
| Reference (إحالة) | A pronoun/reference resolution affects the verdict |

### What This Means Architecturally

```text
Arabic Column = callable infrastructure
NOT = mandatory pipeline for every answer
```

A GPT answer about Python code does not need morphological analysis.
A GPT answer about Islamic jurisprudence may need it.
The **NeedGate** decides.

**FailureCode for mandatory invocation without need**: `M_TBA_05`

---

## The 10 Reasonableness Gates

For the verdict to be `REASONABLE`, ALL of these must pass:

| # | Gate | Verifies |
|---|------|----------|
| 1 | `MaqamFit` | Answer addresses the actual question |
| 2 | `MantuqControl` | Explicit claims are extractable and well-formed |
| 3 | `MafhumRiskControl` | Implications don't produce unacceptable risk |
| 4 | `OriginBinding` | Claims are bound to classified knowledge origins |
| 5 | `EvidenceSupport` | Factual claims have appropriate evidence (or `NotRequired`) |
| 6 | `Coherence` | Claims don't internally contradict |
| 7 | `NoForbiddenLeap` | No illegitimate inference (appearance→cause, etc.) |
| 8 | `VisibleResiduals` | All residuals are declared, none hidden |
| 9 | `BoundedRank` | Rank does not exceed evidence |
| 10 | `TraceContinuity` | Full trace exists from question to verdict |

### Gate Failure Produces Specific Verdicts

| Failed Gate | Resulting Verdict |
|-------------|-------------------|
| `MaqamFit` | `OFF_MAQAM` |
| `MantuqControl` | `NEEDS_CLARIFICATION` |
| `MafhumRiskControl` | `OVERCLAIMED` |
| `OriginBinding` | `ORIGIN_CONTRADICTION` or `UNSUPPORTED` |
| `EvidenceSupport` | `UNSUPPORTED` |
| `Coherence` | `CONTRADICTORY` |
| `NoForbiddenLeap` | `FORBIDDEN_LEAP` |
| `VisibleResiduals` | `RESIDUAL_BLOCKED` |
| `BoundedRank` | `OVERCLAIMED` |
| `TraceContinuity` | `RESIDUAL_BLOCKED` |

---

## What the Barrier Does NOT Do

| Claim | Status | Reason |
|-------|--------|--------|
| "We reveal the model's internal reasoning" | **FORBIDDEN** | Violates TBA-1 (Non-Intrusion) |
| "We prove the answer is absolutely true" | **FORBIDDEN** | Violates TBA-2 (Non-Trust) / RPO constraints |
| "We certify the answer" | **FORBIDDEN** | Certificate language implies authority |
| "We guarantee correctness" | **FORBIDDEN** | Guarantee implies absolute; we assess reasonableness |
| "We replace human judgment" | **FORBIDDEN** | System is an aid, not a replacement |

---

## What the Barrier DOES Do

| Capability | Description |
|------------|-------------|
| Extracts claims | Decomposes GPT answer into verifiable claims |
| Binds to origins | Connects claims to classified knowledge |
| Checks evidence | Verifies factual claims against available evidence |
| Detects leaps | Identifies illegitimate inferences |
| Reveals residuals | Makes visible what remains unverified |
| Issues scoped verdict | Declares reasonableness within stated conditions |
| Produces traceable record | Every step is auditable |

---

## Scoped Acceptance

Every `REASONABLE` verdict is scoped:

```text
REASONABLE(
    scope = declared_domain,
    evidence = cited_sources,
    rank = CANDIDATE,
    residuals = visible_list,
    trace = complete_graph,
    valid_at = timestamp
)
```

There is no unscoped acceptance. There is no `⊤` (absolute top).

The verdict says:

```text
"Under these declared conditions, with this evidence,
 within this domain, at this rank, with these visible residuals,
 the answer is procedurally reasonable."
```

It does NOT say:

```text
"The answer is true."
```

---

## Architectural Identity

```text
Taaqol-GPT = Transparent Reasonableness Barrier

NOT = Euclidean Truth Certificate Engine
NOT = Black Box Explainability Tool
NOT = Arabic Linguistic Analyzer
NOT = GPT Replacement
NOT = Truth Oracle
```

The correct framing:

```text
المشروع هو حاجز شفاف حول الصندوق الأسود:
لا يفتح داخله،
ولا يصدق خارجه مباشرة،
بل يحوّل مخرجه إلى كائن تحقق معقولية
ذي أثر ورتبة وبقايا ودليل وبوابات،
يمكن فحصه آليًا وإنسانيًا وفق قوانين المشروع.
```

---

## What This Law Forbids

| Forbidden action | FailureCode |
|------------------|-------------|
| Claiming to inspect LLM internals | `M_TBA_01` |
| Treating LLM output as true by default | `M_TBA_02` |
| Hiding any step, rejection, or residual | `M_TBA_03` |
| Placing MaqamGPT after verification | `M_TBA_04` |
| Invoking Arabic analysis without NeedGate justification | `M_TBA_05` |
| Using "certificate" language implying authority | `M_TBA_06` |
| Claiming absolute truth or guarantee | `M_TBA_07` |
| Making L0→L7 a mandatory pipeline for all answers | `M_TBA_08` |
| Issuing verdict without scope declaration | `M_TBA_09` |
| Equating `REASONABLE` with `TRUE` | `M_TBA_10` |

---

## Relationship to Existing Documents

| Document | This Law's Relationship |
|----------|------------------------|
| `docs/54` | Defines the goal → this law defines the architecture achieving it |
| `docs/55` | Defines the origins → this law shows where they plug in |
| `docs/56` | Defines the output object → this law defines the process producing it |
| `docs/57` (this) | Defines the overall barrier architecture |
| `docs/58` (future) | Will define composition algebra for RPOs under strict conditions |

---

## Summary

```text
Taaqol-GPT is a Transparent Reasonableness Barrier:
a boundary architecture around black-box LLMs that transforms
their external answers into traceable, evidence-bound,
rank-limited, residual-visible reasonableness proof objects.

It proves not that the answer is absolutely true,
but that the verdict about its reasonableness is procedurally justified
under declared origins, evidence, gates, rank, residuals, and trace.
```

```text
تعقّل-GPT هو حاجز معقولية شفاف حول الصندوق الأسود:
لا يفتح النموذج،
ولا يصدق جوابه مباشرة،
بل يحوّل الجواب إلى كائن تحقق معقولية
قابل للتتبع والمراجعة،
يثبت صحة مسار الحكم لا حقيقة الدعوى المطلقة.
```

---

*End of Transparent Barrier Architecture Law*
