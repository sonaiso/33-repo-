"""Tests for audit-only lexical path gate contracts."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Optional

from taaqqul_slot_geometry.core.lexical_path_gate import (
    BranchCard,
    DecisionKind,
    GateRank,
    LexicalCandidate,
    LexicalFailureCode,
    NullResidualSink,
    PathCard,
    PathCardRepository,
    PathType,
    Residual,
    ResidualSeverity,
    Trace,
    VerbGenerator,
    process_lexical_item,
)


@dataclass
class _StaticRepo(PathCardRepository):
    card: Optional[PathCard]

    def get_path_card(self, word: str, context: Mapping[str, Any]) -> Optional[PathCard]:
        return self.card


@dataclass
class _StubGenerator(VerbGenerator):
    masdar_candidate: LexicalCandidate
    branch_candidate: LexicalCandidate

    def generate_from_masdar(self, card: PathCard) -> LexicalCandidate:
        return self.masdar_candidate

    def generate_from_denominal_branch(self, card: PathCard) -> LexicalCandidate:
        return self.branch_candidate


class _RecordingSink(NullResidualSink):
    def __init__(self) -> None:
        self.calls: list[tuple[str, tuple[Residual, ...], Mapping[str, Any]]] = []

    def store(
        self,
        word: str,
        residuals: tuple[Residual, ...],
        context: Mapping[str, Any],
    ) -> None:
        self.calls.append((word, residuals, context))


class _FailingGenerator(VerbGenerator):
    def generate_from_masdar(self, card: PathCard) -> LexicalCandidate:
        raise RuntimeError("masdar failed")

    def generate_from_denominal_branch(self, card: PathCard) -> LexicalCandidate:
        raise ValueError("branch failed")


def _trace(*refs: str) -> Trace:
    return Trace(refs=refs)


def _candidate(kind: DecisionKind, rank_level: GateRank, trace: Trace) -> LexicalCandidate:
    return LexicalCandidate(
        kind=kind,
        surface="سَطْح",
        root=("ك", "ت", "ب"),
        rank_level=rank_level,
        trace=trace,
    )


def test_empty_word_emits_visible_residual_and_sink_record() -> None:
    sink = _RecordingSink()
    decision = process_lexical_item(
        "   ",
        {},
        card_repo=_StaticRepo(None),
        generator=_StubGenerator(
            _candidate(DecisionKind.VERB_CANDIDATE, GateRank.HYPOTHESIS, _trace("a")),
            _candidate(DecisionKind.DENOMINAL_VERB_CANDIDATE, GateRank.HYPOTHESIS, _trace("a", "b")),
        ),
        residual_sink=sink,
    )

    assert decision.kind == DecisionKind.RESIDUAL
    assert decision.residual_entries[0].code == LexicalFailureCode.PATH_CARD_MISSING
    assert len(sink.calls) == 1


def test_jamid_closed_returns_structured_closed_noun() -> None:
    card = PathCard(
        word="جامد",
        path_type=PathType.JAMID_CLOSED,
        trace=_trace("l0", "l1"),
        rank_level=GateRank.LICENSED,
        identity_ref="id-1",
        entity_load=True,
    )

    decision = process_lexical_item(
        "جامد",
        {},
        card_repo=_StaticRepo(card),
        generator=_StubGenerator(
            _candidate(DecisionKind.VERB_CANDIDATE, GateRank.HYPOTHESIS, _trace("l0", "l1", "l2")),
            _candidate(DecisionKind.DENOMINAL_VERB_CANDIDATE, GateRank.HYPOTHESIS, _trace("l0", "l1", "l2")),
        ),
    )

    assert decision.kind == DecisionKind.CLOSED_NOUN
    assert decision.candidate is not None
    assert decision.candidate.kind == DecisionKind.CLOSED_NOUN


def test_masdar_open_requires_gate_inputs() -> None:
    card = PathCard(
        word="مصدر",
        path_type=PathType.MASDAR_OPEN,
        trace=_trace("l0", "l1"),
        rank_level=GateRank.HYPOTHESIS,
        identity_ref="id-2",
        root=("ك", "ت", "ب"),
        event_load=False,
        vowel_pattern=None,
    )

    decision = process_lexical_item(
        "مصدر",
        {},
        card_repo=_StaticRepo(card),
        generator=_StubGenerator(
            _candidate(DecisionKind.VERB_CANDIDATE, GateRank.HYPOTHESIS, _trace("l0", "l1", "l2")),
            _candidate(DecisionKind.DENOMINAL_VERB_CANDIDATE, GateRank.HYPOTHESIS, _trace("l0", "l1", "l2")),
        ),
    )

    assert decision.kind == DecisionKind.RESIDUAL
    codes = {item.code for item in decision.residual_entries}
    assert LexicalFailureCode.EVENT_LOAD_MISSING in codes
    assert LexicalFailureCode.VOWEL_PATTERN_MISSING in codes


def test_denominal_branch_caps_to_hypothesis() -> None:
    branch = BranchCard(
        branch_id="b-1",
        origin_ref="origin",
        residual_source="audit",
        license_ref="lic-1",
        trace=_trace("l0", "l1", "branch"),
        initial_rank=GateRank.HYPOTHESIS,
    )
    card = PathCard(
        word="اشتقاق",
        path_type=PathType.DENOMINAL_BRANCH,
        trace=_trace("l0", "l1"),
        rank_level=GateRank.LICENSED,
        identity_ref="id-3",
        root=("ك", "ت", "ب"),
        branch_license=True,
        branch_card=branch,
    )

    decision = process_lexical_item(
        "اشتقاق",
        {},
        card_repo=_StaticRepo(card),
        generator=_StubGenerator(
            _candidate(DecisionKind.VERB_CANDIDATE, GateRank.HYPOTHESIS, _trace("l0", "l1", "l2")),
            _candidate(
                DecisionKind.DENOMINAL_VERB_CANDIDATE,
                GateRank.HYPOTHESIS,
                _trace("l0", "l1", "branch", "l2"),
            ),
        ),
    )

    assert decision.kind == DecisionKind.DENOMINAL_VERB_CANDIDATE
    assert decision.rank_level <= GateRank.HYPOTHESIS


def test_blocking_residuals_are_visible_and_deduplicated() -> None:
    duplicate = Residual(
        LexicalFailureCode.BLOCKING_RESIDUAL_PRESENT,
        "duplicate",
        ResidualSeverity.BLOCKING,
    )
    card = PathCard(
        word="ملتبس",
        path_type=PathType.MUSHTAQ_OPEN,
        trace=_trace("l0", "l1"),
        rank_level=GateRank.HYPOTHESIS,
        identity_ref="id-4",
        residual_entries=(duplicate, duplicate),
    )
    sink = _RecordingSink()

    decision = process_lexical_item(
        "ملتبس",
        {},
        card_repo=_StaticRepo(card),
        generator=_StubGenerator(
            _candidate(DecisionKind.VERB_CANDIDATE, GateRank.HYPOTHESIS, _trace("l0", "l1", "l2")),
            _candidate(DecisionKind.DENOMINAL_VERB_CANDIDATE, GateRank.HYPOTHESIS, _trace("l0", "l1", "l2")),
        ),
        residual_sink=sink,
    )

    assert decision.kind == DecisionKind.RESIDUAL
    assert len(decision.residual_entries) == 2
    assert any(item.code == LexicalFailureCode.PATH_CARD_AMBIGUOUS for item in decision.residual_entries)
    assert len(sink.calls) == 1


def test_ambiguous_residual_spelling_is_canonical() -> None:
    assert PathType.AMBIGUOUS_RESIDUAL.value == "AmbiguousResidual"


def test_masdar_generator_failure_becomes_visible_residual() -> None:
    card = PathCard(
        word="مصدر",
        path_type=PathType.MASDAR_OPEN,
        trace=_trace("l0", "l1"),
        rank_level=GateRank.HYPOTHESIS,
        identity_ref="id-5",
        root=("ك", "ت", "ب"),
        event_load=True,
        vowel_pattern="فَعَلَ",
    )
    sink = _RecordingSink()

    decision = process_lexical_item(
        "مصدر",
        {},
        card_repo=_StaticRepo(card),
        generator=_FailingGenerator(),
        residual_sink=sink,
    )

    assert decision.kind == DecisionKind.RESIDUAL
    assert decision.residual_entries[0].code == LexicalFailureCode.GENERATOR_FAILED
    assert len(sink.calls) == 1


def test_denominal_generator_failure_becomes_visible_residual() -> None:
    card = PathCard(
        word="اشتقاق",
        path_type=PathType.DENOMINAL_BRANCH,
        trace=_trace("l0", "l1"),
        rank_level=GateRank.HYPOTHESIS,
        identity_ref="id-6",
        root=("ك", "ت", "ب"),
        branch_license=True,
        branch_card=BranchCard(
            branch_id="b-2",
            origin_ref="origin",
            residual_source="audit",
            license_ref="lic-2",
            trace=_trace("l0", "l1", "branch"),
        ),
    )
    sink = _RecordingSink()

    decision = process_lexical_item(
        "اشتقاق",
        {},
        card_repo=_StaticRepo(card),
        generator=_FailingGenerator(),
        residual_sink=sink,
    )

    assert decision.kind == DecisionKind.RESIDUAL
    assert decision.residual_entries[0].code == LexicalFailureCode.GENERATOR_FAILED
    assert len(sink.calls) == 1
