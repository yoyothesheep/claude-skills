# Test Mapping Guide: Translating Scenarios into Test Suites

Every scenario identified by `product-scenarios` should map directly to an automated verification layer. Do not rely on manual testing for edge cases.

---

## 1. The Verification Pyramid for Scenario Mapping

```
      ▲
     / \     E2E / Browser Tests (Playwright / Cypress)
    /   \    - Happy paths, visual states, auth redirects, cancellation
   /─────\
  /       \   Integration / Pipeline Tests
 /         \  - Network retries, batch chunking, database transactions, idempotency
/───────────\
/             \ Deterministic Unit Tests & AI Eval Fixtures
/               \ - Boundary validations, schema repair, prompt evals, deduplication
─────────────────
```

---

## 2. Test Level Selection Matrix

| Scenario Category | Primary Test Layer | Tooling / Pattern |
|:---|:---|:---|
| **Actor & Auth** | E2E + Unit route guards | Playwright session mocking, route middleware unit tests |
| **Flow Paths & UI State** | E2E Browser | Playwright component / flow specs, DOM assertions |
| **Data Volumes & Scale** | Integration / DB | Parametrized DB fixtures, pagination load tests |
| **Input Boundaries** | Unit Tests | Fuzzing, boundary edge value parametrization |
| **Generic LLM Failures** | Unit with Mock Client | Injectable mock client returning canned malformed/truncated responses |
| **Domain AI Accuracy** | Offline AI Evals | Frozen dataset of input fixtures run against extraction scoring functions |
| **Human Override & Fix** | E2E Browser | Interactive UI tests verifying override persistence |
| **Network & Concurrency** | Integration | Mock slow responses, network abort simulation, concurrent requests |

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
