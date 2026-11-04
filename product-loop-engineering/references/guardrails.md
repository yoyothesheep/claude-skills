# Guardrails: locks, not prompts

A prompt is a keep-out sign. A guardrail is something the environment enforces whatever the agent decides: permissions, credentials, hooks, a sandbox, a CI check. If the agent can talk its way past it, it isn't one.

Two kinds, handled in different places:

| Kind | Limits | Set up in | Checked by |
| :--- | :--- | :--- | :--- |
| **Dev-time** | The agent that builds the app | Phase 0 setup (`scripts/gen_guardrails.py`) | `check_loop.py` + Phase 5 verifier |
| **Runtime** | The AI features inside the app | The unit that builds the feature | `product-launch-audit` before real users |

## Setup (once, by a human, in Phase 0)

1. `python scripts/gen_guardrails.py --init --git-hook` copies `templates/guardrails/guardrails.json` to `.agent/guardrails.json` and generates each agent's config from it. Run it yourself: the generated files are protected from the agent.
2. Write the **baseline guardrails ADR** (`templates/GUARDRAILS_ADR_TEMPLATE.md`) and cite it from the skeleton unit.
3. Credentials, which the scripts cannot do for you. This is the real boundary, because a shell can dodge pattern checks:
   - The dev database login has no `DELETE`/`DROP`.
   - No production credentials in the agent's environment.
   - Run the agent in a sandbox or container where it can't reach what it doesn't need.
   - The verifier is `.claude/agents/loop-verifier.md`: no write tools, Bash limited by the hook to read-only commands, `check_loop.py`, and `verifier_bash_allow` (CONFIG.md's test/lint commands; add a dev-server command by hand if M walkthroughs need one). `check_loop.py fingerprint` before and after catches anything that slips through.

**Lock only what git can't undo.** Git rolls back edits to tracked files, so those get checks, not locks: commits and pushes are allowed, edits to `history/` and the design system are flagged by `check_loop.py` rather than blocked. Commits follow `AUTO_COMMIT` in `CONFIG.md`. What git can't undo gets a lock:

| Locked | Why git doesn't help |
| :--- | :--- |
| Reading secret files | The value goes to the model provider |
| `rm -rf`, `reset --hard`, `clean -f` | They destroy uncommitted work |
| Force-push | Rewrites the remote's history |
| `DROP`/`TRUNCATE`, `curl \| sh` | They act outside the repo. The real lock is the dev login without delete |
| Editing the guardrail config | An agent that loosens its own locks can then do something irreversible |
| Secrets and user data in commits | Once pushed, rolling back doesn't un-leak them |

## What gets enforced

`.agent/guardrails.json` is the single source. It holds `secret_paths` (never read or written), `protected_paths` (guardrail config, changed by hand with an ADR), `append_only_paths` (`history/decisions/**`, `history/milestones/**`: new files only), `private_data_paths` and `private_data_allow` (user-data files that never get committed: databases, dumps, backups, exports, logs, and CSVs outside `tests/fixtures/`), `adr_required_paths` (the design system: tokens, theme, global styles, shared UI components; the agent may edit them, but the change needs a new ADR), and denied shell commands. Set `adr_required_paths` to where this repo's design system lives.

| Layer | Works for | How |
| :--- | :--- | :--- |
| Credentials, sandbox | Any agent | Outside the agent entirely. Strongest. |
| `check_loop.py guardrails` in pre-commit and CI | Any agent | Fails on protected or frozen edits and on config changes without a new ADR. `--git-hook` installs it. |
| `.claude/settings.json` deny rules + `guard.py` PreToolUse hook | Claude Code | Generated. The hook blocks with exit code 2. |
| `.cursorignore`, `.geminiignore`, `AGENTS.md` block | Cursor, Gemini, others | Generated. Secret paths and plain-language rules. Best-effort. |

Not generated: a Codex CLI config. I couldn't verify its current keys. Set its sandbox and approval mode by hand (workspace-write sandbox, approval on request) and rely on the first two layers.

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

## Runtime locks (AI features in the app)

Built into the unit that adds the AI feature, proved by its `[Guardrail]` / `[Abuse]` tests, and checked at launch by `product-launch-audit`:

1. Least-privilege tools: if the feature doesn't need it, the tool doesn't exist.
2. Schema validation and allowlists on every tool argument.
3. Approval bound to the exact action for anything irreversible.
4. PII redacted before the model call.
5. Retrieved and uploaded text labeled as untrusted evidence, never as instructions.

Break the trifecta: never give one feature private data + untrusted content + a way to send data out.
