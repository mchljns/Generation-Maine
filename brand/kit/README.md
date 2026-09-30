# Generation Maine brand kit

Built from `brand/00-platform.md`. Open `kit.html` in a browser to see everything in place.

Recommended direction: **Signature, round two** (mockups starting with `s-`). Round one of Signature (`q-`) is kept as the before. The pressure test that led to round two is in `brand/03-pressure-test.md`, and the before and after sheet is `signature-before-after.png`. Routes A (`a-`) and B (`b-`) are kept as the record of what was tested.

Sample lines and sample towns in the mockups are for layout only. Real lines and towns come from the creators.

## Concept C: Offset (in progress)

Mockups start with `o-`. Contact sheet: `offset-sheet.png`. Every frame breaks at two thirds of its height. Above the line sits footage or a field in the order Spruce, Moss, Pine, with Marigold every ninth post. Below it sits a Birch band with the creator's name and town. In a profile grid the bands line up into one stripe. It keeps the master brand and every Signature type rule.

## Master brand (both routes)

| File | Use |
| --- | --- |
| `assets/logo/wordmark*.svg/.png` | Website header, Substack header, end cards. Spruce, reversed (Birch), black, white |
| `assets/logo/stacked*.svg/.png` | Square spaces |
| `assets/logo/endorsed*.svg/.png` | Wordmark with "An initiative of Maine Policy Institute" |
| `assets/logo/icon*.svg/.png` | G and dot. Spruce, light and Marigold versions |
| `assets/social/avatar-1080.png` | Profile picture on every channel |
| `assets/social/favicon-*.png` | 16, 32, 180 and 512 px |
| `assets/video/ov-bug.png` | Transparent 1080 x 1920 overlay. Top left of the first seconds of every video |

## Signature rules, round two

1. One idea per frame. A cover carries one headline of four words or fewer and one credit line.
2. Big, tight type anchored low left. Bricolage ExtraBold, line height 0.9, tracking minus 3 percent, three lines at most. Margin is one fifteenth of the frame width (72 px at 1080).
3. Fields in a fixed order: Spruce, Birch, Pine, then again. Every ninth post, Marigold takes Pine's place.
4. Marigold once per frame, outside the wordmark: the headline dot or the field. On a Marigold field the dot turns Pine.
5. Name and town are one plain line: name in Inter SemiBold, town in Inter Regular, sentence case. In video it sits 30 percent up from the bottom.

| File | Use |
| --- | --- |
| `assets/video/ov-s-bug.png` | Round two bug: the wordmark, transparent, top left |
| `assets/video/ov-s-lower.png` | Round two name and town, transparent |

## Route overlays (tested, not recommended)

| File | Use |
| --- | --- |
| `assets/video/ov-a-lower.png` | Route A lower third, transparent. Replace the bracketed text in your editor |
| `assets/video/ov-b-lower.png` | Route B lower third, transparent |

## Mockups

`mockups/` holds every mockup at full size: a video's first seconds, the lower third, the end card, the profile grid, the Substack email, the website hero, the collab post and the avatar test. Files starting with `a-` are Route A. Files starting with `b-` are Route B.

## Rules that apply to both routes

- The bug is the only brand mark inside a creator's video. Keep it in the top left, clear of the app's buttons.
- The creator's name and town appear on every video.
- "An initiative of Maine Policy Institute" appears on every end card, bio and page footer.
- Marigold is never text on light backgrounds. It is only a dot, a button or large type on Spruce.
- No italics, no em dashes, no invented facts.

Rebuild: `python3 brand/src/build_kit.py && node brand/src/render_kit.mjs && python3 brand/src/sheet_kit.py`
