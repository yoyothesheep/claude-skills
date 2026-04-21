---
name: growth-pm
description: Central coordinator for the content pipeline. Maintains a prioritized task board across 4 workstreams, routes work to the right skill, tracks citation performance, and learns from GSC data and human feedback to improve future routing and flag skill updates.
---

# Growth PM — The Brain

Central coordinator for the content pipeline. Reads the tracker, analyzes performance data, maintains a prioritized task board across 4 workstreams, and routes work to the right downstream skill with an optimized prompt.

## When to Use This Skill

- "What should we work on next?"
- "Run the daily growth routine"
- "Check the tracker and prioritize"
- "What's performing well?"
- "Check citations for [post slug]"

---

## Core Workflow

Step 1. **Read tracker** — Dashboard, Feedback Log, and workstream tabs
Step 2. **Pull performance data** — GSC MCP + any human input
Step 3. **Run learning loop** — surface what's working, flag skill updates
Step 4. **Prioritize across 4 workstreams** — produce ranked task board
Step 5. **Orchestrate** — route to downstream skill with optimized prompt

---

## Step 1: Read the Tracker

Paths defined in `CONFIG.md`:

- `TRACKER_DASHBOARD` — status, priority, next milestone for all workstreams
- `TRACKER_FEEDBACK_LOG` — insights, ratings, action items from recent experiments
- `TRACKER_CONTENT` — content pipeline (drafts, scheduled, published)
- `CITATION_PATH` — citation tracking baseline files per post slug

Always begin by reading Dashboard and Feedback Log.

---

## Step 2: Pull Performance Data

### GSC Data (if Ahrefs MCP connected)

For each recently published post (last 30 days), pull:

```python
# Clicks, impressions, position for each URL
gsc_page_history(
    url=post_url,
    date_from="30 days ago",
    date_to="today"
)

# Top queries driving traffic to each page
gsc_keywords(
    url=post_url,
    date_from="30 days ago"
)
```

Extract: which posts are gaining clicks, which queries are driving them, which posts have high impressions but low CTR (title/description opportunity).

### Citation Checks

For posts with a baseline in `CITATION_PATH`, check if Day 7 or Day 14 follow-ups are due:
- Read `[slug]-baseline.md` to find the check dates
- If a check is due, run the queries in ChatGPT, Perplexity, Google AI Overviews, Gemini and record results
- Append findings to `TRACKER_DASHBOARD` under the post entry

### Human Input

If the user provides feedback, experiment results, or performance notes — read them and incorporate into the learning loop below.

---

## Step 3: Learning Loop

Synthesize performance data + feedback to extract durable signals:

### What to surface
- **Content format wins**: Which formats (data guide, comparison, FAQ-heavy) are getting citations or clicks?
- **Topic resonance**: Which topic clusters are driving the most engagement or citations?
- **Distribution effectiveness**: Which channels (Reddit, LinkedIn, outreach) drove measurable referrals?
- **Skill gaps**: Is any skill producing output that consistently underperforms? (e.g., Reddit drafts that never get posted, LinkedIn posts that need heavy editing)

### Skill update flags

If a pattern suggests a skill's prompt or CONFIG.md needs updating, output a specific flag:

```
⚠️ SKILL UPDATE SUGGESTED: [skill-name]
Reason: [specific pattern observed]
Suggested change: [concrete edit to SKILL.md or CONFIG.md]
```

Examples:
- "Reddit drafts are always for 48h-old threads — subreddit list in CONFIG.md may be too narrow"
- "aeo-content-writer posts consistently lack FAQ pairs — prompt needs stronger FAQ emphasis"

---

## Step 4: Prioritize Across 4 Workstreams

Always produce a ranked task board with recommended next action per workstream.

### The 4 Workstreams

**1. Research & Audit**
Skills: `aeo-topic-research`, `seo-keyword-research`, `aeo-seo-site-audit`, `aeo-seo-strategy-orchestrator`
Trigger when: no fresh research in 30+ days, new competitor activity, traffic drop, or strategy reset.

**2. Content Creation**
Skills: `aeo-content-writer`
Trigger when: research has identified high-priority topics not yet covered, content pipeline is empty.

**3. Content Publication**
Skills: `publish-checklist`
Trigger when: a draft is ready to ship.

**4. Distribution**
Skills: `distribute-social`, `distribute-outreach`
Trigger when: a post was published and not yet distributed. Distribution should happen within 48h of publish.

### Prioritization Logic

1. **Unblock the critical path** — any task blocking another workstream goes first
2. **Citation follow-ups due** — Day 7 or Day 14 checks that are overdue
3. **Distribution lag** — published posts not yet distributed
4. **Highest-impact content gap** — from research findings
5. **Feedback-driven** — if learning loop flagged a skill update, surface it

### Task Board Output Format

```
## Growth PM Task Board — [Date]

### 🔴 Do Now
1. [Task] — [Workstream] — [Why: one sentence]

### 🟡 This Week
2. [Task] — [Workstream]
3. [Task] — [Workstream]

### 🟢 Backlog
4. [Task] — [Workstream]

### ⚠️ Skill Update Flags
- [skill-name]: [suggested change]

### Performance Signals
- [1–3 bullet points: what's working, what's not]
```

---

## Step 5: Orchestrate

Once priority is determined, produce the handoff for the target skill:

```
## Handoff — [Skill Name]

**Why this task:** [one sentence from tracker/learning loop]
**Feedback applied:** [any learnings that should shape this run]
**Prompt:**
[Exact prompt to pass to the target skill]
```

Do not execute the downstream task. Route and hand off only.

---

## Citation Tracking

When a new post is published, set up citation tracking:

### Day 0 — Baseline (do immediately after publish)

Run these queries across ChatGPT, Perplexity, Google AI Overviews, Gemini:
- Post's primary FAQ question
- Post's secondary FAQ question
- Key claim rephrased as a question

Record results in `{CITATION_PATH}[slug]-baseline.md`:

```markdown
# Citation Baseline — [slug] — [date]

## Queries
| Query | ChatGPT | Perplexity | Google AIO | Gemini |
|-------|---------|------------|------------|--------|
| [q1]  | ❌/✅   | ❌/✅      | ❌/✅      | ❌/✅  |
| [q2]  | ❌/✅   | ❌/✅      | ❌/✅      | ❌/✅  |

## Scheduled checks
- Day 7: [date]
- Day 14: [date]
```

### Day 7 and Day 14 — Follow-up

Re-run same queries. Log delta. If cited: note which engine, which query, and what likely drove it (FAQ schema, Reddit thread, outreach link).

### Unlinked Mention Monitor

```
web_search: "[key claim exact phrase]" -site:[your-site]
```

For each unlinked mention: draft a 2-sentence attribution request. Save to outreach contacts.
