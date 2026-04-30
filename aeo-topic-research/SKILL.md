---
name: aeo-topic-research
description: Research AEO (Answer Engine Optimization) opportunities by discovering what questions AI engines are actually answering in your niche, which domains and pages they're citing, and what content formats are winning citations.
---

# AEO Topic Research Skill

This skill identifies what to create for AEO, and how to present it.

This skill pulls from three data sources: **Ahrefs Brand Radar** (when available) for AI question volumes and citation frequency data, **Reddit** for authentic user language and unmet needs, and **direct page crawls** of top-cited competitor pages for content format and structure signals. When Ahrefs is unavailable, AI engine queries and web search replace Brand Radar — Reddit and page crawls run regardless.

## When to Use This Skill

- User wants to know what topics to target for AEO/AI search
- User wants to understand what their competitors are getting cited for
- User wants to identify content gaps in AI-cited results for their niche
- User wants to know which AI engines (ChatGPT, Perplexity, etc.) to prioritize

## Core Workflow

Step 0. **[Coordinator]** Understand the user's site — scan codebase or crawl URL to extract topics, content themes, and vocabulary
Step 1. **[Coordinator]** Gather Input — brand, competitors, market/niche, AI engines
Step 2. **[Coordinator]** Orchestrate agents — launch Haiku agents in two waves
Steps 3-5. **[Haiku Brand Radar Agents, parallel per AI engine]** Discover AI questions (Step 3), identify cited domains (Step 4), identify cited pages (Step 5)
Step 6. **[Haiku Reddit Agent]** Mine Reddit language — search and fetch threads per topic cluster (launched after Wave 1 with topic clusters from Brand Radar results)
Step 7. **[Haiku Page Crawl Agents, parallel per URL]** Crawl top cited pages — extract content format and structure signals
Steps 8-11. **[Sonnet Agent]** Synthesize patterns, score opportunities, surface content presentation recommendations, generate report

---

## Agent Architecture

### Coordinator (main Claude)
Handles Steps 1–2: gathers user input and orchestrates agents in two waves. Passes AI engine + market context to Brand Radar agents, passes topic clusters (from Brand Radar results) to the Reddit agent, and passes cited URLs to page crawl agents. Then passes all payloads to the Sonnet agent.

### Haiku Brand Radar Agents
- One agent per AI engine (chatgpt, perplexity, google_ai_overviews, gemini)
- Launched in parallel — Wave 1
- Job: Run Brand Radar API calls for that engine — questions (Step 3), cited domains (Step 4), cited pages (Step 5) — mechanical data extraction only
- Output: structured JSON payload (see Brand Radar Agent Output Contract)

### Haiku Reddit Agent
- Single agent — launched in Wave 2 after Brand Radar results are available
- Job: Run web searches and fetch Reddit threads for the topic clusters identified in Brand Radar results
- Output: structured JSON payload (see Reddit Agent Output Contract)

### Haiku Page Crawl Agents
- One agent per top cited URL — see sampling rule below for URL selection
- Launched in parallel — Wave 2, alongside the Reddit agent
- Job: Fetch page and extract content format and structure signals — no analysis
- Output: structured JSON payload (see Page Crawl Agent Output Contract)

### Sonnet Synthesis Agent
- Single agent, runs after all Haiku agents complete
- Receives all Haiku JSON payloads
- Job: synthesize patterns, score content opportunities, write content presentation recommendations, generate final report
- Output: final report

---

## COORDINATOR

## Step 0: Understand the User's Site

Before asking for any input, extract topics, content themes, and vocabulary from the user's site. This context informs the `market` parameter and seeds topic cluster discovery.

**If running inside a codebase** (check for content files — `.md`, `.mdx`, `.tsx` routes, blog post directories):
- Glob for content files: `**/*.md`, `**/*.mdx`, `app/**/page.tsx`, `src/content/**/*`
- Read titles (H1s, frontmatter `title`), headings (H2/H3), and meta descriptions from a sample of 10–20 files
- Extract: main topic areas, recurring vocabulary, content types (guides, tools, data posts, comparisons)

