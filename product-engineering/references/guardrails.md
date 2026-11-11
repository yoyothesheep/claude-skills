# Guardrails: locks, not prompts

A prompt is a keep-out sign. A guardrail is something the environment enforces whatever the agent decides: permissions, credentials, hooks, a sandbox, a CI check. If the agent can talk its way past it, it isn't one.

Two kinds, handled in different places:

| Kind | Limits | Set up in | Checked by |
| :--- | :--- | :--- | :--- |
| **Dev-time** | The agent that builds the app | Phase 0 setup (`scripts/gen_guardrails.py`) | `check_loop.py` + Phase 5 verifier |
| **Runtime** | The AI features inside the app | The unit that builds the feature | `product-launch-audit` before real users |

## Setup (once, by a human, in Phase 0)

1. `python scripts/gen_guardrails.py --init --git-hook --ci` copies `templates/guardrails/guardrails.json` to `.agent/guardrails.json` and generates each agent's config from it, the pre-commit hook, and a GitHub Actions workflow. Run it yourself: the generated files are protected from the agent. Commit and push `.github/workflows/guardrails.yml`; nothing else is needed on GitHub.
2. Write the **baseline guardrails ADR** (`templates/GUARDRAILS_ADR_TEMPLATE.md`) and cite it from the skeleton unit.
3. Credentials, which the scripts cannot do for you. This is the real boundary, because a shell can dodge pattern checks:
   - The dev database login has no `DELETE`/`DROP`.
   - Dev credentials only, each scoped and spend-limited. Assume the agent can read any file or variable on the machine, `.env` included: a token it can find, it can use. Production keys, host tokens and cloud credentials live in the host's dashboard, never where the agent runs.
   - Run the agent in a sandbox or container where it can't reach what it doesn't need.
   - The verifiers are `loop-verifier` and `loop-verifier-strict` (same rules, higher model tier for medium and high risk). How read-only they are depends on the tool:
     - **Claude Code** (`.claude/agents/`): no write tools, Bash limited by the hook to read-only commands, `check_loop.py`, and `verifier_bash_allow` (CONFIG.md's test/lint commands; add a dev-server command by hand if M walkthroughs need one).
     - **Cursor** (`.cursor/agents/`, which Cursor prefers over `.claude/agents/`): `readonly: true`, which blocks file edits and state-changing shell commands. The `.claude/` copies carry `readonly: true` too, so Cursor's fallback is locked as well.
     - **Codex** (`.codex/agents/`): no per-agent lock; a subagent inherits the parent session's sandbox. Low risk: run it as a subagent and rely on the fingerprint. Medium and high risk: run Phase 5 in a fresh `codex --sandbox read-only` session given only the verifier's inputs. If the test command must write (caches, temp databases), use `--sandbox workspace-write` and rely on the fingerprint.
     - Everywhere: `check_loop.py fingerprint` before and after catches anything that slips through.

**Lock only what git can't undo.** Git rolls back edits to tracked files, so those get checks, not locks: commits and pushes are allowed, edits to `history/` and the design system are flagged by `check_loop.py` rather than blocked. Commits follow `AUTO_COMMIT` in `CONFIG.md`. What git can't undo gets a lock:

| Locked | Why git doesn't help |
| :--- | :--- |
| Reading secret files | The value goes to the model provider |
| `rm -rf`, `reset --hard`, `clean -f` | They destroy uncommitted work |
| Force-push | Rewrites the remote's history |
| `DROP`/`TRUNCATE`, `curl \| sh` | They act outside the repo. The real lock is the dev login without delete |
| `terraform destroy`, `railway down`, cloud `delete`/`destroy` | They act on infrastructure. The real lock is dev credentials only |
| Editing the guardrail config | An agent that loosens its own locks can then do something irreversible |
| Secrets and user data in commits | Once pushed, rolling back doesn't un-leak them |
| Skipping the pre-commit hook (`--no-verify`, `core.hooksPath`) | It turns off the check above |

## What gets enforced

`.agent/guardrails.json` is the single source. It holds `secret_paths` (never read or written), `protected_paths` (guardrail config, changed by hand with an ADR), `append_only_paths` (`history/decisions/**`, `history/milestones/**`: new files only), `private_data_paths` and `private_data_allow` (user-data files that never get committed: databases, dumps, backups, exports, logs, and CSVs outside `tests/fixtures/`), `adr_required_paths` (the design system: tokens, theme, global styles, shared UI components; the agent may edit them, but the change needs a new ADR), and denied shell commands. Set `adr_required_paths` to where this repo's design system lives.

| Layer | Works for | How |
| :--- | :--- | :--- |
| Credentials, sandbox | Any agent | Outside the agent entirely. Strongest. |
| `check_loop.py guardrails` in pre-commit and CI | Any agent | Fails on protected or frozen edits, config changes without a new ADR, and the privacy gates below. `--git-hook` installs it and `--ci` writes `.github/workflows/guardrails.yml`, which runs it over each push's commits plus gitleaks: the server-side copy no one can skip, free on GitHub Actions. Both use the copy vendored at `.claude/hooks/check_loop.py`. |
| `.claude/settings.json` deny rules + `guard.py` PreToolUse hook | Claude Code | Generated. The hook blocks with exit code 2. |
| `.cursor/hooks.json`: the same `guard.py` on `preToolUse` and `beforeReadFile` | Cursor | Generated. Exit code 2 plus a `deny` answer blocks; an allowed call answers `{"permission": "allow"}`, since Cursor blocks a permission hook whose output isn't valid JSON. `beforeReadFile` also covers files attached with `@`. Project hooks run only in a trusted workspace. |
| `.codex/hooks.json`: the same `guard.py` on `PreToolUse` (`Bash`, `apply_patch`) | Codex | Generated when `CODEX_MODELS` is set. File edits arrive as patch text; the hook checks every `Add`/`Update`/`Delete`/`Move to` path in it. Trust the hook once with `/hooks`; Codex skips new or changed hooks until you do. Codex fails open when a hook errors or times out, so treat this layer as a guardrail, not a boundary. Still set the session's sandbox by hand (workspace-write, approval on request). |
| `.cursorignore`, `.geminiignore`, `AGENTS.md` block | Gemini, others (and Cursor indexing) | Generated. Secret paths and plain-language rules. Best-effort. |

`guard.py` finds the repo from its own location (`.claude/hooks/`), not from the environment, so all three tools enforce the same `.agent/guardrails.json`. `check_loop.py guardrails` fails when `.cursor/` or `.codex/` exists without its hook registered, or when a Cursor verifier lost `readonly: true`.

Repos set up before these adapters existed: add `.cursor/hooks.json`, `.cursor/agents/loop-*.md` and `.codex/hooks.json` to `protected_paths` by hand (with an ADR), then re-run `gen_guardrails.py`. It warns until you do, and likewise until the template's `denied_bash_patterns` are copied in.

## Privacy gates (every commit)

`check_loop.py guardrails` runs in the pre-commit hook and CI, so these hold for any agent or human:

1. **No secret files in git**: every `secret_paths` entry is gitignored, and none is tracked.
2. **No user-data files**: nothing matching `private_data_paths` outside `private_data_allow`.
3. **No secrets or PII in changed files**: likely keys and tokens, card numbers (Luhn-checked, test cards allowed), and SSNs fail. Real-looking emails and phone numbers are warnings for the verifier.
4. **gitleaks** runs on staged changes when installed, in addition to the built-in patterns.
5. **Synthetic fixtures only**: fake names, `example.com` emails, test card numbers. Never copy real user records into tests.
6. **If a secret was ever committed, rotate it.** Rewriting history doesn't un-leak a pushed secret.

## Risk level

Assigned per unit in Phase 1 from blast radius and reversibility: the worst case if the agent gets it wrong, and whether it can be undone. Unsure: take the higher level. Lowering a level or loosening a lock after planning needs a new ADR that supersedes the old one.

| | Low | Medium | High |
| :--- | :--- | :--- | :--- |
| **Typical unit** | UI copy, one-off page tweaks, static pages | New feature on app data, external API call, schema change | Auth or permissions, payments, deletes or migrations on real data, PII, an AI feature that acts |
| **Worst case** | Cosmetic; a revert fixes it | Bad data or a broken flow, recoverable with effort | Data loss, leak, money or harm; not undoable |
| **Locks** | Baseline only | Baseline + deny rules scoped to the unit's paths | Baseline + throwaway branch or database copy, no real credentials |
| **ADR** | Cites the baseline ADR (design-system changes: own ADR) | Own ADR | Own ADR, naming what could still go wrong |
| **Tests** | Normal T/M | + a `[Guardrail]` T per lock | + `[Abuse]` T: injection, wrong-tenant, replay |
| **Verifier** | Findings at 7+ block | Confirms locks exist and negative tests pass | Same, findings at 5+ block, diff-reviews guardrail config |
| **Human checkpoint** | After the unit | After the unit | Before building (approve design and locks) and after |

Design-system changes (tokens, type, color, spacing, global styles, shared components) need their own ADR at any risk level: they ripple across every page and are easy to drift. UI copy doesn't.

`check_loop.py` enforces: any diff touching `adr_required_paths` carries a new ADR; the contract has a valid Risk and a Guardrails ADR that exists; medium and high have a `[Guardrail]` T scenario and their own ADR (not the baseline); high has an `[Abuse]` T scenario.

## Test network lock

Tests must never spend money or touch production by accident. The skeleton installs this in the test setup (e.g. `conftest.py`):

1. Outbound connections are blocked except to the local machine and the hosts in `LIVE_ALLOWED_HOSTS` (`CONFIG.md`).
2. `LIVE_ALLOWED_HOSTS` holds free dev/sandbox services only (e.g. analytics ingestion and its query API). A paid host never goes on it.
3. Paid-service keys (LLM, SMS, paid APIs) are removed from the test process's environment, so a paid call fails for lack of credentials even if the host were reachable.
4. Only dev/sandbox keys are ever present; production keys never are.
5. Free live tests tag their side effects with a run id.

Proof: a `[Guardrail]` T in the skeleton — a connection to a host not on the list fails; a paid key is absent inside the test process; a free live test without its dev key is reported as skipped, not passed. Paid live checks are manual `[Live]` walkthroughs with a stated cost, run by the user or with the user's OK for that run, and each paid dev key carries a spend limit.

## Dev-only sign-in bypass

When the product has a sign-in gate, the skeleton ships a one-click way in for local development, so a person (and the orchestrator's screenshots and live checks) can reach every page from the first unit. It is a back door unless locked:

1. The bypass route (e.g. `/dev/signin`) is registered only when `ENV=dev`; in every other environment it doesn't exist (404).
2. The app refuses to start when the bypass flag is set with `ENV=prod`.
3. The deploy config never sets the flag (a test parses it).
4. It creates the same session real sign-in creates; the auth check on every other route is unchanged.

Proof: `[Guardrail]` T scenarios for 1–3, and the skeleton's "every route needs auth" test still passes. The unit that adds it cites a guardrails ADR naming these locks (auth work is high risk).

## Production data

Every unit that deploys to production or changes production data (migrations, backfills, imports, deletes) is high risk. Before each one is built, check that `denied_bash_patterns` covers the chosen host, cloud and tools (the template names common ones only). Add each missing destructive command (delete, destroy, down, reset on live data) to `.agent/guardrails.json` by hand, re-run `gen_guardrails.py`, and record it in the unit's guardrails ADR. Its locks:

1. The agent writes deploy config only. A human holds the host's tokens and runs every production action; each token is scoped to one environment and the actions it needs.
2. Backups leave the volume and the account the app and agent can reach (e.g. a bucket with write-only credentials and object lock). A backup on the same volume is deleted with it.
3. A restore from backup into a fresh location is a T test, and a human does one real restore before launch.

## Runtime locks (AI features in the app)

Built into the unit that adds the AI feature, proved by its `[Guardrail]` / `[Abuse]` tests, and checked at launch by `product-launch-audit`:

1. Least-privilege tools: if the feature doesn't need it, the tool doesn't exist.
2. Schema validation and allowlists on every tool argument.
3. Approval bound to the exact action for anything irreversible.
4. PII redacted before the model call.
5. Retrieved and uploaded text labeled as untrusted evidence, never as instructions.

Break the trifecta: never give one feature private data + untrusted content + a way to send data out.
