# Product Spec — [Product or Feature Area]

*Lives in `specs/product/`. What the product does for its users today and why. No internal implementation detail; that belongs in `specs/engineering/`.*

## Users, Goals & Success Metrics

- **Who**: [Primary user role/audience and context in which they arrive]
- **Goals**: [What they come to accomplish; outcome when successful]
- **Success Metrics**:
  - **[Metric 1]**: `[Target / threshold]` — measured via `[observable signal, timing, or event]`
  - **[Metric 2]**: `[Target / threshold]` — measured via `[observable signal, timing, or event]`

## Scope & Feature Prioritization

### Core (In Scope)
- **[Capability 1]**: [User-facing capability required for the primary flow]
- **[Capability 2]**: [User-facing capability required for the primary flow]

### Deferred (Next Milestone)
- **[Deferred Capability]**: [Why deferred — specific complexity multiplier avoided now]

### Non-Goals (Out of Scope)
- **[Excluded Capability]**: [What this product deliberately does not do]

## Key User Flows ($F_1..F_m$)

*Used directly by `loop-engineering` to generate automated ($T_1..T_n$) and manual E2E ($M_1..M_k$) test matrices.*

### F1 — [Primary Flow Name]
- **Actor & Precondition**: [Who is acting and what state exists before starting]
- **Steps**:
  1. [User action] $\to$ [Observable system response]
  2. [User action] $\to$ [Observable system response]
- **Expected End State**: [Final user-visible state and persisted outcome]
- **Edge & Failure Cases**:
  - *Empty / Cold Start*: [Behavior when zero records/data exist]
  - *Invalid / Boundary Input*: [Validation error and recovery path]
  - *Failure Recovery*: [What the user sees and can do if an operation fails]

### F2 — [Secondary / Alternate Flow Name]
- **Actor & Precondition**: [...]
- **Steps**:
  1. [User action] $\to$ [Observable system response]
- **Expected End State**: [...]
- **Edge & Failure Cases**: [...]

## Constraints

- [Non-negotiables: performance bounds, auth/permissions, platform support, accessibility]

## Known Gaps

- [Scoped requirements or flows not yet met by shipped code. Remove when fixed.]
