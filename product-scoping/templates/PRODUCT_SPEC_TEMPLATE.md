# Product Spec — [Product or Feature Area]

*Lives in `specs/product/`. What the product does for its users today and why. No internal implementation detail; that belongs in `specs/engineering/`.*

**Status**: [Draft | Final]

## Open Questions

*Scoping only. Each with a recommendation. Empty when Final.*
1. [Question] — **Recommend**: [default and why]


## Users & Goals

- **Who**: [Primary user role/audience and context in which they arrive]
- **Moments**: [Each situation they arrive in: trigger, device, time available. Separate first session from steady state.]
- **Realistic volume**: [Per moment: the largest plausible first session, and typical steady-state volume, e.g. "300 photos once; 2–5 a week after"]
- **Effort budget**: [What they'll tolerate per item and per session: taps, waits, review]
- **Goals**: [What they come to accomplish; outcome when successful]

## Core Hypothesis

- **Hypothesis**: [The one belief that, if false, makes this not worth building]
- **What they do today**: [The current alternative and what it costs them]
- **Riskiest piece**: [The part most likely to make the hypothesis false]

### How to validate
*The test, in words. Numbers live in Metrics.*
- **Who and how long**: [Who runs the test, over what time window]
- **Commitment signal**: [The skin-in-the-game action that starts the test: payment, deposit, proprietary data uploaded, team invite. Not page views or clicks.]
- **Proof**: [The repeat behavior that shows it works, e.g. replacing the tool they use today]
- **Pass / fail**: [What each looks like; on a fail, which likely cause to check first]
- **Hypothesis Metric**: [The one metric that measures the proof] — continue if [≥ threshold]; rethink if below.

### Why this P0 is enough
*Each P0 item is needed for the test, and together they let the user reach the proof.*
- **[P0 item]**: [The part of the test it carries; or "kept by user choice, not needed by the test"]
- **P0 Journeys**: [F1, …]

## Metrics & Observability

*What to measure, not which tools or event names; `product-engineering` chooses the analytics platform and defines the events.*

### 1. Acquisition & Discovery
*How users arrive at the product.*
- **Traffic Channels & Campaigns**: [Target acquisition channels, campaigns, referrers]
- **Landing Conversion**: [Landing-page-to-activation conversion rate]

### 2. In-App Usage & Adoption
*What users do in the product.*
- **Onboarding & Activation**: [What counts as activated; time to first value (TTFV)]
- **Feature Usage**: [For each P0–P2 capability: how often it's viewed and how often its primary action is used]
- **Watching Real Sessions**: [Journeys and drop-off points where watching real sessions would explain what happened]
- **Engagement & Retention**: [Active users, W1 and W4 cohort retention]

### 3. Feature Success Metrics
*End-to-end conversion showing each flow solved the user's problem.*
- **[F1]**: [Share of users who start this flow and finish it]

### 4. Production Quality & Reliability Metrics
*Live quality and health signals in production.*
- **Output Quality**: [Implicit quality signals, e.g. user edit rate on generated output, empty/fallback rate]
- **System Reliability**: [p50/p95 latency, timeout/error rate]

### 5. Pre-Release QA & Offline Eval Metrics
*Offline gates verified before shipping.*
- **Offline Eval**: [e.g. $\ge 90\%$ accuracy on golden fixtures; $0\%$ fabricated fields on negative fixtures]
- **Deterministic Gates**: [e.g. $100\%$ pass rate on `T1..Tn` logic tests]

## Scope & Priorities

*Ranked by hypothesis risk and unlock, not setup order. `product-engineering` builds P0 → P1 → P2.*

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

*Priority order: P0 flows first, starting at F1. Every header carries its tier. `product-engineering` derives automated ($T_1..T_n$) and manual E2E ($M_1..M_k$) tests from these.*

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
