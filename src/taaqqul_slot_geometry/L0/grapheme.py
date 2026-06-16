"""
Grapheme — 28 Arabic letters, each with articulation point and manner.
Origin: docs/00_MAQOOL_CONSTITUTION.md §2 (Category 2: Grapheme); docs/01_L0_PHONETIC_BOUNDARY.md BL-L0-03
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import FrozenSet, Tuple

from taaqqul_slot_geometry.constitution.failure_taxonomy import FailureCode

# Closed set of 28 Arabic letter symbols (romanised/IPA keys)
_ARABIC_28: FrozenSet[str] = frozenset(
    {
        "ʔ",  # ء  hamza
        "b",  # ب  ba
        "t",  # ت  ta
        "θ",  # ث  tha
        "dʒ", # ج  jeem
        "ħ",  # ح  ha (pharyngeal)
        "x",  # خ  kha
        "d",  # د  dal
        "ð",  # ذ  dhal
        "r",  # ر  ra
        "z",  # ز  zay
        "s",  # س  seen
        "ʃ",  # ش  sheen
        "sˤ", # ص  saad
        "dˤ", # ض  daad
        "tˤ", # ط  taa (emphatic)
        "ðˤ", # ظ  dhaa (emphatic)
        "ʕ",  # ع  ain
        "ɣ",  # غ  ghain
        "f",  # ف  fa
        "q",  # ق  qaf
        "k",  # ك  kaf
        "l",  # ل  lam
        "m",  # م  meem
        "n",  # ن  nun
        "h",  # ه  ha (glottal)
        "w",  # و  waw
        "j",  # ي  ya
    }
)

# Articulation points (makhaarij)
ARTICULATION_POINTS: FrozenSet[str] = frozenset(
    {
        "jauf",        # الجوف — empty cavity
        "halq_aqsa",   # أقصى الحلق — deepest throat
        "halq_wasat",  # وسط الحلق — middle throat
        "halq_adna",   # أدنى الحلق — nearest throat
        "lisan_aqsa",  # أقصى اللسان — back of tongue
        "lisan_wasat", # وسط اللسان — middle of tongue
        "lisan_hadda", # حافة اللسان — edge of tongue
        "lisan_tarif", # طرف اللسان — tip of tongue
        "lisan_shamm", # اللثة — gum
        "shafataan",   # الشفتان — both lips
        "shafa_ulya",  # الشفة العليا — upper lip
    }
)

# Articulation manners (sifaat)
ARTICULATION_MANNERS: FrozenSet[str] = frozenset(
    {
        "jahr",      # جهر — voiced
        "hams",      # همس — voiceless
        "shidda",    # شدة — plosive
        "tawassut",  # توسط — intermediate
        "rakhawa",   # رخاوة — fricative
        "isti_la",   # استعلاء — elevation
        "infitah",   # انفتاح — opening
        "izlaq",     # إذلاق — fluency
        "ikhfa",     # إخفاء — nasalisation
        "qalqala",   # قلقلة — echo
    }
)


@dataclass(frozen=True)
class Grapheme:
    """A single Arabic letter with its phonological properties.

    Parameters
    ----------
    symbol : str
        IPA/romanised symbol; must be one of the 28 letters.
    arabic_letter : str
        The Unicode Arabic character (e.g. ``"ب"``).
    articulation_point : str
        One of the recognised makhaarij.
    articulation_manner : str
        One or more sifaat (comma-separated string).
    phoneme_symbol : str
        The IPA or romanised phoneme symbol (often same as ``symbol``).
    trace_ref : str
        Constitutional reference.
    rank : str
        Always ``"CANDIDATE"``.
    residuals : FrozenSet[str]
        Residual bundle.
    """

    symbol: str
    arabic_letter: str
    articulation_point: str
    articulation_manner: str
    phoneme_symbol: str
    domain_tag: str = "L0_GRAPHEMICS"
    trace_ref: str = "docs/00_MAQOOL_CONSTITUTION.md §2 Category 2 (Grapheme)"
    rank: str = "CANDIDATE"
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if self.symbol not in _ARABIC_28:
            raise ValueError(
                f"{FailureCode.M_00_03.value}: symbol {self.symbol!r} not in the 28 Arabic graphemes"
            )
        if not self.articulation_point:
            raise ValueError(FailureCode.M_00_03.value)
        if not self.trace_ref:
            raise ValueError(FailureCode.M_00_11.value)
        if self.rank != "CANDIDATE":
            raise ValueError(FailureCode.M_00_10.value)


# ── Canonical 28 graphemes ────────────────────────────────────────────────────

GRAPHEME_TABLE: Tuple[Grapheme, ...] = (
    Grapheme("ʔ",  "ء", "halq_aqsa",   "hams,shidda",         "ʔ"),
    Grapheme("b",  "ب", "shafataan",   "jahr,shidda",         "b"),
    Grapheme("t",  "ت", "lisan_tarif", "hams,shidda",         "t"),
    Grapheme("θ",  "ث", "lisan_tarif", "hams,rakhawa",        "θ"),
    Grapheme("dʒ","ج", "lisan_wasat", "jahr,shidda",         "dʒ"),
    Grapheme("ħ",  "ح", "halq_wasat",  "hams,rakhawa",        "ħ"),
    Grapheme("x",  "خ", "halq_aqsa",   "hams,rakhawa,isti_la","x"),
    Grapheme("d",  "د", "lisan_tarif", "jahr,shidda,qalqala", "d"),
    Grapheme("ð",  "ذ", "lisan_tarif", "jahr,rakhawa",        "ð"),
    Grapheme("r",  "ر", "lisan_tarif", "jahr,tawassut,izlaq", "r"),
    Grapheme("z",  "ز", "lisan_tarif", "jahr,rakhawa",        "z"),
    Grapheme("s",  "س", "lisan_tarif", "hams,rakhawa",        "s"),
    Grapheme("ʃ",  "ش", "lisan_wasat", "hams,rakhawa",        "ʃ"),
    Grapheme("sˤ", "ص", "lisan_tarif", "hams,rakhawa,isti_la","sˤ"),
    Grapheme("dˤ", "ض", "lisan_hadda", "jahr,rakhawa,isti_la","dˤ"),
    Grapheme("tˤ", "ط", "lisan_tarif", "jahr,shidda,isti_la,qalqala","tˤ"),
    Grapheme("ðˤ", "ظ", "lisan_tarif", "jahr,rakhawa,isti_la","ðˤ"),
    Grapheme("ʕ",  "ع", "halq_wasat",  "jahr,tawassut",       "ʕ"),
    Grapheme("ɣ",  "غ", "halq_aqsa",   "jahr,rakhawa,isti_la","ɣ"),
    Grapheme("f",  "ف", "shafa_ulya",  "hams,rakhawa",        "f"),
    Grapheme("q",  "ق", "lisan_aqsa",  "jahr,shidda,isti_la,qalqala","q"),
    Grapheme("k",  "ك", "lisan_aqsa",  "hams,shidda",         "k"),
    Grapheme("l",  "ل", "lisan_tarif", "jahr,tawassut,izlaq", "l"),
    Grapheme("m",  "م", "shafataan",   "jahr,tawassut,ikhfa,izlaq","m"),
    Grapheme("n",  "ن", "lisan_tarif", "jahr,tawassut,ikhfa,izlaq","n"),
    Grapheme("h",  "ه", "jauf",        "hams,rakhawa",        "h"),
    Grapheme("w",  "و", "shafataan",   "jahr,rakhawa",        "w"),
    Grapheme("j",  "ي", "lisan_wasat", "jahr,rakhawa",        "j"),
)

assert len(GRAPHEME_TABLE) == 28, (
    f"Expected 28 graphemes, got {len(GRAPHEME_TABLE)}"
)

# Index by symbol for O(1) lookup
GRAPHEME_BY_SYMBOL: dict[str, Grapheme] = {g.symbol: g for g in GRAPHEME_TABLE}


def get_grapheme(symbol: str) -> Grapheme:
    """Pure lookup: return the canonical ``Grapheme`` for ``symbol``.

    Raises
    ------
    ValueError
        With ``FailureCode.M_00_03`` if symbol is not in the 28.
    """
    try:
        return GRAPHEME_BY_SYMBOL[symbol]
    except KeyError:
        raise ValueError(
            f"{FailureCode.M_00_03.value}: {symbol!r} not found in the 28 Arabic graphemes"
        )
