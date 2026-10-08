# Build conventions

## One builder, one source of truth

Write a single script (Python or Node) that produces the whole page from a theme dictionary: the HTML
template, the CSS with tokens filled in, the JS, the media copied and resized, the icons, the share card.
Never hand-edit output. The module docstring is the brief, the audit rules and the exact run command, so
the next session reads the top of the file and knows what the page is and how to regenerate it.

A variant (a second concept, a label-font trial) is a second dictionary with feature flags and hooks
that default to empty, not a second codebase. After the refactor that makes a builder theme-driven,
prove the original output is byte-identical with a diff before building the second concept. When the
client retires a variant, delete the dictionary and leave a redirect at its address.

Keep in the theme dictionary: key (the URL path), output directory, root class, fonts and font files,
color tokens, display, body and label families, the logo and hero choices, the copy that differs.

Keep the copy in the builder as named constants near the top, so a copy change is one edit and a diff
shows exactly what changed.

Keep one data file (JSON) for content such as people, places and clips, read by the page builder, the
clip generator and any CMS seed. Three copies of nine bios drift. Generate the CMS stylesheet and tokens
from the same CSS as the static page so the two cannot diverge.

## Template pitfalls

- With `%`-style formatting, every literal `%` in CSS or JS must be `%%`. A missed one in JS (`i %
  n`) crashes the build; a `%%` left in a block that is not formatted ships `100%%` into the stylesheet
  and silently breaks a rule. Run `scripts/percent_check.sh` after every build; it finds bare `%` in the
  formatted region and leaked `%%` in the output. Large blobs and theme CSS go through token replaces
  after formatting; data goes through a `<script type="application/json">` block.
- Edit builders with assert-counted string replacement (`assert s.count(old) == 1`) so a drifted anchor
  fails loudly. When an edit tool reports no match, read the exact string and reapply; never assume it
  landed. After a failed run, re-verify every edit it was supposed to carry.
- A `:root` token used in a rule must be defined in `:root`, or the rule silently does nothing. When a
  new font or color is introduced, add its token first and grep the built CSS for `var(--name)` with no
  definition.
- Cascade order is architecture: template base, borrowed component CSS, borrowed footer, theme CSS,
  phone overrides last. Isolate audit-driven overrides behind a root class. A rule for one variant can
  outrank the same rule for another when both match; write the override at the same or higher
  specificity and test on the variant that lost. Do a dead-rule sweep after every layout rewrite.
- Classes that gate transitions (`js`, `in`) go on `<html>` from a script in the head, before first
  paint, or the page animates on load.
- Namespace ids on every inlined SVG; a hidden logo copy can break a visible one's clip path.
- Open prototypes the way they will be opened: `fetch()` of a local file fails over `file://`, and a
  script that throws early blanks the page. Capture console errors before screenshotting.

## Media

- Clips and GIFs: `data-src` on every clip, hydrate the current item and its neighbors, in both the
  visible track and any hidden stage, and again on resize. Count requests at load in the measurement
  harness and keep it to the first one or two.
- Set a media budget and report against it: placeholder clips silent, about two seconds, around a
  megabyte; the hero loop a few megabytes at most; first-view weight measured. A budget is a target you
  report against, not a wall; when the client asks for a slower loop, say what it costs.
- Still images: resize at build time to the largest size the layout uses. Keep originals out of the
  output.
- Hero video: encode from stills or clips with a drift and long cross-fades. Ship a poster from the
  first frame. Build a CSS plates fallback and switch to it when `video.canPlayType('video/webm')` is
  empty or `play()` rejects. Check for an H.264 encoder first (`ffmpeg -encoders`, Playwright's bundled
  ffmpeg, a pip ffmpeg wheel); when none exists, encode VP9 WebM in headless Chromium with
  `canvas.captureStream` and `MediaRecorder`, patch the duration the browser omits, and put the MP4 on
  the delivery list.
