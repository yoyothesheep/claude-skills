---
name: product-design
description: >-
  Guides building or improving any visual/UI design (landing pages, app screens, dashboards,
  marketing pages, prototypes) through a numbered process (0 Set up, 1 Explore, 2 Refine, 3 Polish & hand off) that produces
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
"something unique" doesn't help. Variance has to be **imposed from outside** and judged by **something
that didn't build it**.

## Usage

Four numbered stages, each ending at a checkpoint where the user decides. Chain
only if the user says so (`auto-advance`). Re-invoking on an already-polished design is normal.

| Stage | What happens | What the user does | Exit when |
|---|---|---|---|
| **0 · Set up** | Spec check, taste, real content, screen plan, reference images | Answers taste questions; edits the screen plan; swaps references | The user OKs the screen plan (product surface) and the reference set |
| **1 · Explore** | N builders, each from a random seed, make N distinct directions | Picks one, or a mix ("A's colour, C's layout") | A direction is picked |
| **2 · Refine** | Rounds: critic scores the pick → builder applies fixes + user notes | Reacts to each round: notes, then accept / another round / back to Explore | **The user accepts.** The score is a guide, not the exit |
| **3 · Polish & hand off** | Three subtraction passes, then spec sync | Approves each pass; rewrites the copy | All three passes approved, copy has a human pass, spec's UI section updated |

Start every message with "Stage N · Name" (plus "· round R" in Stage 2), progress updates
while builders or the critic run included — never a bare stage name. Folders match: `mocks/1-explore/`,
`mocks/2-refine/`, `mocks/3-polish/`.

