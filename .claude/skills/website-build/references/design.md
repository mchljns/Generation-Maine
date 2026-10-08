# Design: guardrails, design slop, cohesion

## Guardrails

Write the project's guardrails into the record on day one and check every round against them. Typical
ones, and the reason each exists:

- **No cliches of the place or sector.** For a Maine project: no lobsters, no lighthouses, no moose, no
  flags, no Americana. For a tech project: no abstract blobs, no isometric illustrations, no glowing
  nodes. Cliches tell the reader the page was assembled, not made. When the client grants one exception
  (one specific photograph, one specific landmark), record the exception and its reason.
- **No gradient-heavy styling.** Flat fields, real photographs, type doing the work.
- **One accent with a job.** If the brand has a gold, it goes on the mark, one device and the buttons.
  Not on every heading, not as a background.
- **Real texture over stock.** The street, the paperwork, the person at the counter. A photo of the
  actual place beats a better photo of somewhere else.
- **Type carries the voice.** A display face for headlines, a workhorse for body, a label face for the
  utility layer (kickers, nav, buttons, footer). Keep the label layer consistent through the whole page,
  including every piece of footer utility text; a label face that stops at the footer reads as a mistake.

## Design slop

The visual equivalents of hype words. Each of these was called out by a client on a real project as
"vibe coded" or "placeholder-looking".

- Three-column feature grids with an icon above each heading.
- Boxes, pills or circles around social icons. Icons need size and spacing, not containers.
- Decorative dividers, wavy section edges, floating shapes.
- Gradient buttons, gradient text, glassmorphism.
- Stock-photo heroes, especially the smiling-group kind.
- Captions and credits on placeholder media the client has said will be replaced.
- Fake content inside placeholders: a quote band on a sample clip reads as a real quote.
- Copy sections that exist to fill the fold.
- A "social section" that is a row of cards with logos and no handles.
- Numbered steps in a mission block.
- Text shadow as the treatment for text over video.
- An animation that is fast because the default was fast. A hero loop pans in seconds and reads as a
  screensaver; slow it until it drifts.
- A mark that changes proportion between the nav and the footer without a reason.
- Two lockups built on different rules. Horizontal and stacked versions share one frame rule, one stroke
  weight, one padding rule, so they read as one mark.

## Cohesion with a parent brand

When the client says "make it feel like ours", they mean three things in this order: color, type,
device. Do those and stop.

1. Take the exact values from the parent's site. Record them with the URL.
2. Put the parent's accent where it has a job. Replace your accent, do not add theirs beside it.
3. Use one device from the parent (three bars, a slant, a rule) before kickers and section labels. Not
   on every element. If the device cannot be made to work cleanly, leave it out and keep the colors and
   the attribution in the footer; say that you tried.
4. Attribution in the footer ("A [parent] project") with a link.
5. When the client says "don't overthink it", that is scope guidance: do the three things, show them,
   stop.

## Layout rules that held up

- The hero says what the project is in one line a person could say. Its mark, its one line, its one
  action. A pulsing period or a small live detail is enough motion.
- The about or mission block pairs one statement in large type with a real photograph. Statement first
  on phones, photo beside it on desktop. No numbered points.
- Profiles: the name is the identifier, the town is the kicker. The media is the full social frame
  (9:16 for short video) wherever there is room, and a tap-to-expand viewer where there is not.
- The follow block lists every platform named, with handles when confirmed, and says what lives where.
- The footer carries the mark (animated draw once, at arrival), the parent and partner attribution, the
  social links, the legal line and contact. On a preview, a build stamp.
- Section tints change with the content on phones only when the change has meaning (one tint per
  profile). The heading block and the content block change together; a seam between them reads as a bug.

## Phones

Design the phone layout as its own layout, not as the desktop squeezed. A pinned desktop stepper becomes
a horizontal snap carousel on phones. The position row (counter, next name, segments) sits above the
cards where the thumb can reach it. The clip stays a social frame; when the frame and the story cannot
share the screen, a 4:5 crop with a tap-to-expand viewer keeps both.

Tap targets 44 px tall and at least 44 px wide where there is room; a row of nine segments can be 44 tall
and narrower, spaced. Text over the hero video gets a scrim or a band. Padding above the mark and below
the last call to action is checked at 320 and 390 wide, not assumed.

## Motion

- Slow. Hero loops drift (seconds per plate, long dissolves). Footer draws take a full second or more.
- Once. A draw animation runs when the reader arrives, not on load, not on every scroll.
- Clean ends. A path that finishes at a corner is drawn through the corner so the two strokes meet
  without a notch; check the last frame at 2x.
- Respect `prefers-reduced-motion`: no autoplay loops, no draws, controls on video.
- Transitions must not run at load. Add the class that enables transitions before first paint, in the
  head, so the page does not animate into place.
