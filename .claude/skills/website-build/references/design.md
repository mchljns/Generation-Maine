# Design: guardrails, design slop, marks, motion, phones

## Rules with numbers

Turn every visual rule into a number and put the numbers in `:root` and in the builder's docstring:
margin as a fraction of frame width, headline line height and tracking, maximum lines and words, one
control height (48 px is a good default), a small-text floor (12 to 13 px, matched to the parent brand
when there is one), 44 px tap targets, whole-pixel gutters from a scale. Rules without numbers drift;
numbers make a system repeatable in code and in the client's tools and checkable by script.

## Guardrails

Write the project's guardrails into the record on day one and check every round against them:

- **No cliches of the place or sector** unless the record grants a named exception. Write the ban list
  for the region and sector into the brief: tourist symbols, the local silhouette, flag colors,
  founding-era revivals, category symbols (a pin for a map app, a leaf for a green company). When the
  client wants a landmark anyway, give it the large-scale job (a mural, a hero) and keep the small mark
  abstract. Record the exception as client-directed, citing the rule it overrides.
- **No gradients** except a measured scrim that keeps type legible over a photograph. A slow background
  color drift either goes unnoticed or reads as a gradient.
- **One accent with one job.** The accent is the brand's punctuation (the dot, the period, one device)
  and appears once per frame. Whether it may also be a button follows the parent brand when there is
  one; otherwise size and weight give a call to action its pull. Never small accent text on a light
  field, never the accent inside a gradient. Keep the palette closed: a new mark must not need a new
  color, and any new color is tested on the same four surfaces (hero, dark field, paper field, lockup)
  with contrast measured before it is admitted.
- **Real texture over stock.** The street, the paperwork, the person at the counter. A photo of the
  actual place beats a better photo of somewhere else. When the site launches with little photography,
  plan a computed graphic language from the identity (one construction rule at several scales) to carry
  the pages instead of stock.
- **Type carries the voice.** A display face, a workhorse body, a label face for the utility layer.
  The label face runs through every kicker, nav link, button, counter and footer line; a label face that
  stops at the footer reads as a mistake.
- **Never type at partial opacity on a colored field.** Solid tokens, underline for hover. Test
  near-whites on the real dark fields and read rendered pixels; when a tint keeps reading wrong to the
  client, go to pure white and make the field darker.
- **One palette in every OS theme.** When the page paints its own section colors, strip
  `prefers-color-scheme` overrides; a dark-mode override made text unreadable in a client's viewer.
  Derive neutrals from the brand's own hues rather than a template off-white.
- **Decide binary layout questions once** (centered or left, bar or capsule) and never mix them. One
  button shape site-wide, one texture language per frame, one lined thing and one dot.
- **The hero fits a laptop and a phone.** Cap the mark and headline by viewport height as well as width
  so the call to action clears the fold on a short laptop (1280 by 650) and a tablet. On phones the
  picture fills the first screen with text in the lower third over a rising scrim.
- **Check what a rendering implies.** Gold lighting only the coast favors a region; prefer rules of
  geometry over rules of geography. Name the look-alikes (badge, puzzle piece, record button, eye,
  hamburger, honeycomb) before the client does.
- **Hand-draw platform icons** at one unit size in one color inside the builder so they take the ink of
  the field, and never pull brand-colored third-party logos or icon packs into the palette.

## Design slop

The visual equivalents of hype words. Each of these was called out on a real project as "AI default",
"vibe coded" or "placeholder-looking".

- AI-default type (Inter or DM Sans body) and warm cream template off-white.
- Floating pill navigation, icon-only bars, glow bars, mega-menus, this season's SaaS capsule.
- Three-column feature grids with an icon above each heading. Card grids of stacked boxes where a ruled
  list would do. Premium is space and hairlines, not boxes and gradients: hairline rules, one display
  label, one line, the handle at the right edge.
