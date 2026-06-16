"""
Tests for Euclidean-style axiomatic proofs.
Origin: docs/00_MAQOOL_CONSTITUTION.md §5, §8, §9

Test groups:
    TestDefinitions      — 8 tests (7 definitions + freeze + traceability)
    TestPostulates       — 6 tests (P6–P10 + dependencies)
    TestTheorem1         — 6 tests (proof, 10 steps, identity transfer)
    TestTheorem2         — 4 tests (proof, cardinality argument)
    TestTheorem3         — 4 tests (proof, weight as barrier)
    TestTheorem4         — 5 tests (proof, TH3 dependency, corollaries)
    TestProofVerifier    — 6 tests (verify all, reject corrupted proofs)
    TestSystemIntegrity  — 7 tests (hash, sequencing, no-leap)

Total: 46 tests
"""
from __future__ import annotations

import pytest

from tests.conftest import ConstitutionalChainTestCase
from taaqqul_slot_geometry.constitution.euclidean_axioms import (
    ALL_DEFINITIONS,
    ALL_POSTULATES,
    ALL_THEOREMS,
    DEFINITION_ID,
    DEFINITION_LAYER,
    DEFINITION_M,
    DEFINITION_Q,
    DEFINITION_R,
    DEFINITION_S,
    DEFINITION_W,
    POSTULATE_P6,
    POSTULATE_P7,
    POSTULATE_P8,
    POSTULATE_P9,
    POSTULATE_P10,
    SYSTEM_HASH,
    THEOREM_1,
    THEOREM_2,
    THEOREM_3,
    THEOREM_4,
    DefinitionId,
    EuclideanDefinition,
    EuclideanPostulate,
    EuclideanTheorem,
    PostulateId,
    ProofStep,
    ProofVerificationError,
    ProofVerifier,
    TheoremId,
    compute_system_hash,
)


# ══════════════════════════════════════════════════════════════════════════════
# TestDefinitions — 8 tests
# ══════════════════════════════════════════════════════════════════════════════


class TestDefinitions(ConstitutionalChainTestCase):
    """Origin: docs/00_MAQOOL_CONSTITUTION.md §5 Rule 2, §8"""

    def test_seven_definitions_exist(self):
        """All 7 definitions are present."""
        assert len(ALL_DEFINITIONS) == 7

    def test_definition_m_intelligible(self):
        """Definition M (المعقول) is correctly structured."""
        assert DEFINITION_M.definition_id == DefinitionId.M
        assert DEFINITION_M.name_ar == "المعقول"
        assert "phonetic" in DEFINITION_M.formal_statement

    def test_definition_s_sound(self):
        """Definition S (الصوت) references 8 patterns."""
        assert DEFINITION_S.definition_id == DefinitionId.S
        assert "8 patterns" in DEFINITION_S.formal_statement

    def test_definition_w_weight(self):
        """Definition W (الوزن) declares no meaning production."""
        assert DEFINITION_W.definition_id == DefinitionId.W
        assert "meaning" in DEFINITION_W.formal_statement

    def test_all_definitions_frozen(self):
        """Rule 3: All definitions are frozen."""
        for defn in ALL_DEFINITIONS:
            with pytest.raises((AttributeError, TypeError)):
                defn.rank = "VERDICT"  # type: ignore[misc]

    def test_all_definitions_have_trace_ref(self):
        """Rule 2: Every definition carries trace_ref."""
        for defn in ALL_DEFINITIONS:
            assert defn.trace_ref, f"{defn.definition_id.value} missing trace_ref"

    def test_all_definitions_rank_candidate(self):
        """Rule 2: Every definition has rank == CANDIDATE."""
        for defn in ALL_DEFINITIONS:
            assert defn.rank == "CANDIDATE"

    def test_definition_rejects_empty_trace_ref(self):
        """Birth guard: empty trace_ref raises ValueError."""
        with pytest.raises(ValueError, match="missing_trace_ref"):
            EuclideanDefinition(
                definition_id=DefinitionId.M,
                name_ar="test",
                name_en="test",
                formal_statement="test",
                trace_ref="",
            )


