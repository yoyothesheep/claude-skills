---
name: product-design
description: >-
  Guides building or improving any visual/UI design (landing pages, app screens, dashboards,
  marketing pages, prototypes) through a Discover/Define/Deliver process that produces
  several genuinely distinct directions and pushes past the generic "AI slop" look — instead
  of one-shotting a single templated result. Use this whenever the user asks to build,
  redesign, or restyle a UI, landing page, app screen, or any visual layout; whenever they say
  a design "looks AI-generated," "generic," "like every other AI site," "boring," or "not
  unique"; or whenever they ask for design options/directions to choose between, even if they
  don't name this skill directly. Runs as an interactive, stage-by-stage loop — it pauses for
  the user's judgment after each stage rather than delivering a finished result in one pass,
  and expects to be invoked again for further rounds of refinement on the same design.
---

# product-design

LLMs pick the most probable option at every design decision, so unguided output converges on
the average: gradient hero, text-left/graphic-right, three feature cards. Asking for
"something unique" doesn't help — the request is processed by the same machinery that
produces the average. Variance has to be **imposed from outside** and judged by **something
that didn't build it**.

## Usage

Not one-shot. Three checkpointed stages — Discover, Define, Deliver — stop after each and
wait for a decision. Chain only if the user says so (`auto-advance`). Re-invoking on an
already-polished design is normal.

State the knobs in one line before each stage. Don't silently pick and proceed.

**Screenshot every stage, every iteration. No exceptions.** Show the actual pixels inline
before asking anything; a prose description never substitutes.

```bash
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"   # adjust per OS
"$CHROME" --headless=new --disable-gpu --hide-scrollbars --window-size=1440,900 \
  --screenshot="<out.png>" "<file-or-localhost-url>"
```
Serve local files first if they load images or fonts (`python3 -m http.server`). Size the
window to fit the whole frame — a cropped screenshot produces bogus critique. Then read the
PNG back and show it.

### Knobs

| Knob | Values | Default |
|---|---|---|
| Entry point | `fresh` / `re-pass` | Infer. On a re-pass, builders get **explicit permission to break the existing design system** — see below |
| Stage scope | `discover` / `define` / `deliver` / `full` | `full` |
| Auto-advance | `false` / `true` | `false` — pause after every stage |
| Variant count (N) | integer | `3` |
| Concept ideation | `on` / `off` | `on` — `off` means seeds alone drive Discover |
| Critic loop ceiling | integer, per "keep going" answer | `3` |
| Critic references | `auto` / `user-only` / `none` | `auto` — see Stage 2 |
| Builder & critic model | any available | `opus` for both — this is a taste task, not a cost-optimization one |
| Polish passes | subset of {cut dead weight, AI-tells, copy rewrite} | all three, one at a time |

## Before anything: check the product spec, infer vibes & find real content

**1. Check `specs/product/` (works with `product-scoping` & `loop-engineering`):**
Look in `specs/product/` for an existing product specification.
- **If a product spec exists:** Read the target users/personas, goals, scoped features, and Key User Flows ($F_1..F_m$) so the mocks reflect the exact scoped screens and fields without inventing unrequested features.
- **If no product spec exists:** Ask if the user wants to scope one first via `product-scoping` or jump straight into designing (do **not** require a spec if they want to design directly).

