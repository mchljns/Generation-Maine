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
- Full, 72 px and up: 16 lines, one for each of Maine's 16 counties, weight from 2.6 to 4.4 percent of the height. The first line sits at 3.4 percent of the height, where the state is two separate pieces each crossed once: the northwest tip at Estcourt Station and the hump over the St. John valley. Each is drawn as a short pill 2.2 line weights long, so the two points match; the client saw the earlier pill-beside-a-dot as uneven and the equal dots as too small. At 2.4 percent the hump was still two tiny pieces and drew as two overlapping dots, which the client caught in the hero on October 1. The count was the client's idea on October 1, and it gives the drawing a reason it did not have.
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

## Grade, October 1: Signature with the Maine mark

The whole concept as it stands: Bricolage and Inter, the Spruce, Birch and Pine fields with Marigold once per frame, the sixteen-line state in one color, the solid Marigold dot, the two-line lockup as primary. Graded against the platform's eight criteria on the applied surfaces in `brand/identity/apply/`.

| Criterion | Grade | Why |
| --- | --- | --- |
| 1. Signs, does not cover | A- | The solid bug with the name sits in the corner at 22 px tall. It reads as a sign-off, not an ad |
| 2. Survives the crop | B+ | The size system handles it: lines at 110 px, solid at 32 px. The cost is that the avatar and the favicon are a plain silhouette, which is where the brand is least itself |
| 3. Carries a person | A | Unchanged from round two: the name and town are one plain line, the headline is the loudest element, the logo is small |
| 4. Neutral | A- | A state outline is the most neutral Maine symbol there is. One color and no flag colors keep it there |
| 5. Both audiences | A- | The lined state is at home as a TikTok avatar and as a Substack masthead. The two-line lockup carries the Institute line without looking like a letterhead |
| 6. Stands without photos | A | The mural is the strongest thing in the project. The hero and the end card need no photo |
| 7. Ownable | B+ | The lined construction, the weight gradient and the two points are ours. The shape is shared with every Maine brand. One color and no Marigold on the state keep it clear of Baxter |
| 8. Easy to make | A- | One lockup, one dot rule, three cuts chosen by size. A staffer can place it without a guide |

Concept grade: **A-**. The two B+ rows are the same fact seen twice: a state silhouette is recognizable, and recognizable means shared. The platform's on-the-nose test still says the mark restates the name. The client weighed that against recognition and chose recognition, and the sixteen lines, the two points and the dot are what make it ours anyway. The grade goes to A when the brand has lived in the world long enough that the lines alone, with no outline, are read as Generation Maine.

## The splash page, October 1

One page in `brand/identity/splash/` (`brand/src/build_splash.py`, renders in `splash-desktop.png` and `splash-phone.png`, hosted preview published as a private artifact). No photos. The line field is the only picture.

**Motion, and why each piece is there.**
- The hero field makes room for the headline and the lede on load and for the pointer as it moves. The lines stay Moss, so the headline's dot is the frame's one Marigold. This is the brand's language: lines that make room for a person's words.
- The mural draws itself in as it enters, line by line from the top, with the two points first.
- The headline, lede and buttons rise in over 900 ms, staggered by 120 ms. Nothing else on the page animates on load.
- Creator cards reveal a faint field of lines as they scroll into view, staggered by column, then settle. The lines return on hover.
- Reduced motion: the field is drawn once in its final state, the mural is complete, nothing rises.

**Content.** Nine creator cards on the round-two cover rules, each with a real town and a placeholder name. Three Substack posts as placeholders. The Institute line appears in the strip under the nav, in its own section and in the footer. Every unknown is a `[CONFIRM: ...]`. The signup form validates and confirms in the page because there is no backend yet.

**Checks.** Rendered at 1440 and 390 px: no horizontal overflow, no console errors. Dark theme defined through tokens.

**Splash round three, October 1.** Client calls: the Maine Policy Institute line comes off the page entirely. This reverses the credibility stance in `01-strategy.md`, which put the funder's name near the top, in its own section and in the footer. Recorded as the client's decision; the endorsed lockups stay in the files. Other changes: the nav uses the compact lockup so the mark centers with the links; the hero field is six lines with no pointer reaction and a slow drift; the page background changes color as each section passes the middle of the screen (Spruce, Birch, Sand, Marigold, Birch, Sage), which also answers the note that the page was too green; the story cards carry a video still placeholder with a spoken caption and a duration, the content a creator would upload; a Marigold "In their words" section holds three placeholder quotes; the copy was rewritten plainer throughout with no counts and no cadence. Rendered at 1440 and 390 with no overflow and no errors. `splash-scroll.png` shows the page at each scroll position.

**Splash QA, October 1: unreadable text on scroll.** Cause: the page carried dark-theme token overrides that turned the text light in a viewer set to dark mode, while the scrolling backgrounds stayed Birch, Sand and Marigold. Fix: the page commits to one palette in every theme. Verified in a dark-mode render at each section and mid-transition (`splash-darkmode-qa.png`).

**Splash round four, October 1: one section per creator, with video.** The card grid is gone. Each creator has a section: a 9:16 clip on one side, the story title, the spoken line, name and town and a link on the other, sides alternating, page background alternating Sand, Birch and Sage. Clips play while on screen and pause off screen, and wait for a tap under reduced motion. The nine clips are placeholders recorded from a brand animation (`brand/src/make_clips.mjs`): a field of lines, the spoken line arriving as captions, the lower third with the bug. They ship with the page in `brand/identity/splash/media/` until the creators' own videos replace them.

**Hero field and line ends, October 1.** The client saw the hero's background lines competing with the mark's lines. Tested four heroes (`splash/hero-field-options.png`): the field behind everything, no field, a faint field only under the text, and no field with square-cut mural lines. No field wins: the mural is the only lines in the frame, and the motion is the mural drawing in, the type rising and the page color changing on scroll. The field of lines leaves the splash page and stays in the kit as a cover and video device. Square-cut line ends were tested on the mark (`logo-maine/line-ends.png`): sharper at 260 px, no different at 44 px, and the two points at the top become squares beside a round dot. Round ends stay.

**Splash round five, October 1: the pinned stage.** Refero and 21st.dev were searched for components. Refero returned generic marketing pages, nothing to borrow. 21st.dev's sticky-media pattern (media pinned on one side, text panels scrolling past, media swapping per panel) was the one idea worth taking, and it was rebuilt in the brand's own code rather than installed: the hosted page cannot load React or animation libraries, and the design is ours. The nine creator sections became one section: a pinned 9:16 clip with an index of nine marks, and nine text panels that scroll beside it. The clip crossfades to the story in view. Phones get a clip per panel. The page shortened and all nine creators stay (`splash/stories-sticky.png`).

