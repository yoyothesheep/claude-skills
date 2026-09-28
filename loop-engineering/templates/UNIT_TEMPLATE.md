# Build Unit NN — [Unit Name]

*Part of **[Milestone / Epic]** ([Parent Spec Link]), after Unit [Prev].*

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

## Test Scenarios (T1..Tn)

- **T1 [Scenario Name]** — [Given X, when Y, then Z. Exact behavior asserted]
- **T2 [Edge Case / Failure Mode]** — [Given bad input or boundary condition, then clean handling]
- **T3 [Roundtrip / Invariant]** — [Write -> Read back -> Invariant held]

---

## Acceptance Criteria

- [ ] All mapped test cases (`T1..Tn`) exist in `tests/test_NN_*.py` and pass green.
- [ ] [Semantic criterion 1: e.g. Domain logic is 100% deterministic and isolated from LLM]
- [ ] [Semantic criterion 2: e.g. Seam separation respected, no leak across boundaries]
- [ ] [Behavioral / E2E criterion: e.g. Web UI renders cleanly on desktop and mobile viewports]
- [ ] Code formatting and linting pass (`ruff check`, `ruff format --check`).
- [ ] Independent verification pass confirms all criteria.
