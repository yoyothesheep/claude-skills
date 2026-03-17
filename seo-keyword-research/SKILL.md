---
name: seo-keyword-research
description: Analyze competitor websites to identify their SEO strategies, content gaps, and generate prioritized target keywords with ranking potential. Use when users want to understand competitor SEO tactics, find keyword opportunities, identify content gaps, or build a keyword strategy based on competitive intelligence.
---

# SEO Competitor Analysis & Keyword Research Skill

This skill analyzes competitor websites to reverse-engineer their SEO strategies, identifies content gaps and opportunities, and generates a prioritized list of target keywords based on ranking potential, search volume, and competitive dynamics.

## 🚀 Ahrefs Integration

This skill is designed to work with the **Ahrefs MCP server**. When Ahrefs is available, the skill uses real data for:
- Exact search volumes
- Accurate keyword difficulty scores
- Actual organic traffic estimates
- Competitor traffic analysis
- SERP feature detection
- Traffic potential calculations

**Without Ahrefs:** The skill falls back to manual SERP analysis and proxy estimates (still effective, but less precise).

## When to Use This Skill

Trigger this skill when the user:
- Asks to "analyze my competitors' SEO"
- Wants to know "what keywords are my competitors ranking for"
- Requests "keyword opportunities" or "keyword gap analysis"
- Asks "what content should I create to compete"
- Mentions "competitive analysis for SEO"
- Wants to "find keywords I can rank for"
- Asks "what's my competitor's content strategy"

## Core Workflow

Step 1. **[Coordinator]** Gather Input — website, competitor URLs, niche, preferences
Step 2. **[Coordinator]** Orchestrate agents — launch Haiku agents in two waves
Steps 3-4. **[Haiku Competitor Agents, parallel per competitor]** Get Ahrefs metrics + top organic keywords (Step 3), crawl key pages (Step 4)
Step 5. **[Haiku Keyword Research Agent]** Research keywords via Ahrefs (or web search fallback) — launched after Wave 1 with keyword seeds from competitor data
Steps 6-11. **[Sonnet Agent]** Analyze competitor content, identify patterns, perform gap analysis, evaluate ranking potential, prioritize keywords, surface IA recommendations, generate report

---

## Agent Architecture

### Coordinator (main Claude)
Handles Steps 1–2: gathers user input and orchestrates agents in two waves. Passes competitor URLs to Competitor agents, extracts keyword seeds from competitor results, then passes seeds to the Keyword Research agent. Passes all payloads to the Sonnet agent.

### Haiku Competitor Agents
- One agent per competitor URL — launched in parallel, Wave 1
- Job: Pull Ahrefs site metrics + top organic keywords (Step 3), then crawl 5–8 key pages (Step 4) — mechanical data extraction only
- Output: structured JSON payload (see Competitor Agent Output Contract)

### Haiku Keyword Research Agent
- Single agent — launched in Wave 2 after Competitor agent results are available
- Job: Run Ahrefs keyword explorer calls (or web search fallback) using keyword seeds from competitor data
- Output: structured JSON payload (see Keyword Research Agent Output Contract)

### Sonnet Synthesis Agent
- Single agent, runs after all Haiku agents complete
- Receives all Haiku JSON payloads
- Job: content analysis, pattern identification, gap analysis, ranking evaluation, prioritization, IA recommendations, report writing
- Output: final strategy report

---

## COORDINATOR

## Step 1: Gather Input

Ask the user for:

**Required:**
- **Your website**: URL of the user's site (for gap analysis)
- **Competitor URLs**: 2-5 competitor websites to analyze
  - Ask: "Who are your main competitors in search?"
  - If they don't know: "What keywords do you want to rank for? I'll find who's ranking."

**Optional (ask if not clear):**
- **Your niche/industry**: What business are you in?
- **Target audience**: Who are you trying to reach?
- **Geographic focus**: Local, national, or international?
- **Current keyword targets**: What keywords are you already targeting?
- **Goals**: Traffic, conversions, brand awareness, or thought leadership?

---

## Step 2: Orchestrate Agents

After gathering input, launch agents in two waves. Do not wait for individual agents to finish before launching others within the same wave.

