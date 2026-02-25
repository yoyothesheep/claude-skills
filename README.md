# claude-skills

SEO and AEO skills for Claude — a tested workflow for auditing and optimizing websites and web apps for both search engines and AI answer engines.

Designed to complement Ahrefs/Semrush by:
- Understanding your site's content, intent, and target audience
- Recommending UX and IA changes
- Reporting on how real people phrase questions in your niche (Reddit language glossary)
- Validating schema against your pages' content type

## Multi-agent architecture

Each skill uses a **Coordinator → Haiku → Sonnet** pipeline to balance speed, cost, and quality:

- **Coordinator** (main Claude): gathers input, orchestrates agents
- **Haiku agents**: parallel mechanical extraction — API calls, page crawls, data collection
- **Sonnet agent**: analysis, synthesis, and report writing

Every report includes a **Token Usage Summary** with per-agent input/output tokens and estimated cost. The orchestrator aggregates token costs across all three skills into a single grand total.

---

## Table of Contents

- [Setup](#setup)
- [Quick Start](#quick-start)
- [0. aeo-seo-strategy-orchestrator](#0-aeo-seo-strategy-orchestrator--complete-seaaeo-strategy--roadmap-orchestrator) 
- [1. aeo-topic-research](#1-aeo-topic-research--aeo-topic-research--opportunities) 
- [2. seo-keyword-research](#2-seo-keyword-research--competitor-analysis--keyword-research)
- [3. aeo-seo-site-audit](#3-aeo-seo-site-audit--site-audit--aeo-optimization)

---

## Setup

### 1. Recommend using Claude Code

The `aeo-seo-site-audit` skill uses `curl` to analyze schema markup, but Claude Web doesn't have permission to run `curl`, so you'll be prompted to check schema manually using [Google's Rich Results Test](https://search.google.com/test/rich-results)

### 2. Connect Ahrefs MCP (optional)

- A paid Ahrefs account gives you access to real keyword data such as search volumes, difficulty scores, and competitor traffic, and AI engine visibility.
- Otherwise, skills use web-scraped estimates instead of actual data.

---

## Quick Start

### Want Everything in One Report?
Use **`aeo-seo-strategy-orchestrator`** for a unified audit that runs all three core skills in parallel and synthesizes recommendations into one list.

Or, run each skill separately. 
```
* aeo-topic-research      →  Recommends topics, content format, and UX changes for AEO
* seo-keyword-research    →  Find competitive keywords, content gaps, and IA recommendations for SEO
* aeo-seo-site-audit      →  Audit & optimize your pages for SEO and AEO
```

---

## 0. `aeo-seo-strategy-orchestrator` — Complete SEO/AEO Strategy & Roadmap (Orchestrator)

**File:** `aeo-seo-strategy-orchestrator/SKILL.md`

### Goal
An all-in-one strategy. This orchestrates all three core skills (`aeo-topic-research`, `seo-keyword-research`, `aeo-seo-site-audit`) in parallel, then a Sonnet synthesis agent unifies all findings into a single ranked strategy.

### Agent Architecture
- **Coordinator**: gathers input, launches three sub-skill agents simultaneously
- **Sub-skill agents** (parallel): each runs its own full Haiku + Sonnet pipeline
- **Sonnet Synthesis Agent**: merges all three reports, deduplicates, ranks recommendations, aggregates token costs

### Input
- Your domain (i.e. your homepage URL)
- [Optional] 2–5 competitor URLs
- [Optional] Target website URLs to audit (5–10 core pages)
- [Optional] Ahrefs account for real keyword data
- [Optional] Market/niche and business goals
- [Optional] Current site pain points or goals

### What it synthesizes
- **Topic research** — what AI engines are answering, what's being cited
- **Competitive analysis** — keyword gaps, ranking opportunities, quick wins
- **Site audit** — technical SEO, content quality, current AEO level
- **Functionality analysis** — site architecture, feature gaps, UX friction points
- **Unified strategy** — integrated list of prioritized recommendations

### Output
A strategic report with:
- Strategic overview and key insights
- Aggregated Token Usage Summary with grand total cost across all agents
- Unified prioritized recommendations (merged from all three skills): **all** 🔴 Critical and 🟡 Important issues are always included; top 2 🟢 Enhancements per skill are shown, with a note if more were omitted
- Detailed findings grouped by category (AEO research, keywords, on-page, functionality)
- Success metrics and KPIs

---

## 1. `aeo-topic-research` — AEO Topic Research & Opportunities

**File:** `aeo-topic-research/SKILL.md`

### Goal
Discovers what questions AI engines are answering in your niche, which domains and pages they're citing, and what content formats are winning citations — so you know exactly what topics to create for AEO visibility.

### Agent Architecture
- **Coordinator**: gathers input, orchestrates two waves of Haiku agents
- **Haiku Brand Radar Agents** (parallel, one per AI engine): Steps 3–5 — Brand Radar API calls for AI questions, cited domains, cited pages
- **Haiku Reddit Agent**: Step 6 — web searches + thread fetches per topic cluster
- **Haiku Page Crawl Agents** (parallel, one per URL): Step 7 — extract content format and structure signals; sampling ensures **at least 2 pages per content format type** (guide, listicle, comparison, FAQ/definition, HowTo, stat roundup) for reliable pattern detection
- **Sonnet Agent**: Steps 8–11 — synthesize patterns, score opportunities, generate report

### Input
- Your brand name and website URL
- Your market/niche (e.g. "email marketing software")
- [Optional] 2–5 competitor brand names to compare against
- [Optional] Which AI engines to prioritize (ChatGPT, Perplexity, Google AI Overviews, Gemini)
- [Optional] Ahrefs account for real Brand Radar citation data

### What it discovers
- **AI-answered questions** — what are people asking that AI search engines are answering?
- **Reddit language** — how real people phrase questions and describe problems in your niche, surfacing vocabulary and unmet needs that formal research misses
- **Cited domains & pages** — who is AI citing most often, and which specific pages win citations?
- **Content patterns** — what topics, formats, and structures get cited by AI engines?
- **Content gaps** — opportunities where you can create content that AI engines will cite
- **Content presentation & UX** — navigation aids (TOC, jump links, sticky nav), multimedia gaps, and formatting patterns from citation-winning pages

### Output
A prioritized content opportunity brief including: topic clusters ranked by citation potential, a Reddit language glossary with natural phrasing and community vocabulary per topic, competitor citation analysis, winning content formats and structures, content presentation recommendations (navigation, format, multimedia), a prioritized content roadmap, and a Token Usage Summary.

---

## 2. `seo-keyword-research` — Competitor Analysis & Keyword Research

**File:** `seo-keyword-research/SKILL.md`

### Goal
Analyzes competitor websites to reverse-engineer their SEO strategies, identifies content gaps and keyword opportunities, and produces a prioritized list of target keywords with ranking and traffic potential.

### Agent Architecture
- **Coordinator**: gathers input, orchestrates two waves of Haiku agents
- **Haiku Competitor Agents** (parallel, one per competitor): Steps 3–4 — Ahrefs metrics + top keywords (Step 3), crawl key pages (Step 4); each competitor gets **exactly 2 pages per type** (homepage, blog/resource, category/topic hub, product/service detail) for consistent cross-run comparisons
- **Haiku Keyword Research Agent**: Step 5 — Ahrefs keyword explorer calls using seeds from competitor data
- **Sonnet Agent**: Steps 6–11 — content analysis, gap analysis, ranking evaluation, prioritization, IA recommendations, report

### Input
- Your domain (i.e. your homepage URL)
- [Optional] 2–5 competitor domains
- [Optional] Connect your Ahrefs account for real data

### What it analyzes
- **Competitor content strategy** — what topics do they cover, and how?
- **Content gaps** — keywords they rank for that you don't (and vice versa)
- **Keyword opportunities** — ranked by ranking potential, search volume, and competitive difficulty
- **Traffic analysis** — estimated traffic potential and ROI for target keywords
- **Information architecture** — navigation structure, topic cluster hub pages, internal linking, and content silos based on keyword clustering

### Ahrefs integration
When the **Ahrefs MCP server** is connected, you get real data:
- Exact search volumes and traffic figures
- Ahrefs keyword difficulty scores (0–100)
- Actual competitor organic traffic
- SERP feature data and adjustments

### Output
A competitive keyword strategy with keyword tiers (Quick Wins / Strategic / Long-term), traffic opportunity summary with ROI projections, content gap analysis, information architecture recommendations (navigation changes, hub pages, internal linking strategy, content silos), and a Token Usage Summary.

---

## 3. `aeo-seo-site-audit` — Site Audit & AEO Optimization

**File:** `aeo-seo-site-audit/SKILL.md`

### Goal
Analyzes your website pages for content quality, schema markup completeness, and AEO (Answer Engine Optimization) — with actionable recommendations for improving AI citation potential and search ranking for your existing pages. **Complements an Ahrefs Site Audit** by covering content depth and AI-readiness that Ahrefs cannot assess; relies on Ahrefs for technical SEO (title tags, meta descriptions, broken links, crawlability, etc.).

### Agent Architecture
- **Coordinator**: gathers input, launches one Haiku agent per URL (+ one Ahrefs agent if project ID provided) in parallel
- **Haiku URL Agents** (parallel, one per URL): fetch raw HTML, extract JSON-LD schema, extract content and authority signals; after user-specified URLs, **required representative sampling** adds 1–2 pages per type not yet covered (static content, dynamic/app route, category/listing, utility) to prevent missing CSR rendering gaps
- **Haiku Ahrefs Agent** (if project ID provided): pulls technical audit findings from Ahrefs API
- **Sonnet Agent**: schema validation, content analysis, gap prioritization, report writing

### Input
- 1 or more target URLs from your website
- [Optional] Ahrefs Site Audit project ID — automatically pulls technical audit findings to combine with content analysis
- [Optional] Business context and content goals (e.g. targeting AI search engines)

### What it analyzes
- **Schema markup** — validates JSON-LD completeness and accuracy (FAQPage, HowTo, Article, Organization, etc.), flags missing or mismatched schema
- **Content quality** — depth, directness, E-E-A-T signals, readability, topical coherence
- **AEO optimization** — direct-answer formatting, author credentials, source citations, freshness signals, content structure for AI extraction

### Output
A prioritized audit report with findings grouped by severity (🔴 Critical / 🟡 Important / 🟢 Enhancement), specific schema fixes with effort estimates, content recommendations, a page-by-page breakdown, and a Token Usage Summary. If an Ahrefs project ID is provided, the report integrates Ahrefs technical findings alongside the content/AEO analysis.

---
