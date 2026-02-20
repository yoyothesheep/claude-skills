---
name: core-seo-keyword-research
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

**With Ahrefs MCP (Recommended):**
1. **Gather Input** - Get target URLs and preferences from user
2. **Get Ahrefs Baseline** - Fetch current traffic & keyword metrics
3. **Analyze Competitor Keywords** - Use site-explorer-organic-keywords
4. **Crawl for Content Context** - Fetch pages to understand strategy
5. **Research Keywords** - Use keywords-explorer for precise data
6. **Calculate Traffic Potential** - Use Ahrefs volume + clicks data
7. **Evaluate with Difficulty Scores** - Use Ahrefs KD + your DR
8. **Prioritize by Opportunity Score** - Data-driven ranking
9. **Generate Strategy** - Create actionable keyword targeting plan

**Without Ahrefs (Fallback):**
1. **Gather Input** - Get target URLs and preferences from user
2. **Crawl Target Pages** - Fetch all specified URLs
3. **Analyze Competitor Content** - Extract topics, keywords, content types
4. **Identify Content Patterns** - Find what's working for competitors
5. **Perform Gap Analysis** - Compare user's site to competitors
6. **Research Keywords via Web Search** - Manual SERP analysis
7. **Evaluate with Proxy Signals** - Estimate difficulty & volume
8. **Prioritize Keywords** - Rank by quick wins, strategic value
9. **Generate Strategy** - Create actionable keyword targeting plan

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

## Step 1.5: Use Ahrefs for Competitor Traffic Analysis

**If Ahrefs is available**, get baseline metrics for user's site and competitors:

### Get Your Site's Metrics

```python
# Get overall organic performance
user_metrics = AHREFs.site_explorer_metrics(
    target="user-domain.com",
    mode="subdomains",
    date="2026-02-08",  # Use current date
    country="US",  # Or user's target country
    volume_mode="monthly"
)

# Extract key data:
# - org_traffic: Current monthly organic traffic
# - org_keywords: Total keywords ranking
# - org_keywords_1_3: Keywords in top 3
# - org_cost: Estimated traffic value
```

### Get Competitor Metrics

```python
competitor_data = []

for competitor_url in competitor_urls:
    metrics = AHREFs.site_explorer_metrics(
        target=competitor_url,
        mode="subdomains",
        date="2026-02-08",
        country="US",
        volume_mode="monthly"
    )
    
    competitor_data.append({
        'url': competitor_url,
        'traffic': metrics['org_traffic'],
        'keywords': metrics['org_keywords'],
        'top_3_keywords': metrics['org_keywords_1_3'],
        'traffic_value': metrics['org_cost']
    })

# This gives you exact competitive benchmarks:
# - Who has the most traffic
# - Traffic gap to close
# - Market size opportunity
```

### Get Competitor's Top Keywords

```python
# For each competitor, get their highest-traffic keywords
competitor_keywords = AHREFs.site_explorer_organic_keywords(
    target=competitor_url,
    mode="subdomains",
    date="2026-02-08",
    country="US",
    select="keyword,best_position,sum_traffic,volume,keyword_difficulty,serp_features",
    order_by="sum_traffic:desc",
    limit=100,  # Top 100 keywords
    volume_mode="monthly"
)

# Store for gap analysis:
# - Keywords they rank for
# - Traffic each keyword brings
# - Position they hold
# - Keyword difficulty
# - SERP features present
```

**Data to Track:**
- User's current traffic: [X] visits/month
- Competitor A traffic: [Y] visits/month (gap: Y-X)
- Competitor B traffic: [Z] visits/month (gap: Z-X)
- Total market opportunity: Sum of all competitor traffic
- Your market share: X / (X+Y+Z+...)

## Step 2: Crawl Competitor Sites

For each competitor, fetch key pages:

### Priority Page Types:
1. **Homepage** - Overall positioning and main topics
2. **Blog/Resources** - Content strategy and topics
3. **Top-level category pages** - Information architecture
4. **High-traffic pages** (if identifiable from structure/links)

### Crawling Strategy:
```python
# For each competitor:
# 1. Fetch homepage
competitor_home = web_fetch(competitor_url)

# 2. Extract and prioritize internal links
# Focus on:
# - /blog/ or /resources/ or /learn/
# - Main navigation links
# - Category/topic pages
# - Service/product pages

# 3. Crawl 5-8 key pages per competitor
# Total: ~30-40 pages across all competitors
```

**What to extract:**
- Page titles and meta descriptions
- Heading structure (H1, H2, H3)
- Main topics and themes
- Content length and depth
- Internal linking patterns
- Content types (guides, tutorials, comparisons, lists)
- Calls-to-action and conversion focus

## Step 3: Analyze Competitor Content

For each competitor, identify:

### Content Strategy Patterns

**Topic Coverage:**
- What main topics do they cover?
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
- Average word count
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

## Step 4: Identify Content Patterns

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

## Step 5: Perform Gap Analysis

Compare user's site to competitors:

