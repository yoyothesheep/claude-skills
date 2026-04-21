---
name: reddit-content
description: Generates ready-to-post Reddit comment and post drafts for a given piece of content. Output is a markdown file — no Reddit API, no authentication required. The human pastes and posts manually.
---

# Reddit Content Skill

Generates Reddit comment drafts for a new blog post or page. Output is saved as a `.md` file the user can copy-paste directly. No API access needed.

**Trigger:** "draft reddit content for [post]" or invoked by `aeo-distribution` as Step 2.

---

## Inputs Required

- **Post URL** — full URL
- **Post title**
- **Key claim** — the most specific, data-backed sentence in the post
- **Target subreddits** — if not provided, use `SUBREDDITS_TIER1/2/3` from CONFIG.md

---

## Step 1: Find Live Thread Opportunities

Run web searches to find threads posted in the last 48 hours where a comment would be on-topic. Do not draft for threads that are stale (>3 days old).

Use `SEARCH_QUERIES` from CONFIG.md as the base queries, substituting `[topic keywords]` with terms from the post's key claim.

For each result, extract:
- Thread title
- Subreddit
- Approximate post age
- Comment count (signals whether thread is still active)
- Whether OP's question is directly answered by the post

Only proceed to drafts for threads where the post **directly answers** the OP's question. Skip tangential matches.

---

## Step 2: Draft Comments

For each qualifying thread, write one comment draft. Rules:

1. Read the OP's question carefully. Answer it directly in the first sentence.
2. Include exactly one specific stat or data point from the post.
3. Place the link naturally near the end — never the first sentence, never "Check out my site."
4. Match subreddit tone using `SUBREDDIT_TONES` from CONFIG.md.
5. Max 250 words. No headers. No bullet lists (reads as promotional).
6. Do not start with "Great question", "As someone who...", or "I actually wrote about this."
7. One link per comment, at the end.

**Angle selection by thread type:** use `THREAD_ANGLES` from CONFIG.md.

---

## Step 3: Draft a Standalone Post (Optional)

If no qualifying live threads are found, draft a standalone post for the highest-relevance subreddit.

Standalone post format:
- **Title:** A genuine question or specific claim — not "I built a site." Use `STANDALONE_TITLE_EXAMPLES` from CONFIG.md as reference for the site's voice and topic range.
- **Body:** 200–400 words. Lead with the finding, not the story of how you found it. Include 2–3 specific data points. Link at the end with one sentence of context.
- **Flair:** use "Discussion" or "Resource" — never "Self-Promotion"

Standalone posts should only be drafted if the content is genuinely useful as a standalone read, not just a wrapper for the link.

---

## Output Format

Save to: `docs/promotion/reddit/reddit_drafts_[slug]_[YYYY-MM-DD].md`

```markdown
# Reddit Drafts — [Post Title] — [Date]

## Live Thread Opportunities

### 1. "[Thread Title]"
**Subreddit:** r/[sub] | **Age:** Xh | **Comments:** N
**Thread URL:** [URL]
**Why relevant:** [1 sentence]

**Draft comment:**

[comment text — ready to copy-paste]

---

### 2. "[Thread Title]"
...

---

## Standalone Post Draft (if no live threads found)

**Target subreddit:** r/[sub]
**Flair:** Discussion

**Title:** [title]

**Body:**

[post body]
```

---

## Quality Check Before Saving

- [ ] Does each comment open by answering the OP's question — not by introducing yourself or the site?
- [ ] Is the link in the last 20% of the comment?
- [ ] Is every data point sourced from the actual post?
- [ ] Does any comment exceed 250 words? Trim it.
- [ ] Does the standalone post title read like something a non-affiliated person would post?