**2. Infer candidate vibes from users/personas & ask for user preferences:**
Before generating variants, use the target audience, user stories, and domain context to **infer 2–3 distinct visual vibes/directions** that would fit how and where those users use the product (e.g., kitchen glanceability at arm's length vs. editorial cookbook warmth vs. high-contrast utility checklist). These are inputs to concept ideation (Stage 1), not the final directions — inferred vibes are the model's most probable guess. Ask the user for thoughts, reference apps, or vibe preferences; any reference apps they name also feed the Stage 2 critic.

**3. Go get the product's actual content — real names, real copy, real photographs.** Query
the database, read the fixtures, look in the image directory. This is the highest-leverage
step in the whole skill and the easiest to skip.

Gray placeholder bars and gradient rectangles are the single most reliable tell of a
generated design, and they also lie: they let a design that depends on photography look fine
without ever being tested with a photo. A recipe app has dish photos. A dashboard has real
numbers. Use them.

Then tell builders: **no placeholder geometry.** Every region that will hold content holds
real content. If something is genuinely missing — a recipe with no photo, a null value —
that absence is a real design problem to solve honestly, not to paper over with a shape.

## Stage 1 — Discover

Goal: breadth. Always produce N, never one.

### 0. Concept ideation (the user's taste steers)
Distinctiveness comes from the user's taste, not the model's ideas — pasting AI ideas straight
back into AI gets what anyone else would get. Skip only if `concept ideation: off`.

1. **Go broad, not deep.** List 12–20 bold design-language concepts, one line each, no detail
   — an inspiration source (a game genre, an interior trend, an art movement, a physical
   object) and how it would shape the UI. Include the inferred vibes, and include ideas that
   sound like they can't work: "there's no way this works" is the right zone.
2. **Stop. Ask the user to react** — favorites, what each evokes, what feels tacky, what to
   avoid. Reactions matter more than picks.
3. **Sharpen** the favorites against those reactions into N concept briefs (2–4 sentences
   each). Show them; adjust if asked.

Each variant then gets one concept brief **plus** its own seed: the concept supplies intent,
the seed supplies execution entropy (palette, cadence, details) within it.

Discover uses a **3-part anti-slop engine** to guarantee that variants do not collapse into the same generic look (especially avoiding the "Claude 2025 Paper Slop" trap: manila beige background, black wireframe boxes, and monospace brackets):

### 1. Entropy: Generate a Unique Random Alphanumeric Seed per Variant
Generate an independent 32-character alphanumeric seed for each variant using a shell script:
```bash
python3 -c 'import secrets, string; alphabet = string.ascii_letters + string.digits; print("".join(secrets.choice(alphabet) for _ in range(32)))'
```
Instruct each builder subagent:
- **Decode subpatterns, rhythm, and character combinations** in its assigned string to define its creative anchor (palette temperature, contrast balance, layout cadence, micro-depth).
- **Look beyond the surface** for inspiration (e.g. sharp geometric cadences, organic curves, high-contrast jumps).
- **NEVER reveal the string in the UI.** It is purely internal creative entropy to break the LLM's probability bias.

### 2. Diversity Rejection Gate (The Circuit Breaker)
Before presenting screenshots to the user, run an automated pairwise check across the N variants:
1. **Palette Check**: If two variants share the same background family (e.g. both use beige/cream `#F4EFE6` or `#F5EDD6`), automatically reject the weaker one and re-roll.
2. **Surface & Border Check**: If two variants box every section in black `1px solid` wireframes or 0px brutalist cells, reject the weaker one.
3. **Typography Check**: If two variants rely on monospace for general consumer UI labels or brackets `[ ]`, reject the weaker one.

### 3. Write Briefs Under Contract
- Product facts go in as **bullets, ≤60 words, no adjectives, no sample phrasings.**
- The orchestrator writes **zero prose copy.** Builders write their own.
- List what the *other* variants are taking, so each avoids drifting there.
- **Don't** paste `references/ai-tells-checklist.md` in as bans — banning makes the model
  overthink and swap in stranger substitutes. Tells are checked after the build (diversity
  gate here, AI-tells pass in Deliver).
- State what must not be invented — features, fields, or data the product doesn't have.

### 4. Build, Critique, Screenshot
- Build each variant as an isolated subagent on the builder model, fresh context.
- Screenshot all N side-by-side on the specified canvas.
- Present to user with critique notes, then stop for the user's pick.

## Stage 2 — Define

Goal: push the chosen direction past its first draft using an outside eye.

1. Screenshot the current build.
2. Run one critic pass on the critic model using `references/critic-prompt-template.md` —
   fresh context, screenshot only, no code or prior critique. **Scope it:** tell the critic
   which constraints are fixed (data model, missing fields, known upstream bugs) so it spends
   its judgment on craft instead of re-proposing an information architecture the data can't
   support. Give it a visual bar (below) — without one, critics of app screens drift into
   product strategy and scores plateau.
3. Show the before/after screenshots, the score, and the notes.
4. **Stop.** Iterate / accept / stop. Loop unattended only to the ceiling knob, then check in
   regardless of score.

### Reference set (critic visual bar)

"Imagine a top studio" is a mushy bar — the model's imagined best is its average. Real
screenshots make it concrete. Gather **4 references** in the same category and platform, once
per design, and reuse the same set every round so scores stay comparable. Sources, in order:

1. **User-supplied** — images they drop in, or products they named. Always first.
2. **A design-reference tool, if one is connected and responds** (e.g. a screen-library MCP).
   Probe with one call; if it errors or returns nothing usable, move on — don't retry.
3. **Live products** — search for current, well-regarded products in this category (don't
   use a remembered list; it goes stale) and screenshot them with the Chrome command above.
   Skip any page that renders a login wall, cookie banner, or broken layout.

Show the user the set before the first critic pass; they can swap any. If fewer than 2 usable
references turn up, or `critic references: none`, fall back to the single-screenshot prompt.

Run the critic **blind**: shuffle ours in among the references, unlabeled, and use the ranking
prompt in `references/critic-prompt-template.md`. Our rank is the headline score; the gaps
versus higher-ranked images are the fix list. References set the bar — tell the critic not
to copy them, and tell builders the same.

**Route subtraction to Deliver.** Split the critic's fix list: craft fixes (composition,
hierarchy, spacing, component consistency) go into the next Define build; pure cuts (redundant
labels, duplicate state signals, filler metadata) are queued for Deliver's cut pass, where
each is shown separately. Folding cuts into a Define round changes too much at once to see
what helped.