### Content Gaps:
- **Topics competitors cover that you don't**: Defensive opportunities (prevent losing traffic)
- **Topics you cover that competitors don't**: Offensive opportunities (unique positioning)
- **Depth gaps**: Topics where competitors have more comprehensive coverage
- **Format gaps**: Content types competitors use that you don't

### Keyword Gaps (Initial):
Based on visible content, identify:
- Keywords likely targeted by competitors (from titles, headings, content)
- Keywords you're probably missing
- Keyword themes competitors prioritize

### Quality Gaps:
- Where competitors have stronger content
- Where you have stronger content
- Opportunities to create definitive resources

### Competitive Traffic Estimation:

For each competitor, estimate their organic traffic potential:

**Traffic Indicators to Observe:**
1. **Content Freshness:**
   - Recently updated (within 3 months) = likely getting traffic
   - Old dates (2+ years) with no updates = declining or low traffic
   
2. **Engagement Signals:**
   - High comment count = active traffic
   - Social share counts (if visible)
   - Author engagement in comments
   
3. **Content Depth:**
   - 3,000+ word comprehensive guides = likely ranking for multiple keywords
   - Thin content (500 words) = likely limited traffic
   
4. **Internal Linking:**
   - Linked from homepage or main nav = priority page (likely high traffic)
   - Buried deep in site = lower priority (likely low traffic)
   
5. **Backlink Quality (Observable):**
   - Mentioned in major publications = high authority = more traffic
   - Only links from small/unknown sites = lower authority

**Estimate Competitor Traffic Share:**

For each major keyword theme:
- **Competitor A ranks #1-3 for 20 related keywords** → Estimate 10,000-50,000 monthly visits
- **Competitor B ranks #4-7 for 15 keywords** → Estimate 3,000-15,000 monthly visits  
- **Competitor C ranks #8-10 for 10 keywords** → Estimate 1,000-5,000 monthly visits

**Your Opportunity:**
- **Currently rank for 5 keywords** → Current traffic: ~2,000 visits/month
- **Gap:** 15 keywords Competitor A has that you don't
- **Potential gain:** +8,000-25,000 visits/month if you capture these

**Traffic Gap Priority:**
- Focus on keywords where Competitor A gets traffic but you rank #11-20 (quick wins)
- Target keywords where NO competitor dominates (blue ocean)
- Avoid keywords where Competitor has strong #1 position (harder to displace)

## Step 6: Research Keywords with Ahrefs

**If Ahrefs is available**, use it for precise keyword data:

### Method 1: Get Keyword Metrics for Identified Keywords

```python
# Take the keywords identified from competitor analysis
keyword_list = [
    "email marketing automation",
    "best email marketing software",
    "klaviyo vs mailchimp",
    # ... other keywords from content analysis
]

# Get exact metrics from Ahrefs
keyword_data = AHREFs.keywords_explorer_overview(
    keywords=",".join(keyword_list),
    country="US",
    select="keyword,volume,difficulty,cpc,traffic_potential,clicks,cps,serp_features,intents"
)

# For each keyword, you now have:
# - volume: Exact monthly search volume
# - difficulty: Keyword difficulty (0-100)
# - traffic_potential: Traffic the #1 page gets from ALL keywords
# - clicks: Average monthly clicks
# - cps: Clicks per search ratio
# - serp_features: Array of SERP features (ai_overview, snippet, etc.)
# - intents: {informational, commercial, transactional, navigational}
```

### Method 2: Find Related Keywords

```python
# For each main topic, find related keyword opportunities
related = AHREFs.keywords_explorer_related_terms(
    keywords="email marketing automation",
    country="US",
    select="keyword,volume,difficulty,traffic_potential",
    order_by="traffic_potential:desc",
    limit=50,
    where='{"and": [{"field": "difficulty", "is": ["lte", 30]}]}'  # Low difficulty only
)

# This finds:
# - "Also rank for" keywords (related terms)
# - "Also talk about" keywords (semantic keywords)
# - Filtered by low difficulty for quick wins
```

### Method 3: Search Suggestions

```python
# Get autocomplete-style keyword ideas
suggestions = AHREFs.keywords_explorer_search_suggestions(
    keywords="email marketing",
    country="US",
    select="keyword,volume,difficulty,traffic_potential",
    order_by="volume:desc",
    limit=100
)

# Returns questions and phrases people actually search for
```

### Method 4: Matching Terms (Pattern-Based)

```python
# Find all keywords matching a pattern
matches = AHREFs.keywords_explorer_matching_terms(
    terms="email marketing,email automation",
    country="US",
    match_mode="any",  # Match any of the terms
    select="keyword,volume,difficulty,clicks,traffic_potential,serp_features",
    where='{"and": [{"field": "volume", "is": ["gte", 100]}]}',  # Min 100 searches/month
    order_by="traffic_potential:desc",
    limit=200
)

# Great for finding long-tail variations
```

### Keyword Data Enrichment

For each keyword, Ahrefs provides:

