---
name: aeo-seo-site-audit
description: Analyze webpages for content quality, schema markup completeness, and AEO (Answer Engine Optimization). Designed to complement Ahrefs Site Audit findings.
---

# AEO & Content Analysis Skill (Ahrefs Complement)

This skill analyzes content quality, JSON-LD schema validation, and AEO (Answer Engine Optimization) for pages you specify. It complements Ahrefs Site Audit (which handles technical SEO) by focusing on aspects that require content analysis and AI-readiness assessment.

**Use this skill when Ahrefs Site Audit cannot:**
- Validate JSON-LD schema completeness and correctness
- Assess content quality and depth
- Evaluate how well pages answer user questions directly
- Identify authority/expertise signals
- Recommend AI-friendly content restructuring
- Assess natural language optimization
- Flag citability gaps

## When to Use This Skill

Trigger this skill when the user:
- Has run an Ahrefs Site Audit and wants to go deeper on content
- Asks "why isn't my content ranking for [query]?"
- Wants to "optimize for AI search" or "ChatGPT search"
- Asks "how do I get cited by AI" or "appear in AI overviews"
- Wants to "improve schema markup for content types"
- Asks "how can I make my content more AI-friendly?"
- Wants "content quality analysis" beyond technical SEO

## Core Workflow

1. **Gather Input** - Get target URLs, Ahrefs project ID (optional), and business context
2. **Fetch Ahrefs Audit Issues** (if project ID provided) - Pull technical audit findings via Ahrefs API
3. **Crawl Target Pages & Extract JSON-LD** - Fetch URLs (Bash curl or WebFetch), extract schema in ONE pass
4. **Parse Content & Validate Schema** - Extract content elements, validate schema completeness and accuracy
5. **Content Quality Analysis** - Assess content depth, structure, direct answer formats
6. **Authority & Citability Assessment** - Evaluate expertise signals, source attribution, date freshness
7. **AI-Friendly Patterns** - Identify missing FAQ, HowTo, comparison schemas and content structures
8. **Natural Language Optimization** - Check conversational tone, clarity, extractability
9. **Prioritize Content Gaps** - Rank recommendations by AEO impact and effort
10. **Generate Augmented Report** - Create report integrating Ahrefs findings + content analysis

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
- **Target URLs**: The pages to analyze (homepage, key landing pages, important content)
  - If user says "my website" without URLs, ask them to provide 2-5 specific pages to start with

**Optional:**
- **Ahrefs Project ID** (recommended): If you have Ahrefs Site Audit set up, provide the project ID
  - Skill will automatically fetch technical audit findings (titles, H1s, broken links, crawl issues, etc.)
  - Report combines Ahrefs technical findings + this skill's content/AEO analysis
  - No need to manually export/attach CSV—we pull directly from Ahrefs API
- **Business context**: What does the site do? What keywords/topics matter most?
- **Content goals**: Are you targeting AI search engines (ChatGPT, Perplexity, AI Overviews)?
- **Current pain points**: "Content not ranking well" / "Low AI citations" / "Thin content" etc.

**Note:** This skill complements Ahrefs Site Audit (which checks titles, meta descriptions, H1 tags, broken links, etc.). Focus here is content depth, schema, and AEO.

## Step 2: Fetch Ahrefs Audit Issues (Optional)

If user provided an Ahrefs project ID, pull technical audit findings:

```python
# Use Ahrefs MCP to fetch Site Audit issues
ahrefs_issues = site_audit_issues(
    project_id=user_project_id,
    date=None  # Get latest crawl
)

# Parse issues by type:
# - Title/meta description issues
# - H1/heading hierarchy issues
# - Broken links
# - Mobile optimization issues
# - Crawlability issues
# Store for reference in final report
```

**If user doesn't have Ahrefs project ID:**
- Skip this step
- Continue with content-only analysis
- Report will focus on content gaps and schema without technical SEO context

---

## Step 3: Crawl Target Pages & Extract JSON-LD