**If no codebase** (running in Claude Web or no content files found):
- WebFetch the user's homepage URL
- Extract: page title, H1, main nav links, H2 section headings, any visible blog/content index
- If a `/blog`, `/guides`, or `/resources` path exists, fetch it and extract post titles

**Output of Step 0:** A `site_context` object used throughout the skill:
```json
{
  "site_context": {
    "main_topics": ["AI-proof careers", "automation risk by job", "future-proof skills"],
    "content_types": ["data-driven guides", "career comparisons", "industry reports"],
    "vocabulary": ["AI-resistant", "automation-proof", "durable skills", "career pivots"],
    "existing_pages": ["sample titles or slugs"],
    "inferred_market": "careers safe from AI automation"
  }
}
```

Use `inferred_market` as the default `market` parameter in Step 1 if the user doesn't provide one. Use `vocabulary` and `main_topics` to sharpen Brand Radar queries and Reddit search terms.

---

## Step 1: Gather Input

Ask the user for:

**Required:**
- **Brand name**: The brand to research (e.g., "Acme Inc" or "acme.com")
- **Market/niche**: What topic area? (e.g., "email marketing software", "project management")
  - This is the `market` parameter for Brand Radar — the niche context AI engines use
- **Your website URL**: For gap analysis against cited content

**Optional:**
- **Competitors**: 2-5 competitor brand names to compare against
- **AI engines to focus on**: Default is all — `chatgpt`, `perplexity`, `google_ai_overviews`, `gemini`, `copilot`, `google_ai_mode`
- **Country**: Default `US`
- **Goal emphasis**: Citation volume, citation quality, or topic gap coverage?
- **Historical context**: If the user pastes text or provides a file path (e.g. a promotion tracker, past performance notes), read it and pass it to the Sonnet agent. Use it to weight opportunities toward angles that have already proven to resonate.

---

## Step 2: Orchestrate Agents

After gathering input, launch agents in two waves. Do not wait for individual agents to finish before launching others within the same wave.

**Wave 1 — launch in parallel:**
```
For each target AI engine (chatgpt, perplexity, google_ai_overviews, gemini):
  Task(
    subagent_type: "general-purpose",
    model: "haiku",
    prompt: <HAIKU BRAND RADAR AGENT instructions below> + "\n\nAI engine: {engine}\nMarket: {market}\nBrand: {brand}\nCompetitors: {competitors}\nCountry: {country}"
  )
```

Collect all Wave 1 results. Extract topic clusters from the question data in the Brand Radar payloads. Select the top 15–20 cited page URLs across all engines.

**Wave 2 — launch in parallel:**
```
Task(
  subagent_type: "general-purpose",
  model: "haiku",
  prompt: <HAIKU REDDIT AGENT instructions below> + "\n\nMarket: {market}\nTopic clusters: {clusters_from_wave1}"
)

For each URL in top_cited_urls (selected per sampling rule below):
  Task(
    subagent_type: "general-purpose",
    model: "haiku",
    prompt: <HAIKU PAGE CRAWL AGENT instructions below> + "\n\nURL to crawl: {url}"
  )
```

**Page crawl sampling rule:** Start with the top cited URLs ranked by `responses` count. Before launching crawl agents, ensure the selected set includes **at least 2 URLs per content format type**:

| Format type | Signals to identify |
|-------------|-------------------|
| Comprehensive guide | 2000+ word article, multiple H2s, table of contents in title/URL |
| Listicle | "Top N", "Best X for Y", numbered items in title/URL |
| Comparison | "X vs Y", "Alternatives to Z", "[X] compared" in title/URL |
| Definition/FAQ | "What is X", "How does X work", FAQ in title/URL |
| HowTo | "How to X", step-by-step in title/URL |
| Stat roundup | "Statistics", "Data", "Report", "Research" in title/URL |

