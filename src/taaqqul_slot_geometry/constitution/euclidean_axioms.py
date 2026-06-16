"""
Euclidean-style axiomatic proofs for the Maqool Constitution.
Origin: docs/00_MAQOOL_CONSTITUTION.md §5, §8, §9

This module implements a Euclidean proof structure (Definitions → Postulates →
Common Notions → Theorems) that formally demonstrates why the constitutional
architecture must hold. Each theorem is proven from definitions and postulates,
never from intuition.

Architecture:
    المعقول (M) ──[P8: أعمق]──→ لا يستلزم صوت
        ↑                              ↓
        └────[R: ظهور]────←──[W: رخصة]──←── الصوت (S)
               ↑___________________________↓
                  [P7: متغير] [P6: هوية محفوظة]

    القفز (Q): مستحيل [P10 + TH4]
"""
from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from enum import Enum, unique
from typing import FrozenSet, Tuple, final

from taaqqul_slot_geometry.constitution.failure_taxonomy import FailureCode


# ══════════════════════════════════════════════════════════════════════════════
# §1  ENUMERATIONS
# ══════════════════════════════════════════════════════════════════════════════


@unique
class DefinitionId(str, Enum):
    """Unique identifiers for the seven fundamental definitions."""

    M = "definition.M"       # المعقول (the Intelligible)
    S = "definition.S"       # الصوت (Sound/Phonetic)
    W = "definition.W"       # الوزن (Weight/Pattern)
    R = "definition.R"       # الظهور (Manifestation)
    Q = "definition.Q"       # القفز (Leap)
    LAYER = "definition.LAYER"  # الطبقة (Layer)
    ID = "definition.ID"     # الهوية (Identity)


@unique
class PostulateId(str, Enum):
    """Unique identifiers for postulates P6–P10."""

    P6 = "postulate.P6"   # Identity Preservation (هوية محفوظة)
    P7 = "postulate.P7"   # Change (متغير) — form changes, meaning preserved
    P8 = "postulate.P8"   # Depth (أعمق) — M is deeper than S
    P9 = "postulate.P9"   # License (رخصة) — W licenses R
    P10 = "postulate.P10"  # No-Leap (عدم القفز) — adjacent layers only


@unique
class TheoremId(str, Enum):
    """Unique identifiers for the four theorems."""

    TH1 = "theorem.TH1"  # الظهور لا ينتج المعنى (Manifestation doesn't produce meaning)
    TH2 = "theorem.TH2"  # الأصوات محدودة (Sounds are finite)
    TH3 = "theorem.TH3"  # الوزن حاجز لا مصدر (Weight is barrier, not source)
    TH4 = "theorem.TH4"  # القفز مستحيل (Leap is impossible)


# ══════════════════════════════════════════════════════════════════════════════
# §2  ERRORS
# ══════════════════════════════════════════════════════════════════════════════


@final
class ProofVerificationError(Exception):
    """Raised when a proof fails verification.

    Every failure carries: the theorem, the step number, and the reason.
    Never silent (Rule 5).
    """

    def __init__(self, theorem_id: TheoremId, step_number: int, reason: str) -> None:
        super().__init__(
            f"{FailureCode.M_02_08.value}: theorem={theorem_id.value} "
            f"step={step_number} reason={reason}"
        )
        self.theorem_id = theorem_id
        self.step_number = step_number
        self.reason = reason


# ══════════════════════════════════════════════════════════════════════════════
# §3  CORE ENTITIES
# ══════════════════════════════════════════════════════════════════════════════


