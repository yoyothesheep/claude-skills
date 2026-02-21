---
name: aeo-topic-research
description: Research AEO (Answer Engine Optimization) opportunities by discovering what questions AI engines are actually answering in your niche, which domains and pages they're citing, and what content formats are winning citations.
---

# AEO Topic Research Skill

This skill identifies what to create for AEO, and how to present it. 

It uses the **Ahrefs Brand Radar** tools to pull real data: what AI engines are being asked, who they're citing, and what pages are winning citations. Then it synthesizes that into a prioritized content opportunity list.

## When to Use This Skill

- User wants to know what topics to target for AEO/AI search
- User wants to understand what their competitors are getting cited for
- User wants to identify content gaps in AI-cited results for their niche
- User wants to know which AI engines (ChatGPT, Perplexity, etc.) to prioritize

## Core Workflow

1. **Gather Input** — Brand, competitors, market/niche, target AI engines
2. **Discover AI Questions** — What questions are being asked in this space?
3. **Mine Reddit Language** — How do real people talk about this topic?
4. **Identify Cited Domains** — Who is AI citing, and how often?
5. **Identify Cited Pages** — Which specific pages are winning citations?
6. **Crawl Winning Pages** — Analyze what makes cited content work
7. **Synthesize Patterns** — What topics, formats, and structures win?
8. **Score Opportunities** — Prioritize gaps where you can realistically compete
9. **Generate Report** — Actionable content brief with priorities

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

---

## Step 2: Discover AI Questions

Use `brand-radar-ai-responses` to find what questions AI engines are actually answering in the user's market. This is the AEO equivalent of keyword research — these are the topics AI engines consider worth answering.

