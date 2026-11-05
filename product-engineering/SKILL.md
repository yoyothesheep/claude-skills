---
name: product-engineering
description: >-
  Spec-driven dev loop. One-time setup (guardrails, CONFIG.md, dev/prod analytics keys), then
  milestone planning with every unit contract written upfront (automated T tests, manual E2E M
  walkthroughs, analytics events), ADRs, test-first build, an independent maker/verifier gate,
  and living-spec sync. Guardrails are locks, scaled by per-unit risk. Use when planning,
  developing, testing, refactoring, or verifying features and subsystems.
---

# product-engineering

Turns ad-hoc coding into a repeatable spec-and-test-driven loop.

| Phase | Goal | Run by | Leave when |
| :--- | :--- | :--- | :--- |
| 0 Setup (once per repo) | Locks and analytics accounts exist | Orchestrator + human | `check_loop.py guardrails` is ok |
| 1 Plan | Every unit contract written | Orchestrator | `check_loop.py plan` clean; user approves |
| 2 Decide | Non-obvious choices recorded as ADRs | Orchestrator | User aligned; ADR written |
| 3 Tests first | T tests exist and fail for the right reason | `loop-maker` | Red |
| 4 Build | Contract satisfied, code simplified | `loop-maker` | Green; lint and format clean |
| 5 Verify | Independent audit | `loop-verifier` | PASS; fingerprint unchanged |
| 6 Spec sync | Specs match shipped code | `loop-scribe` | Specs updated; user reviews diff |

Phases 3–6 repeat for each unit, in plan order.

---

## Core Tenets

1. **Plan everything, build in priority order.** Pre-document every unit contract in the milestone before writing Unit 01 code (Phase 1), so early decisions don't box in later units. Build order: walking skeleton → P0 → P1 → P2 → analytics reporting. Each unit leaves the app runnable and testable.

2. **Four test tiers, automated first.** Full rules: [Test tiers](references/test-mapping-guide.md).
   - **Unit, integration, end-to-end** (T tokens): run on every `TEST_COMMAND`, nothing leaves the machine. End-to-end means the real app in a real browser (Playwright or equivalent) with outside services stubbed; behavior that only exists in a browser (focus, keyboard, JS state, layout, accessible names) is covered here, never by source-text assertions. Every journey unit automates its happy path end to end.
   - **Live**: real dev/sandbox services. **Free** live checks are automated T tests that run on every `TEST_COMMAND`, limited to `LIVE_ALLOWED_HOSTS`. **Paid** ones (LLM credits, SMS, paid APIs) and ones a program can't do (a real phone, a real inbox) are manual `[Live]` walkthroughs with a stated cost.
   - **Manual walkthroughs (M1..Mk)**: exact user actions, expected look, error recovery. They cover what automation can't judge and act as a human sanity pass over key flows the end-to-end tests already automate.

3. **Seams and determinism.** Domain logic lives in isolated core modules (`lib/`, domain packages, core models). Route handlers, API endpoints, and CLI tools are thin adapters. Multitenancy, permissions, and scoping are enforced at the data-access seam, so unscoped leaks are structurally impossible.

4. **Maker never self-approves.** A separate verifier audits mechanical CI facts, test fidelity, manual E2E repeatability, and acceptance criteria (Phase 5).

5. **Docs by lifecycle.**
   ```
   active/                       # work in progress
     NN-<milestone>/
       plan.md                   # roadmap + status tracker
       units/NN-<slug>.md        # unit contracts
   specs/                        # what the system is today
     README.md                   # index: system overview, links to both halves
     product/                    # what & why (a single short README.md is fine for small products)
     engineering/                # how: one file per layer/subsystem, never per milestone
   history/                      # append-only record of change
     decisions/NNN-<slug>.md     # ADRs
     milestones/NN-<milestone>/  # finished active/ folders, moved here intact
   ```
   - Planning artifacts never live in `specs/`.
   - `specs/` describes only what has shipped: no roadmaps, unbuilt features, "will" statements, strikethroughs, or decommissioned designs. Gaps between intent and reality go under **Known Gaps**. A spec outlives the milestone that created it.
   - ADRs are written when the decision is made, never edited once accepted; a new ADR supersedes an old one. Finished milestone folders are frozen.
   - **Git**: commits follow `AUTO_COMMIT` in `CONFIG.md`; when `false` (the default), leave diffs uncommitted for review. Only what git can't undo is denied: force-push, `reset --hard`, `clean -f`, and secrets or user data entering a commit.

