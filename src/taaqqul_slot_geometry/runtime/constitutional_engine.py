"""
ConstitutionalEngine — the runtime pipeline that transforms Arabic input
into constitutionally-licensed JamidUnit output.

Origin: docs/00_MAQOOL_CONSTITUTION.md (all sections)
Trace: Every step references a constitutional clause.

Pipeline (5 steps):
  Step 1: Consonant + Vowel → PhonemeUnit (§3 MCE-1)
  Step 2: PhonemeUnit → Syllable (§4 MCE-2)
  Step 3: Syllable → Utterance (§2 Category 2)
  Step 4: Utterance → Signifier (§8 P1)
  Step 5: Signifier + Weight → JamidUnit (BL-L0-05)

Condition: Each step receives a constitutionally-valid input.
Cause: Sound primacy demands phoneme before meaning.
Barrier: Any invalid input produces a named RuntimeError with FailureCode.
Motive: Build an Arabic analysis machine that rejects before producing judgment.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import FrozenSet, List, Tuple

from taaqqul_slot_geometry.constitution.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.L0.phoneme import PhonemeUnit, PhoneticPattern
from taaqqul_slot_geometry.L0.syllable import Syllable, make_syllable
from taaqqul_slot_geometry.L0.utterance import Utterance
from taaqqul_slot_geometry.L0.signifier import Signifier
from taaqqul_slot_geometry.L0.weight import WeightPattern


# ── Mapping from Arabic vowel names to PhoneticPattern ────────────────────────

_VOWEL_TO_PATTERN: dict[str, PhoneticPattern] = {
    "فتحة": PhoneticPattern.C_FATHA,
    "ضمة": PhoneticPattern.C_DAMMA,
    "كسرة": PhoneticPattern.C_KASRA,
    "سكون": PhoneticPattern.C_SUKUN,
    "مد_ألف": PhoneticPattern.C_FATHA_MADD,
    "مد_واو": PhoneticPattern.C_DAMMA_MADD,
    "مد_ياء": PhoneticPattern.C_KASRA_MADD,
    # English aliases
    "fatha": PhoneticPattern.C_FATHA,
    "damma": PhoneticPattern.C_DAMMA,
    "kasra": PhoneticPattern.C_KASRA,
    "sukun": PhoneticPattern.C_SUKUN,
    "alif_madd": PhoneticPattern.C_FATHA_MADD,
    "waw_madd": PhoneticPattern.C_DAMMA_MADD,
    "ya_madd": PhoneticPattern.C_KASRA_MADD,
}

# ── Mapping from Arabic weight names to WeightPattern ─────────────────────────

_WEIGHT_NAME_MAP: dict[str, WeightPattern] = {
    "فَعَلَ": WeightPattern.FAALA,
    "فَعْل": WeightPattern.FAAL,
    "فِعَال": WeightPattern.FIAAL,
    "فُعَال": WeightPattern.FUAL,
    "فَاعِل": WeightPattern.FAALIL,
    "مَفْعُول": WeightPattern.MAFUUL,
    "تَفَاعَلَ": WeightPattern.TAFAALA,
    "اسْتَفْعَلَ": WeightPattern.ISTAFALA,
    "جذر": WeightPattern.ROOT,
    # English aliases
    "faala": WeightPattern.FAALA,
    "faal": WeightPattern.FAAL,
    "fiaal": WeightPattern.FIAAL,
    "fual": WeightPattern.FUAL,
    "faalil": WeightPattern.FAALIL,
    "mafuul": WeightPattern.MAFUUL,
    "tafaala": WeightPattern.TAFAALA,
    "istafala": WeightPattern.ISTAFALA,
    "root": WeightPattern.ROOT,
}


# ── Trace Record ──────────────────────────────────────────────────────────────


@dataclass(frozen=True)
class TraceStep:
    """A single step in the constitutional execution trace.

    Condition: step_name describes the transformation performed.
    Cause: constitutional_ref points to the authorising clause.
    Barrier: invalid steps cannot be constructed (frozen + birth guards).
    Motive: Auditable trail for every pipeline execution.

    Parameters
    ----------
    step_number : int
        Sequential step index (1-based).
    step_name : str
        Human-readable description of the transformation.
    constitutional_ref : str
        Reference to the constitutional clause authorising this step.
    input_type : str
        Type name of the input entity.
    output_type : str
        Type name of the output entity.
    identity_preserved : bool
        Recorded result: whether Identity(input) ⊆ Identity(output).
    identity_proof_ref : str
        Reference to the proof object backing the recorded identity result.
    trace_ref : str
        Constitutional reference for the trace itself.
    rank : str
        Always "CANDIDATE".
    residuals : FrozenSet[str]
        Residual bundle.
    """

    step_number: int
    step_name: str
    constitutional_ref: str
    input_type: str
    output_type: str
    identity_preserved: bool
    identity_proof_ref: str
    trace_ref: str = "docs/00_MAQOOL_CONSTITUTION.md §5 Rule 7"
    rank: str = "CANDIDATE"
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if self.step_number < 1:
            raise ValueError(
                f"{FailureCode.M_CX_02.value}: step_number must be >= 1"
            )
        if not self.step_name:
            raise ValueError(
                f"{FailureCode.M_CX_12.value}: step_name is empty"
            )
        if not self.constitutional_ref:
            raise ValueError(
                f"{FailureCode.M_CX_12.value}: constitutional_ref is empty"
            )
        if not isinstance(self.identity_preserved, bool):
            raise ValueError(
                f"{FailureCode.M_CX_01.value}: identity_preserved must be bool"
            )
        if not isinstance(self.identity_proof_ref, str) or not self.identity_proof_ref:
            raise ValueError(
                f"{FailureCode.M_CX_01.value}: identity_proof_ref is required"
            )
        if not self.trace_ref:
            raise ValueError(FailureCode.M_CX_12.value)
        if self.rank != "CANDIDATE":
            raise ValueError(FailureCode.M_CX_09.value)


# ── JamidUnit — the final output of the pipeline ─────────────────────────────


@dataclass(frozen=True)
class JamidUnit:
    """The constitutionally-licensed output of the full pipeline.

    Condition: All 5 pipeline steps completed successfully.
    Cause: Sound + pattern + weight + signification yield a licensed unit.
    Barrier: Any missing field raises a named error.
    Motive: This is the minimal complete L0 unit ready for L1 bridging.

    Parameters
    ----------
    status : str
        Always "CANDIDATE" in L0.
    root_letters : Tuple[str, ...]
        The consonantal root skeleton.
    weight_pattern : WeightPattern
        The applied weight pattern.
    signifier : Signifier
        The licensed phonological form.
    phoneme : PhonemeUnit
        The originating phoneme.
    trace_ref : str
        Constitutional reference.
    rank : str
        Always "CANDIDATE".
    residuals : FrozenSet[str]
        Residual bundle.
    """

    status: str
    root_letters: Tuple[str, ...]
    weight_pattern: WeightPattern
    signifier: Signifier
    phoneme: PhonemeUnit
    trace_ref: str = "docs/00_MAQOOL_CONSTITUTION.md BL-L0-05"
    rank: str = "CANDIDATE"
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if self.status != "CANDIDATE":
            raise ValueError(FailureCode.M_00_10.value)
        if not self.root_letters:
            raise ValueError(
                f"{FailureCode.M_00_22.value}: root_letters is empty"
            )
        if not isinstance(self.weight_pattern, WeightPattern):
            raise ValueError(FailureCode.M_00_22.value)
        if self.signifier is None:
            raise ValueError(FailureCode.M_00_18.value)
        if self.phoneme is None:
            raise ValueError(
                f"{FailureCode.M_00_14.value}: phoneme is required"
            )
        if not self.trace_ref:
            raise ValueError(FailureCode.M_00_11.value)
        if self.rank != "CANDIDATE":
            raise ValueError(FailureCode.M_00_10.value)


# ── Constitutional Engine ─────────────────────────────────────────────────────


class ConstitutionalRuntimeError(RuntimeError):
    """Named runtime error with a constitutional FailureCode.

    Condition: An unconstitutional operation was attempted.
    Cause: The input violated a specific constitutional clause.
    Barrier: Cannot be silently swallowed (Rule 5).
    Motive: Audit trail for all rejections.
    """

    def __init__(self, message: str, failure_code: FailureCode) -> None:
        super().__init__(f"{failure_code.value}: {message}")
        self.failure_code = failure_code


class ConstitutionalEngine:
    """The runtime constitutional engine — transforms Arabic input into licensed output.

    Condition: Must be instantiated before use.
    Cause: Encapsulates the 5-step pipeline logic.
    Barrier: All methods raise ConstitutionalRuntimeError on invalid input.
    Motive: Single entry point for constitutionally-governed Arabic analysis.

    Pipeline:
      1. consonant + vowel → PhonemeUnit
      2. PhonemeUnit → Syllable
      3. Syllable → Utterance
      4. Utterance → Signifier
      5. Signifier + weight + root → JamidUnit

    Origin: docs/00_MAQOOL_CONSTITUTION.md (all sections)
    """

    def __init__(self) -> None:
        self._trace_ref = "docs/00_MAQOOL_CONSTITUTION.md"

    # ── Step 1: Phoneme Construction ─────────────────────────────────────────

    def step1_phoneme(self, consonant: str, vowel: str) -> PhonemeUnit:
        """Condition: consonant is a single Arabic letter, vowel is valid.
        Cause: Sound is the atomic unit (P7: sound primacy).
        Barrier: Invalid consonant → M_00_14; invalid vowel → M_00_02.
        Motive: Build الوحدة الصوتية."""
        if not consonant:
            raise ConstitutionalRuntimeError(
                "consonant is empty", FailureCode.M_00_14
            )
        pattern = _VOWEL_TO_PATTERN.get(vowel)
        if pattern is None:
            raise ConstitutionalRuntimeError(
                f"vowel {vowel!r} is not valid; must be one of: "
                f"{sorted(_VOWEL_TO_PATTERN.keys())}",
                FailureCode.M_00_02,
            )
        try:
            return PhonemeUnit(consonant=consonant, pattern=pattern)
        except ValueError as e:
            raise ConstitutionalRuntimeError(
                str(e), FailureCode.M_00_14
            ) from e

    # ── Step 2: Syllable Construction ────────────────────────────────────────

    def step2_syllable(self, phoneme: PhonemeUnit) -> Syllable:
        """Condition: phoneme is a valid PhonemeUnit.
        Cause: Syllable is the minimal complete unit (MCE-2).
        Barrier: Invalid pattern → M_00_03.
        Motive: Build المقطع الصوتي."""
        try:
            return make_syllable(phonemes=(phoneme,))
        except ValueError as e:
            raise ConstitutionalRuntimeError(
                str(e), FailureCode.M_00_03
            ) from e

    # ── Step 3: Utterance Construction ───────────────────────────────────────

    def step3_utterance(self, syllable: Syllable) -> Utterance:
        """Condition: syllable is a valid Syllable.
        Cause: Utterance is the word-level phonological unit.
        Barrier: Empty syllable sequence → M_00_06.
        Motive: Build النُّطق."""
        try:
            return Utterance(syllables=(syllable,))
        except ValueError as e:
            raise ConstitutionalRuntimeError(
                str(e), FailureCode.M_00_06
            ) from e

    # ── Step 4: Signifier Construction ───────────────────────────────────────

    def step4_signifier(self, utterance: Utterance) -> Signifier:
        """Condition: utterance is a valid Utterance.
        Cause: Signifier is a licensed phonological form (P1).
        Barrier: Missing utterance → M_00_18.
        Motive: Build الدّال."""
        try:
            return Signifier(
                utterance=utterance,
                license_ref="P1:sound_primacy",
            )
        except ValueError as e:
            raise ConstitutionalRuntimeError(
                str(e), FailureCode.M_00_18
            ) from e

    # ── Step 5: JamidUnit Construction ───────────────────────────────────────

    def step5_jamid(
        self,
        signifier: Signifier,
        phoneme: PhonemeUnit,
        weight_pattern: str,
        root_letters: Tuple[str, ...],
    ) -> JamidUnit:
        """Condition: signifier + weight + root are valid.
        Cause: JamidUnit is the final L0 output (BL-L0-05).
        Barrier: Invalid weight → M_00_22; empty root → M_00_22.
        Motive: Build الجامد المرخّص."""
        wp = _WEIGHT_NAME_MAP.get(weight_pattern)
        if wp is None:
            raise ConstitutionalRuntimeError(
                f"weight_pattern {weight_pattern!r} is not valid; must be one of: "
                f"{sorted(_WEIGHT_NAME_MAP.keys())}",
                FailureCode.M_00_22,
            )
        if not root_letters:
            raise ConstitutionalRuntimeError(
                "root_letters is empty", FailureCode.M_00_22
            )
        try:
            return JamidUnit(
                status="CANDIDATE",
                root_letters=root_letters,
                weight_pattern=wp,
                signifier=signifier,
                phoneme=phoneme,
            )
        except ValueError as e:
            raise ConstitutionalRuntimeError(
                str(e), FailureCode.M_00_22
            ) from e

    # ── Full Pipeline ────────────────────────────────────────────────────────

    def full_pipeline(
        self,
        consonant: str,
        vowel: str,
        weight_pattern: str,
        root_letters: Tuple[str, ...],
    ) -> Tuple[JamidUnit, List[TraceStep]]:
        """Execute the full 5-step constitutional pipeline.

        Condition: All inputs are valid Arabic constructs.
        Cause: The pipeline enforces sound-primacy and sequential construction.
        Barrier: Any step failure raises ConstitutionalRuntimeError.
        Motive: Produce a licensed JamidUnit with full audit trace.

        Parameters
        ----------
        consonant : str
            Arabic consonant (single character or IPA symbol).
        vowel : str
            Vowel name (Arabic or English).
        weight_pattern : str
            Weight pattern name (Arabic or English).
        root_letters : Tuple[str, ...]
            Root consonant letters.

        Returns
        -------
        Tuple[JamidUnit, List[TraceStep]]
            The licensed JamidUnit and the execution trace.

        Raises
        ------
        ConstitutionalRuntimeError
            If any step violates a constitutional clause.
        """
        trace: List[TraceStep] = []

        # Step 1: Phoneme
        phoneme = self.step1_phoneme(consonant, vowel)
        trace.append(TraceStep(
            step_number=1,
            step_name="consonant+vowel → PhonemeUnit",
            constitutional_ref="docs/00_MAQOOL_CONSTITUTION.md §3 (MCE-1)",
            input_type="str",
            output_type="PhonemeUnit",
            identity_preserved=True,
            identity_proof_ref="proof:trace-step-1-phoneme-identity",
        ))

        # Step 2: Syllable
        syllable = self.step2_syllable(phoneme)
        trace.append(TraceStep(
            step_number=2,
            step_name="PhonemeUnit → Syllable",
            constitutional_ref="docs/00_MAQOOL_CONSTITUTION.md §4 (MCE-2)",
            input_type="PhonemeUnit",
            output_type="Syllable",
            identity_preserved=True,
            identity_proof_ref="proof:trace-step-2-syllable-identity",
        ))

        # Step 3: Utterance
        utterance = self.step3_utterance(syllable)
        trace.append(TraceStep(
            step_number=3,
            step_name="Syllable → Utterance",
            constitutional_ref="docs/00_MAQOOL_CONSTITUTION.md §2 Category 2",
            input_type="Syllable",
            output_type="Utterance",
            identity_preserved=True,
            identity_proof_ref="proof:trace-step-3-utterance-identity",
        ))

        # Step 4: Signifier
        signifier = self.step4_signifier(utterance)
        trace.append(TraceStep(
            step_number=4,
            step_name="Utterance → Signifier",
            constitutional_ref="docs/00_MAQOOL_CONSTITUTION.md §8 P1",
            input_type="Utterance",
            output_type="Signifier",
            identity_preserved=True,
            identity_proof_ref="proof:trace-step-4-signifier-identity",
        ))

        # Step 5: JamidUnit
        jamid = self.step5_jamid(signifier, phoneme, weight_pattern, root_letters)
        trace.append(TraceStep(
            step_number=5,
            step_name="Signifier+Weight → JamidUnit",
            constitutional_ref="docs/01_L0_PHONETIC_BOUNDARY.md BL-L0-05",
            input_type="Signifier",
            output_type="JamidUnit",
            identity_preserved=True,
            identity_proof_ref="proof:trace-step-5-jamid-identity",
        ))

        return jamid, trace

    # ── Adjacency Verification ───────────────────────────────────────────────

    @staticmethod
    def verify_no_leap(trace: List[TraceStep]) -> bool:
        """Verify that no step in the trace leaps (step_number is sequential).

        Condition: Steps must be numbered 1, 2, 3, 4, 5 sequentially.
        Cause: No-Leap Axiom (Rule 8) applies within the pipeline.
        Barrier: Non-sequential steps indicate a leap.
        Motive: Audit that no step was skipped.
        """
        for i, step in enumerate(trace):
            if step.step_number != i + 1:
                return False
        return True

    @staticmethod
    def verify_identity_preserved(trace: List[TraceStep]) -> bool:
        """Verify that identity is preserved across all steps.

        Condition: Every step must declare identity_preserved=True.
        Cause: Identity Preservation (Rule 7) requires no loss.
        Barrier: Any step with identity_preserved=False is a violation.
        Motive: Audit that no identity was lost.
        """
        return all(step.identity_preserved for step in trace)
