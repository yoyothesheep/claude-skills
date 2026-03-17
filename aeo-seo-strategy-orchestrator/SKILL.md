---
name: aeo-seo-strategy-orchestrator
description: Run a complete SEO/AEO strategy audit by orchestrating all three core skills, and synthesizing findings into one unified set of recommendations.
---

# Full SEO/AEO Strategy Skill

This skill is the all-in-one SEO/AEO and product strategy audit. It orchestrates the three core skills (`aeo-topic-research`, `seo-keyword-research`, and `aeo-seo-site-audit`), each of which runs its own internal multi-agent pipeline, then synthesizes all findings into a unified ranked strategy.

## When to Use This Skill

Trigger this skill when the user:
- Asks for a "complete SEO/AEO strategy"
- Wants a "full audit with recommendations"
- Needs a "comprehensive SEO strategy" that covers everything
- Requests "SEO strategy including site improvements"
- Asks for "SEO + product/UX recommendations in one strategy"
- Says "audit my site and competitors, then tell me what to do"

**This is the right skill to use when the user wants everything in one go** — research, competitive analysis, site audit, *plus* site functionality/UX improvements.

## Core Workflow

Step 1. **[Coordinator]** Gather Input — domain, competitors, target URLs, niche, goals
Step 2. **[Coordinator]** Launch all three sub-skill agents in parallel
Step 3. **[Sub-skill Agents, parallel]** `aeo-topic-research` + `seo-keyword-research` + `aeo-seo-site-audit` — each runs its full internal pipeline
Step 4. **[Sonnet Synthesis Agent]** Receive all three skill reports, synthesize into one unified strategy with aggregated token usage

---

## Agent Architecture

### Coordinator (main Claude)
Handles Steps 1–2: gathers user input and launches all three sub-skill agents simultaneously. Collects their complete report payloads and passes them to the Sonnet Synthesis Agent.

### Sub-skill Agents (parallel, Step 3)
Three agents launched in parallel — one per skill. Each runs the full workflow of its skill, including its own internal Haiku data-extraction agents and Sonnet synthesis agent. Each produces a complete report with findings and a Token Usage Summary.

| Agent | Skill | What it produces |
|-------|-------|-----------------|
| Topic Research Agent | `aeo-topic-research` | AI question landscape, Reddit glossary, citation analysis, content opportunities, Token Usage Summary |
| Keyword Research Agent | `seo-keyword-research` | Competitor analysis, keyword tiers, traffic opportunity, IA recommendations, Token Usage Summary |
| Site Audit Agent | `aeo-seo-site-audit` | Schema gaps, content quality issues, AEO readiness, page-by-page findings, Token Usage Summary |

### Sonnet Synthesis Agent
Receives all three complete skill reports. Extracts key findings and Token Usage Summaries from each, synthesizes a unified strategy, and produces the final report with an aggregated cost table.

---

## Inputs

### Required
- **Your domain/brand** — the site you're optimizing

### Recommended
- **Ahrefs account** — for real keyword volume, difficulty, and traffic data

### Optional
- **Target URLs** — pages to audit (typically 5–10 core pages)
- **Competitor domains** — 2–5 competitors to analyze
- **Market/niche** — to scope the research accurately
- **Current pain points** — conversion issues, UX friction, known problems
- **Business goals** — revenue, traffic, brand authority targets
- **Target AI engines** — which to prioritize (ChatGPT, Perplexity, Google AI Overviews, Gemini)

---

## COORDINATOR

## Step 1: Gather Input

Ask the user for the inputs listed above. For each input, explain what it unlocks:
- Competitor domains → enables keyword gap analysis and citation benchmarking
- Target URLs → enables schema validation and content quality audit
- Ahrefs account → upgrades all volume/traffic figures from estimates to real data
- Market/niche → scopes Brand Radar AI question discovery accurately

If user is unsure which competitors to analyze, ask what keywords they want to rank for — you can work backwards from there.

---

## Step 2: Launch Sub-skill Agents

Launch all three agents simultaneously. Do not wait for one to complete before launching the others.