- Boxes, pills or circles around social icons. Icons need size and spacing, not containers.
- Decorative dividers, wavy section edges, floating shapes, gradient buttons, glassmorphism.
- Stock-photo heroes, especially the smiling-group kind. Mood stock in gray and fog.
- Parallax video heroes and anything tied to the pointer. Counters, tickers, bounces.
- A display device used everywhere until it becomes texture: monospace beyond numbers, eyebrows on every
  block, the logo repeated in an about panel. The logo appears once per screen.
- Captions and credits on placeholder media the client has said will be replaced. Fake content inside
  placeholders: a quote band on a sample clip reads as a real quote.
- Copy sections that exist to fill the fold. A "social section" of logo cards with no handles.
- Visible truncation, dead links, a hand-typed year, a decorative sign-up field that discards what is
  typed, hidden sections with placeholder copy. These are defects to design around, not polish.
- Text shadow as the treatment for text over video.
- An animation that is fast because the default was fast.
- A mark that changes proportion between the nav and the footer without a reason. Two lockups built on
  different rules.
- Skewing to an audience with the obvious moves (heavy type, black, neon, camo). Change temperature,
  grid and labeling instead.

When the client chooses a default anyway, build it without argument, state the distinctness trade-off
once for the record, and keep the swap ready. When a client's idea is doubted, build it fully and render
it at the sizes where it fails, so the sheet makes the case instead of you.

## Marks and lockups

- Design at 16 px first, then judge at every size the mark ships at (16, 32, 40, 48, 110) rendered at
  1x and enlarged pixel for pixel, never from a large vector. Never claim "fixed" until verified at the
  sizes the asset is actually used at.
- The on-the-nose test: write the one sentence that describes the mark. If it restates the name, the
  brief or the category, it fails. A mark that needs a paragraph fails. If the client says they do not
  understand it, replace it rather than explain harder.
- A logo does four jobs at once: carries one idea that belongs to the brand and not the category,
  survives every size and surface, is drawn rather than typed or assembled, and is the smallest part of
  a system that repeats. Grade every candidate against the four.
- One builder, one set of written construction rules (stroke as a fraction of x-height, pads in strokes,
  the long leg drawn through the corner so the return meets it clean), all type outlined, every variant
  regenerated at once. Lockups drawn separately never match.
- A size system with named cuts, thresholds, minimum sizes and clear space. When a number carries a
  story (sixteen lines for sixteen counties), every cut keeps the number and the builder counts it.
- A wordmark-only system is legitimate but still needs a small-size answer; wordmarks die below about
  60 px, so an avatar and favicon device is required, and it should not be initials.
- Use precise, sourced public-domain geometry for any map-shaped mark, pick the right variant
  (shoreline, not legal boundary), choose a simplification per output size, and record the source. Fix
  artifacts with exact geometry, never by trimming the source outline.
- When drawing a representational mark, research real photographs of the object and redraw from what it
  looks like, not from memory; that is where clipart and emoji come from.
- Grade directions against the written criteria in a table (criterion, grade, one line why) and name
  the single weakest criterion. Grade applied surfaces, not only the mark; for a social-first brand the
  templates, story frames and avatars are the primary surfaces.
- Propose a first-reaction test with a few real people and one question as the decider for ownability,
  instead of another round of drawing.

## Cohesion with a parent brand

When the client says "make it feel like ours", they mean three things in this order: color, type,
device. Do those and stop.

1. Take the exact values from the parent's site. Record them with the URL.
2. Put the parent's accent where the parent puts it. Replace your accent, do not add theirs beside it.
3. Use one device from the parent (three bars, a slant, a rule) before kickers and section labels. Not on
   every element. If the device cannot be made to work cleanly, leave it out, keep the colors and the
   attribution in the footer, and say that you tried.
4. Attribution in the footer with a link.
5. When comparing two concepts under a shared client requirement, make everything the client named
   identical on both and keep exactly one axis of difference per concept. Name that axis plainly, even
   when it predicts the winner.

## Layout rules that held up

