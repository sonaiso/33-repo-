# L0 Weight Transition Barrier Mapping Law — `docs/64`

Origin: `docs/00_MAQOOL_CONSTITUTION.md` §5 Rule 8; `docs/15_PROJECT_ROADMAP.md`; `docs/20_AGENT_AUTONOMY_RUNBOOK.md`

## Constitutional status

Runtime status: `AUDIT_ONLY`.
L0 is closed.
L1 is contract/audit bounded.
L2 remains locked.
L3 remains locked.
Runtime embargo remains active.

## One auditable claim

The current repository contains an L0 weight layer (`L0/weight.py` and `core/arabic_weight_pattern.py`) and a licensed transition barrier chain (`core/transition_registry.py`) that ends at `MUFRAD`.
No transition law in the current registry opens semantic/runtime outputs such as `Ifadah`, `Hukm`, or `Tanzil`.

## Official mapping (current tree only)

| Concern | Implemented source | Barrier evidence | Constitutional effect |
|---|---|---|---|
| L0 weight entity | `src/taaqqul_slot_geometry/L0/weight.py` | `rank = "CANDIDATE"`, named `FailureCode` guards | Weight remains pre-semantic candidate only |
| Weight pattern registry | `src/taaqqul_slot_geometry/core/arabic_weight_pattern.py` | TH7/TH8 structural hints only, no verdict output | No direct semantic/hukm/tanzil authority |
| Transition barrier chain | `src/taaqqul_slot_geometry/core/transition_registry.py` | `TransitionLayer` terminates at `MUFRAD`; laws are adjacent and licensed | No layer leap to locked layers |
| Anti-promotion law | `docs/63_SLOT_GEOMETRY_EUCLIDEAN_GRADATION_LAW.md` | `Weight ⇏ Hukm`, `Ifadah ⇏ Truth` | Prevents shortcut from morphology to final judgment |

## Forbidden drift under this law

The repository must not introduce runtime-by-name borrowing from tracks that are not present in this tree unless roadmap/constitutional docs are explicitly amended first.

Examples of forbidden name drift in source code under current roadmap state:
- `LAFZI-D6`
- `coupled_dalalah`
- `x0r`

This is a guard against accidental cross-repository import assumptions, not a runtime opening.

## Scope

- Declare and freeze the current mapping between L0 weight and transition barriers that actually exist in this repository.
- Add audit-only tests that prove no semantic jump (`Ifadah/Hukm/Tanzil`) is opened from current transition laws.
- Add source-level guard against importing non-existent external track names before constitutional roadmap amendment.

## Non-scope

- No runtime engine.
- No decision engine.
- No kernel.
- No computed verdict runtime.
- No opening of L2/L3.
- No introduction of `LAFZI-D6`, `coupled_dalalah`, or `x0r` modules in current source tree.

*End of L0 Weight Transition Barrier Mapping Law.*
