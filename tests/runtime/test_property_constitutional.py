"""
Property-based constitutional tests — prove that the constitution holds for all valid inputs.

Every test class inherits ConstitutionalPropertyTest and declares constitutional origin.

Origin: docs/00_MAQOOL_CONSTITUTION.md (all sections)
"""
from __future__ import annotations

import pytest

from taaqqul_slot_geometry.constitution.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.L0.phoneme import PhoneticPattern
from taaqqul_slot_geometry.L0.weight import WeightPattern
from taaqqul_slot_geometry.runtime.constitutional_engine import (
    ConstitutionalEngine,
    ConstitutionalRuntimeError,
    JamidUnit,
    TraceStep,
)


class ConstitutionalPropertyTest:
    """Base class for constitutional property tests.

    Every subclass MUST declare constitutional origin.
    """

    origin_pr: str = "PR#2.5"
    origin_theorem: str = ""
    origin_postulate: str = ""


# All valid inputs for parametrized tests
VALID_CONSONANTS = ["k", "b", "t", "s", "n", "q", "f", "d", "r", "l", "m"]
# Note: sukun excluded from full-pipeline vowels because C_SUKUN alone cannot form
# a syllable (MCE-2: only CV, CVV, CVC, CVCC are valid; bare sukun needs CVC context)
VALID_VOWELS_EN = ["fatha", "damma", "kasra", "alif_madd", "waw_madd", "ya_madd"]
VALID_WEIGHTS_EN = ["faala", "faal", "fiaal", "fual", "faalil", "mafuul", "tafaala", "istafala", "root"]
VALID_ROOTS = [
    ("k", "t", "b"),
    ("n", "s", "r"),
    ("s", "l", "m"),
    ("q", "t", "l"),
    ("f", "t", "h"),
]


# ═══════════════════════════════════════════════════════════════════════════════
# Property 1: Weight Never Produces Meaning Alone
# ═══════════════════════════════════════════════════════════════════════════════


class TestWeightNeverProducesMeaning(ConstitutionalPropertyTest):
    """Weight pattern alone does not produce meaning — it requires a full pipeline.

    Origin: docs/00_MAQOOL_CONSTITUTION.md §5 Rule 10 (M_02_19)
    """

    origin_pr = "PR#2.5"
    origin_theorem = "TH6"
    origin_postulate = "P10"

    @pytest.mark.parametrize("weight", VALID_WEIGHTS_EN)
    def test_weight_requires_full_pipeline(self, weight: str) -> None:
        """Every weight pattern needs consonant+vowel to produce output.
        Origin: §5 Rule 10."""
        engine = ConstitutionalEngine()
        # Weight alone cannot produce a JamidUnit — it requires the pipeline
        jamid, trace = engine.full_pipeline(
            consonant="k", vowel="fatha",
            weight_pattern=weight, root_letters=("k", "t", "b"),
        )
        # The output is always CANDIDATE (never promoted)
        assert jamid.status == "CANDIDATE"
        # Identity was preserved through all steps
        assert ConstitutionalEngine.verify_identity_preserved(trace)


# ═══════════════════════════════════════════════════════════════════════════════
# Property 2: No Leap Within Pipeline
# ═══════════════════════════════════════════════════════════════════════════════


class TestNoLeapProperty(ConstitutionalPropertyTest):
    """No step in the pipeline may be skipped (No-Leap Axiom).

    Origin: docs/00_MAQOOL_CONSTITUTION.md §5 Rule 8 (M_CX_02)
    """

    origin_pr = "PR#2.5"
    origin_theorem = "TH7"
    origin_postulate = "P8"

    @pytest.mark.parametrize("consonant", VALID_CONSONANTS)
    def test_all_consonants_produce_sequential_trace(self, consonant: str) -> None:
        """For every valid consonant, the trace is sequential.
        Origin: §5 Rule 8."""
        engine = ConstitutionalEngine()
        _, trace = engine.full_pipeline(
            consonant=consonant, vowel="fatha",
            weight_pattern="faala", root_letters=("k", "t", "b"),
        )
        assert ConstitutionalEngine.verify_no_leap(trace)
        assert [s.step_number for s in trace] == [1, 2, 3, 4, 5]


# ═══════════════════════════════════════════════════════════════════════════════
# Property 3: Identity Preservation Across All Steps
# ═══════════════════════════════════════════════════════════════════════════════


