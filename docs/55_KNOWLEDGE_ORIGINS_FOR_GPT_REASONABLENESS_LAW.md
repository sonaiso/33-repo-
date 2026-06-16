# Knowledge Origins for GPT Reasonableness Law — `docs/55`

## Authority
`docs/00_MAQOOL_CONSTITUTION.md §5 Rule 1` (Layered Implementation Order).
`docs/54_GPT_ANSWER_REASONABLENESS_OBJECTIVE_LAW.md` (Operational Goal).

## Phase
GPT-K0 — Knowledge Origins Boundary Law.

---

## Declaration

> No GPT reasonableness verdict may be issued without binding relevant claims
> to at least one required knowledge origin, or explicitly declaring an origin residual.

---

## The Five Knowledge Origins

### Origin 1 — EntityGenusOrigin (أصل الكيانات والأجناس)

**Purpose**: Knowing what the entity mentioned in a GPT claim **is** —
its genus, species, physical class, and stable constraints.

**Answers the question**:
> Is this entity capable of bearing this predicate or claim?

**Schema**:
```text
entity_id:          unique identifier
arabic_surface:     Arabic surface form(s)
genus:              highest category (جرم سماوي, حيوان, نبات, مادة, مفهوم, ...)
species:            specific type within genus
physical_class:     material classification if applicable
stable_constraints: list of known invariant properties
  - what it CAN do/be
  - what it CANNOT do/be
linguistic_gender:  masculine / feminine / variable
rationality:        rational / non_rational / abstract
```

**Example**:
```text
entity_id: moon
arabic_surface: القمر
genus: جرم سماوي
species: قمر تابع لكوكب
physical_class: جسم عاكس للضوء
stable_constraints:
  - self_luminous: false
  - reflects_light: true
  - orbits_earth: true
linguistic_gender: masculine
rationality: non_rational
```

---

### Origin 2 — AttributeEventOrigin (أصل الصفات والأحداث)

**Purpose**: Knowing the nature of the predicate (attribute or event)
that the GPT answer ascribes to an entity.

**Answers the question**:
> What are the conditions for ascribing this attribute/event?
> Is it intrinsic or extrinsic? Self-caused or other-caused?

**Schema**:
```text
attribute_id:       unique identifier
arabic_surface:     Arabic surface form(s)
source:             masdar (verbal noun) from which derived
root:               Arabic root letters
form:               morphological form (اسم فاعل, صفة مشبهة, ...)
semantic_domain:    فيزيائي / بيولوجي / نفسي / اجتماعي / منطقي / ...
requires_bearer:    true/false — must be predicated of something
requires_source:    what enables this attribute (e.g., source of light)
compatible_modes:   list of ways this attribute can hold
distinction_required: critical distinctions the user must respect
```

**Example**:
```text
attribute_id: luminous
arabic_surface: مضيء
source: إضاءة
root: ض و ء
form: اسم فاعل / صفة فاعلية
semantic_domain: فيزيائي
requires_bearer: true
requires_source: source_of_light
compatible_modes:
  - self_luminous (ذاتي الإضاءة)
  - reflected_luminous (عاكس للضوء)
distinction_required:
  - مضيء بذاته ≠ مضيء بغيره
```

---

### Origin 3 — RelationOperatorOrigin (أصل العلاقات والأدوات)

**Purpose**: Knowing the type of relation that connects an entity
to a predicate, qualifier, or another entity in the GPT answer.

**Answers the question**:
> What relation does this operator/particle/qualifier establish?
> Does it change the truth conditions of the claim?

**Schema**:
```text
operator_id:        unique identifier
arabic_surface:     Arabic surface form(s)
operator_type:      حرف جر / ظرف / أداة شرط / أداة ربط / ...
relation_candidates: list of possible semantic relations
  - سببية (causation)
  - استعانة (instrumentality)
  - إلصاق (attachment)
  - مصاحبة (accompaniment)
  - ظرفية (temporal/spatial location)
  - تعليل (reason)
  - غاية (purpose)
effect_on_claim:    how this operator modifies the claim's meaning
```

**Example**:
```text
operator_id: ba_bi_dhatihi
arabic_surface: بذاته
operator_type: باء + ضمير راجع
relation_candidates:
  - سببية ذاتية (self-source)
  - مصاحبة (accompaniment)
effect_on_claim:
  converts "مضيء" from observed brightness
  to claim that light SOURCE is internal to entity
```

---

### Origin 4 — ReferenceOrigin (أصل الإحالات)

**Purpose**: Knowing what pronouns, demonstratives, relative clauses,
and self-references point to in the GPT answer.

**Answers the question**:
> Does this reference/pronoun/qualifier point to the correct entity?
> Does resolving the reference change the verdict?

**Schema**:
```text
reference_id:       unique identifier
arabic_surface:     Arabic surface form
reference_type:     ضمير / اسم إشارة / اسم موصول / إحالة ذاتية / ...
refers_to:          the entity or claim being pointed at
agreement:          gender/number/person agreement
effect_on_claim:    how resolving this reference affects the claim
ambiguity_risk:     whether the reference has multiple valid targets
```

**Example**:
```text
reference_id: dhatihi_in_moon_claim
arabic_surface: ذاته
reference_type: إحالة ذاتية (self-reference)
refers_to: القمر (the moon entity)
agreement: masculine singular
effect_on_claim:
  transfers the qualifier to the entity itself,
  asserting that the source of light is INTERNAL to the moon
ambiguity_risk: low — clear anaphoric resolution
```

