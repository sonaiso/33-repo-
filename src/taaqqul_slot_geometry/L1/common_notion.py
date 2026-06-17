"""
L1 Common Notions — الأفكار العامة (CN1-CN4).

Origin: docs/00_MAQOOL_CONSTITUTION.md §6 L1 (Formal Description)
Authority: docs/15_PROJECT_ROADMAP.md Phase 1 PR-12

Architecture:
    Common Notions are self-evident truths shared by all reasoning agents.
    Unlike postulates (which are domain-specific axioms), common notions
    are universal principles that apply across all layers and domains.

    === The Four Common Notions ===

    CN1 — Transitivity (التعدّي):
        Things equal to the same thing are equal to each other.
        If A = C and B = C, then A = B.

    CN2 — Additive Equality (الجمع):
        If equals are added to equals, the wholes are equal.
        If A = B and C = D, then A + C = B + D.

    CN3 — Subtractive Equality (الطرح):
        If equals are subtracted from equals, the remainders are equal.
        If A = B and C = D, then A - C = B - D.

    CN4 — Whole Greater Than Part (الكل أكبر من الجزء):
        The whole is greater than any of its proper parts.
        If B ⊂ A, then A > B.

Every common notion carries:
    - notion_id: unique identifier (e.g. "CN1")
    - name: human-readable name
    - name_ar: Arabic name
    - statement: formal statement
    - formal_expression: symbolic expression
    - trace_ref: constitutional reference
    - rank: always "CANDIDATE"
    - residuals: residual bundle (FrozenSet)
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, unique
from typing import Dict, FrozenSet, Tuple

from taaqqul_slot_geometry.constitution.failure_taxonomy import FailureCode


# ══════════════════════════════════════════════════════════════════════════════
# §1  ENUMERATIONS
# ══════════════════════════════════════════════════════════════════════════════


@unique
class CommonNotionDomain(str, Enum):
    """Domain of applicability for a common notion.

    Origin: docs/00_MAQOOL_CONSTITUTION.md §6 L1

    Each common notion applies across one or more reasoning domains:
    - EQUALITY: governing equivalence relations (CN1, CN2, CN3)
    - ORDER: governing part-whole and magnitude relations (CN4)
    """

    EQUALITY = "equality"
    ORDER = "order"


# ══════════════════════════════════════════════════════════════════════════════
# §2  COMMON NOTION ENTITY (الفكرة العامة)
# ══════════════════════════════════════════════════════════════════════════════


@dataclass(frozen=True)
class CommonNotion:
    """A formal common notion — فكرة عامة.

    Origin: docs/00_MAQOOL_CONSTITUTION.md §6 L1

    A common notion is a self-evident universal truth that requires no proof
    and applies across all domains. It is more general than a postulate.

    Parameters
    ----------
    notion_id : str
        Unique identifier (e.g. "CN1", "CN2").
    name : str
        Human-readable name (e.g. "Transitivity").
    name_ar : str
        Arabic name (e.g. "التعدّي").
    statement : str
        Formal statement of the common notion.
    formal_expression : str
        Symbolic/logical expression (e.g. "A=C ∧ B=C → A=B").
    domain : CommonNotionDomain
        Which reasoning domain this notion governs.
    constitution_ref : str
        Reference to the constitution section.
    related_failure_codes : Tuple[str, ...]
        FailureCode values that this notion guards against.
    trace_ref : str
        Constitutional reference.
    rank : str
        Always "CANDIDATE".
    residuals : FrozenSet[str]
        Residual bundle.
    """

    notion_id: str
    name: str
    name_ar: str
    statement: str
    formal_expression: str
    domain: CommonNotionDomain
    constitution_ref: str
    related_failure_codes: Tuple[str, ...] = ()
    trace_ref: str = "docs/00_MAQOOL_CONSTITUTION.md §6 L1"
    rank: str = "CANDIDATE"
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        """Birth guard — validates all common notion fields."""
        if not self.notion_id:
            raise ValueError(FailureCode.M_01_04.value)
        if not self.name:
            raise ValueError(FailureCode.M_01_04.value)
        if not self.name_ar:
            raise ValueError(FailureCode.M_01_04.value)
        if not self.statement:
            raise ValueError(FailureCode.M_01_04.value)
        if not self.formal_expression:
            raise ValueError(FailureCode.M_01_04.value)
        if not isinstance(self.domain, CommonNotionDomain):
            raise ValueError(FailureCode.M_01_04.value)
        if not self.constitution_ref:
            raise ValueError(FailureCode.M_01_03.value)
        if not self.trace_ref:
            raise ValueError(FailureCode.M_01_14.value)
        if self.rank != "CANDIDATE":
            raise ValueError(FailureCode.M_01_16.value)


# ══════════════════════════════════════════════════════════════════════════════
# §3  THE FOUR COMMON NOTIONS (الأفكار العامة الأربع)
# ══════════════════════════════════════════════════════════════════════════════


COMMON_NOTION_CN1 = CommonNotion(
    notion_id="CN1",
    name="Transitivity",
    name_ar="التعدّي",
    statement=(
        "Things equal to the same thing are equal to each other. "
        "If A equals C and B equals C, then A equals B."
    ),
    formal_expression="A=C ∧ B=C → A=B",
    domain=CommonNotionDomain.EQUALITY,
    constitution_ref="docs/00_MAQOOL_CONSTITUTION.md §6 L1 CN1",
    related_failure_codes=(
        FailureCode.M_01_13.value,
    ),
)

COMMON_NOTION_CN2 = CommonNotion(
    notion_id="CN2",
    name="Additive Equality",
    name_ar="الجمع",
    statement=(
        "If equals are added to equals, the wholes are equal. "
        "If A equals B and C equals D, then A+C equals B+D."
    ),
    formal_expression="A=B ∧ C=D → A+C=B+D",
    domain=CommonNotionDomain.EQUALITY,
    constitution_ref="docs/00_MAQOOL_CONSTITUTION.md §6 L1 CN2",
    related_failure_codes=(
        FailureCode.M_01_12.value,
    ),
)

COMMON_NOTION_CN3 = CommonNotion(
    notion_id="CN3",
    name="Subtractive Equality",
    name_ar="الطرح",
    statement=(
        "If equals are subtracted from equals, the remainders are equal. "
        "If A equals B and C equals D, then A-C equals B-D."
    ),
    formal_expression="A=B ∧ C=D → A-C=B-D",
    domain=CommonNotionDomain.EQUALITY,
    constitution_ref="docs/00_MAQOOL_CONSTITUTION.md §6 L1 CN3",
    related_failure_codes=(
        FailureCode.M_01_12.value,
    ),
)

COMMON_NOTION_CN4 = CommonNotion(
    notion_id="CN4",
    name="Whole Greater Than Part",
    name_ar="الكل أكبر من الجزء",
    statement=(
        "The whole is greater than any of its proper parts. "
        "If B is a proper subset of A, then A is greater than B."
    ),
    formal_expression="B⊂A → A>B",
    domain=CommonNotionDomain.ORDER,
    constitution_ref="docs/00_MAQOOL_CONSTITUTION.md §6 L1 CN4",
    related_failure_codes=(
        FailureCode.M_01_11.value,
    ),
)


# ══════════════════════════════════════════════════════════════════════════════
# §4  REGISTRY (سِجل الأفكار العامة)
# ══════════════════════════════════════════════════════════════════════════════


COMMON_NOTIONS: Tuple[CommonNotion, ...] = (
    COMMON_NOTION_CN1,
    COMMON_NOTION_CN2,
    COMMON_NOTION_CN3,
    COMMON_NOTION_CN4,
)
"""All 4 common notions in canonical order."""

COMMON_NOTION_BY_ID: Dict[str, CommonNotion] = {
    cn.notion_id: cn for cn in COMMON_NOTIONS
}
"""Lookup any common notion by ID."""


# ══════════════════════════════════════════════════════════════════════════════
# §5  PURE FUNCTIONS (دوال نقية)
# ══════════════════════════════════════════════════════════════════════════════


def get_common_notion(notion_id: str) -> CommonNotion:
    """Look up a common notion by its ID.

    Parameters
    ----------
    notion_id : str
        The ID to look up (e.g. "CN1", "CN2").

    Returns
    -------
    CommonNotion
        The matching common notion.

    Raises
    ------
    ValueError
        If the notion_id is not found (M_01_04).
    """
    if notion_id not in COMMON_NOTION_BY_ID:
        raise ValueError(FailureCode.M_01_04.value)
    return COMMON_NOTION_BY_ID[notion_id]


def common_notions_by_domain(domain: CommonNotionDomain) -> Tuple[CommonNotion, ...]:
    """Return all common notions belonging to a domain.

    Parameters
    ----------
    domain : CommonNotionDomain
        The domain to filter by.

    Returns
    -------
    Tuple[CommonNotion, ...]
        All common notions in that domain.
    """
    return tuple(cn for cn in COMMON_NOTIONS if cn.domain == domain)


def total_common_notion_count() -> int:
    """Return the total number of common notions (always 4).

    Returns
    -------
    int
        The count of common notions in the registry.
    """
    return len(COMMON_NOTIONS)


def verify_common_notion_coverage() -> bool:
    """Verify that all domains have at least one common notion.

    Returns
    -------
    bool
        True if all domains are covered.

    Raises
    ------
    ValueError
        If any domain has no common notions (M_01_04).
    """
    for domain in CommonNotionDomain:
        if not common_notions_by_domain(domain):
            raise ValueError(FailureCode.M_01_04.value)
    return True
