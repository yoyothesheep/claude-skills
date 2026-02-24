# claude-skills

SEO and AEO skills for Claude — a tested workflow for auditing and optimizing websites and web apps for both search engines and AI answer engines. Designed to complement Ahrefs/Semrush by automatically understanding your site's content and intent, then automatically generating content and UX strategy.

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

The `aeo-seo-site-audit skill uses `curl` to analyze schema markup, but Claude Web doesn't have permission to run `curl`, so you'll be prompted to check schema manually using [Google's Rich Results Test](https://search.google.com/test/rich-results)

### 2. Connect Ahrefs MCP (optional)

- A paid Ahrefs account gives you access to real keyword data such as search volumes, difficulty scores, and competitor traffic, and AI engine visibility.
- Otherwise, skills use web-scraped estimates instead of actual data.

---

## Quick Start

### Want Everything in One Report?
Use **`aeo-seo-strategy-orchestrator`** for a unified audit that runs all three core skills, and synthesizes recommendations into one list.

Or, run each core skill separately. 
```
* aeo-topic-research           →  Recommends topics, content format, and UX changes for AEO
* seo-keyword-research      →  Find competitive keywords and content gaps for SEO
* aeo-seo-site-audit           →  Audit & optimize your pages for SEO and AEO
```

---

## 0. `aeo-seo-strategy-orchestrator` — Complete SEO/AEO Strategy & Roadmap (Orchestrator)

**File:** `aeo-seo-strategy-orchestrator/SKILL.md`

### Goal
An all-in-one strategy. This orchestrates all three core skills (`aeo-topic-research`, `seo-keyword-research`, `aeo-seo-site-audit`), then synthesizes all recommendations.

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
- Detailed findings grouped by category (research, keywords, on-page, functionality)
- Feature and product recommendations with business case
- Success metrics and KPIs

---

## 1. `aeo-topic-research` — AEO Topic Research & Opportunities

**File:** `aeo-topic-research/SKILL.md`

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

## 2. `seo-keyword-research` — Competitor Analysis & Keyword Research

**File:** `seo-keyword-research/SKILL.md`

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

## 3. `aeo-seo-site-audit` — Site Audit & AEO Optimization

**File:** `aeo-seo-site-audit/SKILL.md`

### Goal
Crawls your website pages and produces a prioritized audit covering technical SEO, content quality, and AEO (Answer Engine Optimization) — with actionable recommendations for improving both search ranking and AI citation potential for your existing pages. **Complements an Ahrefs audit**, not meant to replace it.

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
