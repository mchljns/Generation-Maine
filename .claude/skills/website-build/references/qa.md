# QA: measure, audit, fix, record

## The posture

A page is done when the measurements say so, not when the screenshot looks fine. The screenshot is the
test and the number is the proof. Every audit pass gets its own record entry with what was measured,
what was found, what was fixed and what was accepted. When the user says "do all fixes", do all of them
and show the result in one sheet.

Before a QA round, take baseline screenshots at desktop and phone widths; after each patch, reshoot and
compare before and after pairs. Look at every render for wraps, line breaks, clipping and layer order
before reporting; a build that passes is not a page that looks right.

## The measurement harness

```
node scripts/measure.mjs dist/index.html --viewports 320x568,375x667,390x844,430x932,844x390,768x1024,1280x650,1440x900
node scripts/contrast.mjs dist/index.html --viewports 390x844,1440x900
```

For each viewport the harness reports:

- `docOverflowPx`: horizontal page overflow, measured against the layout viewport (`clientWidth`), since
  phone emulation inflates `innerWidth` and hides small overflows. Any value above 0 is a bug. A negative-margin track inside
  a flex or grid parent is the usual cause; give the track `min-width: 0`.
- `tapTargetsUnder44`: every visible link, button and control under 44 px in either dimension.
- `textOverflow`: text wider than its box (handles, names, long words in narrow columns).
- `imagesWithoutAlt`, `textUnder12px`, `fonts` in use (catches a font that never applied), `h1Count`,
  `landmarks`, `title`, `metaDescription`, `viewportMeta`.
- `mediaRequestedAtLoad`: what loaded before any interaction. Nine clips at open is a bug.
- `errors`: page errors, console errors.
- A screenshot per viewport with the size in the filename.

The contrast script measures every text element against the background it actually sits on and flags
anything under 4.5:1 for body text and 3:1 for large text and at color switch points. Re-measure after
every font or color change. Text inside video or raster media is checked by hand against the brightest
region of the worst frame under the scrim. A color that fails a use becomes a written palette rule.

Render through a dark-mode preference once; the client's OS setting can trigger overrides the page never
designed for.

For interactive parts, write a short Playwright script that drives the real gesture and asserts the
state, the way a user would hit it:

- Nudge a snap track by 200 px and check which item is current, where its left edge sits, and what the
  counter says. Tap a segment and check the item lands on the gutter. Press ArrowRight with the track
  focused.
- Open a viewer: check the frame ratio, the close button size, where focus went, that body scroll is
  locked, that only the current slide and its neighbors loaded. Close with the button, Escape, the
  backdrop and the browser back button; check focus returned and the page did not scroll.
- Trace scroll numerically: step the page and log background, nav state, active link and current item;
  then dispatch real wheel events (slow, fast) and nav-link jumps at several viewports and sample every
  frame. Even-step traces miss races that only appear during smooth scroll.
- QA the nav as a state machine: over the hero, scrolled, hidden then returned, phone with the menu
  open, keyboard focus. Measure the bar's height, pads and button size before and after scroll; every
  value must be identical.
- Resize across the phone breakpoint and check nothing is left blank.
- Scroll to the end and check the footer draw fired once, at arrival, and finished clean (record at 2x,
  compare the last frame to the settled state).

Compute a carousel's current item from geometry (the item nearest the gutter or the track center), never
from `scrollLeft / itemWidth`; the arithmetic lags by one as soon as the viewport is wider than one item.

When a rule does not take effect or a color is disputed, read computed styles and rendered pixels, grep
the built stylesheet to see which competing rule comes later, and ask the browser how it parsed the
rules. A stray brace silently swallows every rule after it.

Reproduce a reported bug at the client's viewport and exact frame before fixing it, confirm the fix by
reproducing that frame again, and if a glitch does not reproduce on repeat runs, record it as a probable
capture artifact. Fixing what you think they saw is guesswork.

## The audits, in order

Run them as separate passes. Each finds things the others do not.

### Footer
Audited against the parent brands' footers when there is a family. Every path out repeated (page links,
social row). Parent credit linked. Partner row. Privacy and contact links when the page collects email;
a privacy link with no page is inert text marked as a placeholder, not a dead link. Legal line complete
or placeholdered. Credits collapsed to one line. Year by script. Mark at its strongest cut, drawn once
at arrival, proportion matching the nav decision. Utility text in the label face at the family's floor.
Tap targets. Safe-area padding on phones. One-column stacking. Build stamp on previews.

