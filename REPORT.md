# Generation Maine: Work report

## What I built

- A brand strategy with positioning, promise, personality, a look at other outlets and a credibility stance (`brand/01-strategy.md`).
- Two creative directions, shown side by side with avatar, end card and hero mockups (`brand/directions.html`, `brand/02-directions.md`).
- A full logo suite for the chosen direction as outlined SVG, with PNGs and a favicon set (`brand/logo/`).
- A social starter kit with editable SVGs, finished PNGs and blank backgrounds for Canva and CapCut (`brand/social/`).
- A 12-page brand guide in HTML and PDF (`brand/brand-guide.html`, `brand/brand-guide.pdf`).
- The WordPress block theme, built from scratch with the brand applied, plus an installable zip (`generation-maine/`, `dist/generation-maine.zip`).
- The page copy with three headline options (`copy/page-copy.md`).
- QA in WordPress Playground: screenshots, axe, Lighthouse and block validation (`qa/`).

## Chosen direction

**Spruce & Signal.** Spruce green and a pale fog background, with one orange dot. The dot sits on the i in "Maine" and reads as a camera's record light. A contour-line pattern, like a trail map, fills empty space.

I picked it because it stays clear as a 32 px avatar, looks calm enough to let the creators lead, and shares nothing with 76crew.com's navy, red and stars. It is also simple for a small team to repeat in Canva. The full reasoning is in `brand/02-directions.md`.

**To switch to Paper Route:** in WordPress, go to Appearance > Editor > Styles > Browse styles and pick "Paper Route (alternate direction)". The tokens are also in `brand/alt-direction.json`. A preview of the site in that style is in `qa/screenshots/alt-direction-paper-route-1440.png`. The logo files and social kit would need to be rebuilt for Paper Route.

## Assumptions

- **The repo was empty.** The prompt described an existing `generation-maine/` theme with `README.md`, `PROJECT.md`, `inc/creators.php`, patterns and an SEO file. The GitHub repo had no commits at all. I built the whole theme from scratch to match that description: a private Creators post type, the `[gm_creators]` shortcode, a server-rendered Creators Grid block, five section patterns and `inc/seo.php`. There was no newer "public profiles" version to revert.
- **Branch name.** This session is set up to push only to `claude/generation-maine-setup-6s8g2r`, so the work is on that branch instead of `brand-and-splash`. The repo had no default branch, so I created `main` with one empty commit to give the pull request a base.
- **Maine Policy Institute URL.** I used `https://mainepolicy.org/`. It needs confirmation.
- **Channel buttons** link to `#follow` until real URLs exist.
- **Footer copyright** reads "© 2026 Generation Maine." The client may want Maine Policy Institute as the holder.
- **Topic list** in the "What the videos cover" card uses the five topics named in the RFP.
- **Creator card fields** are name, portrait, hometown, bio and up to four links (Instagram, TikTok, YouTube, website).
- **Descriptions of other outlets** in the strategy doc come from general knowledge and are marked "to verify."
- **Sample video headlines** in the brand guide are labeled as style samples, not real videos.
- **Tooling.** wordpress.org is blocked on this machine's network, so Playground ran WordPress 6.8.3 cloned from the official WordPress GitHub mirror. Blueprints were also blocked, so a small QA plugin (`qa/mu-plugins/gm-qa.php`) activated the theme, set pretty permalinks and seeded creators.
- **Your mid-session link list** (Motion, React Spring, KokonutUI and similar). Most of those are React animation libraries. They would add a build step and front-end JavaScript to a theme the brief says must be fast with no build step, so I did not use them. The contour backgrounds are generated SVG, similar in spirit to Haikei.

## Blocked or unfinished

- Nothing in scope is blocked.
- Real content is missing: channel handles, the Substack URL, the Maine Policy description, the press email, creator profiles and photos. All are marked `[CONFIRM]` or shown as placeholders.
- Canva font availability for Bricolage Grotesque is unverified. The guide gives a fallback.

## QA results

**PHP:** `php -l` is clean on every PHP file. Across every page load in both creator states there were zero fatals, warnings, notices or deprecations. The QA plugin logged every PHP error to a file, and the file stayed empty.

**Block validation:** all 7 patterns, 3 templates and 2 template parts parse as valid blocks in the WordPress 6.8 editor (`qa/check-blocks.mjs`).

**theme.json:** `theme.json` and `styles/paper-route.json` both validate against the WordPress 6.8 theme.json schema.

**axe-core** (WCAG 2.0/2.1 A and AA plus best practices, at 1440 px and 375 px): 0 violations in both creator states.

**Lighthouse mobile** (Playground, 12 creators; Playground is slower than real hosting):

| Run | Performance | Accessibility | Best practices | SEO |
| --- | --- | --- | --- | --- |
| 1 | 98 | 100 | 100 | 100 |
| 2 | 97 | 100 | 100 | 92 |
| 3 | 98 | 100 | 100 | 100 |

The SEO dip in run 2 was a failed robots.txt download from Playground. The file returned 200 in every direct check and in runs 1 and 3. Run 3 metrics: FCP 1.7 s, LCP 2.1 s, TBT 0 ms, CLS 0.015. The only remaining suggestions are server-level (text compression, response time), which normal hosting handles. Reports: `qa/lighthouse-mobile-run1-3.report.html` and `.json`.

**Layout checks:** no horizontal scroll and no overflowing elements at 375, 768 or 1440 px in either state. No broken images and no console errors.

**Attribution:** "An initiative of Maine Policy Institute" appears in the hero above the headline, in its own section and in the footer. The words "Maine Policy Institute" appear 5 times on the page.

**Writing rules:** no em dashes and none of the banned words anywhere in the repo or on the rendered page. (Lighthouse's own report CSS contained one escaped em dash glyph, which I replaced.)

**Word count:** about 235 visible words, under the 300-word limit.

**Screenshots** (`qa/screenshots/`):
- `0-creators-375.png`, `0-creators-768.png`, `0-creators-1440.png`
- `12-creators-375.png`, `12-creators-768.png`, `12-creators-1440.png`
- `alt-direction-paper-route-1440.png`
- `brand-guide-preview.png`

After reviewing the screenshots I fixed:
- Hero text that didn't line up with the header.
- A floating headline dot.
- A thin gap above the footer.
- A sticky header that didn't stick.
- Creator cards that made the 375 px page 11,000 px tall. They now use a compact row layout on phones, which halved the page.

## Placeholders to send to the client

Website and copy:
1. `[CONFIRM: one sentence about Maine Policy Institute]` (About Maine Policy Institute section)
2. `[CONFIRM: press email]` (same section; the link currently points to press@example.org)
3. `[CONFIRM: Maine Policy Institute URL]` (currently https://mainepolicy.org/, used in the section button, footer and schema)
4. `[CONFIRM: channel URLs and handles]` for Instagram, TikTok and YouTube (Follow buttons)
5. `[CONFIRM: Substack URL]` (Substack button)

Social kit:
6. `[@handle]` on the end card and YouTube banner
7. `[name].substack.com` on the end card

## Questions for the client

1. Which direction do you prefer: Spruce & Signal or Paper Route?
2. What are the channel handles, and are Instagram, TikTok and YouTube the right three?
3. What is the Substack URL?
4. Can you send one sentence describing Maine Policy Institute, and a press contact email?
5. Should the footer copyright name Generation Maine or Maine Policy Institute?
6. Will creators be allowed to link their personal accounts from their cards?
7. Is there a way for young Mainers to apply or express interest that the page should link to?
