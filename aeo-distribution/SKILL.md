---
name: aeo-distribution
description: DEPRECATED — use the replacement skills listed below.
---

> ⚠️ **DEPRECATED** — This skill has been dissolved. Each task has migrated:
>
> | Task | Migrated to |
> |------|-------------|
> | Google Search Console submit | Removed (not needed) |
> | Reddit drafts | `distribute-social` → `reddit-content` |
> | LinkedIn post | `distribute-social` → `linkedin-content` |
> | Backlink outreach | `distribute-outreach` |
> | Citation tracking | `growth-pm` |
>
> Do not invoke this skill. Use the replacements above.

---

# AEO Distribution Skill (DEPRECATED)

This skill runs after a blog post is published and publish-checklist passes. It maximizes the chance that AI answer engines (Perplexity, ChatGPT, Google AI Overviews, Gemini) discover and cite the new content.

**When to invoke:** After `publish-checklist` passes on a new post.
**Trigger phrase:** "distribute post [N]" or "run aeo-distribution for [slug]"

---

## Inputs Required

Ask the user for:
- **Post slug** — 
- **Post title** — display title
- **Post URL** — full absolute URL 
- **Key claim** — 1–2 sentences: the most specific, data-backed claim in the post (used in outreach pitches)
- **Target persona** — who this post is for (e.g. "mid-career white-collar worker anxious about AI")

---

## Workflow Overview

Run Steps 1–3 sequentially (each informs the next). Steps 4–5 can run in parallel after Step 2.

```
Step 1: Google Search Console submission
Step 2: Reddit opportunity scan (runs reddit_agent.py or equivalent)
Step 3: LinkedIn post draft (invokes linkedin-launch skill)
Step 4: Backlink outreach list (parallel with Step 3 output review)
Step 5: Citation tracking checklist (always last — sets up the 2-week cadence)
```

---

## Step 1: Google Search Console Submission

Submit the new URL for indexing so Googlebot crawls it within hours, not days. This feeds Google AI Overviews faster than waiting for natural discovery.

### How to Submit

