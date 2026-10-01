# Identity system: where things stand

Saved September 30, 2026. Everything below is built as hand-drawn SVG geometry by scripts in `brand/src/`, so it can be redrawn at any size and animated by the same rules that draw it.

## Decisions so far

| Element | Decision | Why |
| --- | --- | --- |
| Lockup | **Two-line.** The state beside the name set on two lines, the state as tall as both lines, Marigold on the dot of Maine | The client's pick on October 1. The state and the name are the same size, so neither is a badge for the other. The horizontal stays for short bars |
| Brandmark | **Maine in lines.** The state drawn in horizontal lines from the precise Census outline, heavier toward the bottom, one color. Three cuts chosen by size: 16 lines, one per county, at 72 px and up, the same 16 lines heavier on a lightly simplified coast from 36 to 72 px, the simplified silhouette alone below 36 px | Chosen by the client on October 1 over the abstract margin-room mark, which is kept in `brand/identity/mark/`. The size system solves the small-size problem the silhouette had: the shape never turns to dashes, because below 36 px it is a shape again. Files: `brand/identity/logo-maine/` |
| Mural | **Grain.** Maine drawn in horizontal lines from the precise Census outline, weight growing toward the bottom, one color | The strongest single image of the project. Lives at sizes where Maine reads: the website hero and the end card |
| Relationship | The mark is a crop of the mural where one line is missing. One rule, two scales | Everything seen large is Maine. Everything seen small is the mark |
| Marigold | **The dot.** The state is one color in every cut. Marigold is the dot on the i of Maine, in the wordmark and in every color lockup, and the period after a headline. The logo's dot does not count against the frame's one Marigold | Chosen by the client on October 1 over the gold stripe. One rule anyone can apply. The state never carries a second color, which settles the Baxter separation |
| Letter marks | Set aside | The G is the generic half of the name. GM reads as General Motors |
| The abstract mark | Set aside, kept | The margin-room mark remains the stronger answer to the platform's on-the-nose test. The client preferred the state, and the size system answers the objection that mattered most |
| Outline data | US Census cartographic boundary, 1:500,000, clipped to the shoreline, 2,265 points, public domain | The legal boundary was tested and rejected: it fills the bays and rings the islands |

## Open

- Signature's typeface: Bricolage Grotesque or Commissioner with flair and volume at 100.
- Bark & Sky: draw its counterpart by the same rule in Sky and Bark, or set it aside.
- The gut check with eight people, from `00-platform.md`, has not been run.

## Files

- `brand/identity/abstract/` the Bend family, `gold-flat` is the mark
- `brand/identity/grain/` Maine in lines, the mural and the outline
- `brand/identity/marks/` the letter marks and early candidates, kept as the record
- `brand/identity/*.png` the sheets shown during the exploration, in order
- `brand/src/maine2.py` and `brand/src/data/maine-census.json` the outline

## Pushing further: four experiments

Built after the save, all on real surfaces. Sheets: `brand/identity/push-1-text-room.png`, `brand/identity/push-2-type-voice-mural.png`. Files: `brand/identity/push/`.

| Experiment | What it is | Verdict |
| --- | --- | --- |
| **Text is the room** | The field of lines makes room for the words. Lines that would cross a headline stop at it, the nearest lines bow and turn gold. On the hero, covers and the lower third | Keep. The strongest extension of the mark. The headline sits in a clearing with gold shoulders. On the lower third the band wraps the name, which suits a short band |
| **Type in grain** | The wordmark and a title drawn in the same horizontal lines as Maine | Set aside as a static treatment. Horizontal lines erase horizontal strokes, so the G's bar and the e's crossbar vanish. It may work as a moment of motion, lines assembling into the word, then the real word taking over |
| **Lines that bend to a voice** | The field bends to the loudness of the creator's audio, gold where it is loud | Hold. Compelling as a live behaviour on the video player. Too close to a podcast waveform as a static image. Needs real audio to judge |
| **The mural as a hero** | Maine in sixty fine lines to the right of the headline, the widest line gold | Keep. Quiet, precise, and it puts the state on the page without making it the logo |

## Motion prototype

`brand/identity/motion/hero.html` is a working page. Open it in a browser.

