# القانون الأعلى للهوية الرقمية العربية
# Arabic Digital Identity Law (docs/59)

## المرجعية

```
docs/00_MAQOOL_CONSTITUTION.md §2 Category 2, §3 MCE-1, §5 Rule 8
```

---

## القانون الأعلى

> لا تمثيل رقميًا معتبرًا بلا إحالة.
> ولا إحالة رقمية بلا مجال.
> ولا مجال بلا حامل.
> ولا حامل بلا هوية.
> ولا هوية بلا جنس.

---

## المبدأ التأسيسي

> اليونيكود يشهد على الرسم، لا على الصوت وحده ولا على المعنى.
> والرسم يشهد على اللفظ، لا على المعنى وحده.
> واللفظ لا يدخل التركيب إلا بعد إغلاق المفرد.

---

## القوانين السبعة للحامل الرقمي

| # | القانون | الصيغة |
|---|---------|--------|
| 1 | الحرف يحفظ الهوية الصامتة | letter_id ثابت مهما تغيرت الحركة |
| 2 | الحركة مُشغّل لا حامل مستقل | haraka operates ON letter, never stands alone |
| 3 | الشدة تُضاعف وظيفيًا ولا تخلق هوية جديدة | shadda(letter) = same letter_id with gemination |
| 4 | السكون يُغلق ولا يمحو | sukun(letter) = closed letter, identity preserved |
| 5 | المد يُطيل الحركة ولا يستقل إلا بترخيص | madd extends vowel conditionally |
| 6 | التنوين حركة مع أثر نوني | tanwin = vowel + nunnation effect |
| 7 | كل انتقال يحتاج ترخيصًا ومانعًا وبقايا | transition_licensed iff conditions AND NOT preventer |

---

## سلسلة الانتقال المرخّصة

```
[Unicode Codepoint]
  ↓ ترخيص رقمي (UNICODE_TO_GLYPH)
[Glyph]
  ↓ ترخيص تصنيف (GLYPH_TO_LETTER / GLYPH_TO_MARK)
[Letter / Mark]
  ↓ ترخيص ربط (LETTER_HARAKA_LINK / LETTER_SUKUN_LINK / LETTER_SHADDA_LINK)
[Vocalized Unit]
  ↓ ترخيص مقطع (VOCALIZED_UNIT_TO_SYLLABLE)
[Syllable]
  ↓ ترخيص سلسلة (SYLLABLE_TO_LAFZ)
[Lafz]
  ↓ إغلاق مفرد (LAFZ_TO_MUFRAD)
[Mufrad: اسم / فعل / حرف / مبني / علم / منقول / دخيل]
```

---

## القاعدة الحاكمة لكل انتقال

```
IF
  carrier_exists
AND domain_declared
AND identity_preserved
AND operator_licensed
AND condition_holds
AND cause_exists
AND NOT preventer_active
THEN
  transition = LICENSED
ELSE
  transition = BLOCKED | DEFERRED | RESIDUAL
```

---

## مبدأ اقتصاد الطاقة (MCE)

> لا تخزّن في الطبقة إلا ما يلزم لإغلاقها وتمكين التالية.

```
MCE(layer_i → layer_i+1) = min Energy subject to:
  IdentityPreserved
  ∧ DomainDeclared
  ∧ TransitionLicensed
  ∧ PreventerAbsent
  ∧ ResidualsDeclared
  ∧ NextLayerEnabled
```

### ما تحتاجه كل طبقة (الحد الأدنى)

| الطبقة | الحقول المطلوبة |
|--------|----------------|
| Unicode | codepoint, script, class, residuals |
| Letter | letter_id, genus, identity, properties |
| Mark | mark_id, genus, function, preventers |
| Vocalized Unit | letter + mark + license |
| Syllable | pattern, nucleus, boundary |
| Lafz | syllable_chain, closure_status |
| Mufrad | path (اسم/فعل/حرف/مبني/علم/منقول/دخيل) |

---

## السجلات الثلاثة

### 1. LetterRegistry (سجل الحروف)

