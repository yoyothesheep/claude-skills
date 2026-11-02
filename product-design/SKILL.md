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

State the settings in one line before each stage. Don't silently pick and proceed.

**Write for people, not prompts.** Design terms (hero, above the fold, affordance) are fine.
Coined AI phrasing isn't — no abstract labels or slogans ("proximity does the sorting"). If a
non-designer couldn't act on a sentence, rewrite it.

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

### Settings

| Setting | Values | Default |
|---|---|---|
| Entry point | `fresh` / `re-pass` | Infer. On a re-pass, builders get **explicit permission to break the existing design system** — see below |
| Stage scope | `discover` / `define` / `deliver` / `full` | `full` |
| Auto-advance | `false` / `true` | `false` — pause after every stage |
| Surface | `marketing` / `product` | Infer. Marketing (homepage, landing) can go big and bold; product UI is functional first, with personality |
| Variant count (N) | integer | `3` |
| Critic loop ceiling | integer, per "keep going" answer | `3` |
| Critic references | `auto` / `user-only` / `none` | `auto` — see Stage 2 |
| Builder model | any available | `sonnet` |
| Critic model | any available | `opus` — the critic supplies the taste |
| Polish passes | subset of {cut dead weight, AI-tells, copy rewrite} | all three, one at a time |

## Before anything: check the product spec, infer vibes & find real content

**1. Check `specs/product/` (works with `product-scoping` & `product-loop-engineering`):**
Look in `specs/product/` for an existing product specification.
- **If a product spec exists:** Read the target users/personas, goals, scoped features, and Key User Flows ($F_1..F_m$) so the mocks reflect the exact scoped screens and fields without inventing unrequested features.
- **If no product spec exists:** Ask if the user wants to scope one first or jump straight into designing (do **not** require a spec if they want to design directly).

**2. Ask for the user's taste.** Reference apps or sites, vibes they like, things they hate.
Start `TASTE.md` with the answers (see Stage 2). Reference apps also feed the Stage 2 critic.
Discover doesn't use them — variety there comes from the seed.

**3. Go get the product's actual content if they exist — real names, real copy, real photographs.** Query
the database, read the fixtures, look in the image directory. This is the highest-leverage
step in the whole skill and the easiest to skip.

## Screen plan — edit before you design (product surface only)

A spec lists everything a screen *can* hold; a mock that shows all of it at once is a
spreadsheet. Screens scroll and reveal on tap. Before any builder sees a brief, write a plan
for each screen in the spec's "Key Screens to Mock" (or the screens the user names):

- **Job to be done** — the one thing the user does here, in one line.
- **Hero** — the single element that carries that job.
- **Shows first** — only what the job needs before any scroll. Aim for ≤5 distinct groups.
- **Below the fold / on tap** — everything else that belongs. In the mock it appears only as a
  scroll hint: a section peeking at the bottom edge. Don't squeeze it in.
- **States** — errors, empty, and edge cases are separate states, not decorations on the
  default frame. Mark issues in place quietly; the fix UI lives on tap. Mock a state only when
  it's the point of the screen, one per frame.
- **Cut** — anything that restates, explains the obvious, or is metadata nobody acts on:
  per-row counts, helper lines, inline fix buttons, "N more" footers, summary rows for content
  that's one scroll away, duplicate add buttons.

Show the screen plans and stop for edits. 

## Stage 1 — Discover (explore options)

Goal: breadth. Always produce N, never one.

### 1. Directions — one random seed per variant
The model can't act randomly or out-think its own averages, so the push has to come from
outside. Draw N long random alphanumeric strings with a shell script
(`python3 -c 'import secrets,string;print("".join(secrets.choice(string.ascii_letters+string.digits) for _ in range(40)))'`).
Each builder gets one string and the brief: look closely at the string — subpatterns,
repeated characters, case shifts, special numbers — define a creative direction (color,
layout, type, mood) from it, then build it. The string never appears in the UI. No concept
list and no feedback loop before the build; the user reacts to pixels.

### 2. Write briefs
- The orchestrator writes **zero prose copy.** Builders write their own.
- List what the *other* variants are taking, so each avoids drifting there.
- State what must not be invented — features, fields, or data the product doesn't have.
- **Product surface:** product facts as bullets (≤60 words, no adjectives), real content, and
  the screen plans verbatim. Function first — the seed shapes personality, not structure.
- **Marketing surface:** product facts; leave room to go big and strange.
- **Don't** paste `references/ai-tells-checklist.md` in as bans — banning makes the model
  swap in stranger substitutes. Tells are handled in Deliver.

