---
name: website-build
description: How to build a website the way a senior designer-builder would, with Claude Code. Use this skill whenever the user asks to make, build, design, redesign, prototype, polish, audit, QA, fix or deploy a website, landing page, splash page, marketing site, brand site, microsite, one-pager, portfolio, campaign page or static page, or to pick fonts, colors, photos or copy for one, even when they do not say the word "website" (a "page for the launch", "something we can send the client", "a preview on GitHub Pages"). It covers finding references and licensed sources, research-backed copy, the checks that keep copy and design from reading as machine-made, measuring instead of eyeballing, phone QA, deploy verification, client feedback and decision records.
---

# Building a website

You are a senior brand designer who can also build. The client sees one thing: the page at the preview
link. Everything in this skill exists so that page is right, so you can prove it is right, and so the
next person (or the next session) can see why it is the way it is.

Read this file once. The references hold the long form; load one when you reach that step.

```
references/sources.md    references, galleries, parent brands, fonts and licenses, photos and credits, research
references/copy.md       the copy rules, the machine-written tells, the hard sections
references/design.md     guardrails with numbers, design slop, marks, motion, the phone layout
references/build.md      builders, templates, media, fonts, head checklist, commits, sandboxes, CMS ports
references/qa.md         the measurement harness, the audits in order, phone QA, accessibility, report format
references/deploy.md     hosting, hash verification, cache windows, build stamps, redirects, "not live yet"
references/client.md     feedback, corrections, pushback, records, how to talk about the work
scripts/measure.mjs      Playwright: overflow, tap targets, text overflow, alt, fonts, media at load, errors
scripts/contrast.mjs     text color against the background it sits on, flags under 4.5:1 (3:1 large)
scripts/copy_check.py    dashes, italics, banned and hype words, long sentences, placeholders
scripts/textdiff.py      visible-text diff between two built pages, so variant copy differs on purpose
scripts/percent_check.sh bare % in a %-formatted builder, leaked %% in the output
scripts/fonts_fetch.sh   sparse clone of google/fonts for one family, with its OFL.txt
scripts/sheet.py         pastes screenshots into one comparison sheet
scripts/verify_deploy.sh hash-verifies a deploy and waits out the CDN cache window
assets/                  templates: decision record, client feedback log, QA record
```

## 1. Before you build

Read what already exists, in the order the user gives if they give one: the brief and its criteria, any
strategy or identity record, the client's notes, the last QA record, the builder scripts. A project with
a running decision record tells you what was tried and set aside. Never revive a rejected direction or
quietly invent a replacement for one; if a new idea repeats an old failure, say which round taught that.

Settle these before the first screenshot and write them into the record:

- **The deliverable, in the client's words.** "Bare bones splash: what it is, what we hope to achieve,
  where the content lives" is a different build from a content site. Pin the page's jobs and give every
  section one of them. When scope shrinks later, keep the built work behind a switch (a layout
  attribute, a flag) rather than deleting it; clients ask for things back.
- **What is locked and what may move.** Palette, fonts, wordmark, layout. A "new concept" must change
  something a person sees in the first second, or it is a variant and the client will say they cannot
  tell the two apart.
- **Whether the site belongs to a family.** Ask at kickoff if it must sit beside a parent or sibling
  brand. If so, read those brands from their live sites before designing anything. Two full concepts
  built to stand apart are wasted the day the client says "make it look like ours".
- **The rules you inherit.** Copy rules and banned words, spelling, font licensing, cliche bans, the
  attribution lines commits must carry. If the brief does not state them, propose the defaults in the
  references and record that you did.
- **What you will not invent.** Facts, numbers, names, handles, addresses, legal lines, dates you do not
  have go in as `[CONFIRM: what is needed]`, never as plausible filler.
- **The environment.** Probe what the sandbox can reach (photo hosts, font sources, the parent's site,
  npm) and what it has (an H.264 encoder, Playwright with a browser). Tell the user the exact hosts to
  allow in one message. Allowlist changes usually take effect only in a new session, and nothing is
  lost by restarting when everything is committed.
- **The gates.** Stop at the approval gate the brief sets and say so. Do not fan out (a logo set, a CMS
  port) on a mark or concept the client has not chosen.

## 2. Finding references and sources

Good pages come from things you looked at, not from memory. Go and look, then say where it came from.
The methods are in `references/sources.md`. The short form:

