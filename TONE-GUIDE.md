---
title: Tone & Communication Guidelines
description: Guidelines for writing analytical, data-driven audit reports and communication
---

# Tone & Communication Guidelines

This guide establishes the communication style for all skill outputs and user-facing communication. The goal is **analytical and data-driven** communication that avoids promotional or hyperbolic language.

## Core Principle

**Analytical over Promotional:** All skill output should read as objective analysis backed by specific metrics, not as marketing or persuasion. The reader should be able to verify claims against the data presented.

---

## Executive Summary Tone

**What to do:**
- State facts without editorial judgment
- Lead with quantified metrics, not value judgments
- Order findings by measurable impact and effort
- Use conservative projections with explicit data sources

**Examples:**

❌ **POOR** (Promotional):
> "This site has great potential with some critical fixes"

✅ **GOOD** (Analytical):
> "Based on analysis of 12 pages, the site has a health score of 38/100. The top 3 issues affecting 100% of pages are missing H1 tags, client-side rendering, and undersized title tags."

❌ **POOR** (Vague):
> "altPath is a genuinely differentiated product that is almost completely invisible to search engines"

✅ **GOOD** (Specific):
> "The site exhibits significant technical limitations that reduce visibility to both search engines and AI systems. An estimated 99% of site content is invisible to crawlers due to client-side rendering."

---

## Detailed Findings Writing Style

**Key principles:**
1. State issues **factually** without editorial language
2. Explain the **mechanism** of impact, not opinion
3. Avoid subjective emphasis without quantified data
4. Use **metrics** to convey severity (affected % of pages, measured impact on scores)
5. Be **specific** about numbers and scopes

**Forbidden language:**
- Subjective descriptors: "major," "significant," "powerful," "devastating," "critical," "huge," "important"
- Exclamation points (these add emotional tone)
- Marketing language: "the good news is," "massive opportunity," "incredible opportunity"
- Unsubstantiated adjectives: "great," "excellent," "best," "worst"
- Emotional framing: "desperately needs," "will transform," "will revolutionize"

**Required language:**
- Specific metrics: "7 of 10 pages lack X" (not "most pages")
- Mechanism explanation: "H1 tags signal page topics to crawlers; their absence reduces topical relevance scoring by ~15-20%"
- Quantified impact: "Estimated impact: +15-20% improvement"
- Data sources: "Based on search volume data from [source]"
- Neutral phrasing: "is/was not found," "is missing," "lacks"

**Examples:**

| Poor | Good | Why |
|------|------|-----|
| "This is a critical asset" | "This baseline metric improves from 10 to 15 points, a 50% gain" | Measurable vs subjective |
| "The good news is the site has great content" | "The site has 520 words of crawlable content on the /about page" | Specific vs vague |
| "Significantly impacts visibility" | "Affects 7 of 10 pages (70%)" | Quantified vs relative |
| "Devastating limitation" | "Results in 99%+ content invisible to crawlers" | Fact-based vs emotional |
| "This will dramatically improve your organic traffic" | "Adding H1 tags improves topic relevance scoring by ~15%; based on current ranking position, this could increase click-through by 2-5% on 40 target keywords" | Measurable vs hyperbolic |
| "Major competitive advantage" | "Provides foundation; requires supporting content" | Balanced assessment |
| "Significantly reduces visibility" | "Affects 99%+ of site content" | Quantified scope |
| "Desperately needs" | "Missing (0 found); recommended for all pages" | Objective language |

---

## Prioritized Recommendations Writing Style

**What to do:**
- Use **neutral language** without dramatic framing
- **Quantify impact** with specific data
- **Avoid vague benefits** — be precise about the outcome
- Explain **how/why** the fix works (mechanism)
- Provide **realistic effort estimates** with hour ranges
- Include **confidence levels** where uncertain

**How to structure each recommendation:**

```
Issue Description
- What's missing/wrong (be specific about count and scope)

Why It Matters
- Explain mechanism: "X causes Y because Z"
- Use data/research to back the claim
- Example: "H1 tags signal page topic to crawlers. Missing H1s reduce topic relevance scoring by ~15-20%"

How to Fix
- Specific, step-by-step actions
- Be concrete (not "improve content" but "add 500 words to the about page")

Estimated Effort
- Quick: <30 minutes
- Moderate: 1-3 hours
- Major: >3 hours
- Always give a time range

Expected Outcome
- Quantified improvement with data source
- Example: "Adding H1 tags improves topic clarity for ~30% of long-tail queries"
```

**Examples:**

❌ **POOR** (Vague and dramatic):
> "CRITICAL -- unlocks the entire site for indexing and AI citation"