28 حرف عربي، كل حرف يحمل:
- `letter_id` — المعرّف الفريد
- `unicode_codepoint` — نقطة اليونيكود
- `glyph` — الرسم العربي
- `genus` — الجنس (صامت / حرف علة طويل / همزة / كرسي ألف)
- `essence` — الهوية المحفوظة
- `accepts_haraka` / `accepts_sukun` / `accepts_shadda` — القابليات
- `connects_right` / `connects_left` — الاتصال الكتابي
- `residuals` — البقايا

### 2. MarkRegistry (سجل العلامات)

10 علامات رئيسية:
- فتحة، ضمة، كسرة (حركات قصيرة)
- سكون (مُغلِق)
- شدة (مُضعِّف)
- فتحتان، ضمتان، كسرتان (تنوين)
- مدة، ألف خنجرية (مد)

### 3. TransitionRegistry (سجل الانتقالات)

9 قوانين انتقال مرخّصة:
1. `UNICODE_TO_GLYPH`
2. `GLYPH_TO_LETTER`
3. `GLYPH_TO_MARK`
4. `LETTER_HARAKA_LINK`
5. `LETTER_SUKUN_LINK`
6. `LETTER_SHADDA_LINK`
7. `VOCALIZED_UNIT_TO_SYLLABLE`
8. `SYLLABLE_TO_LAFZ`
9. `LAFZ_TO_MUFRAD`

---

## البقايا الرقمية (Digital Residuals)

| البقية | المثال | الأثر |
|--------|--------|-------|
| `unicode_only` | رمز بلا وظيفة محسومة | لا ينتقل للصوت |
| `orthographic_ambiguity` | ا، و، ي | مد؟ صامت؟ كرسي؟ |
| `missing_haraka` | كتب | فعل؟ اسم؟ مبني للمجهول؟ |
| `mark_conflict` | حركة + سكون بلا ترخيص | منع أو تعليق |
| `shadda_unresolved` | شدة بلا حركة ظاهرة | يحتاج سياقًا |
| `madd_uncertain` | واو/ياء بعد حركة غير مناسبة | بقايا مد |
| `hamza_seat_issue` | أ، إ، ؤ، ئ، ء | همزة أصل؟ كرسي؟ |
| `madd_or_consonant_ambiguity` | و، ي | حرف مد أم صامت؟ |
| `classification_may_require_context` | مفرد بلا سياق | يحتاج تركيبًا |

---

## التطبيق: مثال بَّ

```json
{
  "reference": {
    "unicode_sequence": ["U+0628", "U+0651", "U+064E"],
    "domain": "Arabic orthographic-vocalized"
  },
  "carrier": {
    "id": "BA",
    "genus": "consonantal_letter",
    "identity": "ba_identity_preserved"
  },
  "operators": [
    {"id": "SHADDA", "function": "gemination"},
    {"id": "FATHA", "function": "short_vowel_opening"}
  ],
  "transitions_applied": [
    "GLYPH_TO_LETTER → BA",
    "LETTER_SHADDA_LINK → geminated_unit",
    "LETTER_HARAKA_LINK → vocalized_unit"
  ],
  "output": {
    "unit": "بَّ",
    "deep_projection": "بْ + بَ",
    "identity_preserved": true,
    "rank": "licensed"
  }
}
```

---

## المرجع الدستوري

هذا القانون يرتبط بـ:
- `docs/00_MAQOOL_CONSTITUTION.md §2 Category 2` — تعريف الحروف والحركات
- `docs/00_MAQOOL_CONSTITUTION.md §3 MCE-1` — الأنماط الصوتية الثمانية
- `docs/00_MAQOOL_CONSTITUTION.md §4 MCE-2` — أنواع المقاطع الأربعة
- `docs/00_MAQOOL_CONSTITUTION.md §5 Rule 8` — مسلّمة عدم القفز
- `docs/01_L0_PHONETIC_BOUNDARY.md` — قوانين حدود الطبقة الصوتية
- `docs/58_SUPREME_TASAWWUR_REALITY_LAW.md` — قانون الإحالة الأعلى