**Splash round six, October 1: the nav.** The plain green bar is gone. The bar is transparent over the hero and turns to a frosted Birch bar with the Spruce lockup once the hero scrolls away. Four links, About, Stories, In their words and Follow, with the active section marked by the Marigold dot. A "Get the newsletter" button on the right. On phones the links fold into a Menu that opens a full-screen Spruce sheet with the links set large in Bricolage, each ending in the dot, and the newsletter button at the bottom. Escape and any link close it (`splash/nav.png`).

**Nav, from 21st.dev, October 1.** Three searches. The floating capsules, mega-menus and glow bars were left alone. Two behaviours were taken and rebuilt in the brand's code: the bar slides away on scroll down once the hero has passed and returns on scroll up, so it never sits over the pinned stage while someone reads; and the phone menu's links enter staggered by 60 ms, with the button following. Both stop under reduced motion.

**Two nav styles, October 1.** The client asked not to rule out SaaS patterns. Both now ship in the page for comparison (`splash/nav-styles.png`). Default: the full-width bar, transparent over the hero, frosted Birch once scrolled, active section marked by the dot. Adding `#capsule` to the link switches to the SaaS style from 21st.dev's morphing navbar, rebuilt in the brand's code: once scrolled, the bar becomes a floating frosted capsule, 52 px tall and 880 px wide, with pill links, the active one filled Spruce, a pill button, and a reading-progress line along the bottom in Spruce. Both hide on scroll down and return on scroll up. Decision pending.

**Body type, October 1.** The client asked for a different body copy style. Five faces were set on the same hero, About columns, story panel and nav (`splash/body-type.png`): Inter, Atkinson Hyperlegible Next, Commissioner with flair and volume at 100, Hedvig Letters Serif and Instrument Sans. Commissioner is applied: it was the type study's sans pick for Signature, it has a voice in quotes and labels that Inter lacks, and it keeps Signature a sans. The flair and volume axes are pinned at 100 and the file is subset to Latin (`generation-maine/assets/fonts/commissioner-flair.*`, OFL). Hedvig Letters Serif stays the alternative: more editorial, closer to Substack, but it is Bark & Sky's face and would blur the two directions. Inter remains in the kit files until the kit is rebuilt.

**Body copy contrast, October 1.** Every text element on the splash page was measured against its real background at each scroll position. Ink on Birch, Sand, Sage and Marigold passes AAA. Birch on Spruce passes AAA, including the 90 percent lede and the 80 percent footer line. Buttons pass AAA both ways. The one failure was the muted grey for secondary copy, Stone at #5E6A63: 4.34 on Sand and 4.38 on Sage, under the 4.5 the AA standard asks for body text, and 4.96 on Birch. The page's muted token is now #4F5B55: 6.2 on Birch, 5.5 on Sand, 5.5 on Sage, 7.1 on white. On Marigold it is 3.8, so Marigold sections carry only ink, which they do. Stone stays in the palette for the kit and for the lines in video, where it is never body text.
Two of the placeholder clip tones also failed for their captions, 4.27 and 3.93. Those tones are now darker clay browns, 7.3 and 6.4 against the Birch caption, and the clips were re-recorded.

**Body type, second round, October 1.** Commissioner was still too close to a default. Eight faces with character were set at 17 px, and the four strongest at 19 px (`splash/body-type-2.png`): Labrada, Newsreader, Finlandica Text, Schibsted Grotesk, Mozilla Text, Stack Sans Text, Epunda Sans and Piazzolla. Labrada is applied at 18 px on a 1.55 line: the type study's pick for character that still reads as credible, a serif that makes the page read as a publication rather than a product, and sturdy enough for the nav and buttons. Finlandica Text is the sans alternative, warm and a little odd. Newsreader reads well but is now common on Substack-style sites. Files: `generation-maine/assets/fonts/labrada-var.ttf`, OFL.

**Body type, second round, October 1.** Commissioner was still too close to a default. Eight faces with character were set at 17 px, and the four strongest at 19 px (`splash/body-type-2.png`): Labrada, Newsreader, Finlandica Text, Schibsted Grotesk, Mozilla Text, Stack Sans Text, Epunda Sans and Piazzolla. Labrada is applied at 18 px on a 1.55 line: the type study's pick for character that still reads as credible, a serif that makes the page read as a publication rather than a product, and sturdy enough for the nav and buttons. Finlandica Text is the sans alternative, warm and a little odd. Newsreader reads well but is now common on Substack-style sites. Files: `generation-maine/assets/fonts/labrada-var.ttf`, OFL.

**Body type, third round, October 1.** Client call: a sans, slightly larger, and DM Sans. Six sanses were set at 19 px and three at 20 px (`splash/body-type-3.png`): DM Sans, Finlandica Text, Schibsted Grotesk, Hanken Grotesk, Figtree and Onest. DM Sans is applied at 19 px on a 1.55 line, text optical size, weight variable, subset to Latin (`generation-maine/assets/fonts/dm-sans-var.ttf`, OFL). Noted for the record: DM Sans is well drawn and the most used body sans on generated pages, so the brand's distinctness rests on Bricolage, the dot, the lines and the color system rather than on the body face. Finlandica Text and Schibsted Grotesk remain the alternatives with more of their own voice.

**Nav QA, October 1.** Client caught the headline scrolling under the transparent bar before the first section arrived, in both styles. Fixed: as soon as the page moves more than 12 px the bar takes a solid Spruce ground with a faint hairline, at 60 px tall; once the hero leaves it changes to the frosted Birch bar, or the capsule. Verified at 140 and 300 px of scroll in both styles (`splash/nav-qa.png`).

**Light fields and Marigold QA, October 1.** The client called the Birch cream an AI default on the page. Six light fields were tested across the hero, About, a story panel and the follow row (`splash/light-field-options.png`). Applied: Fog, white tinted with Spruce, #EEF2EE, with two deeper steps, #E2E8E2 and #D3DDD4, replacing Sand and Sage on the page. Reversed text on Spruce follows it. Birch stays in the kit palette for video and print until the kit is rebuilt. Marigold QA: measured at the real scroll position, every text on the Marigold section is ink at 8.3. The failure was next door: the moving page color carried Marigold under the newsletter's muted grey at 3.8 during the transition. The Marigold section now paints its own background and no longer drives the page color, so Marigold never sits under muted text. Quote footers on Marigold are full ink, no opacity.
Client call, same day: the light fields run from white into light green. White #FFFFFF for About and the newsletter, a pale green #E6EEE8 behind the stories, the deeper sage #D3DDD4 for the follow row. Reversed text on Spruce is white. Contrast re-measured, nothing under 4.5.

