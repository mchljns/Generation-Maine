# Generation Maine WordPress theme

A one-page block theme for GenerationMaine.org, built from the approved v2 page (Concept A, https://mchljns.github.io/Generation-Maine/v2/). Every piece of copy on the page is a block the editor can change. Everything about a creator lives on a Creator post. The channels, the newsletter address and the footer lines live on one settings screen. There is no page builder and no plugin to install.

## What is in the theme

| Path | What it does |
| --- | --- |
| `theme.json` | The palette (navy, blue, gold, tint, white), the button colors, and the settings that turn off WordPress's color and type controls |
| `style.css` | The page's stylesheet and the three fonts: Bricolage Grotesque for headlines, DM Sans for text, Michroma for labels, links and buttons. Generated from the v2 page by `brand/src/build_theme.py` |
| `assets/css/editor.css` | The same styles for the editor, so the page and posts look as they do on the site (generated) |
| `assets/js/site.js` | The page's script: the hero mural, the bar, the phone menu, the creators stepper and phone carousel, the tap to expand viewer, the footer draw (generated) |
| `assets/data/` | The mural lines and the footer markup (generated) |
| `functions.php` | Loads the styles and script and preloads the three fonts. Adds the bars and the gold dot to marked blocks. Loads the about photo after the first screen. Prints the skip link and the phone menu. Turns off the font library, Appearance > Fonts, fonts saved in Styles and the Fit text switch. Gives posts and pages the alignment, columns and sizes set on Row, Stack and Grid blocks |
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
| `assets/fonts/` | The three fonts as WOFF2, self-hosted, with their Open Font License files. `dm-sans-var.ttf` is the copy of DM Sans the brand builders read; it is left out of the zip |
| `assets/img/` | The logo, icons, share card and the about photo |
| `bin/` | A seed script for placeholder creators (`seed-creators.php`). The shell wrapper `seed-creators.sh` stays in the repository and is left out of the zip |
| `screenshot.png` | The thumbnail under Appearance > Themes (generated) |

Requires WordPress 6.5 or newer and PHP 7.4 or newer. Tested on WordPress 7.1.3 and 6.5.13 with PHP 8.4, and on WordPress 6.5 with PHP 7.4. The code avoids PHP 8 only functions.

theme.json uses schema version 3, which arrived in WordPress 6.6. WordPress 6.5 reads it as it is and skips the few settings it does not know. The page looks the same. The one difference is in the editor. A paragraph or heading shows an empty Typography panel. Its menu (the three dots) lists only Font size, and there are no sizes to pick. Ignore it.

## Install

1. Upload the theme zip under **Appearance > Themes > Add New > Upload Theme**. Use **Live Preview** to review it before activating.
2. Under **Settings > Reading** leave "Your homepage displays" on "Your latest posts". The theme's front page template shows the page either way.
3. Under **Settings > Permalinks** choose "Post name".
4. Under **Settings > Generation Maine** fill in the channels and the Substack subscribe page. Until the subscribe page is set, visitors see no signup form and logged-in admins see a note in its place. A channel with no address shows as a plain row with a placeholder handle, never a dead link. An address typed with `http://` is saved as `https://`. The Contact link can also be an email address, written as `mailto:name@example.org`. Anything else is refused with a red notice, and the address saved before is kept (on a new site, the default Contact link). A handle is saved with one @ and no spaces, however it was typed. A handle that is only an @ counts as empty. A channel with an address but no handle shows the handle from the address. That is the @name in a TikTok or YouTube address, even one copied from a video, or the name in an Instagram address. An address with no handle in it, such as a YouTube /channel/ address or an Instagram share link, shows the site instead (youtube.com or instagram.com). Fill in the handle for those. On the page, handles and addresses keep their exact letters, so 4x4 stays 4x4 and two hyphens stay two hyphens. A cleared footer line or legal line goes back to its default.
5. Under **Settings > Privacy** pick the privacy page. The footer links to it; until then "Privacy" is plain text.
6. Optional: set a Site Icon under **Settings > General**. The theme ships a favicon either way.

## Edit the copy

Open **Appearance > Editor > Templates > Front Page**. Every section is made of normal blocks, named in the List View (Kicker, Headline, Lede, Aim, Note, Goal and so on).

In WordPress 7, the hero, About and Follow are pattern sections: click any text to change it. To add a block or change a setting under Advanced, select the section and click **Edit pattern** first, then **Exit pattern** when done. The bar is its own part: click it and choose **Edit original**.

- **The bar:** the three link labels and the button text. Click a label or the button in the bar to change it, or pick it in List View. The sidebar does not list them; WordPress lists only its own theme blocks there. The phone menu and the footer copy them, so there is one place to edit them. In a narrow editor canvas (List View open, or the Mobile preview) the labels and the button wrap inside the bar, which grows to hold them. On a phone the page itself shows the menu button instead. The links point at the sections by fixed ids. The theme keeps the ids `top`, `about`, `creators`, `follow` and `newsletter` whatever the HTML anchor field says, so the links cannot break. On every other page of the site the same links lead back to the front page.
- **The hero:** the label, the headline, the lede and one button. The last word of the headline turns gold with the dot after it, even if it is bold or a link. A period at the end becomes the dot, inside or after the bold or link. Inside quote marks it does too, so "home." shows the dot after the closing quote. A headline that ends in a question mark, an exclamation mark or an ellipsis keeps it and gets no dot, in the editor as on the page. The editor shows the dot but not the gold, and it keeps a final period in front of the dot. Spaces or a line break typed after the last word are taken out when you click away from the headline, as on the page. The dot never wraps onto a line of its own. Keep the headline under about ten words. A word too long for its line, such as a web address, breaks where it must instead of pushing the page sideways.
- **The bars:** any paragraph with the class `k k-bars` gets the small bars before it. Add the class under Advanced > Additional CSS class(es) (Edit pattern first).
- **About:** the photo, the label, the aim in one sentence, a note, and the goal. After replacing the photo, write its Alternative text in the image block's sidebar; WordPress leaves it empty. The photo loads after the first screen, as on the v2 page, also after it is replaced.
- **The creators:** the heading is a block; the stories come from the Creator posts. The Creators block, the Follow List and the Newsletter Signup are locked in place so they cannot be deleted by accident. Each can be used once on a page, so the editor offers no Duplicate for them. If a second Creators block gets onto a page anyway, the editor marks it and the page shows it as the roster, not a second stepper. The Logo, the Phone menu button and the Maine mural show once too. A copy made with Duplicate gets a note in the editor, with Find original and Remove, and the page leaves the copy out. On WordPress 7, a copy inside the hero needs Edit pattern first; then Remove works.
- **Follow:** the heading and lede are blocks; the rows come from Settings > Generation Maine.
- **Newsletter:** the label and heading are blocks; the form comes from Settings > Generation Maine.
- **Footer:** the line, the legal line and the contact link come from Settings > Generation Maine.

Colors, type, the button shape and the motion are not editable in the page. That is on purpose. They live in `theme.json` and the stylesheet. Styles has no color or font controls and no font library, and Appearance > Fonts is hidden. A font installed there before, or picked in Styles under theme 3.1.0, is ignored. The editor and the page keep the three fonts, with no reset needed. Blocks have no font, size, border radius or shadow controls.

On WordPress 7.1, Styles still shows a few panels the theme cannot remove. Typography lists Text, Links, Headings, Captions and Buttons with text alignment only, and Font size presets. Background is an empty panel. Shadows can take new presets. Layout holds the content and wide widths. Under Blocks, Button offers the Outline style and a Width, Quote a Plain style and Table a Stripes style. Each block screen has a States menu for tablet and mobile, and on Button also for hover and focus. The Styles menu (the three dots) holds Additional CSS and Reset styles. Leave all of these as they are. If something was changed under Styles anyway, **Styles > Reset styles** undoes it.

**Start over:** Templates > Front Page > Actions > Reset puts the page back to the theme's version. The bar is a separate part: also reset it under Patterns > Template Parts > Header. Each template keeps its revisions (View revisions) if you only want to step back.

**Other pages.** Posts, pages, archives, search results and the 404 page use the same bar and footer with plain readable type. The editor shows a post or page the same way: the title, then the text in a readable column. A Button block wears the page's gold button, or the outline button with the Outline style. Columns, Buttons, Galleries and Row, Stack and Grid groups lay out as WordPress intends, in the editor as on the page. That includes a Button's Width, a Row's alignment and a Grid's columns and minimum width. A Group's Content width and justification are not used there; the reading column sets the width. Archive page numbers are full-size tap targets. The page sections (About, Follow) can also be inserted into a normal page from Patterns > Generation Maine. They run full width there and look as they do on the front page. So does the Creators block placed on its own, as the stepper or the roster. Place it straight in the page, not inside a Group or Columns, where it would be squeezed into the column.

## Add a creator

1. In the dashboard, click **Creators > Add creator**.
2. **Title** is the creator's name, or their handle if that is how people know them (then the clip shows the handle once). The page shows names and handles with their exact letters, so a creator called @maine.4x4 never shows as 4×4.
3. The text area is their story, two or three sentences in their own words. The page shows the story as typed, like the name. Two hyphens stay two hyphens, three dots stay three dots, and 4x4 keeps its x.
4. **Avatar** (right sidebar, "Set avatar") is a square photo. It shows in a circle on the clip. It is also the still a paused clip shows, so a photo at least 1200 px tall stays sharp. With no avatar, the clip header and the paused still show the placeholder figure.
5. **Creator details** sits in the Meta Boxes drawer at the bottom of the editor. On WordPress 7 the drawer opens over the lower part of the editor. Drag its bar to make it taller or shorter, or click Meta Boxes to close it. It holds the handle, the hometown, the clip and its length, and the Instagram, TikTok and YouTube links. The handle is saved with one @ and no spaces, however it was typed. For the clip, click **Choose or upload a clip** and pick a short vertical video or GIF, or paste a direct link into "Or a clip link". A chosen clip wins over a link; click **Remove** to use the link instead. The box warns when the clip is over 10 MB. A chosen clip gets the warning at once. A link to a file in this site's Media Library gets it once you save and open the creator again. A query string after the link, such as ?v=2, is fine. Changing the link hides its warning until then. Remove brings back the warning of a saved link over 10 MB. A link to another site is not checked. Click **Save** or press Ctrl+S to save a change made in Creator details, as for the title. Leaving the editor with an unsaved change there warns first. The Undo button at the top of the editor does not change Creator details, apart from Place on the page. To undo typing in one of its fields, press Ctrl+Z (Cmd+Z on a Mac) while the cursor is still in that field.
6. **Place on the page**, at the bottom of Creator details, sets the order. Lower numbers come first. It is the same number as WordPress's own Order, so a change in either shows in the other. Order is under Post Attributes in the sidebar on WordPress 6.5, under Actions on WordPress 7, and in Quick Edit in the Creators list. WordPress 7 also shows a "Parent" row in the sidebar; creators do not use it.
7. Publish. The stepper adds the story and the position row renumbers itself.

The Creators list shows each creator's place, hometown and whether they are a placeholder, in page order. Creators have no public pages of their own, though like any published content their name and story can be read through the WordPress REST API. An account that only owns creators is not listed or shown to visitors there. Editors and Administrators still see it. With no creators published, the section shows a short note. A creator marked "Placeholder" renders like any other, so the page can be reviewed before casting. A creator restored from the Trash comes back as a draft; publish it again to put it back on the page. The block shows up to 24 creators (Creators block > Most creators to show); past twelve, the position row on phones is a progress bar and visitors swipe. Up to twelve, the row has one segment per creator. The segments are 44 px tall but narrower on phones. With nine creators they are 35 px wide on a 390 px screen, 28 px at 320 px and 40 px at 430 px. That passes the 24 px minimum in WCAG 2.5.8 but is below the 44 px the rest of the page uses. Visitors can also swipe the cards one at a time, or focus the cards and use the arrow keys.

Who can do what: Editors and Administrators add, edit and remove any creator. Authors can add and publish their own creators straight onto the home page; Contributors can add creators for review but cannot set an avatar or upload a clip. Their Creator details box has the clip link field only, with a line saying an editor can upload the clip. Saving a creator someone else made keeps them as its author. If creators should always be reviewed, give contributors' accounts to the people adding them.

Clips: 9:16, muted, about ten seconds, under 10 MB. MP4 (H.264) plays everywhere. The page loads a clip only when its story is current or next door, plays the current one and pauses the rest. Visitors can pause all clips with the pause button by the counter. A paused clip shows the creator's avatar as a still, or the placeholder figure when there is no avatar. The pulsing dot in the headline stops too. Visitors who ask their device for reduced motion start with the clips paused. On phones the card shows the top 4:5 of the clip; tapping it opens the full frame.

### Placeholder creators

`wp eval-file wp-content/themes/generation-maine/bin/seed-creators.php 9 https://mchljns.github.io/Generation-Maine/v2/media`

This makes nine placeholder creators and imports each one's portrait and clip from the v2 preview into the media library. It then says how many of the 18 files it imported. Leave off the address for creators with no media. Run it with `0` to remove the creators the script made that are still placeholders and still as it left them, in any status. It also removes the media it imported that no other creator uses. Running it with 9 again does the same first. It never touches a creator you made yourself, even one marked Placeholder, nor a seeded creator you turned into a real one by unticking Placeholder. It also keeps a seeded creator someone changed, even one still marked Placeholder. A new name, story, avatar, clip or place, or anything typed in Creator details, counts as a change. Removing the sample's own avatar or clip does not. The script says how many it kept. Untick Placeholder on any that is now a real creator, and delete the rest by hand. Placeholders made by theme 3.0.0, which did not mark them, go to the Trash instead. That happens only while every field and their media are as that script left them. The script says how many it moved. Restore any you want to keep. Their media stays until you empty the Trash and run the script again. On a site with the Trash turned off, the script leaves them in place and says so. Delete any you changed by hand.

**Creators belong to the theme.** The Creators menu, its blocks and Settings > Generation Maine exist only while this theme is active. Switching themes hides them; the creators and settings stay in the database and come back when the theme does.

## The newsletter

The form sends the visitor's address to the publication's subscribe page on Substack, which opens in a new tab, sends the confirmation email and keeps the list. Nothing is stored on this site. The Substack row in the follow list uses the same address, and the footer's channel icons open the accounts once their addresses are set.

## Search engines and sharing

The theme writes the title, description, canonical address, share card and Organization details itself, using the Site Title from Settings > General. With a static front page and a posts page under Settings > Reading, these belong to the front page only. The posts page gets its own title. If an SEO plugin (Yoast SEO, Rank Math, SEOPress, All in One SEO) is activated, the theme steps aside completely. Set the plugin's homepage title, description and share image before relying on it.

## Compared with the v2 preview

The front page matches the v2 preview apart from a few expected differences. The header links have slightly taller click areas (40 px against 35 px), because WordPress wraps each link in a paragraph block. Until the channels and the Substack page are set in Settings > Generation Maine, the stories have no social row and Follow has no signup form. Both are shorter on phones, and the desktop story text sits about 16 px lower. The placeholder creators show their portraits in the handle chips, where the preview shows a silhouette.

## Before launch

- The footer shows a small build stamp while the site is in review, so a stale copy can be told from the current one. Turn it off at launch with `add_filter( 'gm_show_build', '__return_false' );` in a small plugin or the child theme.
- The about photo is a placeholder (Lisbon Street, Lewiston, CC BY 2.0). Replace it, or credit it on the page, before the site is public.
- Replace the placeholder creators with the real ones.
- Theme Check (the plugin) lists a few items that are expected for a theme built for one site. The Creators post type, the blocks and the settings screen belong to this theme on purpose. There is no readme.txt. Only themes in the WordPress.org directory need one. favicon.ico stays for browsers and apps that do not read SVG icons, and it is printed only until a Site Icon is set. The copyright notice waits on the client's wording.

## Rebuilding

`style.css`, `assets/css/editor.css`, `assets/js/site.js`, `assets/data/`, `inc/marks.php`, `inc/build.php`, `theme.json`, the fonts, the images and `screenshot.png` are generated from the v2 page. Change the page in `brand/src/build_splash_lean.py`, or the WordPress additions in `brand/src/build_theme.py`, then run:

```
python3 brand/src/build_splash_lean.py && python3 brand/src/build_theme.py && python3 brand/src/package_theme.py
```

The builders convert DM Sans and Michroma to WOFF2 with fontTools, so the rebuild needs `pip install fonttools brotli` (and Pillow, as before). The PHP, the patterns, the templates and the blocks are written by hand.