**Wave 1 — launch in parallel:**
```
For each competitor_url in competitor_urls:
  Task(
    subagent_type: "general-purpose",
    model: "haiku",
    prompt: <HAIKU COMPETITOR AGENT instructions below> + "\n\nCompetitor URL: {competitor_url}\nUser site: {user_site}\nCountry: {country}\nDate: {current_date}"
  )
```

Collect all Wave 1 results. Extract keyword seeds: take the top 20–30 keywords by traffic from each competitor payload and deduplicate. Also extract the user's Ahrefs domain rating if available from any payload.

**Wave 2 — launch after Wave 1 completes:**
```
Task(
  subagent_type: "general-purpose",
  model: "haiku",
  prompt: <HAIKU KEYWORD RESEARCH AGENT instructions below> + "\n\nKeyword seeds: {keyword_seeds}\nNiche: {niche}\nCountry: {country}\nUser domain rating: {user_dr}"
)
```

Collect Wave 2 results. Once every Haiku agent has returned its payload, proceed to the SONNET AGENT section.

---

## HAIKU COMPETITOR AGENT

One agent is launched per competitor URL. Each agent handles Ahrefs API calls and page crawling for that competitor only.

All work in Steps 3–4 is mechanical data extraction — no analysis or judgment.

## Step 3: Get Ahrefs Metrics + Top Keywords (if Ahrefs available)

```python
# Get competitor's overall organic performance
metrics = AHREFs.site_explorer_metrics(
    target=competitor_url,
    mode="subdomains",
    date="2026-02-25",  # Use current date
    country="US",       # Or user's target country
    volume_mode="monthly"
)

# Extract key data:
# - org_traffic: Current monthly organic traffic
# - org_keywords: Total keywords ranking
# - org_keywords_1_3: Keywords in top 3
# - org_cost: Estimated traffic value
# - domain_rating: DR score
```

```python
# Get competitor's top organic keywords
top_keywords = AHREFs.site_explorer_organic_keywords(
    target=competitor_url,
    mode="subdomains",
    date="2026-02-25",
    country="US",
    select="keyword,best_position,sum_traffic,volume,keyword_difficulty,serp_features",
    order_by="sum_traffic:desc",
    limit=100,
    volume_mode="monthly"
)
```

## Step 4: Crawl Key Pages

For each competitor, crawl **exactly 2 pages per type** using the table below. This ensures consistent coverage across runs and prevents findings from varying based on arbitrary page selection.

**Required page types and how to find them:**

| Type | Pages to crawl | How to identify |
|------|---------------|-----------------|
| Homepage | 1 (the root URL) | Given |
| Blog/Resource | 2 | `/blog/`, `/resources/`, `/learn/`, `/guides/` paths; or main nav links labeled "Blog", "Learn", "Resources" |
| Category/Topic hub | 2 | Top-level nav links for features/topics/solutions; `/solutions/`, `/use-cases/`, `/topics/` |
| Product/Service detail | 2 | Specific feature or offering page; `/features/[x]`, `/solutions/[x]`, `/products/[x]` |

**Rules:**
- Crawl the homepage + 2 pages of each remaining type = minimum 7 pages per competitor
- Use Ahrefs top pages data (if available) to select the 2 highest-traffic pages per type
- If a type doesn't exist (e.g., no blog), substitute with the next most-linked type from the homepage nav
- If a page fetch fails, include `"url": "...", "error": "..."` — do not skip it or substitute silently

```python
# Fetch homepage first
home_content = web_fetch(competitor_url)

# Extract internal links from nav and prioritize by type:
# - /blog/ or /resources/ or /learn/ → Blog/Resource type
# - Main navigation category links → Category/Topic hub type
# - Feature or product-specific pages → Product/Service detail type

# Crawl 2 pages per type after homepage
```

**For each crawled page, extract:**
- Page title and meta description
- H1 and heading structure (H2, H3 patterns)
- Approximate word count
- Main topics and themes
- Content type (guide, tutorial, comparison, list, definition)
- Has table of contents? Has FAQ? Has schema?
- Publication/update date (if visible)
- Internal link count
- Calls-to-action

---

## Competitor Agent Output Contract

