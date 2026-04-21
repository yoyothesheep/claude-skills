---
name: distribute-outreach
description: Backlink and citation outreach for a newly published post. Finds Substack writers, journalists, and bloggers likely to reference the post's key claim, generates personalized pitches, and maintains a running outreach contacts file. Use after a post is published and socially distributed.
---

# Distribute Outreach

Finds writers, journalists, and bloggers likely to reference a new post's key claim. Generates personalized pitches and appends new contacts to the outreach CRM file.

---

## Inputs Required

Ask the user for:
- **Post slug**
- **Post title**
- **Post URL**
- **Key claim** — 1–2 sentences: the most specific, data-backed claim in the post

---

## Workflow

### Step 1: Derive Search Queries

Read the CONFIG.md universal targets. Then extract post-specific angles from the post URL/title/claim to generate 2–3 narrower queries.

Merge both layers — post-specific queries take priority.

### Step 2: Find Contacts

Prioritize in this order:

**Tier 1 — Newsletter writers (highest ROI)**
- Substack writers covering `{OUTREACH_TOPICS}` + post-specific angle
- Search: `{OUTREACH_SUBSTACK_QUERIES}` + post-specific queries
- Target: writers with 1K–50K subscribers

**Tier 2 — Journalists and staff writers**
- Reporters at publications listed in `OUTREACH_PUBLICATIONS`
- Find bylines covering the post's specific topic area

**Tier 3 — Bloggers and independent researchers**
- Personal blogs cited in your topic's research circles
- LinkedIn thought leaders in the space

Searches to run:
```
web_search: "[post-specific claim or topic] site:substack.com"
web_search: "[universal topic from OUTREACH_TOPICS] site:substack.com"
web_search: "[post-specific claim exact phrase]" site:medium.com
web_search: "[specific claim from post]" -site:reddit.com
```

For each result, extract: writer name, publication, URL of a relevant piece, contact method.

### Step 3: Dedup Against Existing Contacts

Before adding any contact, read `{OUTREACH_CONTACTS_PATH}`. Skip any name or publication URL already present regardless of status.

### Step 4: Generate Pitches

One personalized 3-sentence pitch per contact:

```
Sentence 1: Reference their specific piece by name — show you read it.
Sentence 2: Lead with your key claim and the specific data point that supports it.
Sentence 3: Offer the URL as a potential source — no ask for anything in return.
```

Never: "I thought you might be interested in...", promotional openers, mass-template language.

### Step 5: Update Outreach Contacts File

Append each new contact to `{OUTREACH_CONTACTS_PATH}`:

```markdown
| [Name] | [Publication] | [Their Article URL] | [Contact method] | [Post slug] | [Date added] | New |
```

Status values: `New` → `Pitched` → `Responded` → `Linked` → `Declined`

If the file doesn't exist, create it with header:
```markdown
# Outreach Contacts

| Name | Publication | Their Article | Contact | Post | Date Added | Status |
|------|-------------|---------------|---------|------|------------|--------|
```

---

## Output

```
## Outreach — [Post Title] — [Date]

- [N] new contacts added to [OUTREACH_CONTACTS_PATH]
- [N] pitches drafted

### New Contacts
| Name | Publication | Contact | Pitch |
|------|-------------|---------|-------|
| ...  | ...         | ...     | ...   |
```

Minimum 5 new contacts per run, target 10–15.