**⚠️ CRITICAL: JSON-LD extraction is mandatory on every page. Do ONE fetch per URL (not two) to ensure efficiency.**

For each target URL:

### Environment Detection & Fetch Strategy

Before fetching, detect which tools are available:

- **Claude Code (Bash available):** Use `curl` to fetch raw HTML, extract JSON-LD immediately
- **Claude Web (WebFetch only):** Use `web_fetch`, JSON-LD will be stripped during conversion

### Fetch & Extract Implementation

**If `Bash` is available (Claude Code):**
```bash
curl -s "https://example.com" 2>&1 | python3 << 'EOF'
import sys, re, json
html = sys.stdin.read()
# Find all JSON-LD blocks
blocks = re.findall(r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', html, re.DOTALL)
extracted_jsonld = []
if blocks:
  for i, block in enumerate(blocks):
    try:
      data = json.loads(block.strip())
      extracted_jsonld.append(data)
      print(f"=== JSON-LD Block {i+1} ===")
      print(json.dumps(data, indent=2))
    except json.JSONDecodeError as e:
      print(f"Error parsing JSON-LD block {i+1}: {e}")
else:
  print("No JSON-LD found")
EOF
```

**Store for Step 4:**
- Full HTML from curl response
- Extracted JSON-LD blocks (parsed into dictionary/list)
- Page response status and headers

**If only `WebFetch` is available (Claude Web):**
```python
result = web_fetch(url, text_content_token_limit=50000)
# Note: JSON-LD is stripped during conversion. Store HTML as-is.
# Extracted schema will be empty; will note limitation in report.
```

**Store for Step 4:**
- Visible text content from web_fetch
- Empty JSON-LD blocks (or ask user to provide schema via Google Rich Results Test)
- Page metadata

### Extract Internal Links from Stored HTML

```python
# From stored HTML, extract <a href="..."> where:
- href starts with "/" or contains the same domain
- Not pointing to: #anchors, mailto:, tel:, javascript:, files (.pdf, .jpg, etc.)
- Not duplicate URLs
# Store for optional content sampling (Step 5)
```

## Step 4: Parse Content & Validate Schema

For each crawled page (using stored HTML from Step 3):

### Content Elements (for AEO analysis)
```python
# Parse from stored HTML:
- Total word count of main content
- Paragraph structure and sentence complexity
- Lists (<ul>, <ol>) and tables
- Presence of FAQ sections, direct answers to questions
- Formatting: bold, code blocks, callouts
- Links: internal links, citation links, source attribution
- Images: presence of descriptive captions
```

### Authority & Freshness Signals
```python
# Look for in stored HTML:
- Author information (name, title, credentials)
- Publication date (<meta name="article:published_time"> or datePublished in schema)
- Last updated date (dateModified or "Updated:" text)
- Organization/author credentials or bio
- External citations and source links
```

### Schema.org Structured Data Validation

**Using JSON-LD extracted in Step 3:**
- Validate schema structure and completeness
- Check if schema type matches content type (FAQPage for FAQs, Article for blog posts, etc.)
- Identify missing required fields (author, datePublished, answer properties, etc.)
- Flag schema that doesn't match visible content

**Do not validate "no schema found" without Step 3 extraction attempt.**

## Step 5: Optional Content Sampling

If user wants broader content analysis, optionally crawl 3-5 related pages to assess content patterns:

**When to sample related pages:**
- User wants to understand content quality across site
- Site has multiple content types (blog posts, product pages, guide pages)
- Ahrefs report shows consistent issues across pages

**Sample selection:**
- Different content types (if applicable): blog post, product page, guide, FAQ
- Representative pages that user mentions as important
- Pages that should have schema but might be missing it

**Crawl Limits:**
- Maximum 5 additional pages (beyond specified target URLs)
- If fetch fails, note and continue
- Skip if user only wants analysis of specific URLs

**For each sampled page:** Use Step 3 methodology (environment-aware fetch + JSON-LD extraction, store HTML for parsing in Step 4).

