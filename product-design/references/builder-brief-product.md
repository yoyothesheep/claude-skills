# Stage 1 builder brief — product surface (app screens, dashboards)

One brief per variant. Fill the `<…>` slots and paste the result as the builder's whole prompt.
Run it in two phases on the same agent: **translate**, then **build** (sent later as a follow-up
message, so the builder keeps its own direction card in context).

**Leave out on purpose:** the user's taste, TASTE.md, the reference set, and reference product
names. In Stage 1 variety comes from the seed alone. Shared taste words pull every builder to
the same "most likely" screen. Taste enters in Stage 2.

**Function first.** The Stage 0 screen plan fixes what each screen holds and where. The seed
sets personality — accent, type, density, shape, surfaces — not structure. Build on a white,
neutral ground. Food photos and real content carry the colour; the accent appears as a few
small pops that mark what the user can act on.

**Brand kit runs.** When Stage 0 made a `BRAND.md`, include the **Brand kit (fixed)** block in
Phase 1, use the brand-run axes and card below instead of the colour ones, and drop "Base hue
family", "Saturation / energy" and "Palette" from the card. The brand kit is a constraint, not
taste — it's allowed in Stage 1.

**Phone screens are always mobile native.** Paste the *Mobile native* section into Phase 2 for
every phone brief, native or mobile web. Fill its **Platform** and **Ships as** line from the
Platform setting, and keep only the platform block that applies (plus *Mobile web app* when it
ships as one). Use the platform's frame size in **Technical**.

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

### Build only from these
<the complete set of features, fields, data and states the product has — everything on screen
comes from this list and the product facts>