1. On load, the field opens to make room for the headline over about a second, as the headline settles in.
2. The pointer carves its own room. Lines bend around it and turn gold where they bend. When it leaves, the field closes.
3. The lede and buttons interrupt the field without gold. Marigold stays with the headline and the pointer.
4. The Maine mural draws itself in, line by line, as it enters the view.
5. With reduced motion on, the field is drawn once in its final state and nothing moves.

Recording: `brand/identity/motion/hero-motion.gif` and the frame sheet `hero-motion-sheet.png`. Recorder: `brand/src/record_motion.mjs`.

Rules for motion, drawn from the prototype:
- One moving idea per view. The field moves, the words do not.
- Nothing bounces. Ease out, 700 to 1100 ms for the field, 900 ms for type.
- Gold appears only where a line bends, and only for the headline and the pointer.
- The field never covers footage. In video it is a band, not a surface.

## Improving the brandmark, October 1

Three rounds, sheets in `brand/identity/mark-improve-*.png`, result in `mark-before-after.png`.

1. **Rooms.** The circle room with gold only on the two hugging lines, and the room as a headline block, closed and open. The circle, however treated, reads as an eye. Enclosed voids do.
2. **The open block.** Calmer, and the room becomes the shape the hero uses. It slid into document icon territory at small sizes. A lateral move.
3. **The room at the margin.** A round room opening from the left edge. Not enclosed, so not an eye. The lines part like a current for something entering from the margin, which is where every headline sits. Nine lines, heavier toward the bottom. Gold on the bends only. This is the mark.

Also fixed: lines can no longer be pushed out of the box. Files: `brand/identity/mark/` (mark, reversed, mono, white, black, small, avatar, avatar on Birch, app icon).

## The logos, October 1

One complete logo per concept, in `brand/identity/logo/`. Every file is outlined SVG, including the institute line, so nothing depends on an installed font. Sheet: `logo/logos.png`, built by `brand/src/build_logos.py`.

**Signature** (`logo/signature/`, 32 files). The margin-room mark in Spruce and Marigold, with reversed, one-colour, black and white versions and the six-line small version. The Bricolage wordmark, with the dot on the i only when it stands alone. Lockups: horizontal, stacked, endorsed, each in colour, reversed, one colour, black and white. Avatar on Spruce and on Birch, app icon, 32 px favicon. A large-size variant for 110 px and up where the field of lines is Maine itself, the room opening from the western edge. Clear space is the room's radius, one fifth of the mark's height. Minimum sizes: mark 24 px, horizontal lockup 140 px, endorsed lockup 220 px.

**Bark & Sky** (`logo/bark-sky/`, 21 files). The same rule drawn quieter: seven thin lines of one weight, the bends in Clay on paper and white on Sky or Bark. The lowercase Hedvig wordmark. Lockups horizontal, stacked and endorsed, the stacked and endorsed ones centred. Avatar on Bark and on Sky, app icon, favicon.

Open on the logos:
- The Maine variant of the Signature mark is rough where the room meets the western border. Keep it as an option for the gut check, not as a default.
- Bark & Sky's Clay accent is almost invisible on paper. That is in character for the concept, but white on Sky reads better, and the mark sits small against the serif in the horizontal lockup.

## The logo, October 1: Maine in lines

The client's call: the lines with the state of Maine are the logo. Built complete for both concepts in `brand/identity/logo-maine/`. Sheets: `logos.png`, `size-system.png`, `signature.png`, `bark-sky.png`.

**Size system.** One drawing, three cuts.
- Full, 72 px and up: 16 lines, one for each of Maine's 16 counties, weight from 2.6 to 4.4 percent of the height. The first line sits on the crest at Fort Kent and the northern border is drawn as one line, so the top of the state is whole. The count was the client's idea on October 1, and it gives the drawing a reason it did not have.
- Mid, 36 to 72 px: the same 16 lines, heavier, from 3.4 to 4.6 percent of the height, on a coast simplified by 0.6 percent. The horizontal, endorsed, compact and right-hand lockups ship with this cut, because in those lockups the mark is 36 to 60 px tall at every common size. A large version of the horizontal and endorsed lockups carries the full cut for 600 px wide and up, and a solid version serves under 300 px wide. Every lined version of the mark has sixteen lines, so the county count holds everywhere the lines appear.
- Solid, below 36 px: the silhouette simplified by 1.2 percent of the height. Never Marigold, which keeps us clear of Baxter Brewing's orange Maine.

