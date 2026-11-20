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
| **0 · Set up** | Spec check, taste, real content, brand kit (if a brand exists), screen plan, reference images | Answers taste questions; says what the brand kit fixes; edits the screen plan; swaps references | The user OKs the brand kit, the screen plan (product surface) and the reference set |
| **1 · Explore** | Two forks. **Seeds:** N builders each turn a random seed into a direction card; collisions are re-rolled; then each builds. **Concepts:** an idea list → the user picks and reacts → sharpened concepts → each builds | Chooses the fork(s). Concepts: picks ideas, reacts, OKs the concepts. Then picks one result, or a mix ("A's colour, C's layout") | A direction is picked |
| **2 · Refine** | Rounds: critic scores the pick → builder applies fixes + user notes | Reacts to each round: notes, then accept / another round / back to Explore | **The user accepts.** The score is a guide, not the exit |
| **3 · Polish & hand off** | Three subtraction passes, then spec sync | Approves each pass; rewrites the copy | All three passes approved, copy has a human pass, spec's UI section updated |

Start every message with "Stage N · Name" (plus "· round R" in Stage 2), progress updates
while builders or the critic run included — never a bare stage name. Folders match: `mocks/1-explore/`,
`mocks/2-refine/`, `mocks/3-polish/`.

**At the start of each stage**, also add one line on what it will ask of the user ("Stage 2: I'll show
a round, then ask for notes — point at things on the screen") and the settings in effect.
Don't silently pick and proceed.

### Status block — end every stop with it

Every checkpoint ends with this block as plain text. It is the only place the user is asked
anything, so it must say exactly what to reply. A user who reads only the block should know
what is being decided and what to type.

```
Stage 1 of 3 · Explore
Done: 3 directions built (A, B, C) · links above
Decide:
  Q1. Which direction do we refine? Default: A
  Q2. Mix in anything from the others? Default: no
Reply with:
  "1"  → refine A as is [default]
  "2"  → build another batch of 3 directions
  or plain words for Q1/Q2, e.g. "C, with A's colours"
Jump anytime: "skip to polish" · "back to explore" · "one more round" · "stop here"
```

- **Decide** lists every open decision that blocks the next step, one numbered question per
  line, each with its default answer. Include taste questions, the Explore
  fork, and must-not-show. If nothing is open, write `Decide: nothing — just pick below`.
- **Reply with** lists the exact replies, the default first and marked `[default]`, each
  with where it leads. End with one plain-words example that answers the questions.
- Replying "1" (or "ok") accepts every default in **Decide** and the first option.
- Stage 2 adds a `Score:` line after **Done**.
- Keep the **Jump anytime** line in every block.

When the user jumps or stops early, still send the block, naming what was skipped (e.g.
`Stage 3 · Polish — skipped by user`).

The status block holds the only questions in the message. Don't ask anything above it; anything unresolved that doesn't block the next step goes in DESIGN-LOG.md under **Open questions**.

### Review before deciding — present, then end the turn

The user needs time with the output before choosing. A pop-up question covers the screen and
demands an answer before they've opened anything, so this skill never uses them
(no AskUserQuestion).

- Present the output, then the status block as text, then **end the turn**. The user reviews at
  their own pace and replies with a number or plain words ("C, but with A's colours"; "2").
- Make the output easy to open, not just to look at: link each mock file, and serve the folder
  (`python3 -m http.server`) and give the `http://localhost:…` URL for each page. A downscaled
  side-by-side screenshot is for comparing, not for judging detail.
- Taste questions, the Explore fork, and clarifications all go in the status block's
  **Decide** list.

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
| Platform (product surface) | `desktop web` / `mobile web` / `iOS` / `Android` | Infer from the spec's constraints; ask in the Stage 0 status block if unclear. A mobile web app also needs its look: `mobile web · iOS` (default) or `mobile web · Android`. Every phone platform is built mobile native |
| Explore fork | `seeds` / `concepts` / `both` | Asked in the Stage 0 status block's **Decide** list. Seeds need nothing from the user; concepts take two extra stops but carry the user's taste |
| Variant count (N) | integer | `3` per fork |
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
The seed fork of Stage 1 doesn't use them — variety there comes from the seed. The concept fork does.

**3. Go get the product's actual content if they exist — real names, real copy, real photographs.** Query
the database, read the fixtures, look in the image directory. This is the highest-leverage
step in the whole skill and the easiest to skip.

**4. Brand kit** — only when a brand already exists: an accepted marketing page from an earlier
run, the live site, or design tokens in the codebase. See *Brand kit* below.

**5. Screen plan** (product surface only) — below.

**6. Reference set** for the Stage 2 critic — see *Reference set* under Stage 2. Gather it
now so Stage 2 starts straight into round 1.

**Exit Stage 0** when the user OKs the brand kit (if any), the screen plans and the reference
set. Status block, stop.

### Brand kit — fix the brand, vary the rest

When a brand already exists, a seed that picks colours wastes itself: the colours get replaced
later and the variants collapse into one look. Fix the brand up front and let the seed vary
everything that's still open.

1. Pull the palette: `scripts/extract_palette.py <page.html>` (or a screenshot). Give each colour
   a role — background, surface, tint, text, secondary text, primary action, selected state,
   links, status/warning, any category colours. Check every text/background pair with
   `--contrast`; drop or restrict pairs that fail (e.g. "accent text on white only").
   **Product surface: translate the brand into app roles.** Page background is white `#FFFFFF`,
   or a neutral system grey for grouped lists. The brand's ground colour becomes an optional
   secondary surface (sheets, grouped-list backgrounds). The accent marks the primary action,
   the selected state and links. Category colours become small labels or dots. One status
   colour marks items that need attention.
2. Note the fonts (display, body) and the signature motifs (texture, shapes, handwriting,
   illustration style).
3. Write `BRAND.md` next to the mocks: the role table with ratios, the fonts, the motifs.
4. Ask in the status block which parts are fixed. Default: **palette and roles fixed; fonts and
   motifs open** — type is one of the axes that keeps variants apart.
5. **Colour budget (product surface):** neutrals and photos fill the screen; colour appears as
   1–3 small pops per screen, for the primary action, the selected state and one status.
   Photos carry the colour. Write it into `BRAND.md`.

In Stage 1 the fixed parts go into every brief as a **Brand kit (fixed)** block. It's a
constraint like the data model, not taste — TASTE.md and the reference set still stay out. The
seed then varies the open axes (see the product brief template):
- **Pop placement** (product surface) — where the few colour pops go: *action-led* (accent on
  the primary action), *selection-led* (accent on the selected tab and active item), or
  *category-led* (small category labels carry the colour).
- **Colour placement** (marketing surface) — how much of the brand colour is on screen and
  where: *quiet* (neutral ground, accent on actions only), *tinted* (category colours as tabs,
  labels, panels), *bold* (brand colours as large surfaces).
- **Type pairing** — brand display face, brand body face only, or a contrasting companion
  (unless the user fixed fonts).
- **Component shape** — corners, outline vs. fill, tabs vs. segmented control vs. chips.
- **Photo scale & density** — thumbnail rows, large photo cards, or editorial full-bleed.
- **Motif strength** — none, subtle (one touch per screen), or strong.

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

Two ways to push past the model's average, run as separate forks. The user picks one or both
in the Stage 0 status block:
- **Fork A · Seeds** (steps 1–4): variety comes from a random string. Needs nothing from the
  user; good at surprising. Folders: `1-explore/<v>/`.
- **Fork B · Concepts** (below step 4): variety comes from the user steering ambitious ideas.
  Two extra stops; results carry the user's taste. Folders: `1-explore/concepts/<v>/`.
With both, present all results together, labelled by fork.

## Fork A · Seeds

### 1. Directions — one random seed per variant
The model can't act randomly or out-think its own averages, so the push has to come from
outside. Draw N long random alphanumeric strings with a shell script
(`python3 -c 'import secrets,string;print("".join(secrets.choice(string.ascii_letters+string.digits) for _ in range(40)))'`).
Each builder gets one string and looks closely at it — subpatterns, repeated characters,
case shifts, special numbers — to define a creative direction (color, layout, type, mood).
The string never appears in the UI. The user reacts to pixels, not concepts: direction cards
(step 3) are a duplicate check for you, not a menu for the user. With a brand kit, the seed
doesn't pick colours; it picks the open axes listed under *Brand kit*.

### 2. Write briefs — one template per surface
Marketing: `references/builder-brief-marketing.md`. Product: `references/builder-brief-product.md`.
- **Leave out the user's taste, TASTE.md and the reference set.** Shared taste words ("warm,
  playful") outweigh a random string, and every builder lands on the same most-likely page.
  Taste and references enter in Stage 2.
- The orchestrator writes **zero prose copy.** Builders write their own.
- List what to build from — the complete set of features, fields and data the product has (**Build only from these**).
- **Product surface:** product facts as bullets (≤60 words, no adjectives), real content, and
  the screen plans verbatim. Function first — the seed shapes personality (colour, type,
  density, component shape), not structure. App screens sit on a white, neutral ground; the
  photos and 1–3 small colour pops carry the brand. Add the **Brand kit (fixed)** block when
  Stage 0 made one.
- **Phone screens are mobile native.** If the mocks are phone screens — native app or mobile
  web app — they must look and behave like a native app on the chosen platform (iOS or
  Android), not a shrunken web page. The template's *Mobile native* section is mandatory for
  every phone brief: fill in the platform, keep the matching platform block, and add the
  *Mobile web app* rules when it ships as one (installed standalone app, no browser chrome,
  only what a web app can do). The critic scores **Native feel** for phone screens.
- **Marketing surface:** product facts; leave room to go big and strange. The brief is split:
  the **hero** (first 1440×900 screen) is where the seed goes all the way; the **rest of the
  page** is functional, in the hero's palette and type. Fill **Must not show** — by default no
  app screens or phone frames, since they become every builder's easy hero. Ask the user
  before allowing them.
- **No photo, no fake:** where a photo belongs and none exists, builders use a captioned photo
  slot (both templates). Don't bundle stock or placeholder images in the skill — the same
  stand-in on every project becomes its own sameness.
- **Don't** paste `references/ai-tells-checklist.md` in as bans — banning makes the model
  swap in stranger substitutes. Tells are handled in Stage 3.

### 3. Translate seeds, then dedupe — before anyone builds
Builds are slow; cards are fast. Catch collisions on cards.
1. Spawn N builders with the template's **Phase 1** only. Each returns a direction card and
   waits.
2. Compare the cards. Two cards **collide** when any of these match:
   - marketing: the same **saturation/energy** (muted / mid / loud) — loudness reads as sameness first;
   - product: the same **neutral** *and* the same **pop placement**;
   - marketing: the same **hero composition** (type wall, full-bleed image, split, one
     object…) — colour and type changes on the same first screen still look like one page;
   - product: the same **density** *and* the same **component shape** — the layout is fixed
     by the screen plan, so these carry the difference;
   - the same hue family *and* the same display-type class;
   - the same working name.
   With N > 3, energy and composition (or density) may repeat once each; nothing else changes.
   **With a brand kit** hue is fixed, so swap the colour rules for these. Two cards collide when:
   - the same **pop placement** (product) or **colour placement** (marketing) *and* the same
     **component shape**;
   - the same **photo scale** *and* the same **density**;
   - the same **type pairing**;
   - the same working name.
3. For each collision, keep one and re-roll the other: send it a fresh seed plus the kept
   card as "not that". Re-check. Cap at 2 re-rolls per variant, then build anyway and note it.
4. Send each builder **Phase 2** as a follow-up message, listing the other final cards.

### 4. Build, screenshot, present
- Builders run on the builder model, each in its own context (the same agent from step 3).
- If two variants still come out looking alike, rebuild one with an explicit "not that."
- Screenshot all N, present them side by side with links (see *Review before deciding*), and
  end the turn. Marketing: the side-by-side is the 1440×900 hero shots; link the full pages.

## Fork B · Concepts — ambitious prompts the user steers

A bold, specific idea ("each section is a still from a video game") gives the builder a vision
to decide from instead of averaging. Asking the model for ideas alone gets the same ideas
everyone gets; the user's reactions are what make them unique.

1. **Idea list.** Write 20–30 design-language ideas, one line each, no detail — they're there
   to spark the user's imagination, not to be specs. Spread wide: games, interiors, art and
   installations, print and packaging, machines and objects, places, eras, materials. Include
   a few that sound like they can't work. Skip the first ideas anyone would have for this
   product category. Present as text and end the turn.
2. **The user picks and reacts.** Up to N favourites, each with reactions in plain words: what
   they picture, what feels tacky, what to keep or avoid. Fewer than N is fine; offer to fill
   the rest from Fork A.
3. **Sharpen.** Turn each pick plus its reactions into a concept of 4–6 lines: the idea; how it
   lands in the hero (marketing) or across the screens (product); what to avoid, in the user's
   words; and how far to take it — consistent touches that land the look without going
   overboard. TASTE.md may inform it; the reference set stays out. Show the concepts and stop
   for edits or an OK.
4. **Build.** One builder per concept, with the surface template's **concept** Phase 1 (the
   concept, verbatim, in place of the seed), then the usual dedupe and Phase 2. A collision
   here means a builder flattened its concept toward the safe middle: send it back with
   "push the concept further; not that: <other card>" — no new seed.
