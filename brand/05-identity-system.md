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
