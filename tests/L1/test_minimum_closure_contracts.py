"""Tests for audit-only L1 minimum closure contracts (MRK_L)."""
from __future__ import annotations

from dataclasses import FrozenInstanceError, is_dataclass

import pytest

from taaqqul_slot_geometry.constitution.failure_taxonomy import FailureCode
from taaqqul_slot_geometry.L1.minimum_closure_contracts import (
    EvidenceRequirement,
    MINIMUM_CLOSURE_CARRIERS,
    MINIMUM_CLOSURE_CONTRACT_BY_CARRIER,
    MINIMUM_CLOSURE_CONTRACTS,
    MINIMUM_CLOSURE_CONTRACT_ID,
    MINIMUM_CLOSURE_CONTRACT_VERSION,
    MinimumClosureContract,
    MinimumClosureProbe,
    audit_minimum_closure,
    audit_minimum_closure_for_carrier,
    issue_mrk_proof,
)
from taaqqul_slot_geometry.L1.proof_objects import EvidenceProof, IdentityProof, ProofTrace


def _trace(trace_ref: str, evidence_ref: str) -> ProofTrace:
    return ProofTrace(
        trace_id=f"trace::{evidence_ref}",
        trace_ref=trace_ref,
        steps=("step-1",),
        evidence_refs=(evidence_ref,),
    )


def _evidence_proof(kind: str, carrier_id: str, trace_ref: str, suffix: str) -> EvidenceProof:
    return EvidenceProof(
        proof_id=f"ev-proof::{suffix}",
        proof_kind=kind,
        domain_id=carrier_id,
        checked_gate_ids=("gate-1",),
        checked_bridge_ids=("bridge-1",),
        preserved_identity_refs=("id-1",),
        forbidden_outputs_checked=("runtime_authority",),
        evidence_refs=(f"ev::{suffix}",),
        residual_codes=("NON_BLOCKING",),
        failure_codes=(),
        trace=_trace(trace_ref=trace_ref, evidence_ref=f"ev::{suffix}"),
        trace_ref=trace_ref,
        evidence_scope=("AUDIT",),
        invalidators_checked=("invalidator-1",),
    )


def _identity_proof(kind: str, carrier_id: str, trace_ref: str, suffix: str) -> IdentityProof:
    return IdentityProof(
        proof_id=f"id-proof::{suffix}",
        proof_kind=kind,
        domain_id=carrier_id,
        checked_gate_ids=("gate-1",),
        checked_bridge_ids=("bridge-1",),
        preserved_identity_refs=(kind,),
        forbidden_outputs_checked=("runtime_authority",),
        evidence_refs=(f"id-ev::{suffix}",),
        residual_codes=("NON_BLOCKING",),
        failure_codes=(),
        trace=_trace(trace_ref=trace_ref, evidence_ref=f"id-ev::{suffix}"),
        trace_ref=trace_ref,
    )


