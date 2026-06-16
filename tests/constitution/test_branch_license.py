"""
Tests for BranchLicense — branching governance enforcement.

Origin: docs/00_MAQOOL_CONSTITUTION.md §5 Rules 1, 6, 7, 8
        docs/15_PROJECT_ROADMAP.md §حوكمة التفريع
"""
import pytest

from taaqqul_slot_geometry.constitution.branch_license import (
    BranchLicense,
    BranchLicenseError,
)
from taaqqul_slot_geometry.constitution.failure_taxonomy import FailureCode


# ── Valid license fixture ────────────────────────────────────────────────────

def _valid_license(**overrides) -> BranchLicense:
    """Create a valid BranchLicense with optional overrides."""
    defaults = dict(
        roadmap_ref="docs/15_PROJECT_ROADMAP.md Phase 1 PR-10",
        parent_ref="Phase 0 — L0 Closure",
        trunk_complete=True,
        motive="تحويل كيانات L0 إلى تعريفات رسمية",
        description="L1/definition.py — تعريف رسمي لكل كيان L0",
        qualifying_difference="L0 = كيانات خام، L1 = تعريفات رسمية",
        condition="L0 مُغلق رسميًا",
        cause="الاستدلال المنطقي يحتاج تعريفات رسمية",
        barrier_absent=True,
        barrier_check_description="لا يوجد كيان L0 ناقص أو residual مفتوح",
    )
    defaults.update(overrides)
    return BranchLicense(**defaults)


# ── Construction tests ───────────────────────────────────────────────────────


class TestBranchLicenseConstruction:
    """Test that valid licenses construct successfully."""

    def test_valid_license_constructs(self):
        """A fully valid license should construct without error."""
        license = _valid_license()
        assert license.roadmap_ref == "docs/15_PROJECT_ROADMAP.md Phase 1 PR-10"
        assert license.rank == "CANDIDATE"
        assert license.trunk_complete is True

    def test_license_is_frozen(self):
        """BranchLicense must be immutable (Rule 3)."""
        license = _valid_license()
        with pytest.raises(AttributeError):
            license.motive = "something else"  # type: ignore[misc]

    def test_mandatory_entity_fields(self):
        """BranchLicense carries trace_ref, rank, residuals (Rule 2)."""
        license = _valid_license()
        assert license.trace_ref == "docs/15_PROJECT_ROADMAP.md"
        assert license.rank == "CANDIDATE"
        assert isinstance(license.residuals, frozenset)

    def test_sub_branches_defaults_empty(self):
        """Sub-branches set starts empty."""
        license = _valid_license()
        assert license.sub_branches_licensed == frozenset()


# ── Rejection tests (birth guards) ──────────────────────────────────────────


