# Path Card Licensed Derivation Law — `docs/60`

## Authority
- `docs/00_MAQOOL_CONSTITUTION.md` §5 (trace, identity, residual visibility, rank discipline)
- `docs/00A_CONSTITUTIONAL_PROGRAMMING_AMENDMENT.md` (contract-first constitutional programming)
- `docs/12_RUNTIME_EMBARGO_CONSTITUTION.md` (audit-only posture under runtime embargo)
- `docs/15_PROJECT_ROADMAP.md` (L1 contract/audit bounded work)

## Scope
This law defines an audit-only contract for lexical derivation licensing from `PathCard`.
It standardizes when a lexical item may open a derivational path and when it must remain closed or residual.

## Non-scope
This law does not authorize runtime adjudication, decision authority, reality judgment, or rank promotion.
It does not open L2 or L3 and does not replace `FailureCode`.

---

## Constitutional declaration

> لا اشتقاق قبل بطاقة المسار.

> الاشتقاق لا يبدأ من الوزن السطحي وحده، بل من الحمولة الأثرية المرخّصة داخل بطاقة المسار.

---

## Core law

### 1) Surface is not license
`SurfaceWeight(x)` alone is never sufficient for derivation licensing.

`SurfaceWeight(x) ⇏ DerivationLicense(x)`

### 2) PathCard precedes derivation
A lexical item is evaluated through:

`PathCard(x) = <SurfaceWeight, RootIdentity, ZiyadahLicense, SlotLicense, Evidence, Function, EventLoad, EntityLoad, Residuals, Rank>`

### 3) Path type governs the gate
`PathType(x) ∈ {MasdarOpen, JamidClosed, MushtaqOpen, MabniOperator, DenominalBranch, AmbiguousResidual}`

### 4) Verb gate condition
`VerbGate(x) ⇔ MasdarOpen(x) ∨ DenominalBranchLicensed(x)`

If `JamidClosed(x) ∧ ¬DenominalBranchLicensed(x)`, then `¬VerbGate(x)`.

---

## Operational constitutional clauses

1. **Masdar clause**
   - If `EventLoad` is licensed with trace/evidence/identity preservation and no blocking residual, the path is `MasdarOpen`.
   - `MasdarOpen` may open a `VerbCandidate` as a morphological candidate only.

2. **Jamid clause**
   - If `EntityLoad` is closed and no original event load exists, the path is `JamidClosed`.
   - `JamidClosed` remains nominal in the origin path and does not open original verb generation.

3. **Denominal branch clause**
   - Verb emergence from a jamid origin is valid only through `DenominalBranch` with explicit branch license, branch card, reverse trace, and branch residual visibility.
   - لا فرع يرث رتبة أصله.

4. **Ambiguity clause**
   - If evidence/identity/trace conditions are incomplete, the item remains `AmbiguousResidual`.
   - Residual state is visible and non-silent.

5. **Ziyadah clause**
   - Ziyadah is a licensed slot condition, not an automatic derivation generator.

---

## Constitutional invariants preserved
- `rank = "CANDIDATE"` remains mandatory.
- Rejections remain named and explicit.
- No Boolean-as-proof substitution.
- No manual computed verdict authority.
- Runtime embargo remains active; this law is audit-only.