**Volume & Traffic:**
- `volume`: Monthly search volume
- `clicks`: Average clicks per month
- `cps`: Clicks per search (how many results get clicked)
- `traffic_potential`: Traffic the #1 page gets from all its keywords

**Difficulty:**
- `difficulty`: 0-100 score (0=easiest, 100=hardest)
- Interpretation:
  - 0-10: Very easy
  - 11-30: Easy
  - 31-50: Medium  
  - 51-70: Hard
  - 71-100: Very hard

**Intent:**
- `intents.informational`: Boolean
- `intents.commercial`: Boolean
- `intents.transactional`: Boolean
- `intents.navigational`: Boolean
- `intents.branded`: Boolean
- `intents.local`: Boolean

**SERP Features:**
- `serp_features`: Array of features present
  - "ai_overview": AI Overview (SGE)
  - "snippet": Featured snippet
  - "local_pack": Local 3-pack
  - "video": Video carousel
  - "image": Image pack
  - "shopping": Shopping results
  - "question": People Also Ask
  - And many more...

**Monetization:**
- `cpc`: Cost per click in USD cents (commercial intent indicator)

### Calculate Actual Traffic Potential

With Ahrefs data, calculate precise traffic estimates:

```python
def calculate_traffic_potential(keyword_data, target_position):
    """
    Calculate expected monthly traffic for a keyword at a given position.
    
    Args:
        keyword_data: Dict with 'volume', 'clicks', 'serp_features'
        target_position: 1-10
    
    Returns:
        Estimated monthly visits
    """
    volume = keyword_data['volume']
    clicks = keyword_data['clicks']
    serp_features = keyword_data.get('serp_features', [])
    
    # Base CTR by position
    ctr_by_position = {
        1: 0.316,  # 31.6% for position 1
        2: 0.159,
        3: 0.108,
        4: 0.073,
        5: 0.055,
        6: 0.044,
        7: 0.037,
        8: 0.031,
        9: 0.027,
        10: 0.024
    }
    
    base_ctr = ctr_by_position.get(target_position, 0.01)
    
    # Adjust for SERP features
    if 'ai_overview' in serp_features:
        base_ctr *= 0.6  # 40% CTR reduction for AI Overview
    if 'snippet' in serp_features and target_position > 1:
        base_ctr *= 0.8  # 20% reduction if snippet present and not position 1
    if 'local_pack' in serp_features:
        base_ctr *= 0.5  # 50% reduction for local pack
    if len([f for f in serp_features if f.startswith('paid_')]) >= 3:
        base_ctr *= 0.7  # 30% reduction for heavy ads
    
    # Use clicks data if available (more accurate than volume × CTR)
    if clicks and clicks > 0:
        # Distribute clicks by position
        traffic = clicks * (base_ctr / sum(ctr_by_position.values()))
    else:
        # Fallback to volume-based calculation
        traffic = volume * base_ctr
    
    return int(traffic)

# Example usage:
keyword_data = {
    'keyword': 'email marketing automation',
    'volume': 5000,
    'clicks': 2500,
    'serp_features': ['ai_overview', 'snippet']
}

position_1_traffic = calculate_traffic_potential(keyword_data, 1)
position_3_traffic = calculate_traffic_potential(keyword_data, 3)
position_5_traffic = calculate_traffic_potential(keyword_data, 5)

print(f"Position 1: {position_1_traffic} visits/month")
print(f"Position 3: {position_3_traffic} visits/month")
print(f"Position 5: {position_5_traffic} visits/month")
```

## Step 6 (Fallback): Research Keywords Without Ahrefs

Use web search to validate and expand keyword opportunities:

### Search Strategy:

**For Each Topic/Theme Identified:**

1. **Search for the main topic keyword**
   - Example: "content marketing"
   - Extract: Related searches, "People also ask" questions, autocomplete suggestions

2. **Search for "best [topic]" variations**
   - Example: "best content marketing strategies"
   - Extract: What types of content rank (lists, guides, comparisons)

3. **Search for "how to [topic]" variations**
   - Example: "how to create content marketing strategy"
   - Extract: Question-based keywords, informational intent

4. **Search for "[topic] vs" or "[topic] alternatives"**
   - Example: "HubSpot vs Mailchimp"
   - Extract: Comparison keywords, competitor terms

5. **Search for "[topic] for [audience]"**
   - Example: "content marketing for B2B SaaS"
   - Extract: Audience-specific keywords

### Keyword Data to Extract:

From SERP analysis:
- **Top-ranking content types**: Lists, guides, tools, comparisons
- **Title patterns**: Common formats that rank
- **Content depth**: Average word count of top results
- **Featured snippets**: What format triggers them
- **"People Also Ask"**: Related question keywords
- **Related searches**: Semantic keyword variations

### Document for Each Keyword:
- Keyword phrase
- Search intent (informational, commercial, transactional, navigational)
- Estimated competition level (based on who ranks: big brands, exact-match domains, comprehensive content)
- Top-ranking content types
- Opportunity signals (gaps, weak competition, emerging topic)