## Step 5: Schema Markup & Structure Validation

Analyze all crawled pages for JSON-LD completeness and AEO readiness:

### Schema Validation (HIGH PRIORITY)

**Missing Schema for Content Type:**
- ❌ FAQ/Q&A content with no `FAQPage` schema
- ❌ Articles with no `Article` or `BlogPosting` schema
- ❌ How-to content with no `HowTo` schema
- ❌ Product pages with no `Product` schema
- ❌ Organization pages with no `Organization` schema
- ❌ Reviews with no `Review` or `AggregateRating` schema
- ✅ Good: Schema matches content type with all required properties

**Incomplete Schema:**
- ❌ `FAQPage` present but missing author, datePublished, or mainEntity
- ❌ `Article` missing datePublished or author information
- ❌ Schema properties incomplete or marked with placeholder values
- ✅ Good: Schema has all required fields + recommended fields (author, date, description)

**Schema Quality:**
- ❌ Schema doesn't match visible content (e.g., FAQPage claims 10 Q&As but page shows 3)
- ❌ Nested schema incorrectly structured (e.g., Answer not properly nested in Question)
- ✅ Good: Schema structure is valid and matches content accurately

### Content Structure for AI (MEDIUM PRIORITY)

**Direct Answer Formats:**
- ❌ Content doesn't answer main question in first paragraph
- ❌ Answers buried in prose; no clear Q&A or summary
- ✅ Good: First sentence answers the question; FAQ/TL;DR at top

**Scannable Formatting:**
- ❌ Content is all prose; no lists, tables, or visual breaks
- ❌ No numbered steps for how-to content
- ✅ Good: Bulleted lists, comparison tables, numbered steps, short paragraphs

**Topic Coherence:**
- ❌ Content jumps between unrelated subtopics
- ❌ Sections don't connect logically
- ✅ Good: Clear section topics; content flows logically; related pages linked

## Step 6: Content Quality and Structure (SEO and AEO)

Evaluate all content for SEO quality and AEO (Answer Engine Optimization)—how well it serves both traditional search engines and AI systems like ChatGPT, Perplexity, and Google AI Overviews.

### Topic Coverage & Clarity

**User Intent & Comprehensiveness**
- ❌ Content doesn't clearly address the stated topic (from title/H1)
- ❌ Content is too shallow for user intent
- ✅ Good: Comprehensive coverage matching search intent
- ✅ Good: First paragraph directly answers the main question

**Direct Answer Formats (AEO Priority)**
- ❌ Content doesn't answer specific questions directly; answers buried in prose
- ❌ No summary or abstract at the beginning
- ✅ Good: Clear questions as H2/H3 headings with immediate answers
- ✅ Good: Executive summary or TL;DR at top; definitions early in content
- ✅ Good: FAQ sections with explicit Q&A format

### Keyword & Semantic Usage

**Keyword Placement**
- ❌ Target keywords missing or poorly placed
- ✅ Good: Keywords naturally used in title, H1, H2s, and first paragraph
- ✅ Good: Related/semantic keywords present throughout

**Content Originality & Specificity**
- ❌ Generic, thin content; only rehashed information
- ✅ Good: Original research, specific examples, data, or expert analysis
- ✅ Good: Matches user intent (informational vs. commercial vs. transactional)

### Content Structure & Scannability

**Heading Hierarchy & Descriptiveness**
- ❌ Flat structure, generic headings, skipped heading levels
- ✅ Good: Descriptive headings that can stand alone; logical H2 → H3 progression
- ✅ Good: Each section addresses one clear subtopic

**List-Based & Semantic Structure (AEO Priority)**
- ❌ Information only in prose; no lists, comparisons, or checklists
- ❌ Content jumps between unrelated topics
- ✅ Good: Key points in numbered/bulleted lists; comparison tables; checklists
- ✅ Good: Content stays focused; related subtopics logically connected
- ✅ Good: Short paragraphs with varied formatting for scannability