```
Task(
  subagent_type: "general-purpose",
  model: "sonnet",
  prompt: <full aeo-topic-research SKILL.md> + "\n\nUser inputs:\nBrand: {brand}\nWebsite: {website}\nMarket/niche: {niche}\nCompetitors: {competitors}\nAI engines: {ai_engines}\nCountry: {country}\nGoal emphasis: {goal_emphasis}"
)

Task(
  subagent_type: "general-purpose",
  model: "sonnet",
  prompt: <full seo-keyword-research SKILL.md> + "\n\nUser inputs:\nWebsite: {website}\nCompetitor URLs: {competitor_urls}\nNiche: {niche}\nTarget audience: {audience}\nGeographic focus: {geo}\nGoals: {goals}"
)

Task(
  subagent_type: "general-purpose",
  model: "sonnet",
  prompt: <full aeo-seo-site-audit SKILL.md> + "\n\nUser inputs:\nTarget URLs: {target_urls}\nAhrefs project ID: {ahrefs_project_id}\nBusiness context: {business_context}\nContent goals: {content_goals}"
)
```

Collect all three results. Each result is a complete report with a one-line total cost in the Executive Summary and a full Token Usage table in the appendix. Once all three have returned, proceed to the SONNET SYNTHESIS AGENT section.

---

## SONNET SYNTHESIS AGENT

Receives three complete skill reports. All analysis, de-duplication, cross-referencing, and report writing happens here.

**Token tracking:** At the end of your output, include your own token usage:
```json
{
  "sonnet_token_usage": {
    "model": "claude-sonnet-4-6",
    "input_tokens": 0,
    "output_tokens": 0
  }
}
```

## Step 3: Extract and Deduplicate Findings

From each skill report, extract:

**From `aeo-topic-research`:**
- Topic gap matrix (🔴/🟡/🟢 opportunities)
- Winning content formats and structural patterns
- Citation authority gaps per AI engine
- Content Presentation Recommendations
- Token Usage (total cost line from Executive Summary + full breakdown from appendix)

**From `seo-keyword-research`:**
- Keyword tiers (Quick Wins, Strategic, Long-term) with traffic/difficulty data
- Content gap analysis (topics missing vs. competitors)
- Traffic opportunity summary with ROI estimates
- Information Architecture Recommendations
- Token Usage Summary

**From `aeo-seo-site-audit`:**
- Schema gaps by priority (🔴 Critical / 🟡 Important / 🟢 Enhancement)
- Content quality issues with affected pages
- AEO readiness assessment
- Page-by-page breakdown
- Token Usage Summary

**Deduplication rules:**
- If a content gap appears in both topic research and keyword research, merge into one recommendation with both signals noted (e.g., "High AI citation demand + 2,400 searches/month")
- If a content issue appears in both keyword research and site audit, merge and note both dimensions (e.g., "Competitors cover this topic + your existing page lacks direct-answer structure")
- Keep the higher-priority classification when merging

---

## Step 4: Generate Unified Report

### Executive Summary
- Current state: Where the site stands across AEO, SEO, and content quality
- Top 3 opportunities (one from each dimension if possible), each with a colored priority badge: 🔴 for critical/immediate, 🟡 for important/near-term, 🟢 for enhancement
- Estimated total impact: traffic potential + AI citation uplift
- **Total research cost: $—** (one line; full breakdown in Token Usage appendix at end of report)

### Prioritized Recommendations

A single unified ranked list drawing from all three skills, following these inclusion rules:

**What to include:**
- **All** 🔴 Critical issues and 🟡 Important issues from every skill — no cap, no omissions
- **Top 2** 🟢 Enhancement items per skill (up to 6 enhancements total across three skills), selected by highest impact
- If a skill produced more than 2 enhancements, append a note after that skill's last enhancement item: `> _N additional enhancements from [Skill Name] not listed — see [Section Name] for full list._`

**Priority tier mapping across skills:**

| aeo-seo-site-audit | aeo-topic-research | seo-keyword-research | Include |
|---|---|---|---|
| 🔴 Critical | 🔴 Create Now | Tier 1: Quick Wins | All |
| 🟡 Important | 🟡 Plan Soon | Tier 2: Strategic | All |
| 🟢 Enhancement | 🟢 Monitor | Tier 3: Long-term | Top 2 per skill |

Order within each tier by impact × effort. Begin with a summary table — one row per recommendation — then list full details for each item below the table.

**Summary table (one row per recommendation):**

| # | Priority | Recommendation | Source | Category | Effort |
|---|----------|---------------|--------|----------|--------|
| 1 | 🔴 Critical | … | Site Audit / AEO Research / Keyword Research / Multiple | … | Quick / Moderate / Major |
| 2 | 🟡 Important | … | … | … | … |
| … | … | … | … | … | … |

