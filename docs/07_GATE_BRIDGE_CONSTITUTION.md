# Gate and Bridge Constitution — `docs/07_GATE_BRIDGE_CONSTITUTION.md`

## Authority
Derived from `docs/00_MAQOOL_CONSTITUTION.md §5 Rule 6-9` and `docs/05_DOMAIN_REGISTRY_CONSTITUTION.md`.

## Gate/Bridge Contract Law

No gate without executable predicate.
No bridge without identity-preserving translator.

Each gate/bridge contract must declare:
- gate_id / bridge_id
- source_domain
- target_domain
- source_contract
- target_contract
- allowed_operation
- forbidden_outputs
- invariants
- proof_obligations
- failure_code
- residual_code
- trace_requirements

A bridge name alone is invalid.
Bridge legality requires executable identity-preserving translation plus BridgeProof.