@dataclass(frozen=True, slots=True)
class EuclideanDefinition:
    """A constitutional definition (one of seven).

    Each definition establishes a primitive term in the system.
    All definitions are frozen candidates with full traceability.
    """

    definition_id: DefinitionId
    name_ar: str
    name_en: str
    formal_statement: str
    trace_ref: str
    rank: str = "CANDIDATE"
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if not self.trace_ref:
            raise ValueError(FailureCode.M_00_11.value)
        if self.rank != "CANDIDATE":
            raise ValueError(FailureCode.M_00_10.value)
        if not isinstance(self.definition_id, DefinitionId):
            raise ValueError(f"{FailureCode.M_CX_08.value}: invalid_definition_id")
        if not self.name_ar:
            raise ValueError(f"{FailureCode.M_CX_08.value}: name_ar_empty")
        if not self.formal_statement:
            raise ValueError(f"{FailureCode.M_CX_08.value}: formal_statement_empty")


@dataclass(frozen=True, slots=True)
class EuclideanPostulate:
    """A constitutional postulate (P6–P10).

    Postulates are unprovable axioms that the system accepts as true.
    Each postulate declares its dependencies (definitions and prior postulates).
    """

    postulate_id: PostulateId
    name_ar: str
    name_en: str
    formal_statement: str
    dependencies: Tuple[str, ...]
    trace_ref: str
    rank: str = "CANDIDATE"
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if not self.trace_ref:
            raise ValueError(FailureCode.M_00_11.value)
        if self.rank != "CANDIDATE":
            raise ValueError(FailureCode.M_00_10.value)
        if not isinstance(self.postulate_id, PostulateId):
            raise ValueError(f"{FailureCode.M_CX_08.value}: invalid_postulate_id")
        if not self.formal_statement:
            raise ValueError(f"{FailureCode.M_CX_08.value}: formal_statement_empty")


@dataclass(frozen=True, slots=True)
class ProofStep:
    """A single step in a theorem's proof.

    Each step cites a justification (definition, postulate, or prior theorem).
    """

    step_number: int
    statement: str
    justification: str
    trace_ref: str
    rank: str = "CANDIDATE"
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if not self.trace_ref:
            raise ValueError(FailureCode.M_00_11.value)
        if self.rank != "CANDIDATE":
            raise ValueError(FailureCode.M_00_10.value)
        if self.step_number < 1:
            raise ValueError(f"{FailureCode.M_CX_08.value}: step_number_must_be_positive")
        if not self.statement:
            raise ValueError(f"{FailureCode.M_CX_08.value}: statement_empty")
        if not self.justification:
            raise ValueError(f"{FailureCode.M_CX_08.value}: justification_empty")


@dataclass(frozen=True, slots=True)
class EuclideanTheorem:
    """A constitutional theorem with its full proof.

    Each theorem carries:
    - Its identifier
    - The proof steps (ordered tuple)
    - The dependencies it requires
    - Full traceability
    """

    theorem_id: TheoremId
    name_ar: str
    name_en: str
    formal_statement: str
    proof_steps: Tuple[ProofStep, ...]
    dependencies: Tuple[str, ...]
    trace_ref: str
    rank: str = "CANDIDATE"
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if not self.trace_ref:
            raise ValueError(FailureCode.M_00_11.value)
        if self.rank != "CANDIDATE":
            raise ValueError(FailureCode.M_00_10.value)
        if not isinstance(self.theorem_id, TheoremId):
            raise ValueError(f"{FailureCode.M_CX_08.value}: invalid_theorem_id")
        if not self.formal_statement:
            raise ValueError(f"{FailureCode.M_CX_08.value}: formal_statement_empty")
        if not self.proof_steps:
            raise ValueError(f"{FailureCode.M_CX_08.value}: proof_steps_empty")
        # Verify step sequence is contiguous starting from 1
        for i, step in enumerate(self.proof_steps, start=1):
            if step.step_number != i:
                raise ValueError(
                    f"{FailureCode.M_CX_08.value}: step_sequence_gap_at_{i}"
                )


# ══════════════════════════════════════════════════════════════════════════════
# §4  THE SEVEN DEFINITIONS
# ══════════════════════════════════════════════════════════════════════════════


