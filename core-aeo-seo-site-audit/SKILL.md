---
name: seo-aeo-site-audit
description: Crawl a set of webpages and their internal links, analyze technical SEO, content quality, and AEO (Answer Engine Optimization), then generate prioritized recommendations. Use when users want to audit their website for SEO issues, optimize for AI search engines (ChatGPT, Perplexity, Google AI Overviews), identify optimization opportunities, or get actionable advice to improve search rankings.
---

# SEO AEO Site Audit Skill

This skill performs comprehensive on-page SEO and AEO analysis by crawling specified pages and selected internal links, then generating prioritized, actionable recommendations for both traditional search engines and AI-powered answer engines. 

Note this is an on-page analysis only (not backlinks, domain authority, off-page factors).

## When to Use This Skill

Trigger this skill when the user:
- Asks to "audit my website for SEO"
- Wants to know "what's wrong with my site's SEO"
- Requests "SEO analysis" or "SEO recommendations"
- Asks "how can I improve my rankings" or "why isn't my site ranking"
- Mentions "crawl my site and analyze SEO"
- Asks about "AEO" or "Answer Engine Optimization"
- Wants to "optimize for AI search" or "ChatGPT search"
- Asks "how do I get cited by AI" or "appear in AI overviews"

## Core Workflow

1. **Gather Input** - Get target URLs and preferences from user
2. **Crawl Target Pages** - Fetch all specified URLs
3. **Extract & Parse** - Extract SEO-relevant elements from HTML
4. **Crawl Internal Links** - Selectively crawl linked pages (5-10 per target)
5. **Analyze Technical SEO** - Evaluate meta tags, headers, structure, performance
6. **Analyze Content** - Assess quality, keywords, readability, topic coverage
7. **Analyze AEO** - Evaluate optimization for AI search engines (answer formats, citations, clarity)
8. **Prioritize Issues** - Rank by impact (high/medium/low) and effort (quick win/moderate/major)
9. **Generate Report** - Create actionable recommendations document

## Environment Detection

Before starting the audit, check which tools are available and adjust accordingly:

| Environment | Tools Available | Schema Inspection | JSON-LD Extraction Method |
|---|---|---|---|
| **Claude Code** (CLI) | `Bash`, `WebFetch`, file I/O | ✅ Full | Use `curl + grep` or Python to extract from raw HTML |
| **Claude Web** | `WebFetch` only | ⚠️ Partial (stripped) | Use `strings` from curl or ask user for Rich Results Test output |

**Note:** JSON-LD extraction is NOT optional. Audits claiming "no schema found" without explicit JSON-LD extraction attempts are incomplete and inaccurate. Always verify schema presence before reporting it as missing.

## Step 1: Gather Input

Ask the user for:

**Required:**
- **Target URLs**: The main pages to analyze (homepage, key landing pages, important content)
  - If user says "my website" without URLs, ask them to provide 2-5 specific pages to start with

**Optional (ask if not clear):**
- **Crawl depth**: How many internal links to follow per page? (default: 5-10)
- **Focus areas**: "technical SEO", "content quality", "AEO", "all" (default: all)
- **Business context**: What does the site do? What keywords/topics are important?
- **AEO priority**: Is optimizing for AI search engines a priority? (helps determine report emphasis)

## Step 2: Crawl Target Pages

For each target URL:

```python
# Use web_fetch to retrieve the page
result = web_fetch(url, text_content_token_limit=50000)

# Store the full HTML and extracted text for analysis
```

**What to extract:**
- Full HTML source
- Visible text content
- Response status (200, 301, 404, etc.)
- Headers (if available)

## Step 3: Extract & Parse SEO Elements

**⚠️ CRITICAL: JSON-LD extraction is mandatory. Do not proceed without checking for schema markup on every page.**

For each crawled page, extract:

### Meta Elements
```python
# Parse from HTML:
- <title> tag
- <meta name="description"> 
- <meta name="robots">
- <meta name="viewport">
- <link rel="canonical">
- Open Graph tags: <meta property="og:*">
- Twitter Card tags: <meta name="twitter:*">
```

