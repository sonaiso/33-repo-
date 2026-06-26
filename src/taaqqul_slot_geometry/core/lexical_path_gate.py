"""
Audit-only lexical path gate contracts.
Origin: docs/00_MAQOOL_CONSTITUTION.md §5 Rule 2, Rule 5
Authority: docs/15_PROJECT_ROADMAP.md (audit-only contract hardening)
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, IntEnum
from typing import Any, FrozenSet, Mapping, Optional, Protocol

from taaqqul_slot_geometry.constitution.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.core.rank import Rank


class PathType(str, Enum):
    MASDAR_OPEN = "MasdarOpen"
    JAMID_CLOSED = "JamidClosed"
    DENOMINAL_BRANCH = "DenominalBranch"
    MUSHTAQ_OPEN = "MushtaqOpen"
    MABNI_OPERATOR = "MabniOperator"
    AMBIGUOUS_RESIDUAL = "AmbiguousResidual"


class DecisionKind(str, Enum):
    VERB_CANDIDATE = "VerbCandidate"
    CLOSED_NOUN = "ClosedNoun"
    DENOMINAL_VERB_CANDIDATE = "DenominalVerbCandidate"
    RESIDUAL = "Residual"
    BLOCKED = "Blocked"


class GateRank(IntEnum):
    BLOCKED = 0
    RESIDUAL = 1
    HYPOTHESIS = 2
    LICENSED = 3


class ResidualSeverity(str, Enum):
    NON_BLOCKING = "non_blocking"
    DEFERRED = "deferred"
    BLOCKING = "blocking"


class LexicalFailureCode(str, Enum):
    PATH_CARD_MISSING = "PATH_CARD_MISSING"
    PATH_CARD_AMBIGUOUS = "PATH_CARD_AMBIGUOUS"
    TRACE_MISSING = "TRACE_MISSING"
    IDENTITY_MISSING = "IDENTITY_MISSING"
    ROOT_MISSING = "ROOT_MISSING"
    VOWEL_PATTERN_MISSING = "VOWEL_PATTERN_MISSING"
    EVENT_LOAD_MISSING = "EVENT_LOAD_MISSING"
    ENTITY_LOAD_MISSING = "ENTITY_LOAD_MISSING"
    BRANCH_LICENSE_MISSING = "BRANCH_LICENSE_MISSING"
    BRANCH_CARD_MISSING = "BRANCH_CARD_MISSING"
    BRANCH_TRACE_MISSING = "BRANCH_TRACE_MISSING"
    BRANCH_RANK_INHERITANCE = "BRANCH_RANK_INHERITANCE"
    BLOCKING_RESIDUAL_PRESENT = "BLOCKING_RESIDUAL_PRESENT"
    RANK_TOO_LOW = "RANK_TOO_LOW"
    RANK_PROMOTION = "RANK_PROMOTION"
    GENERATOR_FAILED = "GENERATOR_FAILED"
    GENERATED_KIND_MISMATCH = "GENERATED_KIND_MISMATCH"
    GENERATED_TRACE_MISSING = "GENERATED_TRACE_MISSING"
    GENERATED_TRACE_BREAK = "GENERATED_TRACE_BREAK"


@dataclass(frozen=True)
class Trace:
    refs: tuple[str, ...] = ()
    trace_ref: str = "docs/00_MAQOOL_CONSTITUTION.md §5 Rule 2"
    rank: Rank = Rank.CANDIDATE
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if not self.trace_ref:
            raise ValueError(FailureCode.M_CX_12.value)
        if self.rank != Rank.CANDIDATE:
            raise ValueError(FailureCode.M_CX_09.value)

    def is_complete(self) -> bool:
        return bool(self.refs) and all(bool(ref.strip()) for ref in self.refs)

    def is_parent_of(self, child: "Trace") -> bool:
        return set(self.refs).issubset(set(child.refs))


@dataclass(frozen=True)
class Residual:
    code: LexicalFailureCode
    message: str
    severity: ResidualSeverity = ResidualSeverity.BLOCKING
    trace_ref: Optional[str] = None
    rank: Rank = Rank.CANDIDATE
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if not str(self.code):
            raise ValueError(f"{FailureCode.M_CX_08.value}: residual code is required")
        if not self.message.strip():
            raise ValueError(f"{FailureCode.M_CX_08.value}: residual message is required")
        if self.rank != Rank.CANDIDATE:
            raise ValueError(FailureCode.M_CX_09.value)


@dataclass(frozen=True)
class BranchCard:
    branch_id: str
    origin_ref: str
    residual_source: str
    license_ref: str
    trace: Trace
    initial_rank: GateRank = GateRank.HYPOTHESIS
    trace_ref: str = "docs/00_MAQOOL_CONSTITUTION.md §5 Rule 2"
    rank: Rank = Rank.CANDIDATE
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if not self.trace_ref:
            raise ValueError(FailureCode.M_CX_12.value)
        if self.rank != Rank.CANDIDATE:
            raise ValueError(FailureCode.M_CX_09.value)

    def is_valid(self) -> bool:
        return (
            bool(self.branch_id.strip())
            and bool(self.origin_ref.strip())
            and bool(self.residual_source.strip())
            and bool(self.license_ref.strip())
            and self.trace.is_complete()
            and self.initial_rank <= GateRank.HYPOTHESIS
        )


@dataclass(frozen=True)
class PathCard:
    word: str
    path_type: PathType
    trace: Trace
    rank_level: GateRank
    identity_ref: Optional[str] = None
    root: Optional[tuple[str, ...]] = None
    vowel_pattern: Optional[str] = None
    event_load: bool = False
    entity_load: bool = False
    branch_license: bool = False
    branch_card: Optional[BranchCard] = None
    residual_entries: tuple[Residual, ...] = field(default_factory=tuple)
    trace_ref: str = "docs/00_MAQOOL_CONSTITUTION.md §5 Rule 2"
    rank: Rank = Rank.CANDIDATE
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if not self.trace_ref:
            raise ValueError(FailureCode.M_CX_12.value)
        if self.rank != Rank.CANDIDATE:
            raise ValueError(FailureCode.M_CX_09.value)

    def has_blocking_residuals(self) -> bool:
        return any(r.severity == ResidualSeverity.BLOCKING for r in self.residual_entries)


@dataclass(frozen=True)
class LexicalCandidate:
    kind: DecisionKind
    surface: str
    root: Optional[tuple[str, ...]]
    rank_level: GateRank
    trace: Trace
    residual_entries: tuple[Residual, ...] = field(default_factory=tuple)
    trace_ref: str = "docs/00_MAQOOL_CONSTITUTION.md §5 Rule 2"
    rank: Rank = Rank.CANDIDATE
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if not self.trace_ref:
            raise ValueError(FailureCode.M_CX_12.value)
        if self.rank != Rank.CANDIDATE:
            raise ValueError(FailureCode.M_CX_09.value)


@dataclass(frozen=True)
class LexicalDecision:
    kind: DecisionKind
    word: str
    rank_level: GateRank
    candidate: Optional[LexicalCandidate] = None
    residual_entries: tuple[Residual, ...] = field(default_factory=tuple)
    message: str = ""
    trace_ref: str = "docs/00_MAQOOL_CONSTITUTION.md §5 Rule 5"
    rank: Rank = Rank.CANDIDATE
    residuals: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if not self.trace_ref:
            raise ValueError(FailureCode.M_CX_12.value)
        if self.rank != Rank.CANDIDATE:
            raise ValueError(FailureCode.M_CX_09.value)


class PathCardRepository(Protocol):
    def get_path_card(self, word: str, context: Mapping[str, Any]) -> Optional[PathCard]:
        ...


class VerbGenerator(Protocol):
    def generate_from_masdar(self, card: PathCard) -> LexicalCandidate:
        ...

    def generate_from_denominal_branch(self, card: PathCard) -> LexicalCandidate:
        ...


class ResidualSink(Protocol):
    def store(
        self,
        word: str,
        residuals: tuple[Residual, ...],
        context: Mapping[str, Any],
    ) -> None:
        ...


class NullResidualSink:
    def store(
        self,
        word: str,
        residuals: tuple[Residual, ...],
        context: Mapping[str, Any],
    ) -> None:
        return None


def process_lexical_item(
    word: str,
    context: Mapping[str, Any],
    *,
    card_repo: PathCardRepository,
    generator: VerbGenerator,
    residual_sink: Optional[ResidualSink] = None,
) -> LexicalDecision:
    sink = residual_sink or NullResidualSink()
    cleaned_word = word.strip()

    if not cleaned_word:
        return _residual_decision(
            word=word,
            context=context,
            sink=sink,
            residuals=(
                Residual(
                    LexicalFailureCode.PATH_CARD_MISSING,
                    "Empty lexical item cannot be processed.",
                ),
            ),
        )

    card = card_repo.get_path_card(cleaned_word, context)
    if card is None:
        return _residual_decision(
            word=cleaned_word,
            context=context,
            sink=sink,
            residuals=(
                Residual(
                    LexicalFailureCode.PATH_CARD_MISSING,
                    "No PathCard was found for this lexical item.",
                ),
            ),
        )

    if card.path_type == PathType.MASDAR_OPEN:
        return _process_masdar_path(cleaned_word, card, context, generator, sink)
    if card.path_type == PathType.JAMID_CLOSED:
        return _process_jamid_closed(cleaned_word, card)
    if card.path_type == PathType.DENOMINAL_BRANCH:
        return _process_denominal_branch(cleaned_word, card, context, generator, sink)

    return _residual_decision(
        word=cleaned_word,
        context=context,
        sink=sink,
        residuals=(
            *card.residual_entries,
            Residual(
                LexicalFailureCode.PATH_CARD_AMBIGUOUS,
                f"Path type {card.path_type.value!r} is not licensed for derivation in process_lexical_item.",
                ResidualSeverity.DEFERRED,
            ),
        ),
    )


def _process_masdar_path(
    word: str,
    card: PathCard,
    context: Mapping[str, Any],
    generator: VerbGenerator,
    sink: ResidualSink,
) -> LexicalDecision:
    issues = _common_card_issues(card, require_root=True)

    if not card.event_load:
        issues.append(
            Residual(
                LexicalFailureCode.EVENT_LOAD_MISSING,
                "MasdarOpen requires licensed event load.",
            )
        )

    if not card.vowel_pattern:
        issues.append(
            Residual(
                LexicalFailureCode.VOWEL_PATTERN_MISSING,
                "MasdarOpen requires a vowel pattern for verb generation.",
            )
        )

    if card.rank_level < GateRank.HYPOTHESIS:
        issues.append(
            Residual(
                LexicalFailureCode.RANK_TOO_LOW,
                "PathCard rank is too low to generate a verb candidate.",
            )
        )

    if issues:
        return _residual_decision(word, context, sink, tuple(issues))

    try:
        candidate = generator.generate_from_masdar(card)
    except (ValueError, RuntimeError) as exc:  # pragma: no cover - defensive path
        return _residual_decision(
            word,
            context,
            sink,
            (
                Residual(
                    LexicalFailureCode.GENERATOR_FAILED,
                    f"Masdar verb generator failed: {exc.__class__.__name__}: {exc}",
                ),
            ),
        )

    return _candidate_decision(
        word=word,
        context=context,
        sink=sink,
        card=card,
        candidate=candidate,
        expected_kind=DecisionKind.VERB_CANDIDATE,
        max_rank=_rank_ceiling(card.rank_level, GateRank.LICENSED),
        success_message="MasdarOpen opened a licensed verb candidate.",
    )


def _process_jamid_closed(word: str, card: PathCard) -> LexicalDecision:
    issues = _common_card_issues(card, require_root=False)

    if not card.entity_load:
        issues.append(
            Residual(
                LexicalFailureCode.ENTITY_LOAD_MISSING,
                "JamidClosed requires closed entity load.",
            )
        )

    if issues:
        return LexicalDecision(
            kind=DecisionKind.RESIDUAL,
            word=word,
            rank_level=GateRank.RESIDUAL,
            candidate=None,
            residual_entries=_normalize_residuals(tuple(issues)),
            message="JamidClosed could not be closed due to visible residuals.",
        )

    candidate = LexicalCandidate(
        kind=DecisionKind.CLOSED_NOUN,
        surface=word,
        root=card.root,
        rank_level=_rank_ceiling(card.rank_level, GateRank.LICENSED),
        trace=card.trace,
        residual_entries=card.residual_entries,
    )
    return LexicalDecision(
        kind=DecisionKind.CLOSED_NOUN,
        word=word,
        rank_level=candidate.rank_level,
        candidate=candidate,
        residual_entries=_normalize_residuals(card.residual_entries),
        message="JamidClosed blocks original verb generation and closes as noun.",
    )


def _process_denominal_branch(
    word: str,
    card: PathCard,
    context: Mapping[str, Any],
    generator: VerbGenerator,
    sink: ResidualSink,
) -> LexicalDecision:
    issues = _common_card_issues(card, require_root=True)

    if not card.branch_license:
        issues.append(
            Residual(
                LexicalFailureCode.BRANCH_LICENSE_MISSING,
                "DenominalBranch requires an explicit branch license.",
            )
        )

    if card.branch_card is None:
        issues.append(
            Residual(
                LexicalFailureCode.BRANCH_CARD_MISSING,
                "DenominalBranch requires a BranchCard.",
            )
        )
    else:
        if not card.branch_card.trace.is_complete():
            issues.append(
                Residual(
                    LexicalFailureCode.BRANCH_TRACE_MISSING,
                    "BranchCard requires a complete reverse trace.",
                )
            )
        if card.branch_card.initial_rank > GateRank.HYPOTHESIS:
            issues.append(
                Residual(
                    LexicalFailureCode.BRANCH_RANK_INHERITANCE,
                    "A denominal branch cannot inherit the certainty of its origin.",
                )
            )
        if not card.branch_card.is_valid():
            issues.append(
                Residual(
                    LexicalFailureCode.BRANCH_CARD_MISSING,
                    "BranchCard is incomplete or constitutionally invalid.",
                )
            )

    if issues:
        return _residual_decision(word, context, sink, tuple(issues))

    try:
        candidate = generator.generate_from_denominal_branch(card)
    except (ValueError, RuntimeError) as exc:  # pragma: no cover - defensive path
        return _residual_decision(
            word,
            context,
            sink,
            (
                Residual(
                    LexicalFailureCode.GENERATOR_FAILED,
                    f"Denominal branch generator failed: {exc.__class__.__name__}: {exc}",
                ),
            ),
        )

    assert card.branch_card is not None

    return _candidate_decision(
        word=word,
        context=context,
        sink=sink,
        card=card,
        candidate=candidate,
        expected_kind=DecisionKind.DENOMINAL_VERB_CANDIDATE,
        max_rank=min(
            _rank_ceiling(card.rank_level, GateRank.HYPOTHESIS),
            card.branch_card.initial_rank,
        ),
        success_message="DenominalBranch opened a hypothesis-level verb candidate.",
    )


def _common_card_issues(card: PathCard, *, require_root: bool) -> list[Residual]:
    issues: list[Residual] = []

    if not card.trace.is_complete():
        issues.append(
            Residual(
                LexicalFailureCode.TRACE_MISSING,
                "PathCard trace is missing or incomplete.",
            )
        )

    if not card.identity_ref:
        issues.append(
            Residual(
                LexicalFailureCode.IDENTITY_MISSING,
                "PathCard identity reference is missing.",
            )
        )

    if require_root and not card.root:
        issues.append(
            Residual(
                LexicalFailureCode.ROOT_MISSING,
                "Root identity is required for this transition.",
            )
        )

    if card.has_blocking_residuals():
        issues.append(
            Residual(
                LexicalFailureCode.BLOCKING_RESIDUAL_PRESENT,
                "PathCard contains blocking residuals.",
            )
        )
        issues.extend(card.residual_entries)

    return issues


def _candidate_decision(
    *,
    word: str,
    context: Mapping[str, Any],
    sink: ResidualSink,
    card: PathCard,
    candidate: LexicalCandidate,
    expected_kind: DecisionKind,
    max_rank: GateRank,
    success_message: str,
) -> LexicalDecision:
    issues: list[Residual] = []

    if candidate.kind != expected_kind:
        issues.append(
            Residual(
                LexicalFailureCode.GENERATED_KIND_MISMATCH,
                f"Expected {expected_kind.value}, got {candidate.kind.value}.",
            )
        )

    if not candidate.trace.is_complete():
        issues.append(
            Residual(
                LexicalFailureCode.GENERATED_TRACE_MISSING,
                "Generated candidate is missing trace.",
            )
        )

    if candidate.trace.is_complete() and not card.trace.is_parent_of(candidate.trace):
        issues.append(
            Residual(
                LexicalFailureCode.GENERATED_TRACE_BREAK,
                "Generated candidate does not preserve PathCard trace ancestry.",
            )
        )

    if candidate.rank_level > max_rank:
        issues.append(
            Residual(
                LexicalFailureCode.RANK_PROMOTION,
                "Generated candidate rank exceeds the licensed ceiling.",
            )
        )

    if issues:
        return _residual_decision(word, context, sink, tuple(issues))

    return LexicalDecision(
        kind=candidate.kind,
        word=word,
        rank_level=candidate.rank_level,
        candidate=candidate,
        residual_entries=_normalize_residuals((*card.residual_entries, *candidate.residual_entries)),
        message=success_message,
    )


def _residual_decision(
    word: str,
    context: Mapping[str, Any],
    sink: ResidualSink,
    residuals: tuple[Residual, ...],
) -> LexicalDecision:
    visible_residuals = _normalize_residuals(residuals)
    sink.store(word, visible_residuals, context)
    return LexicalDecision(
        kind=DecisionKind.RESIDUAL,
        word=word,
        rank_level=GateRank.RESIDUAL,
        candidate=None,
        residual_entries=visible_residuals,
        message="Lexical item could not be promoted; residuals were recorded visibly.",
    )


def _normalize_residuals(residuals: tuple[Residual, ...]) -> tuple[Residual, ...]:
    seen: set[tuple[str, str, Optional[str], ResidualSeverity]] = set()
    normalized: list[Residual] = []

    for residual in residuals:
        key = (
            str(residual.code),
            residual.message,
            residual.trace_ref,
            residual.severity,
        )
        if key not in seen:
            seen.add(key)
            normalized.append(residual)

    return tuple(normalized)


def _rank_ceiling(rank: GateRank, ceiling: GateRank) -> GateRank:
    return GateRank(min(int(rank), int(ceiling)))


__all__ = [
    "BranchCard",
    "DecisionKind",
    "GateRank",
    "LexicalCandidate",
    "LexicalDecision",
    "LexicalFailureCode",
    "NullResidualSink",
    "PathCard",
    "PathCardRepository",
    "PathType",
    "Residual",
    "ResidualSeverity",
    "ResidualSink",
    "Trace",
    "VerbGenerator",
    "process_lexical_item",
]