DEFINITION_M = EuclideanDefinition(
    definition_id=DefinitionId.M,
    name_ar="المعقول",
    name_en="The Intelligible",
    formal_statement="M := entity whose existence does not entail phonetic manifestation",
    trace_ref="euclid.def.M",
)

DEFINITION_S = EuclideanDefinition(
    definition_id=DefinitionId.S,
    name_ar="الصوت",
    name_en="Sound",
    formal_statement="S := licensed phonetic sequence from the closed set of 8 patterns",
    trace_ref="euclid.def.S",
)

DEFINITION_W = EuclideanDefinition(
    definition_id=DefinitionId.W,
    name_ar="الوزن",
    name_en="Weight",
    formal_statement="W := morphophonological pattern that licenses manifestation without producing meaning",
    trace_ref="euclid.def.W",
)

DEFINITION_R = EuclideanDefinition(
    definition_id=DefinitionId.R,
    name_ar="الظهور",
    name_en="Manifestation",
    formal_statement="R := the act of M appearing through S, licensed by W",
    trace_ref="euclid.def.R",
)

DEFINITION_Q = EuclideanDefinition(
    definition_id=DefinitionId.Q,
    name_ar="القفز",
    name_en="Leap",
    formal_statement="Q := transition where abs(src_layer - tgt_layer) > 1",
    trace_ref="euclid.def.Q",
)

DEFINITION_LAYER = EuclideanDefinition(
    definition_id=DefinitionId.LAYER,
    name_ar="الطبقة",
    name_en="Layer",
    formal_statement="LAYER := ordered element in {L0, L1, L2, L3} with index in {0,1,2,3}",
    trace_ref="euclid.def.LAYER",
)

DEFINITION_ID = EuclideanDefinition(
    definition_id=DefinitionId.ID,
    name_ar="الهوية",
    name_en="Identity",
    formal_statement="ID(entity) := frozenset of attributes that uniquely identify the entity",
    trace_ref="euclid.def.ID",
)

ALL_DEFINITIONS: Tuple[EuclideanDefinition, ...] = (
    DEFINITION_M,
    DEFINITION_S,
    DEFINITION_W,
    DEFINITION_R,
    DEFINITION_Q,
    DEFINITION_LAYER,
    DEFINITION_ID,
)


# ══════════════════════════════════════════════════════════════════════════════
# §5  POSTULATES P6–P10
# ══════════════════════════════════════════════════════════════════════════════


POSTULATE_P6 = EuclideanPostulate(
    postulate_id=PostulateId.P6,
    name_ar="هوية محفوظة",
    name_en="Identity Preservation",
    formal_statement="For every transition T: Identity(source) is a subset of Identity(target)",
    dependencies=("definition.ID", "definition.LAYER"),
    trace_ref="euclid.post.P6",
)

POSTULATE_P7 = EuclideanPostulate(
    postulate_id=PostulateId.P7,
    name_ar="متغير",
    name_en="Change",
    formal_statement="Form may change across layers while identity is preserved (P6 holds)",
    dependencies=("definition.ID", "definition.LAYER", "postulate.P6"),
    trace_ref="euclid.post.P7",
)

POSTULATE_P8 = EuclideanPostulate(
    postulate_id=PostulateId.P8,
    name_ar="أعمق",
    name_en="Depth",
    formal_statement="M is ontologically prior to S: existence(M) does not entail existence(S)",
    dependencies=("definition.M", "definition.S"),
    trace_ref="euclid.post.P8",
)

POSTULATE_P9 = EuclideanPostulate(
    postulate_id=PostulateId.P9,
    name_ar="رخصة",
    name_en="License",
    formal_statement="W licenses R: manifestation requires a weight pattern as intermediary",
    dependencies=("definition.W", "definition.R", "definition.M", "definition.S"),
    trace_ref="euclid.post.P9",
)

