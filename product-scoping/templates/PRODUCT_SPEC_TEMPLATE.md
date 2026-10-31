# Product Spec — [Product or Feature Area]

*Lives in `specs/product/`. What the product does for its users today and why. No internal implementation detail; that belongs in `specs/engineering/`.*

## Users & Goals

- **Who**: [Primary user role/audience and context in which they arrive]
- **Goals**: [What they come to accomplish; outcome when successful]

## Core Hypothesis

- **Hypothesis**: [The one belief that, if false, makes this not worth building]
- **Hypothesis Metric**: [Metric] — continue if [≥ threshold]; rethink if below.
- **P0 Journeys**: [F1, …]

## Metrics

### 1. Usage & Adoption Metrics
*Mostly supplied by the analytics platform; name the events.*
- **Onboarding & Activation**: [Activation event, time to first value]
- **Feature Usage**: [One view + one primary-action event per P0–P2 capability]
- **Engagement & Retention**: [Active users, W1 and W4 cohort retention]

### 2. Feature Success Metrics
*End-to-end funnel conversion showing each flow solved the user's problem.*
- **[F1 funnel]**: [Start event → completion event conversion]

### 3. Production Quality & Reliability Metrics
*Live quality and health signals in production.*
- **Output Quality**: [Implicit quality signals, e.g. user edit rate on generated output, empty/fallback rate]
- **System Reliability**: [p50/p95 latency, timeout/error rate]

### 4. Pre-Release QA & Offline Eval Metrics
*Offline gates verified before shipping.*
- **Offline Eval**: [e.g. $\ge 90\%$ accuracy on golden fixtures; $0\%$ fabricated fields on negative fixtures]
- **Deterministic Gates**: [e.g. $100\%$ pass rate on `T1..Tn` logic tests]

## Scope & Priorities

*Ranked by hypothesis risk and unlock, not setup order. `loop-engineering` builds P0 → P1 → P2.*

### P0 — Hypothesis Journeys
- **[Capability]**: [Why it is P0]

### P1 — Worth a Second Use
- **[Capability]**: [Why it is P1] *(downgraded: [cheaper mechanism now]; full version in P2)*

### P2 — Planned, Built Last
- **[Capability]**: [Why it is P2]

### Deferred (Next Milestone)
- **10-Star Experience**: [The end goal if everything works. Direction, not scope.]
- **[Capability from request]**: [Complexity avoided]

### Non-Goals
- **[Excluded Capability]**: [What this product deliberately does not do]

## Key User Flows ($F_1..F_m$)

*Priority order: P0 flows first, starting at F1. Every header carries its tier. `loop-engineering` derives automated ($T_1..T_n$) and manual E2E ($M_1..M_k$) tests from these.*

### F1 — [P0 Journey Name] [P0]
- **Actor & Precondition**: [Who is acting and what state exists before starting]
- **Steps**:
  1. [User action] $\to$ [Observable system response]
  2. [User action] $\to$ [Observable system response]
- **Expected End State**: [Final user-visible state and persisted outcome]
- **Edge & Failure Cases**:
  - *Empty / Cold Start*: [Behavior when zero records/data exist]
  - *Invalid / Boundary Input*: [Validation error and recovery path]
  - *Failure Recovery*: [What the user sees and can do if an operation fails]

### F2 — [Flow Name] [P1]
- **Actor & Precondition**: [...]
- **Steps**:
  1. [User action] $\to$ [Observable system response]
- **Expected End State**: [...]
- **Edge & Failure Cases**: [...]

## UI Design & Mocks

*Populated during the iterative UI design phase (via `product-design`) after the PRD text is written. Embed approved screen mock screenshots and visual direction notes here.*

- **Design Direction**: [Typography, palette, layout structure chosen]
- **Screen Mocks**:
  - `[Screen 1 Name]`: `![Screen 1 Mock](mocks/screen-1.png)` — `[mock HTML/source path]`

## Constraints

- [Non-negotiables: performance bounds, auth/permissions, platform support, accessibility]

## Known Gaps

- [Scoped requirements or flows not yet met by shipped code. Remove when fixed.]