If the top 15–20 cited URLs are skewed toward one format (e.g., all guides), expand the crawl set by including additional cited URLs until 2 per type are covered, up to a maximum of 25 total URLs.

**Why:** Step 8 pattern analysis requires format diversity to reliably identify which content types AI engines prefer to cite. A crawl set dominated by one format produces misleading conclusions.

Collect all Wave 2 results. Once every Haiku agent has returned its payload, proceed to the SONNET AGENT section. If historical context was provided, include it in the Sonnet agent prompt under a `## Historical Context` heading.

---

## HAIKU BRAND RADAR AGENT

One agent is launched per AI engine. Each agent handles the Brand Radar API calls for that engine only.

Run all three Brand Radar calls for the assigned AI engine. This is mechanical data extraction — no analysis or judgment.

## Step 3: Discover AI Questions

```python
# Get questions + responses in the user's market
responses = AHREFs.brand_radar_ai_responses(
    data_source="chatgpt",          # Use the assigned AI engine
    market="email marketing software",
    select="question,volume,links",
    order_by="volume",
    limit=50
)

# Returns:
# - question: The actual question being asked
# - volume: Estimated monthly search volume behind this question
# - links: Pages cited in the response
```

**What to extract:**
- The question text
- Volume (audience demand signal)
- Whether the brand's domain appears in `links`
- Whether competitor domains appear in `links`

**Topic clustering:** Group questions into themes (e.g., "best X for Y", "how to do Z", "X vs Y", "what is X"). Each cluster = a content category.

## Step 4: Identify Cited Domains

```python
cited_domains = AHREFs.brand_radar_cited_domains(
    data_source="chatgpt",       # Use the assigned AI engine
    market="email marketing software",
    select="domain,responses,pages,volume",
    competitors="competitor1.com,competitor2.com"
)

# Returns:
# - domain: The cited domain
# - responses: How many AI responses cited this domain
# - pages: How many unique pages from this domain were cited
# - volume: Total search volume of queries where this domain was cited
```

## Step 5: Identify Cited Pages

```python
cited_pages = AHREFs.brand_radar_cited_pages(
    data_source="chatgpt",       # Use the assigned AI engine
    market="email marketing software",
    select="url,responses,volume",
    competitors="competitor1.com,competitor2.com"
)

# Returns:
# - url: The specific page URL being cited
# - responses: Number of AI responses that cited this page
# - volume: Search volume of queries where this page was cited
```

**Prioritize pages by:**
1. High `responses` count (cited frequently = AI trusts it)
2. High `volume` (cited on high-demand queries = more impact)
3. Pages from domains with low domain rating (= easier to compete with)

---

## Brand Radar Agent Output Contract

```json
{
  "ai_engine": "chatgpt",
  "questions": [
    {
      "question": "What is the best email marketing software for small businesses?",
      "volume": 4800,
      "brand_cited": false,
      "competitor_cited": true,
      "topic_cluster": "best-for-use-case"
    }
  ],
  "topic_clusters": [
    { "name": "best-for-use-case", "questions": 12, "total_volume": 28000 },
    { "name": "how-to-guides", "questions": 8, "total_volume": 15000 }
  ],
  "cited_domains": [
    { "domain": "competitor.com", "responses": 340, "pages": 24, "volume": 85000 }
  ],
  "cited_pages": [
    { "url": "https://competitor.com/email-marketing-guide", "responses": 45, "volume": 12000 }
  ],
  "brand_citation_count": 12,
  "token_usage": {
    "model": "claude-haiku-4-5-20251001",
    "input_tokens": 0,
    "output_tokens": 0
  }
}
```

**Notes:**
- `brand_cited` should reflect whether the user's domain appeared in `links` for that question
- `topic_clusters` is derived by grouping questions into themes — use judgment to name clusters meaningfully
- `token_usage` must be populated by every Haiku agent. Use actual API response metadata if available; otherwise estimate from prompt + output length.

---

## HAIKU REDDIT AGENT

One agent is launched after Wave 1 completes, with topic clusters passed from Brand Radar results.