# ══════════════════════════════════════════════════════════════════════════════
# TestPostulates — 6 tests
# ══════════════════════════════════════════════════════════════════════════════


class TestPostulates(ConstitutionalChainTestCase):
    """Origin: docs/00_MAQOOL_CONSTITUTION.md §8"""

    def test_five_postulates_exist(self):
        """P6–P10 are all present."""
        assert len(ALL_POSTULATES) == 5

    def test_p6_identity_preservation(self):
        """P6 declares identity preservation."""
        assert POSTULATE_P6.postulate_id == PostulateId.P6
        assert "Identity" in POSTULATE_P6.formal_statement

    def test_p8_depth(self):
        """P8 declares M is ontologically prior to S."""
        assert POSTULATE_P8.postulate_id == PostulateId.P8
        assert "definition.M" in POSTULATE_P8.dependencies

    def test_p10_no_leap(self):
        """P10 declares the no-leap axiom."""
        assert POSTULATE_P10.postulate_id == PostulateId.P10
        assert "definition.Q" in POSTULATE_P10.dependencies

    def test_all_postulates_have_dependencies(self):
        """Every postulate declares its dependencies."""
        for post in ALL_POSTULATES:
            assert len(post.dependencies) > 0

    def test_postulate_rejects_bad_rank(self):
        """Birth guard: rank != CANDIDATE raises ValueError."""
        with pytest.raises(ValueError, match="rank_promotion"):
            EuclideanPostulate(
                postulate_id=PostulateId.P6,
                name_ar="test",
                name_en="test",
                formal_statement="test",
                dependencies=("definition.ID",),
                trace_ref="test.ref",
                rank="VERDICT",
            )


# ══════════════════════════════════════════════════════════════════════════════
# TestTheorem1 — 6 tests
# ══════════════════════════════════════════════════════════════════════════════


class TestTheorem1(ConstitutionalChainTestCase):
    """Origin: docs/00_MAQOOL_CONSTITUTION.md §5 Rule 10"""

    def test_theorem_1_has_10_steps(self):
        """TH1 proof has exactly 10 steps."""
        assert len(THEOREM_1.proof_steps) == 10

    def test_theorem_1_steps_sequential(self):
        """TH1 steps are numbered 1..10 contiguously."""
        for i, step in enumerate(THEOREM_1.proof_steps, start=1):
            assert step.step_number == i

    def test_theorem_1_depends_on_p6_p8_p9(self):
        """TH1 depends on P6, P8, P9."""
        deps = set(THEOREM_1.dependencies)
        assert "postulate.P6" in deps
        assert "postulate.P8" in deps
        assert "postulate.P9" in deps

    def test_theorem_1_trace_ref(self):
        """TH1 has proper trace_ref."""
        assert THEOREM_1.trace_ref == "euclid.th1"

    def test_theorem_1_identity_transfer(self):
        """TH1 conclusion: meaning pre-exists in M."""
        last_step = THEOREM_1.proof_steps[-1]
        assert "meaning" in last_step.statement.lower()
        assert "M" in last_step.statement

    def test_theorem_1_all_steps_have_justification(self):
        """Every step in TH1 cites a justification."""
        for step in THEOREM_1.proof_steps:
            assert step.justification


# ══════════════════════════════════════════════════════════════════════════════
# TestTheorem2 — 4 tests
# ══════════════════════════════════════════════════════════════════════════════


