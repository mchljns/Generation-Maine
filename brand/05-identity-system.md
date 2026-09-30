# Identity system: where things stand

Saved September 30, 2026. Everything below is built as hand-drawn SVG geometry by scripts in `brand/src/`, so it can be redrawn at any size and animated by the same rules that draw it.

## Decisions so far

| Element | Decision | Why |
| --- | --- | --- |
| Brandmark | **Bend, flat.** A field of horizontal lines that make room. Where a line bends it turns Marigold. The room stays empty | One sentence, no picture: the field makes room for the person. Holds at 16 px with six lines. Gold belongs to the lines, not a dot placed on them |
| Mural | **Grain.** Maine drawn in horizontal lines from the precise Census outline, weight growing toward the bottom, the widest line gold | The strongest single image of the project. Lives at sizes where Maine reads: the website hero and the end card |
| Relationship | The mark is a crop of the mural where one line is missing. One rule, two scales | Everything seen large is Maine. Everything seen small is the mark |
| Marigold | Once per frame. In the mark, the bends. In the mural, the widest line. In the wordmark, the dot on the i, but only when the wordmark stands alone | Keeps the rule the platform set and stops gold from spreading |
| Letter marks | Set aside | The G is the generic half of the name. GM reads as General Motors |
| Maine as the brandmark | Set aside | The silhouette needs about 110 px to read. At 32 and 16 px it is a stack of dashes. The outline is also the most used device in Maine branding |
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