## Step 6: Mine Reddit Language

Reddit threads reveal how real people phrase their questions, frustrations, and comparisons — vocabulary that AI engines recognize and answer. This step enriches topic clusters with authentic language.

### Search Strategy

For each topic cluster, run 2-3 Reddit searches using `web_search`:

```
site:reddit.com [topic]
site:reddit.com [topic] recommendations
site:reddit.com [topic] vs [competitor topic]
site:reddit.com best [product/service category]
site:reddit.com [topic] help
```

Fetch the top 3-5 threads per cluster using `web_fetch`. Focus on threads with high comment counts.

### What to Extract From Each Thread

**Question phrasing:**
- Exact wording of the original post title
- Recurring question patterns in comments
- Follow-up questions that reveal gaps in standard content

**Vocabulary and terminology:**
- Jargon the community uses that differs from how brands describe things
- Abbreviations, nicknames, or shorthand (e.g., "ESP" for email service provider)
- Pain points in plain language ("my open rates tanked", "the automations are confusing")

**Sentiment and comparison patterns:**
- How people compare options ("X is better for beginners but Y scales better")
- Common complaints about existing content ("every guide just says the same thing")
- What people wish existed ("I just want a simple comparison that...")

**Cited sources:**
- Links shared as trusted resources in comments — organic endorsements likely overlapping with AI-cited pages

---

## Reddit Agent Output Contract

```json
{
  "topic_clusters": [
    {
      "cluster": "best-for-use-case",
      "reddit_questions": [
        "What email marketing tool actually works for a one-person shop?",
        "Anyone switched from Mailchimp recently and happy with it?"
      ],
      "community_vocabulary": ["ESP", "open rate", "drip sequence", "cold email"],
      "unmet_needs": [
        "Simple comparison that doesn't assume technical background",
        "Honest review that includes pricing gotchas"
      ],
      "cited_sources_in_threads": ["https://trusted-review-site.com/email-tools"],
      "threads_fetched": 4
    }
  ],
  "reddit_cited_by_ai": false,
  "token_usage": {
    "model": "claude-haiku-4-5-20251001",
    "input_tokens": 0,
    "output_tokens": 0
  }
}
```

**Notes:**
- `reddit_cited_by_ai` should be `true` if reddit.com appeared in cited domains from any Brand Radar agent payload
- Include the subreddit name in `threads_fetched` count if notable communities (e.g., r/emailmarketing, r/entrepreneur) appear repeatedly

---

## HAIKU PAGE CRAWL AGENT

One agent is launched per top cited URL (top 15–20 from Brand Radar results, prioritized by `responses` count).

## Step 7: Crawl Winning Pages

Fetch the assigned page and extract content format and structure signals. This is mechanical extraction — no analysis of whether the signals are good or bad.

```python
content = web_fetch(url, text_content_token_limit=30000)
```

**For the page, extract:**

**Content Format:**
- Is it a guide, list, comparison, definition, FAQ, HowTo, or stat roundup?
- Approximate word count
- Does it use numbered lists, bullet points, tables, or primarily prose?
- Does it have a clear direct answer near the top (before elaboration)?

**Structure Signals:**
- H1: Is it a question or a declarative statement?
- H2/H3: Are subheadings phrased as questions?
- Does it have an FAQ section?
- Are there "Key Takeaways" or summary boxes?
- Does it have a table of contents?
- Is there schema markup visible (FAQ, HowTo, Article)?

**Authority Signals:**
- Author bio present?
- Publication/update date visible?
- Citations or external links to sources?
- Statistics with attribution?

**Topic Depth:**
- Does it cover the topic comprehensively or just surface level?
- Does it answer follow-up questions proactively?
- Does it define terms?

---

## Page Crawl Agent Output Contract

