# `loop-engineering` Test Cases (Workshop & Eval Suite)

Use these scenarios to verify that `loop-engineering` advances naturally between checkpoints, asks about architectural tradeoffs before generating files, maps `specs/product/` user flows ($F_1..F_m$) into unit test matrices ($T_1..T_n$ & $M_1..M_k$), simplifies code automatically, and passes `scripts/check_loop.py`.

---

## Test Case 1: Product Flows ($F_1..F_m$) $\to$ Milestone Plan & Tradeoff Alignment

**Precondition:** `specs/product/reading-list.md` exists (from `product-scoping` Test Case 1) with flows `F1..F4`.

**Prompt:**
> "Let's plan and build this milestone using loop-engineering."

**Expected Stage 1 Behavior (Pass Criteria):**
1. **No subcommand memorization required:** Detects that no active milestone exists in `active/` and enters Phases 1–2 automatically.
2. **Checks `CONFIG.md` against repo stack:** Verifies `TEST_COMMAND`, `LINT_COMMAND`, and `FORMAT_COMMAND` match the project's actual toolchain.
3. **Pauses on Architectural Tradeoffs first:** Before generating unit files, asks the user to confirm key technical choices (e.g., storage mechanism such as SQLite vs. JSON/in-memory, HTML parser library vs. stdlib) framed in terms of user impact vs. engineering cost.
4. **Generates Complete Upfront Unit Contracts:** Once aligned, writes `history/decisions/001-*.md` (if needed), `active/01-reading-list/plan.md`, and all unit contracts (`active/01-reading-list/units/01..N-*.md`) with:
   - Every `F1..F4` flow mapped into explicit **Automated Tests ($T_1..T_n$)** and **Manual E2E Scenarios ($M_1..M_k$)**.
   - Zero placeholder units.
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
   - Runs `python loop-engineering/scripts/check_loop.py 01` and verifies `"mechanical_ok": true` with `"missing": []`.
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
python loop-engineering/scripts/check_loop.py 01
```

**Expected JSON Output Invariants:**
- `"spec.test_ids"` lists all `**T1`, `**T2`, ... tokens from `active/*/units/01-*.md`.
- `"test_mapping.missing"` is `[]` when matching `test_t1_*` functions exist.
- `"gates.tests.passed"`, `"gates.linter_check.passed"`, and `"gates.linter_format.passed"` are `true`.
- `"mechanical_ok"` is `true` (exit code `0`).
