# Milestone NN — [Milestone Name]

*Built from [`specs/product/<slug>.md`](../../specs/product/<slug>.md). Every unit below has a contract in `units/`. Order: walking skeleton → P0 → P1 → P2 → reporting. Validate with `check_loop.py plan`.*

## Target End State

[What the user can do once every unit has shipped.]

## Build Sequence

| # | Unit | Type | Serves | Tier | Status |
| :-- | :--- | :--- | :--- | :--- | :--- |
| 01 | Walking skeleton + load-bearing decisions | infra | all | P0 | todo |
| 02 | [Infra the P0 journey needs] | infra | F1 | P0 | todo |
| 03 | [P0 journey] | journey | F1 | P0 | todo |
| 04 | [P1 journey] | journey | F2 | P1 | todo |
| 05 | [P2 journey] | journey | F3 | P2 | todo |
| 06 | Analytics dashboard & reports | reporting | all | — | todo |

*`Type`: infra · journey · reporting. `Serves`: flow ids, or `all`. `Tier` = most important tier among the flows served. **P0 checkpoint** comes after the last P0 unit.*

## Load-Bearing Decisions

*Made in the skeleton because later tiers would be expensive to retrofit (data scoping key, ID scheme, sync model, auth seam).*
- [Decision] — [ADR link] — protects [later unit/flow]

## Migration Matrix

*(Omit if no data or schema migrations.)*

## Notes

- [Manual testing notes, observations, re-prioritizations after the P0 checkpoint]