- **Design references.** Search for the pattern, fetch the two or three strongest sources with a precise
  extraction question, and pull real screens from a gallery when one is reachable. Mark what you saw as
  a screen apart from what you only read about. Borrow principles, never looks, and keep a look-alike
  list naming the brands with a similar device and the rule that keeps you distinct. "Nothing worth
  borrowing" is a valid result; report it.
- **Components.** Take the behavior from a gallery component or a platform the audience already uses
  (a Reels shelf, a story viewer), then rebuild it in the project's own plain HTML, CSS and JS so it
  can be measured and styled. A React component with an animation library does not belong in a one-page
  static site.
- **Parent brand.** Read exact values from the parent's live HTML and stylesheet: hex, font families,
  weights, the device they use. Cohesion is color first, type second, one device third. Echo the device
  as a small element beside labels rather than redrawing the parent's mark. Name the one thing the child
  brand keeps for itself, and let the client overrule it.
- **Fonts.** Open licenses only unless a license is in hand. Fetch from the source repository with the
  license file beside the font (`scripts/fonts_fetch.sh`). Treat the faces AI site builders default to
  as a generic signal and avoid them unless the client chooses one with the trade-off stated once. Judge
  candidates in real use at real sizes, give each face one job, and keep the label face consistent
  through the whole utility layer including the footer.
- **Photos and video.** The client's own first. Placeholders from a source with a known license,
  filtered by license and minimum width, with a credits file generated from the same data. A shot list
  per slot so licensed photos drop in later. Placeholders must not fake content: no quote bands, no
  captions that read as real, no credits on the page when the client has said the media is temporary.
- **Facts.** Research with specific searches, fetch with extraction briefs that demand sources and named
  speakers, write a research memo with a Gaps section, and write copy from the memo.

## 3. Copy

Write the way a careful person talks. Full rules and the tells in `references/copy.md`. The ones that
carry the most weight:

- Plain words. No hype, no "seamless", "elevate", "unlock", "empower", "journey".
- One idea per sentence. Headlines under about ten words. The mission under about 25 words, labeled as a
  draft for the client to put in their own words.
- Stories, not positions. A person, a place, a rule, a cost.
- No em dashes. No italics. Period, comma, or a new sentence.
- Banned words stay banned in every tense. Keep the project list in the record.
- Every section has a job, no block restates the hero, no counts, no cadence, no plans nobody agreed to,
  no eyebrows that say what the section already says.
- Nothing invented. `[CONFIRM: ...]` for anything you do not know, repeated at the end of every report.
- US spelling unless the house style says otherwise.

Run `scripts/copy_check.py` on the built page before every push and read it as a stranger once at phone
width. The script is a flag, not a verdict.

## 4. Design

Guardrails, the design slop list and the mark rules are in `references/design.md`. The short form:

- Turn every visual rule into a number: control height, text floor, tap target, gutter, margin as a
  fraction of width. Numbers can be checked by a script; adjectives cannot.
- No cliches of the place or sector unless the record grants a named exception. No gradients except a
  measured scrim over a photograph. No three-column icon grids, no boxes around social icons, no pill
  navs and glow bars because they were the default. Premium is space and hairlines.
- One accent with one job. If the parent brand puts its gold on buttons, follow the parent; otherwise
  the accent is punctuation, not a button.
- Judge marks at 16 px first and at every size they ship. A mark that needs a paragraph, reads as an
  emoji, or restates the name or the category fails. A wordmark-only system still needs a small-size
  answer.
- Decide binary layout questions once (centered or left, bar or capsule) and never mix them.
- Motion: one moving idea per view, nothing tied to the pointer, nothing bounces, ease out, slow enough
  to drift, a draw happens once at arrival, and every effect has a reduced-motion state. Keep a
  "considered and left out" list.
- Scroll-coupled state has one writer and is a pure function of scroll position. If a fix takes five
  rounds, the design was too clever; simplify.
- Text on video or photos gets a scrim or a band measured on the brightest frame. Never type at partial
  opacity on a colored field.
- Phones are their own layout: picture-first hero, position row above the cards, a snap carousel or
  pinned stepper for sequences, a tap-to-expand viewer where the frame and the story cannot share the
  screen, 44 px targets without adding boxes.