**At the start of each stage**, also add one line on what it will ask of the user ("Stage 2: I'll show
a round, then ask for notes — point at things on the screen") and the settings in effect.
Don't silently pick and proceed.

### Status block — end every stop with it

Every checkpoint ends with this block, then the choices as an AskUserQuestion (default first):

```
Stage 2 of 3 · Refine · round 2 (I check in after 3 rounds)
Done: picked direction C · round 1 applied 6 fixes + your 3 notes
Score: 6.6 (was 6.1) — a guide, not the bar for done
Next: 1. Another round [default] · 2. Accept → Stage 3 Polish · 3. Back to Stage 1 with this as baseline
```

The user can also jump at any time in plain words: "skip to polish", "back to explore",
"one more round", "stop here". List these once, in the first status block. When the user jumps or stops early, still send
the status block, naming what was skipped (e.g. `Stage 3 · Polish — skipped by user`).

### DESIGN-LOG.md — where the work stands

Keep `specs/product/mocks/DESIGN-LOG.md` (or next to the mocks): current stage and round; one
line per round (what changed, score, the user's notes); **settled decisions** (fixes applied
and kept, choices the user made); **rejected suggestions** (critic fixes the user or you
declined, with why). Update it at every checkpoint. On re-entry, read it first and open with
"You're in Stage N · Name, round R." Settled decisions and rejected suggestions go into the
critic's fixed-constraints slot every round, so it can't reverse earlier work.

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
| Stage scope | `explore` / `refine` / `polish` / `full` | `full` (Stage 0 always runs, skipping what's already done) |
| Auto-advance | `false` / `true` | `false` — pause after every stage |
| Surface | `marketing` / `product` | Infer. Marketing (homepage, landing) can go big and bold; product UI is functional first, with personality |
| Variant count (N) | integer | `3` |
| Critic loop ceiling | integer, per "keep going" answer | `3` |
| Critic references | `auto` / `user-only` / `none` | `auto` — see Stage 0 |
| Builder model | any available | `sonnet` |
| Critic model | any available | `opus` — the critic supplies the taste |
| Polish passes | subset of {cut dead weight, AI-tells, copy rewrite} | all three, one at a time |

## Stage 0 · Set up

Goal: everything the builders and critic need, gathered once. Skip any step already done
(check DESIGN-LOG.md, TASTE.md, the spec).

**1. Check `specs/product/` (works with `product-scoping` & `product-engineering`):**
Look in `specs/product/` for an existing product specification.
- **If a product spec exists:** Read the target users/personas, goals, scoped features, and Key User Flows ($F_1..F_m$) so the mocks reflect the exact scoped screens and fields without inventing unrequested features.
- **If no product spec exists:** Ask if the user wants to scope one first or jump straight into designing (do **not** require a spec if they want to design directly).

**2. Ask for the user's taste.** Reference apps or sites, vibes they like, things they hate.
Start `TASTE.md` with the answers (see Stage 2). Reference apps also feed the Stage 2 critic.
Stage 1 doesn't use them — variety there comes from the seed.

**3. Go get the product's actual content if they exist — real names, real copy, real photographs.** Query
the database, read the fixtures, look in the image directory. This is the highest-leverage
step in the whole skill and the easiest to skip.

**4. Screen plan** (product surface only) — below.

**5. Reference set** for the Stage 2 critic — see *Reference set* under Stage 2. Gather it
now so Stage 2 starts straight into round 1.

**Exit Stage 0** when the user OKs the screen plans and the reference set. Status block, stop.

### Screen plan — edit before you design (product surface only)

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

## Stage 1 · Explore — several distinct directions

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
  swap in stranger substitutes. Tells are handled in Stage 3.

### 3. Build, screenshot, present
- Build each variant as an isolated subagent on the builder model, fresh context.
- If two variants come out looking alike, rebuild one with an explicit "not that."
- Screenshot all N side-by-side, present them, stop for the user's pick.

**Exit Stage 1** when the user picks one direction (or names a mix). Log the pick in
DESIGN-LOG.md. Status block; choices: refine the pick [default] · another batch of directions.

## Stage 2 · Refine — improve the pick, in rounds

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
5. **Stop.** Update DESIGN-LOG.md, then the status block: another round [default] / accept →
   Stage 3 / back to Stage 1. Loop unattended only to the critic loop ceiling, then check in
   regardless of score. The ceiling is a check-in, not a limit.

The first time a score appears, explain it once: "Scored out of 10 against pro apps. 6–7 is
normal for a mock — you decide when it's done."

**Exit Stage 2** when the user accepts. **Recommend accepting** (make it the default choice)
when the score moved less than 0.5 over the last 2 rounds, or the critic's fixes start
reversing settled decisions. Say why in plain words: "More rounds probably won't help. What's
left is real photos and copy, which belong in Stage 3."

### Reference set (critic visual bar)

"Imagine a top studio" is a mushy bar — the model's imagined best is its average. Real
screenshots make it concrete. Gather **4 references** in Stage 0, in the same category and
platform, once per design, and reuse the same set every round so scores stay comparable.
Sources, in order:

1. **User-supplied** — images they drop in, or products they named. Always first.
2. **A design-reference tool, if one is connected and responds** (e.g. a screen-library MCP).
   Probe with one call; if it errors or returns nothing usable, move on — don't retry.
3. **Live products** — search for current, well-regarded products in this category (don't
   use a remembered list; it goes stale) and screenshot them with the Chrome command above.
   Skip any page that renders a login wall, cookie banner, or broken layout.

Show the user the set at the end of Stage 0; they can swap any. The critic sees one of
our designs alongside the references as its baseline — a moodboard for the quality bar, not a
target to copy (tell builders the same). With no usable references, it judges against how a
top studio would execute the same aesthetic.

### TASTE.md — the user's taste, kept across rounds

One file per project (template: `references/taste-template.md`): reference images and sites,
what the user loves, what they don't, and product facts they keep correcting ("no days of
the week"). It goes into every Refine brief and into the critic's fixed-constraints slot, so
the critic stops attacking choices the user made. Write entries as look and feel — palette,
type, texture, spacing, shape language, mood — never as what a screen or element *is*
("a stair of balconies"); builders take that literally.

### Brand pass (product surface, when an accepted marketing page exists)

Bring the marketing site's colors into the product — not its fonts or layout. Run
`scripts/extract_palette.py <marketing.html>` to pull its colors, assign them roles in the
product (primary action, accent, "needs checking", background tint, selected state), and
check every text/background pair with `--contrast`. Give the builder the palette as a fixed
constraint — colors in these roles; type and layout stay the product's own — then run the
normal critic round. Do it in Stage 2, not Stage 1: in Stage 1 the seed sets the palette.

**Apply the critic's cuts in the next round** — don't defer them to Stage 3. Clutter left in
keeps drawing the critic's attention and the score stays flat.

**When the critic attacks the chosen aesthetic itself**, don't strip what the user chose.
It's usually reacting to the stack of defaults around that choice — remove the stack, keep
the choice.

**Weigh the critic, don't obey it.** It's judging a picture with no product context. When it
proposes something the data can't support, or contradicts a convention the rest of the app
already uses, say so and skip it — tell the user you did, and log it under rejected
suggestions so the next critic doesn't re-propose it. A flat score across rounds
usually means the real lever isn't reachable by layout edits (often: the design needs real
photography it doesn't have).

## Stage 3 · Polish & hand off

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
4. **Sync to Product Spec (`specs/product/`) & Handoff to `product-engineering`** — Once a design is accepted (after Stage 2 or Stage 3), if a product spec exists in `specs/product/`, update its `## UI Design & Mocks` section with the chosen design direction, mock source path(s), and final screenshot path(s) so `product-engineering` can build and verify UI units against them.

**Exit Stage 3** when all three passes are approved, the copy has had a human pass, and the
spec is synced. Close with a handoff summary: final screenshot, the direction in one line,
file paths, what changed in the spec, and what's still open for the user (copy lines not yet
rewritten, real photos still missing). Next step: `product-engineering`.
If the user locks the design early or skips stages, still sync the spec and close with this
handoff summary.

## Re-entering on an existing design

Normal. Read DESIGN-LOG.md and say where things stand first. Treat the current state as the
baseline: Stage 1 branches off the winner, Stage 2 re-critiques with fresh context, Stage 3
re-checks tells since content moved.

## Image & video generation — use if available, else skip

Coding agents default to code-drawn gradients, shapes, and patterns — a top AI tell. Check
for a real generation tool first: a built-in image tool, the Codex CLI, or an API key the
user has provided (OpenAI/Gemini for images, fal.ai for video).

- **Available:** use it in Stages 2–3 for imagery real content can't supply. Images: hero
  visuals, textures, illustrations. Video: looping graphics on a solid background (chroma-key
  or matte it out to layer in the UI), or keyframe-interpolated transitions scrubbed on
  scroll. Keep keys local — never write them into product code. Verify motion frame-by-frame
  in the browser, not from one screenshot.
- **Not available:** skip it. Never fabricate a tool or claim to call one.

Real existing content still beats generated content.

## Output contract

- Stage 0: screen plans (product surface) and reference set shown and confirmed.
- Stage 1: N seeded options, stops for a pick.
- Stage 2: before/after, score and the user's notes; stops after every critic pass.
- Stage 3: one pass at a time, stops after each; ends with the handoff summary.
- Every stop ends with the status block; DESIGN-LOG.md updated at every stop.
- Every message starts with the stage label, progress updates included; an early exit still
  ends with the status block and the handoff summary.
- A real screenshot, inline, at every point above.
- No invented features, fields, or data — ever, including in mockups.
- Nothing auto-advances without `auto-advance: true`.
