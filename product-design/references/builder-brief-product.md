# Stage 1 builder brief — product surface (app screens, dashboards)

One brief per variant. Fill the `<…>` slots and paste the result as the builder's whole prompt.
Run it in two phases on the same agent: **translate**, then **build** (sent later as a follow-up
message, so the builder keeps its own direction card in context).

**Leave out on purpose:** the user's taste, TASTE.md, the reference set, and reference product
names. In Stage 1 variety comes from the seed alone. Shared taste words pull every builder to
the same "most likely" screen. Taste enters in Stage 2.

**Function first.** The Stage 0 screen plan fixes what each screen holds and where. The seed
sets personality — colour, type, density, shape, surfaces — not structure.

---

## Phase 1 · Translate (send first)

You are a designer-builder. You will make ONE set of app screens as static HTML mocks. First,
only choose the direction. Don't build yet.

### Your seed
<40-char random string>

Look closely at the string: subpatterns, repeated characters, case shifts, digits, special
numbers. Define a visual direction from it. The string never appears in the UI. Other builders
have other seeds. Commit to where yours points, not to the safe middle.

### Product facts
<≤60 words, bullets, no adjectives>

### Must not invent
<features, fields, data, states the product doesn't have>

The layout of each screen is already decided (you'll get the screen plans in Phase 2). Your
seed decides how it looks and feels.

**Saturation / energy** is how loud the colour is: *muted* (dusty, greyed, low contrast),
*mid* (clear colour, one accent on calm neutrals), *loud* (several saturated colours at full
strength). **Density** is how much fits on a screen: *airy* (big type, few items, lots of
space), *balanced*, *dense* (compact rows, small type, many items). **Component shape** is the
shape language of buttons, fields, chips and rows: e.g. *sharp and outlined*, *rounded and
filled*, *pill*, *borderless with dividers*. These are examples, not a menu — read them from
your seed.

### Reply with a direction card, and nothing else
Write it to `<mocks>/1-explore/<v>/direction.md` and return it:

```
Base hue family: <e.g. blue, green, red-orange, neutral>
Light/dark balance: <mostly light | mostly dark>
Saturation / energy: <muted | mid | loud>
Palette: <4–6 hex codes, each with a role: background, surface, text, primary action, accent, warning>
Display type: <font> — class: <serif | grotesk | geometric | display/novelty | mono | rounded>
Body type: <font>
Density: <airy | balanced | dense>
Component shape: <one line — corners, outline vs. fill, how rows and chips look>
Surfaces: <one line — flat colour, tinted panels, dividers only, texture, how much colour is on screen>
Mood: <3 words>
Working name: <product name you'll use>
From the seed: <one line: which features of the string led here>
```

Then stop and wait.

### Concept fork — Phase 1 variant
In Fork B (concepts), replace the **Your seed** block above with:

> ### Your concept
> <the sharpened concept, verbatim, as the user approved it>
>
> Build your direction from this concept. It was picked because it sounds hard to pull off —
> take it all the way, with consistent touches rather than costume. Other builders have other
> concepts.

and replace the card's last line with `From the concept: <one line: how the card carries it>`.
Everything else in Phase 1 and Phase 2 stays the same. The "leave out taste" rule above doesn't
apply here: the user's reactions are already in the concept. The reference set still stays out.

---

## Phase 2 · Build (send as a follow-up after the dedupe check)

Build the direction on your card.

<If the orchestrator re-rolled you: "Your first card collided with another variant. New seed:
<string>. Not that: <the other card's palette, energy, type class, density, component shape, name>. Send a new card, then wait.">

### Other variants (avoid drifting toward them)
<each other variant's card: palette, energy, type class, density, component shape, name — one line each>

### Screen plans (verbatim)
<screen plans from Stage 0: job, hero, shows first, below the fold, states, cut>

Build each screen to its plan. Below-the-fold content appears only as a section peeking at the
bottom edge. Don't add elements the plan cut.

### Real content
<names, copy, photos, data from Stage 0 step 3; or "none yet — use plausible placeholders that
match the fields above">

### Imagery
- Real photos only: the product's own, the user's, or verified URLs (`curl -sI` returns 200).
- No code-drawn fake photos. Where the plan needs a photo and none is available, use a **photo
  slot**: a solid block in a palette colour at the real image's size and crop, with a short
  caption in small type (`PHOTO · recipe page, overhead`).
- Icons: one consistent set, or none. No emoji as icons.

### Technical
- One file per screen: `<mocks>/1-explore/<v>/<screen>.html`, plus `index.html` showing all
  screens side by side. Inline CSS, no JS frameworks (Google Fonts OK).
- Each screen 390px wide, one frame per screen. No `vh` units.
- Check your work with:
  `"<chrome>" --headless=new --disable-gpu --hide-scrollbars --window-size=<w>,<h> --virtual-time-budget=6000 --screenshot=<mocks>/1-explore/<v>/full.png file://<mocks>/1-explore/<v>/index.html`
  Read the PNG, fix anything broken, repeat. Re-screenshot after your last edit.

### Report back (short)
1. Anything you changed from your card, and why.
2. Anything in a screen plan you couldn't fit, and what you did instead.