---

### Origin 5 — EvidenceOrigin (أصل الدليل)

**Purpose**: Recording whether a factual claim in the GPT answer
has supporting evidence, and what kind.

**Answers the question**:
> Is this claim supported? By what kind of evidence? How reliable?

**Schema**:
```text
evidence_id:        unique identifier
claim_ref:          which MantuqGPT claim this evidence supports/refutes
source_type:        نص / عقل / تجربة / عرف / إجماع / مشاهدة / ...
reliability:        قطعي / ظني / احتمالي / مشكوك / مرفوض
direction:          supports / contradicts / neutral
recency:            stable (لا يتغير) / current (يتغير) / historical (سابق)
evidence_summary:   brief description of the evidence
```

**Example**:
```text
evidence_id: moon_light_source_evidence
claim_ref: "القمر مضيء بذاته"
source_type: تجربة / علم فيزيائي
reliability: قطعي
direction: contradicts
recency: stable
evidence_summary:
  القمر لا يصدر ضوءًا ذاتيًا. ضوؤه انعكاس لضوء الشمس.
  مصدر: علم الفلك المعاصر — حقيقة مستقرة.
```

---

## Binding Rules

### Rule K0-1 — No verdict without origin binding
Every factual claim in MantuqGPT MUST be bound to at least one knowledge origin
before a reasonableness verdict is issued.

**FailureCode**: `M_K0_01`

### Rule K0-2 — Origin residual declaration
If a claim cannot be bound to an origin (because the origin is unknown or missing),
the system MUST declare an `origin_residual` explicitly. Hidden gaps are forbidden.

**FailureCode**: `M_K0_02`

### Rule K0-3 — Origin contradiction blocks reasonableness
If a claim contradicts a stable knowledge origin, the verdict MUST be
`UNREASONABLE` or `ORIGIN_CONTRADICTION`. No override without amendment.

**FailureCode**: `M_K0_03`

### Rule K0-4 — Evidence requirement for factual claims
Any claim classified as `factual` in a `high_risk` domain MUST have
an EvidenceOrigin entry. Absence produces `UNSUPPORTED` verdict.

**FailureCode**: `M_K0_04`

### Rule K0-5 — Origins are not exhaustive
The knowledge origins are NOT a complete encyclopedia. They are a **minimal
classified prior knowledge layer** that prevents the system from judging
from a vacuum. Missing origins are declared as residuals, not silently skipped.
Treating origins as an exhaustive encyclopedia is forbidden.

**FailureCode**: `M_K0_05`

### Rule K0-6 — Frozen origins
All origin entries are immutable once classified. Updates require a new
origin entry with trace to the amendment.

**FailureCode**: `M_K0_06`

### Rule K0-7 — Origins serve GPT verification only
Origins exist to verify GPT claims. Building or extending origins for
linguistic analysis rather than GPT verification need is forbidden.

**FailureCode**: `M_K0_07`

---

## Relationship Between Origins and Verification Flow

```text
GPT Answer
  │
  ├─► MaqamGPT (domain, constraints, risk)
  │
  ├─► MantuqGPT (explicit claims with subject, predicate, qualifier)
  │     │
  │     ├─ claim.subject ──────► EntityGenusOrigin
  │     ├─ claim.predicate ────► AttributeEventOrigin
  │     ├─ claim.operator ─────► RelationOperatorOrigin
  │     ├─ claim.reference ────► ReferenceOrigin
  │     └─ claim.evidence_need ► EvidenceOrigin
  │
  ├─► MafhumGPT (implications derived from bound MantuqGPT)
  │
  └─► ReasonablenessGates (10 gates)
        │
        └─► GPTAnswerReasonablenessVerdict
```

---

## Minimal Golden Origins Dataset (Scope for GPT-K2)

The initial dataset is deliberately small — enough to test the system:

| Category | Count | Purpose |
|----------|-------|---------|
| EntityGenusOrigin | 50 entries | Common entities in GPT answers |
| AttributeEventOrigin | 50 entries | Common predicates |
| RelationOperatorOrigin | 30 entries | Arabic operators and particles |
| ReferenceOrigin | 30 entries | Common reference patterns |
| EvidenceOrigin types | 20 entries | Evidence type classifications |

This is NOT an encyclopedia. It is a **test harness** for the verification engine.

---

## What This Law Forbids

| Forbidden action | FailureCode |
|------------------|-------------|
| Issuing verdict without binding claims to origins | `M_K0_01` |
| Silently skipping a missing origin (must declare residual) | `M_K0_02` |
| Accepting a claim that contradicts a stable origin | `M_K0_03` |
| Accepting high-risk factual claim without evidence | `M_K0_04` |
| Mutating a classified origin without amendment trace | `M_K0_06` |
| Treating origins as exhaustive encyclopedia | `M_K0_05` |
| Building origins for linguistic analysis rather than GPT verification | `M_K0_07` |

---

## Relationship to Existing Layers

| Existing Layer | Knowledge Origins Role |
|---------------|----------------------|
| L0 (entities) | Provides the structural building blocks that origins are ABOUT |
| L1 (definitions) | Provides formal criteria that origins must MEET |
| L2 (comparison) | USES origins to compare GPT claims against |
| L3 (verdict) | ISSUES verdict based on origin binding results |

The Knowledge Origins are the **bridge** between the existing layer system
and the GPT verification goal. They are what was missing: the reference
knowledge against which claims are tested.

---

*End of Knowledge Origins for GPT Reasonableness Law*
