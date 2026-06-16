"""
BranchLicense — governance entity for licensed derivation from the roadmap trunk.

Origin: docs/00_MAQOOL_CONSTITUTION.md §5 Rules 1, 6, 7, 8
        docs/15_PROJECT_ROADMAP.md §مبدأ عدم الانفجار

Every piece of work in this project must trace back to the roadmap (الأصل).
No branch (تفريع) is allowed until the trunk meets minimum completeness.
Every branch requires:
  - A roadmap reference (مرجع خارطة الطريق)
  - A motive (دافع) — why this branch exists
  - A distinguishing description (وصف مؤثر) — what makes it different from the trunk
  - A qualifying difference (فرق قادح) — the essential distinction
  - Condition verification (شرط) — what must be true for the branch to exist
  - Cause verification (سبب) — why the branch is needed
  - Barrier check (مانع) — what would prevent the branch from being valid
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import FrozenSet

from taaqqul_slot_geometry.constitution.failure_taxonomy import FailureCode


class BranchLicenseError(ValueError):
    """Raised when a branch license fails governance validation.

    Origin: docs/00_MAQOOL_CONSTITUTION.md §5 Rule 1
    """

    def __init__(self, message: str, failure_code: FailureCode) -> None:
        super().__init__(f"{failure_code.value}: {message}")
        self.failure_code = failure_code


@dataclass(frozen=True)
class BranchLicense:
    """Immutable license authorizing derivation from the roadmap trunk.

    A BranchLicense proves that a piece of work (PR, module, entity) is
    constitutionally authorized. It enforces:

    1. Roadmap traceability — every branch traces to a numbered PR in the roadmap
    2. Trunk completeness — the parent must be minimally complete
    3. Motive — there must be a reason (دافع) for the branch
    4. Distinguishing description — the branch must differ meaningfully (وصف مؤثر)
    5. Qualifying difference — the essential distinction (فرق قادح)
    6. Condition — what must hold true (شرط)
    7. Cause — why it's needed (سبب)
    8. Barrier absence — nothing prevents it (مانع مفقود)

    Parameters
    ----------
    roadmap_ref : str
        Reference to a specific PR or section in docs/15_PROJECT_ROADMAP.md.
    parent_ref : str
        Reference to the parent (trunk) this branch derives from.
        For top-level PRs, this is the phase reference.
    trunk_complete : bool
        Attestation that the trunk (parent) has met minimum completeness.
    motive : str
        The reason (دافع) this branch exists. Must be non-empty.
    description : str
        Distinguishing description (وصف مؤثر) — how this differs from the trunk.
    qualifying_difference : str
        The essential difference (فرق قادح) that separates branch from trunk.
    condition : str
        What must be true (شرط) for this branch to be valid.
    cause : str
        Why the branch is needed (سبب).
    barrier_absent : bool
        Attestation that no barrier (مانع) prevents this branch.
    barrier_check_description : str
        Description of how the barrier was verified absent.
    sub_branches_licensed : FrozenSet[str]
        IDs of sub-branches this license has authorized (recursive licensing).
    trace_ref : str
        Constitutional reference.
    rank : str
        Always "CANDIDATE".
    residuals : FrozenSet[str]
        Residual bundle.
    """

    roadmap_ref: str
    parent_ref: str
    trunk_complete: bool
    motive: str
    description: str
    qualifying_difference: str
    condition: str
    cause: str
    barrier_absent: bool
    barrier_check_description: str
    sub_branches_licensed: FrozenSet[str] = frozenset()
    trace_ref: str = "docs/15_PROJECT_ROADMAP.md"
    rank: str = "CANDIDATE"
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        """Birth guard — validates all governance fields at construction."""
        if not self.roadmap_ref:
            raise BranchLicenseError(
                "roadmap_ref is empty — every branch must reference the roadmap",
                FailureCode.M_CX_16,
            )
        if not self.parent_ref:
            raise BranchLicenseError(
                "parent_ref is empty — every branch must reference its trunk",
                FailureCode.M_CX_16,
            )
        if not self.trunk_complete:
            raise BranchLicenseError(
                "trunk is not complete — no branching before trunk minimum completeness",
                FailureCode.M_CX_17,
            )
        if not self.motive:
            raise BranchLicenseError(
                "motive (دافع) is empty — every branch requires a stated motive",
                FailureCode.M_CX_18,
            )
        if not self.description:
            raise BranchLicenseError(
                "description (وصف مؤثر) is empty — branch must be distinguishable",
                FailureCode.M_CX_19,
            )
        if not self.qualifying_difference:
            raise BranchLicenseError(
                "qualifying_difference (فرق قادح) is empty — "
                "branch must have an essential distinction from trunk",
                FailureCode.M_CX_19,
            )
        if not self.condition:
            raise BranchLicenseError(
                "condition (شرط) is empty — branch validity condition required",
                FailureCode.M_CX_20,
            )
        if not self.cause:
            raise BranchLicenseError(
                "cause (سبب) is empty — branch must have a stated cause",
                FailureCode.M_CX_18,
            )
        if not self.barrier_absent:
            raise BranchLicenseError(
                "barrier (مانع) not verified absent — "
                "branch cannot proceed with unresolved barriers",
                FailureCode.M_CX_20,
            )
        if not self.barrier_check_description:
            raise BranchLicenseError(
                "barrier_check_description is empty — "
                "must describe how barrier absence was verified",
                FailureCode.M_CX_20,
            )
        if not self.trace_ref:
            raise BranchLicenseError(
                "trace_ref is empty",
                FailureCode.M_CX_12,
            )
        if self.rank != "CANDIDATE":
            raise BranchLicenseError(
                "rank above CANDIDATE",
                FailureCode.M_CX_09,
            )

    def license_sub_branch(self, sub_branch_id: str) -> "BranchLicense":
        """Create a new license with an additional sub-branch authorization.

        This enables recursive tree-structured derivation (تشجير) where a
        licensed branch can itself authorize further derivation.

        Parameters
        ----------
        sub_branch_id : str
            Identifier for the sub-branch being licensed.

        Returns
        -------
        BranchLicense
            A new license with the sub-branch added to sub_branches_licensed.
        """
        if not sub_branch_id:
            raise BranchLicenseError(
                "sub_branch_id is empty — cannot license an unnamed branch",
                FailureCode.M_CX_16,
            )
        new_subs = self.sub_branches_licensed | frozenset({sub_branch_id})
        # Use object.__setattr__ pattern for frozen dataclass update
        return BranchLicense(
            roadmap_ref=self.roadmap_ref,
            parent_ref=self.parent_ref,
            trunk_complete=self.trunk_complete,
            motive=self.motive,
            description=self.description,
            qualifying_difference=self.qualifying_difference,
            condition=self.condition,
            cause=self.cause,
            barrier_absent=self.barrier_absent,
            barrier_check_description=self.barrier_check_description,
            sub_branches_licensed=new_subs,
            trace_ref=self.trace_ref,
            rank=self.rank,
            residuals=self.residuals,
        )
