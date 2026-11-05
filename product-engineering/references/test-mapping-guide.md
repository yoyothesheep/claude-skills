# Test Tiers & Mocking Guide

Every scenario found in Phase 1 (see [scenarios.md](scenarios.md)) gets a home: an automated test at the right tier, a manual walkthrough, or both. Record the choice in the unit's Scenario Coverage table and on each T line. Don't leave edge cases to ad-hoc manual testing.

---

## 0. Automated (T) vs Manual (M)

- **Automated ($T_1..T_n$)**: anything a program can assert. Business logic, boundary inputs, schema repair, data scoping, injected AI failures, browser behavior (focus, keyboard, JS state, overflow, accessible names), and free live checks against real dev services. **Prefer automated** whenever a program can judge the result and it costs nothing to run.
- **Manual ($M_1..M_k$)**: what needs human judgment (visual feel, empty-state clarity, recovery and undo end to end, third-party pages, a pass at each breakpoint) and live checks that **cost money** or **can't be automated** (a real phone, a real inbox, an OAuth consent screen).
- **Both**: key happy paths and recovery paths. The end-to-end test proves they work; the walkthrough proves they feel right.

---

## 1. The four tiers

```
        ▲
       / \      Live — real dev/sandbox services (free ones automated, paid ones manual)
      /───\
     /     \    End-to-end — real app + real browser, outside services stubbed
    /───────\
   /         \  Integration — routes, database, seams, idempotency
  /───────────\
 /             \ Unit — pure logic, boundary values, schema repair
/───────────────\
```

| Tier | Proves | Talks to | Runs |
| :--- | :--- | :--- | :--- |
| **Unit** | Pure logic | Nothing | Every test run (`TEST_COMMAND`) |
| **Integration** | Routes + data + seams together | Nothing outside the machine | Every test run |
| **End-to-end** | Whole journeys through the real app in a real browser (Playwright or equivalent) | Outside services stubbed: their endpoints intercepted, payloads decoded and asserted | Every test run |
| **Live, free** | Outside services accept what we send and do what we expect | Real **dev/sandbox** services on `LIVE_ALLOWED_HOSTS` only (e.g. analytics ingestion, payment test mode, email sandbox) | Every test run, tagged `live`; side effects tagged with a run id |
| **Live, paid** | Same, for calls that cost money (LLM credits, SMS, paid APIs) or can't be automated | Real dev services | **Manual only**: a `[Live]` M walkthrough with a cost estimate, run by the user, or by the orchestrator with the user's OK for that run |

Push each scenario as low as it can be proven. Go up a tier only for behavior that doesn't exist below it. Live tests are few: one per external integration path, not one per scenario.

### When live tests run

- **Free live** run inside `TEST_COMMAND`, like every other test. Without the dev key (a fresh clone, CI without secrets) they are **skipped and reported** as `skipped: no dev key for <service>`, never silently passed. In Phase 5 a skipped free live test blocks PASS unless the contract marks that service as not set up yet.
- **Paid live** run at the unit's checkpoint, at the P0 checkpoint, and whenever the thing they cover changes (a prompt, a model, a provider). Each states its cost per run (e.g. "~$0.30: 12 model calls").
- **Never**: production keys, production accounts, or production data in any tier.

### Network lock

Every test run blocks outbound connections except the local machine and the hosts in `LIVE_ALLOWED_HOSTS` (`CONFIG.md`). Only free services go on that list. Paid hosts never do, and paid keys are removed from the test environment, so an accidental paid call fails instead of charging. Rules and proof: [Guardrails](guardrails.md#test-network-lock).

### Reading results back

A free live test often has to ask the service what arrived (an analytics event, a sandbox payment). Phase 0 asks the user for a **read-only, narrowly scoped dev credential** for that. If none exists, the read-back is done by the orchestrator through an MCP in Phase 5 and labelled **semi-automated** in the verdict.

---

## 2. Tier selection matrix

| Dimension | Primary tier | Tooling / pattern | M walkthrough? |
|:---|:---|:---|:---|
| **Actor & Access** | Unit (route guards) + end-to-end | Route middleware unit tests, browser session fixtures | Login redirect only |
| **Flow Paths & Intent** | End-to-end | Flow specs, DOM assertions; **every journey unit automates its happy path here** | Yes: happy path |
| **Data Volumes & State** | Integration | Parametrized DB fixtures, pagination tests | Yes: empty state |
| **Input & Payload Boundaries** | Unit | Boundary-value parametrization, fuzzing | No |
| **AI & Probabilistic Modes** | Unit with mock client; accuracy evals are **paid live** | Injectable client returning canned malformed/truncated responses; frozen fixture set with scoring | Only for review/override UI, plus the paid eval run |
| **Human Agency & Override** | End-to-end | Interactive tests verifying override persists and undo restores | Yes: recovery |
| **Network & Concurrency** | Integration | Repeated submit with same idempotency key; mocked failed response | No |
| **Platform, Viewport & A11y** | End-to-end | Runs at each width in `VIEWPORT_BREAKPOINTS`, keyboard/focus tests, accessibility checker (e.g. axe) | Yes: M2 per breakpoint |
| **External services** | Stubbed in end-to-end; **live** for "the real service accepts it" | Endpoint interception + payload decoding; live tests against dev/sandbox accounts | Paid ones only, as `[Live]` M |

---

## 3. Mocking probabilistic and external systems

Unit, integration and end-to-end tiers never call real LLM/vision APIs or other outside services:
1. **The injectable client seam:** inject an abstract client (`AIClient`, `PaymentClient`) into business logic.
2. **Canned failure payloads:** test each failure archetype with recorded responses:
   - `test_handles_malformed_json_response()`
   - `test_recovers_from_truncated_tokens()`
   - `test_deduplicates_overlapping_screenshot_lines()`
   - `test_flags_low_confidence_extraction()`
3. **Vendored browser libraries:** third-party browser code is served from a pinned local copy so end-to-end tests run it with its endpoints intercepted. Blocking all network hides "library never initialised" bugs.
4. **Accuracy evals** against real models live in a separate suite (e.g. `tests/evals/`) and are **paid live**: a `[Live]` M walkthrough with its cost, never part of `TEST_COMMAND`.
