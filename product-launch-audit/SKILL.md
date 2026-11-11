---
name: product-launch-audit
description: >-
  Audit an app (built with or without product-engineering, including Replit/Lovable/Bolt
  prototypes) against five pillars before going live: infrastructure, code quality,
  security, observability and cost, failure and rollback. Runs a repo scan, then
  produces a status table per pillar and findings split into fix-now, needs-your-credentials,
  and not-a-code-problem. Use before launch, before showing investors, or when asked
  "is this safe to ship?"
---

# product-launch-audit

A one-time pre-launch check of an existing codebase. For per-unit checks during a build, use `product-engineering`.

## Inputs

- **Stage**: `PMF` (default), `Growth` or `Scale`. Ask if unclear. The stage decides which rows of [CHECKLIST.md](CHECKLIST.md) apply.
- **Path**: the repo to audit (default: current directory). It does not need to be a git repo or use product-engineering.

## Steps

1. **Scan.** Run the mechanical checks and read the JSON:
   ```bash
   python .claude/skills/product-launch-audit/scripts/audit_repo.py <path>
   ```
   Statuses: `pass`, `warn`, `fail`, `manual` (a human must check; the script cannot).
2. **Verify heuristics.** `endpoints_without_auth` and `secrets_in_source` are pattern matches. Open each listed file and confirm or dismiss it with file and line. Never report a heuristic hit as confirmed without reading it.
3. **Judge the rest.** For each pillar row in [CHECKLIST.md](CHECKLIST.md) at the chosen stage, check the code itself, not the framework's reputation. Cite file and line for every gap.
4. **Handle `manual` rows.** Ask the user, or list them under "Not a code problem". Never mark one pass on a guess. Per-service rows (`paid_key:*`, `infra_token:*`) are answered from each provider's dashboard: a key whose provider can't cap it is a finding, not a pass.
5. **Report** using the format below.

## Report format

```markdown
# Launch audit: <app>, stage <PMF|Growth|Scale>

| Pillar | Status | What's needed |
| :--- | :--- | :--- |
| Infrastructure & hosting | ✅/⚠️/🔴 | ... |
| Code quality & testing | | |
| Security & data | | |
| Observability & cost | | |
| Failure & rollback | | |

## Blockers
<🔴 items, each with file:line>

## Findings
**Fix directly (AI can do it):** ...
**Needs a credential or account from you first:** ...
**Not a code problem (you do it):** ... (rollback dry run, who to call, spend cap, audit)
```

Rules:
- 🔴 = any `fail` or confirmed security gap. ⚠️ = `warn` or unverified `manual`. ✅ = all rows pass.
- Any 🔴 in Security & data is a launch blocker. Say so first.
- Report only. Do not fix anything unless the user asks.
- Evaluation of AI output quality is out of scope here.
- AI runtime locks (least-privilege tools, argument validation, approval on irreversible actions, PII redaction, untrusted text) apply only when the app calls a model. Their dev-time counterpart, locks on the agent that builds the app, lives in `product-engineering`.