## Step 7: Evaluate Ranking Potential with Ahrefs

**With Ahrefs data**, ranking potential assessment is precise:

### Difficulty Assessment (Ahrefs-Powered)

Use the `difficulty` score from Keywords Explorer:

**Very Easy (0-10):**
- Can rank with minimal effort
- Low-authority sites ranking
- Thin content in top 10
- **Action:** Target immediately

**Easy (11-30):**
- Can rank with quality content
- Mix of authority and smaller sites
- Good quick win candidates
- **Action:** Target in first 30 days

**Medium (31-50):**
- Need strong content + some links
- Established sites ranking but not giants
- **Action:** Build comprehensive content

**Hard (51-70):**
- Need excellent content + solid backlinks
- Strong brands in top 10
- 6-12 month targets
- **Action:** Long-term investment

**Very Hard (71-100):**
- Dominated by major brands
- Extensive backlinks required
- 12+ month targets
- **Action:** Consider alternatives or long-term strategy

### Actual Traffic Potential (Ahrefs Data)

Use the traffic calculation from Step 6:

```python
# For each keyword in your list:
for kw in keywords:
    ahrefs_data = get_keyword_data(kw['keyword'])
    
    kw['volume'] = ahrefs_data['volume']
    kw['difficulty'] = ahrefs_data['difficulty']
    kw['traffic_potential'] = ahrefs_data['traffic_potential']
    kw['serp_features'] = ahrefs_data['serp_features']
    
    # Calculate what YOU could get at different positions
    kw['traffic_if_pos_1'] = calculate_traffic_potential(ahrefs_data, 1)
    kw['traffic_if_pos_3'] = calculate_traffic_potential(ahrefs_data, 3)
    kw['traffic_if_pos_5'] = calculate_traffic_potential(ahrefs_data, 5)
    
    # Realistic position based on difficulty
    if kw['difficulty'] <= 30:
        kw['realistic_position'] = 3  # Can reach top 3
        kw['expected_traffic'] = kw['traffic_if_pos_3']
    elif kw['difficulty'] <= 50:
        kw['realistic_position'] = 5  # Top 5 achievable
        kw['expected_traffic'] = kw['traffic_if_pos_5']
    else:
        kw['realistic_position'] = 8  # Top 10
        kw['expected_traffic'] = calculate_traffic_potential(ahrefs_data, 8)
```

### Competitive Traffic Gap Analysis

**Compare against competitors:**

```python
# For each keyword:
competitor_rankings = AHREFs.serp_overview(
    keyword=keyword,
    country="US",
    select="url,position,traffic,domain_rating,backlinks"
)

# Analyze the gap:
for result in competitor_rankings:
    if result['url'].contains(competitor_domain):
        competitor_traffic = result['traffic']
        competitor_position = result['position']
        competitor_DR = result['domain_rating']
        
        # Your opportunity if you outrank them
        your_potential = calculate_traffic_potential(keyword_data, competitor_position)
        
        traffic_gap = your_potential  # What you could gain
```

### Traffic Opportunity Score (Ahrefs Version)

**Improved scoring with actual data:**

```python
def calculate_opportunity_score(keyword_data, your_domain_rating):
    """
    Score = (Traffic Potential × Feasibility) / (Difficulty × Time Factor)
    
    Where:
    - Traffic Potential = Expected traffic at realistic position
    - Feasibility = How likely you are to rank (based on DR gap)
    - Difficulty = Ahrefs KD score
    - Time Factor = How long it will take
    """
    
    volume = keyword_data['volume']
    difficulty = keyword_data['difficulty']
    traffic_if_pos_3 = keyword_data['traffic_if_pos_3']
    cpc = keyword_data.get('cpc', 0) / 100  # Convert cents to dollars
    
    # Intent multiplier (commercial intent = higher value)
    intent_multiplier = 1.0
    if keyword_data['intents'].get('transactional'):
        intent_multiplier = 2.0
    elif keyword_data['intents'].get('commercial'):
        intent_multiplier = 1.5
    
    # Feasibility based on your DR vs ranking difficulty
    # If you have DR 50 and keyword needs DR 40, feasibility = high
    feasibility = max(0.1, (your_domain_rating - difficulty) / 100 + 0.5)
    
    # Time factor (higher difficulty = longer time = lower score)
    if difficulty <= 30:
        time_factor = 1.0  # 1 month
    elif difficulty <= 50:
        time_factor = 3.0  # 3 months
    elif difficulty <= 70:
        time_factor = 6.0  # 6 months
    else:
        time_factor = 12.0  # 12 months
    
    # Calculate score
    traffic_value = traffic_if_pos_3 * (cpc if cpc > 0 else 2)  # $2/visit default
    score = (traffic_value * feasibility * intent_multiplier) / (difficulty * time_factor)
    
    return {
        'score': round(score, 2),
        'expected_traffic': traffic_if_pos_3,
        'expected_value': round(traffic_value, 2),
        'feasibility': round(feasibility, 2),
        'time_to_rank': f"{int(time_factor)} months"
    }

# Example:
your_DR = 45  # Get from site-explorer-metrics

for kw in keywords:
    kw['opportunity'] = calculate_opportunity_score(kw, your_DR)
    
# Sort by opportunity score
keywords.sort(key=lambda x: x['opportunity']['score'], reverse=True)
```

