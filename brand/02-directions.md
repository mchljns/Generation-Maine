# Generation Maine: Two creative directions

Open `brand/directions.html` in a browser to see both directions side by side. It is a single file with the fonts embedded. It shows each logo as a round social avatar, a 9:16 video end card and the website hero.

Contrast ratios below were calculated with the WCAG 2.1 relative luminance formula (`brand/src/build_directions.py` prints them).

---

## Direction A: Spruce & Signal (recommended)

**Concept.** Maine's working landscape, drawn as clean contour lines like a trail map, with one bright orange dot that reads as a camera's record light. It feels local and current without a single postcard cliché.

**Moodboard (words).** Trail map contour lines. Spruce woods at dusk. The orange of a hunter's cap, a buoy line or a trail blaze. Fog over a harbor town at 7 a.m. Phone footage shot in a kitchen, a garage workshop or a first apartment. Clean sans-serif type on a flat green field.

**Logo approach.** A wordmark plus a small symbol. The full wordmark matters because the project is new and people need to learn the name. The dot on the i in "Maine" is replaced with an orange circle that works as a record light. The same dot sits beside a bold G to make the icon for avatars and favicons, where the full name would be too small to read.

**Type pairing.**

| Role | Font | License |
| --- | --- | --- |
| Display, logo, headlines | Bricolage Grotesque ExtraBold (opsz 96, width 92) | SIL Open Font License 1.1 |
| Body, captions, buttons | Inter (400 to 700) | SIL Open Font License 1.1 |

**Palette.**

| Name | Hex | Use |
| --- | --- | --- |
| Spruce | #0E3B2E | Main brand color, dark backgrounds |
| Fog | #EEF2EC | Light backgrounds, text on Spruce |
| Signal | #FF5B24 | The dot, buttons, small highlights |
| Moss | #2F6B4F | Contour lines, eyebrow text on white |
| Lichen | #C7DB6E | Accent text on Spruce |
| Ink | #0A1A14 | Body text, text on Signal |
| Signal Deep | #C43D0E | Orange links and small text on light backgrounds |

**Contrast (calculated).**

| Text on background | Ratio | Result |
| --- | --- | --- |
| Ink on Fog | 15.84:1 | Passes AA |
| Spruce on Fog | 11.02:1 | Passes AA |
| Fog on Spruce | 11.02:1 | Passes AA |
| Lichen on Spruce | 8.19:1 | Passes AA |
| Ink on Signal | 5.79:1 | Passes AA (button text) |
| Signal Deep on Fog | 4.61:1 | Passes AA |
| Signal on Spruce | 4.02:1 | Large text only (3:1) |
| Signal on Fog | 2.74:1 | Fails. Use for shapes only, never text |

**Risk.** Green and orange is a friendly outdoors pairing. Without discipline it could drift toward an outfitter or state park look. The contour lines and the record dot have to show up consistently to keep it tied to storytelling.

---

## Direction B: Paper Route (alternate)

**Concept.** A photocopied zine made by kids in a small town, with condensed headlines, typewriter captions and a highlighter swipe. It feels handmade and a little loud, as if the creators made it themselves.

**Moodboard (words).** Photocopied flyers on a coffee shop corkboard. Highlighter on newsprint. Label maker tape. Wild blueberry blue. Handwritten notes in the margins of a lease. Black and white photos with one bright color on top.

**Logo approach.** A stacked wordmark in condensed capitals with a highlighter swipe behind "MAINE". The avatar is a "GM" sticker set at a slight angle. It relies on type and one gesture, so a small team can copy it in Canva.

**Type pairing.**

| Role | Font | License |
| --- | --- | --- |
| Display, logo, headlines | Archivo Condensed Black (width 62, weight 900) | SIL Open Font License 1.1 |
| Body and captions | IBM Plex Mono Medium | SIL Open Font License 1.1 |

**Palette.**

| Name | Hex | Use |
| --- | --- | --- |
| Ink | #141414 | Text, logo |
| Newsprint | #ECECE6 | Background |
| Blueberry | #3D2FD1 | Brand color, links, dark sections |
| Highlighter | #E6F03F | Swipes, buttons behind dark text |

**Contrast (calculated).**

| Text on background | Ratio | Result |
| --- | --- | --- |
| Ink on Newsprint | 15.53:1 | Passes AA |
| Blueberry on Newsprint | 7.01:1 | Passes AA |
| White on Blueberry | 8.31:1 | Passes AA |
| Ink on Highlighter | 14.83:1 | Passes AA |
| Blueberry on Highlighter | 6.69:1 | Passes AA |
| Highlighter on Newsprint | 1.05:1 | Fails. Decoration only |

**Risk.** Zine styling is common in youth media and may look dated in two years. Next to a policy institute's name it can also read as a costume, which feeds the exact criticism the brand needs to avoid. Monospace body text is harder to read in long passages.

---

## The pick: Direction A

I built everything on Spruce & Signal for four reasons.

1. **It works at avatar size.** The G and the orange dot stay clear at 32 px. Direction B's angled sticker loses its highlighter edge at small sizes.
2. **It supports the credibility stance.** Direction A looks calm and confident, so the creators' faces can lead. Direction B's handmade style could look like an adult organization imitating youth culture.
3. **It is clearly different from 76crew.com.** There is no navy, no brick red and no stars. The only warm color is one orange dot.
4. **It is easy for a small team.** One dark color, one light color and one orange dot cover most social posts. The contour pattern is a ready-made PNG.

**Switching later.** Direction B is packaged as a WordPress style variation. In the Site Editor, open Styles, browse styles and choose "Paper Route (alternate direction)". Colors, fonts, heading style and button shape all change with one click. The same tokens live in `brand/alt-direction.json`. The logo files and social kit would still need to be rebuilt in Direction B (the website wordmark keeps Direction A's letterforms until then).