5. **Screenshot and present** as in Fork A step 4. Save the concepts that didn't work in
   DESIGN-LOG.md; they're worth retrying when newer models come out.

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
screenshots make it concrete. Gather **4 references** in Stage 0, once per design, and reuse
the same set every round so scores stay comparable.

Match on **broad register, not the exact niche.**:

- **Audience:** consumer vs. enterprise / B2B
- **Purpose:** functional (get a job done) vs. entertainment / expressive
- **Who it's for:** e.g. Gen Z vs. Gen X / boomer, novice vs. expert
- **Platform:** mobile app, desktop web, marketing site

Name the register in one line ("consumer, functional, Gen Z-leaning, mobile") and pick
well-made products from anywhere in that space. Broad references give the critic a quality
bar without pulling the design toward a competitor's layout.

Sources, in order:

1. **User-supplied** — images they drop in, or products they named. Always first.
2. **Live products** — search for current, well-regarded products in that register (don't
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
("a stair of balconies"); builders take that literally. A good colour entry reads like "App
screens: white neutral ground, colour as small pops for action, selection and status."

### Brand pass (product surface, when a marketing page was accepted after Stage 1)

Only when no brand kit went into Stage 1 — e.g. the marketing page was accepted after the app
directions were built. If the brand existed at Stage 0, use the *Brand kit* instead.
Bring the marketing site's colors into the product — not its fonts or layout. Run
`scripts/extract_palette.py <marketing.html>` to pull its colors, assign them roles in the
product (primary action, accent, "needs checking", background tint, selected state) using the
same translation and colour budget as the *Brand kit* (white ground, 1–3 small pops), and
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

- Stage 0: brand kit (when a brand exists), screen plans (product surface) and reference set
  shown and confirmed.
- Stage 1: N seeded options, deduped on direction cards before building, stops for a pick.
- Stage 2: before/after, score and the user's notes; stops after every critic pass.
- Stage 3: one pass at a time, stops after each; ends with the handoff summary.
- Every stop ends with the status block as text, then the turn ends — no pop-ups; the block's
  **Decide** list holds every question and **Reply with** says what to type; DESIGN-LOG.md updated at every stop.
- Every message starts with the stage label, progress updates included; an early exit still
  ends with the status block and the handoff summary.
- A real screenshot, inline, at every point above.
- No invented features, fields, or data — ever, including in mockups.
- Nothing auto-advances without `auto-advance: true`.
