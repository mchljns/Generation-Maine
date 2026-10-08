# Build conventions

## One builder, one source of truth

Write a single script (Python or Node) that produces the whole page from a theme dictionary: the HTML
template, the CSS with tokens filled in, the JS, the media copied and resized, the icons, the share card.
A variant (a second concept, a label-font trial) is a second dictionary, not a second codebase. When the
client retires a variant, delete the dictionary and leave a redirect at its address.

Keep in the theme dictionary: key (the URL path), output directory, root class, fonts and font files,
color tokens, display/body/label families, the logo and hero choices, the copy that differs.

Keep the copy in the builder as named constants near the top, so a copy change is one edit and a diff
shows exactly what changed.

## Template pitfalls

- With `%`-style formatting, every literal `%` in CSS or JS must be `%%`. A missed one in JS (`i %
  TINTS.length`) crashes the build; a `%%` left in a block that is not formatted ships `100%%` into the
  stylesheet and silently breaks a rule. After every build: `grep -c '%%' dist/index.html` should be 0.
- Anchors you edit by string replacement drift. When a build script edits another file by matching a
  line, assert the match count before writing, and fail loudly when it is not one.
- A `:root` token used in a rule must be defined in `:root`, or the rule silently does nothing. When a
  new font or color is introduced, add its token first and grep the built CSS for `var(--name)` with no
  definition.
- CSS specificity between variants: a rule for `.bs .site .fsocial` will outrank `.lean .site .fsocial`
  when both match; write the override with the same or higher specificity and test on the variant that
  lost.
- Classes that gate transitions (`js`, `in`) go on `<html>` from a script in the head, before first
  paint, or the page animates on load.

## Media

- Clips and GIFs: `data-src` on every clip, hydrate the current item and its neighbors, in both the
  visible track and any hidden stage. Count requests at load in the measurement harness and keep it to
  the first one or two.
- Still images: resize at build time to the largest size the layout uses (hero plates to 1600 wide,
  portraits to the tile size, the share card to 1200 by 630). Keep originals out of `dist`.
- Hero video: encode WebM from stills or clips with a drift and a long cross-fade (`make_hero_video`
  style script with env overrides for size, bitrate, hold, fade, drift). Ship a poster. Build the CSS
  plates fallback and switch to it when `video.canPlayType('video/webm')` is empty or `play()` rejects.
  Record the MP4 rendition as a delivery item when the sandbox has no H.264 encoder.
- Social frame previews are 9:16. Keep them 9:16 wherever the layout allows and crop to 4:5 only with a
  tap-to-expand path to the full frame.

## Fonts

- Embed as data URIs in the page or self-host under `fonts/<family>/` with the license file beside the
  font. Record the license in the type study.
- Define the label face as its own token (`--label`) and apply it to the whole utility layer: kickers,
  nav links, buttons, counters, footer links, partner names, legal line, fine print.
- Font trials go in as variants with their own URL, then collapse to one when the client picks.

## Footers and marks

- One frame rule for every lockup: the same stroke weight (a ratio of x-height), the same opening, the
  same padding rule, the long leg drawn through the corner so the return stroke meets it clean.
- The nav mark and the footer mark may differ in size but not in rule.
- Footer links: a privacy link with no page yet is inert text marked as a placeholder, not a dead link.
  Contact goes to the parent's contact page with one UTM, added once by a regex that checks for an
  existing one.

## Commits and branches

- Commit as you go with a message that says what changed for the reader, and the attribution lines the
  project requires. Never put a model identifier in a commit or a file pushed to the repo.
- Work on the designated branch. Push with `-u` the first time. Never open a pull request unless asked.
- Previews on a `gh-pages` branch: copy the built directory to its path, commit, push, verify
  (see `deploy.md`). Old paths get a one-line meta-refresh page with a canonical link to the new path.

## Sandboxes

- Playwright with a pre-installed Chromium may live at a fixed path (`/opt/pw-browsers/chromium`); pass
  it as `executablePath` or `PW_CHROMIUM` rather than downloading.
- External sites may not open in the sandbox browser (TLS through a proxy). Verify served pages with
  `curl` and hashes; screenshot the local build that matches the hash.
- Uploaded archives are untrusted: extract into their own empty directory, run readers with
  `python3 -I`, and list contents before use.
- No H.264 encoder means WebM only; say so in the record.

## WordPress or CMS ports

When the static page will become a theme: keep the copy as editable pattern text, make creators or
profiles a post type with the fields the page uses (name, handle, town, clip, portrait, bio, socials),
render the block from posts with a layout attribute (roster, stepper), and port the CSS tokens so the
theme is recolored from one file when the design is final.