6. **Instrumented by default.** Every journey unit ships the analytics events for what it builds; the last unit turns them into reports. Dev and prod use separate analytics projects and keys. Full rules: [Analytics](references/analytics.md).

7. **Guardrails are locks, not prompts.** Lock only what git can't undo; everything else gets a check. Every unit has a **Risk** (low / medium / high, from blast radius and reversibility; unsure means higher) and a **Guardrails ADR**: low cites the baseline ADR; medium, high, and any design-system change write their own. Higher risk means more locks and a stricter verifier. Runtime locks for AI features in the app are built by the unit that adds them and audited at launch by `product-launch-audit`. Full rules: [Guardrails](references/guardrails.md).

8. **Roles at model tiers, not model names.** `CONFIG.md` maps tiers to each tool's models; `scripts/gen_guardrails.py` writes one subagent per role with its model.

   | Role | Phases | Tier | Gets |
   | :--- | :--- | :--- | :--- |
   | Planner / orchestrator (main session) | 0–2, then spawns the rest and relays `BLOCKED:` questions to the user | top | Everything |
   | `loop-maker` (`loop-maker-high` for high risk) | 3–4 | mid (high risk: top) | Contract path only |
   | `loop-verifier` (`loop-verifier-strict` for medium and high risk) | 5 | mid (medium/high: top) | Contract path, diff, `check_loop.py` JSON |
   | `loop-scribe` | 6 | small | Contract path, verdict table, diff |

   Planning errors compound across every unit, so planning gets the top tier; the build spends the most tokens, so it gets mid. Never put the verifier below mid: a weak verifier approves what it's shown. Tests are never written at the small tier. Name roles in prompts and docs, never models. If the main session runs below `PLANNER_TIER`, say so before Phase 1. Codex agents use underscores (`loop_maker`).
   - **No subagent tool?** Stop and ask the user to run that role in a fresh session on the role's model, given only that role's inputs. Never run a role inline, least of all verification.

9. **A change ships with its ripple.** When a written spec, contract, schema, rule or event changes, grep every name it renames or redefines across `specs/`, `active/` and `history/decisions/`, fix every hit in the same pass (accepted ADRs get a superseding ADR, not an edit), then re-run `check_loop.py plan`. Never hand the leftovers back as a question.

---

## Phase 0: Setup (once per repo)

Skip when `check_loop.py guardrails` already returns `"ok": true`.