class TestBranchLicenseRejections:
    """Test that invalid licenses are rejected with named FailureCodes."""

    def test_empty_roadmap_ref_rejected(self):
        """M_CX_16: Missing roadmap reference."""
        with pytest.raises(BranchLicenseError) as exc_info:
            _valid_license(roadmap_ref="")
        assert exc_info.value.failure_code == FailureCode.M_CX_16

    def test_empty_parent_ref_rejected(self):
        """M_CX_16: Missing parent reference."""
        with pytest.raises(BranchLicenseError) as exc_info:
            _valid_license(parent_ref="")
        assert exc_info.value.failure_code == FailureCode.M_CX_16

    def test_trunk_incomplete_rejected(self):
        """M_CX_17: Trunk not complete."""
        with pytest.raises(BranchLicenseError) as exc_info:
            _valid_license(trunk_complete=False)
        assert exc_info.value.failure_code == FailureCode.M_CX_17

    def test_empty_motive_rejected(self):
        """M_CX_18: Missing motive."""
        with pytest.raises(BranchLicenseError) as exc_info:
            _valid_license(motive="")
        assert exc_info.value.failure_code == FailureCode.M_CX_18

    def test_empty_description_rejected(self):
        """M_CX_19: Missing distinguishing description."""
        with pytest.raises(BranchLicenseError) as exc_info:
            _valid_license(description="")
        assert exc_info.value.failure_code == FailureCode.M_CX_19

    def test_empty_qualifying_difference_rejected(self):
        """M_CX_19: Missing qualifying difference."""
        with pytest.raises(BranchLicenseError) as exc_info:
            _valid_license(qualifying_difference="")
        assert exc_info.value.failure_code == FailureCode.M_CX_19

    def test_empty_condition_rejected(self):
        """M_CX_20: Missing condition."""
        with pytest.raises(BranchLicenseError) as exc_info:
            _valid_license(condition="")
        assert exc_info.value.failure_code == FailureCode.M_CX_20

    def test_empty_cause_rejected(self):
        """M_CX_18: Missing cause."""
        with pytest.raises(BranchLicenseError) as exc_info:
            _valid_license(cause="")
        assert exc_info.value.failure_code == FailureCode.M_CX_18

    def test_barrier_not_absent_rejected(self):
        """M_CX_20: Barrier not verified absent."""
        with pytest.raises(BranchLicenseError) as exc_info:
            _valid_license(barrier_absent=False)
        assert exc_info.value.failure_code == FailureCode.M_CX_20

    def test_empty_barrier_check_description_rejected(self):
        """M_CX_20: Barrier check description missing."""
        with pytest.raises(BranchLicenseError) as exc_info:
            _valid_license(barrier_check_description="")
        assert exc_info.value.failure_code == FailureCode.M_CX_20

    def test_rank_above_candidate_rejected(self):
        """M_CX_09: Rank must be CANDIDATE."""
        with pytest.raises(BranchLicenseError) as exc_info:
            _valid_license(rank="PROVEN")
        assert exc_info.value.failure_code == FailureCode.M_CX_09

    def test_empty_trace_ref_rejected(self):
        """M_CX_12: Missing trace_ref."""
        with pytest.raises(BranchLicenseError) as exc_info:
            _valid_license(trace_ref="")
        assert exc_info.value.failure_code == FailureCode.M_CX_12


# ── Recursive branching tests ────────────────────────────────────────────────


class TestRecursiveBranching:
    """Test that licensed branches can authorize sub-branches."""

    def test_license_sub_branch(self):
        """A licensed branch can license a sub-branch."""
        parent_license = _valid_license()
        updated = parent_license.license_sub_branch("PR-10.1-definition-helpers")
        assert "PR-10.1-definition-helpers" in updated.sub_branches_licensed
        # Original is unchanged (frozen)
        assert "PR-10.1-definition-helpers" not in parent_license.sub_branches_licensed

    def test_license_multiple_sub_branches(self):
        """Multiple sub-branches can be licensed sequentially."""
        license = _valid_license()
        license = license.license_sub_branch("sub-A")
        license = license.license_sub_branch("sub-B")
        assert license.sub_branches_licensed == frozenset({"sub-A", "sub-B"})

    def test_empty_sub_branch_id_rejected(self):
        """Cannot license an empty sub-branch ID."""
        license = _valid_license()
        with pytest.raises(BranchLicenseError) as exc_info:
            license.license_sub_branch("")
        assert exc_info.value.failure_code == FailureCode.M_CX_16

    def test_sub_branch_returns_new_instance(self):
        """license_sub_branch returns a new BranchLicense (immutability)."""
        license = _valid_license()
        updated = license.license_sub_branch("sub-X")
        assert license is not updated
        assert isinstance(updated, BranchLicense)


# ── Integration with FailureCode taxonomy ────────────────────────────────────


class TestFailureCodeIntegration:
    """Verify that all branching failure codes exist in the taxonomy."""

    def test_m_cx_16_exists(self):
        assert FailureCode.M_CX_16.value == "branch_without_roadmap_ref"

    def test_m_cx_17_exists(self):
        assert FailureCode.M_CX_17.value == "branch_trunk_incomplete"

    def test_m_cx_18_exists(self):
        assert FailureCode.M_CX_18.value == "branch_motive_missing"

    def test_m_cx_19_exists(self):
        assert FailureCode.M_CX_19.value == "branch_distinguishing_difference_missing"

    def test_m_cx_20_exists(self):
        assert FailureCode.M_CX_20.value == "branch_barrier_not_verified"
