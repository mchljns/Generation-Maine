# Generation Maine WordPress theme

A one-page block theme for GenerationMaine.org, built from the approved v2 page (Concept A, https://mchljns.github.io/Generation-Maine/v2/). Every piece of copy on the page is a block the editor can change. Everything about a creator lives on a Creator post. The channels, the newsletter address and the footer lines live on one settings screen. There is no page builder and no plugin to install.

## What is in the theme

| Path | What it does |
| --- | --- |
| `theme.json` | The palette (navy, blue, gold, tint, white) and the three fonts: Bricolage Grotesque for headlines, DM Sans for text, Michroma for labels, links and buttons |
| `style.css` | The page's stylesheet. Generated from the v2 page by `brand/src/build_theme.py` |
| `assets/css/editor.css` | The same styles for the block editor, so the canvas looks like the page (generated) |
| `assets/js/site.js` | The page's script: the hero mural, the bar, the phone menu, the creators stepper and phone carousel, the tap to expand viewer, the footer draw (generated) |
| `assets/data/` | The mural lines and the footer markup (generated) |
| `functions.php` | Loads the styles and script, preloads the fonts, adds the bars and the gold dot to marked blocks, prints the skip link and the phone menu |
| `inc/settings.php` | **Settings > Generation Maine**: the three channels, the Substack subscribe page, the footer line, the legal line and the contact link |
| `inc/creators.php` | The Creators post type, its fields, and the two layouts that render them: the stepper (the page's layout) and the roster |
| `inc/follow.php` | The follow list, one row per channel |
| `inc/newsletter.php` | The signup form that hands off to Substack, and a latest-posts reader kept for later |
| `inc/footer.php` | The footer: the drawn mark, the line, the links, the legal line |
| `inc/marks.php` | The logo, the platform marks, the bars and the placeholder avatar (generated) |
| `inc/seo.php` | Title, description, canonical, share card and Organization schema. Steps aside if an SEO plugin is active |
| `inc/build.php` | The build stamp and the version used to refresh cached files (generated) |
| `blocks/` | Creators, Follow, Newsletter Signup, Site Footer, Part (the logo, the phone menu button and the mural, drawn by the theme), and Latest Newsletter Posts (not on the page today) |
| `patterns/` | The page sections: header, hero, about, creators, follow; plus the 404 line and the no-results line |
| `templates/` | The front page, single posts, pages, archives, search, the fallback index and the 404 page |
| `assets/fonts/` | The three fonts, self-hosted, with their Open Font License files |
| `assets/img/` | The logo, icons, share card and the about photo |
| `bin/` | A seed script for placeholder creators |
| `screenshot.png` | The thumbnail under Appearance > Themes (generated) |

Requires WordPress 6.5 or newer and PHP 7.4 or newer. Tested on WordPress 7.2 (alpha) with PHP 8.4. The code avoids PHP 8 only functions.

## Install

1. Upload the theme zip under **Appearance > Themes > Add New > Upload Theme**. Use **Live Preview** to review it before activating.
2. Under **Settings > Reading** leave "Your homepage displays" on "Your latest posts". The theme's front page template shows the page either way.
3. Under **Settings > Permalinks** choose "Post name".
4. Under **Settings > Generation Maine** fill in the channels and the Substack subscribe page. Until the subscribe page is set, visitors see no signup form and logged-in admins see a note in its place. A channel with no address shows as a plain row with a placeholder handle, never a dead link. An address typed with `http://` is saved as `https://`. Anything that is not a web address is refused with a red notice, and the address saved before is kept. A handle gets its @ if it is missing, and a channel with an address but no handle shows the handle from the address. A cleared footer line or legal line goes back to its default.
5. Under **Settings > Privacy** pick the privacy page. The footer links to it; until then "Privacy" is plain text.
6. Optional: set a Site Icon under **Settings > General**. The theme ships a favicon either way.

## Edit the copy

Open **Appearance > Editor > Templates > Front Page**. Every section is made of normal blocks, named in the List View (Kicker, Headline, Lede, Aim, Note, Goal and so on).

In WordPress 7, the hero, About and Follow are pattern sections: click any text to change it. To add a block or change a setting under Advanced, select the section and click **Edit pattern** first, then **Exit pattern** when done. The bar is its own part: click it and choose **Edit original**.

- **The bar:** the three link labels and the button text. The phone menu and the footer copy them, so there is one place to edit them. The links point at the sections by fixed ids. The theme keeps the ids `top`, `about`, `creators`, `follow` and `newsletter` whatever the HTML anchor field says, so the links cannot break. On every other page of the site the same links lead back to the front page.
- **The hero:** the label, the headline, the lede and one button. The last word of the headline turns gold with the dot after it, even if it is bold or a link. A headline that ends in a question mark or an exclamation mark keeps it and gets no dot. The editor shows the dot but not the gold. Keep the headline under about ten words.
- **The bars:** any paragraph with the class `k k-bars` gets the small bars before it. Add the class under Advanced > Additional CSS class(es) (Edit pattern first).
- **About:** the photo, the label, the aim in one sentence, a note, and the goal. After replacing the photo, write its Alternative text in the image block's sidebar; WordPress leaves it empty.
- **The creators:** the heading is a block; the stories come from the Creator posts. The Creators block, the Follow List and the Newsletter Signup are locked in place so they cannot be deleted by accident.
- **Follow:** the heading and lede are blocks; the rows come from Settings > Generation Maine.
- **Newsletter:** the label and heading are blocks; the form comes from Settings > Generation Maine.
- **Footer:** the line, the legal line and the contact link come from Settings > Generation Maine.

Colors, type, the button shape and the motion are not editable in the page. That is on purpose. They live in `theme.json` and the stylesheet, and the color and type controls are turned off in Styles. If something was changed under Styles anyway, **Styles > Reset styles** undoes it.

**Start over:** Templates > Front Page > Actions > Reset puts the page back to the theme's version. The bar is a separate part: also reset it under Patterns > Template Parts > Header. Each template keeps its revisions (View revisions) if you only want to step back.

**Other pages.** Posts, pages, archives, search results and the 404 page use the same bar and footer with plain readable type. The page sections (About, Follow) can also be inserted into a normal page from Patterns > Generation Maine; they run full width there.

## Add a creator

1. In the dashboard, click **Creators > Add creator**.
2. **Title** is the creator's name, or their handle if that is how people know them.
3. The text area is their story, two or three sentences in their own words.
4. **Avatar** (right sidebar, "Set avatar") is a square photo. It shows in a circle on the clip.
5. **Creator details** sits in the Meta Boxes drawer at the bottom of the editor. It holds the handle, the hometown, the clip and its length, and the Instagram, TikTok and YouTube links. For the clip, click **Choose or upload a clip** and pick a short vertical video or GIF, or paste a direct link into "Or a clip link". A chosen clip wins over a link; click **Remove** to use the link instead. A clip over 10 MB gets a warning.
6. **Place on the page**, at the bottom of Creator details, sets the order. Lower numbers come first. (Quick Edit in the Creators list has the same field as Order. WordPress 7 also shows a "Parent" row in the sidebar; creators do not use it.)
7. Publish. The stepper adds the story and the position row renumbers itself.

The Creators list shows each creator's place, hometown and whether they are a placeholder, in page order. Creators have no public pages of their own, though like any published content their name and story can be read through the WordPress REST API. With no creators published, the section shows a short note. A creator marked "Placeholder" renders like any other, so the page can be reviewed before casting. A creator restored from the Trash comes back as a draft; publish it again to put it back on the page. The block shows up to 24 creators (Creators block > Most creators to show); past twelve, the position row on phones is a progress bar and visitors swipe.

Who can do what: Editors and Administrators add, edit and remove any creator. Authors can add and publish their own creators straight onto the home page; Contributors can add creators for review but cannot set an avatar. If creators should always be reviewed, give contributors' accounts to the people adding them.

Clips: 9:16, muted, about ten seconds, under 10 MB. MP4 (H.264) plays everywhere. The page loads a clip only when its story is current or next door, plays the current one and pauses the rest. Visitors can pause all clips with the pause button by the counter; a paused GIF shows the creator's portrait. Visitors who ask their device for reduced motion start with the clips paused. On phones the card shows the top 4:5 of the clip; tapping it opens the full frame.

### Placeholder creators

`wp eval-file wp-content/themes/generation-maine/bin/seed-creators.php 9 https://mchljns.github.io/Generation-Maine/v2/media`

This makes nine placeholder creators and imports each one's portrait and clip from the v2 preview into the media library. It then says how many of the 18 files it imported. Leave off the address for creators with no media. Run it with `0` to remove the creators the script made that are still placeholders, in any status, and the media it imported that no other creator uses. It never touches a creator you made yourself, even one marked Placeholder, nor a seeded creator you turned into a real one by unticking Placeholder.

**Creators belong to the theme.** The Creators menu, its blocks and Settings > Generation Maine exist only while this theme is active. Switching themes hides them; the creators and settings stay in the database and come back when the theme does.

## The newsletter

The form sends the visitor's address to the publication's subscribe page on Substack, which opens in a new tab, sends the confirmation email and keeps the list. Nothing is stored on this site. The Substack row in the follow list uses the same address, and the footer's channel icons open the accounts once their addresses are set.

## Search engines and sharing

The theme writes the title, description, canonical address, share card and Organization details itself, using the Site Title from Settings > General. If an SEO plugin (Yoast SEO, Rank Math, SEOPress, All in One SEO) is activated, the theme steps aside completely. Set the plugin's homepage title, description and share image before relying on it.

## Before launch

- The footer shows a small build stamp while the site is in review, so a stale copy can be told from the current one. Turn it off at launch with `add_filter( 'gm_show_build', '__return_false' );` in a small plugin or the child theme.
- The about photo is a placeholder (Lisbon Street, Lewiston, CC BY 2.0). Replace it, or credit it on the page, before the site is public.
- Replace the placeholder creators with the real ones.

## Rebuilding

`style.css`, `assets/css/editor.css`, `assets/js/site.js`, `assets/data/`, `inc/marks.php`, `inc/build.php`, `theme.json`, the fonts, the images and `screenshot.png` are generated from the v2 page. Change the page in `brand/src/build_splash_lean.py`, or the WordPress additions in `brand/src/build_theme.py`, then run:

```
python3 brand/src/build_splash_lean.py && python3 brand/src/build_theme.py && python3 brand/src/package_theme.py
```

The PHP, the patterns, the templates and the blocks are written by hand.