**Schema Markup for AI Extraction (CRITICAL)**
**These are the #1 issues AI systems care about. Verify schema extraction before marking as missing.**

- ❌ **No FAQ schema** on Q&A content (major AEO issue)
- ❌ **No HowTo schema** for step-by-step guides
- ❌ **Missing Article/BlogPosting schema** with author, date, and structure
- ❌ **Missing Organization schema** on homepage
- ❌ **No BreadcrumbList schema** for navigation
- ✅ Good: `FAQPage` schema with complete Q&A pairs
- ✅ Good: `HowTo` schema with `HowToStep` items
- ✅ Good: `Article`/`BlogPosting` with author info and publication dates
- ✅ Good: `Organization`, `BreadcrumbList`, or other relevant schema types

### Authority & Citability (AEO Priority)

**Expertise & Author Signals**
- ❌ No author information, credentials, or expertise signals
- ✅ Good: Author bio with relevant credentials; "Written by [Name], [Title]"
- ✅ Good: Author schema markup

**Source Attribution & Evidence**
- ❌ Claims without sources or supporting links
- ✅ Good: Direct links to original sources and citations
- ✅ Good: "According to [Source], ..." format; statistics and data attributed

**Freshness Indicators**
- ❌ No date information; outdated without update signals
- ✅ Good: Clear publish date and "Last updated: [date]" for freshness
- ✅ Good: datePublished and dateModified in schema; references recent information

### Natural Language Optimization (AEO Priority)

**Conversational & Accessible Language**
- ❌ Overly technical jargon, corporate speak, or fragmented sentences
- ✅ Good: Explains concepts in plain language; answers like a human would
- ✅ Good: Complete sentences with necessary context; can extract any paragraph and it makes sense
- ✅ Good: Uses "you" to address the reader; includes clear definitions

**Topic Coherence**
- ❌ Content jumps between unrelated topics; no clear focus
- ✅ Good: Each section connects logically to others
- ✅ Good: Internal links to related topics on separate pages

### Content Patterns for AI (AEO Priority)

Identify and optimize for AI-friendly formats:

- **How-To Content**: "How to [task]" format, numbered steps, time estimates, prerequisites
- **Comparison Content**: "[X] vs [Y]" titles, side-by-side tables, pros/cons, clear recommendation
- **Definitive Guides**: "Complete Guide" or "Everything You Need to Know" format, table of contents, multi-section coverage
- **Best/Top Lists**: "Best [X] for [Use Case]" format, clear ranking criteria, descriptions with reasoning

### Priority Summary

| Priority | Issue | Impact |
|----------|-------|--------|
| 🔴 Critical | Missing FAQ/HowTo schema on relevant content | Prevents AI extraction; major ranking loss for AEO |
| 🔴 Critical | No author info/expertise signals | Reduces citability; AI systems deprioritize unsourced content |
| 🔴 Critical | Content doesn't directly answer questions | Users and AI skip the page |
| 🔴 Critical | Missing publish/update dates | AI views content as stale |
| 🟡 Important | Only prose (no lists/tables/structure) | Harder for AI to extract; poor scannability |
| 🟡 Important | Generic/non-descriptive headings | AI can't understand section topics |
| 🟡 Important | Missing source citations | Reduces authority; AI won't cite |
| 🟡 Important | Complex language without explanations | Users bounce; AI struggles to extract meaning |
| 🟢 Enhancement | Add comparison/HowTo schema | Improves featured snippets and AI citations |
| 🟢 Enhancement | Improve conversational tone | Increases engagement and AI relevance |
| 🟢 Enhancement | Add specific examples and data | Supports claim substantiation for AI search |

## Step 7: Authority & Citability Assessment

Evaluate how well pages establish expertise and enable AI systems to cite the content.

### Author Credibility Signals

**Observable signals:**
- ❌ No author information on any page
- ❌ Author listed but no credentials, title, or bio
- ❌ No author schema markup (Author property in schema)
- ✅ Good: Author name + title/credentials visible; Author schema present

