"""
JamidAnchor — binary and ternary lexical anchors.
Origin: docs/00_MAQOOL_CONSTITUTION.md; docs/01_L0_PHONETIC_BOUNDARY.md BL-L0-05
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import FrozenSet, Tuple

from taaqqul_slot_geometry.constitution.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.L0.phoneme import PhonemeUnit, PhoneticPattern


class JamidAnchorType(str, Enum):
    """Classification of jamid anchor by arity."""

    BINARY  = "binary"   # 2-phoneme anchor (yd, dm, xd, fm)
    TERNARY = "ternary"  # 3-phoneme anchor (hjr, byt, bab)


# Closed sets of recognised anchor forms
_BINARY_FORMS: FrozenSet[str] = frozenset({"yd", "dm", "xd", "fm"})
_TERNARY_FORMS: FrozenSet[str] = frozenset({"hjr", "byt", "bab"})


@dataclass(frozen=True)
class JamidAnchor:
    """An immutable lexical anchor that is NOT a derivational root.

    Binary anchors (2 consonants) carry the ``CVC`` phonetic pattern and
    must NEVER be treated as derivational roots (BL-L0-05).

    Ternary anchors (3 consonants) carry the ``CVCVC`` pattern (2×CVC∅).

    Parameters
    ----------
    form : str
        The romanised form of the anchor (e.g. ``"yd"``, ``"hjr"``).
    anchor_type : JamidAnchorType
        BINARY or TERNARY.
    phonemes : Tuple[PhonemeUnit, ...]
        The phoneme units composing this anchor.
    is_derivational_root : bool
        MUST always be ``False``.  Any attempt to set it ``True`` is rejected.
    trace_ref : str
        Constitutional reference.
    rank : str
        Always ``"CANDIDATE"``.
    residuals : FrozenSet[str]
        Residual bundle.
    """

    form: str
    anchor_type: JamidAnchorType
    phonemes: Tuple[PhonemeUnit, ...]
    is_derivational_root: bool = False
    trace_ref: str = "docs/01_L0_PHONETIC_BOUNDARY.md BL-L0-05"
    rank: str = "CANDIDATE"
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        # BL-L0-05: binary anchors are NOT derivational roots
        if self.is_derivational_root:
            raise ValueError(FailureCode.M_00_07.value)

        # Validate form membership
        if self.anchor_type == JamidAnchorType.BINARY:
            if self.form not in _BINARY_FORMS:
                raise ValueError(
                    f"{FailureCode.M_00_23.value}: binary jamid form {self.form!r} "
                    f"not in {sorted(_BINARY_FORMS)}"
                )
            if len(self.phonemes) != 2:
                raise ValueError(
                    f"{FailureCode.M_00_23.value}: binary jamid must have 2 phonemes"
                )
            # Each phoneme must use CVC∅ pattern for binary CVC structure
            for ph in self.phonemes:
                if ph.pattern not in (
                    PhoneticPattern.CVC_SUKUN,
                    PhoneticPattern.C_FATHA,
                    PhoneticPattern.C_DAMMA,
                    PhoneticPattern.C_KASRA,
                    PhoneticPattern.C_SUKUN,
                ):
                    raise ValueError(
                        f"{FailureCode.M_00_23.value}: phoneme pattern {ph.pattern!r} "
                        f"is invalid for binary jamid"
                    )
        elif self.anchor_type == JamidAnchorType.TERNARY:
            if self.form not in _TERNARY_FORMS:
                raise ValueError(
                    f"{FailureCode.M_00_24.value}: ternary jamid form {self.form!r} "
                    f"not in {sorted(_TERNARY_FORMS)}"
                )
            if len(self.phonemes) != 3:
                raise ValueError(
                    f"{FailureCode.M_00_24.value}: ternary jamid must have 3 phonemes"
                )

        if not self.trace_ref:
            raise ValueError(FailureCode.M_00_11.value)
        if self.rank != "CANDIDATE":
            raise ValueError(FailureCode.M_00_10.value)


# ── Canonical binary anchors ─────────────────────────────────────────────────

def _make_binary(form: str, c1: str, c2: str) -> JamidAnchor:
    """Pure factory for binary jamid anchors."""
    return JamidAnchor(
        form=form,
        anchor_type=JamidAnchorType.BINARY,
        phonemes=(
            PhonemeUnit(consonant=c1, pattern=PhoneticPattern.C_FATHA),
            PhonemeUnit(consonant=c2, pattern=PhoneticPattern.C_SUKUN),
        ),
    )


def _make_ternary(form: str, c1: str, c2: str, c3: str) -> JamidAnchor:
    """Pure factory for ternary jamid anchors."""
    return JamidAnchor(
        form=form,
        anchor_type=JamidAnchorType.TERNARY,
        phonemes=(
            PhonemeUnit(consonant=c1, pattern=PhoneticPattern.C_FATHA),
            PhonemeUnit(consonant=c2, pattern=PhoneticPattern.C_FATHA),
            PhonemeUnit(consonant=c3, pattern=PhoneticPattern.C_SUKUN),
        ),
    )


BINARY_ANCHORS: Tuple[JamidAnchor, ...] = (
    _make_binary("yd", "j", "d"),
    _make_binary("dm", "d", "m"),
    _make_binary("xd", "x", "d"),
    _make_binary("fm", "f", "m"),
)

TERNARY_ANCHORS: Tuple[JamidAnchor, ...] = (
    _make_ternary("hjr", "h", "dʒ", "r"),
    _make_ternary("byt", "b", "j", "t"),
    _make_ternary("bab", "b", "ʔ", "b"),
)

ALL_ANCHORS: Tuple[JamidAnchor, ...] = BINARY_ANCHORS + TERNARY_ANCHORS