```json
{
  "url": "https://competitor.com/email-marketing-guide",
  "fetch_status": 200,
  "content_format": "comprehensive-guide",
  "word_count_estimate": 3200,
  "has_direct_answer_at_top": true,
  "uses_numbered_lists": true,
  "uses_bullet_points": true,
  "uses_tables": true,
  "uses_primarily_prose": false,
  "h1_style": "declarative",
  "h2s_as_questions": true,
  "has_faq_section": true,
  "has_key_takeaways": true,
  "has_table_of_contents": true,
  "schema_types_detected": ["FAQPage", "Article"],
  "author_bio_present": true,
  "date_visible": true,
  "external_citations": 8,
  "defines_terms": true,
  "answers_follow_up_questions": true,
  "token_usage": {
    "model": "claude-haiku-4-5-20251001",
    "input_tokens": 0,
    "output_tokens": 0
  }
}
```

**Notes:**
- If fetch fails, include `"fetch_status": null` and `"error": "..."` — do not omit the URL
- `content_format` should be one of: `guide`, `list`, `comparison`, `definition`, `faq`, `howto`, `stat-roundup`, `comprehensive-guide`, `other`

---

## SONNET AGENT

The Sonnet agent receives all Haiku JSON payloads. It never fetches URLs or calls APIs directly. All analysis, judgment, pattern recognition, and report writing happens here.

**Historical context:** If the coordinator received historical performance data (pasted text or a file), pass it in the prompt under a `Historical Context` heading. Use it to boost opportunity scores for angles that match proven high-performers (e.g. if "no degree" listicles drove 311K Reddit views, weight similar angles higher). Explicitly call out in the report which recommendations are reinforced by historical data.

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
Use actual API response metadata if available; otherwise estimate from input/output length.

## Step 8: Synthesize Patterns

After receiving all Haiku payloads, identify repeating patterns across cited pages. The goal is to extract a replicable formula.

### Content Format Patterns

Tally which formats appear most in cited pages:

| Format | # Cited Pages Using It | Notes |
|--------|----------------------|-------|
| Listicle (numbered) | X | "Top 10 X for Y" |
| Comprehensive guide | X | 2000+ words, multiple H2s |
| Comparison/vs | X | Side-by-side structure |
| Definition/what is | X | Direct answer first |
| HowTo (steps) | X | Numbered steps |
| FAQ page | X | Q&A format |
| Stat roundup | X | Data-heavy, cited sources |

### Topic Gap Matrix

For each question cluster from the Brand Radar payloads, assess:

| Topic | Demand (volume) | Your Coverage | Competitor Coverage | AI Cites You? | Opportunity |
|-------|----------------|---------------|---------------------|---------------|-------------|
| "best X for Y" | High | None | Strong | No | 🔴 High |
| "how to Z" | Medium | Weak | Weak | No | 🟡 Medium |
| "what is X" | Low | Good | Strong | No | 🟢 Low |

**Opportunity scoring:**
- 🔴 **High**: High demand + you have no coverage + competitors' content is weak or missing
- 🟡 **Medium**: Medium demand + your coverage is thin or your content isn't getting cited despite existing
- 🟢 **Low**: Low demand OR strong incumbent coverage you'd struggle to displace

### Citation Authority Gap

Compare the brand's domain citation count vs. top competitors across each AI engine (from Brand Radar payloads):

| AI Engine | Your Citations | Competitor A | Competitor B | Gap |
|-----------|---------------|--------------|--------------|-----|
| ChatGPT | X | Y | Z | Y-X |
| Perplexity | X | Y | Z | Y-X |
| Google AI Overviews | X | Y | Z | Y-X |

---

## Step 9: Score and Prioritize Opportunities

Rank content opportunities using a simple scoring model:

**Score = Demand × Competitiveness × Format Fit**

- **Demand** (1-3): Based on question volume from Brand Radar payloads
  - 3 = High volume (top 25% of questions in your market)
  - 2 = Medium volume
  - 1 = Low volume

- **Competitiveness** (1-3): Based on how well competitors are covering this topic and being cited for it
  - 3 = No strong incumbent in AI citations (open territory)
  - 2 = One weak incumbent
  - 1 = Multiple strong incumbents dominating citations