**Scoring Interpretation:**
- Score >100 = Excellent opportunity (pursue immediately)
- Score 50-100 = Strong opportunity (strategic priority)
- Score 20-50 = Good opportunity (long-term)
- Score <20 = Marginal opportunity (skip or deprioritize)

## Step 7 (Fallback): Evaluate Ranking Potential Without Ahrefs

For each identified keyword, assess:

### Difficulty Assessment (Without Tools):

**High Difficulty Indicators:**
- Top 10 dominated by major brands (Forbes, HubSpot, Shopify, etc.)
- Extremely comprehensive content (5,000+ words)
- Many strong backlinks visible in SERPs (articles from authority sites)
- Highly commercial intent with ad-heavy SERPs
- Exact-match domains in top positions

**Medium Difficulty Indicators:**
- Mix of big brands and smaller/niche sites
- Moderate content depth (1,500-3,000 words)
- Mix of content types (not all lists or all guides)
- Some older content (opportunity to update)
- Geographic or niche modifiers in query

**Low Difficulty Indicators:**
- Small/niche sites ranking well
- Thin or outdated content in top 10
- Forum posts or Q&A sites ranking (Reddit, Quora)
- Few branded results
- Very specific long-tail queries
- Newer or emerging topics

### Search Volume Proxy (Without Tools):

**High Volume Signals:**
- Autocomplete suggestions appear early
- Many related searches
- "People Also Ask" section present
- Ads present (commercial intent)
- Big brands competing

**Medium Volume Signals:**
- Some autocomplete suggestions
- Moderate related searches
- Mix of commercial and informational

**Low Volume Signals:**
- Very specific/long-tail
- Few related searches
- No ads
- Niche or technical terminology

### Traffic Potential Estimation

Since we don't have exact search volume data, estimate potential traffic using these methods:

#### Method 1: CTR-Based Traffic Modeling

**Average Organic CTR by Position (Industry Benchmarks):**
- Position 1: 28-35% CTR
- Position 2: 15-20% CTR
- Position 3: 10-12% CTR
- Position 4-5: 6-8% CTR
- Position 6-10: 3-5% CTR

**Traffic Estimation Formula:**
```
Estimated Monthly Visits = (Estimated Search Volume) × (CTR for Target Position)
```

**Volume Estimation Without Tools:**
- **High Volume:** 10,000-100,000+ searches/month
  - Position 1: 2,800-35,000 visits/month
  - Position 3: 1,000-12,000 visits/month
  - Position 5: 600-7,000 visits/month
  
- **Medium Volume:** 1,000-10,000 searches/month
  - Position 1: 280-3,500 visits/month
  - Position 3: 100-1,200 visits/month
  - Position 5: 60-700 visits/month
  
- **Low Volume:** 100-1,000 searches/month
  - Position 1: 28-350 visits/month
  - Position 3: 10-120 visits/month
  - Position 5: 6-70 visits/month

**Adjustments for SERP Features:**
- **Featured Snippet present:** Reduce CTR by 10-15% for position 1-3
- **AI Overview present:** Reduce CTR by 30-40% for all positions
- **Multiple ads (3+):** Reduce CTR by 20-30% for all positions
- **Video carousel:** Reduce CTR by 10-20% depending on position
- **Local pack:** Reduce CTR by 30-50% for non-local results

#### Method 2: Comparative Traffic Analysis

**Estimate competitor traffic:**
1. Identify who ranks in positions 1-5
2. Look for traffic indicators:
   - Social shares (if visible on page)
   - Comment count on blog posts
   - Freshness (recently updated = likely getting traffic)
   - Number of backlinks (more backlinks = more authority = more traffic)
3. Make conservative estimates

**Traffic Benchmarking:**
- If small blog ranks #1 → keyword likely gets 100-500 visits/month
- If medium site ranks #1 → keyword likely gets 500-2,000 visits/month
- If major brand ranks #1 → keyword likely gets 2,000-50,000+ visits/month

#### Method 3: Market Sizing Approach

**Bottom-Up Estimation:**
1. Count number of "People Also Ask" questions (more = higher volume)
2. Count related searches (8-10 = high interest)
3. Check if autocomplete appears after 2-3 characters (yes = higher volume)
4. Note number of ads (3+ ads = commercial + volume)
5. Combine signals into volume estimate

**Example:**
- Keyword: "email marketing automation"
- 8 "People Also Ask" questions ✓
- 10 related searches ✓
- Autocomplete after 3 chars ✓
- 4 ads present ✓
- **Estimate:** High volume (10,000-50,000/month)
- **Position 3 traffic potential:** ~1,500-6,000 visits/month

#### Method 4: Traffic Opportunity Score

Combine multiple factors into single score:

**Traffic Opportunity Score = (Volume Score × CTR Potential × Conversion Potential) / Difficulty**

Where:
- **Volume Score:** High = 10, Medium = 5, Low = 2
- **CTR Potential:** Based on realistic ranking position (1-10)
  - Can rank #1-3 = 10
  - Can rank #4-7 = 6
  - Can rank #8-10 = 3
- **Conversion Potential:** Based on intent
  - Transactional = 10
  - Commercial = 8
  - Informational = 5
  - Navigational = 2
- **Difficulty:** High = 3, Medium = 2, Low = 1

**Example Calculation:**
- Keyword: "best project management software"
- Volume: High (10)
- Can rank #5 with effort (6)
- Commercial intent (8)
- Medium difficulty (2)
- **Score:** (10 × 6 × 8) / 2 = 240

**Prioritization:**
- Score >200 = High Priority
- Score 100-200 = Medium Priority
- Score <100 = Low Priority

### Intent Analysis:

**Informational:**
- "how to", "what is", "guide to", "learn"
- Top content: Guides, tutorials, definitions
- User goal: Learn or understand

**Commercial Investigation:**
- "best", "top", "vs", "review", "comparison"
- Top content: Lists, reviews, comparisons
- User goal: Research before purchase

**Transactional:**
- "buy", "price", "discount", "deal"
- Top content: Product pages, pricing pages
- User goal: Make a purchase

**Navigational:**
- Brand names, specific products
- Top content: Official pages
- User goal: Find specific site

### Opportunity Scoring:

**Quick Win (High Priority):**
- Low-medium difficulty + Medium-high volume + Matches your expertise
- Informational intent + You can create definitive content
- Competitors have thin content + You can do better
- Long-tail variation + Specific to your niche

**Strategic (Medium Priority):**
- Medium difficulty + High volume + Important to your business
- Commercial intent + Aligns with your products/services
- Topic cluster opportunity + Supports other content

**Long-term (Lower Priority):**
- High difficulty + High volume + Worth the investment
- Brand-building topics
- Industry-defining terms

## Step 8: Prioritize Keywords

Group keywords into tiers:

### 🎯 Tier 1: Quick Wins (Target First - Next 30 Days)

**Criteria:**
- Low difficulty
- Reasonable search volume (even if small)
- Clear intent match to your content
- Competitor content is weak or outdated
- You have unique expertise or angle

**Target: 10-20 keywords**

**Example Keywords:**
- "[specific tool] tutorial for [niche]"
- "how to [specific task] in [your industry]"
- "[problem] solution for [specific audience]"

### 🎯 Tier 2: Strategic Targets

**Criteria:**
- Medium difficulty
- Moderate-to-high volume
- Supports business goals
- Part of topic cluster
- Competitors cover but you can do better

**Target: 20-30 keywords**

**Example Keywords:**
- "best [solution] for [use case]"
- "[topic] guide for beginners"
- "[tool A] vs [tool B]"

### 🎯 Tier 3: Long-term Investments (6-12 Months)

**Criteria:**
- High difficulty but high value
- Industry-defining terms
- Large topic clusters
- Competitive but important

**Target: 10-15 keywords**

**Example Keywords:**
- "[industry term]"
- "what is [major topic]"
- "best [product category]"

### Content Gap Priorities:

**Critical Gaps (Must-Have Content):**
- Topics all competitors cover that you don't
- Questions your audience asks that you haven't answered
- Comparison content featuring your competitors

**Opportunity Gaps (Differentiation):**
- Topics one competitor does well but others ignore
- Unique angles no one is taking
- Emerging trends competitors haven't covered yet

## Step 9: Information Architecture Recommendations

Based on competitor content patterns, keyword clustering analysis, and content gaps, surface information architecture (IA) recommendations. These are structural/navigation improvements to how the user's site should be organized.

### Navigation Structure
- Which keyword clusters should be top-level navigation items?
- Are competitors surfacing certain topics in main nav that the user has buried?
- What topics are overshadowed by less-important content in the user's current hierarchy?
- **Recommendation**: Suggest elevating high-opportunity keyword clusters to main navigation based on search volume and user demand

### URL Architecture
- Do competitors use clean, topic-based URL structures (e.g., `/guides/email-marketing/`)?
- Are the user's URLs descriptive and hierarchical, or parameter-heavy?
- Does the user's URL structure align with their keyword clusters?
- **Recommendation**: Suggest URL restructuring if competitors are clearly winning with semantic URL patterns

### Topic Cluster Hub Pages
- Based on keyword clustering (from Step 8 grouping), what hub pages are missing?
- Are there strong clusters of 5-10 related keywords that should be unified under a hub/pillar page?
- Are any clusters orphaned (spoke content without a hub)?
- **Recommendation**: Identify 2-4 new hub pages to create and map which content should link to them

### Internal Linking Gaps
- Within each keyword cluster, which pages should link to each other but currently don't?
- Are there natural topic relationships competitors are leveraging that the user hasn't connected?
- **Recommendation**: Suggest internal linking patterns that would improve both UX and SEO (e.g., "all [Tier 1 keywords] should link to [hub page]")

