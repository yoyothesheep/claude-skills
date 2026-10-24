# Build Unit NN — [Unit Name]

*Part of **[Milestone]** ([plan.md](../plan.md)), after Unit [Prev].*

## Scope & User Story

[1-2 paragraphs describing what this unit changes for the user. What do they see, do, or experience? What does NOT change?]

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

*Specs this unit creates or updates during `/loop finalize`.*
- `specs/product/[file].md` — [create | update]: [requirement added or changed] *(omit if requirements unchanged)*
- `specs/engineering/[subsystem].md` — [create | update]: [what behavior gets documented]
- `specs/README.md` — [update if routes, modules, or env vars change]

---

## Test Matrix (Automated & Manual E2E)

### A. Automated Test Scenarios (T1..Tn)
*Deterministic, programmatic tests run via test runner / CI.*
- **T1 [Scenario Name]** — [Given X, when Y, then Z. Exact behavior asserted]
- **T2 [Edge Case / Failure Mode]** — [Given bad input or boundary condition, clean handling asserted]
- **T3 [Data Invariant / Security Boundary]** — [Data scoping or invariant held]

*Browser coverage: `[tests/e2e/test_NN_*.spec.ts]` ([which T tokens]).*

### B. Manual E2E Scenarios (M1..Mk)
*Step-by-step user-verifiable walkthroughs: a human sanity pass over key flows (including ones the browser suite automates) plus anything automation can't judge.*
- **M1 [Desktop Happy Path]** — **Steps**: 1. Navigate to `/...` 2. Click `...` 3. Verify `...`. **Expected**: [Exact visual/functional outcome].
- **M2 [Mobile / Responsive State]** — **Steps**: 1. Resize viewport to 375px 2. Tap `...`. **Expected**: [Drawer/layout adapts cleanly without horizontal overflow].
- **M3 [Edge / Error Recovery State]** — **Steps**: 1. Trigger `...` with bad input. **Expected**: [Human-readable error state, clean recovery path].

---

## Acceptance Criteria

- [ ] All automated test cases (`T1..Tn`) pass green.
- [ ] All manual E2E scenarios (`M1..Mk`) verified and documented.
- [ ] [Semantic criterion 1: e.g. Domain logic is 100% deterministic and isolated from UI]
- [ ] [Semantic criterion 2: e.g. Seam separation respected, no leak across boundaries]
- [ ] [Behavioral / E2E criterion: e.g. Web UI renders cleanly on desktop and mobile viewports]
- [ ] Code formatting and linting pass clean.
- [ ] Living specs listed above created/updated to match shipped code.
- [ ] Independent verification pass confirms all criteria.
