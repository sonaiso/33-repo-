"""
End-to-end integration tests for the Constitutional Runtime Engine.

Every test class inherits ConstitutionalRuntimeTest and declares:
  - origin_pr: The PR that introduced the tested code
  - origin_theorem: The theorem it validates
  - origin_postulate: The postulate it is grounded in

Origin: docs/00_MAQOOL_CONSTITUTION.md (all sections)
"""
from __future__ import annotations

import pytest

from taaqqul_slot_geometry.constitution.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.L0.phoneme import PhonemeUnit, PhoneticPattern
from taaqqul_slot_geometry.L0.syllable import SyllableType
from taaqqul_slot_geometry.L0.weight import WeightPattern
from taaqqul_slot_geometry.runtime.constitutional_engine import (
    ConstitutionalEngine,
    ConstitutionalRuntimeError,
    JamidUnit,
    TraceStep,
)


class ConstitutionalRuntimeTest:
    """Base class for all runtime integration tests.

    Every subclass MUST declare constitutional origin.
    """

    origin_pr: str = "PR#2.5"
    origin_theorem: str = ""
    origin_postulate: str = ""


# ═══════════════════════════════════════════════════════════════════════════════
# Test Group 1: Full Pipeline Success Cases
# ═══════════════════════════════════════════════════════════════════════════════


class TestFullPipelineBasic(ConstitutionalRuntimeTest):
    """Full pipeline execution with basic inputs.

    Origin: docs/00_MAQOOL_CONSTITUTION.md §3, §4, §2, §8, BL-L0-05
    """

    origin_pr = "PR#1"
    origin_theorem = "TH1"
    origin_postulate = "P7"

    def test_basic_fatha_pipeline(self) -> None:
        """Consonant 'k' + fatha → full JamidUnit.
        Origin: §3 MCE-1 (C_FATHA pattern)."""
        engine = ConstitutionalEngine()
        jamid, trace = engine.full_pipeline(
            consonant="k", vowel="fatha",
            weight_pattern="faala", root_letters=("k", "t", "b"),
        )
        assert jamid.status == "CANDIDATE"
        assert jamid.root_letters == ("k", "t", "b")
        assert jamid.weight_pattern == WeightPattern.FAALA
        assert len(trace) == 5

    def test_basic_damma_pipeline(self) -> None:
        """Consonant 'b' + damma → full JamidUnit.
        Origin: §3 MCE-1 (C_DAMMA pattern)."""
        engine = ConstitutionalEngine()
        jamid, trace = engine.full_pipeline(
            consonant="b", vowel="damma",
            weight_pattern="faal", root_letters=("b", "n", "y"),
        )
        assert jamid.status == "CANDIDATE"
        assert jamid.root_letters == ("b", "n", "y")
        assert jamid.weight_pattern == WeightPattern.FAAL

    def test_basic_kasra_pipeline(self) -> None:
        """Consonant 's' + kasra → full JamidUnit.
        Origin: §3 MCE-1 (C_KASRA pattern)."""
        engine = ConstitutionalEngine()
        jamid, trace = engine.full_pipeline(
            consonant="s", vowel="kasra",
            weight_pattern="fiaal", root_letters=("s", "l", "m"),
        )
        assert jamid.status == "CANDIDATE"
        assert jamid.weight_pattern == WeightPattern.FIAAL

    def test_madd_alif_pipeline(self) -> None:
        """Consonant 'n' + alif_madd → full JamidUnit.
        Origin: §3 MCE-1 (C_FATHA_MADD pattern)."""
        engine = ConstitutionalEngine()
        jamid, trace = engine.full_pipeline(
            consonant="n", vowel="alif_madd",
            weight_pattern="faalil", root_letters=("n", "s", "r"),
        )
        assert jamid.status == "CANDIDATE"
        assert jamid.weight_pattern == WeightPattern.FAALIL

    def test_madd_waw_pipeline(self) -> None:
        """Consonant 'q' + waw_madd → full JamidUnit.
        Origin: §3 MCE-1 (C_DAMMA_MADD pattern)."""
        engine = ConstitutionalEngine()
        jamid, trace = engine.full_pipeline(
            consonant="q", vowel="waw_madd",
            weight_pattern="mafuul", root_letters=("q", "t", "l"),
        )
        assert jamid.status == "CANDIDATE"
        assert jamid.weight_pattern == WeightPattern.MAFUUL