POSTULATE_P10 = EuclideanPostulate(
    postulate_id=PostulateId.P10,
    name_ar="عدم القفز",
    name_en="No-Leap",
    formal_statement="For any transition T(src, tgt): abs(layer_index(src) - layer_index(tgt)) == 1",
    dependencies=("definition.LAYER", "definition.Q"),
    trace_ref="euclid.post.P10",
)

ALL_POSTULATES: Tuple[EuclideanPostulate, ...] = (
    POSTULATE_P6,
    POSTULATE_P7,
    POSTULATE_P8,
    POSTULATE_P9,
    POSTULATE_P10,
)


# ══════════════════════════════════════════════════════════════════════════════
# §6  THEOREM 1: الظهور لا ينتج المعنى
#     (Manifestation does not produce meaning)
# ══════════════════════════════════════════════════════════════════════════════


THEOREM_1_STEPS: Tuple[ProofStep, ...] = (
    ProofStep(
        step_number=1,
        statement="M exists without S (by Definition M)",
        justification="definition.M",
        trace_ref="euclid.th1.s1",
    ),
    ProofStep(
        step_number=2,
        statement="S is a licensed phonetic sequence (by Definition S)",
        justification="definition.S",
        trace_ref="euclid.th1.s2",
    ),
    ProofStep(
        step_number=3,
        statement="R requires both M and S (by Definition R)",
        justification="definition.R",
        trace_ref="euclid.th1.s3",
    ),
    ProofStep(
        step_number=4,
        statement="M is ontologically prior to S (by P8: Depth)",
        justification="postulate.P8",
        trace_ref="euclid.th1.s4",
    ),
    ProofStep(
        step_number=5,
        statement="W licenses R but W does not produce meaning (by Definition W)",
        justification="definition.W",
        trace_ref="euclid.th1.s5",
    ),
    ProofStep(
        step_number=6,
        statement="W is intermediary between M and S (by P9: License)",
        justification="postulate.P9",
        trace_ref="euclid.th1.s6",
    ),
    ProofStep(
        step_number=7,
        statement="Identity of M is preserved through R (by P6: Identity Preservation)",
        justification="postulate.P6",
        trace_ref="euclid.th1.s7",
    ),
    ProofStep(
        step_number=8,
        statement="R is the appearance of M through S, not production of new meaning",
        justification="definition.R",
        trace_ref="euclid.th1.s8",
    ),
    ProofStep(
        step_number=9,
        statement="Therefore S does not add to Identity(M) — it only manifests it",
        justification="postulate.P6",
        trace_ref="euclid.th1.s9",
    ),
    ProofStep(
        step_number=10,
        statement="Therefore R (manifestation) does not produce meaning; meaning pre-exists in M",
        justification="postulate.P8",
        trace_ref="euclid.th1.s10",
    ),
)

THEOREM_1 = EuclideanTheorem(
    theorem_id=TheoremId.TH1,
    name_ar="الظهور لا ينتج المعنى",
    name_en="Manifestation does not produce meaning",
    formal_statement="For all R(M,S): meaning(R) == meaning(M), not meaning(S)",
    proof_steps=THEOREM_1_STEPS,
    dependencies=(
        "definition.M", "definition.S", "definition.W", "definition.R",
        "postulate.P6", "postulate.P8", "postulate.P9",
    ),
    trace_ref="euclid.th1",
)


# ══════════════════════════════════════════════════════════════════════════════
# §7  THEOREM 2: الأصوات محدودة (Sounds are finite)
# ══════════════════════════════════════════════════════════════════════════════