class TestIdentityPreservationProperty(ConstitutionalPropertyTest):
    """Identity(source) ⊆ Identity(target) for all pipeline executions.

    Origin: docs/00_MAQOOL_CONSTITUTION.md §5 Rule 7 (M_CX_01)
    """

    origin_pr = "PR#2.5"
    origin_theorem = "TH8"
    origin_postulate = "P7"

    @pytest.mark.parametrize("vowel", VALID_VOWELS_EN)
    def test_all_vowels_preserve_identity(self, vowel: str) -> None:
        """For every valid vowel, identity is preserved.
        Origin: §5 Rule 7."""
        engine = ConstitutionalEngine()
        _, trace = engine.full_pipeline(
            consonant="k", vowel=vowel,
            weight_pattern="faala", root_letters=("k", "t", "b"),
        )
        assert ConstitutionalEngine.verify_identity_preserved(trace)


# ═══════════════════════════════════════════════════════════════════════════════
# Property 4: Rank Never Exceeds CANDIDATE in L0
# ═══════════════════════════════════════════════════════════════════════════════


class TestRankCeilingProperty(ConstitutionalPropertyTest):
    """Rank is always CANDIDATE — never promoted in L0.

    Origin: docs/00_MAQOOL_CONSTITUTION.md §5 Rule 2 (M_CX_09)
    """

    origin_pr = "PR#2.5"
    origin_theorem = "TH9"
    origin_postulate = "P2"

    @pytest.mark.parametrize("root", VALID_ROOTS)
    def test_all_roots_produce_candidate_rank(self, root: tuple) -> None:
        """For every valid root, output rank is CANDIDATE.
        Origin: §5 Rule 2."""
        engine = ConstitutionalEngine()
        jamid, _ = engine.full_pipeline(
            consonant="k", vowel="fatha",
            weight_pattern="faala", root_letters=root,
        )
        assert jamid.rank == "CANDIDATE"
        assert jamid.status == "CANDIDATE"


# ═══════════════════════════════════════════════════════════════════════════════
# Property 5: Trace Ref Always Present
# ═══════════════════════════════════════════════════════════════════════════════


class TestTraceRefProperty(ConstitutionalPropertyTest):
    """Every output entity has a non-empty trace_ref.

    Origin: docs/00_MAQOOL_CONSTITUTION.md §5 Rule 2 (M_00_11)
    """

    origin_pr = "PR#2.5"
    origin_theorem = "TH10"
    origin_postulate = "P2"

    @pytest.mark.parametrize("consonant", VALID_CONSONANTS)
    def test_all_outputs_have_trace_ref(self, consonant: str) -> None:
        """Every JamidUnit produced has trace_ref.
        Origin: §5 Rule 2."""
        engine = ConstitutionalEngine()
        jamid, trace = engine.full_pipeline(
            consonant=consonant, vowel="fatha",
            weight_pattern="faala", root_letters=("k", "t", "b"),
        )
        assert jamid.trace_ref
        assert jamid.phoneme.trace_ref
        assert jamid.signifier.trace_ref
        for step in trace:
            assert step.trace_ref
            assert step.constitutional_ref


# ═══════════════════════════════════════════════════════════════════════════════
# Property 6: Frozen Immutability
# ═══════════════════════════════════════════════════════════════════════════════


class TestFrozenProperty(ConstitutionalPropertyTest):
    """All output entities are frozen (Rule 3).

    Origin: docs/00_MAQOOL_CONSTITUTION.md §5 Rule 3 (M_CX_06)
    """

    origin_pr = "PR#2.5"
    origin_theorem = "TH11"
    origin_postulate = "P3"

    @pytest.mark.parametrize("vowel", VALID_VOWELS_EN)
    def test_jamid_is_immutable_for_all_vowels(self, vowel: str) -> None:
        """JamidUnit cannot be mutated for any valid vowel.
        Origin: §5 Rule 3."""
        engine = ConstitutionalEngine()
        jamid, _ = engine.full_pipeline(
            consonant="k", vowel=vowel,
            weight_pattern="faala", root_letters=("k", "t", "b"),
        )
        with pytest.raises(Exception):
            jamid.status = "PROMOTED"  # type: ignore[misc]


# ═══════════════════════════════════════════════════════════════════════════════
# Property 7: Named Failures — Never Silent
# ═══════════════════════════════════════════════════════════════════════════════