The layout of each screen is already decided (you'll get the screen plans in Phase 2). Your
seed decides how it looks and feels.

**Accent:** one accent colour, chosen from your seed, on 1–3 elements per screen. Your seed also
picks the **neutral** ground (white, warm white, cool white, light grey) and the **pop
placement**: *action-led* (accent on the primary action), *selection-led* (accent on the
selected tab and active item), or *category-led* (small labels carry the colour).
**Density** is how much fits on a screen: *airy* (big type, few items, lots of space),
*balanced*, *dense* (compact rows, small type, many items). **Component shape** is the shape
language of buttons, fields, chips and rows: e.g. *sharp and outlined*, *rounded and filled*,
*pill*, *borderless with dividers*. These are examples, not a menu — read them from your seed.

### Reply with a direction card, and nothing else
Write it to `<mocks>/1-explore/<v>/direction.md` and return it:

```
Neutral: <white | warm white | cool white | light grey> — <hex>
Accent: <hue family> — <hex>, plus text <hex> and secondary text <hex>
Pop placement: <action-led | selection-led | category-led> — <the 1–3 elements that carry the accent>
Display type: <font> — class: <serif | grotesk | geometric | display/novelty | mono | rounded>
Body type: <font>
Density: <airy | balanced | dense>
Component shape: <one line — corners, outline vs. fill, how rows and chips look>
Surfaces: <one line — how layers separate: whitespace, hairlines, white cards on a light grey ground>
Mood: <3 words>
Working name: <product name you'll use>
From the seed: <one line: which features of the string led here>
```

Then stop and wait.

### Brand kit runs — Phase 1 additions
Add this block after **Build only from these**:

> ### Brand kit (fixed)
> <role table from BRAND.md (translated app roles, contrast-checked); the colour budget; fixed
> fonts if the user fixed them; motifs available>
>
> Use these roles as written: white ground, ink text, the accent on the primary action and
> selected state, category colours as small labels, 1–3 colour pops per screen. Your seed
> decides everything else below.

Replace the accent paragraph with:

> **Pop placement** is where the few colour pops go: *action-led* (accent on the primary
> action), *selection-led* (accent on the selected tab and active item), or *category-led*
> (small category labels carry the colour). **Type pairing**: the brand display face, the brand
> body face only, or a contrasting companion. **Photo scale**: thumbnail rows, large photo
> cards, or editorial full-bleed. **Motif strength**: none, subtle, strong. **Density** and
> **component shape** as above. Read them from your seed.

And use this card:

```
Pop placement: <action-led | selection-led | category-led> — <the 1–3 elements that carry colour>
Type pairing: <display font> + <body font> — class: <serif | grotesk | geometric | display/novelty | mono | rounded>
Photo scale: <thumbnail rows | large cards | editorial full-bleed>
Density: <airy | balanced | dense>
Component shape: <one line — corners, outline vs. fill, tabs vs. segmented vs. chips, how rows look>
Motif strength: <none | subtle | strong> — <which motif>
Mood: <3 words>
Working name: <product name you'll use>
From the seed: <one line: which features of the string led here>
```

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
<string>. Not that: <the other card's neutral, accent, pop placement, type class, density, component shape, name>
(brand runs: pop placement, type pairing, photo scale, density, component shape, name). Send a new card, then wait.">

### Other variants (avoid drifting toward them)
<each other variant's card: neutral, accent, pop placement, type class, density, component shape, name — one line each>

### Screen plans (verbatim)
<screen plans from Stage 0: job, hero, shows first, below the fold, states, cut>

Build each screen to its plan. Below-the-fold content appears only as a section peeking at the
bottom edge. Don't add elements the plan cut.

### Mobile native (phone screens — always include)
**Platform:** <iOS | Android> · **Ships as:** <native app | mobile web app>

These are phone app screens. Native app or mobile web, they must read as a native app on the
platform above, not a web page squeezed to phone width. Your direction styles the native
structure; it doesn't replace it.

**Both platforms**
- **Content first:** content fills the screen edge to edge; images can bleed to the edges. No
  boxed page sections or framed "cards inside a page" unless the component really is a card.
- **Thumb reach:** primary actions sit in the bottom third (bottom bar, floating button,
  toolbar) or in the top app bar as an icon or text button.
- **App structure:** platform bars and controls carry navigation; actions are buttons and rows;
  the screen is the app from edge to edge.
- **Check:** "Would this look at home next to the best apps on my home screen?" If it looks like
  a website, fix the structure before the styling.

**iOS** (Human Interface Guidelines)
- **Frame:** 390×844. Status bar in the top safe area (~54px), home indicator in the bottom safe
  area (~34px). Nothing interactive inside either.
- **Navigation:** navigation bar with a large title on top-level screens that becomes a small
  centred title on pushed screens; back chevron plus the parent's name. Top-level sections → a
  bottom tab bar with icons and labels.
- **Controls:** segmented control for switching views, search field in or under the nav bar,
  inset-grouped or plain list rows with full-width tap areas and a chevron where they push,
  sheets with a grabber, action sheets, context menus, swipe actions on rows.
- **Sizing:** tap targets ≥44pt. Body ~17pt, secondary ~15pt, large title ~34pt. Side margins
  16–20pt.

**Android** (Material 3)
- **Frame:** 412×915. Status bar (~24dp) and a gesture navigation bar (~24dp).
- **Navigation:** top app bar (small, medium or large, collapsing on scroll); back arrow on the
  left with no parent label. Top-level sections → a bottom navigation bar with icons and labels.
- **Controls:** tabs or segmented buttons for switching views, a search bar, list items, a FAB
  (or extended FAB) for the primary action, bottom sheets, menus, chips.
- **Sizing:** tap targets ≥48dp. Body ~16sp, title ~22sp, large headline ~28–32sp. Side margins 16dp.

**Mobile web app** (add to the platform rules above)
- Mock it as the installed home-screen app in standalone mode, with no browser address bar or
  toolbars. The native structure above still applies.
- Use only what a web app can do: no widgets, Live Activities, Dynamic Island, haptics or
  system-only controls (e.g. the native photo picker UI beyond "choose photos"). Bars are fixed
  or sticky, padded with `env(safe-area-inset-*)`.
- Native app: platform-only patterns are allowed when the spec includes them.

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
- One frame per screen at the platform's size (iOS 390×844, Android 412×915; desktop: the
  spec's width). No `vh` units.
- Check your work with:
  `"<chrome>" --headless=new --disable-gpu --hide-scrollbars --window-size=<w>,<h> --virtual-time-budget=6000 --screenshot=<mocks>/1-explore/<v>/full.png file://<mocks>/1-explore/<v>/index.html`
  Read the PNG, fix anything broken, repeat. Re-screenshot after your last edit.

### Report back (short)
1. Anything you changed from your card, and why.
2. Anything in a screen plan you couldn't fit, and what you did instead.