```python
# Get questions + responses in the user's market
responses = AHREFs.brand_radar_ai_responses(
    data_source="chatgpt",          # Run for each target engine
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

**Run this for each target AI engine** (chatgpt, perplexity, google_ai_overviews, gemini). This surfaces:
- High-volume questions your niche gets asked
- Which questions mention your brand vs. competitors vs. neither
- Citation patterns per question

**What to extract:**
- The question text (= potential content topic)
- Volume (= audience demand signal)
- Whether your domain appears in `links` (= current citation status)
- Whether competitor domains appear in `links`

**Topic clustering:** Group questions into themes. E.g., "best X for Y", "how to do Z", "X vs Y comparisons", "what is X" definitions. Each cluster = a content category.

---

## Step 3: Mine Reddit Language

Reddit threads reveal how real people phrase their questions, frustrations, and comparisons — often in the exact natural language that AI engines are trained to recognize and answer. This step enriches your topic clusters with authentic vocabulary and surfaces pain points that formal keyword research misses.

### Search Strategy

For each topic cluster from Step 2, run 2-3 Reddit searches using `web_search`:

```
site:reddit.com [topic]
site:reddit.com [topic] recommendations
site:reddit.com [topic] vs [competitor topic]
site:reddit.com best [product/service category]
site:reddit.com [topic] help
```

For example, for "email marketing software":
- `site:reddit.com email marketing software recommendations`
- `site:reddit.com klaviyo vs mailchimp`
- `site:reddit.com email marketing for small business`

Fetch the top 3-5 threads per cluster using `web_fetch`. Focus on threads with high comment counts — that signals genuine engagement and vocabulary richness.

### What to Extract From Each Thread

**Question phrasing:**
- The exact wording of the original post title (this is often a raw, unfiltered version of what AI engines get asked)
- Recurring question patterns in comments ("does anyone know how to...", "what's the best way to...")
- Follow-up questions that reveal what people still don't understand after reading standard content

**Vocabulary and terminology:**
- Jargon the community uses that differs from how brands describe things
- Abbreviations, nicknames, or shorthand (e.g., "ESP" for email service provider)
- Pain points described in plain language ("my open rates tanked", "the automations are confusing")

**Sentiment and comparison patterns:**
- How people compare options ("X is better for beginners but Y scales better")
- Common complaints about existing content ("every guide just says the same thing")
- What people wish existed ("I just want a simple comparison that...")

**Cited sources:**
- Links people share as trusted resources in comments — these are organic community endorsements and likely overlap with AI-cited pages
- Subreddits that come up repeatedly (= dedicated communities worth monitoring)

### Reddit Citation Check

Also check whether reddit.com appears in your Brand Radar cited-domains results (Step 4). If it does, note which subreddits are being cited — AI engines sometimes cite Reddit threads directly, meaning those threads are themselves AEO content worth studying in Step 6.

### Output: Reddit Language Glossary

For each topic cluster, produce a short glossary of:
- **Natural language questions** — verbatim phrasings to use in H1s, FAQs, and content
- **Community vocabulary** — terms to use throughout content for semantic match
- **Unmet needs** — gaps people complain about that your content could uniquely fill

This glossary feeds directly into Step 7 (Synthesize Patterns) and the content briefs in Step 9.

---

## Step 4: Identify Cited Domains

Use `brand-radar-cited-domains` to understand which domains AI engines trust most in this space. High citation counts = high AI authority signals.

```python
cited_domains = AHREFs.brand_radar_cited_domains(
    data_source="chatgpt",
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

**Run for each AI engine.** This tells you:
- Which domains have earned AI trust (citation authority)
- Whether your domain is in the list, and how you rank vs. competitors
- Which domains you're competing against for citations
- Which domains to study as citation role models

**Gap analysis:** If competitor domains have 10x your citation count, that's your benchmark target. If unknown domains are outperforming everyone — dig into what they're doing right.

---

## Step 5: Identify Cited Pages

Use `brand-radar-cited-pages` to find the specific pages winning citations. This is the most actionable data — you can reverse-engineer exactly what's working.

```python
cited_pages = AHREFs.brand_radar_cited_pages(
    data_source="chatgpt",
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

Collect the top 15-20 cited URLs for crawling in Step 6.

---

## Step 6: Crawl Winning Pages

Fetch the top-cited pages and analyze their structure. This reveals the *content formula* AI engines are rewarding.

```python
for url in top_cited_pages:
    content = web_fetch(url, text_content_token_limit=30000)
    # Extract and analyze
```

**For each page, extract:**

**Content Format:**
- Is it a guide, list, comparison, definition, FAQ, HowTo, or stat roundup?
- Word count range
- Does it use numbered lists, bullet points, tables, or primarily prose?
- Does it have a clear direct answer near the top (before elaboration)?

**Structure Signals:**
- H1: Is it a question or a declarative statement?
- H2/H3: Are subheadings phrased as questions?
- Does it have an FAQ section?
- Are there "Key Takeaways" or summary boxes?
- Is there schema markup (FAQ, HowTo, Article)?

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

## Step 7: Synthesize Patterns

After crawling, identify the repeating patterns across cited pages. The goal is to extract a replicable formula.

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

For each question cluster from Step 2, assess:

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

Compare your domain's citation count vs. top competitors across each AI engine:

| AI Engine | Your Citations | Competitor A | Competitor B | Gap |
|-----------|---------------|--------------|--------------|-----|
| ChatGPT | X | Y | Z | Y-X |
| Perplexity | X | Y | Z | Y-X |
| Google AI Overviews | X | Y | Z | Y-X |

This shows which AI engines you're underrepresented in, and where a focused push would have the most impact.

---

## Step 8: Score and Prioritize Opportunities

Rank content opportunities using a simple scoring model:

**Score = Demand × Competitiveness × Format Fit**

- **Demand** (1-3): Based on question volume from Step 2
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

For each high-priority opportunity, write a brief content brief (see Step 10).

---

## Step 9: Content Presentation Recommendations

Based on the winning content formula and patterns identified in Step 6, surface content presentation and structure recommendations for the user's site. These are UX-focused improvements to how content should be delivered.

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

## Step 10: Generate Report

Create a structured report with:

### Executive Summary
- AI engines analyzed
- Total questions discovered in market
- Your current citation status (# citations, # engines citing you)
- Competitor citation comparison
- Top 3 highest-priority content opportunities

### AI Question Landscape
- Full list of discovered questions, grouped by topic cluster
- Volume estimates for each
- Which questions currently cite you vs. competitors vs. neither

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

A short list (3-5 items) of structural and format recommendations based on Step 9 analysis. Example items:
- "Add table of contents with jump links to long-form guides"
- "Use collapsible FAQ sections instead of inline Q&A paragraphs"
- "Include comparison tables in competitive analysis content"
- "Implement short-paragraph formatting with bolded key terms"
- "Add 1-2 diagrams or infographics per technical guide"

### Prioritized Recommendations

A single ranked list of content opportunities, ordered by score from Step 8. For each opportunity:

**Topic:** [Topic name]
**Target question(s):** [Specific questions from Step 2]
**Monthly demand:** [Volume estimate]
**Current citation landscape:** [Who's cited, if anyone]
**Recommended format:** [Based on Step 6 patterns]
**Content brief:**
- Primary question to answer (use Reddit phrasing where available)
- Key subtopics/H2s to cover
- Natural language variants and community vocabulary to weave in
- Data/stats to include
- Schema type to implement (FAQ, HowTo, Article)
- Target length
- Authority signals to add (author bio, citations, dates)

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

If Brand Radar tools are unavailable, fall back to:
- Web search for "[niche] questions ChatGPT answers" to find common AI topics
- Manually querying AI engines for top questions in the user's niche
- Crawling competitor content to reverse-engineer what's being cited
- This fallback produces directional insights but lacks volume/citation data

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