class TestTheorem2(ConstitutionalChainTestCase):
    """Origin: docs/00_MAQOOL_CONSTITUTION.md §3 (MCE-1)"""

    def test_theorem_2_has_steps(self):
        """TH2 proof has steps."""
        assert len(THEOREM_2.proof_steps) == 6

    def test_theorem_2_cardinality_argument(self):
        """TH2 formal statement contains cardinality bound."""
        assert "896" in THEOREM_2.formal_statement or "finite" in THEOREM_2.formal_statement

    def test_theorem_2_depends_on_p8(self):
        """TH2 requires P8 (cardinality/depth postulate)."""
        assert "postulate.P8" in THEOREM_2.dependencies

    def test_theorem_2_depends_on_definition_s(self):
        """TH2 requires Definition S."""
        assert "definition.S" in THEOREM_2.dependencies


# ══════════════════════════════════════════════════════════════════════════════
# TestTheorem3 — 4 tests
# ══════════════════════════════════════════════════════════════════════════════


class TestTheorem3(ConstitutionalChainTestCase):
    """Origin: docs/00_MAQOOL_CONSTITUTION.md §5 Rule 10"""

    def test_theorem_3_has_steps(self):
        """TH3 has 7 proof steps."""
        assert len(THEOREM_3.proof_steps) == 7

    def test_theorem_3_weight_not_source(self):
        """TH3 conclusion references weight as barrier."""
        assert "barrier" in THEOREM_3.name_en.lower() or "barrier" in THEOREM_3.formal_statement.lower()

    def test_theorem_3_depends_on_definition_w(self):
        """TH3 requires Definition W (weight)."""
        assert "definition.W" in THEOREM_3.dependencies

    def test_theorem_3_depends_on_p9(self):
        """TH3 requires P9 (license postulate)."""
        assert "postulate.P9" in THEOREM_3.dependencies


# ══════════════════════════════════════════════════════════════════════════════
# TestTheorem4 — 5 tests
# ══════════════════════════════════════════════════════════════════════════════


class TestTheorem4(ConstitutionalChainTestCase):
    """Origin: docs/00_MAQOOL_CONSTITUTION.md §5 Rule 8"""

    def test_theorem_4_has_steps(self):
        """TH4 has 8 proof steps."""
        assert len(THEOREM_4.proof_steps) == 8

    def test_theorem_4_depends_on_th3(self):
        """TH4 depends on Theorem 3."""
        assert "theorem.TH3" in THEOREM_4.dependencies

    def test_theorem_4_depends_on_p10(self):
        """TH4 depends on P10 (no-leap postulate)."""
        assert "postulate.P10" in THEOREM_4.dependencies

    def test_theorem_4_conclusion_no_leap(self):
        """TH4 conclusion: leap is impossible."""
        assert "impossible" in THEOREM_4.name_en.lower() or "no exceptions" in THEOREM_4.formal_statement

    def test_theorem_4_corollary_chain(self):
        """TH4 last step declares the only valid chain."""
        last_step = THEOREM_4.proof_steps[-1]
        assert "chain" in last_step.statement.lower() or "path" in last_step.statement.lower()


# ══════════════════════════════════════════════════════════════════════════════
# TestProofVerifier — 6 tests
# ══════════════════════════════════════════════════════════════════════════════


