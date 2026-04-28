---
name: publish-checklist
description: Pre-publish checklist for blog posts, career pages, industry pages, and /now articles. Run before publishing or updating to validate SEO, dates, sitemap, formatting, and build.
---

# Publish Checklist

Run before publishing or updating any page. Unless otherwise specified, fix failures immediately using Edit/Write tools before moving on. Report final results as PASS/FAIL/FIXED.

## Setup

Read `.claude/skills/publish-checklist/CONFIG.md` and load:
- `PUBLISH_SCRIPT` — the automated validation script command
- `SITE_CHECKLIST_PATH` — path to the site-specific checklist instruction file
- `TRACKER_AEO_CONTENT` — content tracker file (all published pages)

Read the file at `SITE_CHECKLIST_PATH` — it defines page type detection, the automated script flags, and all Phase 2 page-type-specific checks.

---

## Phase 0: Detect & Run Script

Detect the page type from the user's input using the rules in `SITE_CHECKLIST_PATH`.

Run the automated script from `PUBLISH_SCRIPT` and fix all FAILs before continuing.

---

## Phase 1: Shared Checks (all page types)

### Formatting

- [ ] Anchor links: every `href="#..."` has a matching `id` attribute in rendered output
- [ ] Image/asset paths: all referenced files exist in the public directory
- [ ] Internal links point to valid routes

### SEO & Metadata

- [ ] Title matches `<h1>`; title <60 chars
- [ ] Description: 1 sentence, distinct from homepage, <160 chars, specific (names a number, entity, or data point)
- [ ] OG quality: action-oriented or curiosity-driven — would you click this in search results?
- [ ] FAQ pairs are real questions (not statements) with concise, specific answers
- [ ] JSON-LD: correct schema type present for the page type (see `SITE_CHECKLIST_PATH` for type mapping)
- [ ] AEO: first paragraph of each `<h2>` directly answers the implied question; headings match common queries

### Accessibility & Mobile

- [ ] `aria-expanded` on all expandable toggles
- [ ] Decorative SVGs have `aria-hidden="true"`
- [ ] Body prose uses responsive text sizing
- [ ] Stat rows widen on mobile (never fixed half-width)
- [ ] Charts/graphs use stacked vertical layout on mobile

---

## Phase 2: Page-Type Checks

Run the section from `SITE_CHECKLIST_PATH` matching the detected page type.

---

## Phase 3: Update Content Tracker

After all checks pass, update `TRACKER_AEO_CONTENT`:

- If the page already has a row: update its Status to `Published YYYY-MM-DD` (today's date).
- If no row exists: add one to the Content Status table with columns: `Title | Type | Status | Priority | Slug | Notes`. Set Type to `Blog`, `Career`, `Industry`, or `Now`. Set Priority to `—`. Leave Notes blank unless there's something actionable.

The automated script (`publish_check.py`) handles this for pages already in the tracker with a Draft/Planned status. Only intervene manually if the script reports "no Draft/Planned row found."

**For blog posts only:** The script also creates `docs/tracker/citation_baselines/[slug]-baseline.md` with the Day 0/7/14 schedule pre-filled from the post's `faqQuestion`. After the script runs, open that file and fill in the Day 0 query results by running the listed queries in ChatGPT, Perplexity, Google AI Overview, and Gemini. Add 2 additional queries from the post's key claims before saving.
