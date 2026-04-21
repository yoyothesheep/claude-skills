---
name: distribute-social
description: Social distribution for a newly published post. Drafts Reddit comments/posts and a LinkedIn post in one run. Invokes reddit-content and linkedin-content as sub-skills. Use when a post is published and ready to distribute to social channels.
---

# Distribute Social

Runs after `publish-checklist` passes on a new post. Produces ready-to-use drafts for Reddit and LinkedIn in a single run.

**Sub-skills invoked:**
- `distribute-social/reddit-content.md` — finds live threads, drafts comment text
- `distribute-social/linkedin-content.md` — writes LinkedIn post draft

---

## Inputs Required

Ask the user for:
- **Post slug**
- **Post title** — display title
- **Post URL** — full absolute URL
- **Key claim** — 1–2 sentences: the most specific, data-backed claim in the post
- **Target persona** — who this post is for (e.g. "mid-career white-collar worker anxious about AI")
- **Best data point** — one specific number from the post (for LinkedIn opening)

---

## Workflow

Run both sub-skills in parallel after gathering inputs.

### Step 1: Reddit Drafts

Invoke `reddit-content` with: post URL, title, key claim.

The skill searches for live threads (≤48h old) where a comment is on-topic, drafts ready-to-paste comment text, and saves output to `{REDDIT_OUTPUT_PATH}reddit_drafts_[slug]_[date].md`.

Output: saved `.md` file path. User pastes and posts manually.

### Step 2: LinkedIn Draft

Invoke `linkedin-content` with: post title, key claim, target persona, best data point, post URL.

Output: one ready-to-post LinkedIn draft with graphic suggestions.

---

## Output Summary

```
## Social Distribution — [Post Title] — [Date]

- Reddit: [N] drafts saved → [file path]
- LinkedIn: draft ready (graphic needed: yes/no)
```
