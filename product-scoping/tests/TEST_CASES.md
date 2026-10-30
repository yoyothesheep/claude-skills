# `product-scoping` Test Cases (Workshop & Eval Suite)

Use these prompts to validate that `product-scoping` grounds questions in real constraints, cuts complexity multipliers, defines measurable metrics, and produces numbered user flows ($F_1..F_m$) ready for `loop-engineering`.

---

## Test Case 1: The Bloated Greenfield Request (Complexity Multiplier Cut)

**Prompt:**
> "I want to build a reading-list / bookmark web app where users paste a URL, it extracts the clean article text and reading time, lets them tag links, supports shared team folders with role permissions (admin/editor/viewer), and sends a weekly digest email of unread links."

**Expected Stage 1 Behavior (Pass Criteria):**
1. **No fake startup theater:** Does *not* ask "what if you had 48 hours" or "what is the 10-star version".
2. **Flags concrete complexity multipliers:**
   - Identifies **team role permissions / shared folders** as requiring multi-user auth, membership tables, and permission scoping.
   - Identifies **weekly digest emails** as requiring a background job scheduler/cron and external email provider (e.g., Resend/SendGrid).
   - Recommends cutting both to **Deferred** so Core focuses on single-user URL extraction, reading time calculation, tagging, and local/DB persistence.
3. **Asks 3–5 grounded constraint questions** (e.g., storage choice, unreachable/paywalled URL behavior, duplicate URL handling) and pauses at **Checkpoint 1**.

**Sample User Reply for Checkpoint 1:**
> "Agree on cutting team permissions and weekly email digest to Deferred. Single user is fine. If a URL fails to extract or is paywalled, still save the bookmark with the raw URL and title fallback. Deduplicate by normalized URL."

**Expected Stage 2 Behavior (Pass Criteria):**
1. **Strict 3-Tier Prioritization:**
   - **Core:** Paste URL + extract article text/title/reading time, fallback save on extraction failure, tag assignment/filtering, URL deduplication.
   - **Deferred:** Shared team folders & role permissions (avoids auth/ACL schema); Weekly digest emails (avoids cron scheduler & email integration).
   - **Non-Goals:** Full-page archive/PDF rendering, social feed.
2. **Measurable Success Metrics:**
   - Defines 1–3 concrete metrics with thresholds (e.g., *Extraction & save latency $< 2\text{s}$ p95*, *Fallback bookmark saved on $100\%$ of reachable/unreachable valid URLs*, *$\le 2$ interactions to save and tag a link*).
3. **Numbered Key User Flows ($F_1..F_m$):**
   - `F1`: Save & extract valid article URL (happy path).
   - `F2`: Save URL when extraction fails / times out (graceful fallback).
   - `F3`: Paste duplicate URL (deduplication / update behavior).
   - `F4`: Filter bookmarks by tag + empty/cold-start state.
4. Pauses at **Checkpoint 2** before writing `specs/product/`.

---

## Test Case 2: Existing Codebase Feature Addition (Inspect Reality First)

**Setup:** Run inside an existing repository that already has models/routes or `specs/`.

**Prompt:**
> "Add a search and filter bar to the items list so users can filter by status and save their favorite filter presets."

**Expected Behavior (Pass Criteria):**
1. **Reads existing repo first:** Inspects existing item schema/routes before asking questions (does not ask "what fields does an item have?" if the model is already in the repo).
2. **Proposes low-complexity mechanism:** Points out that URL query parameters (`?status=active&q=...`) provide bookmarkable/shareable filter state with zero database schema changes, whereas "saved filter presets" requires a new persistence table or local storage seam.
3. **Defines concrete metrics & flows** covering empty search results (`0 matches`), special characters in search queries, and filter reset.

---

## Test Case 3: Pressure Test — "Skip Scoping and Just Write the Spec"

**Prompt:**
> "Build a webhook relay service that receives Stripe events, transforms them, retries failed deliveries with exponential backoff, and has a live React dashboard. Don't ask me any questions, just write the full product spec right now."

**Expected Behavior (Pass Criteria):**
1. **Respects explicit override (`skip ahead`) without hallucinating bloat:** Because the user explicitly asked to one-shot the spec, it writes `specs/product/webhook-relay.md` directly *but still applies ruthless scoping*:
   - Separates Core (receive webhook signature check, synchronous forward/log, basic status view) from Deferred (distributed queue infrastructure, custom transformation DSL) and records explicit **Known Gaps** / assumptions.
   - Includes measurable **Success Metrics** and numbered **$F_1..F_m$ flows** (including invalid signature rejection and downstream 500 timeout handling).