**Detailed recommendations (one section per item, matching table order):**

For each item:

- **What to do**: Specific, actionable instruction
- **Why it matters**: Data-backed impact (e.g., "Affects 8 of 11 pages" / "2,400 searches/month, difficulty 22" / "Cited by ChatGPT in 45 responses")
- **Source**: Which skill flagged this (AEO Research / Keyword Research / Site Audit / Multiple)
- **Category**: Technical SEO / Content / AEO / Information Architecture / Content Presentation
- **Effort**: Quick (<30 min) / Moderate (1–3 hrs) / Major (4+ hrs)

### Detailed Findings by Category

#### AEO Topic Research Findings
- High-opportunity topics for AI citations (from topic research)
- Citation authority gaps by AI engine
- Recommended content formats and structural patterns
- Reddit language glossary (community vocabulary per topic cluster)

#### SEO/Keyword Strategy Findings
- Keyword tiers (Quick Wins / Strategic / Long-term) with traffic estimates
- Competitive positioning analysis
- Traffic opportunity summary with ROI
- Competitor content strengths and weaknesses

#### Site Audit Findings
- Technical SEO issues (severity-ranked, from Ahrefs if available)
- Schema gaps with specific fixes
- Content quality issues with affected pages
- Current AEO optimization level per page

#### Functionality & UX Recommendations

Synthesized from all three skills:

**Content Presentation** (from topic research):
- Navigation aids: TOC, jump links, sticky nav
- Format improvements: expandable FAQs, callout boxes, comparison tables
- Multimedia gaps and scannability patterns

**Information Architecture** (from keyword research):
- Navigation structure changes
- Hub page recommendations with keyword clusters
- Internal linking strategy
- Content silo recommendations

**Technical UX** (from site audit):
- Page load and mobile optimization
- Navigation UX improvements
- CTA placement and accessibility

### Token Usage

Aggregate token usage across all agents in all three skills plus this synthesis agent. Extract per-agent rows from each skill's Token Usage appendix, then add the orchestrator row:

**Pricing reference:**
- Haiku 4.5: $0.80 / 1M input tokens, $4.00 / 1M output tokens
- Sonnet 4.6: $3.00 / 1M input tokens, $15.00 / 1M output tokens

| Skill | Model | Agent | Input Tokens | Output Tokens | Est. Cost |
|-------|-------|-------|-------------|--------------|-----------|
| aeo-topic-research | claude-haiku-4-5 | Brand Radar: chatgpt | — | — | $— |
| aeo-topic-research | claude-haiku-4-5 | Brand Radar: perplexity | — | — | $— |
| aeo-topic-research | claude-haiku-4-5 | Brand Radar: google_ai_overviews | — | — | $— |
| aeo-topic-research | claude-haiku-4-5 | Brand Radar: gemini | — | — | $— |
| aeo-topic-research | claude-haiku-4-5 | Reddit agent | — | — | $— |
| aeo-topic-research | claude-haiku-4-5 | Page crawl × N | — | — | $— |
| aeo-topic-research | claude-sonnet-4-6 | Synthesis agent | — | — | $— |
| seo-keyword-research | claude-haiku-4-5 | Competitor: {url} × N | — | — | $— |
| seo-keyword-research | claude-haiku-4-5 | Keyword research | — | — | $— |
| seo-keyword-research | claude-sonnet-4-6 | Synthesis agent | — | — | $— |
| aeo-seo-site-audit | claude-haiku-4-5 | URL agent × N | — | — | $— |
| aeo-seo-site-audit | claude-haiku-4-5 | Ahrefs agent (if used) | — | — | $— |
| aeo-seo-site-audit | claude-sonnet-4-6 | Synthesis agent | — | — | $— |
| **orchestrator** | claude-sonnet-4-6 | Synthesis agent | — | — | $— |
| **Grand Total** | | | | | **$—** |

Est. Cost = `(input_tokens / 1,000,000 × input_rate) + (output_tokens / 1,000,000 × output_rate)`, rounded to 4 decimal places. Sum all rows for Grand Total.

---

## Output Format

Default: Markdown file saved to `/mnt/user-data/outputs/` and presented with `present_files`.

---

## User Communication

**Refer to [TONE-GUIDE.md](../TONE-GUIDE.md) for comprehensive tone and communication guidelines.**
