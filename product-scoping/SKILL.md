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

Turns a product idea or feature request into `specs/product/<slug>.md`: a core hypothesis, prioritized scope, metrics, and priority-ordered user flows ($F_1..F_m$) that `product-engineering` plans, builds, and tests against.

**Progression**: Stage 1 Ground & Challenge (draft spec written) → ⏸ → Stage 2 Prioritize, Metrics & Flows (spec updated) → ⏸ → Stage 3 Finalize Spec → optional `product-design` pass. Pause at each ⏸ for the user's decisions unless they explicitly ask to skip ahead; when skipping, still apply every rule below.

---

## Principles

1. **Inspect reality first.** Read `specs/`, data models, routes, and UI components before asking anything. Never ask what the codebase already answers.
2. **Grounded questions, no startup theater.** No *"if you had 48 hours…"* prompts. Ask about data sources, persistence, auth boundaries, external dependencies, and failure states.
3. **Ruthless scoper.** The request is a wish list, not a scope. Every capability has to earn its tier, and the default answer to a complexity multiplier is "cheaper mechanism first." Cutting and downgrading what the user asked for is the job; inventing features they didn't ask for is not.
4. **Priority by risk and unlock, never by setup order.** Rank by (a) the hypothesis that most needs validating and (b) what unlocks the most downstream value. Onboarding, accounts, and sharing take the tier of what they unlock, which is rarely first.
5. **User effort is a cost.** A mechanism is only "cheaper" if it stays within the user's effort budget at realistic volume. A limit, a manual sort, or a per-item review step doesn't remove cost; it moves it onto the user. Every downgrade must pass this check.
6. **Flows are test foundations.** Every in-scope capability becomes a numbered flow with preconditions, steps, end state, and edge/failure cases. `product-engineering` derives its automated ($T_1..T_n$) and manual E2E ($M_1..M_k$) tests from them.
7. **The spec file is the working memory.** Write `specs/product/<slug>.md` (or `specs/product/README.md` for a small single-surface product) as a draft at the end of Stage 1, from `templates/PRODUCT_SPEC_TEMPLATE.md`, and update it every time the user answers. Start each stage by re-reading it instead of relying on earlier conversation. Chat carries short summaries and questions; the full detail lives in the file.

### Keeping the spec current

- **Status line** at the top: `Draft`, or `Final`.
- **Unfilled sections** say `*TBD*`, never template brackets.
- **Open Questions**: every question you ask goes here, numbered, with your recommendation.
- **When the user answers**, before anything else: edit every section the answer affects so the spec reads as if it had always said this, then delete the question from Open Questions. Don't keep a decision log; the answer lives in the spec itself. 
- Describe behavior from the user's side. File paths, function names, library details, analytics tools, event names, and session-replay setup belong to `product-engineering` and `specs/engineering/`. The product spec says *what we need to learn* (e.g. "how often an opened recipe is cooked", "where users stall in F1"); engineering picks the tool and names the events.

---

## Stage 1: Ground & Challenge Scope

*Order matters: user moments and the user-side journey come before the bet and before any system audit, so mechanisms are chosen to fit the user, not the other way round.*

1. **Read the current system**: `specs/README.md`, `specs/product/`, `specs/engineering/`, and the models, routes, or components the request touches.
2. **Map the user's moments**:
   - **The users and stakeholders**: Who cares about this product, and who actually uses it? Those may be different audiences.
   - **Moments**: each distinct situation in which they arrive, with its trigger, place, device, and time available. Separate the **first session** (backfill, setup, the initial big import) from **steady state** (everyday use); they usually differ by an order of magnitude in volume.
   - **Effort budget**: what the user will tolerate per item and per session (taps, waits, decisions, review), given the time they actually have.
   - **What they do today**, and what it costs them. If that's cheap, say so.
3. **Walk every user journey as the user**, each at its own realistic volume from step 2. For the first session, use the largest plausible amount. Write each walk as a short narrative: what they tap, what they wait for, what they check, and when they can walk away. Count the user's effort per item and per session against the budget. Anything over budget is a requirement, not a nice-to-have (e.g. "review only what the system is unsure about," "resume after the app is closed").
   - **What success looks like**: What are our users' goals and how will we know if they have achieved their goals?
   - **10-star experience**: what the product looks like if everything works and the users have an amazing and memorable experience. This sets direction; it is not scope. It goes into the spec under Deferred.
