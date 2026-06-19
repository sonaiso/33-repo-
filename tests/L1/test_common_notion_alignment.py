"""
PR-B regression tests: constitutional alignment of L1 common notions.

trace_ref: docs/00_MAQOOL_CONSTITUTION.md §9
"""
from pathlib import Path

from taaqqul_slot_geometry.L1.common_notion import COMMON_NOTIONS


REPO_ROOT = Path(__file__).resolve().parents[2]
CONSTITUTION_PATH = REPO_ROOT / "docs" / "00_MAQOOL_CONSTITUTION.md"

EXPECTED_CN = (
    {
        "notion_id": "CN1",
        "name": "Self-Equality",
        "name_ar": "المساواة الذاتية",
        "statement": "Every entity is equal to itself.",
        "formal_expression": "A=A",
        "order": 1,
        "constitution_ref": "docs/00_MAQOOL_CONSTITUTION.md §9 CN1",
        "trace_ref": "docs/00_MAQOOL_CONSTITUTION.md §9 CN1",
    },
    {
        "notion_id": "CN2",
        "name": "Whole Greater Than Part",
        "name_ar": "الكل أكبر من الجزء",
        "statement": "If A contains B and B is not empty, then A is greater than B.",
        "formal_expression": "B⊂A ∧ B≠∅ → A>B",
        "order": 2,
        "constitution_ref": "docs/00_MAQOOL_CONSTITUTION.md §9 CN2",
        "trace_ref": "docs/00_MAQOOL_CONSTITUTION.md §9 CN2",
    },
    {
        "notion_id": "CN3",
        "name": "Substitution",
        "name_ar": "الاستبدال",
        "statement": "If A = B and B = C, then A = C.",
        "formal_expression": "A=B ∧ B=C → A=C",
        "order": 3,
        "constitution_ref": "docs/00_MAQOOL_CONSTITUTION.md §9 CN3",
        "trace_ref": "docs/00_MAQOOL_CONSTITUTION.md §9 CN3",
    },
    {
        "notion_id": "CN4",
        "name": "Transitivity of Subsumption",
        "name_ar": "تعدّي الاشتمال",
        "statement": (
            "If Identity(a) ⊆ Identity(b) and Identity(b) ⊆ Identity(c), "
            "then Identity(a) ⊆ Identity(c)."
        ),
        "formal_expression": (
            "Identity(a) ⊆ Identity(b) ∧ Identity(b) ⊆ Identity(c) → "
            "Identity(a) ⊆ Identity(c)"
        ),
        "order": 4,
        "constitution_ref": "docs/00_MAQOOL_CONSTITUTION.md §9 CN4",
        "trace_ref": "docs/00_MAQOOL_CONSTITUTION.md §9 CN4",
    },
)


def test_total_common_notions_is_4():
    assert len(COMMON_NOTIONS) == 4


def test_ids_are_exactly_cn1_to_cn4_in_order():
    assert [cn.notion_id for cn in COMMON_NOTIONS] == ["CN1", "CN2", "CN3", "CN4"]


def test_required_names_match_constitution():
    assert COMMON_NOTIONS[0].name == "Self-Equality"
    assert COMMON_NOTIONS[1].name == "Whole Greater Than Part"
    assert COMMON_NOTIONS[2].name == "Substitution"
    assert COMMON_NOTIONS[3].name == "Transitivity of Subsumption"


def test_every_common_notion_has_trace_ref_and_candidate_rank():
    for cn in COMMON_NOTIONS:
        assert cn.trace_ref
        assert cn.rank == "CANDIDATE"


def test_cn2_cn3_are_not_additive_or_subtractive_equality():
    cn2_name = COMMON_NOTIONS[1].name
    cn3_name = COMMON_NOTIONS[2].name
    assert cn2_name != "Additive Equality"
    assert cn3_name != "Subtractive Equality"


def test_common_notion_payload_matches_explicit_constitutional_constants():
    actual = [
        {
            "notion_id": cn.notion_id,
            "name": cn.name,
            "name_ar": cn.name_ar,
            "statement": cn.statement,
            "formal_expression": cn.formal_expression,
            "order": cn.order,
            "constitution_ref": cn.constitution_ref,
            "trace_ref": cn.trace_ref,
        }
        for cn in COMMON_NOTIONS
    ]
    assert actual == list(EXPECTED_CN)


def test_regression_constitution_section_9_contains_expected_cn_text():
    """Intentional file-based regression check against constitutional source text."""
    constitution_text = CONSTITUTION_PATH.read_text(encoding="utf-8").replace("\r\n", "\n")
    expected_snippets = (
        "### CN1 — Self-Equality\nEvery entity is equal to itself.",
        "### CN2 — Whole Greater Than Part\nIf A contains B and B is not empty, then A is greater than B.",
        "### CN3 — Substitution\nIf A = B and B = C, then A = C.",
        (
            "### CN4 — Transitivity of Subsumption\n"
            "If Identity(a) ⊆ Identity(b) and Identity(b) ⊆ Identity(c), "
            "then Identity(a) ⊆ Identity(c)."
        ),
    )
    for snippet in expected_snippets:
        assert snippet in constitution_text