## Splash round seven: QA, the hamburger, the pin

A pass over both widths before anything new was added.

- The newsletter section collapsed into two squeezed columns on phones. A later rule beat the phone rule. The phone rule now comes last.
- Dead CSS from the old card layout and a duplicate set of stage rules came out.
- Anchors landed under the fixed bar. Sections carry a scroll margin now.
- Phone clips are a little narrower, so nine stories run shorter.

The phone menu is a hamburger: three lines, round ends, which fold into a cross in place. The sheet sits under the bar and fades in, so the lockup and the button never jump.

The hero's period moved onto the state. The headline ends on "here" and the Marigold dot sits where "here" is: on the map, at the town the current story was filmed in, with a slow pulse ring and a caption below the state, "Filmed in Skowhegan". Every four seconds it moves to the next town. The dot keeps the size of a headline period and wears a Spruce halo so it reads on the white lines. The hero still carries Marigold once.

Why this and not a moving background: a shifting field behind the mural was tried earlier and removed, and a slow color drift either goes unnoticed or starts to look like a gradient. The pin puts the motion on the one thing the hero is about, where the stories come from. Reduced motion shows a still pin and no cycle.

Other motion added, all on scroll and all off under reduced motion: the thin rules above the about columns and the quotes draw from the left; the pinned clip settles from a slight zoom as it changes; the footer lockup draws its sixteen lines when it enters, so the page ends the way it began. Considered and left out: parallax on the mural, hover effects on the follow links, a count or ticker, anything on the pointer.

Town coordinates are town centers and carry a [CONFIRM] until the creators are cast.

Revised the same day: the map pin and the "Filmed in" caption are out. The period stays at the end of the headline and pulses like a location marker, a ring breathing out of the dot and fading, every 2.4 seconds. The dot itself holds still. Town coordinates stay in the data for a later map.

## The follow row and Substack

The follow row carries the four platform marks, drawn by hand at 24 units in one color, so they take the ink of whatever field they sit on. Instagram, TikTok and YouTube link to the accounts. Substack links to the publication.

How Substack connects to the site. Substack is a hosted newsletter. The emails, the subscriber list and the archive all live at [name].substack.com. The site touches it in three places:

- Subscribing. Substack gives every publication an embed, a small form served from substack.com in an iframe. On the live site that iframe sits where the mockup's form is now. The mockup cannot load it because the artifact host blocks iframes. There is no public API for adding a subscriber from our own form, so the embed, or a link to the Substack signup page, is the honest choice.
- The posts list. Every Substack publication has an RSS feed at [name].substack.com/feed. The WordPress theme reads it with fetch_feed, caches it for an hour, and fills "The full story, by email" with the latest three posts: title, first line, author and date. Nothing is typed twice.
- Reading. Each post links out to Substack. Readers who subscribe there get the email. The site is the front door; Substack is the room.

If the team would rather own the list, Buttondown or Beehiiv offer the same three pieces with an API for the form. Substack wins on cost (free until paid subscriptions) and on the network of readers it already has. [CONFIRM: platform choice]

## The creators section

The section is about the creators now, not the stories. The heading reads "The creators" and the line under it says what the reader needs: nine young Mainers in nine towns, each filming where they live. The creator comes first in every panel, with a one-line bio placeholder, then the story.

The two-column layout no longer scrolls nine panels past a pinned clip. The whole block pins for nine steps of scroll. At each step the clip crossfades and the next creator's details arrive from the right, line by line, while the last one slips out to the left. Scrolling back reverses the direction. The index marks on the clip jump to a creator. Phones keep the stacked list with a clip per creator. Reduced motion swaps with a fade and no movement.

Under the two columns, a row says where you are among the nine: a counter on the left, nine short lines with the current one in ink and the passed ones faded, and the next town on the right so the reader knows what is arriving. The lines are buttons and jump to a creator. The marks that used to sit inside the clip are gone; one indicator is enough. Phones hide the row, since their list scrolls on its own.

## Capsule, green about, the fade to white

The capsule is the only nav. The bar over the hero folds into the capsule on the first scroll: height, width, corners and background all move together over about half a second. No hairline under it, just a soft shadow. It hides on the way down past the hero and comes back on the way up. The footer switch is gone.

The about section is Spruce, white text, white rules. The page itself starts green, so hero and about read as one block. Once about reaches the top of the screen the page fades to white behind it, and the creators arrive on white. The light fields after that stay as they were.

The hero period's pulse ring now draws behind the letters, so the ring breathes out from under the last letter instead of over it.

Fix: the creators could land on green. The page color was set by two things at once, a scroll rule for the green block and an observer for the sections after it, and during a smooth scroll the observer could fire first and get overwritten. The color is now one calculation on every scroll frame: green while about's top is below the top of the screen, otherwise the color of the last section whose top has passed the middle of the screen, white by default. Checked by slow scroll, fast scroll and the nav jump at four viewport sizes.

Second fix: the page now turns white once the about section reaches the middle of the screen, not its top. About paints its own green, so the earlier switch costs nothing and the creators heading is on white as soon as it appears under the green block.

## Each creator, as a profile

The creator panel is a profile now. The eyebrow is the town. The headline is the creator's name, or their handle if that is how people know them. Under it, two or three sentences in their own words, then the latest story with its length, then their Instagram, TikTok and YouTube handles with the hand-drawn marks.

The clip carries a social header: the creator's avatar in a circle, their handle in bold and their name under it, the way a post looks on their own feed. The header belongs to the page, not the clip, so the same clip works anywhere and the clips themselves carry only the caption and the brand bug.

What this asks of WordPress. A Creator post type with these fields: display name, handle, town, bio (two or three sentences), avatar (the featured image, square, shown in a circle), one clip (a video upload or a link), the latest story (title, link and length), and three social URLs. The theme draws the header from the avatar and handle. The creator fills this in once and the page updates itself.

The about section is where the page turns white. It starts on the green with white text. When it reaches the top of the screen the page fades to white and the text to ink together, over about seven tenths of a second, and the creators arrive already on white.

Third pass on the fade, after it still felt buggy. The cause was timing: a fade on a clock kept running while the reader kept scrolling, and the text and the field faded on separate clocks, so for a stretch grey type sat on a mid green. Now the fade is driven by scroll position. As the about section rises through the upper half of the screen the page mixes from green to white in step with the hand, is white by the time about reaches the top, and reverses the same way on the way back. The type does not crossfade: it switches from white to ink in one quick step once the field is 40 percent white, where both colors still read. The creators section always arrives on white. No timers remain in that zone. Latest story is gone from the creator panel.

