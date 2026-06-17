"""
LafzClosure — close a syllable chain into a LafzCandidate.

Takes the output of the Syllabifier and produces a LafzCandidate:
a phonetically/orthographically closed utterance that is ready
to enter the next layer (Mufrad classification).

This module operates ONLY at the L0 level:
- It validates that the syllable chain forms a valid lafz
- It checks the SYLLABLE_TO_LAFZ transition
- It does NOT say anything about word class, root, weight, or meaning

Origin: docs/59_ARABIC_DIGITAL_IDENTITY_LAW.md §LafzClosure
trace_ref: docs/59_ARABIC_DIGITAL_IDENTITY_LAW.md §LafzClosure
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import FrozenSet, Tuple

from taaqqul_slot_geometry.constitution.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.core.transition_registry import (
    TransitionVerdict,
    check_transition_licensed,
)
from taaqqul_slot_geometry.core.syllabifier import SyllabificationResult
from taaqqul_slot_geometry.L0.syllable import Syllable, SyllableType


@dataclass(frozen=True)
class LafzCandidate:
    """A phonetically/orthographically closed utterance (lafz).

    This is the final product of L0: a lafz that has been validated
    through the full pipeline Unicode→Letter/Mark→VocalizedUnit→Syllable→Lafz.

    It carries NO morphological information — only phonetic/orthographic identity.

    Parameters
    ----------
    syllables : Tuple[Syllable, ...]
        The ordered syllable sequence.
    syllable_pattern : str
        Human-readable syllable pattern (e.g. "CV-CV-CV").
    identity_preserved : bool
        Whether all letter identities are preserved throughout.
    lafz_closed : bool
        Whether the lafz is phonetically/orthographically closed.
    transition_verdict : TransitionVerdict
        Whether the SYLLABLE_TO_LAFZ transition was licensed.
    trace_ref : str
        Constitutional reference.
    rank : str
        Always "CANDIDATE".
    residuals : FrozenSet[str]
        Residual bundle.
    """

    syllables: Tuple[Syllable, ...]
    syllable_pattern: str
    identity_preserved: bool
    lafz_closed: bool
    transition_verdict: TransitionVerdict
    trace_ref: str = "docs/59_ARABIC_DIGITAL_IDENTITY_LAW.md §LafzClosure"
    rank: str = "CANDIDATE"
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if not self.syllables:
            raise ValueError(FailureCode.M_00_06.value)
        if not self.trace_ref:
            raise ValueError(FailureCode.M_00_11.value)
        if self.rank != "CANDIDATE":
            raise ValueError(FailureCode.M_00_10.value)


def close_lafz(syllabification: SyllabificationResult) -> LafzCandidate:
    """Close a syllable chain into a LafzCandidate (pure function).

    This function validates:
    1. The syllable sequence is non-empty
    2. All syllable transitions were licensed
    3. The SYLLABLE_TO_LAFZ transition is licensed
    4. Identity is preserved throughout

    It does NOT:
    - Determine word class (noun/verb/particle)
    - Extract root or weight
    - Assign any morphological properties
    - Produce meaning

    Parameters
    ----------
    syllabification : SyllabificationResult
        Output from syllabify().

    Returns
    -------
    LafzCandidate
        The closed lafz, ready for L1 (Mufrad classification).
    """
    syllables = syllabification.syllables
    syllable_types = syllabification.syllable_types

    # Build the syllable pattern string
    syllable_pattern = "-".join(st.value for st in syllable_types)

    # Check identity preservation: all units maintained their letter_id
    identity_preserved = syllabification.transition_verdict == TransitionVerdict.LICENSED

    # Check if there are any blocking residuals
    blocking_residuals = frozenset({
        r for r in syllabification.residuals
        if r in ("missing_harakat", "isolated_sukun_unit", "syllabification_fallback")
    })

    # A lafz is closed if:
    # 1. There are syllables
    # 2. No blocking residuals (fully vocalized, no fallbacks)
    # 3. Syllabification was licensed
    lafz_closed = (
        len(syllables) > 0
        and not blocking_residuals
        and syllabification.transition_verdict == TransitionVerdict.LICENSED
    )

    # Check the SYLLABLE_TO_LAFZ transition
    verdict = check_transition_licensed(
        law_id="SYLLABLE_TO_LAFZ",
        carrier_exists=len(syllables) > 0,
        domain_declared=True,
        identity_preserved=identity_preserved,
        operator_licensed=True,
        condition_holds=lafz_closed,
        cause_exists=True,
        preventer_active=not lafz_closed,
    )

    # Collect all residuals from syllabification
    all_residuals = set(syllabification.residuals)

    # Filter out L0-internal residuals that don't propagate
    propagating_residuals = frozenset({
        r for r in all_residuals
        if r in (
            "tanwin_requires_word_layer",
            "hamzat_wasl_requires_domain_license",
            "alif_seat_requires_domain_license",
            "ta_marbuta_requires_word_layer",
            "missing_harakat",
        )
    })

    return LafzCandidate(
        syllables=syllables,
        syllable_pattern=syllable_pattern,
        identity_preserved=identity_preserved,
        lafz_closed=lafz_closed,
        transition_verdict=verdict,
        residuals=propagating_residuals,
    )