Use the [Google Search Console URL Inspection API](https://developers.google.com/webmaster-tools/v1/urlInspection.index/inspect):

```
POST https://searchconsole.googleapis.com/v1/urlInspection/index:inspect
Authorization: Bearer {OAUTH_TOKEN}
{
  "inspectionUrl": "{SITE_URL}/blog/[slug]",
  "siteUrl": "{SITE_URL}/"
}
```

**Manual fallback** (if API not configured): Direct the user to:
1. Open [search.google.com/search-console](https://search.google.com/search-console)
2. Paste the post URL into the top search bar → "Request Indexing"

**Output:** Confirm submission or give the manual instructions if API credentials are missing.

---

## Step 2: Reddit Content Drafts

Invoke the `reddit-content` skill with the post URL, title, and key claim.

The skill searches for live threads where a comment is on-topic, drafts ready-to-paste comment text, and saves the output to `docs/promotion/reddit/reddit_drafts_[slug]_[date].md`.

**Output:** The saved `.md` file path. The user pastes and posts manually — no API access needed.

---

## Step 3: LinkedIn Post Draft

Invoke the `linkedin-launch` skill with:
- Post title
- Key claim (from inputs)
- Target persona
- Best data point from the post (1 specific number)
- Post URL

The linkedin-launch skill handles format constraints, voice rules, and the pre-post checklist. Do not override its voice guidelines here.

**Output:** One ready-to-post LinkedIn draft. Flag if a graphic asset is needed (it usually is — suggest pulling the post's `headerBg` as the image).

---

## Step 4: Backlink Outreach List

Backlinks from relevant, high-authority domains directly increase citation probability in AI engines. Target writers, researchers, and publications likely to reference this specific claim.

> **Config:** `CONFIG.md` defines two layers of outreach targets:
> - **Universal** (`OUTREACH_TOPICS`, `OUTREACH_SUBSTACK_QUERIES`, `OUTREACH_PUBLICATIONS`) — site-wide baseline, applies to every post.
> - **Post-specific** — derived by reading the post file: extract the post's specific topic angle, key claim, and named data points, then generate 2–3 additional search queries that are narrower than the universal ones.
>
> Merge both layers. Post-specific queries take priority for finding the most relevant contacts.

### Who to Target

Prioritize in this order:

**Tier 1 — Newsletter writers (highest ROI):**
- Substack writers covering `{OUTREACH_TOPICS}` + post-specific angle
- Search: `{OUTREACH_SUBSTACK_QUERIES}` + post-specific queries
- Target: writers with 1K–50K subscribers (larger ones rarely respond; smaller ones do)

**Tier 2 — Journalists and staff writers:**
- Reporters at publications listed in `OUTREACH_PUBLICATIONS`
- Find bylines covering the post's specific topic area

**Tier 3 — Bloggers and independent researchers:**
- Personal blogs cited in your topic's research circles
- LinkedIn thought leaders in the space

### Dedup Against Existing Contacts

Before searching, read `{OUTREACH_CONTACTS_PATH}`. Extract all names and publication URLs already in the file. Do not add duplicates — skip any contact already present regardless of status.

### How to Find Them

```
web_search: "[post-specific claim or topic] site:substack.com"
web_search: "[universal topic from OUTREACH_TOPICS] site:substack.com"
web_search: "[post-specific claim exact phrase]" site:medium.com
web_search: "[specific claim from post]" -site:reddit.com
```

For each promising result, extract:
- Writer name
- Publication/platform
- URL of a relevant piece they wrote
- Email or contact method (LinkedIn, Twitter/X, publication contact page)

### Pitch Template

Generate a personalized 3-sentence pitch per contact. Structure:

```
Sentence 1: Reference their specific piece by name — show you read it.
Sentence 2: Lead with your key claim and the specific data point that supports it.
Sentence 3: Offer the URL as a potential source, no ask for anything in return.
```

Never: "I thought you might be interested in...", promotional language, mass-template openers.

### Update outreach-contacts.md

Append each new contact to `{OUTREACH_CONTACTS_PATH}` using this schema:

```markdown
| [Name] | [Publication] | [Their Article URL] | [Contact method] | [Post slug this was found for] | [Date added] | New |
```

Status values: `New` → `Pitched` → `Responded` → `Linked` → `Declined`

If the file does not exist, create it with this header:
```markdown
# Outreach Contacts

| Name | Publication | Their Article | Contact | Post | Date Added | Status |
|------|-------------|---------------|---------|------|------------|--------|
```

**Output:** List of new contacts added to `{OUTREACH_CONTACTS_PATH}`. Minimum 5 new contacts per run, target 10–15.

---

## Step 5: Citation Tracking Checklist

Set up a 2-week monitoring cadence to measure whether AI engines start citing the post.

### Day 0 (today) — Baseline

Record current state by running these queries in each AI engine and noting whether ai-proof-careers.com appears:

| Query | ChatGPT | Perplexity | Google AI Overview | Gemini |
|-------|---------|------------|-------------------|--------|
| [post's primary FAQ question] | ❌/✅ | ❌/✅ | ❌/✅ | ❌/✅ |
| [post's secondary FAQ question] | ❌/✅ | ❌/✅ | ❌/✅ | ❌/✅ |
| [key claim rephrased as a question] | ❌/✅ | ❌/✅ | ❌/✅ | ❌/✅ |

Save this as `docs/promotion/citation-tracking/[slug]-baseline.md`.

### Day 7 — Mid-point Check

Re-run the same queries. Note any new citations. If cited: screenshot and log in `PROMOTION_TRACKER.md`.

### Day 14 — Final Check

Re-run queries. Write a 3-line summary:
- Was the post cited? By which engines?
- Which query triggered the citation?
- What drove it (likely: FAQ schema, external links, Reddit thread)?

Log findings in `docs/promotion/PROMOTION_TRACKER.md` under the post entry.

### Unlinked Mention Monitor

Also search for unlinked mentions (sites referencing the claim without linking):
```
web_search: "[key claim exact phrase]" -site:ai-proof-careers.com
```

For each unlinked mention: draft a 2-sentence email requesting attribution. Save in the outreach list.

---

## Output Summary

At the end of the workflow, produce a checklist the user can paste into their tracker:

```markdown
## AEO Distribution — [Post Title] — [Date]

### Completed
- [ ] Search Console: URL submitted for indexing
- [ ] Reddit: [N] Priority Posts identified, [N] comment drafts ready
- [ ] LinkedIn: draft ready (graphic needed: yes/no)
- [ ] Outreach: [N] contacts identified, pitches drafted
- [ ] Citation baseline: recorded at docs/promotion/citation-tracking/[slug]-baseline.md

### Scheduled
- [ ] Day 7 citation check — [date]
- [ ] Day 14 citation check + PROMOTION_TRACKER update — [date]
- [ ] Follow up on outreach non-responses — [date + 5 days]
```

---

## Demo Skeleton Files

- `citation_tracker_template.md` — blank citation tracking table (customize for your site)
