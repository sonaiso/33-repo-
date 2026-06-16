# تعقُّل — Taaqol-GPT

**محرك تحليل لغوي عربي محكوم دستوريًا**

> **"لا كود بلا أصل، ولا فرع بلا ترخيص، ولا انتقال بلا إثبات"**

---

## الرؤية

بناء نظام يُحلّل اللغة العربية عبر أربع طبقات متسلسلة (L0→L1→L2→L3) بحيث:
- كل كيان مُجمّد (immutable) ومُتتبّع دستوريًا
- كل رفض مُسمّى بكود فشل واضح (`FailureCode`)
- كل دالة نقيّة (pure) — بلا آثار جانبية
- كل انتقال بين الطبقات مُرخّص ومحفوظ الهوية

---

## الأهداف الاستراتيجية

| # | الهدف | المؤشر | الحالة |
|---|-------|--------|--------|
| S1 | بناء نظام تحليل لغوي عربي كامل 4 طبقات | 4 طبقات مُغلقة + 24 PR | 🔄 33% |
| S2 | إثبات أن المنهج الدستوري قابل للتنفيذ | 0 خروقات دستورية في CI | ✅ مُحقق |
| S3 | بناء نظام قياس واستدلال (L2) | محرك قياس + محرك برهان | 🔒 مقفل |
| S4 | تطبيق نتائج الاستدلال على الواقع (L3) | أدلة + مناط + حكم + تنزيل | 🔒 مقفل |

---

## المعمارية — Architecture

```
L0 (Object Language)  →  L1 (Formal Description)  →  L2 (Logical)  →  L3 (Real-world)
```

| Layer | Domain | Status | Entities |
|-------|--------|--------|----------|
| L0 | لغة موضوعية (صوت، خط، دلالة) | ✅ Complete | 13 entities |
| L1 | وصف رسمي (تعريفات، مسلّمات، جسور) | ⏳ Pending | 0/5 |
| L2 | منطق (قياس، برهان، إغلاق) | 🔒 Locked | 0/4 |
| L3 | واقع (أدلة، مناط، حكم، تنزيل) | 🔒 Locked | 0/5 |

---

## المرجعية الجذرية — Governing Law

كل التطوير في هذا المشروع يستمد شرعيته من:

```
docs/00_MAQOOL_CONSTITUTION.md
```

**لا يُسمح بأي كود بدون `trace_ref` يُشير لقسم في هذا الدستور.**

---

## بنية الحزمة — Package Layout

```
src/taaqqul_slot_geometry/
  constitution/   ← FailureCode, IdentityPreservation, TransitionGate,
                    MaqoolConstitution, BranchLicense
  core/           ← SlotGraph (9-tuple), Rank, ResidualBundle, TraceRef
  L0/             ← Phoneme, Grapheme, Vowel, Syllable, Utterance, Signifier,
                     Signified, Union, Signification, JamidAnchor, HarfMaani,
                     Weight, WaqfWasl
  L1/             ← ⏳ PENDING (requires L0 formal closure)
  L2/             ← 🔒 LOCKED
  L3/             ← 🔒 LOCKED
  runtime/        ← ConstitutionalEngine (5-step pipeline)
```

---

## الحقول الإلزامية — Mandatory Entity Fields

كل كيان في هذا المشروع يحمل (Rule 2):

| Field | Type | Constraint |
|-------|------|------------|
| `trace_ref` | `str` | مرجع غير فارغ للدستور |
| `rank` | `str` | دائمًا `"CANDIDATE"` — لا ترقية في L0 |
| `residuals` | `FrozenSet[str]` | قد يكون فارغًا لكن يجب أن يوجد |

---

## التطوير — Development

```bash
# تثبيت البيئة التطويرية
pip install -e ".[dev]"

# تشغيل جميع الاختبارات (399 اختبار)
pytest tests/

# تشغيل اختبارات L0 فقط
pytest tests/L0/ tests/constitution/

# تشغيل مؤشرات الأداء (KPIs)
pytest tests/test_kpi_indicators.py -v

# تشغيل الحارس الدستوري
python -m ci.constitutional_guard --source-dir src
```

---

## مؤشرات الأداء — KPIs

المشروع يُقاس آليًا عبر `pytest tests/test_kpi_indicators.py`:

| KPI | الوصف | المستهدف |
|-----|-------|----------|
| KPI-01 | تغطية trace_ref | 100% |
| KPI-02 | مطابقة frozen | 100% |
| KPI-03 | تغطية FailureCode | 100% |
| KPI-04 | عدد كيانات L0 | 13 |
| KPI-05 | عدم تسرّب طبقات | 0 |
| KPI-06 | CI guard نظيف | 0 خروقات |
| KPI-07 | Residuals مُغلقة | 0 مفتوح |

---

## حوكمة التفريع — Branching Governance

لا يُسمح بأي عمل خارج خارطة الطريق بدون ترخيص (`BranchLicense`):

| الشرط | الوصف | كود الرفض |
|--------|-------|-----------|
| مرجع الخارطة | كل عمل يُشير لـ PR مرقّم | `M_CX_16` |
| اكتمال الأصل | لا فرع قبل اكتمال الأصل | `M_CX_17` |
| الدافع | لماذا هذا الفرع موجود | `M_CX_18` |
| الفرق القادح | ما الذي يميّزه عن الأصل | `M_CX_19` |
| غياب المانع | تحقق من عدم وجود ما يمنع | `M_CX_20` |

---

## القيود الأساسية — Key Constraints

- Frozen dataclasses مع `__post_init__` birth guards (Rule 3)
- دوال نقيّة فقط — لا I/O, لا network (Rule 4)
- رفض مُسمّى — لا silent exceptions (Rule 5)
- حفظ الهوية عبر الانتقالات (Rule 7)
- No-Leap Axiom: الطبقات تتقدم خطوة واحدة (Rule 8)
- لا ترقية rank فوق `CANDIDATE` في L0

---

## التوثيق — Documentation

| المستند | الوصف |
|---------|-------|
| `docs/00_MAQOOL_CONSTITUTION.md` | الدستور الجذري — السلطة العليا |
| `docs/01_L0_PHONETIC_BOUNDARY.md` | قوانين حدود L0 |
| `docs/01_EUCLIDEAN_PROOFS.md` | البراهين الإقليدية الأربعة |
| `docs/02_L1_META_LANGUAGE_BOUNDARY.md` | حدود L1 (معلّق) |
| `docs/03_L2_LOGICAL_BOUNDARY.md` | حدود L2 (مقفل) |
| `docs/04_L3_REALITY_BOUNDARY.md` | حدود L3 (مقفل) |
| `docs/14_PR_CHAIN_ROADMAP.md` | سلسلة PRs المرقّمة |
| `docs/15_PROJECT_ROADMAP.md` | خارطة الطريق الشاملة |
| `docs/16_STRATEGIC_METHODOLOGY.md` | المنهجية الاستراتيجية + KPIs |
| `docs/19_MORPHOLOGY_GENERATOR_THEOREM.md` | نظريات التوليد الصرفي |
| `docs/20_WAQF_WASL_BOUNDARY_THEOREM.md` | نظرية الوقف والوصل |

---

## الخطوة التالية

**PR-9: إعلان إغلاق L0 وفتح L1** — راجع `docs/15_PROJECT_ROADMAP.md`

---

*مشروع محكوم دستوريًا — لا تطوير بلا أصل*
