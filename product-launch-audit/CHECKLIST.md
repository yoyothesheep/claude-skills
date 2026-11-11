# Checklist by stage

Each stage includes the rows of the stages before it. `Script` = covered by `audit_repo.py` (id in brackets); the rest is judgment.

## PMF

| Pillar | Row | Script |
| :--- | :--- | :--- |
| Infrastructure & hosting | Code is in a real git repo with a remote | [git_repo, git_remote] |
| | `.env` not committed, in `.gitignore` | [env_committed] |
| | Hosting is always-on (dedicated instance), not cold-start | [hosting_defaults] |
| | Database backups stored outside the volume and account the app and agent can reach; one restore done | [backups] |
| | Rate limit on public and login endpoints | [rate_limit] |
| Code quality & testing | At least one test on the critical flow | [tests_exist, critical_flow_covered] |
| | Tech debt audit: dead code, unused APIs, duplicated logic | judgment |
| Security & data | No hardcoded secrets | [secrets_in_source] |
| | Every endpoint that reads or writes data requires login | [endpoints_without_auth] |
| | Every deploy and cloud token scoped to one environment and the actions it needs; production tokens only in the host's dashboard | [infra_token:*] |
| | Database access controls (RLS or equivalent) on every table | [rls] |
| | No user data in local storage that belongs in the database | judgment |
| | No customer data sent to third-party AI tools | [ai_data_handling] |
| | *If the app calls a model:* tools are least-privilege (nothing the feature doesn't need, no delete or send it doesn't use) | [ai_tool_review] |
| | *If the app calls a model:* every tool argument is schema-validated against an allowlist | [ai_validation] |
| | *If the app calls a model:* irreversible actions (send, delete, pay, publish) need approval bound to the exact action | manual |
| | *If the app calls a model:* PII redacted before the model call | manual |
| | *If the app calls a model:* retrieved and uploaded text is labeled untrusted, and no feature combines private data + untrusted content + a way to send data out | judgment |
| Observability & cost | Error tracker installed (e.g. Sentry) | [error_tracker] |
| | Analytics shows where users drop off | judgment |
| | Monthly cost known | [monthly_cost] |
| | Every paid API key: hard spend cap (or a limit in your own code where the provider can't cap it), spend alerts, restricted to the APIs it uses | [paid_key:*] |
| Failure & rollback | Manual rollback done once as a dry run | [rollback_dry_run] |
| | Named person to call if the API or database goes down | [runbook] |

## Growth

| Pillar | Row | Script |
| :--- | :--- | :--- |
| Infrastructure & hosting | Branch protection; separate staging environment | [ci], [staging] |
| Code quality & testing | Tests on the top flows; PR review; CI/CD | [ci] |
| Security & data | Secrets audited and rotated; role-based access for humans | judgment |
| | CI runs a secret scanner | [ci_secret_scan] |
| | Dependencies reviewed; lockfile committed | [lockfile, dependency_audit] |
| Observability & cost | Uptime monitoring; alerts to Slack; cost by feature | judgment |
| Failure & rollback | Written runbooks; incident docs | [runbook] |

## Scale

| Pillar | Row | Script |
| :--- | :--- | :--- |
| Infrastructure & hosting | Granular permissions for AI agents | [agent_permissions] |
| Code quality & testing | Adversarial review of AI-written code; tech debt roadmap | judgment |
| Security & data | Data governance; retention policy; third-party audit | judgment |
| Observability & cost | Cost governance across model tiers | judgment |
| Failure & rollback | Incident review process | judgment |