### Content Silos
- Would grouping content into topical silos improve both rankings and user navigation?
- Which silos make sense for the user's keyword clusters?
- **Recommendation**: Suggest 2-3 silos to implement (e.g., "Beginner Guides" silo, "Comparisons" silo, "Advanced Strategies" silo)

### Output: Information Architecture Recommendations
Include a short section in the report (3-5 items max) titled "**Information Architecture Recommendations**" that lists:
- 1-2 navigation structure changes (e.g., "Elevate 'Email Automation' to main nav; rank-driving cluster with 15+ keywords")
- 1 hub page recommendation (e.g., "Create hub page for '[Topic]' cluster with 12 related keywords")
- 1-2 internal linking improvements (e.g., "Link all 'Best Tool' articles to main '[Tool Category]' comparison page")
- 1 silo structure recommendation (e.g., "Create 'Beginner Guides' silo for Tier 1 quick-win keywords")

---

## Step 10: Generate Strategy Document

Create comprehensive keyword strategy report:

### Executive Summary
- Total keywords identified: X
- Quick win opportunities: Y
- Content gaps found: Z
- Recommended first 5 pieces of content
- Estimated timeline to execute

### Competitor Analysis Summary

**For Each Competitor:**
- Domain: URL
- Overall Strategy: [Topic focus, content approach, strengths]
- Top Topics: [Main themes they cover]
- Content Strengths: [What they do well]
- Content Weaknesses: [Gaps or opportunities]
- Key Takeaways: [What to learn or do differently]

### Keyword Opportunities by Tier

**Tier 1: Quick Wins**
For each keyword:
- Keyword phrase
- Estimated difficulty: Low/Medium/High
- Estimated search volume: Low (100-1K) / Medium (1K-10K) / High (10K+)
- **Traffic potential if ranking #3:** [Specific monthly visit estimate]
- **Traffic potential if ranking #1:** [Specific monthly visit estimate]
- **Current ranking:** [If applicable, otherwise "Not ranking"]
- Search intent: Info/Commercial/Transactional
- SERP features: Featured snippet / AI Overview / Video / None
- Why it's a quick win: [Specific reasoning]
- **Traffic opportunity score:** [Number based on formula]
- Recommended content type: Guide/List/Comparison/Tool
- Recommended title: [Specific title suggestion]
- Key points to cover: [Bullet list]
- Estimated word count: [Based on top-ranking content]
- **Expected timeline to rank:** [30 days / 60 days / 90 days]

**Tier 2: Strategic Targets**
(Same format as Tier 1)

**Tier 3: Long-term Investments**
(Same format, with timeline notes)

### Traffic Potential Summary

