# claude-skills

SEO and AEO skills for Claude — a tested workflow for auditing and optimizing websites and web apps for both search engines and AI answer engines.

## Table of Contents

- [Setup](#setup)
- [Quick Start](#quick-start)
- [0. aeo-seo-strategy](#0-aeo-seo-strategy--complete-seoaeo-strategy--roadmap-orchestrator)
- [1. core-aeo-topic-research](#1-core-aeo-topic-research--aeo-topic-research--opportunities)
- [2. core-seo-keyword-research](#2-core-seo-keyword-research--competitor-analysis--keyword-research)
- [3. core-aeo-seo-site-audit](#3-core-aeo-seo-site-audit--site-audit--aeo-optimization)

---

## Setup

### 1. Load a skill

**Claude Code**

Add this repo to your project, then reference skills by name or file path in conversation:

```
Read core-aeo-seo-site-audit/SKILL.md and run the audit for example.com
```

**Claude Web**

Either: 
- Upload the `SKILL.md` to your chat, and it'll be available only for that chat.
- Go to Settings -> Capabilities -> Skills and upload the `SKILL.md` files so they're always available to all conversations.

---

### 2. Enable internet access

Skills use `web_fetch` and `web_search` to fetch and analyze web pages.

- **Claude Code:** Internet access is available by default
- **Claude Web:** Go to **Settings → Capabilities** and enable **"Allow network egress"**. Add the domain you're trying to audit to the Domain allowlist.

---

### 3. Connect Ahrefs MCP (optional)

- A paid Ahrefs account gives you access to real keyword data in `core-seo-keyword-research`. 
- A paid or free account gives you access to AI engine visibility in `aeo-seo-strategy`. 
- Without either, those skills use web-scraped estimates instead of actual search volumes, difficulty scores, and competitor traffic.

Connect and authenticate via the Ahrefs MCP server in your Claude Code or Web settings.

---

### 4. Grant tool access to subagents (Claude Code only)

When Claude Code runs skills as background agents (e.g., using the Task tool to parallelize research), subagents cannot prompt you interactively for tool approval. Tools not in your `permissions.allow` list will be auto-denied, causing the agent to fail silently.

To grant subagents automatic access to the tools these skills need, add the following to `~/.claude/settings.json`:

```json
{
  "permissions": {
    "allow": [
      "WebFetch",
      "WebSearch",
      "Bash",
      "Write",
      "Read",
      "Edit",
      "Glob",
      "Grep",
      "mcp__claude_ai_AHREFs__*"
    ]
  }
}
```

Without this, subagents running `core-aeo-topic-research`, `core-seo-keyword-research`, or `core-aeo-seo-site-audit` will be unable to fetch pages, run shell commands, write output files, or call Ahrefs tools.

---

### Claude Web Limitations

Claude Web can run these skills, but with reduced capability when running `core-aeo-seo-site-audit`, as compared to Claude Code:

| Feature | Claude Code | Claude Web |
|---|---|---|
| Fetch page content | ✅ Full | ✅ Full (requires network egress enabled) |
| Extract JSON-LD schema | ✅ Full (via `curl`) | ❌ Not available — `WebFetch` strips script tags |

**Schema markup** is the most significant gap. `WebFetch` converts HTML to markdown, which strips `<script type="application/ld+json">` blocks entirely. When running the site audit on Claude Web:
- The skill will note which pages could not have schema inspected
- You'll be prompted to check schema manually using [Google's Rich Results Test](https://search.google.com/test/rich-results)
- For full schema coverage, run the audit in Claude Code

---

## Quick Start

### Want Everything in One Report?
Use **`aeo-seo-strategy`** for a unified audit that runs all three core skills, then synthesizes recommendations into one list.

Or, run each core skill separately. 
```
* core-aeo-topic-research           →  Discover what topics to target for AEO
* core-seo-keyword-research      →  Find competitive keywords and content gaps
* core-aeo-seo-site-audit           →  Audit & optimize your pages for SEO and AEO
```

---

## 0. `aeo-seo-strategy` — Complete SEO/AEO Strategy & Roadmap (Orchestrator)

**File:** `aeo-seo-strategy/SKILL.md`

### Goal
An all-in-one strategy. This orchestrates all three core skills (`core-aeo-topic-research`, `core-seo-keyword-research`, `core-aeo-seo-site-audit`), then synthesizes recommendations.

### Input
- Your domain (i.e. your homepage URL)
- [Optional] 2–5 competitor URLs
- [Optional] Target website URLs to audit (5–10 core pages)
- [Optional] Ahrefs account for real keyword data
- [Optional] Market/niche and business goals
- [Optional] Current site pain points or goals

### Output
A strategic report with:
- Strategic overview and key insights
- Detailed findings grouped by category (research, keywords, on-page, functionality)
- Feature and product recommendations with business case
- Success metrics and KPIs

---

## 1. `core-aeo-topic-research` — AEO Topic Research & Opportunities

**File:** `core-aeo-topic-research/SKILL.md`

### Goal
Discovers what questions AI engines are answering in your niche, which domains and pages they're citing, and what content formats are winning citations — so you know exactly what topics to create for AEO visibility.

### Input
- Your domain (i.e. your homepage URL)
- [Optional] 2–5 competitor domains  
- [Optional] Target market or niche
- [Optional] Which AI engines to prioritize (ChatGPT, Perplexity, Google AI Overviews, Gemini)

### What it discovers
- **AI-answered questions** — what are people asking that AI search engines are answering?
- **Cited domains & pages** — who is AI citing most often, and which specific pages win citations?
- **Content patterns** — what topics, formats, and structures get cited by AI engines?
- **Content gaps** — opportunities where you can create content that AI engines will cite

### Output
A prioritized content opportunity brief with topics ranked by citation potential, competitor analysis showing what they're getting cited for, recommended content formats and structures, and a recommended content roadmap.

---

## 2. `core-seo-keyword-research` — Competitor Analysis & Keyword Research

**File:** `core-seo-keyword-research/SKILL.md`

### Goal
Analyzes competitor websites to reverse-engineer their SEO strategies, identifies content gaps and keyword opportunities, and produces a prioritized list of target keywords with ranking and traffic potential.

### Input
- Your domain (i.e. your homepage URL)
- [Optional] 2–5 competitor domains  
- [Optional] Connect your Ahrefs account for real data

### What it analyzes
- **Competitor content strategy** — what topics do they cover, and how?
- **Content gaps** — keywords they rank for that you don't (and vice versa)
- **Keyword opportunities** — ranked by ranking potential, search volume, and competitive difficulty
- **Traffic analysis** — estimated traffic potential and ROI for target keywords

### Ahrefs integration
When the **Ahrefs MCP server** is connected, you get real data:
- Exact search volumes and traffic figures
- Ahrefs keyword difficulty scores (0–100)  
- Actual competitor organic traffic
- SERP feature data and adjustments

### Output
A competitive keyword strategy with keyword tiers (Quick Wins / Strategic / Long-term), traffic opportunity summary with ROI projections, and a content gap analysis.

---

## 3. `core-aeo-seo-site-audit` — Site Audit & AEO Optimization

**File:** `core-aeo-seo-site-audit/SKILL.md`

### Goal
Crawls your website pages and produces a prioritized audit covering technical SEO, content quality, and AEO (Answer Engine Optimization) — with actionable recommendations for improving both search ranking and AI citation potential for your **existing pages**.

### Input
- 1 or more target URLs from your website
- [Optional] Specify how many internal linked pages to analyze
- [Optional] Your target keywords or topics

### What it analyzes
- **Technical SEO** — title tags, meta descriptions, heading structure, internal linking, schema markup, image alt text, page speed signals
- **Content quality** — depth, freshness, E-E-A-T signals, readability, topical relevance
- **AEO optimization** — FAQ/HowTo schema, direct-answer formatting, author credentials, citability signals, content structure for AI extraction

### Output
A scored audit report (0–100) with findings grouped by severity (🔴 High / 🟡 Medium / 🟢 Low), implementation examples, and a phased action plan.

---

