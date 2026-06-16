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

## Phase 0 — L0 Closure ✅ CURRENT

**Goal**: Implement and test all L0 entities. Close L0 boundary.

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

## Phase 1 — L1 Closure ⏳ PENDING

**Blocked by**: Phase 0 (L0 must be fully closed).

**Goal**: Implement formal definitions, postulates, common notions, and L0→L1 bridges.

### Deliverables (not yet implemented)
- [ ] `src/taaqqul_slot_geometry/L1/definition.py`
- [ ] `src/taaqqul_slot_geometry/L1/postulate.py`
- [ ] `src/taaqqul_slot_geometry/L1/common_notion.py`
- [ ] `src/taaqqul_slot_geometry/L1/meta_bridge.py`
- [ ] All L1 tests passing

---

## Phase 2 — L2 Closure 🔒 LOCKED

**Blocked by**: Phase 1 (L1 must be fully closed).

**Goal**: Implement qiyas engine, proof engine, and L1→L2 bridges.

### Deliverables (not yet implemented)
- [ ] `src/taaqqul_slot_geometry/L2/qiyas.py`
- [ ] `src/taaqqul_slot_geometry/L2/proof.py`
- [ ] `src/taaqqul_slot_geometry/L2/closure.py`
- [ ] `src/taaqqul_slot_geometry/L2/meta_bridge.py`
- [ ] All L2 tests passing

---

## Phase 3 — L3 Closure 🔒 LOCKED

**Blocked by**: Phase 2 (L2 must be fully closed).

**Goal**: Implement evidence types, manat verification, hukm candidates, and L2→L3 bridges.

### Deliverables (not yet implemented)
- [ ] `src/taaqqul_slot_geometry/L3/evidence.py`
- [ ] `src/taaqqul_slot_geometry/L3/manat.py`
- [ ] `src/taaqqul_slot_geometry/L3/hukm.py`
- [ ] `src/taaqqul_slot_geometry/L3/tanzil.py`
- [ ] `src/taaqqul_slot_geometry/L3/meta_bridge.py`
- [ ] All L3 tests passing

---

*End of PR Chain Roadmap*
