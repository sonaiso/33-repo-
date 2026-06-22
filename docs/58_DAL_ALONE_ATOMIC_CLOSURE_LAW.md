# DAL-A0 Alone Atomic Closure Law

## Authority

Derived from `docs/00_MAQOOL_CONSTITUTION.md §5` and
`docs/15_PROJECT_ROADMAP.md §حوكمة التفريع`.

Branch license: DAL-A0 is a law-only branch under D1_DAL_ONLY. It exists to
lock the dal-alone surface before any `LafziMadlulGate`.

## DAL-A0 Status

`DAL-A0 = Ratified`

This document is law-only:

- no runtime
- no carriers implementation
- no enums
- no operations
- no adapter
- no audit execution
- no global `FailureCode` expansion

## Governing Sequence

```text
DalOnlyCandidate
→ DalAloneAtomicClosure
→ DalAloneClosed
→ LafziMadlulGate
```

`DalAloneClosed` opens the gate only; it does not cross the gate.

## Non-Domain

`DalAloneClosed != Meaning`

`DalAloneClosed != WordKind`

`DalAloneClosed != Root/Pattern`

Forbidden outputs:

- `WordKind`
- `Root`
- `Pattern`
- `LicensedWeight`
- `LexicalMeaning`
- `VerbalMadlulCandidate`
- `IfadahCandidate`
- `HukmCandidate`
- `TanzilCandidate`
- `Reality`
- `LafziMadlul`

## Atomic Gate Names

The following names are legal names only in DAL-A0; they are not executable
gates in this phase:

- `RawAcousticTraceGate`
- `UnicodeNormalizationGate`
- `SoundLetterGraphemeSeparationGate`
- `ArabicSoundInventoryGate`
- `MakhrajSifahMatrixGate`
- `QadihSoundDifferenceGate`
- `HarakaCarrierGate`
- `MaddExtensionGate`
- `HamzaResolutionGate`
- `ShaddaIdghamGate`
- `TanwinTraceGate`
- `SukunCollisionGate`
- `SyllableLicenseGate`
- `InitialSukunGate`
- `HamzatWaslGate`
- `SoundTransitionMatrixGate`
- `AdjacencyToSequenceGate`
- `AtomicSoundCountingGate`
- `S1_S5LicenseGate`
- `WaqfLicenseGate`
- `WaslLicenseGate`
- `UsageBeforeMeaningGate`
- `LoanArabizedGate`
- `DeletionTraceGate`
- `DalResidualAuditGate`

## Local Residual Vocabulary

These residual names are local to dal-alone closure and must not expand the
global `FailureCode` taxonomy:

- `RAW_TRACE_NOT_SPEECH`
- `MAKHRAJ_MISSING`
- `SIFAH_MISSING`
- `QADIH_SOUND_DIFF_MISSING`
- `HARAKA_WITHOUT_CARRIER`
- `MADD_WITHOUT_EXTENSION`
- `SHADDA_UNEXPANDED`
- `HAMZA_UNRESOLVED`
- `SUKUN_COLLISION`
- `SYLLABLE_UNLICENSED`
- `WAQF_UNTESTED`
- `WASL_UNTESTED`
- `UNVOCALIZED_SURFACE`
- `UNUSED_LAFZ`
- `LOAN_PATH_REQUIRED`
- `DELETION_UNLICENSED`
- `ENERGY_COLLISION`

## §12 DalAloneClosed Closure Conditions

`DalAloneClosed` requires all of the following:

1. raw trace / graphic trace / sound trace are separated.
2. every Arabic sound has makhraj and sifah.
3. qādih sound difference is visible when confusion is possible.
4. every haraka has a carrier.
5. every madd has an extension.
6. shadda expands or blocks closure.
7. hamza resolves or blocks closure.
8. sukun collision is licensed or blocks closure.
9. syllable is licensed.
10. graphic adjacency becomes sound sequence.
11. S1-S5 counting states origin, branch, cause, condition, barrier,
    preserved effect, and new addition.
12. waqf and wasl are tested.
13. unvocalized text remains a candidate set.
14. usage / unused / loan status is visible before `LafziMadlulGate`.
15. deletion and estimation have trace and license.
16. all residuals are visible.
17. no crossing to word kind, meaning, syntax, ifadah, hukm, or reality.

## Remaining Runtime Path

```text
DAL-A0 law-only
→ DAL-A1 carriers + local residual vocabulary only
→ DAL-A2 raw trace / grapheme / letter / sound separation gates
→ DAL-A3 ArabicSoundInventory + makhraj/sifah/qādih matrix
→ DAL-A4 hamza / shadda / tanwin / sukun / madd gates
→ DAL-A5 syllable / transition / adjacency / S1-S5 gates
→ DAL-A6 detailed waqf / wasl closure
→ DAL-A7 usage / loan / unvocalized / deletion residual gates
→ DAL-A8 final DalAloneClosed → LafziMadlulGate integration
```

## DAL-A1 Scope

DAL-A1 is limited to carriers and local residual vocabulary only:

- no gate execution
- no `DalAloneClosed`
- no `LafziMadlulGate`
- no `WordKind`
- no meaning
- no root
- no pattern
- no weight
- no ifadah
- no hukm
- no reality

DAL-A1 may define only:

- `RawTrace`
- `GraphemeCandidate`
- `DalLetterIdentityCarrier`
- `PhoneticRealization`
- `AtomicSoundUnit`
- `DalResidual`
- `DalAloneClosureSurface`

`DalAloneClosureSurface` is a candidate surface, not `DalAloneClosed`.

## DAL-A2 Scope

DAL-A2 is limited to raw trace / grapheme / letter / sound separation gates:

- `RawTraceSeparationGate`
- `UnicodeNormalizationGate`
- `SoundLetterGraphemeSeparationGate`
- `DalA2SeparationSurface`

DAL-A2 is separation-only:

- no `DalAloneClosed`
- no `LafziMadlulGate`
- no `WordKind`
- no meaning
- no root
- no pattern
- no weight licensing
- no ifadah
- no hukm
- no reality

DAL-A2 prepares DAL-A3 but does not perform:

- `ArabicSoundInventory`
- `Makhraj`
- `Sifah`
- `QadihSoundDifference`

`DalA2SeparationSurface` is a candidate separation surface, not a closure
verdict and not a bridge to `LafziMadlul`.
