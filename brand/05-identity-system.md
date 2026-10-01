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