def _valid_probe(carrier_kind: str) -> MinimumClosureProbe:
    contract = MINIMUM_CLOSURE_CONTRACT_BY_CARRIER[carrier_kind]
    carrier_id = f"{carrier_kind}-id"
    trace_ref = contract.trace_ref
    evidence_proofs = tuple(
        _evidence_proof(
            kind=requirement.accepted_kinds[0],
            carrier_id=carrier_id,
            trace_ref=trace_ref,
            suffix=f"{carrier_kind}-ev-{index}",
        )
        for index, requirement in enumerate(contract.required_evidence)
    )
    identity_proofs = tuple(
        _identity_proof(
            kind=requirement.identity_kind,
            carrier_id=carrier_id,
            trace_ref=trace_ref,
            suffix=f"{carrier_kind}-id-{index}",
        )
        for index, requirement in enumerate(contract.required_identity)
    )
    return MinimumClosureProbe(
        carrier_kind=carrier_kind,
        carrier_id=carrier_id,
        present_fields=contract.required_fields,
        evidence_proofs=evidence_proofs,
        identity_proofs=identity_proofs,
        residuals=frozenset({"probe_residual"}),
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


@pytest.mark.parametrize("carrier_kind", MINIMUM_CLOSURE_CARRIERS)
def test_valid_probe_meets_carrier_specific_contract(carrier_kind: str) -> None:
    probe = _valid_probe(carrier_kind)
    result = audit_minimum_closure_for_carrier(probe)

    assert result.status == "MINIMUM_CLOSURE_MET"
    assert result.required_fields_met is True
    assert result.required_evidence_met is True
    assert result.identity_requirements_met is True
    assert result.no_blocking_residual is True
    assert result.missing_fields == ()
    assert result.missing_evidence_requirements == ()
    assert result.missing_identity_requirements == ()
    assert result.trace_ref == probe.trace_ref
    assert result.rank == probe.rank
    assert result.residuals == frozenset({"probe_residual"})
    assert result.contract_id == MINIMUM_CLOSURE_CONTRACT_ID
    assert result.contract_version == MINIMUM_CLOSURE_CONTRACT_VERSION


@pytest.mark.parametrize("carrier_kind", MINIMUM_CLOSURE_CARRIERS)
def test_missing_field_fails_contract(carrier_kind: str) -> None:
    base_probe = _valid_probe(carrier_kind)
    missing_field = MINIMUM_CLOSURE_CONTRACT_BY_CARRIER[carrier_kind].required_fields[0]
    probe = MinimumClosureProbe(
        carrier_kind=carrier_kind,
        carrier_id=base_probe.carrier_id,
        present_fields=tuple(f for f in base_probe.present_fields if f != missing_field),
        evidence_proofs=base_probe.evidence_proofs,
        identity_proofs=base_probe.identity_proofs,
        trace_ref=base_probe.trace_ref,
    )
    result = audit_minimum_closure_for_carrier(probe)

    assert result.status == "MINIMUM_CLOSURE_NOT_MET"
    assert missing_field in result.missing_fields


@pytest.mark.parametrize("carrier_kind", MINIMUM_CLOSURE_CARRIERS)
def test_missing_evidence_fails_contract(carrier_kind: str) -> None:
    base_probe = _valid_probe(carrier_kind)
    contract = MINIMUM_CLOSURE_CONTRACT_BY_CARRIER[carrier_kind]
    wrong_kind = "unrelated_evidence_kind"
    probe = MinimumClosureProbe(
        carrier_kind=carrier_kind,
        carrier_id=base_probe.carrier_id,
        present_fields=base_probe.present_fields,
        evidence_proofs=(
            _evidence_proof(
                kind=wrong_kind,
                carrier_id=base_probe.carrier_id,
                trace_ref=base_probe.trace_ref,
                suffix=f"{carrier_kind}-wrong-evidence",
            ),
        ),
        identity_proofs=base_probe.identity_proofs,
        trace_ref=base_probe.trace_ref,
    )
    result = audit_minimum_closure_for_carrier(probe)

    assert result.status == "MINIMUM_CLOSURE_NOT_MET"
    assert result.required_evidence_met is False
    assert result.missing_evidence_requirements == tuple(
        requirement.requirement_id for requirement in contract.required_evidence
    )


@pytest.mark.parametrize("carrier_kind", MINIMUM_CLOSURE_CARRIERS)
def test_missing_identity_proof_fails_contract(carrier_kind: str) -> None:
    base_probe = _valid_probe(carrier_kind)
    contract = MINIMUM_CLOSURE_CONTRACT_BY_CARRIER[carrier_kind]
    probe = MinimumClosureProbe(
        carrier_kind=carrier_kind,
        carrier_id=base_probe.carrier_id,
        present_fields=base_probe.present_fields,
        evidence_proofs=base_probe.evidence_proofs,
        identity_proofs=base_probe.identity_proofs[:-1],
        trace_ref=base_probe.trace_ref,
    )
    result = audit_minimum_closure_for_carrier(probe)

    assert result.status == "MINIMUM_CLOSURE_NOT_MET"
    assert result.identity_requirements_met is False
    assert contract.required_identity[-1].requirement_id in result.missing_identity_requirements


@pytest.mark.parametrize("carrier_kind", MINIMUM_CLOSURE_CARRIERS)
def test_blocking_residual_fails_contract(carrier_kind: str) -> None:
    base_probe = _valid_probe(carrier_kind)
    probe = MinimumClosureProbe(
        carrier_kind=carrier_kind,
        carrier_id=base_probe.carrier_id,
        present_fields=base_probe.present_fields,
        evidence_proofs=base_probe.evidence_proofs,
        identity_proofs=base_probe.identity_proofs,
        trace_ref=base_probe.trace_ref,
        residuals=frozenset({"probe_residual"}),
        blocking_residuals=("BLOCK_1",),
    )
    result = audit_minimum_closure_for_carrier(probe)

    assert result.status == "MINIMUM_CLOSURE_NOT_MET"
    assert result.no_blocking_residual is False
    assert result.blocking_residuals == ("BLOCK_1",)
    assert result.residuals == frozenset({"probe_residual", "BLOCK_1"})


@pytest.mark.parametrize("carrier_kind", MINIMUM_CLOSURE_CARRIERS)
def test_evidence_domain_mismatch_fails_contract(carrier_kind: str) -> None:
    base_probe = _valid_probe(carrier_kind)
    evidence = tuple(
        _evidence_proof(
            kind=requirement.accepted_kinds[0],
            carrier_id="different-subject",
            trace_ref=base_probe.trace_ref,
            suffix=f"{carrier_kind}-domain-mismatch-{index}",
        )
        for index, requirement in enumerate(
            MINIMUM_CLOSURE_CONTRACT_BY_CARRIER[carrier_kind].required_evidence
        )
    )
    probe = MinimumClosureProbe(
        carrier_kind=carrier_kind,
        carrier_id=base_probe.carrier_id,
        present_fields=base_probe.present_fields,
        evidence_proofs=evidence,
        identity_proofs=base_probe.identity_proofs,
        trace_ref=base_probe.trace_ref,
    )
    result = audit_minimum_closure_for_carrier(probe)

    assert result.status == "MINIMUM_CLOSURE_NOT_MET"
    assert result.required_evidence_met is False


@pytest.mark.parametrize("carrier_kind", MINIMUM_CLOSURE_CARRIERS)
def test_identity_subject_mismatch_fails_contract(carrier_kind: str) -> None:
    base_probe = _valid_probe(carrier_kind)
    identity = tuple(
        _identity_proof(
            kind=requirement.identity_kind,
            carrier_id="different-subject",
            trace_ref=base_probe.trace_ref,
            suffix=f"{carrier_kind}-identity-mismatch-{index}",
        )
        for index, requirement in enumerate(
            MINIMUM_CLOSURE_CONTRACT_BY_CARRIER[carrier_kind].required_identity
        )
    )
    probe = MinimumClosureProbe(
        carrier_kind=carrier_kind,
        carrier_id=base_probe.carrier_id,
        present_fields=base_probe.present_fields,
        evidence_proofs=base_probe.evidence_proofs,
        identity_proofs=identity,
        trace_ref=base_probe.trace_ref,
    )
    result = audit_minimum_closure_for_carrier(probe)

    assert result.status == "MINIMUM_CLOSURE_NOT_MET"
    assert result.identity_requirements_met is False


@pytest.mark.parametrize("carrier_kind", MINIMUM_CLOSURE_CARRIERS)
def test_disconnected_trace_fails_contract(carrier_kind: str) -> None:
    base_probe = _valid_probe(carrier_kind)
    disconnected_trace_ref = "docs/99_other_trace.md"
    evidence = tuple(
        _evidence_proof(
            kind=requirement.accepted_kinds[0],
            carrier_id=base_probe.carrier_id,
            trace_ref=disconnected_trace_ref,
            suffix=f"{carrier_kind}-trace-mismatch-{index}",
        )
        for index, requirement in enumerate(
            MINIMUM_CLOSURE_CONTRACT_BY_CARRIER[carrier_kind].required_evidence
        )
    )
    probe = MinimumClosureProbe(
        carrier_kind=carrier_kind,
        carrier_id=base_probe.carrier_id,
        present_fields=base_probe.present_fields,
        evidence_proofs=evidence,
        identity_proofs=base_probe.identity_proofs,
        trace_ref=base_probe.trace_ref,
    )
    result = audit_minimum_closure_for_carrier(probe)

    assert result.status == "MINIMUM_CLOSURE_NOT_MET"
    assert result.required_evidence_met is False


def test_rank_promotion_is_rejected() -> None:
    base_probe = _valid_probe("SoundUnitCandidate")
    with pytest.raises(ValueError, match=FailureCode.M_01_16.value):
        MinimumClosureProbe(
            carrier_kind=base_probe.carrier_kind,
            carrier_id=base_probe.carrier_id,
            present_fields=base_probe.present_fields,
            evidence_proofs=base_probe.evidence_proofs,
            identity_proofs=base_probe.identity_proofs,
            rank="CERTIFICATE",  # type: ignore[arg-type]
        )


def test_claimed_identity_without_identity_proofs_is_rejected() -> None:
    base_probe = _valid_probe("SoundUnitCandidate")
    with pytest.raises(ValueError, match=FailureCode.M_CX_30.value):
        MinimumClosureProbe(
            carrier_kind=base_probe.carrier_kind,
            carrier_id=base_probe.carrier_id,
            present_fields=base_probe.present_fields,
            evidence_proofs=base_probe.evidence_proofs,
            identity_proofs=(),
            claimed_identity_kinds=("TraceIdentity",),
        )


def test_empty_identity_proofs_without_claims_is_auditable() -> None:
    base_probe = _valid_probe("SoundUnitCandidate")
    probe = MinimumClosureProbe(
        carrier_kind=base_probe.carrier_kind,
        carrier_id=base_probe.carrier_id,
        present_fields=base_probe.present_fields,
        evidence_proofs=base_probe.evidence_proofs,
        identity_proofs=(),
        trace_ref=base_probe.trace_ref,
    )
    result = audit_minimum_closure_for_carrier(probe)

    assert result.status == "MINIMUM_CLOSURE_NOT_MET"
    assert result.identity_requirements_met is False
    assert FailureCode.M_CX_30 in result.failure_codes


def test_contract_probe_carrier_mismatch_is_rejected() -> None:
    contract = MINIMUM_CLOSURE_CONTRACT_BY_CARRIER["LetterUnitCandidate"]
    with pytest.raises(ValueError, match=FailureCode.M_CX_02.value):
        audit_minimum_closure(contract, _valid_probe("SoundUnitCandidate"))


def test_issue_mrk_proof_from_successful_result() -> None:
    probe = _valid_probe("SoundUnitCandidate")
    contract = MINIMUM_CLOSURE_CONTRACT_BY_CARRIER[probe.carrier_kind]
    result = audit_minimum_closure(contract, probe)

    proof = issue_mrk_proof(contract=contract, audit_result=result, probe=probe)

    assert proof.proof_kind == MINIMUM_CLOSURE_CONTRACT_ID
    assert proof.domain_id == probe.carrier_id
    assert proof.rank == "CANDIDATE"
    assert proof.trace_ref == probe.trace_ref


def test_issue_mrk_proof_requires_met_status() -> None:
    probe = _valid_probe("SoundUnitCandidate")
    contract = MINIMUM_CLOSURE_CONTRACT_BY_CARRIER[probe.carrier_kind]
    failed_probe = MinimumClosureProbe(
        carrier_kind=probe.carrier_kind,
        carrier_id=probe.carrier_id,
        present_fields=probe.present_fields,
        evidence_proofs=probe.evidence_proofs,
        identity_proofs=probe.identity_proofs,
        trace_ref=probe.trace_ref,
        blocking_residuals=("BLOCK_1",),
    )
    failed_result = audit_minimum_closure(contract, failed_probe)

    with pytest.raises(ValueError, match=FailureCode.M_00_22.value):
        issue_mrk_proof(contract=contract, audit_result=failed_result, probe=failed_probe)


def test_issue_mrk_proof_rejects_carrier_mismatch() -> None:
    probe = _valid_probe("SoundUnitCandidate")
    sound_contract = MINIMUM_CLOSURE_CONTRACT_BY_CARRIER[probe.carrier_kind]
    result = audit_minimum_closure(sound_contract, probe)
    mismatched_contract = MINIMUM_CLOSURE_CONTRACT_BY_CARRIER["LetterUnitCandidate"]

    with pytest.raises(ValueError, match=FailureCode.M_CX_02.value):
        issue_mrk_proof(contract=mismatched_contract, audit_result=result, probe=probe)


def test_issue_mrk_proof_filters_mismatched_envelope_proofs() -> None:
    probe = _valid_probe("SoundUnitCandidate")
    contract = MINIMUM_CLOSURE_CONTRACT_BY_CARRIER[probe.carrier_kind]
    result = audit_minimum_closure(contract, probe)

    mismatched_evidence = _evidence_proof(
        kind=contract.required_evidence[0].accepted_kinds[0],
        carrier_id="other-carrier",
        trace_ref=probe.trace_ref,
        suffix="mismatched-evidence",
    )
    mismatched_identity = _identity_proof(
        kind="NonRequiredIdentity",
        carrier_id="other-carrier",
        trace_ref=probe.trace_ref,
        suffix="mismatched-identity",
    )
    proof = issue_mrk_proof(
        contract=contract,
        audit_result=result,
        probe=MinimumClosureProbe(
            carrier_kind=probe.carrier_kind,
            carrier_id=probe.carrier_id,
            present_fields=probe.present_fields,
            evidence_proofs=probe.evidence_proofs + (mismatched_evidence,),
            identity_proofs=probe.identity_proofs + (mismatched_identity,),
            trace_ref=probe.trace_ref,
            residuals=probe.residuals,
        ),
    )

    assert "ev::mismatched-evidence" not in proof.evidence_refs
    assert contract.required_identity[0].identity_kind in proof.preserved_identity_refs
    assert "NonRequiredIdentity" not in proof.preserved_identity_refs


def test_evidence_requirement_minimum_matches_semantics() -> None:
    base_probe = _valid_probe("SoundUnitCandidate")
    base_contract = MINIMUM_CLOSURE_CONTRACT_BY_CARRIER[base_probe.carrier_kind]
    at_least_two_contract = MinimumClosureContract(
        carrier_kind=base_contract.carrier_kind,
        required_fields=base_contract.required_fields,
        required_evidence=(
            EvidenceRequirement(
                requirement_id="two_of_two_required",
                accepted_kinds=("kind-a", "kind-b"),
                minimum_matches=2,
            ),
        ),
        required_identity=base_contract.required_identity,
    )
    matching_probe = MinimumClosureProbe(
        carrier_kind=base_probe.carrier_kind,
        carrier_id=base_probe.carrier_id,
        present_fields=base_probe.present_fields,
        evidence_proofs=(
            _evidence_proof("kind-a", base_probe.carrier_id, base_probe.trace_ref, "kinda"),
            _evidence_proof("kind-b", base_probe.carrier_id, base_probe.trace_ref, "kindb"),
        ),
        identity_proofs=base_probe.identity_proofs,
        trace_ref=base_probe.trace_ref,
    )
    one_match_probe = MinimumClosureProbe(
        carrier_kind=base_probe.carrier_kind,
        carrier_id=base_probe.carrier_id,
        present_fields=base_probe.present_fields,
        evidence_proofs=(_evidence_proof("kind-a", base_probe.carrier_id, base_probe.trace_ref, "kinda"),),
        identity_proofs=base_probe.identity_proofs,
        trace_ref=base_probe.trace_ref,
    )

    assert audit_minimum_closure(at_least_two_contract, matching_probe).status == "MINIMUM_CLOSURE_MET"
    failing_result = audit_minimum_closure(at_least_two_contract, one_match_probe)
    assert failing_result.status == "MINIMUM_CLOSURE_NOT_MET"
    assert failing_result.missing_evidence_requirements == ("two_of_two_required",)
