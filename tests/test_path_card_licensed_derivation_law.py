"""Regression checks for docs/60 path-card licensed derivation law."""
from pathlib import Path


REPO_ROOT = Path(__file__).parent.parent
LAW_DOC = REPO_ROOT / "docs" / "60_PATH_CARD_LICENSED_DERIVATION_LAW.md"


def test_path_card_law_doc_exists() -> None:
    """trace_ref: docs/60_PATH_CARD_LICENSED_DERIVATION_LAW.md Authority."""
    assert LAW_DOC.exists()


def test_path_card_law_requires_path_card_before_derivation() -> None:
    """trace_ref: docs/60_PATH_CARD_LICENSED_DERIVATION_LAW.md Core law."""
    content = LAW_DOC.read_text(encoding="utf-8")
    assert "لا اشتقاق قبل بطاقة المسار." in content
    assert "SurfaceWeight(x) ⇏ DerivationLicense(x)" in content
    assert "VerbGate(x) ⇔ MasdarOpen(x) ∨ DenominalBranchLicensed(x)" in content


def test_path_card_law_preserves_branch_rank_non_inheritance() -> None:
    """trace_ref: docs/60_PATH_CARD_LICENSED_DERIVATION_LAW.md Operational constitutional clauses."""
    content = LAW_DOC.read_text(encoding="utf-8")
    assert "لا فرع يرث رتبة أصله." in content
    assert 'rank = "CANDIDATE"' in content
