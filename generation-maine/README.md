# Generation Maine WordPress theme

A one-page block theme for GenerationMaine.org. Every piece of copy on the page is a block the editor can change. Everything about a creator lives on a Creator post. There is no page builder, no build step and no plugin to install.

## What is in the theme

| Path | What it does |
| --- | --- |
| `theme.json` | The palette (Spruce, Pine, Moss, Marigold, Sage, Sand, white, ink), the two fonts, the type scale and the pill buttons |
| `style.css` | The page's stylesheet. Generated from `brand/src/build_theme.py`, which shares its CSS with the splash mockup |
| `assets/js/site.js` | The page's motion: the mural, the pulsing period, the color fade on scroll, the capsule bar, the creators stepper, the reveals |
| `assets/data/mural.json` | The sixteen lines of the hero mural, generated from the state outline |
| `functions.php` | Loads the stylesheet and script, preloads the headline font, a favicon fallback |
| `inc/creators.php` | The Creators post type, its fields, and the stepper that renders them |
| `inc/newsletter.php` | Settings > Newsletter, the signup form that hands off to Substack, and the latest-posts feed reader |
| `inc/marks.php` | The hand-drawn platform marks and placeholder avatar (generated) |
| `inc/seo.php` | Title, description, canonical, Open Graph and Organization schema. Steps aside if an SEO plugin is active |
| `blocks/creators/` | The Creators block |
| `blocks/newsletter/` | The Newsletter Signup block |
| `blocks/posts/` | The Latest Newsletter Posts block |
| `patterns/` | The page sections as block patterns: header, hero, about, creators, words, newsletter, follow, footer |
| `templates/front-page.html` | The page, assembled from the patterns |
| `assets/fonts/` | Bricolage Grotesque and DM Sans, self-hosted, with their OFL licenses |
| `assets/img/` | The logo files and icons |
| `bin/` | A seed script for placeholder creators (not needed on the live site) |

Requires WordPress 6.5 or newer and PHP 7.4 or newer.

## Install

1. Upload the theme zip under **Appearance > Themes > Add New > Upload Theme** and activate it.
2. Under **Settings > Reading** leave "Your homepage displays" on "Your latest posts". The theme's front page template shows the page either way.
3. Under **Settings > Permalinks** choose "Post name".
4. Under **Settings > Newsletter** paste the publication's subscribe page address. Until you do, the signup form stays hidden and the posts list shows placeholders.
5. Optional: set a Site Icon under **Settings > General**.

## Edit the copy

Open **Appearance > Editor > Templates > Front Page**. Every section is made of normal blocks.

- **Headlines and paragraphs:** click and type. The Marigold period at the end of each section heading is added by the page, so it survives any rewrite. Keep headlines under about ten words.
- **The bar:** the four link labels and the button text are in the Header template part. The links point at the sections by their anchors, which do not change.
- **The hero:** headline, lede, one button and one text link.
- **About:** a heading and three columns, each a small heading and a paragraph.
- **In their words:** three Quote blocks. The words go in the quote, the name and town in the citation.
- **Newsletter:** heading and lede are blocks; the form and the posts list come from Settings > Newsletter.
- **Follow:** four platforms, each a small heading and a link. Paste the real address on each link.
- **Footer:** a line about the project and the legal line.

Colors, type, the pill shape and the motion are not editable in the page. That is on purpose. They live in `theme.json` and the stylesheet.

## Add a creator

1. In the dashboard, click **Creators > Add creator**.
2. **Title** is the creator's name, or their handle if that is how people know them.
3. The text area is their bio, two or three sentences in their own words.
4. **Avatar** (right sidebar, "Set avatar") is a square photo. It shows in a circle on the clip.
5. **Creator details** sits in the Meta Boxes drawer at the bottom of the editor. Click the drawer to open it. It holds the handle, hometown, the clip (upload a short vertical video, or paste a direct link), its length, and the Instagram, TikTok and YouTube links.
6. **Page Attributes > Order** sets the order on the page. Lower numbers come first.
7. Publish. The creator appears in the stepper and the position row renames itself.

Creators have no public pages of their own. With no creators published, the section shows a short note. A creator marked "Placeholder" renders like any other, so the page can be reviewed before casting.

Clips: 9:16, muted, about ten seconds, under 10 MB. The page loops them and shows the creator's avatar and handle on top, so the clip itself needs no titles.

To fill the page with placeholders: `wp eval-file wp-content/themes/generation-maine/bin/seed-creators.php 9`. Run it with `0` to remove them.

## The newsletter

The form sends the visitor's address to the publication's subscribe page on Substack, which opens in a new tab, sends the confirmation email and keeps the list. Nothing is stored on this site. The posts list reads the publication's feed and caches it for an hour. Both are driven by the one address under Settings > Newsletter.

## Rebuilding the stylesheet

`style.css`, `assets/data/mural.json` and `inc/marks.php` are generated. Change the CSS in `brand/src/build_splash.py` or the WordPress additions in `brand/src/build_theme.py`, then run `python3 brand/src/build_theme.py`.