**Impact on AEO:** AI systems check author credibility before citing. Missing author signals = low citability.

### Source Attribution & Citations

**Observable signals:**
- ❌ Claims made without sources or supporting links
- ❌ Statistics cited without attribution ("trusted data" but no link to source)
- ❌ No distinction between original data and curated information
- ✅ Good: Direct links to sources; "According to [Source]" format; statistics attributed
- ✅ Good: Original research/data clearly marked; methodology explained

**Impact on AEO:** AI systems prioritize citing well-sourced content. Direct links increase citability.

### Freshness Indicators

**Observable signals:**
- ❌ No publication or update date visible
- ❌ Outdated information without update signals
- ❌ No datePublished or dateModified in schema
- ✅ Good: Clear "Published [date]" and "Updated [date]" visible
- ✅ Good: datePublished and dateModified in schema; content references recent data

**Impact on AEO:** AI systems deprioritize stale content. Dates signal ongoing relevance.

### Expertise Depth

**Observable signals:**
- ❌ Shallow coverage; content could be written by anyone
- ❌ No evidence of specialized knowledge or experience
- ⚠️ Good domain knowledge but not explicitly stated
- ✅ Good: Domain expertise evident (specific examples, methodology, credentials)
- ✅ Good: Depth of coverage exceeds surface-level information

---

## Step 8: Prioritize Content & AEO Gaps

Group all identified issues into three priority tiers:

### 🔴 High Priority (Critical for AEO)

Issues that significantly impact AI citability and content quality:
- **Missing schema for content type** (e.g., no FAQPage on FAQ content, no Article on blog posts)
- **No author/expertise signals** (missing author name, credentials, or author schema)
- **Content doesn't directly answer main question** (answer buried in prose)
- **Missing publication date** (no datePublished in schema or visible date)
- **Incomplete schema** (FAQPage present but missing required fields like author, question, answer)

### 🟡 Medium Priority (Improves AEO)

Issues that enhance content quality and extractability:
- **Thin content** (<300 words for informational pages; missing depth vs competitors)
- **No source citations** (claims made without supporting links or attribution)
- **Only prose formatting** (no lists, tables, or scannable structure for how-to/comparison content)
- **Missing dateModified** (no update signal for content refresh)
- **Poor topic structure** (content jumps between topics; sections not logically connected)
- **Complex language** (jargon-heavy without explanations; not conversational)

### 🟢 Low Priority (Enhancements)

Nice-to-have improvements:
- **Add comparison/HowTo schema** (improves featured snippets and AI citations)
- **Improve conversational tone** (makes content more readable and extractable)
- **Add specific examples and data** (supports claim substantiation for AI search)
- **Internal linking to related topics** (improves content coherence and crawlability)

For each issue, include:
- **What's wrong**: Clear description (e.g., "FAQ schema incomplete—missing 'answer' field in Q&A pairs")
- **Why it matters**: Specific AEO impact (e.g., "AI systems can't extract answers without complete schema")
- **How to fix**: Specific steps (e.g., "Add 'answer' property to each Q&A item in FAQPage schema")
- **Affected pages**: URLs with this issue
- **Estimated effort**: Quick (<30 min), Moderate (1-3 hours), Major (4+ hours)

## Step 9: Generate Content & AEO Report

Create a well-structured document (markdown or docx) with:

### Executive Summary
- **Tone:** Analytical and data-driven (see [TONE-GUIDE.md](../TONE-GUIDE.md))
- Total pages analyzed
- Summary of Ahrefs findings (if available): "Ahrefs identified X technical issues across Y pages"
- Overall AEO readiness score (based on schema, content, authority signals)
- Top 3-5 critical gaps (prioritized by AEO impact and effort)
- Estimated improvement: "With these changes, content will be 40-50% more extractable by AI systems"

### Detailed Findings

**Writing style guidelines:** See [TONE-GUIDE.md](../TONE-GUIDE.md). Key principles:
- State issues factually without editorializing
- Explain specific mechanism of impact
- Use metrics: "3 of 11 pages" not "some pages"
- Distinguish between content quality and schema completeness