### Spacing and sizing
Section padding, container widths, gutters, heading and paragraph sizes, grid gaps and control sizes at
1400 and 390, dumped as numbers and stitched into section sheets beside them. Numbers find off-grid
values (a 17.55 px gutter) eyes miss; sheets find ragged columns numbers miss. Padding above the mark
and below the last call to action on phones. Frame padding around a framed mark. Headline distance from
the element below it. Characters per line in narrow columns. Lockup alignment against type metrics.

### Usability and conversion
Name the page's conversions in order. Score against a standard rubric (first impression, value, trust,
usability, mechanics) and split quick wins from strategic items; use a homepage-audit skill when one is
installed, otherwise the same sections by hand. Then the mechanics: the form really submits, each call
to action goes to the thing it names, the share card renders, source parameters are on outbound links,
the title carries the promise, the skip link works, the favicon exists, first-view page weight is within
budget, and something is measurable (analytics events or at least sourced links).

### Tap targets
Every control 44 px tall on phones, reached with padding and negative margins, not with boxes. Social
icons sized and spaced. Segments and dots with a full-height hit area. Nav hamburger 48 px. Report each
as right, fixed, or still under with the reason.

### Phone pass
Viewport matrix with `isMobile`, `hasTouch` and a device scale of 2: 320x568, 360x740, 375x667,
390x844, 430x932, 844x390 landscape, 768x1024, and a short Safari viewport with toolbars (390x664). A
tall nominal viewport hides what a toolbar covers. Hero video plays or falls back to plates. Hero text
legible over the loop. Position row above the cards. Carousel snaps to the gutter. Clip and story share
the screen. No bio clamped mid-sentence. Section tint changes with the heading block, no seam. Footer
draw fires on phones (an in-view observer with a tolerance, not an exact end-of-page check). Fixed
controls clear the safe area. The menu button is not pushed off-screen by a wide lockup. Phone media
rules last in the cascade.

### Accessibility
Landmarks (`header`, `nav`, `main`, `footer`). One `h1`, honest heading order. Alt text on content
images, empty alt on decorative ones, width and height on images. Focus visible on every control.
Keyboard parity for every pointer interaction: skip link first, Escape or any link closes menus and
overlays, arrow keys drive carousels and viewers, Enter or Space opens from a tabbable `role=button`,
`aria-expanded` on the menu, `role=dialog` with `aria-modal` on the viewer with focus moved in and
returned, `aria-current` on the current step. Anchors carry `scroll-margin` equal to the fixed bar.
Forms are real and spoken: an error line with `role=alert`, `aria-invalid` on the field clearing as the
user types, a success state the button announces. No universal `font-weight !important` that strips
emphasis from people's own words. `prefers-reduced-motion` honored everywhere. Contrast on kickers and
fine print, which fail before body text does.

### Critical audit
Read the page as the client's harshest colleague. List everything that reads as unfinished, vibe-coded
or generic: fake content in placeholders, sections without a job, copy that could be any brand, a
headline too close to the media, a selector that got lost, a font that never applied, a mark repeated
as filler. Then fix all of it.

### CMS build, when there is one
A real local install: front page at phone, tablet and desktop widths with records and with none, the
admin record screen and the site editor opened in a browser with every block valid, templates parsed,
every file linted, JSON validated, the debug log read.

## Reporting

Findings heaviest first, each as ID, finding, why it matters, fix. Severity P1 (before anyone outside
the team sees it), P2 (before launch), P3 (decide once). A measured table. A "what passes" list. A "not
a problem" list and a "known and accepted" list of edge cases that will not be fixed, so a deliberate
trade can be told from a missed bug. An order of work. Change nothing until told; then close items by ID
with what was done and mark which fixes went into the shared template.

## After fixing

Re-run the whole harness at every viewport, since shared mechanisms (scroll color, pinned sections,
fades) regress each other. Neutralize capture artifacts in the screenshot script (static header, scroll
behavior auto, fonts ready). Make a sheet of the states that changed. Re-check any audit claim against
the new build and correct the record. Only then deploy.