class TestProofVerifier(ConstitutionalChainTestCase):
    """Origin: docs/00_MAQOOL_CONSTITUTION.md §5 Rules 4, 5"""

    def test_verify_all_theorems_pass(self):
        """All 4 theorems pass verification."""
        result = ProofVerifier.verify_all(ALL_THEOREMS)
        assert result == (True, True, True, True)

    def test_verify_theorem_1_pass(self):
        """TH1 passes individual verification."""
        assert ProofVerifier.verify_theorem_1(THEOREM_1) is True

    def test_reject_th1_wrong_steps(self):
        """TH1 with fewer than 10 steps is rejected."""
        bad_th = EuclideanTheorem(
            theorem_id=TheoremId.TH1,
            name_ar="test",
            name_en="test",
            formal_statement="test",
            proof_steps=(
                ProofStep(step_number=1, statement="s", justification="j", trace_ref="t"),
            ),
            dependencies=THEOREM_1.dependencies,
            trace_ref="test",
        )
        with pytest.raises(ProofVerificationError) as exc_info:
            ProofVerifier.verify_theorem_1(bad_th)
        assert "10_steps" in exc_info.value.reason

    def test_reject_th2_missing_p8(self):
        """TH2 without P8 is rejected (missing cardinality postulate)."""
        bad_th = EuclideanTheorem(
            theorem_id=TheoremId.TH2,
            name_ar="test",
            name_en="test",
            formal_statement="test",
            proof_steps=(
                ProofStep(step_number=1, statement="s", justification="j", trace_ref="t"),
            ),
            dependencies=("definition.S",),
            trace_ref="test",
        )
        with pytest.raises(ProofVerificationError) as exc_info:
            ProofVerifier.verify_theorem_2(bad_th)
        assert "missing_cardinality_postulate" in exc_info.value.reason

    def test_reject_th3_missing_weight(self):
        """TH3 without Definition.W is rejected."""
        bad_th = EuclideanTheorem(
            theorem_id=TheoremId.TH3,
            name_ar="test",
            name_en="test",
            formal_statement="test",
            proof_steps=(
                ProofStep(step_number=1, statement="s", justification="j", trace_ref="t"),
            ),
            dependencies=("postulate.P9",),
            trace_ref="test",
        )
        with pytest.raises(ProofVerificationError) as exc_info:
            ProofVerifier.verify_theorem_3(bad_th)
        assert "missing_weight_definition" in exc_info.value.reason

    def test_reject_th4_missing_th3(self):
        """TH4 without TH3 dependency is rejected."""
        bad_th = EuclideanTheorem(
            theorem_id=TheoremId.TH4,
            name_ar="test",
            name_en="test",
            formal_statement="test",
            proof_steps=(
                ProofStep(step_number=1, statement="s", justification="j", trace_ref="t"),
            ),
            dependencies=("postulate.P10",),
            trace_ref="test",
        )
        with pytest.raises(ProofVerificationError) as exc_info:
            ProofVerifier.verify_theorem_4(bad_th)
        assert "missing_theorem_3_dependency" in exc_info.value.reason


# ══════════════════════════════════════════════════════════════════════════════
# TestSystemIntegrity — 7 tests
# ══════════════════════════════════════════════════════════════════════════════


class TestSystemIntegrity(ConstitutionalChainTestCase):
    """Origin: docs/00_MAQOOL_CONSTITUTION.md §5"""

    def test_system_hash_stable(self):
        """System hash is deterministic."""
        assert compute_system_hash() == SYSTEM_HASH

    def test_system_hash_length(self):
        """System hash is 16 hex characters."""
        assert len(SYSTEM_HASH) == 16
        assert all(c in "0123456789abcdef" for c in SYSTEM_HASH)

    def test_definitions_all_unique_ids(self):
        """All definition IDs are unique."""
        ids = [d.definition_id for d in ALL_DEFINITIONS]
        assert len(ids) == len(set(ids))

    def test_postulates_all_unique_ids(self):
        """All postulate IDs are unique."""
        ids = [p.postulate_id for p in ALL_POSTULATES]
        assert len(ids) == len(set(ids))

    def test_theorems_all_unique_ids(self):
        """All theorem IDs are unique."""
        ids = [t.theorem_id for t in ALL_THEOREMS]
        assert len(ids) == len(set(ids))

    def test_no_theorem_skips_dependency_chain(self):
        """TH4 depends on TH3, not directly on TH1 or TH2 (no leap in proof chain)."""
        assert "theorem.TH3" in THEOREM_4.dependencies
        # TH4 should not directly depend on TH1 or TH2
        assert "theorem.TH1" not in THEOREM_4.dependencies
        assert "theorem.TH2" not in THEOREM_4.dependencies

    def test_proof_verifier_is_frozen(self):
        """ProofVerifier itself is frozen."""
        pv = ProofVerifier()
        with pytest.raises((AttributeError, TypeError)):
            pv.rank = "VERDICT"  # type: ignore[misc]