The fade now begins with the first pixel of scroll. From the top of the page until the about section reaches the top of the screen, the page mixes from green to white in step with the scroll, so the reader lands on a white about section. The hero paints its own green, so what shows is the about section lightening as it rises.

The fade now finishes earlier: it runs from the first pixel of scroll and is complete once the about section's top has risen to 60 percent of the screen height. By the time the about heading is in the upper part of the screen, the page is fully white.

The gap between the creators head and the stage is closed. The pinned block used to be centered in a full screen height before it pinned, which opened an empty half screen. It is now its own height and sits just under the capsule when pinned, with a small margin under the head.

In the creator panel the Marigold period moved from the name to the town. It sits after the location in the eyebrow and pulses like the hero's period, so the dot marks a place in both spots where it appears. The name carries no dot.

## Snow replaces cream on dark fields

The reversed mark was Birch, the kit's cream. Against the page's pure white type and fields it read as yellowed. A new near-white, Snow #F7F8F6, now carries the reversed mark in every logo file, the nav and sheet, the hero type and buttons, the about type before it turns to ink, the footer, and the hero mural. It is white with the smallest lean toward the greens, so it sits with the palette without looking like cream. Birch stays in the kit for light fields and the one Birch-field avatar.

Room after the creators. The stepper used to run straight into the Marigold section, with the position row almost touching it. The creators section now carries a tail of about a tenth of the screen height, so the row and the next section breathe.

The footer wordmark pings. Once the footer is on screen, the dot on the i sends out the same slow ring as the hero period and the town dots, so the page closes on the mark the way it opened.

## The signup hand-off

The form's action is the publication's subscribe page on Substack, with the address in the query string, opened in a new tab. Substack fills its field from the query, sends the confirmation email and shows its own confirmation page. The splash page stays put and shows its own "check your inbox" line. Substack offers no return URL after a free signup, so the confirmation page is theirs; a custom domain on the publication puts our name on it. For a visitor who never leaves the page, the server relay in the theme is the route, with this hand-off as its fallback. The publication address is a CONFIRM, and until it is set the form confirms in the page only.

The position row names the next creator rather than the town, since the section is about the people.

## Where the redirect lives in WordPress

Settings > Newsletter, a small page in wp-admin. Four fields: the publication's subscribe page URL, open in a new tab, the line shown after submit, and the small print under the form. The URL is checked to be https and to end in /subscribe. A Newsletter Signup block renders the form from those settings, so no template holds the address. With the URL empty the form hides itself and shows an admin-only note pointing at the settings page. The hand-off needs no script; a few lines show the confirmation line in the page after submit.

## Buttons

Every button on the site is a pill. The capsule nav was already a pill and the brand's lines end round, so the squared corners on the hero and form buttons were the odd ones out. Colors: the primary action is Spruce with Snow type on light fields, and Snow with Spruce type on green. The secondary action is an outline in the current color. Hover lifts the button two pixels and deepens the fill one step, Spruce to Pine or Snow to white. The email field is a pill to match its button. Marigold is never a button; it stays the dot. The theme will carry the same rule in theme.json.

## The creators on phones

Phones keep the pinned stepper rather than a long list. The clip sits on top, the creator's details under it with the bio held to four lines, and the position row under both. Scrolling steps through the nine the same way as on desktop, and the next creator's details arrive from the right. The details block takes the height of the tallest panel so the row sits close. The section clips horizontally so the slide-in offset never widens the page. Checked at 390 by 844 and 375 by 667.

The hero's second action is a text link, not a second button. One pill, "Watch the stories", and beside it "Get the newsletter" in Snow with a short underline that draws to full length on hover. The capsule carries the newsletter button, so the hero does not need two.

At rest the bar is a Moss band over the hero, a horizon line the capsule folds out of on the first scroll. Snow type on Moss reads at 5.4 to 1. The band drops away when the phone menu opens. A Sage band was tried and cut the green block in two; transparent left the capsule arriving from nowhere.

The hero text link is underlined full width at rest; the line brightens and drops a touch on hover. A partial underline read as broken.

No blended type over green. The nav links sat at 88 percent, the hero lede at 92, the about paragraphs and footer at 80 to 82. Over Moss and Spruce those blends mixed into a pale green that read as a wrong color beside the solid mark. Every piece of type on a green field is now solid Snow. Nav hover is an underline rather than an opacity change.

Snow adjusted to #F9F8F6. The first Snow, #F7F8F6, had green as its highest channel, and small type takes on the hue of its surround, so on the Moss band and the Spruce hero it read as pale green. The new value is neutral with a hair of warmth and reads white on every green. Every logo file, the surfaces, the motion prototype and the splash page carry it.

Snow is pure white, #FFFFFF. Two near-whites were tried on the greens and both read as pale green to the client's eye, so the reversed mark and all type on Spruce, Moss and Pine are white. The token name stays so the files need no renaming.

The nav band is Pine, not Moss. White on the mid-green Moss took on a cast by contrast and read as pale green even at 255,255,255. On Pine, the darkest green, white reads white, the band sits as a shadow line over the hero rather than a stripe, and the page opens on the footer's color. Ink was crisper still but read as browser chrome; Sage capped the hero.

## The WordPress build

The splash page is now a block theme, built so that every piece of copy is a block and every creator is a post.

What the editor can change: every headline, paragraph, link label and button on the page, in the site editor. Section headings carry their Marigold period automatically, so a rewrite keeps the dot. The four platforms in the follow row are small groups with a heading and a link; their marks come from the stylesheet.

What lives on the Creator post: name, bio, avatar as the featured image, handle, hometown, the clip as an upload or a link, its length, and three social links. The Creators block reads every published creator and renders the pinned clip with the creator's avatar and handle on it, their details beside it and the position row under both. With no creators it shows a short note.

What is not editable in the page: colors, type, the pill shape and the motion. They live in theme.json and the stylesheet. The stylesheet is generated from the same CSS as the splash mockup, so the two cannot drift.

The newsletter: one address under Settings > Newsletter drives the signup hand-off and the latest-posts feed. The form hides until the address is set.

Tested in a local WordPress on SQLite: the front page at 375, 768 and 1440 with nine creators and with none, the site editor opening the template with every block valid and the theme's styles in the canvas, the Creator screen, the admin note when no newsletter address is set, PHP lint on every file. The one fault found was a stray brace in the shared CSS that hid the newsletter grid; fixed at the source.

Still open: the funder line. The SEO module still names Maine Policy Institute as the parent organization and the optional About Maine Policy Institute pattern remains available in the inserter. Both wait on the decision.

