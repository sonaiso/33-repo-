# GPT Answer Reasonableness Objective Law — `docs/54`

## Authority
`docs/00_MAQOOL_CONSTITUTION.md §5 Rule 1` (Layered Implementation Order).
`docs/15_PROJECT_ROADMAP.md` (Strategic Vision).

## Phase
GPT-R0 — Objective Correction Law.

---

## Declaration of Operational Goal

The operational goal of this system is:

> **Verifying the reasonableness (معقولية) of GPT answers as claims in context,
> NOT performing Arabic linguistic analysis for its own sake.**

---

## Binding Definitions

### MaqamGPT — مقام جي بي تي

```text
MaqamGPT = سؤال المستخدم وقيوده ومجاله ومخاطره.
```

The context in which the GPT answer is given. Includes:
- `question_type`: the kind of question (scientific, legal, historical, technical, etc.)
- `domain`: the knowledge domain
- `constraints`: what the user requested or prohibited
- `risk_level`: potential harm of an incorrect answer
- `evidence_need`: what kind of evidence the domain demands

---

### MantuqGPT — منطوق جي بي تي

```text
MantuqGPT = الدعاوى الصريحة في جواب GPT.
```

The explicit claims made by the GPT answer. Each claim has:
- `subject`: what entity the claim is about
- `predicate`: what is being asserted
- `qualifier`: any restriction or condition
- `modality`: level of certainty (assertion, suggestion, possibility)
- `domain`: knowledge area of the claim
- `span_trace`: pointer to the exact text in the answer

---

### MafhumGPT — مفهوم جي بي تي

```text
MafhumGPT = اللوازم الضمنية للجواب ومخاطره.
```

The implicit commitments and risks of the GPT answer. Includes:
- `implicit_commitments`: what the answer necessarily entails
- `unstated_assumptions`: what the answer takes for granted
- `risk_implications`: potential harms if the entailments are wrong
- `overclaim_candidates`: places where the answer may say more than evidence supports

**Rule**: MafhumGPT is a licensed branch of MantuqGPT. No mafhum without a closed mantuq.

---

### ReasonablenessGPT — معقولية جي بي تي

```text
ReasonablenessGPT = جواب ملائم للمقام، مدعوم بالدليل، بلا تناقض، بلا قفزة، بلا بقايا مخفية.
```

A GPT answer is REASONABLE if and only if:
1. It fits the MaqamGPT (user's question, domain, constraints).
2. Its MantuqGPT claims are supported by evidence or stable origins.
3. Its MafhumGPT implications do not contradict known origins.
4. It contains no forbidden leap (appearance → cause, possibility → certainty, form → meaning).
5. Its residuals are visible, not hidden.

---

### NeedGate — بوابة الحاجة

```text
NeedGate = لا تحليل لغوي إلا عند الحاجة لتدقيق دعوى بعينها.
```

No linguistic layer (morphology, syntax, semantics, pragmatics) opens unless
the verification of a specific GPT claim requires it.

| Layer | Opens when... |
|-------|---------------|
| Morphology (صرف) | a claim's meaning depends on derivational form |
| Syntax (نحو) | a claim's relation structure is ambiguous |
| Semantics (دلالة) | a claim's truth/metaphor status is disputed |
| Pragmatics (تداول) | a claim's force (report vs. command vs. wish) is unclear |
| Reference (إحالة) | a pronoun, demonstrative, or qualifier changes the verdict |

**Forbidden**: opening any layer "just to be thorough" without a declared need.

---

## Verdict States

The final output of the system is `GPTAnswerReasonablenessVerdict`:

| State | Meaning |
|-------|---------|
| `REASONABLE` | All gates pass; answer fits context, supported, no contradiction |
| `PARTIALLY_REASONABLE` | Some claims pass, others fail |
| `UNREASONABLE` | Critical gate failure (contradiction, forbidden leap, overclaim) |
| `OFF_MAQAM` | Answer does not address the user's question |
| `UNSUPPORTED` | Factual claims lack evidence in the required domain |
| `CONTRADICTORY` | Answer contradicts a stable knowledge origin |
| `OVERCLAIMED` | Claims exceed available evidence |
| `ORIGIN_CONTRADICTION` | Explicit conflict with classified prior knowledge |
| `FORBIDDEN_LEAP` | Illegitimate inference (appearance → cause, etc.) |
| `RESIDUAL_BLOCKED` | Hidden residuals prevent verdict |
| `NEEDS_CLARIFICATION` | Insufficient information to decide |

---

## The Reasonableness Formula

```text
GPTAnswerReasonableness =
    MaqamFit
  + MantuqControl
  + MafhumRiskControl
  + OriginBinding
  + EvidenceSupport
  + Coherence
  + NoForbiddenLeap
  + VisibleResiduals
  + BoundedRank
  + TraceContinuity
```

All 10 gates must pass for `REASONABLE`. Any single failure produces
a specific verdict state with `FailureCode` and trace.

---

## Forbidden Leaps (exhaustive list)

| From | To | Why forbidden |
|------|----|---------------|
| Appearance | Self-source | Looking bright ≠ producing light |
| Possibility | Certainty | "could be" ≠ "is" |
| Candidate | Certificate | Unverified claim ≠ proven truth |
| Form | Meaning | Grammatical pattern ≠ semantic content |
| Claim | Evidence | Asserting X ≠ proving X |
| Correlation | Causation | Co-occurrence ≠ cause |

---

## Instrumental Chain (شروط الإمكان)

```text
معقولية الجواب
  └── شرطها: المفهوم (لوازم الجواب)
        └── شرطه: المنطوق (الدعاوى الصريحة)
              └── شرطه: الإخبار أو الإنشاء
                    └── شرطه: النسب الإسنادية والتضمينية والتقييدية
                          └── شرطها: الفاعلية والمفعولية والسببية
                                └── شرطها: اللفظ المفرد (الكيان/الجنس + الصفة/المصدر)
                                      └── شرطه: الأوزان والمقاطع والحروف (L0)
```

Each layer is built **only** because the layer above it needs it.

---

## What This Law Forbids

| Forbidden action | FailureCode |
|------------------|-------------|
| Analyzing Arabic for its own sake without GPT verification need | `M_R0_01` |
| Issuing MantuqGPT without MaqamGPT context | `M_R0_02` |
| Issuing MafhumGPT without closed MantuqGPT | `M_R0_03` |
| Issuing verdict without OriginBinding | `M_R0_04` |
| Opening a linguistic layer without NeedGate justification | `M_R0_05` |
| Treating GPT answer as truth (bypassing verification) | `M_R0_06` |
| Issuing verdict without trace | `M_R0_07` |
| Hidden residuals in final verdict | `M_R0_08` |

---

## Methodology Statement

```text
نحن لا نحلل جواب GPT لأنه نص عربي فقط.
نحلله لأنه دعوى في مقام.

ولا نطلب المنطوق لذاته.
نطلبه لأنه أصل المفهوم.

ولا نطلب المفهوم لذاته.
نطلبه لأنه يكشف اللوازم والمخاطر.

ولا نطلب المقام لذاته.
نطلبه لأنه أصل الملاءمة.

ولا نطلب الدلالة والصرف والنحو لذاتها.
نطلبها عند الحاجة لأنها شروط إمكان الحكم على المعقولية.

ولا نحكم على المعقولية من النص وحده.
بل نربط النص بأصول معرفية:
كيان، صفة/حدث، علاقة/أداة، إحالة، ودليل.
```

---

*End of GPT Answer Reasonableness Objective Law*