✅ **GOOD** (Specific and measurable):
> "2. Add H1 tags to all pages | Effort: 2-4 hours | Impact: +15-20% improvement in topic clarity | Mechanism: Crawlers identify page topic from H1"

❌ **POOR** (No data):
> "This will dramatically improve your organic traffic"

✅ **GOOD** (With data):
> "Adding H1 tags improves topic relevance scoring by ~15%; based on current ranking position, this could increase click-through by 2-5% on 40 target keywords. Effort: 2-4 hours."

---

## User Communication Guidelines

**Overall tone:**
- Neutral and analytical (not enthusiastic or promotional)
- Focus on **data and metrics** rather than subjective praise
- **Explain why** each issue matters (mechanism, not opinion)
- Provide **context** for recommendations
- Be **specific** with examples

**Avoid:**
- Hyperbolic descriptors: "genuinely," "significant," "powerful," "devastating," "critical"
- Exclamation points
- Marketing language: "good news," "opportunity," "potential," "untapped"
- Unsubstantiated adjectives: "great," "wonderful," "excellent"
- Emotional framing: "This will transform," "This is devastating," "This changes everything"

**Prefer:**
- Factual statements
- Measurable metrics
- Quantified impact
- Neutral comparisons
- Mechanism explanations
- Data sources and citations

**Term explanations:**
- Always explain technical terms in plain language
- Don't assume user knows specialized jargon
- Provide examples of good vs bad implementations
- Present issues objectively without editorial emphasis

**Examples of Tone Shifts:**

| What You Might Say | What to Say Instead |
|---|---|
| "altPath is a genuinely differentiated product" | "Free platform with no course sales, unlike direct competitors" |
| "This represents a significant competitive asset" | "Schema is valid and complete; provides foundation for AI extraction" |
| "All recommendations have been updated to reflect this corrected baseline" | "Baseline metric updated: FAQ schema adds 10 points to AEO score" |
| "This is the root cause of altPath's invisibility" | "This is the root cause of low organic visibility. [Followed by specific metrics]" |
| "Wrapped in a technically invisible package" | "99%+ of site content is invisible to crawlers due to client-side rendering" |
| "Significantly improves the starting AEO position" | "Updated AEO score baseline from 15/50 (30%) to 25/50 (50%)" |

---

## Content Format Analysis

When analyzing content, use this framing:

**❌ Poor framing:**
> "This content is weak and lacks depth"

**✅ Good framing:**
> "The content is 250 words. For this topic (career change guides), competitive content averages 1,500-2,000 words. Adding 1,000-1,500 more words would improve topic coverage. Specific gaps: no step-by-step process, no time estimates, no success rate data."

---

## Scoring & Metrics

**Present scores analytically, never as judgment:**

❌ **POOR:**
> "The site has a poor health score"

✅ **GOOD:**
> "The site has a health score of 38/100 based on: Title tags (2/10), H1 tags (0/10), Meta descriptions (0/10), FAQ schema (10/10), etc."

**Always include the breakdown** so the user understands what drives the score.

---

## Confidence & Uncertainty

When uncertain, **explicitly state it:**

✅ "Based on the rendered HTML, estimated crawlable content: <500 words (limited due to client-side rendering)"

✅ "This page may have JavaScript-rendered content not visible in the HTML"

✅ "Schema analysis unavailable in this environment; JSON-LD extraction requires curl access"

❌ Never state uncertain findings as facts

---

## Before Publishing Any Report

Check your output for:

- [ ] No exclamation points (except headings if needed for structure)
- [ ] All claims backed by specific metrics or data
- [ ] No marketing language ("opportunity," "potential," "good news," "powerful")
- [ ] No unsubstantiated adjectives ("significant," "major," "huge")
- [ ] Each issue has a quantified impact or scope (X of Y pages, ~N% improvement)
- [ ] Mechanisms explained (how/why, not just what)
- [ ] Effort estimates realistic and specific
- [ ] Tone consistent across all sections
- [ ] No emotional framing ("devastating," "critical," "transformed")

---

## Reference Documents

For tone improvements applied to SEO audits, see:
- [TONE-COMPARISON.md](outputs/altpath-2026-02-20/TONE-COMPARISON.md) - Before/after examples with explanations
- [1-site-audit-REVISED.md](outputs/altpath-2026-02-20/1-site-audit-REVISED.md) - Example of revised analytical tone
- [2-aeo-topic-research-REVISED.md](outputs/altpath-2026-02-20/2-aeo-topic-research-REVISED.md) - Data-driven AEO analysis
