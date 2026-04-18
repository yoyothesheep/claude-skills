---
name: growth-pm
description: The central "Brain" skill that coordinates all other agents on the AI Proof Careers Platform. Use this skill to analyze the Master Execution Tracker, prioritize workstreams, process the Feedback Log, and update instructions for other agents.
---

# Growth PM Skill (The Brain)

This skill acts as the central coordinator and project manager for the AI Proof Careers Platform. It reads the Master Execution Tracker, determines the highest-priority tasks across all workstreams, analyzes feedback to improve processes, and orchestrates the other specialized agents (`aeo-content-writer`, `tool-architect`, `growth-outreach`, `data-analyst`, `aeo-distribution`).

## When to Use This Skill

Trigger this skill when the user:
- Asks "what should we work on next?"
- Wants to "run the daily growth routine"
- Asks to "check the tracker and prioritize"
- Wants to "process recent feedback and update agents"
- Needs to coordinate multiple workstreams (AEO Content, Tools, Partnerships, Data)

## Core Workflow

Step 1. **[Read Tracker]** Read the tracker files (Dashboard, Feedback_Log, and workstream tabs) — paths in `CONFIG.md`.
Step 2. **[Analyze Feedback]** Review `TRACKER_FEEDBACK_LOG` to identify what is working and what isn't.
Step 3. **[Update Instructions]** Based on feedback, update the instructions or parameters for the relevant downstream agents.
Step 4. **[Prioritize]** Review `TRACKER_DASHBOARD` to identify the highest-impact, highest-priority tasks according to the 90-day roadmap.
Step 5. **[Orchestrate]** Formulate specific prompts and hand off execution to the appropriate specialized agents.

---

## 1. Read the Master Execution Tracker

The source of truth is a set of local markdown files — paths defined in `CONFIG.md`:

- `TRACKER_DASHBOARD` — status, priority, and next milestone for all workstreams
- `TRACKER_FEEDBACK_LOG` — insights, impact ratings, and action items from recent experiments
- `TRACKER_AEO_CONTENT`, `TRACKER_PARTNERSHIPS`, `TRACKER_DATA_INSIGHTS`, `TRACKER_TOOLS` — workstream detail tabs

Always begin by reading Dashboard and Feedback_Log.

## 2. Analyze the Feedback Loop

The `Feedback_Log` tab contains critical learnings (e.g., "Reddit prefers comment-first strategy over direct posts" or "AEO research shows AI engines cite high-density tables").

For each new or unprocessed entry in the Feedback Log:
1. Identify which workstream and agent it affects.
2. Determine the specific change in behavior required.
3. Formulate an updated instruction set for that agent.

## 3. Update Agent Instructions

Before handing off tasks to other agents, ensure their operating instructions reflect the latest feedback.

- If the feedback affects a skill file (e.g., `.claude/skills/reddit-outreach/SKILL.md`), propose an edit to that file.
- If the feedback is contextual, include it explicitly in the prompt you pass to the agent.

*Example: If the Feedback Log says "Career guides for mid-career professionals are seeing higher GSC impressions," instruct the `aeo-content-writer` to prioritize mid-career personas in the next batch of guides.*

## 4. Prioritize Workstreams

Review the `Dashboard` tab to determine the next action.

**Workstreams & Agents:**
- **AEO Content Factory** (`aeo-content-writer`): Creates career guides and blog posts based on BLS data.
- **Interactive Tool Lab** (`tool-architect`): Builds interactive features like the AI-Proof Score logic.
- **Partnership & PR** (`growth-outreach`): Handles Reddit and LinkedIn distribution.
- **Data & Insights** (`data-analyst`): Pulls GSC/GA4 data to measure KPIs.
- **AEO Distribution** (`aeo-distribution`): Post-publication workflow — invoke after `publish-checklist` passes. Handles Search Console submission, Reddit comment opportunities, LinkedIn launch draft, backlink outreach list, and 2-week citation tracking.

**Prioritization Logic:**
1. **Unblock Critical Path**: Are any "High" priority tasks blocking other workstreams? (e.g., Data Insights needed before AEO Content can be measured).
2. **Highest Impact**: Which "Active" status task has the highest potential impact on the core KPIs (Organic Impressions, Referral Traffic, etc.)?
3. **Feedback-Driven**: Did a recent feedback log entry highlight an immediate opportunity?

## 5. Orchestrate Execution

Once the priority is determined, formulate a clear, actionable prompt for the target agent.

Your output should be a structured handoff:

### Growth PM Handoff Report

**1. Current Priority:** [State the chosen task and why it was selected based on the tracker]
**2. Feedback Applied:** [List any learnings from the Feedback Log that apply to this task]
**3. Agent Handoff:** [Provide the exact prompt/instructions to be passed to the target agent, e.g., `aeo-content-writer`]

*Do not execute the downstream task yourself. Your job is to analyze, prioritize, and provide the optimized instructions for the specialized agent to execute.*