# ═══════════════════════════════════════════════════════════════════════════════
# Test Group 2: Arabic Input Acceptance
# ═══════════════════════════════════════════════════════════════════════════════


class TestArabicInputPipeline(ConstitutionalRuntimeTest):
    """Pipeline accepts Arabic vowel and weight names.

    Origin: docs/00_MAQOOL_CONSTITUTION.md §2 Category 2
    """

    origin_pr = "PR#2.5"
    origin_theorem = "TH2"
    origin_postulate = "P1"

    def test_arabic_fatha(self) -> None:
        """Arabic فتحة vowel input.
        Origin: §3 MCE-1."""
        engine = ConstitutionalEngine()
        jamid, _ = engine.full_pipeline(
            consonant="ك", vowel="فتحة",
            weight_pattern="فَعَلَ", root_letters=("ك", "ت", "ب"),
        )
        assert jamid.status == "CANDIDATE"
        assert jamid.root_letters == ("ك", "ت", "ب")

    def test_arabic_damma(self) -> None:
        """Arabic ضمة vowel input.
        Origin: §3 MCE-1."""
        engine = ConstitutionalEngine()
        jamid, _ = engine.full_pipeline(
            consonant="ب", vowel="ضمة",
            weight_pattern="فَعْل", root_letters=("ب", "ن", "ي"),
        )
        assert jamid.status == "CANDIDATE"

    def test_arabic_kasra(self) -> None:
        """Arabic كسرة vowel input.
        Origin: §3 MCE-1."""
        engine = ConstitutionalEngine()
        jamid, _ = engine.full_pipeline(
            consonant="س", vowel="كسرة",
            weight_pattern="فِعَال", root_letters=("س", "ل", "م"),
        )
        assert jamid.status == "CANDIDATE"

    def test_arabic_sukun_requires_cvc_context(self) -> None:
        """Arabic سكون cannot form a syllable alone — must be CVC.
        Origin: §4 MCE-2 (CVC requires CVC∅ pattern, not bare sukun)."""
        engine = ConstitutionalEngine()
        # Sukun alone cannot form a syllable (constitutionally correct)
        with pytest.raises(ConstitutionalRuntimeError) as exc_info:
            engine.full_pipeline(
                consonant="ت", vowel="سكون",
                weight_pattern="جذر", root_letters=("ت", "ر", "ك"),
            )
        assert exc_info.value.failure_code == FailureCode.M_00_03

    def test_arabic_madd_alif(self) -> None:
        """Arabic مد_ألف vowel input.
        Origin: §3 MCE-1."""
        engine = ConstitutionalEngine()
        jamid, _ = engine.full_pipeline(
            consonant="ن", vowel="مد_ألف",
            weight_pattern="فَاعِل", root_letters=("ن", "ص", "ر"),
        )
        assert jamid.status == "CANDIDATE"


# ═══════════════════════════════════════════════════════════════════════════════
# Test Group 3: Trace Verification
# ═══════════════════════════════════════════════════════════════════════════════