class TestNamedFailureProperty(ConstitutionalPropertyTest):
    """Every rejection is named with a FailureCode (Rule 5).

    Origin: docs/00_MAQOOL_CONSTITUTION.md §5 Rule 5 (M_CX_08)
    """

    origin_pr = "PR#2.5"
    origin_theorem = "TH12"
    origin_postulate = "P5"

    @pytest.mark.parametrize("invalid_vowel", [
        "xyz", "123", "", "notavowel", "FATHA",
    ])
    def test_invalid_vowels_produce_named_failure(self, invalid_vowel: str) -> None:
        """Invalid vowels always produce M_00_02.
        Origin: §5 Rule 5."""
        engine = ConstitutionalEngine()
        # Empty consonant with empty vowel produces M_00_14 (consonant checked first)
        if invalid_vowel == "":
            # empty vowel still triggers consonant check first if consonant is valid
            with pytest.raises(ConstitutionalRuntimeError) as exc_info:
                engine.step1_phoneme("k", invalid_vowel)
            assert exc_info.value.failure_code == FailureCode.M_00_02
        else:
            with pytest.raises(ConstitutionalRuntimeError) as exc_info:
                engine.step1_phoneme("k", invalid_vowel)
            assert exc_info.value.failure_code == FailureCode.M_00_02


# ═══════════════════════════════════════════════════════════════════════════════
# Property 8: Pipeline Produces Consistent Phoneme
# ═══════════════════════════════════════════════════════════════════════════════


class TestPipelineConsistency(ConstitutionalPropertyTest):
    """The phoneme in JamidUnit matches the original input.

    Origin: docs/00_MAQOOL_CONSTITUTION.md §3 MCE-1
    """

    origin_pr = "PR#2.5"
    origin_theorem = "TH13"
    origin_postulate = "P7"

    @pytest.mark.parametrize("consonant,vowel,expected_pattern", [
        ("k", "fatha", PhoneticPattern.C_FATHA),
        ("b", "damma", PhoneticPattern.C_DAMMA),
        ("s", "kasra", PhoneticPattern.C_KASRA),
        ("n", "alif_madd", PhoneticPattern.C_FATHA_MADD),
        ("q", "waw_madd", PhoneticPattern.C_DAMMA_MADD),
        ("f", "ya_madd", PhoneticPattern.C_KASRA_MADD),
    ])
    def test_phoneme_matches_input(
        self, consonant: str, vowel: str, expected_pattern: PhoneticPattern
    ) -> None:
        """JamidUnit.phoneme reflects the original input.
        Origin: §3 MCE-1."""
        engine = ConstitutionalEngine()
        jamid, _ = engine.full_pipeline(
            consonant=consonant, vowel=vowel,
            weight_pattern="faala", root_letters=("k", "t", "b"),
        )
        assert jamid.phoneme.consonant == consonant
        assert jamid.phoneme.pattern == expected_pattern


# ═══════════════════════════════════════════════════════════════════════════════
# Property 9: All Weight Patterns Are Accepted
# ═══════════════════════════════════════════════════════════════════════════════


class TestAllWeightsAccepted(ConstitutionalPropertyTest):
    """Every valid WeightPattern produces a successful pipeline.

    Origin: docs/00_MAQOOL_CONSTITUTION.md §5 Rule 10
    """

    origin_pr = "PR#2.5"
    origin_theorem = "TH14"
    origin_postulate = "P10"

    @pytest.mark.parametrize("weight", VALID_WEIGHTS_EN)
    def test_weight_accepted(self, weight: str) -> None:
        """Every weight pattern name is accepted by the pipeline.
        Origin: §5 Rule 10."""
        engine = ConstitutionalEngine()
        jamid, trace = engine.full_pipeline(
            consonant="k", vowel="fatha",
            weight_pattern=weight, root_letters=("k", "t", "b"),
        )
        assert jamid.status == "CANDIDATE"
        assert len(trace) == 5


# ═══════════════════════════════════════════════════════════════════════════════
# Property 10: Cross-Validation with Existing L0 Entities
# ═══════════════════════════════════════════════════════════════════════════════


class TestCrossValidation(ConstitutionalPropertyTest):
    """Pipeline output is compatible with existing L0 entity constraints.

    Origin: docs/00_MAQOOL_CONSTITUTION.md §2, §3, §4
    """

    origin_pr = "PR#2.5"
    origin_theorem = "TH15"
    origin_postulate = "P1"

    @pytest.mark.parametrize("consonant,vowel", [
        ("k", "fatha"),
        ("b", "damma"),
        ("s", "kasra"),
    ])
    def test_signifier_has_valid_utterance(
        self, consonant: str, vowel: str
    ) -> None:
        """The Signifier in JamidUnit contains a valid Utterance.
        Origin: §2 Category 2."""
        engine = ConstitutionalEngine()
        jamid, _ = engine.full_pipeline(
            consonant=consonant, vowel=vowel,
            weight_pattern="faala", root_letters=("k", "t", "b"),
        )
        assert jamid.signifier.utterance is not None
        assert jamid.signifier.utterance.syllable_count >= 1
        assert jamid.signifier.utterance.syllables[0].phonemes[0].consonant == consonant