- **Format Fit** (1-3): Based on whether the winning format is something you can execute
  - 3 = Format matches your existing content capabilities
  - 2 = Learnable with moderate effort
  - 1 = Requires significant new capability

**Priority tiers:**
- 🔴 **Create Now** (Score 7-9): High-impact, low-competition topics with clear format playbook
- 🟡 **Plan Soon** (Score 4-6): Good opportunities that need more effort or planning
- 🟢 **Monitor** (Score 1-3): Lower priority — watch to see if competition weakens

---

## Step 10: Content Presentation Recommendations

Based on the winning content formula and patterns identified in the page crawl payloads, surface content presentation and structure recommendations. These are UX-focused improvements to how content should be delivered.

### Content Navigation
- Do top-cited pages include a table of contents for longer content?
- Are there jump links (#anchor links) to sections?
- Is sticky navigation used for quick access to key sections?
- **Recommendation**: Suggest adding these navigation aids if they appear in winning content but not in the user's existing content

### Content Format & Structure
- What format do winning pages use? (Expandable FAQs, collapsible sections, tabs, inline definitions, accordion-style Q&A)
- Are these formats more scannable or engaging than what the user currently has?
- **Recommendation**: Suggest adopting formats that appear frequently in cited content if they improve scannability

### Visual Hierarchy Signals
- Do cited pages use callout boxes, highlighted statistics, summary cards, or "key takeaways" boxes?
- Are there visual breaks (rules, spacing) that improve readability?
- **Recommendation**: Note if the user's content lacks visual breaks compared to competitors

### Multimedia Integration
- Do top-cited pages use video, diagrams, infographics, screenshots, or interactive elements?
- Where are these elements positioned (near key concepts, at the beginning, scattered)?
- **Recommendation**: Suggest adding multimedia to specific sections of planned content to match citation-winning pages

### Scannability Patterns
- Are short paragraphs more common than long blocks of text in cited pages?
- Do cited pages use bold key phrases, pull-quotes, or highlighted stats?
- **Recommendation**: Suggest adopting these patterns if planning long-form content

### Output: Content Presentation Recommendations
Include a short section in the report (3-5 bullet points max) titled "**Content Presentation Recommendations**" that lists:
- 1-2 navigation improvements (TOC, jump links, etc.)
- 1-2 format/structure improvements (accordions, callout boxes, etc.)
- 1 multimedia gap to address
- 1 scannability improvement

Example:
- "Add table of contents with jump links to all 'How to X' guides based on winning formats"
- "Use collapsible FAQ sections for Q&A content instead of inline paragraphs (matches cited pages)"
- "Include 1-2 comparison tables per guide (100% of cited competitors use these)"
- "Use short paragraphs (2-4 sentences max) and bold key terms (matches 8 of 10 top-cited pages)"

---

## Step 11: Generate Report

Create a structured report with:

### Executive Summary
- AI engines analyzed
- Total questions discovered in market
- Your current citation status (# citations, # engines citing you)
- Competitor citation comparison
- Top 3 highest-priority content opportunities
- **Total research cost: $—** (one line; full breakdown in Token Usage appendix at end of report)

### Prioritized Recommendations

**CRITICAL: This section MUST be titled exactly `## Prioritized Recommendations` (H2, no variation).** growth-pm scans for this exact string to extract citation candidates. Do not rename it, reorder it, or nest it under another heading.

**What to include:**
- **All** 🔴 Create Now and 🟡 Plan Soon opportunities — no cap, no omissions
- **Top 2** 🟢 Monitor items, selected by highest score
- If more than 2 Monitor items were identified, append: `> _N additional Monitor items not listed — see AI Question Landscape for full list._`

**Priority tiers:**

| Tier | Score | Label | Include |
|---|---|---|---|
| 🔴 Create Now | 7–9 | High-impact, low-competition; clear format playbook | All |
| 🟡 Plan Soon | 4–6 | Good opportunity; needs more effort or planning | All |
| 🟢 Monitor | 1–3 | Lower priority; watch for competition weakening | Top 2 |

**Table preview** — one row per recommendation, ordered by tier then score descending:

| # | Priority | Score | Content Piece | Category | Effort |
|---|---|---|---|---|---|
| 1 | 🔴 Create Now | 9 | [Title of content piece] | AEO / Content | Moderate |
| 2 | 🔴 Create Now | 8 | [Title of content piece] | Content | Major |
| 3 | 🟡 Plan Soon | 6 | [Title of content piece] | AEO / Content | Moderate |
| 4 | 🟡 Plan Soon | 5 | [Title of content piece] | Content | Moderate |
| 5 | 🟢 Monitor | 3 | [Title of content piece] | Content | Quick |
| 6 | 🟢 Monitor | 2 | [Title of content piece] | Content | Moderate |

Then the full list with details for each item, in the same order as the table:

Order within each tier by score (descending). For each item:

- **What to do**: Specific content action (e.g., "Create FAQ page targeting 'how to X'")
- **Why it matters**: Data-backed impact (e.g., "Cited by ChatGPT in 45 responses" / "2,400 searches/month, no strong incumbent")
- **Category**: AEO / Content / Information Architecture / Content Presentation
- **Effort**: Quick (<30 min) / Moderate (1–3 hrs) / Major (4+ hrs)

**Content brief** (for each 🔴 Create Now item):
- Primary question to answer (use Reddit phrasing where available)
- Key subtopics/H2s to cover
- Natural language variants and community vocabulary to weave in
- Data/stats to include
- Schema type to implement (FAQ, HowTo, Article)
- Target length
- Authority signals to add (author bio, citations, dates)


### AI Question Landscape

Full list of discovered questions, grouped by topic cluster.

**Format: table, one row per question, ordered by volume descending within each cluster.**

| Question | Cluster | Est. Monthly Volume | Channels | Cited: You | Cited: Competitors |
|----------|---------|---------------------|----------|------------|-------------------|
| What is the best X for Y? | best-for-use-case | 1,000–5,000 | ChatGPT, Perplexity, Reddit | ✗ | ✓ Competitor A |

**Volume format depends on data source:**
- **With Brand Radar**: use numeric ranges derived from the raw `volume` value:
  - < 500 → `< 500`
  - 500–999 → `500–1,000`
  - 1,000–4,999 → `1,000–5,000`
  - 5,000–9,999 → `5,000–10,000`
  - 10,000+ → `10,000+`
- **Without Brand Radar** (fallback mode): use `High / Medium / Low` based on how frequently the question appeared across manual AI engine queries and Reddit. Never show numbers you don't have.

**Channels column:** List every source where this question appeared — e.g. `ChatGPT, Perplexity, Reddit`. If a question appeared across all engines, write `All engines`. If it surfaced only in Reddit threads, write `Reddit only`. This signals where to prioritize distribution.

### Reddit Language Glossary
- Natural language question phrasings extracted from top threads, per topic cluster
- Community vocabulary and terminology to use in content
- Unmet needs and content gaps surfaced from complaints and unanswered questions
- Any Reddit threads that are themselves being cited by AI engines

### Citation Authority Analysis
- Domain citation rankings per AI engine
- Your rank vs. competitors
- Which engines are underserving your brand

### Winning Content Formula
- The 2-3 dominant content formats getting cited in your niche
- Structural patterns (H1 style, FAQ presence, schema, author bios, etc.)
- Average depth and length of cited content

### Content Presentation Recommendations

A short list (3-5 items) of structural and format recommendations based on Step 10 analysis. Example items:
- "Add table of contents with jump links to long-form guides"
- "Use collapsible FAQ sections instead of inline Q&A paragraphs"
- "Include comparison tables in competitive analysis content"
- "Implement short-paragraph formatting with bolded key terms"
- "Add 1-2 diagrams or infographics per technical guide"

### Token Usage

**Pricing reference:**
- Haiku 4.5: $0.80 / 1M input tokens, $4.00 / 1M output tokens
- Sonnet 4.6: $3.00 / 1M input tokens, $15.00 / 1M output tokens

| Model | Agent | Input Tokens | Output Tokens | Total Tokens | Est. Cost |
|-------|-------|-------------|--------------|-------------|-----------|
| claude-haiku-4-5 | Brand Radar: chatgpt | — | — | — | $— |
| claude-haiku-4-5 | Brand Radar: perplexity | — | — | — | $— |
| claude-haiku-4-5 | Brand Radar: google_ai_overviews | — | — | — | $— |
| claude-haiku-4-5 | Brand Radar: gemini | — | — | — | $— |
| claude-haiku-4-5 | Reddit agent | — | — | — | $— |
| claude-haiku-4-5 | Page crawl: {url} | — | — | — | $— |
| claude-sonnet-4-6 | Synthesis agent | — | — | — | $— |
| **Total** | | | | | **$—** |

Populate from the `token_usage` fields in each Haiku payload plus the Sonnet agent's self-reported usage. Est. Cost = `(input_tokens / 1,000,000 × input_rate) + (output_tokens / 1,000,000 × output_rate)`, rounded to 4 decimal places.

---

## Output Format

Default: Markdown file saved to `/mnt/user-data/outputs/` and presented with `present_files`.

Optional additions if user requests:
- **Spreadsheet**: Keyword/topic list with scoring columns
- **Content briefs**: One doc per high-priority topic

---

## User Communication

**Refer to [TONE-GUIDE.md](../TONE-GUIDE.md) for comprehensive tone and communication guidelines.**

---

## Important Notes

### Brand Radar Data Nuances

- `market` parameter is a niche descriptor — keep it specific (e.g., "email marketing software" not just "software")
- The `volume` field is an *estimate* based on Google search data for related queries, not direct AI query counts
- Data availability varies by AI engine — Google AI Overviews and ChatGPT tend to have the most coverage
- If Brand Radar returns sparse results for a very narrow market, broaden the `market` string slightly

### Without Ahrefs Brand Radar

If Brand Radar tools are unavailable, substitute each API call with manual equivalents, then proceed with the same Reddit and page crawl steps.

**Replacing Brand Radar AI Responses (Step 3):**
- Directly query each AI engine (ChatGPT, Perplexity, etc.) with prompts like: "What are the most common questions people ask about [niche]?" and "What's the best [product/service] for [use case]?" Record what it says and what it cites.
- Web search: `site:reddit.com OR site:quora.com "[niche]" questions` to surface real phrasing
- Pull Google's "People Also Ask" results for the top 3–5 niche terms
- Search `"[niche]" perplexity answers` or `chatgpt "[niche]"` to find published AI response research

**Replacing Brand Radar Cited Domains (Step 4):**
- Run 10–15 representative questions through each AI engine manually; record every domain cited in the responses
- Tally domains by frequency — this is your cited domain ranking without volume data

**Replacing Brand Radar Cited Pages (Step 5):**
- From the cited domains above, note specific page URLs that appear repeatedly across AI responses
- Web search `site:[competitor.com] [topic]` to surface their most-indexed content in this niche

**Reddit and page crawls (Steps 6–7) run the same as with Ahrefs.** Topic clusters for the Reddit agent come from manually grouped question themes instead of Brand Radar payloads.

This fallback produces directional insights but lacks volume estimates and citation frequency data — treat findings as qualitative signals rather than ranked metrics.

### Integration with Other Skills

This skill is the **research phase** in a three-part workflow:

1. **`aeo-topic-research`** (this skill) → Discover what topics to create
2. **`aeo-seo-site-audit`** → Audit existing content for AEO compliance
3. **`seo-keyword-research`** → Validate topics against traditional SEO demand

### Communicating Results

- Explain that "citations" = AI engines recommending your content, not traditional backlinks
- Frame volume estimates as directional signals, not guarantees
- Remind users that AEO is still an emerging field — what works today may evolve
- Be specific: give exact question strings, not vague topic areas