class TestTraceVerification(ConstitutionalRuntimeTest):
    """Verify that the execution trace is correct and auditable.

    Origin: docs/00_MAQOOL_CONSTITUTION.md §5 Rules 7, 8
    """

    origin_pr = "PR#2.5"
    origin_theorem = "TH3"
    origin_postulate = "P7"

    def test_trace_has_5_steps(self) -> None:
        """Full pipeline produces exactly 5 trace steps.
        Origin: §5 Rule 8 (No-Leap)."""
        engine = ConstitutionalEngine()
        _, trace = engine.full_pipeline(
            consonant="k", vowel="fatha",
            weight_pattern="faala", root_letters=("k", "t", "b"),
        )
        assert len(trace) == 5

    def test_trace_steps_sequential(self) -> None:
        """Steps are numbered 1-5 sequentially.
        Origin: §5 Rule 8 (No-Leap)."""
        engine = ConstitutionalEngine()
        _, trace = engine.full_pipeline(
            consonant="k", vowel="fatha",
            weight_pattern="faala", root_letters=("k", "t", "b"),
        )
        assert [s.step_number for s in trace] == [1, 2, 3, 4, 5]

    def test_no_leap_verified(self) -> None:
        """ConstitutionalEngine.verify_no_leap confirms sequential execution.
        Origin: §5 Rule 8."""
        engine = ConstitutionalEngine()
        _, trace = engine.full_pipeline(
            consonant="k", vowel="fatha",
            weight_pattern="faala", root_letters=("k", "t", "b"),
        )
        assert ConstitutionalEngine.verify_no_leap(trace) is True

    def test_identity_preserved_verified(self) -> None:
        """ConstitutionalEngine.verify_identity_preserved confirms no loss.
        Origin: §5 Rule 7."""
        engine = ConstitutionalEngine()
        _, trace = engine.full_pipeline(
            consonant="k", vowel="fatha",
            weight_pattern="faala", root_letters=("k", "t", "b"),
        )
        assert ConstitutionalEngine.verify_identity_preserved(trace) is True

    def test_trace_steps_have_constitutional_refs(self) -> None:
        """Every trace step has a non-empty constitutional_ref.
        Origin: §5 Rule 7."""
        engine = ConstitutionalEngine()
        _, trace = engine.full_pipeline(
            consonant="k", vowel="fatha",
            weight_pattern="faala", root_letters=("k", "t", "b"),
        )
        for step in trace:
            assert step.constitutional_ref
            assert "docs/" in step.constitutional_ref


# ═══════════════════════════════════════════════════════════════════════════════
# Test Group 4: Rejection Cases
# ═══════════════════════════════════════════════════════════════════════════════


class TestRejectionCases(ConstitutionalRuntimeTest):
    """All rejection paths raise ConstitutionalRuntimeError with named code.

    Origin: docs/00_MAQOOL_CONSTITUTION.md §5 Rule 5
    """

    origin_pr = "PR#2.5"
    origin_theorem = "TH4"
    origin_postulate = "P5"

    def test_empty_consonant_rejected(self) -> None:
        """Empty consonant → M_00_14.
        Origin: §3 MCE-1."""
        engine = ConstitutionalEngine()
        with pytest.raises(ConstitutionalRuntimeError) as exc_info:
            engine.full_pipeline(
                consonant="", vowel="fatha",
                weight_pattern="faala", root_letters=("k", "t", "b"),
            )
        assert exc_info.value.failure_code == FailureCode.M_00_14

    def test_invalid_vowel_rejected(self) -> None:
        """Invalid vowel → M_00_02.
        Origin: §3 MCE-1."""
        engine = ConstitutionalEngine()
        with pytest.raises(ConstitutionalRuntimeError) as exc_info:
            engine.full_pipeline(
                consonant="k", vowel="invalid_vowel",
                weight_pattern="faala", root_letters=("k", "t", "b"),
            )
        assert exc_info.value.failure_code == FailureCode.M_00_02

    def test_invalid_weight_rejected(self) -> None:
        """Invalid weight → M_00_22.
        Origin: §5 Rule 10."""
        engine = ConstitutionalEngine()
        with pytest.raises(ConstitutionalRuntimeError) as exc_info:
            engine.full_pipeline(
                consonant="k", vowel="fatha",
                weight_pattern="invalid_weight", root_letters=("k", "t", "b"),
            )
        assert exc_info.value.failure_code == FailureCode.M_00_22

    def test_empty_root_rejected(self) -> None:
        """Empty root_letters → M_00_22.
        Origin: BL-L0-05."""
        engine = ConstitutionalEngine()
        with pytest.raises(ConstitutionalRuntimeError) as exc_info:
            engine.full_pipeline(
                consonant="k", vowel="fatha",
                weight_pattern="faala", root_letters=(),
            )
        assert exc_info.value.failure_code == FailureCode.M_00_22

    def test_step1_failure_does_not_proceed(self) -> None:
        """If step 1 fails, steps 2-5 never execute.
        Origin: §5 Rule 5 (no silent exceptions)."""
        engine = ConstitutionalEngine()
        with pytest.raises(ConstitutionalRuntimeError) as exc_info:
            engine.full_pipeline(
                consonant="", vowel="fatha",
                weight_pattern="faala", root_letters=("k", "t", "b"),
            )
        assert exc_info.value.failure_code == FailureCode.M_00_14


