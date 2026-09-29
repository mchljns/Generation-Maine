# Generation Maine WordPress theme

A one-page block theme for GenerationMaine.org, an initiative of Maine Policy Institute. It has no page builder, no build step and needs no plugins.

## What is in the theme

| Path | What it does |
| --- | --- |
| `theme.json` | Colors, fonts, type scale, spacing and button styles (brand: Spruce & Signal) |
| `styles/paper-route.json` | The alternate brand direction as a one-click style variation |
| `style.css` | Theme header plus the few styles theme.json cannot express (sticky header, contour pattern, creator cards) |
| `functions.php` | Loads the stylesheet, preloads the headline font, adds a favicon fallback |
| `inc/creators.php` | Private "Creators" post type, its fields and the `[gm_creators]` shortcode |
| `blocks/creators/` | The server-rendered Creators Grid block (plain JS, no build) |
| `inc/seo.php` | Title, description, canonical, Open Graph and Organization schema with Maine Policy Institute as parent. Turns itself off if Yoast, Rank Math, SEOPress or AIOSEO is active |
| `patterns/` | The page sections: header, hero, about, creators, follow, mpi, footer |
| `templates/` | `front-page.html` (the splash page), `index.html`, `404.html` |
| `assets/fonts/` | Self-hosted Bricolage Grotesque and Inter (plus the alternate direction's fonts), with OFL license files |
| `assets/img/` | Wordmark, icon, favicon, contour pattern and share card |
| `bin/` | Seed script for placeholder creators (not needed on the live site) |

## Install

1. Download `dist/generation-maine.zip` from the repo.
2. In WordPress, go to **Appearance > Themes > Add New > Upload Theme** and upload the zip.
3. Activate **Generation Maine**.
4. Go to **Settings > Reading** and leave "Your homepage displays" on "Your latest posts". The theme's front page template shows the splash page either way.
5. Go to **Settings > Permalinks** and choose "Post name".
6. Optional: set a Site Icon in **Settings > General**. Until you do, the theme uses its own favicon.

Requires WordPress 6.5 or newer and PHP 7.4 or newer. Tested on WordPress 6.8.3 with PHP 8.3.

## Edit the page

Open **Appearance > Editor > Templates > Front Page**. Every section is made of normal blocks.

- **Text:** click any heading or paragraph and type.
- **Channel links:** the Instagram, TikTok, YouTube and Substack buttons point to `#follow` until the real URLs exist. Click each button and paste the link.
- **Hero photo:** select the hero (a Cover block), then use **Add Media** in the toolbar. With no photo, the hero shows the contour pattern on Spruce green. With a photo, the pattern hides and the overlay keeps text readable (raise the overlay opacity if a photo is busy).
- **Press email and Maine Policy sentence:** in the "About Maine Policy Institute" section, replace the `[CONFIRM: ...]` text.
- **Header and footer:** edit under **Patterns > Template Parts**. The logo is inline SVG in a Custom HTML block.
- **SEO text:** change the title and description in `inc/seo.php`, or install an SEO plugin and the theme steps aside.

## Add creators

1. In the dashboard, click **Creators > Add creator**.
2. **Title** is the creator's name.
3. The text area is their bio. Two or three sentences work best.
4. **Portrait** (right sidebar) is their photo. Use a 4:5 photo at least 1000 × 1250 px.
5. **Creator details** (below the editor) holds hometown and links.
6. **Page Attributes > Order** sets the order on the page (lower numbers first).
7. Publish. The creator appears in the grid right away.

Creators have no public pages of their own. With no creators published, the grid shows a "Creators coming soon" card. If a creator is marked "This is a placeholder", the card shows a Placeholder label.

To test with fake creators: `wp eval-file wp-content/themes/generation-maine/bin/seed-creators.php 12`. Run it with `0` to remove them.

## Switch to the alternate brand direction

The theme ships with the recommended direction, **Spruce & Signal**. The alternate, **Paper Route**, is a style variation.

1. Go to **Appearance > Editor > Styles**.
2. Click **Browse styles** and pick **Paper Route (alternate direction)**.
3. Save.

That swaps colors, fonts, heading style and button shape. To switch back, pick the default style. The wordmark keeps Direction A's letterforms (it picks up the new colors). If the client chooses Paper Route, the logo files and social kit in `brand/` should be rebuilt for it.

## Local development

- **WordPress Playground:** from the repo root, run `npx @wp-playground/cli@latest server --mount=./generation-maine:/wordpress/wp-content/themes/generation-maine --login`, then activate the theme. `qa/mu-plugins/gm-qa.php` can be mounted too; it activates the theme, sets permalinks and seeds creators at `/?gm_seed=12`.
- **wp-env:** `cd generation-maine && npx @wordpress/env start`.

## Performance and accessibility notes

- Fonts are self-hosted WOFF2 subsets (about 70 KB total for the default direction) and the headline font is preloaded.
- No JavaScript loads on the front end except WordPress's own.
- Colors in the default palette meet WCAG AA for their intended pairings. See `brand/02-directions.md` for the ratios.
