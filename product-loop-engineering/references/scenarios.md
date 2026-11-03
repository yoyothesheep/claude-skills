# Scenario Discovery & Clarification Guide

A systematic framework for discovering edge cases, failure states, and probabilistic behaviors before code is written, ensuring test matrices ($T_1..T_n$ automated and $M_1..M_k$ manual E2E) cover real-world failure modes.

---

## 1. The 8 Universal System Dimensions

When planning build units and formulating test matrices in Phase 1, evaluate each flow ($F_1..F_m$) across these 8 universal dimensions:

1. **Actor & Access Context**:
   - Unauthenticated ingress (redirect to login with return state).
   - Authenticated role permissions / RBAC (tenant boundary, admin vs. member).
   - Multi-actor concurrency (two users editing same resource).
   - Session expiry mid-flow.

2. **Flow Paths & Intent**:
   - Primary nominal / happy path.
   - Alternate entry points / deep links.
   - Cancellation mid-stream (dismiss modal, click back, navigate away).
   - Abandonment & draft recovery (partial inputs retained or cleanly discarded).

3. **Data Volumes & State**:
   - Cold start / zero state (first-time user, 0 items; needs clear onboarding/empty CTA).
   - Sparse data (1 item, missing optional fields).
   - Nominal volume.
   - Extreme / bulk scale (20+ items, pagination, chunking, progress indicators).
   - Stale or conflicting state (out-of-order updates).

4. **Input & Payload Boundaries**:
   - Nominal clean inputs.
   - Extreme boundary sizes (0 chars, max allowed, oversized uploads).
   - Degraded / dirty inputs (malformed formatting, noisy text/images).
   - Hostile payloads (script injection, XSS vectors, invalid UTF-8).

5. **Generic AI & Probabilistic Modes** (for AI features):
   - Schema compliance failure (malformed JSON, broken fences).
   - Hallucination / ungrounded generation.
   - Omission / "lost in the middle" token dropping.
   - False positives / false negatives.
   - Repetition loops or overlapping extraction artifacts.
   - Rate limits (429), timeouts (504), service outages.
   *(See [LLM Failure Archetypes](llm-failure-archetypes.md) for exhaustive catalog).*

6. **Human Agency & Override**:
   - Glanceable verification diffs (user can inspect AI proposals).
   - $\le 2$-tap manual corrections / overrides.
   - Reversibility & undo (non-destructive mutations).
   - Actionable error feedback (what went wrong and what the user can do now).

7. **Network & Concurrency**:
   - Fast connection (nominal).
   - High latency / slow 3G (optimistic UI or loading feedback).
   - Flaky / offline transition mid-submission (queue/retry vs. prompt).
   - Double-submits (debouncing, idempotency keys).
   - Race conditions (out-of-order API responses).

8. **Platform, Viewport & Accessibility**:
   - Viewport breakpoints (`VIEWPORT_BREAKPOINTS` in `CONFIG.md`).
   - Mobile touch vs. desktop pointer/keyboard navigation.
   - Keyboard focus traps and tab order.
   - Screen reader accessible names and ARIA live announcements.

---

## 2. Clarification Protocol: When to Ask the User

**Rule**: If any edge case, boundary state, failure recovery path, or probabilistic behavior is ambiguous, underspecified, or has multiple valid UX interpretations:
**STOP before finalizing unit contracts.**

Do not guess or assume product behavior. Ask the user concrete, structured questions:
1. **Identify the Gap**: State the scenario and trigger (e.g. *"When a user abandons an in-flight AI extraction mid-stream..."*).
2. **Present Concrete Options**: Provide 2–3 clear trade-offs (e.g., *Option A: Discard all partial state immediately; Option B: Save draft with resume chip*).
3. **Recommend a Default**: Prefix the recommended option with `(Recommended)` based on system invariants or standard UX patterns.
4. **Lock Answer into Contract**: Record the user's chosen outcome directly into the unit's $T$ or $M$ scenario.

---

## 3. Mapping Scenarios to the Dual Test Matrix

Every discovered scenario maps directly to the unit spec's test matrix:

- **Automated Tests ($T_1..T_n$)**: Programmatic CI checks.
  - Deterministic business logic, schema repair, boundary checks, input sanitation, database scoping, injectable mock AI failures.
- **Manual E2E Walkthroughs ($M_1..M_k$)**: User-verifiable steps.
  - Real human recovery flows, undo/reversibility, responsive breakpoint checks, visual empty states, loading indicators.

See [Test Mapping Guide](test-mapping-guide.md) for test level selection and mocking patterns, and [Scenario Matrix Template](matrix-template.md) for full matrix specifications.