**Rules.**
- The wordmark keeps its dot on the i only when it stands alone. With the mark present it is solid, so Marigold appears once.
- In lockups the state stands taller than the capitals, like a flag beside the name: 96 units against a 66 unit cap height, with a 26 unit gap.
- The video bug uses the solid cut with the wordmark, Birch on footage, no gold.
- Clear space on every side is one tenth of the mark's height. Minimum sizes: mark 16 px (solid), horizontal lockup 120 px, endorsed lockup 220 px.

**Trade accepted.** The platform's on-the-nose test says the name already says Maine, and a mark that says it again restates the name. The client weighed that against recognition and chose recognition. The grain, the weight gradient and the single gold line are what keep it from being another Maine silhouette.

**Grades.** Full mark A-. Horizontal and endorsed lockups A-. Stacked lockup B+. Size system B+. Avatars B+. Bark & Sky version B+, with the Clay line subtle by design.

## Applied, October 1

The Maine logo on the eight surfaces from the platform, in `brand/identity/apply/` (`apply.html`, `mockups/`, `applied-sheet.png`). Built by `brand/src/build_apply.py`, rendered by `render_apply.mjs`.

| Surface | Cut used | Note |
| --- | --- | --- |
| Video, first seconds | Solid, with the wordmark, Birch | The bug is 22 px tall at 360 wide. Nothing else on the footage |
| Lower third | None | Name and town, plain, on the safe line. The bug stays |
| End card | Full mural, 48 lines | The mural carries the frame. The widest line is the Marigold, so the headline ends in a plain period |
| Profile grid | Full, in the avatar | Covers keep the round-two rules |
| Avatar among accounts | Full at 110, mid at 40, solid at 16 | One cut per size, as the rule says |
| Substack header | Horizontal lockup, reversed | The disclosure strip under the masthead |
| Website hero | Mural, 64 lines in Moss, widest Marigold | Headline, lede and buttons stacked at left so the right belongs to the state. The lockup in the nav |
| Collab post | Solid, with the wordmark | Same bug as the video |

The motion prototype (`brand/identity/motion/hero.html`) now carries the lockup in its nav. The field motion stays: Maine is drawn in lines, so lines that make room for words are still the brand's language.

## Where the yellow goes, October 1

The client asked whether there is a better way to use the yellow in the logo. The current answer is a rule of geometry: the widest line is Marigold. A rule is not an idea, and the line is the weakest-contrast element of the logo. Four placements were built in `brand/src/build_gold.py` and shown on one sheet, `brand/identity/gold/yellow-options.png`: each on the lockup at 96 and 44 px, reversed, on the avatar on a light field, and the two strongest on the end card.

| Option | What it is | What the sheet shows | Grade |
| --- | --- | --- | --- |
| A, the stripe | The widest line of the state is Marigold. Current | At 44 px the gold line is about 1 px tall and disappears on white. The one-color version is a different logo. A horizontal gold line through Maine sits closer to Baxter Brewing's orange ridgeline than it should | B |
| B, the dot | The state is one color. Marigold is the dot on the i, as in every headline | At 44 px the dot is about 5 px across and still reads. The mark is one color in every cut, so color, mono, embroidery and vinyl are the same drawing. The end card gets its headline dot back and the mural turns Birch | A- |
| C, the thread | The widest line runs out of the state and reaches the name | The boldest of the four and the only one with a picture in it: a map's leader line, the state pointing at its name. It fails at 44 px for the same reason A does, and it is a connector, which is a cliché of the category | B- |
| D, the baseline | No gold in the state. A Marigold rule under the name | Arbitrary. The avatar version reads as an underline | C+ |

**Recommendation.** B. Marigold becomes punctuation, one rule for the whole brand: the dot on the i, the period after a headline, once per frame. The state stays Spruce or Birch and never carries a second color, which also settles the Baxter separation for good.

**Trade.** The mark alone, in the avatar, the app icon and the favicon, carries no Marigold. On the sheet the A avatar's gold line at 110 px is about 2 px tall, so little is lost. The yellow lives in the type and in the Marigold field every ninth frame.

