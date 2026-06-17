"""
TransitionRegistry — Licensed transition laws between digital Arabic layers.

Every transition from one layer to the next requires:
- Carrier exists
- Domain declared
- Identity preserved
- Operator licensed
- Condition holds
- Cause exists
- NOT preventer
- Residuals declared

Origin: docs/00_MAQOOL_CONSTITUTION.md §5 Rule 8 (No-Leap Axiom)
trace_ref: docs/59_ARABIC_DIGITAL_IDENTITY_LAW.md §TransitionRegistry
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import FrozenSet, Tuple

from taaqqul_slot_geometry.constitution.failure_taxonomy import FailureCode


class TransitionLayer(str, Enum):
    """Layers in the Arabic digital identity chain.

    Origin: docs/59_ARABIC_DIGITAL_IDENTITY_LAW.md §TransitionRegistry
    """

    UNICODE = "unicode"
    GLYPH = "glyph"
    LETTER = "letter"
    MARK = "mark"
    VOCALIZED_UNIT = "vocalized_unit"
    SYLLABLE = "syllable"
    LAFZ = "lafz"
    MUFRAD = "mufrad"


class TransitionVerdict(str, Enum):
    """Outcome of a transition attempt.

    Origin: docs/59_ARABIC_DIGITAL_IDENTITY_LAW.md §TransitionRegistry
    """

    LICENSED = "licensed"
    BLOCKED = "blocked"
    DEFERRED = "deferred"
    RESIDUAL = "residual"


@dataclass(frozen=True)
class TransitionLaw:
    """A single licensed transition law between two adjacent layers.

    Each law defines what conditions must hold for the transition to be licensed,
    and what happens if conditions fail.

    Parameters
    ----------
    law_id : str
        Canonical identifier (e.g. "LETTER_HARAKA_LINK").
    source_layer : TransitionLayer
        The layer being transitioned from.
    target_layer : TransitionLayer
        The layer being transitioned to.
    description : str
        Human-readable description of the transition.
    carrier_requirement : str
        What carrier must exist.
    domain_requirement : str
        What domain must be declared.
    identity_preservation : str
        How identity is preserved across transition.
    condition : str
        What condition must hold.
    cause : str
        Why this transition exists.
    preventers : FrozenSet[str]
        What can block this transition.
    output_on_success : str
        What is produced on successful transition.
    output_on_failure : TransitionVerdict
        What happens when transition fails.
    trace_ref : str
        Constitutional reference.
    rank : str
        Always "CANDIDATE".
    residuals : FrozenSet[str]
        Residual bundle.
    """

    law_id: str
    source_layer: TransitionLayer
    target_layer: TransitionLayer
    description: str
    carrier_requirement: str
    domain_requirement: str
    identity_preservation: str
    condition: str
    cause: str
    preventers: FrozenSet[str]
    output_on_success: str
    output_on_failure: TransitionVerdict
    trace_ref: str = "docs/59_ARABIC_DIGITAL_IDENTITY_LAW.md §TransitionRegistry"
    rank: str = "CANDIDATE"
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if not self.law_id:
            raise ValueError(
                f"{FailureCode.M_CX_02.value}: law_id cannot be empty"
            )
        if not isinstance(self.source_layer, TransitionLayer):
            raise ValueError(
                f"{FailureCode.M_CX_02.value}: source_layer must be TransitionLayer"
            )
        if not isinstance(self.target_layer, TransitionLayer):
            raise ValueError(
                f"{FailureCode.M_CX_02.value}: target_layer must be TransitionLayer"
            )
        if not self.trace_ref:
            raise ValueError(FailureCode.M_00_11.value)
        if self.rank != "CANDIDATE":
            raise ValueError(FailureCode.M_00_10.value)


# ── Canonical transition laws ─────────────────────────────────────────────────

TRANSITION_REGISTRY: Tuple[TransitionLaw, ...] = (
    TransitionLaw(
        law_id="UNICODE_TO_GLYPH",
        source_layer=TransitionLayer.UNICODE,
        target_layer=TransitionLayer.GLYPH,
        description="Unicode codepoint resolves to a glyph candidate",
        carrier_requirement="valid Unicode codepoint in Arabic block",
        domain_requirement="Unicode Arabic script",
        identity_preservation="codepoint identity maps to exactly one glyph",
        condition="codepoint is assigned and not deprecated",
        cause="digital reference requires visual manifestation",
        preventers=frozenset({"unassigned_codepoint", "deprecated_codepoint"}),
        output_on_success="glyph_candidate",
        output_on_failure=TransitionVerdict.BLOCKED,
    ),
    TransitionLaw(
        law_id="GLYPH_TO_LETTER",
        source_layer=TransitionLayer.GLYPH,
        target_layer=TransitionLayer.LETTER,
        description="Glyph identified as an Arabic letter with preserved identity",
        carrier_requirement="glyph in Arabic letter range",
        domain_requirement="Arabic orthographic system",
        identity_preservation="glyph→letter_id is a bijection for the 28",
        condition="glyph belongs to the 28 Arabic letter set",
        cause="orthographic identity must be established before operation",
        preventers=frozenset({"non_arabic_glyph", "combining_mark_only"}),
        output_on_success="letter_identity",
        output_on_failure=TransitionVerdict.BLOCKED,
    ),
    TransitionLaw(
        law_id="GLYPH_TO_MARK",
        source_layer=TransitionLayer.GLYPH,
        target_layer=TransitionLayer.MARK,
        description="Glyph identified as a diacritical mark (haraka/sukun/shadda)",
        carrier_requirement="glyph in Arabic mark range",
        domain_requirement="Arabic diacritical system",
        identity_preservation="glyph→mark_id preserves operator identity",
        condition="glyph belongs to Arabic combining marks",
        cause="operator identity must be established before attachment",
        preventers=frozenset({"non_arabic_mark", "standalone_mark_without_base"}),
        output_on_success="mark_identity",
        output_on_failure=TransitionVerdict.BLOCKED,
    ),
    TransitionLaw(
        law_id="LETTER_HARAKA_LINK",
        source_layer=TransitionLayer.LETTER,
        target_layer=TransitionLayer.VOCALIZED_UNIT,
        description="Letter + haraka produces a licensed vocalized unit (CV)",
        carrier_requirement="letter with letter_id established",
        domain_requirement="Arabic vocalization domain",
        identity_preservation="letter_id preserved; haraka operates, does not consume",
        condition="letter accepts haraka AND no contradictory mark exists",
        cause="formation of minimal phonological unit (CV)",
        preventers=frozenset({
            "letter_does_not_accept_haraka",
            "conflicting_short_vowel",
            "sukun_blocks_haraka",
        }),
        output_on_success="vocalized_unit_CV",
        output_on_failure=TransitionVerdict.RESIDUAL,
    ),
    TransitionLaw(
        law_id="LETTER_SUKUN_LINK",
        source_layer=TransitionLayer.LETTER,
        target_layer=TransitionLayer.VOCALIZED_UNIT,
        description="Letter + sukun produces a closed consonant unit",
        carrier_requirement="letter with letter_id established",
        domain_requirement="Arabic vocalization domain",
        identity_preservation="letter_id preserved; sukun closes without erasing",
        condition="letter accepts sukun AND no conflicting vowel",
        cause="consonant closure for syllable coda",
        preventers=frozenset({
            "conflicting_short_vowel",
            "shadda_without_resolution",
        }),
        output_on_success="closed_consonant_C",
        output_on_failure=TransitionVerdict.RESIDUAL,
    ),
    TransitionLaw(
        law_id="LETTER_SHADDA_LINK",
        source_layer=TransitionLayer.LETTER,
        target_layer=TransitionLayer.VOCALIZED_UNIT,
        description="Letter + shadda produces a geminated unit (requires follow-up)",
        carrier_requirement="letter with letter_id established",
        domain_requirement="Arabic vocalization domain",
        identity_preservation="letter_id preserved; shadda doubles function, not identity",
        condition="letter accepts shadda",
        cause="morphological/phonological gemination",
        preventers=frozenset({"letter_does_not_accept_shadda"}),
        output_on_success="geminated_unit_pending_vowel",
        output_on_failure=TransitionVerdict.BLOCKED,
    ),
    TransitionLaw(
        law_id="VOCALIZED_UNIT_TO_SYLLABLE",
        source_layer=TransitionLayer.VOCALIZED_UNIT,
        target_layer=TransitionLayer.SYLLABLE,
        description="Vocalized unit(s) compose into a syllable with recognized pattern",
        carrier_requirement="one or more vocalized units",
        domain_requirement="Arabic syllable structure",
        identity_preservation="all letter_ids preserved in syllable",
        condition="unit sequence matches CV/CVC/CVV/CVCC pattern",
        cause="syllable is minimal prosodic unit",
        preventers=frozenset({
            "no_nucleus_vowel",
            "pattern_unrecognized",
            "isolated_consonant_without_context",
        }),
        output_on_success="syllable_candidate",
        output_on_failure=TransitionVerdict.DEFERRED,
    ),
    TransitionLaw(
        law_id="SYLLABLE_TO_LAFZ",
        source_layer=TransitionLayer.SYLLABLE,
        target_layer=TransitionLayer.LAFZ,
        description="Syllable chain forms a lafz (utterance candidate)",
        carrier_requirement="one or more licensed syllables",
        domain_requirement="Arabic phonological word",
        identity_preservation="syllable sequence preserved in order",
        condition="syllable chain forms a prosodically valid sequence",
        cause="lafz is the minimal independently pronounceable unit",
        preventers=frozenset({
            "isolated_syllable_fragment",
            "boundary_violation",
        }),
        output_on_success="lafz_candidate",
        output_on_failure=TransitionVerdict.DEFERRED,
    ),
    TransitionLaw(
        law_id="LAFZ_TO_MUFRAD",
        source_layer=TransitionLayer.LAFZ,
        target_layer=TransitionLayer.MUFRAD,
        description="Lafz classified into word path (noun/verb/particle/proper/etc.)",
        carrier_requirement="closed lafz with all syllables licensed",
        domain_requirement="Arabic lexical classification",
        identity_preservation="lafz identity preserved under classification",
        condition="lafz permits at least one word-path classification",
        cause="word must be classified before entering syntax",
        preventers=frozenset({
            "unresolved_harakat",
            "ambiguous_root",
            "no_valid_path",
        }),
        output_on_success="mufrad_candidate: ism/fiil/harf/mabni/alam/manqul/dakhil",
        output_on_failure=TransitionVerdict.DEFERRED,
        residuals=frozenset({"classification_may_require_context"}),
    ),
)


# ── Index map ─────────────────────────────────────────────────────────────────

TRANSITION_BY_ID: dict[str, TransitionLaw] = {
    t.law_id: t for t in TRANSITION_REGISTRY
}


def get_transition_law(law_id: str) -> TransitionLaw:
    """Pure lookup: return TransitionLaw by canonical ID.

    Raises
    ------
    ValueError
        With FailureCode.M_CX_02 if law_id is not found.
    """
    try:
        return TRANSITION_BY_ID[law_id]
    except KeyError:
        raise ValueError(
            f"{FailureCode.M_CX_02.value}: transition law {law_id!r} not in registry"
        )


def check_transition_licensed(
    law_id: str,
    carrier_exists: bool,
    domain_declared: bool,
    identity_preserved: bool,
    condition_holds: bool,
    cause_exists: bool,
    preventer_active: bool,
) -> TransitionVerdict:
    """Pure function: evaluate whether a transition is licensed.

    This implements the universal transition rule:
        IF carrier AND domain AND identity AND condition AND cause AND NOT preventer
        THEN licensed
        ELSE verdict from the law's output_on_failure

    Parameters
    ----------
    law_id : str
        Which transition law to evaluate.
    carrier_exists : bool
        Whether the carrier is present.
    domain_declared : bool
        Whether the domain is declared.
    identity_preserved : bool
        Whether identity is preserved.
    condition_holds : bool
        Whether the transition condition holds.
    cause_exists : bool
        Whether the cause for transition exists.
    preventer_active : bool
        Whether a preventer is blocking.

    Returns
    -------
    TransitionVerdict
        LICENSED if all conditions met, else the law's failure verdict.
    """
    law = get_transition_law(law_id)

    if (
        carrier_exists
        and domain_declared
        and identity_preserved
        and condition_holds
        and cause_exists
        and not preventer_active
    ):
        return TransitionVerdict.LICENSED

    return law.output_on_failure
