# product-launch-audit

A one-time check of an existing app before it goes live. It covers five areas:
- infrastructure;
- code quality;
- security;
- observability and cost;
- failure and rollback.

It works on any codebase, including Replit, Lovable or Bolt prototypes, whether or not it was built with `product-engineering`. It reports only; it fixes nothing unless you ask.

Instructions for Claude live in [SKILL.md](SKILL.md). This page is for people.

## Flow

```mermaid
flowchart TD
    start([Repo to audit]) --> stage{{"You pick the stage:<br/>PMF / Growth / Scale"}}
    stage --> scan[Run the repo scan script]
    scan --> heur[Open every pattern-match hit<br/>and confirm or dismiss it]
    heur --> judge[Check each checklist row<br/>for the stage, with file and line]
    judge --> manual{Rows the script can't check?}
    manual -- yes --> ask{{"You answer, e.g. from<br/>a provider dashboard"}}
    manual -- no --> report
    ask --> report[Report: status per area,<br/>blockers, findings]
    report --> fix{{"You decide what to fix"}}
    fix --> done([Fixes only if you ask])

    classDef you fill:#fff4d6,stroke:#c99a2e,color:#3d2e00;
    class stage,ask,fix you;
```

Yellow boxes are where the skill stops and waits for you.

## Where it stops for you

| Stop | What you do |
|---|---|
| Start | Pick the stage: `PMF` (the default), `Growth` or `Scale`. It decides which checklist rows apply. |
| Rows needing a human | Answer from your accounts or dashboards, e.g. whether a paid API key has a spending cap. Nothing is marked as passing on a guess. |
| Report | Choose what to fix, if anything. |

## What you get

- A status table covering the five areas: ✅, ⚠️ or 🔴.
- **Blockers**, each with its file and line. Any 🔴 in security is a launch blocker and is listed first.
- Findings in three groups:
  - fixes the AI can make;
  - fixes that need a credential or account from you first;
  - things that aren't a code problem, such as a rollback dry run or a spending cap.

The checklist is in [CHECKLIST.md](CHECKLIST.md).

## Works with

- [product-engineering](../product-engineering/README.md) runs this audit at its P0 checkpoint, before real users.
