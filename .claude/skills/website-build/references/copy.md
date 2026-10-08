# Copy: the rules and the tells

The page is read by someone on a phone who did not ask to read it. Every sentence has to be worth the
thumb. These rules exist because the default output of a language model reads as a brochure, and a
brochure is the one thing a client can get anywhere.

## The rules

1. **Plain-spoken.** Words a neighbor would use. If a sentence would sound odd said aloud across a
   table, rewrite it.
2. **One idea per sentence.** About twenty words. Short does not mean clipped; a sentence beats a label
   with a colon.
3. **Headlines under about ten words.** A headline is a sentence with a verb or a noun phrase with a
   specific in it. "Young Mainers on building a life here" works. "Empowering the next generation" does
   not.
4. **Stories, not positions.** A person, a place, a rule, a cost, what happened. The reader draws the
   conclusion. Arguments go in the long form, not on the splash page.
5. **No hype.** No superlatives, no "seamless", "elevate", "unlock", "empower", "journey", "vibrant",
   "robust", "world-class", "cutting-edge", "transform". No "we believe". No "more than just".
6. **No em dashes. No italics.** A period, a comma, or a new sentence. Emphasis comes from word order and
   from what you leave out. A decorative element marked `aria-hidden` is not italics; a quoted client
   note may keep its dash.
7. **Banned words stay banned** in every tense and form. Keep the project list in the record and in the
   lint.
8. **US spelling** unless the house style says otherwise.
9. **Nothing invented.** Names, handles, addresses, numbers, dates, legal lines: `[CONFIRM: what is
   needed]` until the client confirms. Placeholders are visible on purpose, so they get resolved, and the
   UI degrades gracefully while one is unset (a form confirms in the page instead of opening a dead
   tab). Repeat the open placeholders at the end of every report. A phone number in the 555-01XX block or an
    address at example.com is fiction even when it came from an earlier draft; bracket it.
10. **Every section has a job.** Before adding a section, say what the reader does after reading it. If
    the answer is "nothing", cut it. Audit copy line by line for repetition across blocks; no block
    restates the hero, no phrase appears four times on one page.
11. **No counts, no cadence, no plans nobody agreed.** "Nine creators", "every Tuesday", "first" and
    "launching in spring" are promises. Keep unconfirmed specifics out of public copy, and after
    removing one, grep the builder and the output for residual mentions, including counters and
    stylesheet comments.
12. **No numbers in prose on a brand page** unless the number is the point and has a source. Numbers
    belong in the long form with their sourcing.
13. **Don't number sections** in an about or mission block, and cut eyebrows and kickers that say what
    the section already says.
14. **Say who.** "The clips go out on the creators' own accounts." Not "content is distributed across
    channels."
15. **Use the audience's vocabulary** from the research memo and ban the editorial phrases they do not
    use.

## The tells (what reads as machine-written)

Check for these before every push. `scripts/copy_check.py` catches the mechanical ones; the rest are
yours to read for.

- Em dashes and spaced en dashes as punctuation.
- Italics for emphasis.
- Triplets everywhere: "faster, cleaner, smarter". One or two is a choice; three is a habit.
- The contrast tic: "It's not X. It's Y." and "This isn't about X, it's about Y."
- Opening a section with a question the section then answers.
- "Whether you're a ... or a ..."
- "In today's ...", "In a world where ..."
- "Look no further", "dive in", "at the heart of", "a tapestry of", "a testament to".
- Nominalizations: "the provision of support" for "support".
- Abstract nouns doing the work of verbs: "impact", "engagement", "alignment", "ecosystem".
- Every paragraph the same length. Every sentence the same shape.
- A closing line that summarizes what the reader just read.
- A call to action with an exclamation point.
- Copy that describes the page ("This section highlights...") instead of saying the thing.
- A quote with no name, or a name with no town or role.
- Headlines that could sit on any organization's site.
- A statistic with no source. An anonymous testimonial.
- A hand-typed copyright year.

## Typographic care

- Curly quotes, with the opening mark hung. Third-party names keep their own casing even in a lowercase
  system; lowercase is a CSS transform so screen readers get the source casing.
- URLs out of running sentences and into fine print.
- Re-break headlines so a one-word accent line is not a widow. A widow dressed as a feature is still a
  widow.
- The page title carries the one-line promise, not only the name. Meta, Open Graph and Twitter
  descriptions repeat the same plain sentence, not a slogan. Tab, bookmark and search are surfaces.
- A disclosure or funder line, when the strategy calls for one, has fixed homes (near the top, its own
  section if required, the footer) with unchanging wording and normal capitals, and is not repeated
  beyond them. When the client removes it, do so, flag the consequence once for the record, keep the
  files.

## Writing the hard sections

**The mission or "what we hope to achieve" block.** One statement in large type that a person could
say, under about 25 words, labeled as a draft for the client to put in their own words. One paragraph of
goal in plain sentences: who does what, where it goes, what it adds up to. No numbered points, no
sub-headings, no stats. A photo of the real place beside it, not a stock image.

**The follow or "where to find it" block.** Name the platforms and the handles. Say plainly what is and
is not published on this page. Include every platform the client named; leaving one out reads as a
decision.

**The newsletter block.** What arrives, in whose name. One field, one button, one line of fine print
about unsubscribing. No cadence until it is agreed. No "join the movement".

**Creator or team profiles.** The name is the identifier, then the place. Bio in the first person if the
client supplies it, or `[CONFIRM: bio]`. Handles only when confirmed; a plausible fake handle looks
finished and ships.

**Placeholder copy.** Read it as a brand-new stranger. A section intro says the one thing a new reader
needs and nothing else. A visible bracket in the lede reads as broken, so put placeholders where a
reader expects a fact, not in the first sentence.

## Checking

```
python3 scripts/copy_check.py dist/index.html --ban earn,earns,earned,earning
python3 scripts/textdiff.py dist/a/index.html dist/b/index.html
```

Run the checker on the built page, not the source, so what the reader gets is what is checked. Diff the
visible text of two variants so copy differences between concepts are intentional. Then read the page
aloud once, start to finish, at phone width. That pass catches what the script cannot.
