# Build Unit NN — [Unit Name]

*Part of **[Milestone]** ([plan.md](../plan.md)), after Unit [Prev].*

- **Type**: [infra | journey | reporting]
- **Serves**: [F1, F2 | all]
- **Tier**: [P0 | P1 | P2 | —]
- **Risk**: [low | medium | high]. Worst case if the agent gets this wrong, and can it be undone? See `references/guardrails.md`. Unsure: take the higher level.
- **Guardrails ADR**: [ADR-NNN]. Low risk cites the baseline ADR from Phase 0; medium and high write their own, and so does any design-system change (tokens, theme, global styles, shared components) at any risk level. UI copy cites the baseline from `templates/GUARDRAILS_ADR_TEMPLATE.md`.

## Scope & User Story

[1-2 paragraphs describing what this unit changes for the user. What do they see, do, or experience? What does NOT change?]

**Testable after this unit**: [What a human can do in the running app once this unit ships]

### In-Scope:
- [Item 1]
- [Item 2]

### Out-of-Scope:
- [Explicit boundary / what is deferred]

---

## Architectural Seam & Data Boundaries

- **Boundary / Seam**: [Which modules own the logic? e.g. Domain core vs Web Route]
- **Data Models / Schema**: [Any new tables, columns, or migration numbers]
- **Tenancy / Security Scoping**: [How isolation or authentication is guaranteed at the boundary]

---

## Living Specs Affected

*Specs this unit creates or updates in Phase 6 (Living Spec Sync).*
- `specs/product/[file].md` — [create | update]: [requirement added or changed] *(omit if requirements unchanged)*
- `specs/engineering/[subsystem].md` — [create | update]: [what behavior gets documented]
- `specs/README.md` — [update if routes, modules, or env vars change]

---

## Test Matrix (Automated & Manual E2E)

### A. Automated Test Scenarios (T1..Tn)
*Deterministic, programmatic tests run via test runner / CI (audited against 8 universal dimensions; see references/scenarios.md).*
- **T1 [Happy Path]** — [Given X, when Y, then Z. Exact behavior asserted]
- **T2 [Edge Case / Boundary / Dirty Payload]** — [Given bad input or boundary condition, clean handling asserted]
- **T3 [Guardrail]** — *(medium and high risk)* [Each lock holds: the blocked action stays blocked, e.g. an unapproved recipient is rejected, a delete with the dev login fails]
- **T4 [Abuse]** — *(high risk)* [Injection in a document does nothing, wrong-tenant access denied, replayed request rejected]
- **T5 [Data Invariant / Security / Concurrency]** — [Data scoping, idempotency, or invariant held]. *Doesn't prove: [what a pass leaves untested, e.g. a mocked clock says nothing about the user's timezone] (optional)*

*Browser coverage: `[tests/e2e/test_NN_*.spec.ts]` ([which T tokens]).*

### B. Manual E2E Scenarios (M1..Mk)
*Step-by-step user-verifiable walkthroughs: a human sanity pass over key flows (including ones the browser suite automates) plus anything automation can't judge.*
- **M1 [Desktop Happy Path]** — **Steps**: 1. Navigate to `/...` 2. Click `...` 3. Verify `...`. **Expected**: [Exact visual/functional outcome].
- **M2 [Responsive State]** — **Steps**: 1. At each width in `VIEWPORT_BREAKPOINTS` (CONFIG.md; else 375px) load `/...` 2. Tap `...`. **Expected**: [Layout matches each breakpoint tier, wide screens included; no horizontal overflow].
- **M3 [Edge / Error Recovery / Human Override]** — **Steps**: 1. Trigger `...` with bad input or cancel mid-flight. **Expected**: [Human-readable error state, clean recovery/undo path].

### C. Instrumentation
*Events emitted through the analytics seam (`ANALYTICS_PLATFORM` in CONFIG.md). Journey units: one view + one primary-action event per capability; P0 journeys also emit their hypothesis-metric events. Reporting unit: list the dashboards/queries built instead.*
- `[event_name]` — [Trigger]. Properties: `[prop]`, `[prop]`.

---

## Acceptance Criteria

- [ ] All automated test cases (`T1..Tn`) pass green.
- [ ] All manual E2E scenarios (`M1..Mk`) verified and documented.
- [ ] Every Instrumentation event fires with its listed properties.
- [ ] Locks for this unit's risk level exist and their `[Guardrail]` / `[Abuse]` tests pass; guardrail config unchanged, or the change is in the cited ADR.
- [ ] [Semantic criterion 1: e.g. Domain logic is 100% deterministic and isolated from UI]
- [ ] [Semantic criterion 2: e.g. Seam separation respected, no leak across boundaries]
- [ ] [Behavioral / E2E criterion: e.g. Web UI renders correctly at every width in `VIEWPORT_BREAKPOINTS`]
- [ ] Code formatting and linting pass clean.
- [ ] Living specs listed above created/updated to match shipped code.
- [ ] Independent verification pass confirms all criteria.