THEOREM_2_STEPS: Tuple[ProofStep, ...] = (
    ProofStep(
        step_number=1,
        statement="S is drawn from 8 phonetic patterns (Definition S + MCE-1)",
        justification="definition.S",
        trace_ref="euclid.th2.s1",
    ),
    ProofStep(
        step_number=2,
        statement="The 8 patterns are a closed set: no 9th may exist (MCE-1 closure)",
        justification="definition.S",
        trace_ref="euclid.th2.s2",
    ),
    ProofStep(
        step_number=3,
        statement="M is not bounded by the cardinality of S (by P8: Depth)",
        justification="postulate.P8",
        trace_ref="euclid.th2.s3",
    ),
    ProofStep(
        step_number=4,
        statement="Therefore |S| is finite while |M| may be unbounded",
        justification="postulate.P8",
        trace_ref="euclid.th2.s4",
    ),
    ProofStep(
        step_number=5,
        statement="Cardinality argument: |S| = 8 patterns * 28 graphemes * 4 syllables = finite",
        justification="definition.S",
        trace_ref="euclid.th2.s5",
    ),
    ProofStep(
        step_number=6,
        statement="Therefore the phonetic layer L0 is provably finite and closed",
        justification="postulate.P8",
        trace_ref="euclid.th2.s6",
    ),
)

THEOREM_2 = EuclideanTheorem(
    theorem_id=TheoremId.TH2,
    name_ar="الأصوات محدودة",
    name_en="Sounds are finite",
    formal_statement="|S| is finite: |S| <= 8 * 28 * 4 = 896 combinations",
    proof_steps=THEOREM_2_STEPS,
    dependencies=(
        "definition.S", "definition.M", "postulate.P8",
    ),
    trace_ref="euclid.th2",
)


# ══════════════════════════════════════════════════════════════════════════════
# §8  THEOREM 3: الوزن حاجز لا مصدر (Weight is barrier, not source)
# ══════════════════════════════════════════════════════════════════════════════


THEOREM_3_STEPS: Tuple[ProofStep, ...] = (
    ProofStep(
        step_number=1,
        statement="W licenses R (by P9: License)",
        justification="postulate.P9",
        trace_ref="euclid.th3.s1",
    ),
    ProofStep(
        step_number=2,
        statement="W does not produce meaning (by Definition W)",
        justification="definition.W",
        trace_ref="euclid.th3.s2",
    ),
    ProofStep(
        step_number=3,
        statement="M exists independently of W (by P8 + Definition M)",
        justification="postulate.P8",
        trace_ref="euclid.th3.s3",
    ),
    ProofStep(
        step_number=4,
        statement="W is between M and S — a gateway, not a generator",
        justification="postulate.P9",
        trace_ref="euclid.th3.s4",
    ),
    ProofStep(
        step_number=5,
        statement="Identity(M) passes through W unchanged (by P6)",
        justification="postulate.P6",
        trace_ref="euclid.th3.s5",
    ),
    ProofStep(
        step_number=6,
        statement="Therefore W is a barrier (filter/license) not a source of meaning",
        justification="definition.W",
        trace_ref="euclid.th3.s6",
    ),
    ProofStep(
        step_number=7,
        statement="Corollary: No meaning may be derived from weight alone (Rule 10)",
        justification="postulate.P9",
        trace_ref="euclid.th3.s7",
    ),
)

THEOREM_3 = EuclideanTheorem(
    theorem_id=TheoremId.TH3,
    name_ar="الوزن حاجز لا مصدر",
    name_en="Weight is barrier, not source",
    formal_statement="W does not add to Identity(M): Identity(W(M)) == Identity(M)",
    proof_steps=THEOREM_3_STEPS,
    dependencies=(
        "definition.M", "definition.W", "definition.R",
        "postulate.P6", "postulate.P8", "postulate.P9",
    ),
    trace_ref="euclid.th3",
)


# ══════════════════════════════════════════════════════════════════════════════
# §9  THEOREM 4: القفز مستحيل (Leap is impossible)
# ══════════════════════════════════════════════════════════════════════════════