```json
{
  "competitor_url": "https://competitor.com",
  "ahrefs_available": true,
  "ahrefs_metrics": {
    "org_traffic": 850000,
    "org_keywords": 125000,
    "org_keywords_1_3": 18000,
    "org_cost": 1250000,
    "domain_rating": 78
  },
  "top_keywords": [
    {
      "keyword": "project management software",
      "best_position": 2,
      "sum_traffic": 45000,
      "volume": 110000,
      "keyword_difficulty": 68,
      "serp_features": ["ai_overview", "snippet"]
    }
  ],
  "crawled_pages": [
    {
      "url": "https://competitor.com/blog/project-management-guide",
      "title": "The Complete Guide to Project Management",
      "meta_description": "...",
      "h1": "The Complete Guide to Project Management in 2026",
      "headings": [
        { "level": "h2", "text": "What is project management?" },
        { "level": "h2", "text": "Project management methodologies" }
      ],
      "word_count_estimate": 4200,
      "content_type": "comprehensive-guide",
      "has_table_of_contents": true,
      "has_faq": true,
      "has_schema": true,
      "date_visible": "2025-11-12",
      "internal_link_count": 18
    }
  ],
  "token_usage": {
    "model": "claude-haiku-4-5-20251001",
    "input_tokens": 0,
    "output_tokens": 0
  }
}
```

**Notes:**
- If Ahrefs is unavailable, set `"ahrefs_available": false` and omit `ahrefs_metrics` and `top_keywords`
- If a page fetch fails, include `"url": "...", "error": "..."` — do not omit it
- `token_usage` must be populated by every Haiku agent. Use actual API response metadata if available; otherwise estimate from prompt + output length.

---

## HAIKU KEYWORD RESEARCH AGENT

One agent, launched in Wave 2 after Competitor agent results are available. Receives keyword seeds extracted from competitor data.

## Step 5: Research Keywords

Run Ahrefs keyword explorer calls using the seeds provided. If Ahrefs is unavailable, fall back to web search SERP analysis.

### With Ahrefs

```python
# Method 1: Get exact metrics for keyword seeds
keyword_data = AHREFs.keywords_explorer_overview(
    keywords=",".join(keyword_seeds),
    country="US",
    select="keyword,volume,difficulty,cpc,traffic_potential,clicks,cps,serp_features,intents"
)

# Method 2: Find related keyword opportunities
for seed in top_seeds:
    related = AHREFs.keywords_explorer_related_terms(
        keywords=seed,
        country="US",
        select="keyword,volume,difficulty,traffic_potential",
        order_by="traffic_potential:desc",
        limit=50,
        where='{"and": [{"field": "difficulty", "is": ["lte", 40]}]}'
    )

# Method 3: Matching terms for pattern-based discovery
matches = AHREFs.keywords_explorer_matching_terms(
    terms=",".join(top_seeds[:5]),
    country="US",
    match_mode="any",
    select="keyword,volume,difficulty,clicks,traffic_potential,serp_features",
    where='{"and": [{"field": "volume", "is": ["gte", 100]}]}',
    order_by="traffic_potential:desc",
    limit=200
)
```

### Without Ahrefs (Fallback)

