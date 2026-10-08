# Copy: the rules and the tells

The page is read by someone on a phone who did not ask to read it. Every sentence has to be worth the
thumb. These rules exist because the default output of a language model reads as a brochure, and a
brochure is the one thing a client can get anywhere.

## The rules

1. **Plain-spoken.** Words a neighbor would use. If a sentence would sound odd said aloud across a table,
   rewrite it.
2. **One idea per sentence.** About twenty words. Short does not mean clipped; a sentence beats a label
   with a colon.
3. **Headlines under about ten words.** A headline is a sentence with a verb or a noun phrase with a
   specific in it. "Young Mainers on building a life here" works. "Empowering the next generation" does
   not.
4. **Stories, not positions.** A person, a place, a rule, a cost, what happened. The reader draws the
   conclusion. Arguments go in the newsletter, not on the splash page.
5. **No hype.** No superlatives, no "seamless", "elevate", "unlock", "empower", "journey", "vibrant",
   "robust", "world-class", "cutting-edge", "transform". No "we believe". No "more than just".
6. **No em dashes. No italics.** A period, a comma, or a new sentence. Emphasis comes from word order and
   from what you leave out. (A decorative element marked `aria-hidden` is not italics; a quoted client
   note may keep its dash.)
7. **Banned words stay banned.** Keep the project list in the record and run the checker. A word the
   client has banned is banned in every tense and form.
8. **US spelling** unless the client's house style says otherwise.
9. **Nothing invented.** Names, handles, addresses, numbers, dates, legal lines: `[CONFIRM: what is
   needed]` until the client confirms. Placeholders are visible on purpose, so they get resolved.
10. **Every section has a job.** Before adding a section, say what the reader does after reading it. If
    the answer is "nothing", cut it. Copy added to fill a layout is the first thing a client notices.
11. **No numbers in prose on a brand page** unless the number is the point and has a source. Numbers
    belong in the newsletter with their sourcing.
12. **Don't number sections** in an about or mission block. Numbered steps imply a process the reader
    has to follow.
13. **Say who.** "The clips go out on the creators' own accounts." Not "content is distributed across
    channels."

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

## Writing the hard sections

**The mission or "what we hope to achieve" block.** One statement in large type that a person could
say. One paragraph of goal in plain sentences: who does what, where it goes, what it adds up to. No
numbered points, no sub-headings, no stats. A photo of the real place beside it, not a stock image.

**The follow or "where to find it" block.** Name the platforms and the handles. Say plainly what is and
is not published on this page ("Nothing is published here. The clips live on the feeds."). Include every
platform the client named; leaving one out reads as a decision.

**The newsletter block.** What arrives, how often, in whose name. One field, one button, one line of
fine print about unsubscribing. No "join the movement".

**Creator or team profiles.** The name is the identifier, then the place. Bio in the first person if the
client supplies it, or `[CONFIRM: bio]`. Handles only when confirmed.

## Checking

```
python3 scripts/copy_check.py dist/index.html --ban earn,earns,earned,earning
```

Run it on the built page, not the source, so what the reader gets is what is checked. Then read the page
aloud once, start to finish, at phone width. That pass catches what the script cannot.
