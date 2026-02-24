# claude-skills

SEO and AEO skills for Claude — a tested workflow for auditing and optimizing websites and web apps for both search engines and AI answer engines. 

Designed to complement Ahrefs/Semrush with:
- Content & intent understanding
- UX and IA recommendations
- Reddit language glossary (how real people phrase questions in your niche)
- Schema validation with content type


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
* seo-keyword-research      →  Find competitive keywords, content gaps, and IA recommendations for SEO
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
- Feature, UX, and IA recommendations (navigation structure, hub pages, internal linking, content silos, page load, mobile, CTAs, accessibility)
- Success metrics and KPIs

---

## 1. `aeo-topic-research` — AEO Topic Research & Opportunities

**File:** `aeo-topic-research/SKILL.md`

### Goal
Discovers what questions AI engines are answering in your niche, which domains and pages they're citing, and what content formats are winning citations — so you know exactly what topics to create for AEO visibility.

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
A prioritized content opportunity brief including: topic clusters ranked by citation potential, a Reddit language glossary with natural phrasing and community vocabulary per topic, competitor citation analysis, winning content formats and structures, content presentation recommendations (navigation, format, multimedia), and a prioritized content roadmap.

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
- **Information architecture** — navigation structure, topic cluster hub pages, internal linking, and content silos based on keyword clustering

### Ahrefs integration
When the **Ahrefs MCP server** is connected, you get real data:
- Exact search volumes and traffic figures
- Ahrefs keyword difficulty scores (0–100)
- Actual competitor organic traffic
- SERP feature data and adjustments

### Output
A competitive keyword strategy with keyword tiers (Quick Wins / Strategic / Long-term), traffic opportunity summary with ROI projections, content gap analysis, and information architecture recommendations (navigation changes, hub pages, internal linking strategy, content silos).

---

## 3. `aeo-seo-site-audit` — Site Audit & AEO Optimization

**File:** `aeo-seo-site-audit/SKILL.md`

### Goal
Analyzes your website pages for content quality, schema markup completeness, and AEO (Answer Engine Optimization) — with actionable recommendations for improving AI citation potential and search ranking for your existing pages. **Complements an Ahrefs Site Audit** by covering content depth and AI-readiness that Ahrefs cannot assess; relies on Ahrefs for technical SEO (title tags, meta descriptions, broken links, crawlability, etc.).

### Input
- 1 or more target URLs from your website
- [Optional] Ahrefs Site Audit project ID — automatically pulls technical audit findings to combine with content analysis
- [Optional] Business context and content goals (e.g. targeting AI search engines)

### What it analyzes
- **Schema markup** — validates JSON-LD completeness and accuracy (FAQPage, HowTo, Article, Organization, etc.), flags missing or mismatched schema
- **Content quality** — depth, directness, E-E-A-T signals, readability, topical coherence
- **AEO optimization** — direct-answer formatting, author credentials, source citations, freshness signals, content structure for AI extraction

### Output
A prioritized audit report with findings grouped by severity (🔴 Critical / 🟡 Important / 🟢 Enhancement), specific schema fixes with effort estimates, content recommendations, and a page-by-page breakdown. If an Ahrefs project ID is provided, the report integrates Ahrefs technical findings alongside the content/AEO analysis.

---