#### Schema Markup Gaps
For each page/content type:
- Missing or incomplete schema (e.g., "FAQPage present but 3 of 10 Q&As missing 'answer' field")
- Affected pages (X of Y total)
- Impact on AEO (e.g., "AI systems can't cite answers without complete schema")
- Specific fix (e.g., "Add 'answer' property to all Question items")

#### Content Quality Issues
- Thin content vs competitors (word count, depth analysis)
- Direct answer format gaps (where content buries answers in prose)
- Scannable formatting (lack of lists, tables, sections for how-to/comparison content)
- Authority signal gaps (missing author info, credentials, source citations)
- Freshness signals (missing publication/update dates)

#### AI-Friendly Content Structure Gaps
- Missing FAQ sections on Q&A content
- How-to content without numbered steps or schema
- Comparison content without tables or pros/cons
- General content lacking topic coherence and internal linking

#### Natural Language Optimization
- Complex jargon without explanations
- Conversational tone assessment (readable for AI extraction)
- Paragraph-level extractability (can AI extract any paragraph and understand it alone?)

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

### Integration with Ahrefs

**If user provides Ahrefs Project ID:**
- Call `site_audit_issues(project_id=...)` to fetch technical audit findings
- Reference findings in report: "Ahrefs identified X pages with missing meta descriptions"
- Build upon them: "This analysis focuses on why content may not rank despite correct metadata"
- Combine results: Ahrefs technical issues + content/AEO gaps in single report

**If user provides no Ahrefs data:**
- Proceed with content-only analysis
- Flag in report that technical SEO was not assessed
- Focus entirely on content quality, schema, authority, and AEO readiness

### JSON-LD Extraction (CRITICAL)

**This is the core of this audit. Do not skip schema extraction.**

- **Claude Code** (Required for accurate schema analysis):
  - MUST use bash to extract JSON-LD on every page
  - Use robust Python extraction to parse and validate schema
  - Extract all `<script type="application/ld+json">` blocks
  - Validate: Schema type matches content type (FAQPage for FAQs, Article for blog posts, etc.)
  - Report specific findings: "FAQPage present but 'author' field missing" (not just "has FAQ schema")

