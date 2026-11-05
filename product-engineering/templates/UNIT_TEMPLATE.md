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

## Scenario Coverage

*Consider every dimension from `references/scenarios.md`; test only where it pays. A row needs either the T/M tokens covering it or a one-line reason it's skipped. "Doesn't apply" and "low value for this unit" are both valid. Don't write a test just to fill a row. Low-risk units usually cover 2–4 dimensions. Tier choice: `references/test-mapping-guide.md`.*

**Tiers used**: [unit, integration, end-to-end, live] — name any tier skipped and why (e.g. "live: no outside service in this unit").

| Dimension | Covered by | Skipped (why) |
|:---|:---|:---|
| Actor & Access | [T3, M1] | |
| Flow Paths & Intent | | |
| Data Volumes & State | | |
| Input & Payload Boundaries | | |
| AI & Probabilistic Modes | — | [e.g. No model calls in this unit] |
| Human Agency & Override | | |
| Network & Concurrency | — | [e.g. Read-only view, nothing to double-submit] |
| Platform, Viewport & A11y | | |

---

## Test Matrix (Automated & Manual E2E)

### A. Automated Test Scenarios (T1..Tn)
*Programmatic tests run by `TEST_COMMAND`. Each line names its tier `(unit | integration | e2e | live)` and what breaks if it's wrong. `live` = free calls to real dev/sandbox services on `LIVE_ALLOWED_HOSTS`; paid live checks go in section B as `[Live]` walkthroughs.*
- **T1 [Happy Path] (e2e)** — *(journey units)* [The unit's main flow, automated end to end in a real browser against the real app, outside services stubbed]. *Fails if broken: [the journey doesn't work]*
- **T2 [Rule] (unit)** — [Given X, when Y, then Z. Exact behavior asserted]. *Fails if broken: [user-visible consequence, e.g. saved plan silently lost]*
- **T3 [Edge Case / Boundary / Dirty Payload] (unit)** — [Given bad input or boundary condition, clean handling asserted]. *Fails if broken: [...]*
- **T4 [Guardrail] (integration)** — *(medium and high risk)* [Each lock holds: the blocked action stays blocked, e.g. an unapproved recipient is rejected, a delete with the dev login fails]
- **T5 [Abuse] (integration)** — *(high risk)* [Injection in a document does nothing, wrong-tenant access denied, replayed request rejected]
- **T6 [Data Invariant / Security / Concurrency] (integration)** — [Data scoping, idempotency, or invariant held]. *Fails if broken: [e.g. duplicate records]*. *Doesn't prove: [what a pass leaves untested, e.g. a mocked clock says nothing about the user's timezone] (optional)*
- **T7 [Instrumentation] (integration + e2e)** — *(journey units)* Drive each flow in this unit; assert every event in section C fires with its listed properties via the fake sink's `assert_tracked` (server) and the intercepted analytics requests (browser). New events added to the catalogue. *Fails if broken: the metrics this unit feeds are silently empty.*
- **T8 [Live] (live)** — *(units that call a free outside service)* [Run the flow against the real dev/sandbox service and read back the result, e.g. each section C event arrives in the dev analytics project with its properties, tagged with the run id]. Skipped and reported when the dev key is absent. *Fails if broken: [the real service rejects or drops what we send]*

*End-to-end coverage: `[tests/e2e/test_NN_*.py]` ([which T tokens]). Live coverage: `[tests/live/test_NN_*.py]` ([which T tokens]).*

### B. Manual E2E Scenarios (M1..Mk)
*Step-by-step user-verifiable walkthroughs: a human sanity pass over key flows (including ones the browser suite automates) plus anything automation can't judge.*
- **M1 [Desktop Happy Path]** — **Steps**: 1. Navigate to `/...` 2. Click `...` 3. Verify `...`. **Expected**: [Exact visual/functional outcome].
- **M2 [Responsive State]** — **Steps**: 1. At each width in `VIEWPORT_BREAKPOINTS` (CONFIG.md; else 375px) load `/...` 2. Tap `...`. **Expected**: [Layout matches each breakpoint tier, wide screens included; no horizontal overflow]. **Compare with**: [mock frames for these screens; reference screenshots added in Phase 6 at `NN-reference/`]. **What to look for**: [3–6 bullets: navigation, titles, key states, what must not appear].
- **M3 [Edge / Error Recovery / Human Override]** — **Steps**: 1. Trigger `...` with bad input or cancel mid-flight. **Expected**: [Human-readable error state]. **Recovery**: [How the user gets back on track: retry, undo, edit, or resume].
- **M4 [Live]** — *(units with a paid or non-automatable outside call)* **Cost**: [e.g. ~$0.30 per run: 12 model calls | free, but needs a real phone]. **When**: [unit checkpoint, P0 checkpoint, and whenever <prompt/model/provider> changes]. **Steps**: [...]. **Expected**: [...]. Run by the user, or by the orchestrator only with the user's OK for that run.

### C. Instrumentation
*Events emitted through the analytics seam (`ANALYTICS_PLATFORM` in CONFIG.md). Journey units: one view + one primary-action event per capability; P0 journeys also emit their hypothesis-metric events. Reporting unit: list the dashboards/queries built instead.*
- `[event_name]` — [Trigger]. Properties: `[prop]`, `[prop]`.

---

## Open Questions

*Unresolved items that block or shape this unit. Raised when this unit is next worked on, not at every checkpoint. Remove each once answered and written into the contract. Empty is normal.*
- [Question] — **Recommend**: [default and why]

---

## Acceptance Criteria

- [ ] All automated test cases (`T1..Tn`) pass green; free live tests ran (not skipped) or the service is marked not set up yet.
- [ ] All manual E2E scenarios (`M1..Mk`) verified and documented.
- [ ] Every Instrumentation event fires with its listed properties.
- [ ] Locks for this unit's risk level exist and their `[Guardrail]` / `[Abuse]` tests pass; guardrail config unchanged, or the change is in the cited ADR.
- [ ] [Semantic criterion 1: e.g. Domain logic is 100% deterministic and isolated from UI]
- [ ] [Semantic criterion 2: e.g. Seam separation respected, no leak across boundaries]
- [ ] [Behavioral / E2E criterion: e.g. Web UI renders correctly at every width in `VIEWPORT_BREAKPOINTS`]
- [ ] Code formatting and linting pass clean.
- [ ] Living specs listed above created/updated to match shipped code.
- [ ] Independent verification pass confirms all criteria.