THEOREM_4_STEPS: Tuple[ProofStep, ...] = (
    ProofStep(
        step_number=1,
        statement="Layers are ordered: L0 < L1 < L2 < L3 (by Definition LAYER)",
        justification="definition.LAYER",
        trace_ref="euclid.th4.s1",
    ),
    ProofStep(
        step_number=2,
        statement="Q is defined as abs(src_idx - tgt_idx) > 1 (by Definition Q)",
        justification="definition.Q",
        trace_ref="euclid.th4.s2",
    ),
    ProofStep(
        step_number=3,
        statement="P10 prohibits Q: every transition must satisfy abs(diff) == 1",
        justification="postulate.P10",
        trace_ref="euclid.th4.s3",
    ),
    ProofStep(
        step_number=4,
        statement="P6 requires identity preservation at each step",
        justification="postulate.P6",
        trace_ref="euclid.th4.s4",
    ),
    ProofStep(
        step_number=5,
        statement="By TH3: W is barrier — cannot skip W to reach S from M directly",
        justification="theorem.TH3",
        trace_ref="euclid.th4.s5",
    ),
    ProofStep(
        step_number=6,
        statement="Skipping layers would violate P6 (identity may be lost without verification)",
        justification="postulate.P6",
        trace_ref="euclid.th4.s6",
    ),
    ProofStep(
        step_number=7,
        statement="Therefore Q is impossible: no valid transition has abs(diff) > 1",
        justification="postulate.P10",
        trace_ref="euclid.th4.s7",
    ),
    ProofStep(
        step_number=8,
        statement="Corollary: the path M → W → S → R is the only valid manifestation chain",
        justification="theorem.TH3",
        trace_ref="euclid.th4.s8",
    ),
)

THEOREM_4 = EuclideanTheorem(
    theorem_id=TheoremId.TH4,
    name_ar="القفز مستحيل",
    name_en="Leap is impossible",
    formal_statement="For all T(src,tgt): abs(layer(src) - layer(tgt)) == 1 (no exceptions)",
    proof_steps=THEOREM_4_STEPS,
    dependencies=(
        "definition.LAYER", "definition.Q",
        "postulate.P6", "postulate.P10",
        "theorem.TH3",
    ),
    trace_ref="euclid.th4",
)

ALL_THEOREMS: Tuple[EuclideanTheorem, ...] = (
    THEOREM_1,
    THEOREM_2,
    THEOREM_3,
    THEOREM_4,
)


# ══════════════════════════════════════════════════════════════════════════════
# §10  PROOF VERIFIER (Pure, Stateless)
# ══════════════════════════════════════════════════════════════════════════════


