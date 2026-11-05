# Test Levels & Mocking Guide

Every scenario found in Phase 1 (see [scenarios.md](scenarios.md)) gets a home: an automated test at the right level, a manual walkthrough, or both. Record the choice in the unit's Scenario Coverage table and on each T line. Don't leave edge cases to ad-hoc manual testing.

---

## 0. Automated (T) vs Manual (M)

- **Automated ($T_1..T_n$)**: anything a program can assert deterministically. Business logic, boundary inputs, schema repair, data scoping, injected AI failures, and browser behavior (focus, keyboard, JS state, overflow, accessible names).
- **Manual ($M_1..M_k$)**: what needs human judgment. Visual feel, empty-state clarity, recovery and undo flows end to end, third-party pages, a sanity pass at each breakpoint.
- **Both**: key happy paths and recovery paths. The browser suite proves they work; the walkthrough proves they feel right.

---

## 1. The Verification Pyramid

```
      ▲
     / \     Browser Tests (Playwright / Cypress)
    /   \    - Happy paths, visual states, auth redirects, cancellation
   /─────\
  /       \   Integration / Pipeline Tests
 /         \  - Network retries, batch chunking, database transactions, idempotency
/───────────\
/             \ Deterministic Unit Tests & AI Eval Fixtures
/               \ - Boundary validations, schema repair, prompt evals, deduplication
─────────────────
```

Push each scenario as low as it can be proven. Go up a level only for behavior that doesn't exist below it.

---

## 2. Test Level Selection Matrix

| Dimension | Primary Level | Tooling / Pattern | M walkthrough? |
|:---|:---|:---|:---|
| **Actor & Access** | Unit (route guards) + browser | Route middleware unit tests, browser session fixtures | Login redirect only |
| **Flow Paths & Intent** | Browser | Flow specs, DOM assertions | Yes: happy path |
| **Data Volumes & State** | Integration | Parametrized DB fixtures, pagination tests | Yes: empty state |
| **Input & Payload Boundaries** | Unit | Boundary-value parametrization, fuzzing | No |
| **AI & Probabilistic Modes** | Unit with mock client; evals for accuracy | Injectable client returning canned malformed/truncated responses; frozen fixture set with scoring | Only for review/override UI |
| **Human Agency & Override** | Browser | Interactive tests verifying override persists and undo restores | Yes: recovery |
| **Network & Concurrency** | Integration | Repeated submit with same idempotency key; mocked failed response | No |
| **Platform, Viewport & A11y** | Browser | Runs at each width in `VIEWPORT_BREAKPOINTS`, keyboard/focus tests, accessibility checker (e.g. axe) | Yes: M2 per breakpoint |

---

## 3. Mocking Probabilistic Systems in Deterministic Tests

Never hit live LLM/vision APIs in continuous integration (CI) tests:
1. **The Injectable Client Seam:** Inject an abstract `AIClient` protocol into business logic.
2. **Canned Failure Payloads:** Test each failure archetype using recorded JSON payloads:
   - `test_handles_malformed_json_response()`
   - `test_recovers_from_truncated_tokens()`
   - `test_deduplicates_overlapping_screenshot_lines()`
   - `test_flags_low_confidence_extraction()`
3. **Dedicated Eval Benchmarks:** Keep a separate `tests/evals/` suite that runs against live models on release candidates to measure real-world precision and recall.