For each seed keyword, run web searches to assess:
- What types of content rank (lists, guides, comparisons)
- Title patterns in top results
- "People Also Ask" questions
- Related searches
- SERP features present
- Competition level (who's ranking: major brands, niche sites, thin content)

---

## Keyword Research Agent Output Contract

```json
{
  "ahrefs_available": true,
  "keywords": [
    {
      "keyword": "project management software",
      "volume": 110000,
      "difficulty": 68,
      "traffic_potential": 185000,
      "clicks": 62000,
      "cpc": 890,
      "serp_features": ["ai_overview", "snippet", "question"],
      "intents": {
        "informational": false,
        "commercial": true,
        "transactional": false,
        "navigational": false
      }
    },
    {
      "keyword": "agile project management for small teams",
      "volume": 2400,
      "difficulty": 22,
      "traffic_potential": 4800,
      "clicks": 1400,
      "cpc": 340,
      "serp_features": ["question"],
      "intents": {
        "informational": true,
        "commercial": true,
        "transactional": false,
        "navigational": false
      }
    }
  ],
  "total_keywords_found": 187,
  "token_usage": {
    "model": "claude-haiku-4-5-20251001",
    "input_tokens": 0,
    "output_tokens": 0
  }
}
```

**Notes:**
- `cpc` is in USD cents (Ahrefs convention) — Sonnet will convert to dollars for display
- If Ahrefs unavailable, set `"ahrefs_available": false` and include `"serp_signals"` objects instead of exact metrics

---

## SONNET AGENT

The Sonnet agent receives all Haiku JSON payloads. It never fetches URLs or calls APIs directly. All analysis, gap identification, ranking evaluation, prioritization, and report writing happens here.

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

## Step 6: Analyze Competitor Content

Using the `crawled_pages` data from each Competitor agent payload:

### Content Strategy Patterns

**Topic Coverage:**
- What main topics does each competitor cover?
- How deep is their coverage of each topic?
- What subtopics do they address?
- Are there topic clusters?

**Content Types:**
- Guides (how-to, ultimate guide, beginner's guide)
- Lists (top 10, best X for Y)
- Comparisons (X vs Y, alternatives to Z)
- Tools/calculators/resources
- Case studies/examples
- News/updates
- Definitions/glossaries

**Content Depth:**
- Average word count across crawled pages
- Level of detail (beginner, intermediate, advanced)
- Use of examples, data, visuals
- Comprehensiveness

**Content Freshness:**
- Publication dates (if visible)
- Update frequency
- Evergreen vs timely content

### SEO Optimization Patterns

**Title Tag Strategy:**
- Keyword placement
- Format patterns (e.g., "How to [X]: [Benefit] Guide")
- Brand positioning

**Heading Strategy:**
- H1 formats
- H2/H3 structure
- Keyword usage in headings

**Content Structure:**
- Table of contents usage
- Section organization
- List vs paragraph heavy
- Visual content integration

**Internal Linking:**
- Link density
- Anchor text patterns
- Topic clustering approach

---

## Step 7: Identify Content Patterns

Synthesize findings across all competitors:

### Common Themes:
- Topics ALL competitors cover (table stakes)
- Topics MOST competitors cover (important)
- Topics FEW competitors cover (opportunities)

### Successful Patterns:
- Content formats that appear frequently
- Structural approaches that repeat
- Topic angles that multiple sites use

### Differentiation Opportunities:
- Topics only one competitor covers well
- Gaps where no competitor has comprehensive coverage
- Angles or approaches no one is taking

---

## Step 8: Perform Gap Analysis

Compare the user's site to competitors:

### Content Gaps:
- **Topics competitors cover that you don't**: Defensive opportunities (prevent losing traffic)
- **Topics you cover that competitors don't**: Offensive opportunities (unique positioning)
- **Depth gaps**: Topics where competitors have more comprehensive coverage
- **Format gaps**: Content types competitors use that you don't

### Keyword Gaps (from Ahrefs data):
- Keywords competitors rank for that the user doesn't
- Keyword themes competitors prioritize
- Traffic being captured by competitors that user is missing

### Quality Gaps:
- Where competitors have stronger content
- Where you have stronger content
- Opportunities to create definitive resources

### Traffic Opportunity Analysis (with Ahrefs data):

Use the keyword data from the Step 5 Keyword Research agent payload. For each keyword, calculate expected traffic at different positions:

```python
def calculate_traffic_potential(keyword_data, target_position):
    volume = keyword_data['volume']
    clicks = keyword_data['clicks']
    serp_features = keyword_data.get('serp_features', [])

    ctr_by_position = {
        1: 0.316, 2: 0.159, 3: 0.108, 4: 0.073, 5: 0.055,
        6: 0.044, 7: 0.037, 8: 0.031, 9: 0.027, 10: 0.024
    }

    base_ctr = ctr_by_position.get(target_position, 0.01)

    if 'ai_overview' in serp_features:
        base_ctr *= 0.6
    if 'snippet' in serp_features and target_position > 1:
        base_ctr *= 0.8
    if 'local_pack' in serp_features:
        base_ctr *= 0.5
    if len([f for f in serp_features if f.startswith('paid_')]) >= 3:
        base_ctr *= 0.7

    if clicks and clicks > 0:
        traffic = clicks * (base_ctr / sum(ctr_by_position.values()))
    else:
        traffic = volume * base_ctr

    return int(traffic)
```

---

## Step 9: Evaluate Ranking Potential and Prioritize Keywords

### Difficulty Assessment (with Ahrefs)

Use the `difficulty` score from the Keyword Research agent payload:

| Range | Label | Action |
|-------|-------|--------|
| 0-10 | Very Easy | Target immediately |
| 11-30 | Easy | Target in first 30 days |
| 31-50 | Medium | Build comprehensive content |
| 51-70 | Hard | Long-term investment (6-12 months) |
| 71-100 | Very Hard | Consider alternatives |

### Difficulty Assessment (without Ahrefs)

**High Difficulty Indicators:**
- Top 10 dominated by major brands (Forbes, HubSpot, Shopify, etc.)
- Extremely comprehensive content (5,000+ words)
- Many strong backlinks visible in SERPs
- Highly commercial intent with ad-heavy SERPs

**Medium Difficulty Indicators:**
- Mix of big brands and smaller/niche sites
- Moderate content depth (1,500-3,000 words)
- Some older content (opportunity to update)

**Low Difficulty Indicators:**
- Small/niche sites ranking well
- Thin or outdated content in top 10
- Forum posts or Q&A sites ranking (Reddit, Quora)
- Very specific long-tail queries

### Traffic Opportunity Score (with Ahrefs)

```python
def calculate_opportunity_score(keyword_data, your_domain_rating):
    volume = keyword_data['volume']
    difficulty = keyword_data['difficulty']
    traffic_if_pos_3 = calculate_traffic_potential(keyword_data, 3)
    cpc = keyword_data.get('cpc', 0) / 100  # Convert cents to dollars

    intent_multiplier = 1.0
    if keyword_data['intents'].get('transactional'):
        intent_multiplier = 2.0
    elif keyword_data['intents'].get('commercial'):
        intent_multiplier = 1.5

    feasibility = max(0.1, (your_domain_rating - difficulty) / 100 + 0.5)

    if difficulty <= 30:
        time_factor = 1.0
    elif difficulty <= 50:
        time_factor = 3.0
    elif difficulty <= 70:
        time_factor = 6.0
    else:
        time_factor = 12.0

    traffic_value = traffic_if_pos_3 * (cpc if cpc > 0 else 2)
    score = (traffic_value * feasibility * intent_multiplier) / (difficulty * time_factor)

    return {
        'score': round(score, 2),
        'expected_traffic': traffic_if_pos_3,
        'expected_value': round(traffic_value, 2),
        'feasibility': round(feasibility, 2),
        'time_to_rank': f"{int(time_factor)} months"
    }
```

**Scoring:** Score >100 = Excellent; 50-100 = Strong; 20-50 = Good; <20 = Marginal

### Traffic Opportunity Score (without Ahrefs)

**Score = (Volume Score × CTR Potential × Conversion Potential) / Difficulty**

- **Volume Score:** High = 10, Medium = 5, Low = 2
- **CTR Potential:** Can rank #1-3 = 10; Can rank #4-7 = 6; Can rank #8-10 = 3
- **Conversion Potential:** Transactional = 10, Commercial = 8, Informational = 5
- **Difficulty:** High = 3, Medium = 2, Low = 1

**Prioritization:** Score >200 = High; 100-200 = Medium; <100 = Low

### Keyword Priority Tiers

#### 🔴 Tier 1: Quick Wins (Next 30 Days)
- Low difficulty
- Reasonable search volume
- Clear intent match to your content
- Competitor content is weak or outdated
- **Target: 10-20 keywords**

#### 🟡 Tier 2: Strategic Targets
- Medium difficulty
- Moderate-to-high volume
- Supports business goals
- Part of topic cluster
- **Target: 20-30 keywords**

#### 🟢 Tier 3: Long-term Investments (6-12 Months)
- High difficulty but high value
- Industry-defining terms
- Large topic clusters
- **Target: 10-15 keywords**

---

## Step 10: Information Architecture Recommendations

Based on competitor content patterns, keyword clustering, and content gaps, surface IA recommendations for how the user's site should be organized.

### Navigation Structure
- Which keyword clusters should be top-level navigation items?
- Are competitors surfacing certain topics in main nav that the user has buried?
- **Recommendation**: Suggest elevating high-opportunity keyword clusters to main navigation

### URL Architecture
- Do competitors use clean, topic-based URL structures (e.g., `/guides/email-marketing/`)?
- Does the user's URL structure align with their keyword clusters?
- **Recommendation**: Suggest URL restructuring if competitors are clearly winning with semantic URL patterns

### Topic Cluster Hub Pages
- What hub pages are missing based on keyword clustering?
- Are any clusters orphaned (spoke content without a hub)?
- **Recommendation**: Identify 2-4 new hub pages to create and map which content should link to them

### Internal Linking Gaps
- Within each keyword cluster, which pages should link to each other but currently don't?
- **Recommendation**: Suggest internal linking patterns that would improve both UX and SEO

### Content Silos
- Which silos make sense for the user's keyword clusters?
- **Recommendation**: Suggest 2-3 silos to implement

### Output: Information Architecture Recommendations
Include a short section in the report (3-5 items max) titled "**Information Architecture Recommendations**" that lists:
- 1-2 navigation structure changes
- 1 hub page recommendation
- 1-2 internal linking improvements
- 1 silo structure recommendation

---

## Step 11: Generate Strategy Document

Create comprehensive keyword strategy report:

### Executive Summary
- Total keywords identified: X
- Quick win opportunities: Y
- Content gaps found: Z
- Recommended first 5 pieces of content
- **Total research cost: $—** (one line; full breakdown in Token Usage appendix at end of report)

### Prioritized Recommendations

A single consolidated table combining all keyword and IA recommendations, sorted by priority. Place this immediately after the Executive Summary so the reader sees the full action plan before diving into details.

| Priority | Type | ID | Recommendation | Difficulty | Traffic Opp | Details |
|---|---|---|---|---|---|---|
| 🚨 P0 — Immediate | IA | IA-01 | [Fix blocking technical issue] | — | Blocker | [§IA-01] |
| 🔴 1 — Quick Win | Keyword | KW-01 | [Title] | Low | [score] | [§KW-01] |
| 🟡 5 — Strategic | IA | IA-02 | [IA recommendation] | — | High | [§IA-02] |
| 🟢 15 — Long-Term | Keyword | KW-11 | [Title] | High | [score] | [§KW-11] |
| ... | | | | | | |

**Columns:**
- **Type**: `Keyword` or `IA`
- **ID**: matches the ID used in its detail section (KW-XX or IA-XX)
- **Difficulty**: Low / Medium / High / — (for IA items)
- **Traffic Opp**: numeric score from the keyword tier analysis, or — for IA items
- **Details**: link anchor to the relevant detail section

**Priority badges:**
- 🚨 P0 — Immediate blocker (must fix before anything else)
- 🔴 Quick Win — Tier 1, low difficulty, rankable in 30–90 days
- 🟡 Strategic — Tier 2 keywords + High/Medium-priority IA items
- 🟢 Long-Term — Tier 3, high difficulty, 6–12 month investment

Sort order: P0 blockers first, then Tier 1 keywords and High-priority IA items, then Tier 2 + Medium-priority IA, then Tier 3. Within each group, sort by Traffic Opp score descending.

### Competitor Analysis Summary

**For Each Competitor:**
- Domain: URL
- Overall Strategy: [Topic focus, content approach, strengths]
- Top Topics: [Main themes they cover]
- Content Strengths: [What they do well]
- Content Weaknesses: [Gaps or opportunities]
- Key Takeaways: [What to learn or do differently]

**Traffic Benchmarks (if Ahrefs available):**
- Competitor A: [traffic] visits/month, [keywords] ranking
- Competitor B: [traffic] visits/month, [keywords] ranking
- Your site: [traffic] visits/month, [keywords] ranking
- Gap to leader: [X] visits/month

### Keyword Opportunities by Tier

**What to include:**
- **All** 🔴 Tier 1 and 🟡 Tier 2 keywords — no cap, no omissions
- **Top 3** 🟢 Tier 3 keywords, selected by highest traffic opportunity score
- If more than 3 Tier 3 keywords were identified, append: `> _N additional Tier 3 keywords not listed — see Prioritized Recommendations table for full list._`

**Priority tiers:**

| Tier | Label | Include |
|---|---|---|
| 🔴 Tier 1: Quick Wins | Low difficulty; rankable within 30–90 days | All |
| 🟡 Tier 2: Strategic | Medium difficulty; supports topic clusters and business goals | All |
| 🟢 Tier 3: Long-term | High difficulty; 6–12 month investment | Top 3 |

Order within each tier by traffic opportunity score (descending). For each keyword:

- **What to do**: Specific content action (e.g., "Create comparison guide targeting '[keyword]'")
- **Why it matters**: Data-backed impact (e.g., "2,400 searches/month, difficulty 22, weak competitor content")
- **Category**: Technical SEO / Content / Information Architecture
- **Effort**: Quick (<30 min) / Moderate (1–3 hrs) / Major (4+ hrs)

**Content details** (for each keyword):
- Keyword phrase + difficulty score (Low/Medium/High, with Ahrefs score if available)
- Estimated search volume + traffic potential at #1 and #3
- Search intent: Info / Commercial / Transactional
- SERP features present: Featured snippet / AI Overview / Video / None
- Recommended content type: Guide / List / Comparison / Tool
- Recommended title
- Key points to cover
- Estimated word count
- Expected timeline to rank

### Information Architecture Recommendations

**Navigation Structure:**
- Top-level nav changes
- Buried topics that should be surfaced

**Hub & Spoke Pages:**
- New hub pages recommended
- Clusters lacking a hub that need one

**Internal Linking Strategy:**
- Links to establish between keyword-related pages
- Topic clusters that need internal linking reinforcement

**Content Silos:**
- Recommended silos based on keyword clustering

### Content Gap Analysis

**Topics You're Missing:**
1. [Topic] - Covered by: [Competitor A, B] - Priority: High/Medium/Low
2. [Topic] - Covered by: [Competitor C] - Priority: High/Medium/Low

**Topics You Can Dominate:**
1. [Topic] - Why: [Unique expertise, weak competitor content, etc.]

### Success Metrics

**Track These KPIs:**
- Organic traffic growth
- Keyword rankings (use Google Search Console)
- Content performance (pages per session, time on page)
- Conversion rate from organic traffic

**Expected Outcomes:**
- Month 1: Rank for 5-10 Tier 1 keywords
- Month 3: Rank for 10-15 Tier 1 + 5-10 Tier 2 keywords
- Month 6: Established presence in key topics, driving consistent traffic
- Month 12: Competitive visibility in all tier 3 keywords

### Implementation Checklist

**Before Creating Content:**
- [ ] Validate keyword still has weak competition
- [ ] Review top 10 results for content gaps
- [ ] Identify unique angle or value-add
- [ ] Determine optimal content format
- [ ] Plan internal linking strategy

**While Creating Content:**
- [ ] Target keyword in title, H1, H2s naturally
- [ ] Match or exceed top-ranking content depth
- [ ] Add unique value (data, examples, expertise)
- [ ] Implement technical SEO best practices
- [ ] Add relevant internal links

**After Publishing:**
- [ ] Monitor rankings (Google Search Console)
- [ ] Update based on performance
- [ ] Build internal links from new content
- [ ] Promote through available channels

### Token Usage

**Pricing reference:**
- Haiku 4.5: $0.80 / 1M input tokens, $4.00 / 1M output tokens
- Sonnet 4.6: $3.00 / 1M input tokens, $15.00 / 1M output tokens

| Model | Agent | Input Tokens | Output Tokens | Total Tokens | Est. Cost |
|-------|-------|-------------|--------------|-------------|-----------|
| claude-haiku-4-5 | Competitor: {url} | — | — | — | $— |
| claude-haiku-4-5 | Competitor: {url} | — | — | — | $— |
| claude-haiku-4-5 | Keyword research | — | — | — | $— |
| claude-sonnet-4-6 | Synthesis agent | — | — | — | $— |
| **Total** | | | | | **$—** |

Populate from the `token_usage` fields in each Haiku payload plus the Sonnet agent's self-reported usage. Est. Cost = `(input_tokens / 1,000,000 × input_rate) + (output_tokens / 1,000,000 × output_rate)`, rounded to 4 decimal places.

---

## Output Format

Provide the report in user's preferred format:
- **Markdown file** (default): Easy to reference and update
- **Spreadsheet**: Sortable keyword list with all data columns
- **Presentation**: For stakeholder buy-in
- **Combination**: Strategy doc + keyword spreadsheet

Always save to `/mnt/user-data/outputs/` and use `present_files` to share.

---

## Important Notes

### Research Limitations

**Without SEO Tools:**
- We can't get exact search volumes
- We can't see exact keyword difficulty scores
- We can't see competitor backlink profiles
- We rely on SERP analysis and observable signals

**What We CAN Do:**
- Analyze actual search results for patterns
- Identify content gaps through manual review
- Assess competition based on who's ranking
- Extract keywords from visible content
- Use Google autocomplete and related searches
- Evaluate ranking potential through SERP features

### Research Accuracy

**Be Transparent:**
- Flag when making educated guesses
- Explain reasoning for difficulty assessments
- Note when competitor data is limited
- Recommend validation steps

**Conservative Estimates:**
- Err on the side of higher difficulty
- Don't overpromise on volume estimates
- Be realistic about timelines

### User Communication

**Refer to [TONE-GUIDE.md](../TONE-GUIDE.md) for comprehensive tone and communication guidelines.**

**Explain Your Analysis:**
- Why you rated keywords as you did
- What signals you used for difficulty assessment
- How you prioritized opportunities

**Provide Context:**
- Industry-specific considerations
- Audience alignment
- Business goal fit

**Be Actionable:**
- Specific content recommendations
- Clear next steps
- Realistic timelines

---

## Example Interaction

**User:** "I run a project management SaaS. Can you analyze Asana, Monday.com, and ClickUp to find keyword opportunities for us?"

**Assistant (With Ahrefs):**

1. **Gathers information:**
   - "What's your website URL so I can do a gap analysis?"
   - "What's your target audience? (e.g., small teams, enterprises, specific industries)"
   - "Are there any specific features or use cases you want to focus on?"

2. **Launches Wave 1 — three Competitor agents in parallel:**
   - Asana agent: pulls site metrics, top 100 keywords, crawls 6 key pages
   - Monday.com agent: same
   - ClickUp agent: same

3. **Extracts keyword seeds from Wave 1 results**, launches Wave 2 Keyword Research agent with the top traffic-driving keywords as seeds

4. **Launches Sonnet agent** with all payloads — receives competitor data + keyword data

5. **Sonnet generates strategy** with precise data:
   - 65 keyword opportunities identified
   - Total potential: +45,000 monthly visits
   - Quick wins: 18 keywords (difficulty <30)
   - Token usage summary with cost breakdown

6. **Delivers report:**
   - Traffic gap analysis with actual numbers
   - Prioritized keyword list with opportunity scores
   - ROI projections based on real traffic values
   - IA recommendations and content gap analysis

**Assistant (Without Ahrefs):**
1. Asks clarifying questions
2. Launches Competitor agents that crawl pages only (no Ahrefs calls)
3. Keyword Research agent runs web SERP analysis
4. Sonnet generates strategy with proxy estimates and directional insights

---

## Edge Cases

**Scenario: User doesn't know competitors**
- Ask for keywords they want to rank for
- Search for those keywords
- Identify who's ranking as competitors
- Proceed with analysis

**Scenario: Competitors are much larger (Nike, Amazon, etc.)**
- Focus on long-tail opportunities
- Look for niche angles big brands miss
- Identify local or specific use case keywords
- Set realistic expectations about difficulty

**Scenario: Very niche industry with few competitors**
- Analyze adjacent niches
- Look at broader category leaders
- Focus more on keyword research than competitor analysis
- Identify opportunity to become category leader

**Scenario: User has no website yet**
- Skip gap analysis
- Focus purely on keyword research
- Provide content roadmap for new site
- Prioritize foundational content

**Scenario: User wants 100+ keywords**
- Explain quality > quantity
- Focus on most impactful opportunities
- Provide framework for them to continue research
- Suggest starting with 20-30 keywords to prove value

---

## Success Metrics

A successful analysis includes:
- ✅ 2-5 competitors analyzed thoroughly
- ✅ 40-60 keyword opportunities identified
- ✅ Clear prioritization with reasoning
- ✅ Specific content recommendations
- ✅ Actionable prioritized recommendations list
- ✅ Realistic difficulty and opportunity assessments
- ✅ Token usage summary with cost breakdown

---

## Integration with SEO Site Audit Skill

These skills work together:

**Workflow:**
1. Use **seo-keyword-research** to identify opportunities
2. Create content targeting those keywords
3. Use **aeo-seo-site-audit** to ensure content is optimized
4. Repeat and iterate

**Cross-references:**
- Site audit identifies current keyword targeting
- Keyword research identifies new opportunities
- Both assess content quality and structure
- Both provide prioritized action plans