**Weigh the critic, don't obey it.** It's judging a picture with no product context. When it
proposes something the data can't support, or contradicts a convention the rest of the app
already uses, say so and skip it — and tell the user you did. A flat score across rounds
usually means the real lever isn't reachable by layout edits (often: the design needs real
photography it doesn't have).

## Stage 3 — Deliver

Goal: subtract. AI adds and rarely removes — the fix list at this stage is almost always
subtraction. Apply passes one at a time, screenshot after each, stop for confirmation.

1. **Cut dead weight** — does this element carry information, or fill space? Cut filler:
   redundant counters, labels stating the default case, decorative rules, watermarks, chrome
   that crowds out content. Count the chrome-to-content ratio on the first screen.
2. **AI-tells pass** — `references/ai-tells-checklist.md`. Try the alternative, show both.
3. **Copy rewrite** — AI copy is placeholder, like Lorem ipsum. A human rewrites every line
   before shipping. Never auto-finalize copy.
4. **Sync to Product Spec (`specs/product/`) & Handoff to `loop-engineering`** — Once a design is accepted (either after Discover/Define or after Deliver), if a product spec exists in `specs/product/`, update its `## UI Design & Mocks` section with the chosen design direction, mock source path(s), and final screenshot path(s) so `loop-engineering` can build and verify UI units against them.

## Re-entering on an existing design

Normal. Treat the current state as the baseline: Discover branches off the winner, Define
re-critiques with fresh context, Deliver re-checks tells since content moved.

## Image & video generation — use if available, else skip

Coding agents default to code-drawn gradients, shapes, and patterns — a top AI tell. Check
for a real generation tool first: a built-in image tool, the Codex CLI, or an API key the
user has provided (OpenAI/Gemini for images, fal.ai for video).

- **Available:** use it in Define/Deliver for imagery real content can't supply. Images: hero
  visuals, textures, illustrations. Video: looping graphics on a solid background (chroma-key
  or matte it out to layer in the UI), or keyframe-interpolated transitions scrubbed on
  scroll. Keep keys local — never write them into product code. Verify motion frame-by-frame
  in the browser, not from one screenshot.
- **Not available:** skip it. Never fabricate a tool or claim to call one.

Real existing content still beats generated content.

## Output contract

- Discover: stops for the user's concept reactions (unless ideation is `off`), then ≥N
  options, diversity-gated and critiqued, stops for a pick.
- Define: reference set shown once; before/after, rank, and score; stops after every critic pass.
- Deliver: one pass at a time, stops after each.
- A real screenshot, inline, at every point above.
- No invented features, fields, or data — ever, including in mockups.
- Nothing auto-advances without `auto-advance: true`.