## Placeholder creators

Nine placeholder creators now fill the page for review: a first name, a handle, a town, a bio in the creator's voice and a story. They are not real people and are flagged as placeholders in WordPress. They live in one file, brand/content/creators-placeholder.json, which the splash page, the clip generator and the WordPress seed all read.

The clips are story cards, not footage. The two video connectors available to this session had no credits, and the brand's credibility rests on real faces, so no faces were generated. Each card animates the fact at the heart of the story: three apartments become one, eleven signatures tally up, a clock runs forty minutes, two bars fill, a running total climbs. The caption arrives word by word and the town signs off with the Marigold dot. They stand in until the creators film.

## Placeholder portraits and GIF clips

At the client's request the placeholder clips now show people. Nine portraits were generated through the Canva connector, one per creator and scene: a lease at a kitchen table, a coffee cart in the snow, a riverside mill walk, a dawn commute, a childhood bedroom, an empty apartment, a parked car between shifts, a nursing desk, a plow truck at dusk. They are generated faces, not real people. Each clip carries a PLACEHOLDER tag so no one mistakes one for a creator, and every record is flagged in WordPress.

Each GIF is a slow push in on the portrait with the story's caption on a flat Pine band, the town and the Marigold dot. Silent, about two seconds, under 1.2 MB each. The connector returned the portraits at thumbnail size and the full files could not be fetched from here, so the GIFs are softened to read as film rather than pixels. The full-size images are in the client's Canva account under the media ids recorded in brand/content/portraits/canva-media-ids.json; dropping them into brand/content/portraits and rerunning make_gifs.py sharpens every clip.

The stage, on the splash and in the theme, now accepts an image clip as well as a video, so a GIF or a still can stand in wherever a video is expected. The story-card clips remain in the media folder as creator-N.webm.

Phone QA of the creator panels, at 375 by 667, 390 by 844 and 430 by 932. The bio was being cut mid-sentence by a four-line clamp; the clamp is gone, every bio shows in full, and the stage gives up height on short screens so the clip, the details and the position row all fit without scrolling inside the pinned block. On the clip the handle ran into the duration badge; the header now stops short of it and trims with an ellipsis, and the GIF's PLACEHOLDER tag moved to the bottom right, clear of the header. No horizontal overflow at any size.

## Preview URL

The splash is published from the `gh-pages` branch of this repo through GitHub Pages:
https://mchljns.github.io/Generation-Maine/

The branch holds a standalone copy of brand/identity/splash/index.html plus the placeholder clips in media/. To refresh it after a change to the splash, rebuild with build_splash.py, copy index.html and media/ onto `gh-pages`, and push. Pages serves the branch directly, no workflow. The repo had to be public for this; the WordPress theme and brand files are therefore public too.

## Phone stepper, second pass

Found on the live preview on a phone-sized screen: the clip was capped at 340px tall, which on a 390 by 664 Safari viewport left a 134px wide clip, and the position row sat on the bottom edge under the toolbar. Fixes, in the splash and the theme script together:

- The clip takes the room the screen has. The block starts 16px from the top since the bar hides on the way down, the details sit tight under it (kicker, name, bio, platform marks without handles since the handle is on the clip), and the row at the bottom has a 28px tap height and clears the safe area. The clip floor is 200px, the ceiling two thirds of the screen or the column width at 9:16.
- The fit runs again once the fonts load, so the measured details height is the real one.
- The clip change is a fade of the next clip over the last one, which stays whole until it is covered. Before, both faded at once and showed through each other. Clips that are not showing are hidden outright, so a phone is not decoding nine GIFs at once.

Measured after the change: 390 by 664 gives a 181 by 322 clip, 430 by 932 gives 343 by 610.

## Bark & Sky, built as a page, October 2

The second concept had lived only as kit mockups. It is now a full splash page on the same template as Signature, so the two can be compared on the same content, the same sections and the same motion. Files: `brand/identity/splash-bark-sky/`, built by `brand/src/build_splash_barksky.py`, which passes a theme into `build_splash.page()`. Signature's output is unchanged by the refactor.

What is different, by the concept's own rules:

- Sky is the hero field and the start of the scroll scrub, Paper the page, Bark the dark fields (the sheet, in their words, the footer), Mist the light one (follow), Clay the quiet text.
- Hedvig Letters Serif for titles and names, Hedvig Letters Sans for everything else, one weight each. Titles, names, nav, buttons and kickers are lowercase. Reading text keeps its case.
- No dot anywhere. The hero period, the headline periods, the nav marker and the footer ping are gone. The active nav link is underlined instead.
- The hero is centered and airy: the sixteen-line state in Bark above the headline, the headline in the serif, the lede and two pills under it.
- Buttons are Bark pills with Paper type everywhere. The bar has no band: Bark type on Sky, then the same frosted capsule.
- The lockups follow the same size system as Signature. Two cuts were added to `logo-maine/bark-sky/`: `lockup-horizontal-solid` for the bar and `lockup-horizontal-large` for the footer, each with a reversed version.

Found and fixed in QA: the horizontal lockup is wide, and sized by height it ran past a phone screen and pushed the menu button off the edge. It is sized by width now.

Preview: https://mchljns.github.io/Generation-Maine/bark-sky/ (served from the same `gh-pages` branch, reading the same placeholder clips). Artifact: https://claude.ai/artifact/2y7Hbbnz5ro7TBPy5gJnUk

What this build does not decide: the Clay accent stays subtle by design, and the concept still has no equivalent of Marigold once per frame. Whether that quiet reads as calm or as absent is the question for the comparison.

## Bark & Sky, the brand mark and the set, October 2

The second concept's logo set was 21 files and a thin sheet. It is now the same matrix as Signature, 76 files in `brand/identity/logo-maine/bark-sky/`, built by the same script and the same size system.

- Marks: full, mid and solid cuts, each in Bark, Sky, black and white. No mono version, because the mark and the name are already one color.
- Wordmark in one line and stacked on two, lowercase Hedvig, one weight.
- Lockups: horizontal (mid cut, with large and solid versions), horizontal with the state after the name, compact, stacked left, stacked centered, two-line, endorsed (horizontal with large and solid versions) and endorsed stacked. Each in the four colors.
- Avatars at full, mid and solid, Sky on Bark, plus one in Bark on Sky. App icon, favicon, and the video bug: the solid cut and the name in Paper.

Sheets: `logo-maine/lockups-bark-sky.png` (every lockup in color on Paper and reversed on Bark, then the set at working sizes) and `apply-bark-sky/applied-sheet.png` (the eight surfaces: first seconds, lower third, end card, grid, avatar among accounts, Substack, collab post, the hero as built). The old `bark-sky.png` sheet is removed; it predated the full set and had a rendering fault.

