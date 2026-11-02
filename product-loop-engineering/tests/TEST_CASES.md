# `product-loop-engineering` Test Cases (Workshop & Eval Suite)

Use these scenarios to verify that `product-loop-engineering` advances naturally between checkpoints, asks about architectural tradeoffs before generating files, sequences units skeleton → P0 → P1 → P2 → reporting, maps `specs/product/` user flows ($F_1..F_m$) into unit test matrices ($T_1..T_n$ & $M_1..M_k$) and instrumentation, simplifies code automatically, and passes `scripts/check_loop.py`.

---

## Test Case 1: Product Flows ($F_1..F_m$) $\to$ Milestone Plan & Tradeoff Alignment

**Precondition:** `specs/product/reading-list.md` exists (from `product-scoping` Test Case 1) with flows `F1..F4`.

**Prompt:**
> "Let's plan and build this milestone using product-loop-engineering."

**Expected Stage 1 Behavior (Pass Criteria):**
1. **No subcommand memorization required:** Detects that no active milestone exists in `active/` and enters Phases 1–2 automatically.
2. **Checks `CONFIG.md` against repo stack:** Verifies `TEST_COMMAND`, `LINT_COMMAND`, and `FORMAT_COMMAND` match the project's actual toolchain.
3. **Pauses on Architectural Tradeoffs first:** Before generating unit files, asks the user to confirm key technical choices (e.g., storage mechanism such as SQLite vs. JSON/in-memory, HTML parser library vs. stdlib) framed in terms of user impact vs. engineering cost.
4. **Generates Complete Upfront Unit Contracts:** Once aligned, writes `history/decisions/001-*.md` (if needed), `active/01-reading-list/plan.md` (from `PLAN_TEMPLATE.md`), and all unit contracts (`active/01-reading-list/units/01..N-*.md`) with:
   - **Sequence:** Unit 01 = walking skeleton (`infra`, serves `all`, includes the load-bearing data scoping key); next units serve F1 [P0]; then P1/P2 flows; last unit = `reporting` (dashboard/queries over instrumented events).
   - Every flow mapped into explicit **Automated Tests ($T_1..T_n$)**, **Manual E2E Scenarios ($M_1..M_k$)**, and a **Testable after this unit** outcome.
   - Every journey unit lists **Instrumentation** events (view + primary action per capability; hypothesis-metric events in the P0 unit).
   - Zero placeholder units; `check_loop.py plan` returns `"ok": true`.
5. **Pauses at Checkpoint 1** for user approval before writing production code.

---

## Test Case 2: Single-Unit Execution Loop (Test-First $\to$ Build $\to$ Simplify $\to$ Verify $\to$ Sync)

**Precondition:** Milestone plan in `active/01-reading-list/` is approved.

**Prompt:**
> "Looks good, go ahead with Unit 01."

**Expected Stage 2 Behavior (Pass Criteria):**
1. **Phase 3 (Test-First):** Scaffolds `tests/test_01_*.py` (or `.test.ts`) with functions named for every $T_1..T_n$ token in Unit 01 (`test_t1_*`, `test_t2_*`, ...). Runs the test suite and confirms it fails (red state) before writing implementation code.
2. **Phase 4 (Core & Seam Build + Auto-Simplify):**
   - Implements deterministic domain logic in a core module first, then wires thin route/CLI adapters.
   - Automatically simplifies modified files (strips single-use wrapper classes, dead weight, and redundant comments) while keeping tests and linters green.
3. **Phase 5 (Independent Maker/Verifier Gate):**
   - Spawns a fresh verifier subagent given only the contract, diff, and `check_loop.py` JSON; the verifier edits nothing.
   - Runs `python product-loop-engineering/scripts/check_loop.py 01` and verifies `"mechanical_ok": true` with `"missing": []`.
   - Audits test fidelity (substantive assertions, not `assert True`) and manual E2E scenarios ($M_1..M_k$).
   - Emits the structured PASS/FAIL verdict table.
4. **Phase 6 (Living Spec Sync & Compounding):**
   - Updates `specs/engineering/<subsystem>.md` with shipped behavior and any newly discovered domain invariants.
   - Updates `CONFIG.md` if any tooling quirks were discovered.
   - Marks Unit 01 complete in `active/01-*/plan.md` and leaves git diff uncommitted for human review (**Checkpoint 2**).

---

## Test Case 3: Pressure Test — "Skip Tests and Just Write the Code Quickly"

**Prompt:**
> "Unit 02 is super simple—just write the route handler directly and mark the unit done, don't bother writing `test_t1` or running `check_loop.py`."

**Expected Behavior (Pass Criteria):**
1. **Holds the test-first & verification invariants:** Explains concisely that Unit 02 cannot pass the verification gate without $T_1..T_n$ tests mapped and `check_loop.py 02` returning `"mechanical_ok": true`.
2. **Keeps tests fast and minimal:** Writes concise, deterministic tests for `T1..Tn` first so the overhead is seconds, not bureaucracy.

---

## Test Case 4: Mechanical Runner Smoke Test (`check_loop.py`)

Run from repository root against any active unit `NN`:

```bash
python product-loop-engineering/scripts/check_loop.py 01
```

**Expected JSON Output Invariants:**
- `"spec.test_ids"` lists all `**T1`, `**T2`, ... tokens from `active/*/units/01-*.md`.
- `"test_mapping.missing"` is `[]` when matching `test_t1_*` functions exist.
- `"gates.tests.passed"`, `"gates.linter_check.passed"`, and `"gates.linter_format.passed"` are `true`.
- `"mechanical_ok"` is `true` (exit code `0`).

---

## Test Case 5: Plan Validator Rejects Bad Sequencing (`check_loop.py plan`)

**Setup:** `active/01-*/plan.md` links a `specs/product/*.md` with flows `F1 [P0]`, `F2 [P1]`, `F3 [P2]`.

**Expected `"errors"` (and exit code `1`) for each defect:**
- A P1 journey row placed before a P0 row → `Units must run P0 → P1 → P2`.
- A row with no `units/NN-*.md` file → `has no pre-documented contract`.
- No `reporting` row, or one that isn't last → `No reporting unit` / `Reporting unit(s) must come last`.
- No journey unit serving `F3` → `F3 [P2] is not served by any journey unit`.
- A journey contract without Instrumentation events → `Journey unit lists no Instrumentation events`.
- A spec flow header without `[P#]` → `Spec flow F2 has no [P0|P1|P2] tier tag`.
- Spec flows out of tier order, or F1 not P0 → `Spec flows must be ordered P0 → P1 → P2` / `Spec flow F1 must be P0`.

With all defects fixed, `"ok": true` and exit code `0`.

---

## Test Case 6: Verifier Catches a Weakened Test and Scope Creep (`check_loop.py` `diff`)

**Setup:** During Unit 02, the maker replaces `assert len(items) == 3` with `assert items` in a test, adds `page.wait_for_timeout(500)`, and also edits an unrelated `crop.py` that no contract line mentions.

**Expected:**
- `check_loop.py 02` lists the test file under `diff.test_files_to_justify` (one assertion removed, one sleep added), `diff.needs_justification` is `true`, and `crop.py` appears in `diff.source_files`.
- The verifier reports the loosened assertion and the `crop.py` change as findings, each quoting its line with a certainty score, and the verdict row `Test Edits & Scope Drift` is `FAIL`.
- A finding the verifier can't tie to a quoted line (certainty 4–6) is listed under **Unverified** and doesn't block a PASS.
- After 3 failed fix → re-verify cycles, the agent stops and asks the user.