4. **Name the bet**:
   - **Core hypothesis**: the one belief that, if false, makes the product not worth building. Tie it to the current alternative and cost from step 2.
   - **Commitment signal vs. what would prove it**: keep these separate.
     - *Commitment signal* (activation gate): high-intent setup effort with skin in the game (paying, deposit, proprietary data uploaded, team member invited), not vanity engagement (page views, casual clicks, polite feedback). It shows willingness to try, never that the product works.
     - *What would prove it* (retention): repeated use of the core loop over a stated time window, or replacing an active tool. Never accept a setup or one-time action as proof.
   - **How to validate**: the test, in words. The numbers come later, in Metrics.
     - Who runs it, and for how long.
     - The behavior that counts as proof.
     - The order of evidence: commitment signal, then repeat use, then a decision.
     - What pass and fail look like. On a fail, which likely cause to check first.
   - **Biggest unlock**: the capability most other capabilities depend on.
   - **P0 journeys**: the end-to-end flow(s) needed to test the hypothesis. Keep them as few as possible.
5. **Audit each requested capability** (system side):
   - **Actor & trigger**: who starts it, from what state, behind what auth boundary.
   - **Data & persistence**: where input comes from, what is persisted vs. computed, what cold start looks like.
   - **Complexity multipliers**: new tables, multi-user or roles, real-time sync, schedulers or background jobs, external APIs, notifications.
   - **Failure reality**: malformed, empty, or over-limit input; a dependency failing mid-flow; the user leaving mid-flow at realistic volume.
6. **Push back.** For every multiplier, propose the cheaper mechanism that delivers the same user outcome now, and rank the full version later. Before proposing it, re-walk the affected step 3 journeys with it in place: if it pushes the user over their effort budget at realistic volume, it doesn't deliver the same outcome, so reject it. Prefer cutting system cost the user doesn't feel (batching, async, background processing) over limits they hit.
   - *Good*: "Live cross-device sync needs a realtime channel and conflict handling. Refresh-on-open gives the same outcome for a list edited a few times a week. Recommend refresh-on-open in P1, realtime in P2."
   - *Bad*: "If you only had 48 hours, would you really need sync?"
   - *Bad*: "Cap uploads at 20 photos to keep processing fast." This fails the effort check when the first session is 300 photos. Process in the background instead.

   For the P0 journey, also compare two whole ways to deliver it, not only cheaper versions of one (e.g. recipes come in by photo upload and vision parse, vs. syncing an existing photo album, vs. typing). Name the one you'd build first and why.

   If you recommend cutting or downgrading fewer than ~30% of the requested capabilities, state why the request is already minimal.
7. **Write the draft spec** (`Draft — Stage 1`): Users & Goals (including moments, realistic volume, and effort budget), Core Hypothesis (including How to validate), a first pass at Scope & Priorities (each downgrade names both mechanisms), the 10-star experience under Deferred, and Open Questions. Metrics and flows are `*TBD (Stage 2)*`. The audit tables stay out of the file.
8. **Present** in this order, need-to-know only. **Stop and wait.**
   0. **Spec**: the draft's path, one line.
   1. **Building**: one sentence.
   2. **The user's journey**: the step 3 narratives in 3–5 lines at realistic volume, so the user can correct the moments and volumes before anything else. Describe any limit as the user would meet it (e.g. "one upload holds any number of recipes"), never as a bare system number.
   3. **Stories and priorities**: the 10-star experience; the bet (hypothesis, what users do today instead, the riskiest piece, and **How to validate**: commitment signal → <repeat behavior> over <time window> → pass/fail and what to check on a fail); a table of user stories by tier P0 / P1 / P2 / Later.
   4. **Features and priorities**: a table of feature, tier, and what gets built. A line naming what you cut that the user didn't ask for, and what replaced it.
   5. **Questions**: 3–5 grounded questions, each with a recommendation. Ask about volume and moments first if you are unsure of them; every later decision depends on them.

---

## Stage 2: Prioritize, Metrics & Flows

