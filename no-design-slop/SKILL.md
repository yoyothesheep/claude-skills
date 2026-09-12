---
name: no-design-slop
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

# no-design-slop

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

## Before anything: find the real content

**Go get the product's actual content first — real names, real copy, real photographs.** Query
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

**1. Draw the variants' directions — don't choose them.** Assign each variant a combination
drawn randomly, *without replacement* so no two collide on an axis:

| Axis | Draw from |
|---|---|
| Layout skeleton | full-bleed type / split-screen / list-as-hero / off-grid editorial / photo-mosaic / centered column / dense index / card carousel |
| First thing the eye lands on | a photograph / a list / one sentence / a grid |
| Type | all-grotesk / serif display + mono / all-mono / condensed sans + wide serif |
| Color | near-black + paper + one accent / duotone / full-bleed photo + white type / monochrome |
| **Domain transplant** | a non-software visual grammar to steal composition from: seed catalog / Swiss pharmaceutical brochure / subway wayfinding / record sleeve / museum wall label / mid-century menu / field guide / newspaper front page / airline safety card / scoreboard |
| **Dare** (falsifiable) | one element ≥4× larger than a cautious designer would pick / zero rounded corners / one photo full-bleed across ≥60% / no button above the fold / two colors total plus photography / no icon or chevron anywhere |

```bash
p3() { printf '%s\n' "$@" | sort -R | head -3; }   # 3 distinct values per axis
```

The domain transplant carries a whole visual grammar — composition, density, type, color — so
it moves a design far more than any adjective. The dare must be **objectively checkable**;
"be bold" has no failure condition, so a model satisfies it by nudging something off-center.

*A random hex string as a seed does not work* and shouldn't be used. It's semantically empty
but formally suggestive — it reads as a catalog number, so every builder decodes it the same
way and converges harder. If you want a string seed, draw real words
(`sort -R /usr/share/dict/words | head -4`), which at least differ in meaning.

**2. Write briefs under contract.** Whatever the orchestrator writes identically across
variants becomes the dominant signal and overrides the drawn direction. So:
- Product facts go in as **bullets, ≤60 words, no adjectives, no sample phrasings.**
- The orchestrator writes **zero prose copy.** Builders write their own; vivid phrasing in a
  brief gets reproduced verbatim in the output, and in every variant at once.
- List what the *other* variants are taking, so each avoids drifting there.
- Paste `references/ai-tells-checklist.md` in as banned patterns. It's short, and applying it
  only at Deliver means every variant is born with the same tells.
- State what must not be invented — features, fields, or data the product doesn't have.
- On a re-pass: say explicitly that the existing design system may be broken. Anchoring to a
  generic system guarantees a generic result.

**3. Build each variant as an isolated subagent** on the builder model, fresh context.

**4. Gate on diversity before showing anything.** Compare the N screenshots yourself. If two
share a layout skeleton, palette family, and type pairing, rebuild the loser with an explicit
"not that." Shipping near-identical variants wastes the user's judgment.

**5. Critique before presenting.** Run a critic pass per variant (below). Don't hand the user
unjudged first drafts — that makes them the first line of quality control.

**6. Screenshot all N, show side by side, stop.** User picks, blends, or rerolls.

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
