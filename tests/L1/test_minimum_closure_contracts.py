"""Tests for audit-only L1 minimum closure contracts (MRK_L)."""
from __future__ import annotations

from dataclasses import FrozenInstanceError, is_dataclass

import pytest

from taaqqul_slot_geometry.constitution.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.L1.minimum_closure_contracts import (
    MINIMUM_CLOSURE_CARRIERS,
    MINIMUM_CLOSURE_CONTRACT_BY_CARRIER,
    MINIMUM_CLOSURE_CONTRACTS,
    MinimumClosureProbe,
    audit_minimum_closure,
    audit_minimum_closure_for_carrier,
)


def _sound_probe() -> MinimumClosureProbe:
    return MinimumClosureProbe(
        carrier_kind="SoundUnitCandidate",
        present_fields=("sound_unit_id", "trace_ref", "rank", "residuals"),
        present_evidence=("sensory_evidence",),
        preserved_identity=("TraceIdentity", "PhonemicIdentity"),
    )


def test_registry_covers_all_declared_carriers() -> None:
    assert tuple(contract.carrier_kind for contract in MINIMUM_CLOSURE_CONTRACTS) == (
        MINIMUM_CLOSURE_CARRIERS
    )
    assert set(MINIMUM_CLOSURE_CONTRACT_BY_CARRIER) == set(MINIMUM_CLOSURE_CARRIERS)


def test_contracts_are_frozen_dataclasses() -> None:
    for contract in MINIMUM_CLOSURE_CONTRACTS:
        assert is_dataclass(contract)
        with pytest.raises(FrozenInstanceError):
            contract.rank = "CERTIFICATE"  # type: ignore[misc]


def test_rank_promotion_is_rejected() -> None:
    with pytest.raises(ValueError, match=FailureCode.M_01_16.value):
        MinimumClosureProbe(
            carrier_kind="SoundUnitCandidate",
            present_fields=("sound_unit_id", "trace_ref", "rank", "residuals"),
            present_evidence=("sensory_evidence",),
            preserved_identity=("TraceIdentity", "PhonemicIdentity"),
            rank="CERTIFICATE",  # type: ignore[arg-type]
        )


def test_valid_probe_meets_minimum_closure() -> None:
    result = audit_minimum_closure_for_carrier(_sound_probe())
    assert result.status == "MINIMUM_CLOSURE_MET"
    assert result.required_fields_met is True
    assert result.required_evidence_met is True
    assert result.identity_preserved is True
    assert result.no_blocking_residual is True
    assert result.missing_fields == ()
    assert result.missing_evidence == ()
    assert result.missing_identity == ()


def test_missing_field_fails_minimum_closure() -> None:
    probe = MinimumClosureProbe(
        carrier_kind="SoundUnitCandidate",
        present_fields=("trace_ref", "rank", "residuals"),
        present_evidence=("sensory_evidence",),
        preserved_identity=("TraceIdentity", "PhonemicIdentity"),
    )
    result = audit_minimum_closure_for_carrier(probe)
    assert result.status == "MINIMUM_CLOSURE_NOT_MET"
    assert result.required_fields_met is False
    assert "sound_unit_id" in result.missing_fields


def test_missing_evidence_fails_minimum_closure() -> None:
    probe = MinimumClosureProbe(
        carrier_kind="SoundUnitCandidate",
        present_fields=("sound_unit_id", "trace_ref", "rank", "residuals"),
        present_evidence=("written_evidence",),
        preserved_identity=("TraceIdentity", "PhonemicIdentity"),
    )
    result = audit_minimum_closure_for_carrier(probe)
    assert result.status == "MINIMUM_CLOSURE_NOT_MET"
    assert result.required_evidence_met is False
    assert "sensory_evidence" in result.missing_evidence


def test_missing_identity_fails_minimum_closure() -> None:
    probe = MinimumClosureProbe(
        carrier_kind="SoundUnitCandidate",
        present_fields=("sound_unit_id", "trace_ref", "rank", "residuals"),
        present_evidence=("sensory_evidence",),
        preserved_identity=("TraceIdentity",),
    )
    result = audit_minimum_closure_for_carrier(probe)
    assert result.status == "MINIMUM_CLOSURE_NOT_MET"
    assert result.identity_preserved is False
    assert "PhonemicIdentity" in result.missing_identity


def test_blocking_residual_fails_minimum_closure() -> None:
    probe = MinimumClosureProbe(
        carrier_kind="SoundUnitCandidate",
        present_fields=("sound_unit_id", "trace_ref", "rank", "residuals"),
        present_evidence=("sensory_evidence",),
        preserved_identity=("TraceIdentity", "PhonemicIdentity"),
        blocking_residuals=("M_00_22",),
    )
    result = audit_minimum_closure_for_carrier(probe)
    assert result.status == "MINIMUM_CLOSURE_NOT_MET"
    assert result.no_blocking_residual is False
    assert "M_00_22" in result.residuals


def test_contract_probe_carrier_mismatch_is_rejected() -> None:
    contract = MINIMUM_CLOSURE_CONTRACT_BY_CARRIER["LetterUnitCandidate"]
    with pytest.raises(ValueError, match=FailureCode.M_CX_02.value):
        audit_minimum_closure(contract, _sound_probe())
