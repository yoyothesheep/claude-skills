# Claude Skills

- This project contains Claude skills that I've tested, iterated on, and found valuable. I'll aim to keep them updated.
- To use, download the individual SKILL.md files, then upload to your environment (eg Claude Web -> Settings -> Capabilities -> Skills -> Add (upload), then call it in a chat!)
- If using Claude Web, make sure you turn on "Network Egress" in settings, then add *.yourdomain.com to the allow list. This allows the Claude agent to check the Schema markup, and not just HTML

---

Note: Use 1. `seo-competitor-keywords` and 2. `seo-site-audit` and the scans included in a free Ahrefs account to create a complete beginner-level, baseline SEO/AEO audit and strategy. 

### Recommended Workflow

```
0. Scan your site with a free Ahrefs account → scans ALL your pages for technical SEO 
1. seo-competitor-keywords  →  Find what keywords to target
2. Create content
3. seo-site-audit           →  Looks at specific pages for technical SEO, content SEO, and AEO
4. Publish → measure → repeat
```

---

## 1. `seo-competitor-keywords` — Competitor Analysis & Keyword Research

**File:** `seo-competitor-keywords/SKILL.md`

### Goal
Analyzes 2–5 competitor websites to reverse-engineer their content strategy, identifies keyword and content gaps, and produces a prioritized list of target keywords with traffic potential estimates.

### Input
- Competitor websites URLs 
- \[Optional\] Connect your Ahrefs account through their MCP server, and be on at least a Lite plan. 

### What it analyzes
- **Competitor content strategy** — topic coverage, content types, depth, structure
- **Content gaps** — topics competitors rank for that you don't (and vice versa)
- **Keyword opportunities** — grouped into three tiers by effort and payoff

### Ahrefs integration
When the **Ahrefs MCP server** is connected, the skill uses real data instead of estimates:

| Metric | Without Ahrefs | With Ahrefs |
|---|---|---|
| Search volume | High / Medium / Low | Exact monthly figure |
| Keyword difficulty | SERP-based proxy | Ahrefs KD score (0–100) |
| Traffic potential | CTR × estimated volume | Clicks data + SERP feature adjustments |
| Competitor traffic | Observable signals | Exact monthly visits |

### Output
A strategy document containing a competitor summary, keyword tiers (Quick Wins / Strategic / Long-term), a traffic opportunity summary with ROI projection, a content gap analysis, and a 90-day content calendar.

### When to use it
- Entering a new market or niche
- Planning a content strategy from scratch
- Identifying quick-win keyword opportunities
- Understanding how much traffic competitors are capturing

---


## 2. `seo-site-audit` — Site Audit & AEO Analysis


**File:** `seo-site-audit/SKILL.md`

### Goal
Crawls a target website and produces a prioritized audit covering technical SEO, content quality, and Answer Engine Optimization (AEO) — the emerging practice of optimizing for AI-generated search results (ChatGPT, Perplexity, Google AI Overviews).

### Input
- A list of your site's URLs, or provide base URL(s) and ask the agent to crawl a small sample of the linked pages. 
*Be mindful of your account level's context window, and don't crawl your entire site!*

### What it analyzes
- **Technical SEO** — title tags, meta descriptions, heading structure, internal linking, schema markup, image alt text
- **Content quality** — depth, freshness, E-E-A-T signals, readability
- **AEO** — FAQ/HowTo schema, author credentials, direct-answer formatting, citability signals

### Output
A structured report with a scored summary (0–100), findings grouped by severity (🔴 High / 🟡 Medium / 🟢 Low), and a phased action plan with implementation examples.

### When to use it
- Before launching or relaunching a site
- To diagnose a traffic drop
- To audit a competitor's on-page optimization
- After publishing new content to validate SEO hygiene

---
