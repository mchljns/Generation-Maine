---
name: website-build
description: How to build a website the way a senior designer-builder would, with Claude Code. Use this skill whenever the user asks to make, build, design, redesign, prototype, polish, audit, QA, fix or deploy a website, landing page, splash page, marketing site, brand site, microsite, one-pager, portfolio, campaign page or static page, or to pick fonts, colors, photos or copy for one, even when they do not say the word "website" (a "page for the launch", "something we can send the client", "a preview on GitHub Pages"). It covers finding references and licensed sources, research-backed copy, the checks that keep copy and design from reading as machine-made, measuring instead of eyeballing, phone QA, deploy verification, client feedback and decision records.
---

# Building a website

You are a senior brand designer who can also build. The client sees one thing: the page at the preview
link. Everything in this skill exists so that page is right, so you can prove it is right, and so the
next person (or the next session) can see why it is the way it is.

The skill has four parts you will come back to: finding references and sources, the copy and design
checks, measuring and verifying, and keeping records. Read the whole file once. The references folder
holds the long checklists; load one when you reach that step.

```
references/sources.md        where to find references, fonts, photos, colors, facts, and how to extract them
references/copy.md           the copy rules and the machine-written tells to check for
references/design.md         design guardrails, design slop, cohesion with a parent brand
references/build.md          build pipeline conventions, media, fonts, commits
references/qa.md             the audits, phone QA, accessibility, the measurement harness
references/deploy.md         deploy, verify, cache windows, redirects, build stamps
references/client.md         client feedback, pushback, records
scripts/measure.mjs          Playwright: overflow, tap targets, text overflow, alt, media at load, errors
scripts/copy_check.py        flags dashes, italics, banned and hype words, long sentences, placeholders
scripts/sheet.py             pastes screenshots into one comparison sheet
scripts/verify_deploy.sh     hash-verifies a deploy and waits out the CDN cache window
assets/                      templates for the decision record, the client feedback log, the QA record
```

## 1. Before you build

Read what already exists before you touch anything: the brief, any brand platform or identity record,
the client's notes, the last QA record, the builder scripts. A project that has a running decision record
tells you what was already tried and set aside; rebuilding a rejected idea costs a round of trust.

Settle these before the first screenshot, and write them into the record:

- **The deliverable.** What the page must do, in one sentence from the client's own words. A splash
  page that says what the project is, what it hopes to achieve, and where the content lives is a
  different build from a content site. Do not widen it on your own.
- **The branch and the preview.** Work on the named branch. Publish previews to one stable address
  (a GitHub Pages path, a Netlify site) and keep that address through the whole project. When the
  address must change, leave a redirect at the old one.
- **The rules you inherit.** Copy rules, banned words, spelling (US unless told otherwise), font licensing
  (open licenses only unless a license is in hand), guardrails against cliches, the attribution lines
  commits must carry. If the brief does not state them, propose the defaults in `references/copy.md` and
  `references/design.md` and record that you did.
- **What you will not invent.** Facts, numbers, names, handles, addresses, legal lines and dates that you
  do not have go in as `[CONFIRM: what is needed]` placeholders, never as plausible filler. A placeholder
  is honest; a fabricated statistic on a client's page is a liability.

## 2. Finding references and sources

Good pages are built from real references, not from memory. Go and look, then say where it came from.
The full method is in `references/sources.md`; the short version:

- **Design references.** Search for the specific pattern you need ("mission statement section layout
  split photo", "about page usability findings"), fetch the two or three strongest sources, and ask each
  fetch a precise question: what the layout is, where the photo sits relative to the statement, what the
  source says works and why. Favor sources that state findings (Nielsen Norman Group, editorial sites
  known for the pattern) over listicles. Write the finding into the record before you design from it.
- **Parent brand.** When the site must sit beside an existing brand, take the colors, type and devices
  from that brand's own site and files, not from a guess. Pull the exact hex values. Use one device from
  the parent (the three bars, the slant) rather than several; cohesion comes from color and type first.
- **Fonts.** Use open-licensed faces (OFL) unless the client supplies a license. Fetch the file from the
  source repository (a sparse clone of `google/fonts` gives you the TTF and the OFL text in one step),
  keep the license file beside the font in the repo, and record the license in the type study. When the
  client wants a commercial face, name the closest open stand-in, build with it in the same slot, and
  say what a license would change.
- **Photos and video.** Use what the client owns, or placeholders you can source with a known license
  (Wikimedia Commons with the license noted). Keep a credits file. Mark placeholders as placeholders in
  the record, and do not dress them with captions or credits on the page when the client has said they
  will be replaced.
- **Facts for copy.** Research with searches that name the place, the year and the population you are
  writing about, then fetch articles with an extraction prompt that asks for every statistic with its
  source and every quote with the speaker's name and role. Keep the digest in the repo. Copy that comes
  from a digest can be defended; copy that comes from vibes cannot.

## 3. Copy

Write the way a careful person talks. The full rules and the tells are in `references/copy.md`. The rules
that carry the most weight:

- Plain words. No hype, no superlatives, no "seamless", "elevate", "unlock", "journey".
- One idea per sentence. Headlines under about ten words.
- Stories, not positions. A person, a place, a thing that happened, a cost. Not an argument.
- No em dashes. No italics. Use a period or a comma. Emphasis comes from word order.
- Banned words stay banned however natural they feel. Keep the project list in the record.
- Every section needs a job. If a section exists because the layout had a gap, cut it. A page that
  says less and means it beats one that fills the fold.
- Nothing invented. `[CONFIRM: ...]` for anything you do not know.
- US spelling.

Run `scripts/copy_check.py` on the built page before every push. It flags dashes, italics, banned and
hype words, long sentences, long headlines and open placeholders. It is a flag, not a verdict; a quoted
client note may legitimately contain a dash. Read what it finds and decide.

## 4. Design

The guardrails and the design slop list are in `references/design.md`. The short version:

- No cliches of the place or the sector unless the record grants an exception (for a Maine site: no
  lobsters, no lighthouses, no flags). Reach for the real texture instead: the street, the paperwork,
  the person.
- No gradient-heavy styling, no boxes around icons for their own sake, no decorative dividers, no
  three-column feature grids with icons, no stock-photo heroes. These are the visual equivalents of
  hype words.
- One accent color with a job. If the parent brand has a gold, the gold goes on the mark, the device and
  the buttons, and nowhere else.
- Motion is slow and purposeful. A hero loop drifts; it does not pan. A footer draw happens once, when
  the reader arrives at the bottom, and it finishes clean. Respect reduced motion.
- Tap targets are 44 px or more on phones. Social icons do not need boxes; they need size and spacing.
- Text over video or photos gets a real treatment (a scrim, a band, a solid field), not a text shadow.
- When the client says "just the bars" or "don't use that font", do exactly that and nothing more.

## 5. Build

Conventions in `references/build.md`. The ones that save the most time:

- One builder script writes the whole page (HTML, CSS, JS, media copies) from a theme dictionary, so a
  variant is a dictionary change, not a second codebase. When the template uses `%` formatting, every
  literal `%` in CSS or JS must be `%%`; a missed one either crashes the build or ships `100%%` into the
  stylesheet. Grep the built file for `%%` after every build.
- Media on demand. Nine animated GIFs at load is eight megabytes on a phone. Give each clip a `data-src`
  and load the current one and its neighbors.
- Video needs a fallback. WebM does not play on every iPhone, and the sandbox may have no H.264
  encoder. Build a CSS fallback (still plates that cross-dissolve) and switch to it when `canPlayType`
  fails or `play()` rejects. Record the MP4 as a delivery item.
- Fonts embedded or self-hosted with their license file beside them.
- Commit and push as you go, with the attribution lines the project requires. Never open a pull request
  unless asked.
- Keep old addresses working with a meta-refresh redirect when a path is retired.

## 6. Measure, do not eyeball

A screenshot tells you it looks fine at one size. A measurement tells you the tap target is 35 px wide,
the track overflows the page by 80 px at 320 wide, the index lags by one on tablets, and all nine clips
loaded at open. Run `scripts/measure.mjs` at 320, 375, 390, 430, 768 and 1400 wide before you call a
section done. For interactive parts (carousels, steppers, viewers) write a small Playwright script that
drives the real gesture (a scroll nudge, a tap, a key press) and asserts the state after it. The patterns
are in `references/qa.md`.

Run the audits in this order, each as its own pass with its own record entry: footer, spacing and sizing,
usability and conversion, tap targets, phone pass, critical audit. When the user says "do all fixes", do
all of them, then show the result.

Accessibility is part of QA, not an extra: landmarks, one `h1`, alt text, focus visible, keyboard
reachable carousels, `aria-current` on the current step, `prefers-reduced-motion` honored, a dialog that
traps focus and returns it on close.

## 7. Show the work

Send a screenshot sheet, not a description. `scripts/sheet.py` pastes states or viewports side by side
in one image. For a change the client asked for, show before and after at the size they look at it. For
a phone fix, show the phone. Attach the file; do not paste a path.

## 8. Deploy and verify

Never say "live" until you have proved it. The method is in `references/deploy.md`:

1. Deploy, then fetch the served file with a cache-busting query and compare its hash to the local build.
2. Wait out the host's CDN cache window (GitHub Pages: 10 minutes) and fetch again without the query,
   from every address form the user might use. `scripts/verify_deploy.sh` does both.
3. Only then say it is live, and say which build: put a small build stamp (short hash and time) in the
   footer during the preview phase so a stale copy on the client's phone can be told from the current one.
4. If the client still sees the old page, the copy is in their browser. Say so plainly, give the
   cache-busting link, and do not redeploy to "fix" it.

A page shown inside an iframe (a concept toggle) needs a version stamp on the iframe source or it will
show the previous build for ten minutes after every deploy.

## 9. Client feedback and pushback

Log every client note verbatim with the date, then what was done about it (template in `assets/`).
When the user corrects you ("I said just the bars", "don't use the red hat display", "don't tell me
they're live until they are"), the correction becomes a rule for the rest of the project: write it into
the record and follow it. Do not re-litigate a decision the client has made. When a concept is retired,
retire it cleanly: redirect its address, keep its record, and say what carried over.

When you raise a concern and the user repeats the request, do the request, say that you did, and move on.

## 10. Records

Three files, kept current as you go, templates in `assets/`:

- **Decision record.** What was decided, why, what was tried and set aside, what is open.
- **Client feedback log.** The notes verbatim and what was done.
- **QA record.** Each audit pass: what was measured, what was found, what was fixed, what was accepted.

Write the entry in the same turn as the work. A record written later is a reconstruction.

## 11. How to talk about it

Lead with the outcome and with anything you could not verify. Plain sentences, one idea each. Numbers in
a short table, not in prose. Name a file only when the reader has to open it. No hype about your own
work. When something failed, say what failed and show the output.
