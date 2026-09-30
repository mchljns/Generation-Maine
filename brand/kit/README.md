# Generation Maine brand kit, round one

Built from `brand/00-platform.md`. Open `kit.html` in a browser to see everything in place.

Recommended direction: **Signature** (mockups starting with `q-`). Routes A (`a-`) and B (`b-`) are kept as the record of what was tested.

Sample lines and sample towns in the mockups are for layout only. Real lines and towns come from the creators.

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

## Signature rules

1. One idea per frame.
2. Big, tight type anchored low left.
3. Full color fields in a fixed order: Spruce, Birch, Pine, with Marigold once in a set of nine.
4. Marigold once per frame, usually as the dot that ends a headline.
5. Creator name and town as plain text, no box or device.

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

Rebuild: `python3 brand/src/build_kit.py && node brand/src/render_kit.mjs`