# ═══════════════════════════════════════════════════════════════════════════════
# Test Group 5: Output Structure Verification
# ═══════════════════════════════════════════════════════════════════════════════


class TestOutputStructure(ConstitutionalRuntimeTest):
    """Verify the structure of the JamidUnit output.

    Origin: docs/00_MAQOOL_CONSTITUTION.md §5 Rules 2, 3
    """

    origin_pr = "PR#2.5"
    origin_theorem = "TH5"
    origin_postulate = "P7"

    def test_jamid_is_frozen(self) -> None:
        """JamidUnit is immutable (Rule 3).
        Origin: §5 Rule 3."""
        engine = ConstitutionalEngine()
        jamid, _ = engine.full_pipeline(
            consonant="k", vowel="fatha",
            weight_pattern="faala", root_letters=("k", "t", "b"),
        )
        with pytest.raises(Exception):
            jamid.status = "PROMOTED"  # type: ignore[misc]

    def test_jamid_has_trace_ref(self) -> None:
        """JamidUnit carries trace_ref (Rule 2).
        Origin: §5 Rule 2."""
        engine = ConstitutionalEngine()
        jamid, _ = engine.full_pipeline(
            consonant="k", vowel="fatha",
            weight_pattern="faala", root_letters=("k", "t", "b"),
        )
        assert jamid.trace_ref
        assert "docs/" in jamid.trace_ref

    def test_jamid_rank_is_candidate(self) -> None:
        """JamidUnit rank is always CANDIDATE (Rule 2).
        Origin: §5 Rule 2."""
        engine = ConstitutionalEngine()
        jamid, _ = engine.full_pipeline(
            consonant="k", vowel="fatha",
            weight_pattern="faala", root_letters=("k", "t", "b"),
        )
        assert jamid.rank == "CANDIDATE"

    def test_jamid_has_signifier(self) -> None:
        """JamidUnit carries the licensed Signifier.
        Origin: §8 P1."""
        engine = ConstitutionalEngine()
        jamid, _ = engine.full_pipeline(
            consonant="k", vowel="fatha",
            weight_pattern="faala", root_letters=("k", "t", "b"),
        )
        assert jamid.signifier is not None
        assert jamid.signifier.license_ref == "P1:sound_primacy"

    def test_jamid_has_phoneme(self) -> None:
        """JamidUnit carries the originating PhonemeUnit.
        Origin: §3 MCE-1."""
        engine = ConstitutionalEngine()
        jamid, _ = engine.full_pipeline(
            consonant="k", vowel="fatha",
            weight_pattern="faala", root_letters=("k", "t", "b"),
        )
        assert jamid.phoneme is not None
        assert jamid.phoneme.consonant == "k"
        assert jamid.phoneme.pattern == PhoneticPattern.C_FATHA