**Current State:**
- Total estimated monthly organic traffic: [Number]
- Top 10 traffic-driving keywords: [List with estimates]
- Untapped potential: [Number] (keywords ranking #11-20)

**Opportunity Analysis:**
- **Quick Wins (Tier 1):** +[X] monthly visits potential
- **Strategic (Tier 2):** +[Y] monthly visits potential  
- **Long-term (Tier 3):** +[Z] monthly visits potential
- **Total Opportunity:** +[X+Y+Z] monthly visits (+[%] increase)

**Competitive Traffic Benchmarks:**
- Competitor A estimated traffic: [Number] visits/month
- Competitor B estimated traffic: [Number] visits/month
- Your current estimated traffic: [Number] visits/month
- **Gap to leader:** [Number] visits/month ([%] difference)
- **Achievable in 6 months:** [Number] visits/month

**ROI Projection:**
- Estimated traffic value @ $2/visit: $[Number]/month
- Content investment: [Number of articles] × $[Cost per article]
- **Estimated ROI:** [X]% in 6 months

### Information Architecture Recommendations

**Navigation Structure:**
- Top-level nav changes (e.g., "Elevate '[Topic Cluster]' to main nav based on 15+ ranking keywords")
- Buried topics that should be surfaced (e.g., "Move '[Topic]' from deep in site hierarchy to secondary nav")

**Hub & Spoke Pages:**
- New hub pages recommended (e.g., "Create hub page for '[Cluster Name]' to link 12 related spoke pages")
- Clusters lacking a hub that need one

**Internal Linking Strategy:**
- Links to establish between keyword-related pages (e.g., "All '[Type A]' pages should link to '[Hub]' page")
- Topic clusters that need internal linking reinforcement

**Content Silos:**
- Recommended silos based on keyword clustering (e.g., "Create 'Beginner Guides' silo for Tier 1 keywords")
- Pages that should be reorganized into silos

### Content Gap Analysis

**Topics You're Missing:**
1. [Topic] - Covered by: [Competitor A, B] - Priority: High/Medium/Low
2. [Topic] - Covered by: [Competitor C] - Priority: High/Medium/Low

**Topics You Can Dominate:**
1. [Topic] - Why: [Unique expertise, weak competitor content, etc.]
2. [Topic] - Why: [Reasoning]

### Competitive Positioning Recommendations

**Your Unique Angle:**
- What makes your content different from competitors
- Topics where you have unique expertise
- Angles competitors aren't taking

**Content Format Recommendations:**
- Formats competitors use successfully (replicate)
- Formats missing from the space (innovate)
- Formats that match your strengths

**Internal Linking Strategy:**
- Topic cluster recommendations
- Hub pages to create
- Spoke content to support

### Success Metrics

**Track These KPIs:**
- Organic traffic growth
- Keyword rankings (use free tools like Google Search Console)
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

## Output Format

Provide the report in user's preferred format:
- **Markdown file** (default): Easy to reference and update
- **Spreadsheet**: Sortable keyword list with all data columns
- **Presentation**: For stakeholder buy-in
- **Combination**: Strategy doc + keyword spreadsheet

Always save to `/mnt/user-data/outputs/` and use `present_files` to share.

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

## Example Interaction

**User:** "I run a project management SaaS. Can you analyze Asana, Monday.com, and ClickUp to find keyword opportunities for us?"

**Assistant (With Ahrefs):**

1. **Gathers information:**
   - "What's your website URL so I can do a gap analysis?"
   - "What's your target audience? (e.g., small teams, enterprises, specific industries)"
   - "Are there any specific features or use cases you want to focus on?"

2. **Gets Ahrefs baseline data:**
   ```python
   # Your site
   your_metrics = AHREFs.site_explorer_metrics(
       target="yourpm.com",
       mode="subdomains",
       date="2026-02-08",
       country="US"
   )
   # Result: 5,000 monthly visits, 1,200 keywords
   
   # Competitors
   asana_metrics = AHREFs.site_explorer_metrics(target="asana.com", ...)
   # Result: 850,000 monthly visits, 125,000 keywords
   
   monday_metrics = AHREFs.site_explorer_metrics(target="monday.com", ...)
   # Result: 620,000 monthly visits, 98,000 keywords
   ```

3. **Analyzes competitor keywords:**
   ```python
   asana_keywords = AHREFs.site_explorer_organic_keywords(
       target="asana.com",
       mode="subdomains",
       date="2026-02-08",
       country="US",
       select="keyword,best_position,sum_traffic,volume,keyword_difficulty",
       order_by="sum_traffic:desc",
       limit=500
   )
   # Identifies top traffic-driving keywords
   ```

4. **Finds keyword opportunities:**
   ```python
   # Related keywords for "project management"
   opportunities = AHREFs.keywords_explorer_related_terms(
       keywords="project management software",
       country="US",
       select="keyword,volume,difficulty,traffic_potential,clicks",
       where='{"and": [{"field": "difficulty", "is": ["lte", 40]}]}',
       order_by="traffic_potential:desc",
       limit=100
   )
   ```

5. **Generates strategy with precise data:**
   - 65 keyword opportunities identified
   - Total potential: +45,000 monthly visits
   - Quick wins: 18 keywords (difficulty <30)
   - Each keyword has:
     * Exact search volume
     * Precise difficulty score
     * Expected traffic at positions 1, 3, 5
     * Current competitor positions
     * SERP features present
   
6. **Delivers report:**
   - Traffic gap analysis with actual numbers
   - Prioritized keyword list with opportunity scores
   - ROI projections based on real traffic values

**Assistant (Without Ahrefs):**
1. Asks clarifying questions:
   - "What's your website URL so I can do a gap analysis?"
   - "What's your target audience? (e.g., small teams, enterprises, specific industries)"
   - "Are there any specific features or use cases you want to focus on?"

2. Crawls competitor sites:
   - Fetches homepages and blog/resource sections
   - Analyzes 5-8 pages per competitor
   - Extracts topics, content types, keyword patterns

3. Performs analysis:
   - Identifies common themes (workflows, collaboration, productivity)
   - Finds content gaps (specific use cases competitors miss)
   - Researches keywords via web search
   - Evaluates difficulty and opportunity

4. Generates strategy:
   - 50+ keyword opportunities across 3 tiers
   - Prioritized recommendations list
   - Specific recommendations for differentiation
   - Quick wins to target first

5. Delivers report with specific next steps

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

## Success Metrics

A successful analysis includes:
- ✅ 2-5 competitors analyzed thoroughly
- ✅ 40-60 keyword opportunities identified
- ✅ Clear prioritization with reasoning
- ✅ Specific content recommendations
- ✅ Actionable prioritized recommendations list
- ✅ Realistic difficulty and opportunity assessments

## Integration with SEO Site Audit Skill

These skills work together:

**Workflow:**
1. Use **core-seo-keyword-research** to identify opportunities
2. Create content targeting those keywords
3. Use **core-aeo-seo-site-audit** to ensure content is optimized
4. Repeat and iterate

**Cross-references:**
- Site audit identifies current keyword targeting
- Keyword research identifies new opportunities
- Both assess content quality and structure
- Both provide prioritized action plans
