"""
HarfMaani — Arabic particles (حروف المعاني).
Origin: docs/00_MAQOOL_CONSTITUTION.md; docs/01_L0_PHONETIC_BOUNDARY.md BL-L0-07
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import FrozenSet, Tuple

from taaqqul_slot_geometry.constitution.failure_taxonomy import FailureCode


@dataclass(frozen=True)
class HarfMaani:
    """A constitutionally-licensed Arabic particle.

    Most particles are built on sukun (BL-L0-07).  This is a PHONOLOGICAL
    fact — not a semantic one.  Particles do not carry meaning in L0.

    Parameters
    ----------
    name : str
        The romanised name of the particle (e.g. ``"wa"``).
    arabic_form : str
        The Arabic Unicode form (e.g. ``"وَ"``).
    phonetic_form : str
        The phonetic transcription (must be non-empty).
    function : str
        The grammatical function label (must be non-empty).
    is_built_on_sukun : bool
        ``True`` for most particles.
    trace_ref : str
        Constitutional reference.
    rank : str
        Always ``"CANDIDATE"``.
    residuals : FrozenSet[str]
        Residual bundle.
    """

    name: str
    arabic_form: str
    phonetic_form: str
    function: str
    is_built_on_sukun: bool = True
    domain_tag: str = "L0_PARTICLE"
    trace_ref: str = "docs/01_L0_PHONETIC_BOUNDARY.md BL-L0-07"
    rank: str = "CANDIDATE"
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if not self.phonetic_form:
            raise ValueError(FailureCode.M_00_25.value)
        if not self.function:
            raise ValueError(FailureCode.M_00_08.value)
        if not self.trace_ref:
            raise ValueError(FailureCode.M_00_11.value)
        if self.rank != "CANDIDATE":
            raise ValueError(FailureCode.M_00_10.value)


# ── Canonical particle table ─────────────────────────────────────────────────

HARF_MAANI_TABLE: Tuple[HarfMaani, ...] = (
    HarfMaani("wa",  "وَ",  "wa",   "conjunction",         is_built_on_sukun=False),
    HarfMaani("fa",  "فَ",  "fa",   "sequential_conj",     is_built_on_sukun=False),
    HarfMaani("bi",  "بِ",  "bi",   "preposition_by_with", is_built_on_sukun=False),
    HarfMaani("li",  "لِ",  "li",   "preposition_for",     is_built_on_sukun=False),
    HarfMaani("hal", "هَلْ", "hal",  "interrogative",       is_built_on_sukun=True),
    HarfMaani("qad", "قَدْ", "qad",  "emphasis_perfectivity",is_built_on_sukun=True),
    HarfMaani("min", "مِنْ", "min",  "preposition_from",    is_built_on_sukun=True),
    HarfMaani("an",  "عَنْ", "ʕan",  "preposition_about",   is_built_on_sukun=True),
    HarfMaani("ila", "إِلَى","ʔila", "preposition_to",      is_built_on_sukun=False),
    HarfMaani("ala", "عَلَى","ʕala", "preposition_on_upon", is_built_on_sukun=False),
    HarfMaani("fi",  "فِي", "fiː",  "preposition_in",      is_built_on_sukun=False),
    HarfMaani("lam", "لَمْ", "lam",  "negation_past",       is_built_on_sukun=True),
    HarfMaani("lan", "لَنْ", "lan",  "negation_future",     is_built_on_sukun=True),
    HarfMaani("la",  "لَا", "laː",  "negation_present",    is_built_on_sukun=False),
    HarfMaani("in",  "إِنْ", "ʔin",  "conditional",         is_built_on_sukun=True),
    HarfMaani("inna","إِنَّ","ʔinna","emphasis_nominal",    is_built_on_sukun=False),
    HarfMaani("ka",  "كَ",  "ka",   "preposition_like_as", is_built_on_sukun=False),
    HarfMaani("aw",  "أَوْ", "ʔaw",  "disjunction_or",      is_built_on_sukun=True),
    HarfMaani("am",  "أَمْ", "ʔam",  "interrogative_or",    is_built_on_sukun=True),
    HarfMaani("bal", "بَلْ", "bal",  "contrast_but_rather", is_built_on_sukun=True),
)

HARF_MAANI_BY_NAME: dict[str, HarfMaani] = {h.name: h for h in HARF_MAANI_TABLE}


def get_harf(name: str) -> HarfMaani:
    """Pure lookup: return the canonical ``HarfMaani`` for ``name``.

    Raises
    ------
    ValueError
        With ``FailureCode.M_00_08`` if the name is not recognised.
    """
    try:
        return HARF_MAANI_BY_NAME[name]
    except KeyError:
        raise ValueError(
            f"{FailureCode.M_00_08.value}: particle {name!r} not recognised"
        )