**If B is chosen.** The lockups keep the dot on the i in every version. The full and mid cuts lose the gold line. The mural loses its gold line, and the end card and hero headlines get their dot back. The motion prototype's arriving gold line goes. Bark & Sky is unaffected in color, since it uses Clay, but its lowercase Hedvig wordmark has two i's, so its state should simply go one color with no Clay in the logo. Nothing changes until the client chooses.

## The dot, October 1: chosen, and the lockups

The client chose B. Applied in `brand/src/build_logo_maine.py`, the eight surfaces, and the motion prototype. The mural lost its gold line and the end card and hero headlines got their dot back. The mark alone carries no Marigold.

**Lockups**, in `brand/identity/logo-maine/signature/`, sheet `lockups.png`. Each in color, reversed, mono, black, white, and the mid-cut small version.

| Lockup | Use | Grade |
| --- | --- | --- |
| Two-line | **Primary**, chosen by the client on October 1. The state beside the name on two lines, as tall as both. End card, Substack masthead, merch, print, square posts | A |
| Horizontal | Short bars: the website nav, the video bug with the solid cut, co-branding strips | A- |
| Horizontal, state after the name | In the files, not recommended | B |
| Compact | The mid cut inside the cap height. Footers, bylines | B+ |
| Stacked left | Narrow columns, the left-aligned title card | B+ |
| Stacked centered | Centered title cards, print covers | B+ |
| Endorsed | Horizontal with the disclosure line. Anywhere the Institute must be named | A- |
| Endorsed, stacked | End card, back of print | B+ |
| Wordmark alone | Where the state is already in frame, as on the end card and the hero | A- |

The one-color versions are the same drawing as the color versions with the dot in the ink color, so one file set serves print, embroidery and vinyl.

**Two colors in the name, tested October 1** (`two-color-test.png`). Maine in Moss, Generation in Moss, Maine in Marigold and Generation in Stone, each on the horizontal and two-line lockups. Rejected. Splitting the color splits the name into a modifier and a noun, and the quieter word drops back on every background. Marigold type fails contrast on Birch and puts a yellow Maine next to a Maine shape, which is Baxter's territory. The name stays one color. Stacking is allowed only in the two-line and stacked lockups, never as a free setting in headlines.

**Yellow by line weight, tested October 1** (`brand/identity/gold-mark/gold-mark.png`, `brand/src/build_gold_mark.py`). The client asked for Marigold in the brandmark mirroring the thickness of the lines from top to bottom. Four readings: Marigold lines interleaved and heavy at the top, each line split between ink and Marigold, thin Marigold lines mirroring the ink's weight, and a fade from ink to Marigold. At 240 px on Spruce the mirror reading is handsome. At 96 and 44 px every reading blends to one color, and that color is yellow or olive: a yellow Maine at small sizes, which is Baxter's mark, and a muddy one on Birch. Rejected for the logo. The one-color mark and the dot stand.

**The stamp, October 1** (`brand/identity/stamp/`, `brand/src/build_stamp.py`). The client's idea for an alternate brandmark: a square of sixteen lines with the solid state on it. Eight treatments at 240, 110, 48 and 24 px: the state in Marigold, Birch and Moss on Spruce lines, in Spruce and Marigold on Birch lines, and three knockouts where the lines stop short of the state. Under review. The knockouts are the strongest: the state is the one place the lines do not go, which is the same idea as the field motion on the website, and they use one ink on one field. A solid Marigold state is the Baxter Brewing problem and is shown only because it was asked for.

**The lined dot, tested October 1** (`dot-lined-test.png`). The client asked whether the dot on the i could carry the line treatment. Five versions on the horizontal lockup at 900, 480 and 300 px: the solid Marigold dot, the dot in four and in three Marigold lines, the dot in lines of the ink, and a Marigold dot with the ink's lines through it. Rejected. At 900 px the lined dot reads as a stack of coins or a loading spinner above the i, and it fights the state, which is already the lined element in the lockup. At 480 px the lines merge and the dot is a slightly dull Marigold. At 300 px there is no difference. The lines are the state's. The dot stays solid.
