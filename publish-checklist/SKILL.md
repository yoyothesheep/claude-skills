---
name: publish-checklist
description: Pre-publish checklist for site pages (blog posts, case studies, career/industry pages, /now articles). Run before publishing or updating a page to validate SEO, dates, sitemap, links, formatting, and build. Site-specific rules live in the project, not in this skill.
---

# Publish Checklist

Run before publishing or updating any page. Unless otherwise specified, fix failures immediately using Edit/Write tools before moving on. Report final results as PASS/FAIL/FIXED.

This skill is generic and shared across sites. Everything site-specific (page types, files, scripts, trackers, data wiring) lives in the project's `docs/publish-checklist/`.

## Setup

Read `docs/publish-checklist/CONFIG.md` in the project root. If it is missing, stop and tell the user to create it from `CONFIG.example.md` and `site-checklist.example.md` in this skill's folder. Load:
- `SITE_CHECKLIST_PATH` (required) — the site-specific checklist: page type detection, Phase 2 checks
- `PUBLISH_SCRIPT` (optional) — automated validation command
- `SITEMAP_PATH` (optional) — sitemap to verify
- `TRACKER_AEO_CONTENT` (optional) — content tracker file

Read the file at `SITE_CHECKLIST_PATH` in full before doing anything else. Its checks are mandatory, in addition to the shared ones below.

---

## Phase 0: Detect & Run Script

Detect the page type from the user's input using the rules in `SITE_CHECKLIST_PATH`.

If `PUBLISH_SCRIPT` is set, run it and fix all FAILs before continuing. Otherwise do the "Automated" items in the site checklist by hand.

---

## Phase 1: Shared Checks (all page types)

### Formatting

- [ ] Anchor links: every `href="#..."` has a matching `id` attribute in rendered output
- [ ] Image/asset paths: all referenced files exist in the public directory
- [ ] Internal links point to valid routes

### SEO & Metadata

- [ ] Title matches `<h1>` (unless the site has a separate SEO title field); title <60 chars
- [ ] Description: 1 sentence, distinct from homepage, <160 chars, specific (names a number, entity, or data point)
- [ ] OG quality: action-oriented or curiosity-driven — would you click this in search results?
- [ ] FAQ pairs (if present) are real questions (not statements) with concise, specific answers
- [ ] JSON-LD: correct schema type present for the page type (see `SITE_CHECKLIST_PATH` for type mapping)
- [ ] AEO: first paragraph of each `<h2>` directly answers the implied question; headings match common queries

### Accessibility

- [ ] `aria-expanded` on all expandable toggles
- [ ] Decorative SVGs have `aria-hidden="true"`

---

## Phase 2: Page-Type Checks

Run the section from `SITE_CHECKLIST_PATH` matching the detected page type. Include its cross-reference checks: places outside the page itself that must change or already link to it (sitemap, indexes, data files, other pages' links, specs, tests).

---

## Phase 3: Update Content Tracker

Skip if `TRACKER_AEO_CONTENT` is not set.

After all checks pass, update the tracker: if the page has a row, set Status to `Published YYYY-MM-DD` (today); otherwise add a row using the columns and Type values defined in the site checklist. Only intervene manually if `PUBLISH_SCRIPT` handles tracker updates and reports it could not.

---

## Phase 4: Report

List every check as PASS / FAIL / FIXED. Name anything skipped and why.
