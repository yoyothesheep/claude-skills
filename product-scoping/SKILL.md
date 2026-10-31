---
name: product-scoping
description: >-
  Scopes a product or feature into a prioritized, test-ready specification (specs/product/<slug>.md).
  Inspects the existing codebase and specs first, names the core hypothesis, pushes back hard on
  scope by cutting or downgrading complexity multipliers, ranks every capability P0/P1/P2 by
  biggest unlock and riskiest hypothesis, defines metrics led by one hypothesis metric, and writes
  priority-ordered user flows (F1..Fm) with edge/failure states that map directly to engineering
  test matrices. Use whenever starting a new product, scoping a feature, or turning a raw idea
  into a product spec before implementation.
---

# product-scoping

Turns a product idea or feature request into `specs/product/<slug>.md`: a core hypothesis, prioritized scope, metrics, and priority-ordered user flows ($F_1..F_m$) that `loop-engineering` plans, builds, and tests against.

**Progression**: Stage 1 Ground & Challenge → ⏸ → Stage 2 Prioritize, Metrics & Flows → ⏸ → Stage 3 Write Spec → optional `product-design` pass. Pause at each ⏸ for the user's decisions unless they explicitly ask to skip ahead; when skipping, still apply every rule below.

---

## Principles

1. **Inspect reality first.** Read `specs/`, data models, routes, and UI components before asking anything. Never ask what the codebase already answers.
2. **Grounded questions, no startup theater.** No *"if you had 48 hours…"* prompts. Ask about data sources, persistence, auth boundaries, external dependencies, and failure states.
3. **Ruthless scoper.** The request is a wish list, not a scope. Every capability has to earn its tier, and the default answer to a complexity multiplier is "cheaper mechanism first." Cutting and downgrading what the user asked for is the job; inventing features they didn't ask for is not.
4. **Priority by risk and unlock, never by setup order.** Rank by (a) the hypothesis that most needs validating and (b) what unlocks the most downstream value. Onboarding, accounts, and sharing take the tier of what they unlock, which is rarely first.
5. **Flows are test foundations.** Every in-scope capability becomes a numbered flow with preconditions, steps, end state, and edge/failure cases. `loop-engineering` derives its automated ($T_1..T_n$) and manual E2E ($M_1..M_k$) tests from them.

---

## Stage 1: Ground & Challenge Scope

1. **Read the current system**: `specs/README.md`, `specs/product/`, `specs/engineering/`, and the models, routes, or components the request touches.
2. **Name the end goal, then the bet**:
   - **10-star experience**: what the product looks like if everything works. This sets direction; it is not scope. It goes into the spec under Deferred.
   - **Core hypothesis**: the one belief that, if false, makes the product not worth building.
   - **Biggest unlock**: the capability most other capabilities depend on.
   - **P0 journeys**: the end-to-end flow(s) needed to test the hypothesis. Keep them as few as possible.
3. **Audit each requested capability**:
   - **Actor & trigger**: who starts it, from what state, behind what auth boundary.
   - **Data & persistence**: where input comes from, what is persisted vs. computed, what cold start looks like.
   - **Complexity multipliers**: new tables, multi-user or roles, real-time sync, schedulers or background jobs, external APIs, notifications.
   - **Failure reality**: malformed, empty, or over-limit input; a dependency failing mid-flow.
4. **Push back.** For every multiplier, propose the cheaper mechanism that delivers the same user outcome now, and rank the full version later:
   - *Good*: "Live cross-device sync needs a realtime channel and conflict handling. Refresh-on-open gives the same outcome for a list edited a few times a week. Recommend refresh-on-open in P1, realtime in P2."
   - *Bad*: "If you only had 48 hours, would you really need sync?"

   If you recommend cutting or downgrading fewer than ~30% of the requested capabilities, state why the request is already minimal.
5. **Present** the hypothesis, P0 journeys, proposed cuts and downgrades, and 3–5 grounded questions, each paired with a recommendation. **Stop and wait.**

---

## Stage 2: Prioritize, Metrics & Flows

1. **Tier every capability**, each with a one-line reason:

   | Tier | Rule |
   | :--- | :--- |
   | **P0** | The journeys that test the hypothesis, and only what they need. |
   | **P1** | Needed before the product is worth using a second time. |
   | **P2** | In scope and planned, built last. Usually the full versions of downgraded multipliers. |
   | **Deferred** | Requested, but outside this milestone. Name the complexity avoided. |
   | **Non-goal** | Explicitly excluded during scoping. |

   A downgraded capability names both mechanisms: *"P1: refresh on open; P2: realtime sync."*
2. **Metrics**:
   - **Hypothesis metric** (leads the spec): exactly one metric with a continue/rethink threshold. Everything else is secondary.
   - **Usage & Adoption**: activation, time to first value, retention cohorts, and a usage event (view + primary action) for **every** P0–P2 capability. The analytics platform supplies the aggregates; the spec names the events.
   - **Feature Success**: funnel conversion per flow.
   - **Production Quality & Reliability**: runtime health and implicit quality signals (user edit rate on generated output, empty/fallback rate, p95 latency, error rate).
   - **Pre-Release QA & Offline Eval**: offline gates checked before shipping (golden-dataset accuracy, negative fixtures, deterministic test pass rate).
3. **Flows, numbered in priority order.** P0 flows come first, starting at F1. Every header carries its tier: `### F1 — <Name> [P0]`. Each flow has:
   - **Actor & Precondition**: starting state, screen, and data.
   - **Steps**: `User does [action] → System responds with [observable result]`.
   - **Expected End State**: user-visible outcome and persisted state.
   - **Edge & Failure Cases**: cold start, invalid/boundary input, failure recovery.

   For multi-actor concurrency, offline state, or AI outputs, cross-check against `product-scenarios` dimensions.
4. **Present** tiers, metrics, and flows. **Stop and confirm before writing the spec.**

---

## Stage 3: Write the Spec

1. Write `specs/product/<slug>.md` (or `specs/product/README.md` for a small single-surface product) from `templates/PRODUCT_SPEC_TEMPLATE.md`. Describe behavior from the user's side; file paths, function names, and library details belong in `specs/engineering/`.
2. Link the spec from `specs/README.md` if one exists.
3. Hand off: for UI-facing products, offer `product-design` to render mocks from the spec's real copy and flows and embed the chosen ones in `## UI Design & Mocks`. Then `loop-engineering`.