### 3. Build, screenshot, present
- Build each variant as an isolated subagent on the builder model, fresh context.
- If two variants come out looking alike, rebuild one with an explicit "not that."
- Screenshot all N side-by-side, present them, stop for the user's pick.

## Stage 2 — Define (improve one)

Goal: push the chosen direction past its first draft using an outside eye.

1. Screenshot the current build.
2. Run one critic pass on the critic model using `references/critic-prompt-template.md` —
   a new agent per design per round, fresh context, screenshot only, no code or prior
   critique, same prompt every round. It scores the design against the criteria for its
   surface. Never have it rank our own variants against each other. **Scope it:** tell the critic
   which constraints are fixed (data model, missing fields, known upstream bugs) so it spends
   its judgment on craft instead of re-proposing an information architecture the data can't
   support. Give it a visual bar (below) — without one, critics of app screens drift into
   product strategy and scores plateau.
3. Show the before/after screenshots, the score, and the critic's fixes.
4. **Ask for the user's notes** (optional, one prompt): anything they love or that bugs them —
   point at it on the screen, or at an element from another variant to borrow. Reacting to
   pixels works; reacting to descriptions doesn't. Notes go to the builder with the critic's
   fixes, and **the user's notes win** where they conflict. Lasting likes and dislikes go into
   `TASTE.md`.
5. **Stop.** Iterate / accept / stop. Loop unattended only to the critic loop ceiling, then check in
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

Show the user the set before the first critic pass; they can swap any. The critic sees one of
our designs alongside the references as its baseline — a moodboard for the quality bar, not a
target to copy (tell builders the same). With no usable references, it judges against how a
top studio would execute the same aesthetic.

### TASTE.md — the user's taste, kept across rounds

One file per project (template: `references/taste-template.md`): reference images and sites,
what the user loves, what they don't, and product facts they keep correcting ("no days of
the week"). It goes into every Define brief and into the critic's fixed-constraints slot, so
the critic stops attacking choices the user made. Write entries as look and feel — palette,
type, texture, spacing, shape language, mood — never as what a screen or element *is*
("a stair of balconies"); builders take that literally.

### Brand pass (product surface, when an accepted marketing page exists)

Bring the marketing site's colors into the product — not its fonts or layout. Run
`scripts/extract_palette.py <marketing.html>` to pull its colors, assign them roles in the
product (primary action, accent, "needs checking", background tint, selected state), and
check every text/background pair with `--contrast`. Give the builder the palette as a fixed
constraint — colors in these roles; type and layout stay the product's own — then run the
normal critic round. Do it in Define, not Discover: in Discover the seed sets the palette.

**Apply the critic's cuts in the next round** — don't defer them to Deliver. Clutter left in
keeps drawing the critic's attention and the score stays flat.

**When the critic attacks the chosen aesthetic itself**, don't strip what the user chose.
It's usually reacting to the stack of defaults around that choice — remove the stack, keep
the choice.

**Weigh the critic, don't obey it.** It's judging a picture with no product context. When it
proposes something the data can't support, or contradicts a convention the rest of the app
already uses, say so and skip it — and tell the user you did. A flat score across rounds
usually means the real lever isn't reachable by layout edits (often: the design needs real
photography it doesn't have).

## Stage 3 — Deliver (polish)

Goal: subtract. AI adds and rarely removes — the fix list at this stage is almost always
subtraction. Apply passes one at a time, screenshot after each, stop for confirmation.

1. **Cut dead weight** — re-check each screen against its plan. Does this element carry
   information, or fill space? Cut filler: redundant counters, labels stating the default
   case, decorative rules, watermarks, buttons and labels that crowd out content. On the first
   screen, compare how much is UI vs. actual content. Swap
   custom buttons, fields, and controls for the platform's native components unless the
   custom one does something the native one can't.
2. **AI-tells pass** — `references/ai-tells-checklist.md`. Try the alternative, show both.
3. **Copy rewrite** — AI copy is placeholder, like Lorem ipsum. A human rewrites every line
   before shipping. Never auto-finalize copy.
4. **Sync to Product Spec (`specs/product/`) & Handoff to `product-loop-engineering`** — Once a design is accepted (either after Discover/Define or after Deliver), if a product spec exists in `specs/product/`, update its `## UI Design & Mocks` section with the chosen design direction, mock source path(s), and final screenshot path(s) so `product-loop-engineering` can build and verify UI units against them.

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

- Product surface: screen plans shown and confirmed before Discover.
- Discover: N seeded options, stops for a pick.
- Define: reference set shown once; before/after, score and the user's notes; stops after every
  critic pass.
- Deliver: one pass at a time, stops after each.
- A real screenshot, inline, at every point above.
- No invented features, fields, or data — ever, including in mockups.
- Nothing auto-advances without `auto-advance: true`.