**Grades, against the same bar as Signature.** Two-line A-. Horizontal A-. Compact B. Stacked centered A-. Stacked left B+. Endorsed B+. Avatars B+. Bug A-. Size system A-.

What the sheet says:

- The serif at one weight makes the horizontal lockup the natural primary. The state and the lowercase name sit at the same visual weight, which the Bricolage version never quite managed, so this concept does not need the two-line lockup to balance the pair.
- The compact lockup is the weak one. Inside the x-height the mid cut drops to about 14 lines of visible weight at nav size and reads as a smudge. Use the solid cut below 36 px, as the system already says, and prefer the horizontal solid in bars.
- The endorsed lockups set the institute line in Hedvig Sans at 24 units, a touch large next to the serif. It can come down to 22 if the line ever crowds the name.
- The avatar at 40 px uses the solid cut and holds. At 16 px the state is a silhouette either way.
- Nothing on the sheet carries a second color. That is the concept, and it is the thing to weigh against Signature's one Marigold per frame.

## Bark & Sky: marks the direction allows, October 2

Asked whether the second concept opens a different brand mark. It does. Signature needed weight and one bright accent, so the lined state won there. Bark & Sky is quiet, serif and one weight, which admits marks that would look thin or precious beside Bricolage. Five drawn against the lined state, in `brand/identity/marks-bark-sky/` (`candidates.png`, built by `brand/src/build_marks_barksky.py`):

| Mark | What it is | Read |
| --- | --- | --- |
| The opening quote | Hedvig's opening quotation mark alone | The strongest new idea. It says what the brand does (young people in their own words) instead of where it is, which is the platform's on-the-nose test passed outright. Holds at 16 px. Risk: quotation marks are a common device in publishing and podcast marks; it needs the serif's exact shape and the lockup to be its own |
| The gm monogram | The initials in the serif, tight | Reads as a byline or a bookplate. Calm and literary, but GM still reads as the carmaker in isolation, and at 16 px it is two grey letters |
| Ruled paper, Maine left blank | Notebook rules stopping at the state's edge | The cleverest, and the weakest in use. At avatar size the gap does not read as Maine, and the rules fight the serif in the lockup |
| The state as one line | The coast as a single hairline | Honest and quiet, and this concept can carry a stroke that thin. But a one-line outline of a state is the most common Maine mark there is, and it dies at 40 px |
| Ground and sky | A disc split at the horizon | Abstract and calm, and it answers "building a life here" without a map. Also the most anonymous: a split circle belongs to a hundred brands |

Recommendation if the client takes Bark & Sky: keep the lined state as the system mark for recognition, and test the opening quote as the avatar and the bug, where the mark stands alone and the state is already in the name. That is a two-mark system, which Signature does not need; it suits a quieter concept whose covers rely on type.

## Ground and sky, with Maine in it, October 2

The client liked the split disc and asked whether the state can be worked in. Six ways, all keeping the horizon (Sky above, ground below, a thin line of light between), in `brand/identity/marks-bark-sky/horizon/` (`candidates.png`, `brand/src/build_horizon_barksky.py`).

| Version | Read |
| --- | --- |
| Counterchange | The state centred on the line, dark on the sky, light on the ground. Clever, and at 16 px it is mud |
| Rising from the ground | The state stands on the horizon and rises into the sky, its base in the ground. Reads as a landform first and a map second, which is the point of the disc. Holds at 40, and at 16 it is still a shape on a line |
| A place on the line | A small state on the horizon. Lovely at 110, gone at 40 |
| Cut from the ground | The state cut out of the ground. The quietest; too quiet to read |
| Maine holds the horizon | No disc, the state is the field. The clearest at every size, and also the most literal: a solid Maine silhouette, which the stamp and the lined mark were both built to avoid |
| The lined state on the horizon | The shared sixteen lines counterchanged in the disc. The system mark and the horizon in one, and too busy for an avatar |

Recommendation: **Rising from the ground.** It keeps what the client liked (the horizon, the calm) and makes Maine the ground itself rather than a badge on it. Next step if it goes forward: tune where the horizon cuts the state (the coast should sit just under the line), draw the solid cut for under 36 px, and test it as the avatar and bug on the applied sheet.

## Bark & Sky, the QA pass, October 2

The strict QA in `brand/06-qa-bark-sky.md` is worked through. The page now fits a laptop fold, centers its section heads the way the kit's surfaces did, carries its own placeholder clips in its own colors, shows the wordmark alone at rest and the lockup in the capsule, sets hierarchy with the serif and size instead of weight, and keeps third-party names in their own casing. The form has an error line and a settled success state, the quotes are curly and hung, the sheet carries the platform marks, and touch and type minimums hold on phones. Those last five went into the shared template, so Signature has them too. One item stays open by choice: the hero mark's weight gradient reads top-light over the serif, and the mid cut is worth a look.

## Bark & Sky, color and mark, round two, October 2

Sheets in `brand/identity/marks-bark-sky/explore/` (`colors.png`, `rising.png`, built by `brand/src/build_explore2_barksky.py`).

**The color question.** The concept is a pale sky, a dark ground and paper between. Four pairings asked what the sky and the ground are made of, each shown as a hero, a dark surface, a paper surface and the lockup, with contrast measured.

| Pairing | What it is | Read | Grade |
| --- | --- | --- | --- |
| Bark & Sky | Sky #CFE3F0, Bark #2B211C | Cool against warm is the one contrast the concept has, and it is what keeps it from reading as a weather app. Ground on sky 11.9 to 1 | A- |
| Dawn | A peach sky #F2DCCA over Bark | Softer and more literary, and warm on warm loses the contrast. Drifts toward a bakery. Clay on sky drops to 4.8 | B- |
| Fog & Granite | A grey-blue sky over granite #2E3236 | Calm and serious, and the palette of every public-radio app. Nothing in it says warmth or a person | C+ |
| Barrens | Sky over a rust ground #46261F | The blueberry barrens after first frost. Still a brown, so still clear of the flag, and the one ground that is a Maine thing without being a picture of one. 10.2 to 1 | A- |

**The accent question.** The concept has no equivalent of Marigold once per frame. Four answers tried on a link, a button, a cover and the horizon line.

| Accent | Read | Grade |
| --- | --- | --- |
| None | Links and buttons in Bark. Nothing is ever the loud thing. Honest to the concept, and links do not announce themselves | B+ |
| Blueberry #2F4E7A | The sky's dark sibling. Links read as links without being told to, the one-in-nine cover gets a field of its own, and it stays in the family | A- |
| Lichen #8FA98B | Quiet, and too close to Signature's greens to be this concept's own | C |
| Lamp #D9A54E | Marigold by another name. It drags Signature's one idea into the quiet concept | C |