1. **Config**: copy `CONFIG.example.md` to the repo root as `CONFIG.md` (not into the skill folder, which may be a symlink shared across repos). Set the commands, paths, breakpoints, and analytics fields for this stack.
2. **Guardrails** (a human runs it; the generated files are protected from the agent): `scripts/gen_guardrails.py --init --git-hook`. Set `adr_required_paths` to where this repo's design system lives. The agent drafts the **baseline guardrails ADR** (`templates/GUARDRAILS_ADR_TEMPLATE.md`). Details: [Guardrails](references/guardrails.md).
3. **Human-only steps**: stop and ask, with exact instructions. Never work around a missing one.
   - A dev database login without `DELETE`/`DROP`; no production credentials in the agent's environment.
   - Dev and prod analytics projects and keys ([Analytics](references/analytics.md#phase-0-accounts-and-keys-human-only)).
   - For each free outside service the app uses: a dev/sandbox key, plus a **read-only, narrowly scoped dev credential** so free live tests can read back what arrived. Their hosts go in `LIVE_ALLOWED_HOSTS`. Paid services get a spend limit on their dev key and never go on that list ([Test tiers](references/test-mapping-guide.md#when-live-tests-run)).
4. **Check**: `check_loop.py guardrails` returns `"ok": true`. Phase 1 doesn't start until it does.

---

## Phase 1: Milestone Plan & Unit Contracts

1. **Frame the product and stack**
   - Read `CONFIG.md` and `specs/engineering/` for the stack and storage. Only ask about stack or database on a brand-new empty repo; in an existing codebase, reuse the stack and surface only feature-specific tradeoffs.
   - Read `specs/product/`: prioritized scope and tier-tagged flows (F1..Fm `[P0|P1|P2]`). If it doesn't exist, define them with the user first: outcomes, user stories, out-of-scope boundaries, and a tier per flow (P0 = the flows that test the riskiest assumption).
   - Frame tradeoffs as user gains vs. losses and concrete engineering cost. If non-obvious architectural forks exist, **ask the user first** with concrete options.
2. **Sequence the units** to cover **every** P0–P2 flow, in this order:
   1. **Walking skeleton** (`infra`): app shell, data layer, one end-to-end round trip, tests and lint running. Only what every journey needs. **Launch-hygiene basics go here** (cheap now, painful to retrofit): real git repo with a remote; secrets only in env (`.env` gitignored); error tracker; analytics, session replay, and the analytics test kit ([Analytics](references/analytics.md#skeleton-unit)); rate limit on public and login endpoints; every data-touching route behind auth; when the product has a sign-in gate, a **dev-only sign-in bypass** so every walkthrough is reachable from the first unit ([Guardrails](references/guardrails.md#dev-only-sign-in-bypass)); cites the baseline guardrails ADR.
   2. **Load-bearing decisions** also go in the skeleton, even when the feature using them is P2: choices expensive to retrofit (data scoping key such as `owner_id`/`tenant_id`, ID scheme, sync model, auth seam as an interface). One ADR each.
   3. **P0 journeys**, then **P1**, then **P2**. Feature-specific infrastructure (external API seam, eval harness, invite tables, scheduler) arrives just in time, as an `infra` unit right before the first journey that needs it.
   4. **Reporting** (last unit): dashboard, reports, or saved queries over the events from earlier units.
   - Every unit leaves the app runnable and states what a human can try once it ships. Infra units prove themselves through the skeleton's round trip or a runnable harness, never "nothing visible yet."
3. **Write every contract** with `templates/UNIT_TEMPLATE.md` at `active/NN-<milestone>/units/NN-<slug>.md`. No placeholders. Fill `Type`, `Serves` (flows), `Tier`, `Risk`, `Guardrails ADR`, and **Living Specs Affected** (which `specs/product/` and `specs/engineering/` files it will create or update). Write `active/NN-<milestone>/plan.md` with `templates/PLAN_TEMPLATE.md`.
4. **Find the scenarios**
   - **Read `references/scenarios.md` before writing any T or M scenario.** Walk each flow across its 8 dimensions: Actor/Auth, Flow Paths/Abandonment, Data Volumes/Zero State, Input Boundaries, AI Failures, Human Agency/Recovery, Network/Concurrency, Platform/A11y.
   - **Read `references/test-mapping-guide.md` to place each one**: T or M, and which tier (unit, integration, end-to-end, live). Prefer automated; manual only for human judgment, paid calls, or what a program can't do.
   - Fill the **Scenario Coverage** table: each dimension lists its T/M tokens or a one-line reason it's skipped, and **Tiers used** names any tier skipped and why. Consider every dimension; don't test every one.
   - **Clarification gate**: if expected behavior is ambiguous or has several valid UX readings, **stop before writing contracts** and ask the user (protocol: `references/scenarios.md` §2). Never guess product behavior.
   - **Part A, T scenarios**: deterministic logic, dirty payloads, schema repair, boundary inputs, security invariants. Every journey unit has an end-to-end happy-path T (`(e2e)`). Every unit that calls a free outside service has a `[Live]` T (`(live)`). Medium and high risk add a `[Guardrail]` scenario per lock (the blocked action stays blocked); high risk adds an `[Abuse]` scenario (injection, wrong-tenant access, replay).
   - **Part B, M scenarios**: key flows, mobile/responsive states, error recovery and human override. Every step must be doable by a person once this unit ships; a step that needs a later unit, an account or key the human doesn't have yet, or a particular time of day moves to the unit that makes it doable (or uses a dev override). UI walkthroughs name their expected look: the mock frames for the screens they cover plus a short "what to look for" list. Paid or non-automatable live checks are `[Live]` walkthroughs that state their cost per run and when they run.
   - **Part C, Instrumentation**: events plus an `[Instrumentation]` T scenario for every journey unit ([Analytics](references/analytics.md#unit-contracts-phase-1-part-c)).
   - Format for all three: `UNIT_TEMPLATE.md`. UI units: follow `VIEWPORT_BREAKPOINTS` and `PARITY_REFERENCE_URL` in `CONFIG.md`.
5. **Check seams and dependencies**: does each unit get the schema or seam it relies on from an earlier one? Resolve schema, API, or contract conflicts before any code. Then run the validator and fix every error it reports:
   ```bash
   python .claude/skills/product-engineering/scripts/check_loop.py plan
   ```
6. **Checkpoint**: present the plan, contracts, and ADRs; pause for approval to build. **High-risk units** pause again before their build: present the design and the locks, and get approval.

---

## Phase 2: Architectural Decision Gate

1. **Triggers**: framework or runtime choices, schema migrations, third-party API providers, security boundaries, deliberate cuts of planned scope, and guardrails: the baseline in the skeleton, one ADR per medium- or high-risk unit, any loosening of a lock or lowering of a risk level (a new ADR superseding the old one), and design-system changes (tokens, type, color, spacing, global styles, shared components) at any risk level. UI copy needs none.
2. **Align, then write**: present options, user and technical tradeoffs, and a recommendation. Once aligned, write `templates/ADR_TEMPLATE.md` at `history/decisions/NNN-<slug>.md`: context and problem, decision and how its boundary is enforced, alternatives rejected and why, consequences and accepted costs.

---

## Phases 3–4: Tests First, then Build (`loop-maker`)

Spawn a fresh `loop-maker` (`loop-maker-high` for high risk) with the contract path and nothing else from planning. If it returns `BLOCKED:`, put the question to the user, record the answer in the contract, and spawn a new maker.

**Phase 3, tests first**
1. Tests go in `tests/<subsystem>/` or the configured test directory, named by token (`test_t1_happy_path`).
2. Unit, integration and end-to-end tests stub networks, third-party APIs (e.g. Resend, Stripe), clocks, and AI model calls (patterns: `references/test-mapping-guide.md` §3); they run fast and deterministically. Free live tests reach only `LIVE_ALLOWED_HOSTS` and skip-and-report without a dev key. The test network lock blocks everything else, and paid keys are stripped from the test environment ([Guardrails](references/guardrails.md#test-network-lock)). `TEST_COMMAND` runs every automated tier, so Phase 5 sees them all.
3. Run them and confirm they fail for the expected reasons.

**Phase 4, build**
1. Business logic, validations, and data models in pure core modules first. Keep deterministic rules out of LLM prompts and UI glue.
2. Thin adapters second: routes, controllers, templates, CLI. Enforce scoping at the data-access seam. Emit events through the single `track()` seam and add new ones to the catalogue ([Analytics](references/analytics.md#build-phase-4)).
3. When a test fails unexpectedly, read the full output and trace the root cause before editing. No shotgun fixes. Never weaken a contract-mandated assertion to make it pass.
4. Once green, simplify the changed files: inline single-use wrappers, drop speculative abstractions and redundant comments. Re-run tests, then `LINT_COMMAND` and `FORMAT_COMMAND`.

---

## Phase 5: Independent Verification (`loop-verifier`)

1. Run `check_loop.py fingerprint`.
2. Spawn a fresh `loop-verifier` (`loop-verifier-strict` for medium and high risk). Its prompt gets only: the contract path, the `git diff` of the unit's changes, the `check_loop.py` JSON, and a pointer to [verification steps](references/verification.md). Never pass the maker's reasoning, summaries, or "known issues" notes. The verifier has no write tools, and the guard hook limits its Bash to read-only commands, `check_loop.py`, and `verifier_bash_allow`.
3. Free live tests run inside `TEST_COMMAND`. If a service has no read-only credential, do its **semi-automated** read-back yourself through `ANALYTICS_ACCESS` (or the service's MCP) and give the verifier the result, labelled as such ([Analytics](references/analytics.md#verify-phase-5)). Paid `[Live]` walkthroughs are not run here: they run at the Phase 6 checkpoint, by the user or with the user's OK for that run.
4. When it returns, run `check_loop.py fingerprint` again. A different hash voids the verdict; re-run with a new verifier.
5. It returns the verdict table plus findings with a certainty of 1–10. Findings at 7+ block a PASS (5+ for high risk); 4–6 are listed as **Unverified**; below 4 are dropped.
6. **On FAIL**: a new maker gets the contract path plus the findings, then a **new** verifier re-runs the full gate. Don't reuse the old verifier or narrow its scope to the fixes. After 3 fix → re-verify cycles, stop and ask the user.

---

## Phase 6: Living Spec Sync (`loop-scribe`)

Spawn `loop-scribe` with the contract path, the verdict table, and the diff. Review its file list before the checkpoint. A unit isn't complete until this is done.

1. **Sync specs**: every file in **Living Specs Affected**, plus any other area the unit changed: `specs/engineering/<subsystem>.md` (`templates/LIVING_SPEC_TEMPLATE.md`) and, if requirements changed, `specs/product/` (`templates/PRODUCT_SPEC_TEMPLATE.md`). Document shipped behavior from the code, not the contract; where they differ, the spec follows the code and lists the difference under **Known Gaps**. Record non-obvious domain invariants in the engineering spec. Update `CONFIG.md` for tooling quirks, and `specs/README.md` when routes, modules, or env vars changed. Remove obsolete descriptions (no strikethroughs).
2. **Update status**: tick acceptance criteria in the contract, update its row in `plan.md`, and note manual testing observations. **Last unit done**: `git mv active/NN-*/ history/milestones/NN-*/` in the same pass and repoint links to it (`check_loop.py plan` fails on a plan whose units are all done).
3. **Reference screenshots (UI units)**: capture each page the unit's M steps cover at every `VIEWPORT_BREAKPOINTS` width (signed in through the dev bypass where needed) into `active/NN-*/units/NN-reference/`, and link them from the M step so the user has something to compare against.
4. **Checkpoint**: present user impact, modified files, test results, the verdict table, and exact M steps for the user, including any paid `[Live]` walkthrough with its cost. Leave diffs uncommitted unless `AUTO_COMMIT` is `true`. Then queue the next unit for Phase 3.
   - **End with the one decision the user must make now, or with nothing.** Don't append side items. Anything unresolved goes in the **Open Questions** section of the unit it blocks and is raised when that unit is next worked on.

---

## Where Work Stands

Don't make the user type phase commands. Inspect `active/`, `specs/`, and `tests/` and advance:
- `check_loop.py guardrails` fails → Phase 0; pause for the human-only steps.
- No plan → Phases 1–2; pause for approval.
- Incomplete unit in `plan.md` → Phases 3–6 for it in one sequence, each through its role; pause at the Phase 6 checkpoint.
- **P0 checkpoint**: after the last P0 unit, pause before any P1 work. The user runs the P0 journeys hands-on and the paid `[Live]` walkthroughs shipped so far, and confirms the hypothesis-metric events are arriving. Before real users, run `product-launch-audit`. If what they learn changes priorities, update the spec and re-run `check_loop.py plan`.

---

## References

* [Guardrails: locks, not prompts](references/guardrails.md)
* [Analytics: instrumented by default](references/analytics.md)
* [Verification steps (Phase 5)](references/verification.md)
* [Scenario discovery and clarification](references/scenarios.md)
* [LLM and probabilistic failure archetypes](references/llm-failure-archetypes.md)
* [Test levels and mocking](references/test-mapping-guide.md)