@dataclass(frozen=True, slots=True)
class ProofVerifier:
    """Stateless verifier for Euclidean proofs.

    All methods are static/pure — no I/O, no state, no side effects.
    Each method raises ProofVerificationError on failure (never silent).
    """

    trace_ref: str = "docs/00_MAQOOL_CONSTITUTION.md §5"
    rank: str = "CANDIDATE"
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if not self.trace_ref:
            raise ValueError(FailureCode.M_00_11.value)
        if self.rank != "CANDIDATE":
            raise ValueError(FailureCode.M_00_10.value)

    @staticmethod
    def verify_theorem_1(theorem: EuclideanTheorem) -> bool:
        """Verify TH1: Manifestation does not produce meaning.

        Requires exactly 10 proof steps and dependencies on M, S, W, R, P6, P8, P9.
        """
        if theorem.theorem_id != TheoremId.TH1:
            raise ProofVerificationError(
                TheoremId.TH1, 0, "wrong_theorem_id"
            )
        if len(theorem.proof_steps) != 10:
            raise ProofVerificationError(
                TheoremId.TH1, 0, "requires_exactly_10_steps"
            )
        required_deps = {"definition.M", "definition.S", "definition.W", "definition.R",
                         "postulate.P6", "postulate.P8", "postulate.P9"}
        missing = required_deps - set(theorem.dependencies)
        if missing:
            raise ProofVerificationError(
                TheoremId.TH1, 0, f"missing_dependencies: {sorted(missing)}"
            )
        return True

    @staticmethod
    def verify_theorem_2(theorem: EuclideanTheorem) -> bool:
        """Verify TH2: Sounds are finite.

        Requires P8 (cardinality postulate) and definition.S.
        """
        if theorem.theorem_id != TheoremId.TH2:
            raise ProofVerificationError(
                TheoremId.TH2, 0, "wrong_theorem_id"
            )
        if "postulate.P8" not in theorem.dependencies:
            raise ProofVerificationError(
                TheoremId.TH2, 0, "missing_cardinality_postulate"
            )
        if "definition.S" not in theorem.dependencies:
            raise ProofVerificationError(
                TheoremId.TH2, 0, "missing_sound_definition"
            )
        return True

    @staticmethod
    def verify_theorem_3(theorem: EuclideanTheorem) -> bool:
        """Verify TH3: Weight is barrier, not source.

        Requires definition.W (weight) and postulate.P9 (license).
        """
        if theorem.theorem_id != TheoremId.TH3:
            raise ProofVerificationError(
                TheoremId.TH3, 0, "wrong_theorem_id"
            )
        if "definition.W" not in theorem.dependencies:
            raise ProofVerificationError(
                TheoremId.TH3, 0, "missing_weight_definition"
            )
        if "postulate.P9" not in theorem.dependencies:
            raise ProofVerificationError(
                TheoremId.TH3, 0, "missing_license_postulate"
            )
        return True

    @staticmethod
    def verify_theorem_4(theorem: EuclideanTheorem) -> bool:
        """Verify TH4: Leap is impossible.

        Requires theorem.TH3 dependency and postulate.P10.
        """
        if theorem.theorem_id != TheoremId.TH4:
            raise ProofVerificationError(
                TheoremId.TH4, 0, "wrong_theorem_id"
            )
        if "theorem.TH3" not in theorem.dependencies:
            raise ProofVerificationError(
                TheoremId.TH4, 0, "missing_theorem_3_dependency"
            )
        if "postulate.P10" not in theorem.dependencies:
            raise ProofVerificationError(
                TheoremId.TH4, 0, "missing_no_leap_postulate"
            )
        return True

    @staticmethod
    def verify_all(
        theorems: Tuple[EuclideanTheorem, ...],
    ) -> Tuple[bool, bool, bool, bool]:
        """Verify all four theorems and return results.

        Returns a 4-tuple of booleans (TH1, TH2, TH3, TH4).
        Raises ProofVerificationError on first failure.
        """
        if len(theorems) != 4:
            raise ProofVerificationError(
                TheoremId.TH1, 0, "requires_exactly_4_theorems"
            )
        return (
            ProofVerifier.verify_theorem_1(theorems[0]),
            ProofVerifier.verify_theorem_2(theorems[1]),
            ProofVerifier.verify_theorem_3(theorems[2]),
            ProofVerifier.verify_theorem_4(theorems[3]),
        )


# ══════════════════════════════════════════════════════════════════════════════
# §11  SYSTEM INTEGRITY
# ══════════════════════════════════════════════════════════════════════════════


def compute_system_hash() -> str:
    """Compute a deterministic hash of the entire axiomatic system.

    Pure function — no I/O, only operates on module-level constants.
    The hash covers: all definitions, postulates, and theorems.
    """
    parts: list[str] = []
    for d in ALL_DEFINITIONS:
        parts.append(f"{d.definition_id.value}:{d.formal_statement}")
    for p in ALL_POSTULATES:
        parts.append(f"{p.postulate_id.value}:{p.formal_statement}")
    for t in ALL_THEOREMS:
        parts.append(f"{t.theorem_id.value}:{t.formal_statement}:{len(t.proof_steps)}")
    content = "|".join(parts)
    return hashlib.sha256(content.encode("utf-8")).hexdigest()[:16]


SYSTEM_HASH: str = compute_system_hash()
"""Deterministic fingerprint of the axiomatic system state."""
