# ADR-NNN — Guardrails: [Baseline | Unit NN <name>]

- **Date**: YYYY-MM
- **Status**: `Proposed` | `Accepted` | `Superseded by ADR-XXX`
- **Scope**: [Baseline for every unit | Unit NN]
- **Risk**: [low | medium | high]. Worst case if the agent gets this wrong, and whether it can be undone: [...]

## Locks (enforced, not prompted)

- **Dev-time**: [deny rules, hook, dev credentials without delete, sandbox, branch or database copy for high risk]
- **Runtime (AI features)**: [least-privilege tools, argument validation, approval on irreversible actions, PII redaction, untrusted text labeled; checked at launch by `product-launch-audit`]
- **Proof**: [the `[Guardrail]` / `[Abuse]` T scenarios that show each lock holds]

## What could still go wrong

[Residual risk the locks don't cover, and who watches it.]

## Changed from previous ADR

[Only when loosening or tightening a lock or risk level: what changed and why. Otherwise "n/a".]
