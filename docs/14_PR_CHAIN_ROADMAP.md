# PR Chain Roadmap — `docs/14_PR_CHAIN_ROADMAP.md`

## Authority
`docs/00_MAQOOL_CONSTITUTION.md §5 Rule 1` (Layered Implementation Order).

## See Also
**`docs/15_PROJECT_ROADMAP.md`** — خارطة الطريق الشاملة بالأهداف والمدخلات والمخرجات لكل مرحلة.

## Status Legend
- ✅ CURRENT — actively being implemented in this PR chain
- ⏳ PENDING — blocked until previous phase is fully closed
- 🔒 LOCKED — may not be opened until all prior phases are closed

---

## Phase 0 — L0 Closure ✅ COMPLETE

**Goal**: Implement and test all L0 entities — the foundational building blocks for analyzing GPT answer structure.

**Closure**: Formally closed via `docs/L0_CLOSURE_DECLARATION.md`.

### Deliverables
- [x] `src/taaqqul_slot_geometry/constitution/failure_taxonomy.py`
- [x] `src/taaqqul_slot_geometry/constitution/identity_preservation.py`
- [x] `src/taaqqul_slot_geometry/constitution/transition_gate.py`
- [x] `src/taaqqul_slot_geometry/constitution/maqool_constitution.py`
- [x] `src/taaqqul_slot_geometry/core/slot_graph.py`
- [x] `src/taaqqul_slot_geometry/core/rank.py`
- [x] `src/taaqqul_slot_geometry/core/residual.py`
- [x] `src/taaqqul_slot_geometry/core/trace.py`
- [x] `src/taaqqul_slot_geometry/L0/phoneme.py`
- [x] `src/taaqqul_slot_geometry/L0/grapheme.py`
- [x] `src/taaqqul_slot_geometry/L0/vowel.py`
- [x] `src/taaqqul_slot_geometry/L0/syllable.py`
- [x] `src/taaqqul_slot_geometry/L0/utterance.py`
- [x] `src/taaqqul_slot_geometry/L0/signifier.py`
- [x] `src/taaqqul_slot_geometry/L0/signified.py`
- [x] `src/taaqqul_slot_geometry/L0/union.py`
- [x] `src/taaqqul_slot_geometry/L0/signification.py`
- [x] `src/taaqqul_slot_geometry/L0/jamid.py`
- [x] `src/taaqqul_slot_geometry/L0/harf_maani.py`
- [x] `src/taaqqul_slot_geometry/L0/weight.py`
- [x] All L0 tests passing

---

## Phase 1 — L1 Closure ✅ COMPLETE

**Unblocked by**: L0 formal closure (`docs/L0_CLOSURE_DECLARATION.md`).

**Goal**: Build formal definitions, postulates, and common notions that serve as **reasonableness criteria** — the reference standards against which GPT answers are measured.

### Deliverables (reconciled to implemented PR chain)
- [x] `src/taaqqul_slot_geometry/L1/definition.py` (PR-10..PR-12 baseline)
- [x] `src/taaqqul_slot_geometry/L1/postulate.py` (PR-10..PR-12 baseline)
- [x] `src/taaqqul_slot_geometry/L1/common_notion.py` (PR-10..PR-12 baseline)
- [x] `src/taaqqul_slot_geometry/L1/proof_objects.py` (PR-33)
- [x] `src/taaqqul_slot_geometry/L1/domain_ids.py` + `domain_bridge_gate.py` (PR-34)
- [x] `src/taaqqul_slot_geometry/L1/dal_atomic.py` (PR-35)
- [x] `src/taaqqul_slot_geometry/L1/lafzi_form.py` (PR-36)
- [x] `src/taaqqul_slot_geometry/L1/dal_to_lafzi_bridge.py` (PR-37)
- [x] Runtime embargo + failure-alignment guardrails (PR-38)
- [x] Closure/conflict kernel contracts + hotfix through PR-43
- [x] `docs/L1_CLOSURE_DECLARATION.md` with required verification evidence
- [x] All L1 and repository tests passing at closure time

> Note: Early PR-chain placeholders in this file were superseded by the realized L1 expansion (PR-33..PR-43); this section reflects the implemented sequence.

---

## Phase 2 — L2 Closure 🔒 LOCKED

**Blocked by**: Phase 1 (L1 must be fully closed).

**Goal**: Build a **comparison and qiyas engine** that takes a GPT answer (decomposed via L0, defined via L1) and compares it against the reference criteria — testing whether the unifying cause exists, whether the effective description is correct, and whether there is a disqualifying difference.

### Deliverables (not yet implemented)
- [ ] `src/taaqqul_slot_geometry/L2/qiyas.py`
- [ ] `src/taaqqul_slot_geometry/L2/proof.py`
- [ ] `src/taaqqul_slot_geometry/L2/closure.py`
- [ ] `src/taaqqul_slot_geometry/L2/meta_bridge.py`
- [ ] All L2 tests passing

---

## Phase 3 — L3 Closure 🔒 LOCKED

**Blocked by**: Phase 2 (L2 must be fully closed).

**Goal**: Issue the **final reasonableness verdict** on GPT answers:
- `MAQOOL` (reasonable): All transitions licensed, no barrier, correct cause
- `GHAYR_MAQOOL` (unreasonable): Barrier exists, disqualifying difference, or incorrect cause
- `MU'ALLAQ` (suspended): Insufficient evidence to decide

### Deliverables (not yet implemented)
- [ ] `src/taaqqul_slot_geometry/L3/evidence.py`
- [ ] `src/taaqqul_slot_geometry/L3/manat.py`
- [ ] `src/taaqqul_slot_geometry/L3/hukm.py`
- [ ] `src/taaqqul_slot_geometry/L3/tanzil.py`
- [ ] `src/taaqqul_slot_geometry/L3/meta_bridge.py`
- [ ] All L3 tests passing

---

*End of PR Chain Roadmap*