0. **Re-read the draft spec** and apply the user's Stage 1 answers to it (see *Keeping the spec current*) before tiering.
1. **Tier every capability**, each with a one-line reason:

   | Tier | Rule |
   | :--- | :--- |
   | **P0** | The journeys that test the hypothesis, and only what they need. |
   | **P1** | Needed before the product is worth using a second time. |
   | **P2** | In scope and planned, built last. Usually the full versions of downgraded multipliers. |
   | **Deferred** | Requested, but outside this milestone. Name the complexity avoided. |
   | **Non-goal** | Explicitly excluded during scoping. |

   A downgraded capability names both mechanisms: *"P1: refresh on open; P2: realtime sync."*

   **Check that P0 is just enough**, against How to validate, before fixing the tiers:
   - **Each item is needed**: remove one P0 item. Could the validation test still run, and would a failure still mean the bet is wrong? If so, it isn't needed for the test, so move it to P1. Keep it only if removing it would make the test fail for an unrelated reason (e.g. too slow to find anything).
   - **Together they're enough**: walk the validation test using only P0. If the user can't reach the proof behavior, something is missing.

   Write the result as **Why this P0 is enough** in Core Hypothesis: one line per P0 item on the part of the test it carries. Name any P0 item kept by user choice rather than the test.
2. **Metrics & Observability**: name what to measure, not the tools or the event names (see *Keeping the spec current*).
   - **Hypothesis metric** (leads the spec): exactly one metric that measures How to validate, anchored on a high-intent commitment signal, with a continue/rethink threshold. Everything else is secondary. Avoid vanity metrics (page views, button clicks) as validation proof.
   - **Acquisition**: how users arrive at the product (channels, campaigns, referrers), and landing-to-activation conversion.
   - **In-app usage & funnels**: activation, time to first value (TTFV), funnel conversion per flow, the journey points where watching real sessions would explain drop-offs, and a view and a primary action measured for **every** P0–P2 capability.
   - **Production Quality & Reliability**: runtime health and implicit quality signals (user edit rate on generated output, empty/fallback rate, p95 latency, error rate).
   - **Pre-Release QA & Offline Eval**: offline gates checked before shipping (golden-dataset accuracy, negative fixtures, deterministic test pass rate).
3. **Flows, numbered in priority order.** P0 flows come first, starting at F1. Every header carries its tier: `### F1 — <Name> [P0]`. Each flow has:
   - **Actor & Precondition**: starting state, screen, and data.
   - **Steps**: `User does [action] → System responds with [observable result]`.
   - **Expected End State**: user-visible outcome and persisted state.
   - **Edge & Failure Cases**: cold start, invalid/boundary input, failure recovery, and **realistic volume** (each flow's volume from Stage 1, the largest plausible amount for the first session: what the user sees, how long it takes, what they have to review, and what happens if they leave).

   Write each P0 flow's steps from the moment it serves, at its volume (e.g. "User selects 240 photos", not "User selects photos").

   For multi-actor concurrency, offline state, or AI outputs, cross-check against the 8 universal scenario dimensions (`product-engineering/references/scenarios.md`).
4. **Update the spec** (`Draft — Stage 2`): full Scope & Priorities, Metrics & Observability, every flow in full (P1/P2 flows included), and the remaining Open Questions.
5. **Present** in this order, need-to-know only. Chat shows the short form; the spec holds the full flows. **Stop and confirm before finalizing.**
   1. **Updated by the answers**: a few lines on what the user's answers changed.
   2. **Priorities**: one table by tier.
   3. **Success measure**: the hypothesis metric with its continue/rethink threshold, then one line of secondary signals and offline gates.
   4. **Flows**: each flow in two to four lines (steps, key edge and failure cases); P1/P2 flows named only.
   5. **Questions**: only what's still open, each with a recommendation.

---

## Stage 3: Finalize the Spec

1. Re-read the spec. Apply the last answers. Open Questions must be empty; any still open become a Known Gap, or take the recommended default written into the section it affects. No `*TBD*` left. Core Hypothesis has How to validate and Why this P0 is enough. No analytics tools or event names in the spec. Set the status to `Final`.
2. Link the spec from `specs/README.md` if one exists.
3. Hand off: for UI-facing products, offer `product-design` to render mocks from the spec's real copy and flows and embed the chosen ones in `## UI Design & Mocks`. Then `product-engineering`.
