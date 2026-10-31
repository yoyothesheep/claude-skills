# Product Spec — [Product or Feature Area]

*Lives in `specs/product/`. What the product does for its users today and why. No internal implementation detail; that belongs in `specs/engineering/`.*

## Users & Goals

- **Who**: [Primary user role/audience and context in which they arrive]
- **Goals**: [What they come to accomplish; outcome when successful]

## Metrics

### 1. Usage & Adoption Metrics
*Onboarding, screen/feature depth, and retention telemetry.*
- **Onboarding & Activation**: [e.g., Workspace creation/join rate, multi-member join rate, Time to First Value (TTFV)]
- **Key Screen & Feature Usage**: [e.g., Views and primary actions across each core screen/feature]
- **Engagement & Retention**: [e.g., DAU/WAU/WAF, W1 and W4 cohort retention]

### 2. Feature Success Metrics
*End-to-end funnel conversion and user-value signals showing the workflow solved the user's problem.*
- **[Success Metric 1]**: [e.g., Upload-to-approval funnel conversion rate]
- **[Success Metric 2]**: [e.g., Plan-to-action completion rate]

### 3. Production Quality & Reliability Metrics
*Live monitoring of AI/parser quality and system health in production.*
- **AI / Parser Quality in Prod**: [e.g., Pre-approval manual edit rate by field, edit distance, empty/fallback rate]
- **System & Sync Reliability**: [e.g., p50/p95 latency, timeout/error rate, multi-user sync latency]

### 4. Pre-Release QA & Offline Eval Metrics
*Offline benchmark gates and deterministic invariants verified before shipping.*
- **Golden Dataset AI Eval**: [e.g., $\ge 90\%$ extraction completeness across benchmark fixture inputs]
- **Negative Fixture & Deterministic Gates**: [e.g., $0\%$ hallucinated fields on negative fixtures; $100\%$ pass rate on deterministic `T1..Tn` logic tests]

## Scope & Feature Prioritization

### Core (In Scope)
- **[Capability 1]**: [User-facing capability required for the primary flow]
- **[Capability 2]**: [User-facing capability required for the primary flow]

### Deferred (Next Milestone)
- **[Deferred Capability from Request]**: [Why deferred — specific complexity multiplier avoided now]

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

## UI Design & Mocks

*Populated during the iterative UI design phase (via `product-design`) after the PRD text is written. Embed approved screen mock screenshots and visual direction notes here.*

- **Design Direction**: [Typography, palette, layout structure chosen]
- **Screen Mocks**:
  - `[Screen 1 Name]`: `![Screen 1 Mock](mocks/screen-1.png)` — `[mock HTML/source path]`

## Constraints

- [Non-negotiables: performance bounds, auth/permissions, platform support, accessibility]

## Known Gaps

- [Scoped requirements or flows not yet met by shipped code. Remove when fixed.]
