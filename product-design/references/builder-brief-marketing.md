# Stage 1 builder brief — marketing surface (homepage, landing page)

One brief per variant. Fill the `<…>` slots and paste the result as the builder's whole prompt.
Run it in two phases on the same agent: **translate**, then **build** (sent later as a follow-up
message, so the builder keeps its own direction card in context).

**Leave out on purpose:** the user's taste, TASTE.md, the reference set, and reference product
names. In Stage 1 variety comes from the seed alone. Shared taste words pull every builder to
the same "most likely" page. Taste enters in Stage 2.

**Where the effort goes:** the hero (the first screen) is where variants differ and where the
user decides. The rest of the page is functional: it carries the hero's palette and type and
says what the product does, plainly.

**Hero tiers.** With the Hero range setting on `tiers`, give each builder one tier in Phase 1
(**Your hero tier**). The tier sets the composition; the seed sets everything else.

---

## Phase 1 · Translate (send first)

You are a designer-builder. You will make ONE marketing landing page as a static HTML mock.
First, only choose the direction. Don't build yet.

### Your seed
<40-char random string>

Look closely at the string: subpatterns, repeated characters, case shifts, digits, special
numbers. Define a creative direction from it. The string never appears in the UI. Other
builders have other seeds. Commit to where yours points, not to the safe middle.

### Your hero tier
<one of the three, verbatim:>
- **Tier 1 · Classic split.** Headline, supporting line and call to action on the left; one
  strong visual on the right. Your seed decides the visual, the palette, the type and the
  background. Aim for instant clarity, executed beautifully.
- **Tier 2 · Split, extended.** The classic reading order — headline, line and call to action
  on the left — with the visual running past its box: a moving gradient, light or texture
  behind the whole first screen, or a graphic that bleeds off the edge and flows under the next
  section. Your seed decides what extends, how it moves, the palette and the type.
- **Tier 3 · Immersive.** A full-bleed photo, video loop or animation fills the first screen and
  is the hero; the headline and call to action sit over it. Your seed decides the image or
  motion idea, the type treatment and how the copy sits on the image.

### Product facts
<≤60 words, bullets, no adjectives>

### Build only from these
<the complete set of features, data and proof the product has, and the call to action as it stands (e.g. waitlist if not launched) — every claim on the page comes from this list>

### What the hero shows
<Default: "The hero shows the outcome the product gives — people, food, place, type or
graphics. Product UI, if the user wants it, sits further down the page." Change only if the
user asks for product UI in the hero.>

**Saturation / energy** is how loud the colour is: *muted* (dusty, greyed, low contrast),
*mid* (clear colour, one accent on calm neutrals), *loud* (several saturated colours at full
strength). **Hero composition** is how the first screen is built before colour or type: e.g.
*type wall* (the headline is the image), *full-bleed image* with type over it, *split* (two
halves), *one object* (a single big graphic in the middle), *collage* (several pieces
overlapping), *off-grid* (one element pushed to an edge, lots of empty space). These are
examples, not a menu — read both from your seed. With a hero tier, the tier sets the
composition; read the energy and the way you build your tier from the seed.

### Reply with a direction card, and nothing else
Write it to `<mocks>/1-explore/<v>/direction.md` and return it:

```
Base hue family: <e.g. blue, green, red-orange, neutral>
Light/dark balance: <mostly light | mostly dark | split>
Saturation / energy: <muted | mid | loud>
Palette: <4–6 hex codes, each with a role>
Display type: <font> — class: <serif | grotesk | geometric | display/novelty | mono | script>
Body type: <font>
Hero tier: <1 classic split | 2 split, extended | 3 immersive — or "seed" without tiers>
Hero composition: <named plainly — e.g. type wall | full-bleed image | split | one object | collage | off-grid | something else>
Hero: <one line: what fills the first screen and where the headline and call to action sit>
Imagery: <photo | type-only | graphics (shapes, pattern, texture, type as image) | mix>
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
<string>. Not that: <the other card's palette, energy, type class, hero composition, name>. Keep your hero tier. Send a new card, then wait.">

### Other variants (avoid drifting toward them)
<each other variant's card: hero tier, palette, energy, type class, hero composition, name — one line each>

### Real content
<names, copy, photos from Stage 0 step 3; or "none yet">

### Imagery
- <Image tool available? Say which, and use it for the hero image. If not: say "none".>
- Real photography only from verified URLs (`curl -sI` returns 200), or the user's own.
- No code-drawn fake photos. Where a photo belongs and none is available, use a **photo
  slot**: a solid block in a palette colour, at the real image's size and crop, with a short
  art-direction caption in small type, e.g. `PHOTO · overhead, open cookbook, flour on the
  counter, late light`. The slot stands in for that photo; the critic judges it as described.
- Graphics you draw are fine: shapes, pattern, texture, type used as image.
- <What the hero shows, repeated from Phase 1.>

### Part 1 · Hero (the first screen, 1440×900) — most of your effort
- This is where your seed goes all the way. Everything visible at 1440×900 counts.
- Holds: product name, headline, one supporting line, the call to action, and the hero visual.
  Nothing else needs to be above the fold.
- Make it unmistakably yours: it should not look like the other variants' heroes.
- Build your hero tier. Tiers 2–3 with motion: CSS animation or a looping video, with a strong
  first frame — the screenshot shows that frame. Check the motion with temporary copies that
  set a negative `animation-delay` (e.g. -3s, -9s) to freeze later moments, screenshot each,
  then delete the copies. (Headless Chrome's virtual time doesn't advance CSS animations.)

### Part 2 · Rest of the page — functional
- Same palette and type as the hero; quieter. Clear, plainly laid out sections, no new tricks.
- Sections: <list what the page must cover, from the product facts — e.g. how it works in
  3 steps, what it does, who it's for, the call to action again, footer>. Builders write
  their own copy.
- Keep it short: each section says one thing.

### Technical
- One file: `<mocks>/1-explore/<v>/index.html`, inline CSS, no JS frameworks (Google Fonts OK).
- Width 1440px. No `vh` units or `min-height: 100vh` (screenshots use a tall window).
  Whole page 2000–4000px.
- Check your work with two screenshots:
  - Hero: `"<chrome>" --headless=new --disable-gpu --hide-scrollbars --window-size=1440,900 --virtual-time-budget=6000 --screenshot=<mocks>/1-explore/<v>/hero.png file://<mocks>/1-explore/<v>/index.html`
  - Full page: same command with `--window-size=1440,<page height>` and `full.png`.
  Read the PNGs, fix anything broken, repeat. Re-screenshot after your last edit.

### Report back (short)
1. Anything you changed from your card, and why.
2. Rendered height at 1440px.