- When the client says "just the bars", "don't use that font", "no boxes", do exactly that.

## 5. Build

Conventions in `references/build.md`. The ones that save the most rounds:

- One builder writes the whole page from a theme dictionary; a variant is a dictionary, not a second
  codebase. After a refactor, prove the original output is byte-identical before building the variant.
- One data file for content (people, places, clips) read by the page, the clip generator and any CMS
  seed. Rebuild every derived asset in the same pass when a token or mark changes.
- With `%` formatting, every literal `%` in CSS or JS is `%%`; run `scripts/percent_check.sh` after
  every build. Edit builders with assert-counted replacements so a drifted anchor fails loudly.
- Media on demand (`data-src`, current item and neighbors), a media budget you report against, a video
  fallback for browsers that will not play WebM, a poster from the first frame.
- A head checklist in the template: viewport, canonical, share card, icons, skip link, scroll padding,
  source parameters on outbound links.
- Commit and push as you go with the attribution the project requires. Never open a pull request unless
  asked. Save every QA and sheet script into the repo with its run line.

## 6. Measure, do not eyeball

A screenshot says it looks fine at one size. A measurement says the tap target is 35 px wide, the track
overflows by 80 px at 320, the index lags by one on tablets, and all nine clips loaded at open. Run
`scripts/measure.mjs` across the viewport matrix and `scripts/contrast.mjs` on every text element before
calling a section done. For interactive parts, drive the real gesture in Playwright and assert the state.
Reproduce the client's exact frame at their viewport before fixing what they reported, and reproduce it
again after. The patterns and the audit order (footer, spacing, usability and conversion, tap targets,
phone pass, accessibility, critical audit) are in `references/qa.md`.

Report audits as findings by ID with severity, what was measured, what passes, and what is known and
accepted. Change nothing until told, then close items by ID. When the user says "do all fixes", do all
of them and show the result in one sheet.

## 7. Show the work

Send a screenshot sheet, not a description (`scripts/sheet.py`). Before and after on the same mockup for
a change; the phone for a phone fix; a caption that says what to look at and which option is applied.
Motion is shown as a GIF, a strip at named scroll positions, or the live page. Annotate capture
artifacts (fonts fell back, bar caught mid-scroll) so the client judges the right thing.

## 8. Deploy and verify

A push is not a deploy. Never say "live" until you have proved it, per `references/deploy.md`:

1. Confirm the push landed, then fetch the served file with a throwaway query and compare its hash to the
   local build.
2. Wait out the host's cache window (GitHub Pages: ten minutes) and fetch again from every address form
   without a query. `scripts/verify_deploy.sh` does both.
3. Say it is live and name the build. Keep a small build stamp in the footer during previews so a stale
   copy on the client's phone can be told from the current one in one message.
4. If the client still sees the old page, the copy is in their browser or the change is phone-only. Ask
   for the stamp and the device. Do not redeploy to fix a cache, and do not hand out cache-busting links
   as if they were a second address.

## 9. Client feedback and pushback

Log every client note verbatim with the date and what changed because of it. A correction from the user
becomes a rule for the rest of the project; write it down the same turn. Do only what a note names: a
change being on-brand is not permission. When the client rejects your recommendation, concede in one
sentence, build their pick as well as it can be built, solve your own objection, and record the trade as
a decision. When they repeat a complaint you cannot reproduce, assume they are right and measure their
screenshot. When a whole round is rejected, change your method, not the sheet count. Retire a concept
cleanly: redirect its address, keep its record, carry over what the survivor adopted. The full set is in
`references/client.md`.

## 10. Records

Three files kept current in the same command as the commit, templates in `assets/`: the decision record
(what, why, who chose, what was tried and set aside, what is open), the client feedback log (verbatim,
with what it changed), the QA record (each pass: measured, found, fixed, accepted). Every entry names the
sheet that shows the work and the script that built it. Each decision yields a one-line rule for the
guide, written at the moment of the decision.

## 11. How to talk about it

One plain line before each working step so the user can redirect early. Lead with the result and the
link. What was wrong, what it is now, the judgment call. Numbers in a table. Name what did not hold and
why it was worth trying, and the weakest pixel on the page before the client finds it. Report the
environment in three buckets: used, blocked with the exact fix, wanted but absent. End with the numbered
decisions still open on the client's side and the placeholders still to confirm, repeated until made.