- The hero says what the project is in one line a person could say: its mark, its line, its one action.
  A pulsing period or one small live detail is enough motion. Transparent chrome over a hero needs a
  solid state within a few pixels of scroll.
- The about or mission block pairs one statement in large type with a real photograph: statement first
  on phones, photo beside it on desktop, a single reading column, no numbered points.
- Profiles: the name is the identifier, the town is the kicker. The media is the full social frame
  (9:16 for short video) wherever there is room, and a tap-to-expand viewer where there is not.
- Pinned or stepper blocks pin at their own height with a small top margin, never centered in a full
  screen height, which opens an empty half screen before pinning.
- The follow block lists every platform named, with handles when confirmed, and says what lives where.
- The footer, audited against the parents' footers: every path out repeated (page links, social row),
  the parent credit linked, a partner or family row, privacy and contact links when the page collects
  email, a complete legal line or a placeholder for it, credits collapsed to one line, the year set by
  script, the mark at its strongest cut, one-column stacking on phones, and on previews a build stamp.
- Section tints change with the content on phones only when the change has meaning. The heading block
  and the content block change together; a seam between them reads as a bug.

## Motion

- One moving idea per view. Everything on scroll or on arrival, nothing tied to the pointer. No parallax
  on the hero mark, no counters, no hover for its own sake, nothing bounces. Ease out, 700 to 1100 ms
  for reveals.
- Slow. Hero loops drift (seconds per plate, long dissolves). A draw-in reads as intentional above about
  two seconds on desktop and as a loading delay above about 1.5 seconds on a phone; set both per
  project and keep hero and footer draws at the same pace.
- Once. A draw runs when the reader arrives, not on load, not on every scroll. Fire on the element being
  fully in view with a tolerance, never on reaching the exact page end.
- Clean ends. Record the draw at 2x and compare the last frame to the settled state pixel for pixel;
  check the direction of travel so strokes meet without a jump; check stills at several points of a
  pulse cycle.
- Scroll-coupled state (page color, fades) is one calculation per frame with exactly one writer. Never a
  timer, never a scroll rule plus an observer on the same property. Switch text color in one step where
  both colors clear 3:1.
- Crossfade one way (the next clip fades in over the last, which stays whole); hide inactive clips with
  `visibility: hidden` so a phone does not decode all of them.
- Transitions must not run at load: add the class that enables them from a script in the head, before
  first paint.
- Respect `prefers-reduced-motion` at every site: no autoplay loops, no draws, controls on video,
  programmatic scrolls use `behavior: auto`. Publish "with reduced motion on, nothing moves".
- When the client names a motion reference they know (a phone's location pulse), match it and check
  stills at several points of the cycle.
- Keep a "considered and left out" list in the record.

## Phones

Design the phone layout as its own layout, restacked, not reduced. A pinned desktop stepper becomes a
horizontal snap carousel on phones; a desktop grid becomes explicit tile counts per breakpoint derived
from the minimum readable tile width. The position row (counter, next name, segments) sits above the
cards where the thumb can reach it. The clip stays a social frame; when the frame and the story cannot
share the screen, do the pixel arithmetic (available height, media at ratio, remainder), offer the
options with their costs, and recommend one (a 4:5 crop with a tap-to-expand viewer, a row card with the
frame beside the text, an overlay) rather than cropping away the thing the component exists to show.

Tap targets 44 px tall and at least 44 px wide where there is room, achieved with `min-height`, padding
and negative margins so the visual stays the same; a row of nine segments can be 44 tall and narrower,
spaced. Do not add boxes to reach the number. Text over the hero video gets a scrim weighted to the text
column. Nav links about 40 px, dialog close 48 px. Padding above the mark and below the last call to
action is measured at 320 and 390 wide, not assumed. Pinned media is sized from the viewport minus
persistent bars and the safe area, with a floor that keeps it legible and a ceiling that leaves the name
and the first lines on screen, refit after fonts load.
