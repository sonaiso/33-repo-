"""Regression checks for the DAL-A0 law-only closure document."""
from pathlib import Path

from tests.markdown_sections import get_section


REPO_ROOT = Path(__file__).parent.parent
DAL_ALONE_DOC = REPO_ROOT / "docs" / "58_DAL_ALONE_ATOMIC_CLOSURE_LAW.md"


def test_dal_alone_law_document_exists():
    """trace_ref: docs/58_DAL_ALONE_ATOMIC_CLOSURE_LAW.md DAL-A0 Status."""
    assert DAL_ALONE_DOC.exists()


def test_dal_a0_is_law_only():
    """trace_ref: docs/58_DAL_ALONE_ATOMIC_CLOSURE_LAW.md DAL-A0 Status."""
    content = DAL_ALONE_DOC.read_text(encoding="utf-8")
    section = get_section(content, "## DAL-A0 Status", "## ")
    assert "`DAL-A0 = Ratified`" in section
    assert "law-only" in section
    assert "no runtime" in section
    assert "no global `FailureCode` expansion" in section


def test_dal_a1_order_comes_after_a0_before_a2():
    """trace_ref: docs/58_DAL_ALONE_ATOMIC_CLOSURE_LAW.md Remaining Runtime Path."""
    content = DAL_ALONE_DOC.read_text(encoding="utf-8")
    section = get_section(content, "## Remaining Runtime Path", "## ")
    assert section.index("DAL-A0 law-only") < section.index("DAL-A1 carriers")
    assert section.index("DAL-A1 carriers") < section.index("DAL-A2 raw trace")


def test_dal_a1_scope_is_carriers_and_residuals_only():
    """trace_ref: docs/58_DAL_ALONE_ATOMIC_CLOSURE_LAW.md DAL-A1 Scope."""
    content = DAL_ALONE_DOC.read_text(encoding="utf-8")
    section = get_section(content, "## DAL-A1 Scope", "## ")
    assert "carriers and local residual vocabulary only" in section
    assert "no gate execution" in section
    assert "no `DalAloneClosed`" in section
    assert "no `LafziMadlulGate`" in section


def test_dal_alone_does_not_cross_to_lafzi_madlul():
    """trace_ref: docs/58_DAL_ALONE_ATOMIC_CLOSURE_LAW.md Non-Domain."""
    content = DAL_ALONE_DOC.read_text(encoding="utf-8")
    non_domain = get_section(content, "## Non-Domain", "## ")
    assert "`DalAloneClosed != Meaning`" in non_domain
    assert "`DalAloneClosed != WordKind`" in non_domain
    assert "`LafziMadlul`" in non_domain
    assert "`LafziMadlulGate`" not in get_section(
        content, "## DAL-A1 Scope", "## "
    ).split("DAL-A1 may define only:")[1]