Recommendation: keep Bark & Sky as the pairing and take Blueberry as the interactive color only: links, focus, the ninth cover. Do not combine Blueberry with the Barrens ground; rust and blue together edge toward the flag the guardrails rule out. If the client wants the warmer ground, Barrens stands alone with no accent.

**The mark, pushed.** Eight variations on Rising from the ground.

| Version | Read | Grade |
| --- | --- | --- |
| As drawn (horizon 60, state 170) | Works. The ground strip is a little heavy | B+ |
| Lower horizon, larger state (66, 200) | More sky, more land, the state has room to stand. Holds at 40 | A- |
| The lined state rising | The shared sixteen lines above the horizon, the silhouette below. The system mark and the disc in one, and busy at 40 | B |
| The line runs through | The horizon is one unbroken stroke and the state stands behind it, like land seen across water. Calmer, and it fixes the coast's ragged meeting with the line | A- |
| Square tile | The same drawing for app icons and covers. Fine | B+ |
| No container | A field, not a badge. Right for the hero and the end card, not for an avatar | B+ as a surface |
| Equal halves | Calmer and the state has less sky to stand in | B |
| **Recommended: horizon at 64, state at 190, line through** | The two improvements together | **A-** |

Next, if the client agrees: draw the recommended mark into the size system (full for 72 px and up, the solid cut below 36 where the line becomes a single pixel), build the lockups and avatars in `logo-maine/bark-sky/` beside the lined state, and put it on the splash and the applied sheet so the two marks can be compared in place.

## Bark & Sky, Field notes, October 2

The brief: make the identity appeal to Gen Z, skew masculine, and keep the understatement. Three treatments on the same four surfaces in `brand/identity/marks-bark-sky/field/field.png` (`brand/src/build_field_barksky.py`).

| Treatment | What changes | Read |
| --- | --- | --- |
| A. Slate | Sky to steel #B9C9D3, Paper to bone #F4F3EE, Bark to peat #26201C. Type unchanged | Already less soft. The pastel was most of the problem |
| **B. Field notes** | Slate, plus IBM Plex Mono (OFL) for every label and number: kickers, counters, towns, timestamps, handles, nav. The serif keeps names and headlines. A grid that sits left. The horizon mark as the badge | **Chosen.** The mono reads as gear tags and camera overlays, which is where this audience lives, and the serif keeps a person in it |
| C. Utility | B, with Instrument Sans at medium in place of the serif | The most Gen Z and the most masculine, and the least this identity. A different concept wearing the horizon |

What was not used, on purpose: heavy weights, black, neon, texture, camo, anything that looks like a drop. The masculine skew comes from temperature, grid and labeling, not from force.

**Applied to the page.** `splash-bark-sky/` now carries Field notes: the steel sky and bone paper, the mono labels in uppercase with 0.06 em tracking, a left grid with the index line "nine young mainers · nine towns" above the headline and no mural in the hero, the Rising mark (horizon at 64, state at 190, line through) as the lockup in the bar and the footer, Blueberry #2B4760 as the link color, and the placeholder clips re-rendered with the peat band. Logo files: `logo-maine/bark-sky/mark-rising*`, `lockup-rising*`, `avatar-rising`, `favicon-rising`. The template gained an optional hero kicker and makes inlined logo ids unique, since two copies of one mark on a page, one hidden, were sharing a clip path.

Open: the lined state remains the shared system mark in the files. Whether Bark & Sky keeps it anywhere, or runs on the horizon alone, is the next decision. The applied sheet (`apply-bark-sky/`) still shows the earlier treatment and should be rebuilt once that is settled.

## Bark & Sky, the client's four notes, October 2

The client on Field notes: the brandmark is not it yet, the footer is out of whack, too much monospace, too much eyebrow text, and explore stock photography to fill the empty spaces, for Gen Z in Maine. And a tone note on the imagery: not too depressing.

**Done on the page.**
- The monospace is for numbers only now: the counter, the clip length, the dates. Every label is back in the sans, sentence case.
- Eyebrows cut. The hero index line is gone. The town is a line under the creator's name, not a label over it. The form's label is for screen readers only.
- The footer is the wordmark at 34 px with the two lines beside it, nothing out of scale.
- The bar and footer carry the wordmark alone until a mark is chosen.
- Photography: the hero's empty right column holds a 4 by 5 photograph, and the creators heading carries a strip of the nine portraits. Both are placeholders built from small generated thumbnails, graded cool and grained like the clip placeholders and tagged. `brand/content/photos/SHOTLIST.md` says what to license for each slot and why: young people in Maine doing things, in daylight, together. The stock-photo guardrail in `00-platform.md` is set aside at the client's request for this concept; the rule that survives is that the picture is of the thing, not of a mood.

**The mark, round three** (`marks-bark-sky/round3/candidates.png`, `brand/src/build_marks3_barksky.py`): patch, sticker, the state as a grid at three resolutions, a heavy outline, the split silhouette, and the name alone. My read: the grid at 5 by 6 is the one with a future. It is a feed, an app icon and the state in one gesture, it is abstract enough to pass the on-the-nose test, and it holds at 40 px. The patch is the safe choice. The sticker is the loudest and the most Gen Z. The name alone is honest and leaves the avatar weak.

**Imagery note.** Four generated test frames: a tailgate, a kitchen table with a lease, a main street, a lot in fog. Only the tailgate is in use. The other three were grey and solitary, which is the wrong temperature; the shot list says so. The image generator is out of credits and every photo host is blocked from this environment, so real photography comes from the client's licensing.

## Bark & Sky, a video hero, October 2

The client asked for a video hero, then specified the placeholder: a GIF that pans two seconds across each of four famous Maine settings and loops. No photography is reachable from this environment and the image generator is out of credits, so the four settings are drawn flat in the concept's palette by `brand/src/make_hero_gif.py`: Katahdin over a lake with the Knife Edge as a pale line, Cadillac Mountain's granite with the Porcupine Islands, the Old Port's brick blocks and the Custom House tower, and the Aroostook fields converging to a line of spruce. No lighthouse, per the guardrails. 96 frames at 12 a second, 640 by 800, about 1 MB, tagged PLACEHOLDER. It sits in the hero's media slot in place of the photograph, with the photograph kept as the slot's background while the GIF loads, and it is hidden under reduced motion.

The template now lets a theme replace the hero media outright, and the mural script tolerates a hero without the mural.

