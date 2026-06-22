# خارطة طريق مشروع تعقُّل — Project Roadmap

## المرجعية
`docs/00_MAQOOL_CONSTITUTION.md §5 Rule 1` — الترتيب الطبقي الإلزامي

---

## الرؤية العامة

> بناء نظام تدقيق معقولية إجابات GPT، محكوم دستوريًا ومبني على أربع طبقات متسلسلة (L0→L1→L2→L3).
> التحليل اللغوي (L0-L1) هو **شرط إمكان** للتدقيق وليس غاية بذاته.
> الهدف النهائي: إدخال إجابة GPT ← تحليلها عبر الطبقات ← إصدار حكم على معقوليتها
> (MAQOOL / GHAYR_MAQOOL / MU'ALLAQ).

### الهدف الاستراتيجي النهائي

```
إجابة GPT ──► تحليل بنيوي (L0) ──► تعريف رسمي (L1) ──► قياس واستدلال (L2) ──► حكم المعقولية (L3)
                                                                                         │
                                                                              ┌──────────┼──────────┐
                                                                              ▼          ▼          ▼
                                                                          MAQOOL   GHAYR_MAQOOL  MU'ALLAQ
                                                                          (معقول)   (غير معقول)   (معلّق)
```

### العلاقة بين الطبقات والهدف

| الطبقة | الدور في التدقيق | الدور في المنظومة |
|--------|------------------|------------------|
| L0 (لغة موضوعية) | تفكيك بنية إجابة GPT إلى كيانات أساسية | شرط إمكان — توفير المادة الخام |
| L1 (وصف رسمي) | تعريف معايير المعقولية (ما الذي يجعل إجابة معقولة؟) | شرط إمكان — بناء القاموس المرجعي |
| L2 (منطق واستدلال) | مقارنة إجابة GPT بالمعايير المرجعية (هل تتطابق؟) | محرك المقارنة والقياس |
| L3 (واقع وتطبيق) | إصدار حكم نهائي على المعقولية | **الهدف النهائي** — الحكم: معقول / غير معقول / معلّق |

---

## المبادئ الحاكمة لخارطة الطريق

| # | المبدأ | الهدف |
|---|--------|-------|
| 1 | **إغلاق قبل انتقال** | لا تُفتح L(n+1) حتى تُغلق L(n) |
| 2 | **PR واحد = هدف واحد** | كل PR يحقق مخرجًا واحدًا محددًا قابلاً للاختبار |
| 3 | **لا انفجار** | عدد PRs محدود ومُرقّم مسبقًا لكل مرحلة |
| 4 | **لا قفز** | Rule 8 (No-Leap Axiom) ينطبق على التطوير كما ينطبق على الكيانات |
| 5 | **اختبار أولاً** | كل مخرج له اختبار قبل إغلاق PR |

---

## الوضع الحالي

| المرحلة | الحالة | عدد PRs المنجزة | الباقي |
|---------|--------|----------------|--------|
| Phase 0 (L0) | ✅ مكتمل | مغلق رسميًا | 0 |
| Phase 1 (L1) | ✅ مكتمل | سلسلة إنجازات حتى PR #43 + إعلان الإغلاق | 0 |
| Phase 2 (L2) | 🔒 مقفل | 0 | محجوب حتى إعلان إغلاق L1 |
| Phase 3 (L3) | 🔒 مقفل | 0 | محجوب حتى إعلان إغلاق L2 |

---

## Phase 0 — طبقة اللغة الموضوعية (L0) ✅ مكتمل

### الهدف
تمثيل جميع كيانات اللغة العربية على المستوى الصوتي/الخطّي كهياكل بيانات مجمّدة.

### المدخلات
- الدستور (§2 Category 2, §3 MCE-1, §4 MCE-2)
- 28 حرفًا عربيًا + 4 حركات قصيرة + 3 حروف مد
- 8 أنماط صوتية + 4 أنواع مقاطع

### المخرجات المُنجزة
| المخرج | الملف | الاختبار |
|--------|-------|---------|
| أنماط صوتية (8) | `L0/phoneme.py` | `tests/L0/test_phoneme.py` |
| حروف عربية (28) | `L0/grapheme.py` | `tests/L0/test_grapheme.py` |
| حركات (7) | `L0/vowel.py` | ✅ |
| مقاطع (4 أنواع) | `L0/syllable.py` | `tests/L0/test_syllable.py` |
| المنطوق | `L0/utterance.py` | ✅ |
| الدال | `L0/signifier.py` | ✅ |
| المدلول | `L0/signified.py` | ✅ |
| اتحاد الدلالة | `L0/union.py` | ✅ |
| نوع الدلالة | `L0/signification.py` | ✅ |
| الجامد | `L0/jamid.py` | `tests/L0/test_jamid.py` |
| حروف المعاني | `L0/harf_maani.py` | `tests/L0/test_harf_maani.py` |
| الوزن | `L0/weight.py` | ✅ |
| الوقف والوصل | `L0/waqf_wasl.py` | `tests/L0/test_waqf_wasl_closure.py` |
| محرك التشغيل | `runtime/constitutional_engine.py` | `tests/runtime/` |

### شرط الإغلاق
- [x] جميع الاختبارات تمر
- [x] الحارس الدستوري يمر (`ci/constitutional_guard.py`)
- [x] لا يوجد كيان L1+ في الشيفرة
- [x] **مراجعة نهائية وإعلان إغلاق رسمي** (`docs/L0_CLOSURE_DECLARATION.md`)

---

## Phase 1 — طبقة الوصف الرسمي (L1) ✅ مكتمل

### الهدف
تحويل كيانات L0 إلى تعريفات رسمية ومسلّمات وأفكار عامة تُشكّل **معايير المعقولية** —
أي القواعد المرجعية التي تُقاس عليها إجابات GPT لتحديد ما إذا كانت معقولة أم لا.

### شرط الفتح
- [x] إعلان إغلاق L0 رسميًا (`docs/L0_CLOSURE_DECLARATION.md`)

### المدخلات
- جميع كيانات L0 (13 كيان)
- الدستور (§6 L1 Boundary)
- `docs/02_L1_META_LANGUAGE_BOUNDARY.md`

### المخرجات المنجزة حتى PR #43

| PR | الهدف | المخرج | الاختبار |
|----|-------|--------|---------|
| PR-9 → PR-12 | فتح L1 + تعريفات/مسلّمات/أفكار عامة | `L1/definition.py`, `L1/postulate.py`, `L1/common_notion.py` | `tests/L1/test_l1_definition.py`, `tests/L1/test_l1_postulate.py`, `tests/L1/test_l1_common_notion.py` |
| PR-33 | Proof Objects contract-only | `L1/proof_objects.py` | `tests/L1/test_proof_objects.py` |
| PR-34 | Domain IDs + Gate/Bridge specs | `L1/domain_ids.py`, `L1/domain_bridge_gate.py` | `tests/L1/test_domain_ids.py`, `tests/L1/test_gate_bridge_specs.py` |
| PR-35 | DAL atomic layer contracts | `L1/dal_atomic.py` | `tests/L1/test_dal_atomic_contracts.py` |
| PR-36 | LAFZI form contract layer | `L1/lafzi_form.py` | `tests/L1/test_lafzi_form_contracts.py`, `tests/test_lafzi_form_contract.py` |
| PR-37 | DAL→LAFZI declarative bridge spec | `L1/dal_to_lafzi_bridge.py` | `tests/L1/test_dal_to_lafzi_bridge_specs.py` |
| PR-38 | Runtime embargo + failure-alignment guardrails | `docs/12`, `docs/13`, `data/failure_alignment.csv` | `tests/test_runtime_embargo_constitution.py`, `tests/test_failure_alignment_matrix.py` |
| PR-41 → PR-43 | Closure/Conflict kernel contracts + hotfix | `core/closure_kernel.py`, `L1/signifier_domain.py` | `tests/core/test_closure_kernel.py`, `tests/core/test_conflict_engine.py`, `tests/L1/test_signifier_domain_contracts.py` |

### مخرجات حزمة الإغلاق (مكتملة)

- **L1 Closure Pack**:
  1. [x] تشغيل `pytest tests/`
  2. [x] تشغيل `pytest tests/test_kpi_indicators.py -v`
  3. [x] تشغيل `python -m ci.constitutional_guard --source-dir src`
  4. [x] توثيق إعلان الإغلاق في `docs/L1_CLOSURE_DECLARATION.md`
  5. [x] تحديث الوثائق المرجعية لتوافق حالة PR #43

### شرط الإغلاق
- [x] جميع اختبارات المشروع تمر
- [x] مؤشرات KPI تمر
- [x] الحارس الدستوري يمر
- [x] توثيق إغلاق L1 في `docs/L1_CLOSURE_DECLARATION.md`
- [x] بقاء L2/L3 مقفلتين حتى اعتماد إعلان الإغلاق

---

## Phase 2 — طبقة المنطق (L2) 🔒 مقفل

### الهدف
بناء **محرك مقارنة وقياس** يأخذ إجابة GPT (بعد تفكيكها في L0 وتعريفها في L1)
ويقارنها بالمعايير المرجعية — يختبر: هل العلة الجامعة موجودة؟ هل الوصف المؤثر صحيح؟
هل يوجد فرق قادح يبطل المعقولية؟

### شرط الفتح
- إعلان إغلاق L1 رسميًا

### المدخلات
- تعريفات L1 (Definition, Postulate, CommonNotion)
- الدستور (§6 L2 Boundary)
- `docs/03_L2_LOGICAL_BOUNDARY.md`

### المخرجات المطلوبة (5 PRs)

| PR | الهدف | المخرج | الاختبار |
|----|-------|--------|---------|
| PR-14 | إعلان إغلاق L1 + فتح L2 | وثيقة إغلاق | `test_l1_closure_declaration.py` |
| PR-15 | محرك القياس | `L2/qiyas.py` — بنية القياس (مقدمة كبرى، صغرى، نتيجة) | `test_l2_qiyas.py` |
| PR-16 | محرك البرهان | `L2/proof.py` — سلاسل إثبات من مسلّمات إلى نتائج | `test_l2_proof.py` |
| PR-17 | الإغلاق المنطقي | `L2/closure.py` — اختبار اكتمال المنظومة | `test_l2_closure.py` |
| PR-18 | جسر L1→L2 + إغلاق | `L2/meta_bridge.py` | `test_l2_bridge.py` |

### شرط الإغلاق
- [ ] محرك القياس يُنتج نتائج صحيحة
- [ ] TransitionGate(L1→L2) يعمل
- [ ] Identity(L1) ⊆ Identity(L2) محفوظ
- [ ] لا يوجد حكم واقعي (L3) في شيفرة L2

---

## Phase 3 — طبقة الواقع (L3) 🔒 مقفل

### الهدف
**إصدار حكم المعقولية النهائي** على إجابة GPT:
- `MAQOOL` (معقولة): الانتقالات مرخصة + لا مانع + العلة صحيحة
- `GHAYR_MAQOOL` (غير معقولة): يوجد مانع أو فرق قادح أو علة غير صحيحة
- `MU'ALLAQ` (معلّقة): لا يمكن الحكم لنقص الدليل أو غموض غير قابل للحل

يشمل: أنواع الأدلة، تحقيق المناط (ربط الإجابة بالواقع)، إصدار الحكم، وتنزيله على الإجابة.

### شرط الفتح
- إعلان إغلاق L2 رسميًا

### المدخلات
- براهين L2 (Qiyas, Proof, Closure)
- الدستور (§6 L3 Boundary)
- `docs/04_L3_REALITY_BOUNDARY.md`

### المخرجات المطلوبة (6 PRs)

| PR | الهدف | المخرج | الاختبار |
|----|-------|--------|---------|
| PR-19 | إعلان إغلاق L2 + فتح L3 | وثيقة إغلاق | `test_l2_closure_declaration.py` |
| PR-20 | أنواع الأدلة | `L3/evidence.py` — Evidence types | `test_l3_evidence.py` |
| PR-21 | تحقيق المناط | `L3/manat.py` — Manat verification | `test_l3_manat.py` |
| PR-22 | مرشحات الحكم | `L3/hukm.py` — HukmCandidate | `test_l3_hukm.py` |
| PR-23 | التنزيل | `L3/tanzil.py` — TanzilCandidate | `test_l3_tanzil.py` |
| PR-24 | جسر L2→L3 + إغلاق نهائي | `L3/meta_bridge.py` | `test_l3_bridge.py` |

### شرط الإغلاق
- [ ] جميع أنواع الأدلة مُمثّلة
- [ ] المناط قابل للتحقيق
- [ ] TransitionGate(L2→L3) يعمل
- [ ] Identity(L2) ⊆ Identity(L3) محفوظ
- [ ] المنظومة الكاملة مُغلقة

---

## ملخّص تنفيذي

```
المجموع الكلي: 24 PR مُرقّم ومُوجّه
├── Phase 0 (L0): 8 PRs  ✅ مكتمل
├── Phase 1 (L1): 5 PRs  ✅ مكتمل
├── Phase 2 (L2): 5 PRs  🔒 مقفل
└── Phase 3 (L3): 6 PRs  🔒 مقفل
```

### مبدأ عدم الانفجار

| القاعدة | الشرح |
|---------|-------|
| **PR واحد = ملف واحد رئيسي** | لا يُنشئ PR أكثر من ملف مصدر رئيسي واحد |
| **ترقيم مُسبق** | كل PR مُرقّم في الخارطة قبل البدء |
| **لا PRs خارج الخارطة** | أي عمل خارج هذه القائمة يحتاج تعديل دستوري |
| **مراجعة قبل إغلاق** | لا يُغلق PR بدون اختبارات ناجحة |
| **لا عمل متوازي على طبقتين** | Rule 8 يحكم التطوير |

---

## مخطط التدفق

```
[الدستور] ──────────────────────────────────────────────────────┐
     │                                                            │
     ▼                                                            │
[Phase 0: L0]                                                     │
  المدخل: 28 حرف + 4 حركات + 8 أنماط                             │
  المخرج: 13 كيان L0 مجمّد + محرك تشغيل                             │
  الدور: تفكيك بنية إجابة GPT إلى كيانات أساسية                   │
  الحالة: ✅ مكتمل + مُغلق رسميًا                                   │
     │                                                            │
     ▼ (إغلاق رسمي ✅ — docs/L0_CLOSURE_DECLARATION.md)           │
[Phase 1: L1]                                                     │
  المدخل: 13 كيان L0                                              │
  المخرج: تعريفات + مسلّمات + أفكار عامة + جسر                   │
  الدور: بناء معايير المعقولية المرجعية                            │
  الحالة: ✅ مكتمل — تم تنفيذ سلسلة PR-33..PR-43 مع اعتماد حزمة الإغلاق │
     │                                                            │
     ▼ (إغلاق رسمي عبر L1 Closure Declaration)                   │
[Phase 2: L2]                                                     │
  المدخل: تعريفات L1                                              │
  المخرج: محرك قياس + محرك برهان + إغلاق                         │
  الدور: مقارنة إجابة GPT بالمعايير (هل تتطابق؟)                 │
  الحالة: 🔒 مقفل                                                  │
     │                                                            │
     ▼ (إغلاق رسمي PR-19)                                        │
[Phase 3: L3]                                                     │
  المدخل: براهين L2                                               │
  المخرج: أدلة + مناط + حكم + تنزيل                              │
  الدور: إصدار حكم المعقولية (MAQOOL/GHAYR_MAQOOL/MU'ALLAQ)     │
  الحالة: 🔒 مقفل                                                  │
     │                                                            │
     ▼                                                            │
[النظام المكتمل] ◄────────────────────────────────────────────────┘
  إدخال إجابة GPT ← تحليل ← مقارنة ← حكم على المعقولية
```

---

## حوكمة التفريع — Branching Governance

### المبدأ

> لا يُسمح بأي تفريع (branch) عن الأصل (trunk) حتى يكتمل الأصل بالحد الأدنى.
> كل فرع يتطلب ترخيصًا (`BranchLicense`) يحمل: دافعًا، ووصفًا مؤثرًا، وفرقًا قادحًا،
> وشرطًا، وسببًا، وتحققًا من المانع. الفرع المُرخّص يمكنه ترخيص تفريع جديد بنفس المنهجية.

### الإلزام (Enforcement)

| الآلية | الملف | الوصف |
|--------|-------|-------|
| `BranchLicense` dataclass | `constitution/branch_license.py` | كيان مجمّد يمنع البناء بدون استيفاء جميع الشروط |
| CI Guard check | `ci/constitutional_guard.py` | يرفض أي ملف مصدر لا يرجع لمرجع دستوري أو خارطة طريق |
| Failure codes | `M_CX_16..M_CX_20` | أكواد رفض مسمّاة لكل انتهاك |

### شروط ترخيص الفرع (7 شروط إلزامية)

| # | الشرط | الوصف | كود الرفض |
|---|--------|-------|-----------|
| 1 | **مرجع الخارطة** (roadmap_ref) | يجب أن يشير لـ PR مرقّم أو قسم في الخارطة | `M_CX_16` |
| 2 | **اكتمال الأصل** (trunk_complete) | الأصل يجب أن يكون مكتملاً بالحد الأدنى | `M_CX_17` |
| 3 | **الدافع** (motive) | لماذا هذا الفرع موجود | `M_CX_18` |
| 4 | **الوصف المؤثر** (description) | ما الذي يميّز هذا الفرع عن الأصل | `M_CX_19` |
| 5 | **الفرق القادح** (qualifying_difference) | الفرق الجوهري الذي يفصله عن الأصل | `M_CX_19` |
| 6 | **الشرط** (condition) + **السبب** (cause) | ماذا يجب أن يتحقق ولماذا | `M_CX_18` / `M_CX_20` |
| 7 | **غياب المانع** (barrier_absent) | تحقق من عدم وجود ما يمنع الفرع | `M_CX_20` |

### التشجير — Recursive Branching

```
[الأصل / الخارطة]
    │
    ├── فرع مرخّص A (BranchLicense ✓)
    │       │
    │       ├── فرع فرعي A.1 (BranchLicense ✓ — الأصل هو A)
    │       └── فرع فرعي A.2 (BranchLicense ✓ — الأصل هو A)
    │
    └── فرع مرخّص B (BranchLicense ✓)
            │
            └── فرع فرعي B.1 (BranchLicense ✓ — الأصل هو B)
```

**القاعدة**: الفرع المُرخّص يمكنه ترخيص تشجير جديد عبر `license_sub_branch()`
بشرط أن الفرع نفسه مكتمل بالحد الأدنى أولاً.

### مثال على ترخيص

```python
from taaqqul_slot_geometry.constitution import BranchLicense

license = BranchLicense(
    roadmap_ref="docs/15_PROJECT_ROADMAP.md Phase 1 PR-10",
    parent_ref="Phase 1 — L1 Closure",
    trunk_complete=True,  # L0 مكتمل
    motive="تحويل كيانات L0 إلى تعريفات رسمية",
    description="L1/definition.py — تعريف رسمي لكل كيان L0",
    qualifying_difference="L0 = كيانات خام، L1 = تعريفات رسمية مع شروط حدود",
    condition="L0 مُغلق رسميًا",
    cause="الاستدلال المنطقي يحتاج تعريفات رسمية كمدخل",
    barrier_absent=True,
    barrier_check_description="لا يوجد كيان L0 ناقص أو residual مفتوح",
)
```

---

## الخطوة التالية الفورية

**Prepare L1 closure declaration and roadmap reconciliation**

المطلوب:
1. إضافة `docs/L1_CLOSURE_DECLARATION.md`
2. تثبيت شرط عدم فتح L2 دون وثيقة إغلاق L1
3. تشغيل الاختبارات الكاملة + KPI + constitutional guard
4. إبقاء نطاق العمل داخل L1 (لا qiyas / لا ifadah / لا hukm / لا reality/tanzil)

---

*نهاية خارطة الطريق*