### Header Structure
```python
# Extract all headings:
- <h1> tags (should be exactly 1)
- <h2> through <h6> tags
- Check hierarchy: no skipping levels (H1→H2→H3, not H1→H3)
```

### Content Structure
```python
# Parse:
- Word count of main content
- Paragraph structure
- Lists (<ul>, <ol>)
- Images: <img> tags with src and alt attributes
- Links: <a> tags with href and anchor text
- Internal vs external links

### Schema.org Structured Data (CRITICAL - Always Extract)
**JSON-LD extraction is NOT optional.** All schema markup must be extracted and analyzed.

- **If `Bash` is available (Claude Code):** MUST use curl to fetch raw HTML and extract JSON-LD
  ```bash
  curl -s "https://example.com" | grep -o '<script[^>]*type="application/ld+json"[^>]*>.*</script>' | head -5
  ```
  Or use this more robust Python extraction:
  ```bash
  curl -s "https://example.com" 2>&1 | python3 << 'EOF'
  import sys, re, json
  html = sys.stdin.read()
  # Find all JSON-LD blocks
  blocks = re.findall(r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', html, re.DOTALL)
  if blocks:
    for i, block in enumerate(blocks):
      try:
        data = json.loads(block.strip())
        print(f"=== JSON-LD Block {i+1} ===")
        print(json.dumps(data, indent=2))
      except json.JSONDecodeError as e:
        print(f"Error parsing JSON-LD block {i+1}: {e}")
  else:
    print("No JSON-LD found")
  EOF
  ```

- **If only `WebFetch` is available (Claude Web):** JSON-LD is stripped during conversion. This is a significant limitation. For accurate schema analysis in web environment:
  - Use `strings` command piped to grep if bash available: `curl -s "url" 2>&1 | strings | grep -A5 "FAQPage\|Article\|Organization\|Product"`
  - Ask user to run [Google's Rich Results Test](https://search.google.com/test/rich-results) and share output
  - Note clearly in report: "⚠️ JSON-LD schema extraction not available in this environment. See appendix for manual verification steps."

**Do not report "No structured data" without explicitly attempting to extract JSON-LD first.**
```

### Internal Links for Crawling
```python
# Extract <a href="..."> where:
- href starts with "/" or contains the same domain
- Not pointing to: #anchors, mailto:, tel:, javascript:, files (.pdf, .jpg, etc.)
- Not duplicate URLs
```

## Step 4: Selective Link Crawling

For each target page, select 5-10 internal links to crawl based on priority:

**Priority 1: Navigation & Structure** (2-3 links)
- Header/footer navigation links
- Main menu items
- Breadcrumb links
- Category/section pages

**Priority 2: High-Value Content** (2-3 links)
- About page, Services/Products pages
- Popular content (if indicated by link prominence)
- Pages linked multiple times

**Priority 3: Content Diversity** (1-2 links)
- Blog posts (if site has blog)
- Different content types (product vs article vs landing page)

**Crawl Limits:**
- Maximum 10 links per target URL
- Maximum 50 total pages across entire audit
- Skip already-crawled URLs (track in a set)
- If web_fetch fails, note it and continue

For each crawled link, extract the same SEO elements as Step 3.

## Step 5: Technical SEO Analysis

Analyze all crawled pages against these criteria:

### Critical Issues (High Impact)

**Missing or Poor Title Tags**
- ❌ No title tag
- ❌ Title <30 characters or >70 characters
- ❌ Duplicate titles across pages
- ❌ Generic titles like "Home" or "Welcome"
- ✅ Good: 50-60 characters, unique, includes target keyword

**Missing or Poor Meta Descriptions**
- ❌ No meta description
- ❌ Description <120 characters or >165 characters
- ❌ Duplicate descriptions
- ✅ Good: 150-160 characters, compelling, includes keyword

**H1 Issues**
- ❌ No H1 tag
- ❌ Multiple H1 tags on same page
- ❌ H1 is generic or not descriptive
- ✅ Good: Single H1, descriptive, includes primary keyword

**Heading Hierarchy Problems**
- ❌ Skipping levels (H1 → H3, skipping H2)
- ❌ Using headings for styling instead of structure
- ✅ Good: Logical progression H1→H2→H3→H4

**Broken or Poor Internal Linking**
- ❌ Internal links with generic anchor text ("click here", "read more")
- ❌ No internal links to other important pages
- ❌ Broken internal links (404s)
- ✅ Good: Descriptive anchor text, strategic linking

### Important Issues (Medium Impact)

**Content Length**
- ⚠️ Thin content (<300 words for informational pages)
- ⚠️ Overly long without structure (>2500 words without subheadings)
- ✅ Good: Sufficient depth for topic, well-structured

**Image Optimization**
- ⚠️ Images missing alt text
- ⚠️ Alt text is generic ("image1.jpg", "photo")
- ✅ Good: Descriptive alt text for all images

**Mobile Optimization**
- ⚠️ Missing viewport meta tag
- ⚠️ Fixed-width layouts (evidence in HTML/CSS)
- ✅ Good: Responsive meta tag present

**Canonical Tags**
- ⚠️ No canonical tag (can cause duplicate content issues)
- ⚠️ Canonical pointing to wrong URL
- ✅ Good: Self-referencing canonical or correct canonical

**Structured Data (JSON-LD) — MUST ALWAYS CHECK**
- ⚠️ **No schema.org markup when appropriate** (articles, products, FAQ, local business, organization)
  - FAQ pages/Q&A content should have `FAQPage` schema
  - Articles should have `Article`, `BlogPosting`, or `NewsArticle` schema
  - Organizations should have `Organization` schema on homepage
  - Products should have `Product` schema
  - How-to content should have `HowTo` schema
  - Reviews should have `Review` or `AggregateRating` schema
- ⚠️ Incomplete or invalid schema (doesn't match content or missing required properties)
- ⚠️ Schema present but poorly structured (not extractable by AI/crawlers)
- ✅ Good: Complete, valid schema.org markup relevant to page content
- ✅ Good: Multiple relevant schema types (e.g., Article + FAQPage on a Q&A article)
- ✅ Good: Schema uses required properties (name, description, author, datePublished, etc.)

### Enhancement Opportunities (Lower Priority)

**Social Meta Tags**
- No Open Graph or Twitter Card tags (affects social sharing)
- ✅ Good: OG tags for title, description, image

**Content Readability**
- Large walls of text without breaks
- No use of lists for scannable content
- ✅ Good: Short paragraphs, bullet points, clear structure

**URL Structure** (if visible in links)
- Long, parameter-heavy URLs
- Non-descriptive URLs
- ✅ Good: Clean, descriptive URLs with keywords

**Page Performance Indicators**
- Excessive HTML size (>1MB uncompressed)
- Huge number of DOM elements (rough indicator if HTML is very large)

## Step 6: Content Quality Analysis

Evaluate content against these criteria:

### Topic Coverage & Relevance
- Does the content clearly address the page's stated topic (from title/H1)?
- Is the content comprehensive enough to answer user intent?
- Are there keyword opportunities being missed? (Look for partial mentions that could be expanded)

### Keyword Usage
- Are target keywords used naturally in:
  - Title tag
  - H1 and H2 headings
  - First paragraph
  - Throughout content (without overstuffing)
- Are related/semantic keywords present?

### Content Quality Signals
- Is content original and valuable (not generic/thin)?
- Does it provide specific information, examples, or data?
- Is there an expertise indicator (author credentials, specific details)?
- Does content match user intent (informational, commercial, transactional)?

### User Experience
- Is content scannable (headings, short paragraphs, lists)?
- Is the writing clear and accessible?
- Does it have a clear call-to-action where appropriate?

### Freshness (if date indicators present)
- Is the content dated or reference recent information?
- Are there opportunities to update with current data?

## Step 7: AEO (Answer Engine Optimization) Analysis

Evaluate content for AI search engine optimization. AEO focuses on how well content can be understood, extracted, and cited by AI systems like ChatGPT, Perplexity, Google AI Overviews, and other LLM-powered search tools.

### Direct Answer Formats

**Question-Answer Structure**
- ❌ Content doesn't answer specific questions directly
- ❌ Answers buried deep in paragraphs
- ✅ Good: Clear questions as H2/H3 headings with concise answers immediately following
- ✅ Good: FAQ sections with explicit Q&A format

**Concise Summaries**
- ❌ No summary or abstract at the beginning
- ❌ Summary is generic or vague
- ✅ Good: Executive summary or TL;DR at top of page
- ✅ Good: First paragraph directly answers the main topic question

**Definition Clarity**
- ❌ Key terms not defined
- ❌ Definitions scattered throughout text
- ✅ Good: Clear definitions early in content
- ✅ Good: Glossary or "What is X?" sections

### Content Structure for AI Extraction

**Semantic HTML & Schema (JSON-LD)**
**CRITICAL: These are the #1 issues AI systems care about. Verify schema extraction before marking as missing.**

- ❌ **No FAQ schema** for question-answer content (major AEO issue)
- ❌ **No HowTo schema** for step-by-step guides
- ❌ **Missing Article/BlogPosting schema** with author, date, and content structure
- ❌ **Missing Organization schema** on homepage
- ❌ **No BreadcrumbList schema** for navigation (helps AI understand site structure)
- ✅ Good: `FAQPage` schema with complete Q&A pairs
- ✅ Good: `HowTo` schema with `HowToStep` items clearly marked
- ✅ Good: `Article`/`BlogPosting` schema with author info and publication dates
- ✅ Good: `Organization` schema with full metadata (name, logo, contact, social profiles)
- ✅ Good: `BreadcrumbList` schema enabling navigation clarity

**List-Based Content**
- ❌ Information presented only in prose
- ❌ No use of numbered or bulleted lists
- ✅ Good: Key points in lists (top 5, best practices, steps)
- ✅ Good: Comparison tables for multiple options
- ✅ Good: Checklist format for actionable items

**Clear Hierarchy**
- ❌ Flat content structure without clear sections
- ❌ Generic headings that don't indicate content
- ✅ Good: Descriptive headings that can stand alone
- ✅ Good: Logical H2 → H3 progression with clear topics
- ✅ Good: Each section addresses one specific subtopic

### Citability & Authority

**Expertise Indicators**
- ❌ No author information
- ❌ No credentials or expertise signals
- ❌ Generic "by admin" or no attribution
- ✅ Good: Author bio with relevant credentials
- ✅ Good: "Written by [Expert Name], [Title/Credentials]"
- ✅ Good: Author schema markup

**Source Attribution**
- ❌ Claims without sources
- ❌ "Studies show" without linking to studies
- ✅ Good: Direct links to original sources
- ✅ Good: Citations for statistics and data
- ✅ Good: "According to [Source Name], ..." format

**Publish/Update Dates**
- ❌ No date information
- ❌ Only publish date, no update date
- ✅ Good: Clear publish date
- ✅ Good: "Last updated: [date]" for freshness signal
- ✅ Good: datePublished and dateModified in schema

**Unique Insights**
- ❌ Only rehashed information from other sources
- ❌ Generic advice without specifics
- ✅ Good: Original research or data
- ✅ Good: Specific examples and case studies
- ✅ Good: Expert opinion or analysis

### Natural Language Optimization

**Conversational Tone**
- ❌ Overly technical jargon without explanation
- ❌ Corporate/marketing speak
- ✅ Good: Explains concepts in plain language
- ✅ Good: Answers questions the way a human would
- ✅ Good: Uses "you" to address the reader

**Complete Sentences**
- ❌ Fragmented thoughts across paragraphs
- ❌ Missing context for standalone statements
- ✅ Good: Each sentence is self-contained
- ✅ Good: Statements include necessary context
- ✅ Good: Can extract any paragraph and it makes sense

**Topic Clustering**
- ❌ Content jumps between unrelated topics
- ❌ No clear focus or theme
- ✅ Good: Content stays focused on one main topic
- ✅ Good: Related subtopics logically connected
- ✅ Good: Internal links to related topics on separate pages

### AI-Friendly Content Patterns

**"How To" Content**
- Check for: Numbered steps, clear process, expected outcome
- ✅ Good: "How to [accomplish task]" in title/H1
- ✅ Good: Step 1, Step 2, Step 3 format
- ✅ Good: Time estimates, difficulty level, prerequisites

**Comparison Content**
- Check for: Side-by-side comparisons, pros/cons lists
- ✅ Good: "[X] vs [Y]" format in title
- ✅ Good: Comparison table with clear criteria
- ✅ Good: Summary recommendation at the end

**Definitive Guides**
- Check for: Comprehensive coverage, chapter structure
- ✅ Good: "Complete Guide to [Topic]" or "Everything You Need to Know"
- ✅ Good: Table of contents with anchor links
- ✅ Good: Multiple sections covering different aspects

**Best/Top Lists**
- Check for: Clear ranking criteria, specific recommendations
- ✅ Good: "Best [X] for [Use Case]" format
- ✅ Good: Each item has clear description and reason
- ✅ Good: Summary comparison at the end

### AEO Priority Issues

**🔴 Critical for AEO:**
- Missing FAQ schema on Q&A content
- No author information or expertise signals
- Content doesn't directly answer questions
- No clear summary or TL;DR
- Missing publish/update dates

**🟡 Important for AEO:**
- Lack of list-based content (only prose)
- Poor heading structure (not descriptive)
- No internal topic clustering
- Missing source citations
- Complex language without explanations

**🟢 Enhancement for AEO:**
- Add HowTo or comparison schema
- Improve conversational tone
- Add more specific examples
- Include relevant statistics/data
- Optimize for featured snippet formats

## Step 8: Prioritize Issues

Group all identified issues into three priority tiers:

### 🔴 High Priority (Quick Wins + High Impact)
Issues that are easy to fix and have significant SEO/AEO impact:
- Missing title tags or meta descriptions
- Missing or multiple H1 tags
- Missing image alt text on key pages
- Broken heading hierarchy
- **AEO:** No FAQ schema on Q&A content
- **AEO:** Missing author information/expertise signals
- **AEO:** No publish or update dates
- **AEO:** Content doesn't directly answer questions

### 🟡 Medium Priority (Important but More Effort)
Issues that require moderate work but improve SEO/AEO:
- Thin content that needs expansion
- Missing canonical tags
- Poor internal linking structure
- Missing structured data
- Non-optimized content (keyword opportunities)
- **AEO:** No list-based content (only prose)
- **AEO:** Generic/non-descriptive headings
- **AEO:** Missing source citations
- **AEO:** Poor topic clustering
- **AEO:** Complex language without explanations

### 🟢 Low Priority (Enhancements)
Nice-to-have improvements:
- Missing social meta tags
- URL structure improvements
- Content readability enhancements
- Minor mobile optimization tweaks
- **AEO:** Add HowTo or comparison schema
- **AEO:** Improve conversational tone
- **AEO:** Add more specific examples and data

For each issue, include:
- **What's wrong**: Clear description of the problem
- **Why it matters**: SEO/AEO impact explanation
- **How to fix**: Specific, actionable steps
- **Affected pages**: List of URLs with this issue
- **Estimated effort**: Quick (<30 min), Moderate (1-3 hours), Major (>3 hours)

## Step 9: Generate Report

Create a well-structured document (markdown or docx) with:

### Executive Summary
- **Tone:** Analytical and data-driven (see [TONE-GUIDE.md](../TONE-GUIDE.md) for detailed tone guidelines)
- Total pages analyzed (target + crawled)
- Overall SEO health score (based on issues found) - state as metric, not value judgment
- Top 3-5 critical issues to fix first - order by measurable impact and effort
- Estimated improvement potential - use conservative projections with data sources

### Detailed Findings

**Writing style guidelines for all findings sections:** See [TONE-GUIDE.md](../TONE-GUIDE.md) for detailed style guidelines. Key principles:
- State issues factually without editorial language
- Explain mechanism of impact, not opinion
- Use metrics to convey severity, not emotional language
- Quantify specificity: "7 of 10 pages" not "most pages"

#### Technical SEO Issues
For each category (Meta Tags, Headings, Links, Images, etc.):
- List of issues found
- Affected pages (with counts: X of Y total)
- Priority level (based on measured impact)
- Recommended fix with realistic effort estimate

#### Content Quality Issues
- Pages with thin/weak content
- Keyword optimization opportunities
- Content structure improvements
- User experience enhancements

#### AEO (Answer Engine Optimization) Issues
- Direct answer format opportunities
- Missing FAQ/HowTo schema
- Authority and citability improvements
- AI-friendly content structure gaps
- Natural language optimization needs

### Prioritized Recommendations

**Writing style for recommendations:** See [TONE-GUIDE.md](../TONE-GUIDE.md) for detailed style guidelines. Key principles:
- Use neutral language without dramatic framing
- Quantify impact with specific data
- Avoid vague benefits (no "better SEO" without specifics)
- Explain mechanisms and provide realistic effort estimates

A single ranked list of all issues and improvements, ordered by impact and effort. Each item includes:
- Issue description and affected pages (with counts)
- Why it matters with specific mechanism (SEO/AEO impact with data)
- Specific fix steps
- Estimated effort (Quick / Moderate / Major) with hour range
- Expected outcome (with confidence level if uncertain)

### Page-by-Page Breakdown
For each analyzed page:
- URL
- Current issues (prioritized)
- Recommended changes
- Current vs recommended title/description examples

### Appendix
- Full list of crawled URLs
- Technical details (response codes, page sizes if notable)
- Glossary of SEO and AEO terms used

**Key Terms:**
- **SEO (Search Engine Optimization)**: Optimizing content for traditional search engines like Google
- **AEO (Answer Engine Optimization)**: Optimizing content for AI-powered search and answer engines like ChatGPT, Perplexity, Google AI Overviews
- **FAQ Schema**: Structured data markup that helps AI systems identify and extract question-answer pairs
- **HowTo Schema**: Structured data for step-by-step instructions that AI can easily parse
- **Citability**: How easily AI systems can extract and attribute information from your content
- **Direct Answer Format**: Content structure that provides immediate, clear answers to questions

## Output Format

Provide the report in the user's preferred format:
- **Markdown file** (default): For easy viewing and editing
- **Word document**: For formal presentation or sharing
- **Spreadsheet**: For tracking fixes (URLs in rows, issues in columns)

Always save the final report to `/mnt/user-data/outputs/` and use the `present_files` tool to share it with the user.

## Important Notes

### Crawling Etiquette
- Respect web_fetch rate limits
- If a page fails to load, note it and continue
- Don't crawl the same URL twice

### Schema Inspection Limitations & Requirements
**This is critical to audit accuracy. Do not skip.**

- **Claude Code** (Recommended): Full schema inspection via `curl`
  - MUST use bash to extract JSON-LD on every page before analyzing
  - Example: `curl -s "url" 2>&1 | grep -o '<script type="application/ld+json">.*</script>'`
  - Extract and parse all JSON-LD blocks
  - Verify schema type matches content (FAQ schema for FAQs, Article schema for articles, etc.)
  - Report specific schema findings, not "no schema"

- **Claude Web**: Schema markup is NOT visible via `WebFetch` due to HTML stripping
  - This is a significant limitation — JSON-LD extraction is impossible in web environment
  - When running in Claude Web:
    - ⚠️ Note prominently: "Schema analysis unavailable in this environment"
    - Ask the user to run [Google's Rich Results Test](https://search.google.com/test/rich-results) and paste the output
    - OR ask user to run: `curl -s "https://yoursite.com" | grep "application/ld+json" -A 20`
    - Do NOT report "no schema found" — report "schema verification pending"
    - Recommend the user re-run the audit in Claude Code for accurate schema analysis
    - Flag any AEO recommendations as conditional on schema verification

### Analysis Accuracy
- Base recommendations on what's visible in the HTML/content
- Flag uncertainties (e.g., "This page may have JavaScript-rendered content not visible in the HTML")
- Don't make assumptions about backend or server-side issues

### User Communication
**Refer to [TONE-GUIDE.md](../TONE-GUIDE.md) for comprehensive tone and communication guidelines.**

Key principles:
- Use neutral, analytical language
- Focus on data and metrics rather than subjective praise
- Avoid promotional or enthusiastic framing
- Explain SEO and AEO terms in plain language
- Provide context for why each issue matters with data

### Scope Management
- If user wants to analyze >20 target pages, suggest breaking into batches
- If crawling discovers major issues, offer to stop and report early
- Remind user this is on-page SEO and AEO analysis only (not backlinks, domain authority, off-page factors)
- AEO analysis focuses on content optimization for AI systems; actual AI search ranking factors may vary

## Example Interaction

**User:** "Can you audit my website's SEO? Here's my homepage: example.com"

**Assistant:** 
1. Asks for clarification: "I'll analyze your homepage and crawl some internal links. A few questions:
   - Are there specific pages you want me to focus on (like key landing pages or product pages)?
   - What does your business do? Any specific keywords you're targeting?
   - Should I look at technical SEO, content quality, AEO, or all of them?
   - Is optimizing for AI search engines (ChatGPT, Perplexity, etc.) a priority?"

2. Gets user input, then:
   - Crawls the homepage
   - Extracts SEO elements
   - Selects 5-10 internal links to crawl
   - Analyzes all pages (technical SEO, content, AEO)
   - Generates prioritized recommendations
   - Creates a report document
   - Shares the report with specific next steps
   - Generates prioritized recommendations
   - Creates a report document
   - Shares the report with specific next steps

**User:** "Just analyze my homepage for now, focus on technical issues."

**Assistant:**
1. Crawls homepage only (no internal links)
2. Performs technical SEO analysis
3. Generates focused technical report with quick fixes
4. Presents findings and asks if user wants full site analysis next

**User:** "I want to optimize my blog for ChatGPT and AI search. Can you audit it?"

**Assistant:**
1. Clarifies: "I'll focus on AEO (Answer Engine Optimization) for your blog. I'll check:
   - How well your content answers questions directly
   - FAQ schema and other structured data for AI
   - Author credibility signals
   - Content structure for AI extraction
   Should I also check traditional SEO, or just focus on AEO?"
2. Crawls blog homepage and several posts
3. Analyzes AEO factors: direct answers, schema, citability, natural language
4. Generates report with AEO-specific recommendations
5. Provides examples of how to restructure content for AI search

## Success Metrics

A successful audit includes:
- ✅ All specified URLs successfully crawled
- ✅ Clear identification of high-priority issues
- ✅ Specific, actionable recommendations (not generic advice)
- ✅ Realistic effort estimates for each fix
- ✅ Well-organized report the user can act on immediately

## Edge Cases

**Scenario: JavaScript-heavy site**
- Note that analysis is limited to server-rendered HTML
- Recommend using browser tools to check client-rendered content
- Flag this limitation in the report

**Scenario: Large e-commerce site**
- Focus on representative pages (homepage, category, product pages)
- Note that patterns may repeat across similar pages
- Suggest systematic fixes rather than page-by-page

**Scenario: All pages look good**
- Still provide the report with confirmations
- Suggest next-level optimizations (schema enhancements, content expansion)
- Recommend competitive analysis as next step

**Scenario: User asks for competitor comparison**
- Note this is out of scope for this skill
- Offer to analyze competitor sites separately
- Suggest the user create a separate competitive analysis skill or use web search