Real footage: four two-second pans of the real places, or better, of the creators in them, cut to the same 4 by 5 and dropped in as `media/hero.gif` or as a muted MP4 in the same slot. A first draft of the video route (`make_hero_video.mjs`, a Playwright-recorded montage of the clip placeholders) is in the repo for when footage exists.

## Bark & Sky, the hero becomes the video, October 2

The client opened the environment to Wikimedia Commons, asked for the video to span the whole hero with legible type over it, and added Portland Head Light as a fifth setting, with a note that the sources must hold up at full width.

What changed:

- `brand/src/fetch_commons.py` searches Commons by subject, keeps only CC BY, CC BY-SA, CC0 and public domain files, and now rejects anything under 3000 px wide. The five sources used are 3840 px wide as fetched (the Commons 3840 rendition, or the original where it was smaller than that), and the candidate set is listed in `brand/content/photos/commons/candidates.json`. Unused candidates stay out of the repo.
- `brand/src/make_hero_real.py` grades each source lightly toward Sky (color down to 84 percent, 6 percent Sky blend), cuts a 2150 by 1210 plate per setting, writes the poster and `CREDITS.md`, and `make_hero_video.mjs` records the loop in Chromium: five settings, two seconds each, a slow drift with a two percent push in, alternating direction, 1920 by 1080, muted WebM of about 3 MB. Order: Katahdin from Abol Bridge, the Aroostook potato fields (Jack Delano, 1940), sunrise from Cadillac Mountain, Portland Head Light, the Old Port waterfront.
- The hero is now the video edge to edge, 100svh tall at most. The bar sits over it in Paper with the Sky wordmark, then takes the capsule on scroll as before. The type is Paper on a Bark scrim that is heaviest at the left and along the bottom. Measured against the brightest three percent of each frame under the scrim, the headline's worst case is 5.0:1 (Aroostook) and the lede's 8.0:1, so every frame clears AA for both. Reduced motion shows the poster alone.
- A small credit sits in the hero's corner and the full credit line, with licenses, is in the footer. CC BY-SA requires that line wherever the loop appears.

The lighthouse: this direction's guardrails said no lighthouses, as a cliché. The client asked for Portland Head Light by name, so it is in as a client-directed exception and recorded here. The frame chosen keeps it small in a wide sea and rock view rather than a postcard.

Still a placeholder in one sense: these are landscapes, not the creators. The slot is ready for real footage of young Mainers in these places, cut to the same 16 by 9 and dropped in as `media/hero.webm`. An MP4 rendition for older Safari needs ffmpeg, which this environment does not have; convert before launch. [CONFIRM: hosting can serve a 3 MB video on the first paint, or move it behind a lazy load]

### The loop, second cut

The client asked for more cinematic pans. Changes in `make_hero_video.mjs` and `make_hero_real.py`:

- Each setting holds 2.6 seconds and dissolves into the next over 0.9 of them, so nothing cuts; the loop runs 13 seconds.
- The moves are near constant speed, with only the gentlest ease, and each pairs a drift with a push in or a pull out: push toward Katahdin's summit, pull out over the Aroostook fields, push toward the islands from Cadillac, pull out from the Head Light to the sea, drift along the Old Port waterfront. Plates are 22 percent larger than the frame to give the moves room.
- The grade is filmic: color at 80 percent, a soft S curve with the blacks lifted to 6 percent and the highlights held under 96, a touch of Sky in the shadows, a light vignette.
- The file is now drawn on a canvas and encoded in the browser, which gives an exact start and end on the first setting at rest, so the loop point is seamless and the poster is the true first frame. The encoder omits the duration, so the script writes it into the WebM header.

## Bark & Sky, photographs through the page, October 2

The client asked where else imagery could lift the splash page. The judgment, section by section:

- **About.** The left column held only the heading and a void below it. Now a 3 by 2 photograph of Belfast's brick downtown and harbor from above sits under the heading, with a one line caption. It answers "where" while the three columns answer who, what and how.
- **Between the creators and their words.** A full-bleed band, Lewiston's mills and downtown from above. A breath after the long stepper, in the hero's language, before the dark quotes section. It first carried a line of copy; the client asked for the photograph alone, so the only type on it is the credit.
- **In their words.** Each quote's footer carries a small still of the creator beside the name, so the words have a face. Forty by fifty two pixels, the same 3 by 4 as the strip.
- **The newsletter.** Each post gets a 3 by 2 thumbnail of its town (Belfast, Machias, Lewiston). A list of three titles reads as a publication once it has pictures.
- **Left alone.** The hero already carries the loop. The follow row is icons and handles and needs nothing. The form needs nothing. The footer is the credits.

All of it is template hooks (`about_media`, `band`, `post_thumbs`, `quote_stills`) that default to nothing, so the Signature page is unchanged. Sources are Commons, 2000 px or wider, graded like the hero by `brand/src/make_photos_page.py`, credited in the footer line and in `CREDITS.md`. Skowhegan and Sanford street photographs were not usable (rate limited, or carrying a flag); the posts use the three towns with good pictures.

## Bark & Sky, the mark is decided: the cairn, October 2

After four rounds of marks, a typographic detour (quotation mark, me, 207) and a research pass on real cairns from Wikimedia Commons, the client chose a cairn: flat stones of different sizes and shapes with one rounded stone on top. The build is "wedges ii": a long base thick at one end, a shorter wedge thick at the other and set left, a slightly wider flat, a block with a dip, and the round stone sitting in the dip. Every stone is a different shape. The stack is physically possible: each stone rests on the one below and its center of mass sits over the bearing surface under it, which `build_cairn6.py` checks numerically. Shadow hairlines of the background color separate the stones so they never fuse into a mound, which is where the emoji read came from.

The meaning: the flats were laid by the people before you; the round stone, in Sky, is the one this generation sets. The way is marked, and you mark it for the next.

Weighed and recorded: cairns carry a burial reading and the outdoors community objects to visitor-built stacks. The client heard both and chose it anyway. The drawing leans on the realism of the Commons references and away from the three smooth pebbles of spa imagery.

The system (`build_system_cairn.py`, 40 files in `brand/identity/logo-maine/bark-sky-cairn`): mark, horizontal, horizontal large, two line, stacked left, stacked centered, endorsed, compact; each in Bark on Paper with the round stone in Sky, Sky on Bark with the round stone in Paper, black and white. Avatar in three fields, app icon, a favicon that drops the shadow lines so it stays solid at 16 px, and the bug. The funder line in the endorsed lockup is still [CONFIRM].

Still to do: put the compact lockup in the splash bar and footer, regenerate the clip end card and the applied sheet, and retire the earlier mark candidates from the lockup sheet.