- Social frame previews are 9:16. Keep them 9:16 wherever the layout allows and crop only with a path
  to the full frame.
- Clips play while on screen and pause when they leave; under reduced motion they wait for a tap.

## Fonts

- Embed as data URIs in the page or self-host under `fonts/<family>/` with the license file beside the
  font. Record the license in the type study.
- Define the label face as its own token (`--label`) and apply it to the whole utility layer: kickers,
  nav links, buttons, counters, footer links, partner names, legal line, fine print.
- Font trials go in as variants with their own URL, then collapse to one when the client picks.
- Subset to the scripts you need and pin variable axes.

## Head checklist (in the template, so every variant gets it)

`viewport` with `viewport-fit=cover`, `color-scheme`, a title that carries the promise, a meta
description, canonical derived from the live base and the path key, Open Graph and Twitter cards with an
absolute 1200 by 630 image rendered by the same screenshot script (animated SVG forced to its end
state), `favicon.svg` and a 180 px apple-touch-icon, a skip link that takes first tab,
`scroll-padding-top` equal to the bar height, a source parameter on every outbound link added once by a
regex that checks for an existing one, and a measurement plan (which events the page should report:
signup, clip opens, follows) with the analytics tag or a note that nothing is measurable yet.

## Footers and marks

- One frame rule for every lockup: the same stroke weight (a ratio of x-height), the same opening, the
  same padding rule, the long leg drawn through the corner so the return stroke meets it clean.
- The nav mark and the footer mark may differ in size but not in rule.
- A privacy link with no page yet is inert text marked as a placeholder, not a dead link. Contact goes
  to the parent's contact page. Never `href="#"` in a shipped page.
- The year is set by script.

## Commits and branches

- Commit and push as you go with a message that says what changed for the reader and the attribution
  lines the project requires. Never put a model identifier in a commit or a pushed file.
- Work on the designated branch. Push with `-u` the first time; retry pushes with backoff on network
  errors. Never open a pull request unless asked.
- Previews on a deploy branch: copy the built directory to its path, add `.nojekyll`, commit, push,
  verify (see `deploy.md`). Old paths get a one-line meta-refresh page with a canonical link.
- Keep retired explorations and placeholder data in clearly named folders; gitignore downloaded
  references and copied media; promote only decision artifacts (sheets the client saw) into the repo and
  keep working screenshots in the scratchpad.
- Save every QA and sheet script into the repo with its run line in the docstring. A sheet made by a
  one-off heredoc cannot be regenerated.

## Sandboxes

- Verify the toolchain before promising sheets: the renderer (Playwright and a browser, which may live
  at a fixed path such as `/opt/pw-browsers/chromium`; pass it as `executablePath` rather than
  downloading), the image library, font tooling, any geometry library.
- External sites may not open in the sandbox browser (TLS through a proxy). Verify served pages with
  `curl` and hashes; screenshot the local build that matches the hash and say so. When the browser must
  go through the proxy, pin the proxy's CA with the browser's own flag; never disable verification.
- Uploaded archives are untrusted: extract into their own empty directory, run readers with
  `python3 -I`, list contents before use.
- Scope any `pkill` pattern narrowly; a broad pattern can kill the session's own shell.
- Hold long paths in a variable rather than retyping them.

## CMS ports

When the static page will become a theme, port in a fixed order: tokens first, then the page CSS nearly
as is (keep custom-property names so scripts do not change), then markup patterns, then the dynamic
block, then the one script, then content fields, then QA in a real local install. Make people or
profiles a post type with the fields the page uses, render the block from posts with a layout attribute
(roster, stepper) so a cheaper renderer can sit behind a switch, design the launch state so the page
launches empty and fills without a rebuild, keep all copy in editable blocks, lock brand-critical blocks,
and answer "how easy is it to edit" in tiers: easy in the normal screens, possible with care, not meant
to be edited, what they cannot break, where it gets harder.