- **Claude Web**: Schema markup is stripped during conversion
  - Not suitable for accurate schema analysis
  - Ask user to run [Google's Rich Results Test](https://search.google.com/test/rich-results) and share output
  - OR ask user for bash output: `curl -s "https://yoursite.com" | grep "application/ld+json" -A 30`
  - Flag report: "⚠️ Schema analysis conducted via user-provided JSON-LD output"

### Analysis Boundaries

**This skill focuses on:**
- Content quality & depth
- Schema completeness & validity
- Authority & citability signals
- AEO-friendly content structure

**This skill assumes Ahrefs has checked:**
- Title tags, meta descriptions
- H1 tags, heading hierarchy
- Broken links, 404s
- Mobile optimization
- Crawlability issues

### Content Assessment Notes
- Compare content depth vs top-ranking competitors (note: requires separate research or user context)
- Flag "thin content" only if visibly <300 words for informational pages
- Assess readability for AI extraction (not readability score, but extractability)
- Don't assume technical implementation limits (e.g., "content is JS-rendered" — flag for verification)

### User Communication
**Refer to [TONE-GUIDE.md](../TONE-GUIDE.md) for tone guidelines.**

### Scope Management
- Focus on 5-20 target pages; break larger sites into batches
- This analysis is content & AEO focused (not technical SEO, backlinks, or domain metrics)
- Actual AI search ranking factors may differ from this optimization framework

## Example Interaction

**User:** "I have Ahrefs Site Audit set up. Can you analyze my content and schema?"

**Assistant:**
1. Asks: "Perfect! A few quick questions:
   - What's your Ahrefs project ID? (I can pull your audit findings automatically)
   - What are the main pages you want me to focus on (homepage, key landing pages)?
   - What does your site do? (This helps me assess if schema choices match content types)
   - Are you primarily targeting AI search engines (ChatGPT, Perplexity, etc.)?

2. Upon receiving project ID and URLs:
   - Calls Ahrefs API to fetch technical issues (titles, H1s, broken links, etc.)
   - Crawls pages to extract JSON-LD schema and content
   - Analyzes content depth, structure, authority signals
   - Assesses AEO readiness (direct answers, schema completeness, citability)
   - Generates report combining Ahrefs technical findings + content/AEO gaps
   - Provides specific schema fixes and content recommendations

**User:** "My blog posts don't rank well and AI doesn't cite my content. Can you analyze it?"

**Assistant:**
1. Asks: "Let me check your content structure and schema.
   - What's a specific page/post URL?
   - Do you have Ahrefs? If so, what's your project ID?
   - What does your blog cover?

2. Crawls the page and:
   - Checks for author info, credentials, publication date
   - Validates schema (Article? BlogPosting? Anything?)
   - Assesses if content directly answers questions or buries answers in prose
   - Checks source citations and freshness

3. If Ahrefs provided: Compares Ahrefs technical findings + content analysis

4. Generates report with gaps like:
   - "No author schema → AI can't attribute content"
   - "No schema.org metadata → AI can't extract structured data"
   - "Content lacks direct answers in opening → AI/users skip it"
   - "Statistics cited without links → Not citable"

**User:** "I have FAQ pages but they don't show in AI responses. Can you check?"

**Assistant:**
1. Crawls FAQ pages and extracts JSON-LD
2. Finds issues like:
   - "FAQPage schema present but missing 'answer' field on 5 of 8 Q&As"
   - "Schema doesn't match visible content (claims 8 FAQs but page shows 3)"
3. Provides specific fixes:
   - "Add complete 'answer' property to each Question item in FAQPage schema"
   - "Ensure every visible FAQ is represented in schema"
4. Explains impact: "Complete FAQPage schema enables AI systems to extract and cite your Q&As in search results"

## Success Metrics

A successful audit includes:
- ✅ Ahrefs data fetched automatically (if project ID provided)
- ✅ JSON-LD extracted and validated on every page (not "no schema found" without verification)
- ✅ Clear schema gaps identified (e.g., "FAQPage schema incomplete: missing 'answer' field on X Q&As")
- ✅ Content quality issues specific to ranking/citability (e.g., "Content doesn't answer main question in first paragraph")
- ✅ Authority signal assessment (author, dates, citations present/missing)
- ✅ Specific schema/content fixes with effort estimates ("Add datePublished to Article schema: 30 minutes")
- ✅ Report integrates Ahrefs technical findings with content/AEO gaps (not duplicate analysis)
- ✅ User can act on recommendations immediately

## Edge Cases

**Scenario: User provides Ahrefs report with no content issues noted**
- Don't assume content is good; Ahrefs doesn't assess content depth or schema completeness
- Still crawl and analyze content quality independently
- Focus on schema gaps and AI-friendliness, not technical SEO

**Scenario: Pages have schema but it's incomplete**
- Don't report "schema present" as passing; specify gaps
- Example: "Article schema present but missing author, datePublished, and description fields"
- Provide exact fixes to complete schema

**Scenario: Content is JavaScript-rendered**
- Note that analysis is limited to SSR content visible in initial HTML
- Recommend user verify CSR-rendered content in browser or via Puppeteer
- Flag which content gaps may be due to CSR rendering

**Scenario: Site has no schema at all**
- This is HIGH priority for AEO; provide specific schema recommendations for each content type
- Example: "Homepage needs Organization schema; blog posts need Article schema; FAQ section needs FAQPage schema"

**Scenario: User asks "is my schema valid?"**
- Don't just say "valid" or "invalid"
- Provide specific assessment: "Schema structure is valid but missing 3 required properties: author, datePublished, image"
- Recommend user run [Google's Rich Results Test](https://search.google.com/test/rich-results) for official validation
