# QA: measure, audit, fix, record

## The posture

A page is done when the measurements say so, not when the screenshot looks fine. Every audit pass gets
its own record entry with what was measured, what was found, what was fixed and what was accepted. When
the user says "do all fixes", do all of them and show the result in one sheet.

## The measurement harness

`scripts/measure.mjs <url-or-file> --viewports 320x568,375x667,390x844,430x932,768x1024,844x390,1400x900`

For each viewport it reports:

- `docOverflowPx`: horizontal page overflow. Any value above 0 is a bug (a negative-margin track inside
  a flex or grid parent is the usual cause; give the track `min-width:0`).
- `tapTargetsUnder44`: every visible link, button and control under 44 px in either dimension.
- `textOverflow`: text wider than its box (handles, names, long words in narrow columns).
- `imagesWithoutAlt`, `textUnder12px`, `fonts` in use (catches a font that never applied), `h1Count`,
  `landmarks`, `title`, `metaDescription`, `viewportMeta`.
- `mediaRequestedAtLoad`: what loaded before any interaction. Nine clips at open is a bug.
- `errors`: page errors and console errors.
- A screenshot per viewport.

For interactive parts, write a short Playwright script that drives the real gesture and asserts the
state, the way a user would hit it:

- Nudge a snap track by 200 px and check which item is current, where its left edge sits, and what the
  counter says.
- Tap a segment and check the item lands on the gutter.
- Press ArrowRight with the track focused.
- Open a viewer: check the frame ratio, the close button size, where focus went, that body scroll is
  locked, that only the current slide and its neighbors loaded. Close with the button, Escape, the
  backdrop and the browser back button; check focus returned and the page did not scroll.
- Resize across the phone breakpoint and check nothing is left blank.
- Scroll to the end and check the footer draw fired once, at arrival, and finished clean (zoom the
  corner at 2x).

Compute the current item from geometry (the item whose edge is nearest the gutter or whose center is
nearest the track center), never from `scrollLeft / itemWidth`; the arithmetic lags by one as soon as
the viewport is wider than one item.

## The audits, in order

Run them as separate passes. Each finds things the others do not.

### Footer
Links all work (no dead privacy link; contact goes to a real page with one UTM). Mark draws once at
arrival. Mark proportion matches the nav decision. Utility text in the label face. Partner names and
legal line present or placeholdered. Tap targets. Safe-area padding on phones. Build stamp on previews.

### Spacing and sizing
Vertical rhythm between sections at 320, 390 and 1400. Padding above the mark and below the last call to
action on phones. Frame padding around a framed mark (not too tight, not too tall). Headline distance
from the element below it. Hero text size at 320.

### Usability and conversion
One primary action per screen. Newsletter form: one field, one button, visible fine print, keyboard
submit. Social links reachable without scrolling past the fold on phones. Nothing that looks clickable
and is not. Nothing clickable that looks like text. Copy that says what happens after the click.

### Tap targets
Every control 44 px tall on phones. Social icons sized and spaced without boxes. Segments and dots
with a full-height hit area. Nav hamburger 48 px.

### Phone pass
Hero video plays or falls back to plates. Hero text legible over the loop (scrim or band). Position row
above the cards. Carousel snaps to the gutter. Clip and story share the screen. Section tint changes
with the heading block, no seam. Footer draw fires on phones (an IntersectionObserver with a tolerance,
not an exact end-of-page check). Padding above the mark and below the form.

### Accessibility
Landmarks (`header`, `nav`, `main`, `footer`). One `h1`. Alt text on content images, empty alt on
decorative ones. Focus visible on every control. Carousels focusable with arrow keys. `aria-current` on
the current step. Dialogs with `role=dialog`, `aria-modal`, focus moved in and returned on close, Escape
closes. `prefers-reduced-motion` honored (no loops, no draws, controls on video). Color contrast on
kickers and fine print (an 11 px label in 45 percent white on navy fails; raise it).

### Critical audit
Read the page as the client's harshest colleague. List everything that reads as unfinished, vibe-coded
or generic: fake content in placeholders, sections without a job, copy that could be any brand, a
headline too close to the media, a selector that got lost, a font that never applied. Then fix all of it.

## After fixing

Re-run the harness at every viewport. Make a sheet of the states that changed. Write the record entry.
Only then deploy.
