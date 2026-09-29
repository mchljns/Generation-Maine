# Generation Maine identity v2

Open `identity-v2.html` in a browser. It is one self-contained file with animated brandmarks, lockups, color, type and applications for both directions. `identity-v2-preview.png` is a full-page screenshot.

Version 1 is saved unchanged in `brand/archive/v1/`. The website theme still uses v1 until a v2 direction is chosen.

## What the brandmark is

**v1 did not really have one.** It was the name set in Bricolage Grotesque, with the dot on the i swapped for an orange circle, plus a bold G with a dot for the avatar. That is a treatment of a typeface, not a mark with an idea in it.

**v2 gives each direction a real brandmark:**

- **First Light (A, recommended):** the outline of Maine cut out of an orange disc. The disc is the rising sun and the red light a camera shows while recording. The cutout is transparent and holds together as one shape down to 16 px. It animates: the disc appears, Maine rises into it, then it blinks like a record light. Two alternates are kept for reference: the earlier G-sunrise and "Sunrise State" (the silhouette with the sun rising off Lubec).
- **Postmark (B):** a round postmark with GENERATION MAINE and YOUNG MAINERS on the ring and the outline of Maine in the center. Cancellation lines run off to the right. Each creator gets their own postmark with a dot on their town. At small sizes it switches to "ME", the postal code for Maine and the first-person voice of every creator.

The Maine outline comes from Natural Earth 1:10m map data, which is public domain. It is simplified to 94 points (`brand/src/maine.py`, data in `brand/src/data/maine.json`).

## What makes v2 more premium

1. **A mark with meaning.** A symbol that tells a story in one look is the biggest single upgrade over styled type.
2. **Disciplined type, no italics.** First Light uses Instrument Sans for everything and gets emphasis from color. Postmark pairs Anton with IBM Plex Mono. Italics are not used anywhere in either direction.
3. **Fewer, stronger devices, used the same way every time.** First Light has the horizon rule, a thin line with the sun sitting on it. Postmark has the stamp, yellow label tape and perforated photo edges. Consistency is what reads as premium.
4. **Restraint with color.** First Light adds Pine, a near-black green, for video and dark sections, and keeps Signal orange to about 3 percent of any layout.
5. **Motion.** Both marks have a short animation that can open or close every video.
6. **A system for the creators.** Postmark's town stamps give every creator their own branded asset without a designer.

## Files

| Path | Contents |
| --- | --- |
| `first-light/logo/` | Symbol, horizontal and stacked lockups (color, reversed, black, white) and app icon. SVG plus 1024 px PNG |
| `first-light/social/` | Avatar, 9:16 end card, YouTube thumbnail, lower third, share card, YouTube banner. SVG and PNG |
| `postmark/logo/` | Postmark, lockup with cancel lines, small version, app icon and four sample creator stamps |
| `postmark/social/` | The same six applications |
| `fonts-web/` | Web subsets used by the presentation |
| `../fonts/v2/` | Desktop fonts for Canva and design tools, with OFL license files |
| `first-light/logo/alt-*.svg` | Alternates: G-sunrise and Sunrise State |

All fonts are under the SIL Open Font License. Every logo is hand-built SVG geometry and outlined type. No AI image generation was used.

## Rebuild

```bash
python3 brand/src/build_v2.py
node brand/src/render_v2.mjs
```

## To confirm

- The "first place in the country to see the sunrise" line is common knowledge about Maine (Cadillac Mountain, part of the year) but should be checked before it is used in public copy. The brandmark does not depend on it.
- The towns on the sample creator stamps are examples only.

## Next step

Pick a direction. I will then apply it to the WordPress theme, rebuild the brand guide and social kit around it, and run the full QA again.
