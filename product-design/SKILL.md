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
| Critic loop ceiling | integer, per "keep going" answer | `3` |
| Builder & critic model | any available | `opus` for both — this is a taste task, not a cost-optimization one |
| Polish passes | subset of {cut dead weight, AI-tells, copy rewrite} | all three, one at a time |

## Before anything: check the product spec, infer vibes & find real content

**1. Check `specs/product/` (works with `product-scoping` & `loop-engineering`):**
Look in `specs/product/` for an existing product specification.
- **If a product spec exists:** Read the target users/personas, goals, scoped features, and Key User Flows ($F_1..F_m$) so the mocks reflect the exact scoped screens and fields without inventing unrequested features.
- **If no product spec exists:** Ask if the user wants to scope one first via `product-scoping` or jump straight into designing (do **not** require a spec if they want to design directly).

**2. Infer candidate vibes from users/personas & ask for user preferences:**
Before generating variants, use the target audience, user stories, and domain context to **infer 2–3 distinct visual vibes/directions** that would fit how and where those users use the product (e.g., kitchen glanceability at arm's length vs. editorial cookbook warmth vs. high-contrast utility checklist). Ask the user if they have any thoughts, reference apps, or vibe preferences before or alongside Stage 1.

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

### 2. Archetype Diversity Across Mediums
Ensure variants span genuinely distinct visual grammars appropriate to the product medium (especially digital and mobile products):

| Archetype / Grammar | Key Visual Attributes | Typical Medium / Reference |
|---|---|---|
| **Clean Native / HIG** | Fluid squircle cards, subtle multi-layer elevation, frosted glass/blur tab bars, native segmented controls, crisp optical whites (`#FFFFFF`, `#F8F9FA`) | Apple Reminders, iOS 18 System, Things 3 |
| **High-End Editorial** | Large hero photography, refined editorial serif headlines, generous whitespace, delicate thin rules, subtle tinted surfaces | NYT Cooking, Kinfolk, Cereal, Crouton |
| **Playful Modern Consumer** | Saturated punchy accent pigments (cobalt, tangerine, sage), friendly rounded typography, soft 16–20px radii, tactile pill badges | Duolingo, Headspace, Opal, Linear Mobile |
| **Minimalist Functionalism** | Pure typography & photography hierarchy, high contrast, subtle neutral grays, zero borders, compact functional density | Scandinavian furniture catalogs, Braun/Rams, Minimal Swiss |

### 3. Falsifiable Dares (without replacement)
Draw one falsifiable dare per variant to force distinct visual commitments:
- One element $\ge 4\times$ larger than a cautious designer would pick (oversized typographic/numeric anchor).
- Zero card borders (hierarchy expressed purely through whitespace, surface fills, and typography).
- Deep immersive surface (dark/inverted chassis that illuminates content).
- Full-bleed edge-to-edge media cards across the viewport.

### 4. Diversity Rejection Gate (The Circuit Breaker)
Before presenting screenshots to the user, run an automated pairwise check across the N variants:
1. **Palette Check**: If two variants share the same background family (e.g. both use beige/cream `#F4EFE6` or `#F5EDD6`), automatically reject the weaker one and re-roll.
2. **Surface & Border Check**: If two variants box every section in black `1px solid` wireframes or 0px brutalist cells, reject the weaker one.
3. **Typography Check**: If two variants rely on monospace for general consumer UI labels or brackets `[ ]`, reject the weaker one.

### 5. Write Briefs Under Contract
- Product facts go in as **bullets, ≤60 words, no adjectives, no sample phrasings.**
- The orchestrator writes **zero prose copy.** Builders write their own.
- List what the *other* variants are taking, so each avoids drifting there.
- Paste `references/ai-tells-checklist.md` in as banned patterns.
- State what must not be invented — features, fields, or data the product doesn't have.

### 6. Build, Critique, Screenshot
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
   support. Supply reference screenshots the user admires if they have any — without a visual
   bar, critics of app screens drift into product strategy and scores plateau.
3. Show the before/after screenshots, the score, and the notes.
4. **Stop.** Iterate / accept / stop. Loop unattended only to the ceiling knob, then check in
   regardless of score.

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

## No image or video generation here

There's no image/video API in this environment. Never fabricate one or claim to call one. If
a design genuinely needs generated imagery, write the user a paste-ready prompt naming
subject, style, the physical/lighting effect, and framing, tell them where to save the file,
and wait. Prefer real existing content over generated content anyway.

## Output contract

- Discover: ≥N options, diversity-gated and critiqued, stops for a pick.
- Define: before/after, stops after every critic pass.
- Deliver: one pass at a time, stops after each.
- A real screenshot, inline, at every point above.
- No invented features, fields, or data — ever, including in mockups.
- Nothing auto-advances without `auto-advance: true`.
