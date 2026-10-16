# Round 2 results (retest of round 1 plus new findings)

Totals: retest {'fixed': 60, 'partly': 11, 'not_fixed': 3}; new by severity {'medium': 10, 'low': 33, 'info': 10}

## install
retest: {'fixed': 8, 'partly': 1}; new findings: 5
- I08 [partly] Fixed: the header now says 'Tested up to: 7.1' (it said 6.8), and the schema logo now uses the Site Icon (cropped-sample-portrait.jpg). Still open: the README says 'Tested on WordPress 7.2 (alpha) with PHP 8.4' while the header says 7.1 and the templates run 7.1.3. The details overlay still shows no tags, and 'By Green Falls' has no link because there is no Author URI. Theme Check still warns 'Could not find a copyright notice'. The fix plan listed adding an Author URI and a copyright line; neither is in style.css. The other Theme Check flags match round 1 (plugin territory and so on) and do not matter for a bespoke theme.
  evidence: /tmp/claude-0/wptest/work/r2-install/logs/c71-s8-details.txt, /tmp/claude-0/wptest/work/r2-install/logs/c65-s8-details.txt, /tmp/claude-0/wptest/work/r2-install/logs/s71-themecheck.txt

### INS-N01 [medium] A Button block in a post or page shows blue text on WordPress's default dark gray (1.64:1), while the editor shows it white
- template: seeded71
- steps: wpt new t <port> seeded71 / Pages > Add New: add a Buttons block with two Button blocks (+ > Buttons, type 'First button', add a second), publish. The same markup is in /tmp/claude-0/wptest/work/r2-install/scripts/blocks-page.html / Open the page as a visitor at 1440 and 390, and look at the buttons / Open the same page in the block editor and compare
- expected: A button a client adds to a page is readable and looks like a theme button, and it looks the same in the editor and on the page.
- actual: On the page the button text is #0556A5 on #32373c, in 11px Michroma: a contrast of 1.64:1. axe reports color-contrast (serious) on both buttons at 1440 and 390. In the editor canvas the same buttons are white on gray, so the client sees nothing wrong before publishing. The theme turns off the text and background color controls (theme.json settings.color.text and background are false), so the color cannot be fixed from the block sidebar. Reproduced on WordPress 7.1.3 (seeded71 and clean71-installed) and on 6.5.13 (clean65-installed).
- likely cause: style.css, WordPress additions: '.gm-entry a{color:var(--blue);text-decoration:underline}' also matches the button's link (a.wp-block-button__link) and overrides core's white text. The button keeps core's default #32373c background because theme.json styles.elements.button sets only the radius and the font. There is no rule for .gm-entry .wp-block-button__link: it could be excluded from the link rule and given the theme's button colors.
- evidence: /tmp/claude-0/wptest/work/r2-install/shots/c71-blocks-pages-blocks-1440.png, /tmp/claude-0/wptest/work/r2-install/shots/c65-blocks-pages-blocks-1440.png, /tmp/claude-0/wptest/work/r2-install/logs/s71-axe.json, /tmp/claude-0/wptest/work/r2-install/logs/p8511-edcanvas-47.json

### INS-N02 [low] Columns run into each other and pagination stacks on three rows in posts, pages and archives: the flex layout and gap styles are missing
- template: seeded71
- steps: wpt new t <port> seeded71 / Publish a page with a two-column Columns block, each column holding a sentence (markup in /tmp/claude-0/wptest/work/r2-install/scripts/cols-page.html) / Publish 12 or more posts in one category and open /category/news/ at 1440 and 390 / Also add a Separator and a Quote with a citation to a page (scripts/blocks-page.html)
- expected: Columns have a gutter. The pagination shows Previous, the numbers and Next on one row, as its 'space-between' setting says. A separator lines up with the text column. Citations are not italic (project rule: no italics).
- actual: There is no gap between the columns: the left column's text ends at x=529 and the right column's starts at x=535 at 1440, so the lines read as one run (shots/s71-cols-crop-1440.png). The pagination nav has display:block, so 'Previous page', '1 2 3 4' and 'Next page' sit on three separate lines at both widths. The Buttons block is display:block too. The separator is centered on a 68ch measure (it starts at x=325 while the text starts at x=140). The quote's cite renders italic. Reproduced on seeded71 and clean65-installed for the columns, and on clean71-installed, seeded71 and clean65-installed for the pagination, separator and cite.
- likely cause: theme.json sets settings.spacing.blockGap to false, so WordPress prints no layout rules ('.is-layout-flex{display:flex}', column gaps) in global-styles-inline-css; I checked and none are there. The is-layout-flex classes on the pagination and buttons therefore do nothing, and core Columns get no gap. In style.css, '.gm-entry>*{max-width:68ch}' combined with the separator's auto margins centers the hr. There is no rule for cite.
- evidence: /tmp/claude-0/wptest/work/r2-install/shots/s71-cols-crop-1440.png, /tmp/claude-0/wptest/work/r2-install/logs/s71-cols-pages.json, /tmp/claude-0/wptest/work/r2-install/shots/s71-many-pag-390.png, /tmp/claude-0/wptest/work/r2-install/shots/c71-pag-1440.png

### INS-N03 [low] Archive page numbers are 11px-wide tap targets about 4px apart
- template: seeded71
- steps: wpt new t <port> seeded71 / Publish about 32 posts in one category so the archive has 4 pages / Open /category/news/page/2/ at 390 and try to tap 3 or 4
- expected: Page links are comfortable to tap, at least 24px apart (WCAG 2.5.8) and ideally 44px, as the rest of the theme aims for.
- actual: Each number link is 11-12px wide and 44px tall, at x=20, 35, 51 and 66 at 390 (centers 15-16px apart), so a finger covers two numbers. The same widths show at 1440. Measured on seeded71 (4 pages), clean71-installed and clean65-installed (2 pages).
- likely cause: style.css '.wp-block-query-pagination a,.wp-block-query-pagination .page-numbers{display:inline-flex;align-items:center;min-height:44px}' sets a height but no min-width or side padding. The nav's 'gap:8px 20px' applies only between its flex children, and the numbers wrapper is a single child (with the layout styles missing, it does not apply at all).
- evidence: /tmp/claude-0/wptest/work/r2-install/logs/s71-many-pag.json, /tmp/claude-0/wptest/work/r2-install/shots/s71-many-pag-390.png, /tmp/claude-0/wptest/work/r2-install/logs/c71-pag.json, /tmp/claude-0/wptest/work/r2-install/logs/c65-pag.json

### INS-N04 [low] The Follow section inserted into a page from Patterns picks up post typography: smaller heading, pushed below the lede
- template: seeded71
- steps: wpt new t <port> seeded71 / Create a page and insert Patterns > Generation Maine > About and Follow (the pattern markup I used is in /tmp/claude-0/wptest/work/r2-install/scripts/patterns-page.html), publish / Compare the Follow section on that page with the one on the front page at 1440 and 390
- expected: The README says the About and Follow sections can be inserted into a normal page and run full width there, so they should look the same as on the front page.
- actual: About matches the front page to the pixel. In Follow, 'Where to find it' is 34px instead of 52px at 1440 (26px instead of 34px at 390). It gets a 61px top margin (47px at 390), so it sits 61px lower than the lede beside it instead of level with it. The lede grows from 19px to 21px at 1440 (and shrinks to 18px at 390), and the section is 42px taller. Reproduced on clean71-installed and seeded71.
- likely cause: style.css '.gm-entry h2{font-size:clamp(26px,3vw,34px);line-height:1.15;margin-top:1.8em}' and 'main.gm-page .lede{font-size:clamp(18px,2vw,21px)}' are descendant rules, so they reach inside an inserted section. The full-width rule '.gm-entry>.wp-block-group.block' fixes only the width. The post-content rules could stop at sections (for example with :not(.block *) or by scoping them to direct children).
- evidence: /tmp/claude-0/wptest/work/r2-install/logs/c71-cmp-sections.json, /tmp/claude-0/wptest/work/r2-install/logs/s71-cmp-sections.json, /tmp/claude-0/wptest/work/r2-install/shots/c71-sections-pages-sections-1440.png

### INS-N05 [low] The post and page editor canvas does not match the new templates: title smaller than the headings, text flush to the edge
- template: seeded71
- steps: wpt new t <port> seeded71 / Follow README step 5: Settings > Privacy > Use This Page, then open the page in the block editor / Compare the canvas with /privacy-policy/ on the site
- expected: The editor previews the page roughly as it will look: the title is the largest heading, and the text is inset and at a readable width, as on the published page.
- actual: In the canvas the title 'Privacy Policy' is 34px while each content h2 ('Who we are' and so on) is 46.4px. The text starts at x=0 of the canvas and runs the full 1160px. The published page shows a 72px title, 34px h2s, text inset 140px and a 68ch measure. Same on the Privacy Policy page on clean71-installed, seeded71 and clean65-installed, and on another page on seeded71. Round 1 saw this once and left it untested; it is a client's first page edit in the README.
- likely cause: assets/css/editor.css has .gm-title and .gm-entry rules, but the post editor renders the content without the template. The canvas root is '.is-root-container.wp-block-post-content' with no gm-entry class, and the title is .editor-post-title. So the general section rule 'h2,.h2{font-size:clamp(34px,4vw,52px)}' applies, and nothing sets the title size, padding or width. The editor needs the same rules scoped to the post editor wrapper and title.
- evidence: /tmp/claude-0/wptest/work/r2-install/shots/c71-s2-privacy-3-editor.png, /tmp/claude-0/wptest/work/r2-install/shots/s71-s2-privacy-3-editor.png, /tmp/claude-0/wptest/work/r2-install/logs/p8501-edcanvas-3.json, /tmp/claude-0/wptest/work/r2-install/logs/p8511-edcanvas-3.json

not tested: Saving Post name permalinks through the UI on Apache or nginx (the PHP built-in server saves /index.php/%postname%/); A subdirectory install, which would test the new home_url links for real; A real Substack sign-up (the form request was intercepted); The PHP 7.4 Playground site (the compat tester's area); Lighthouse and contrast.mjs on secondary pages (I used axe instead); The Hero and Creators patterns inserted into a page (the README names only About and Follow); Other core blocks in posts (Image with caption, Gallery, Cover, Embeds); Theme Check on 6.5; Whether single posts should offer comments or previous/next links (the templates have neither; I did not judge it)

## editor (retest after round 1 fixes)
retest: {'partly': 4, 'fixed': 12}; new findings: 6
- E01 [partly] Fixed part: each tile now shows the number and name (opacity 1, navy, static position). The 'Label before the next name' and 'Label on the last creator' controls disappear in Roster. Remaining: the town is still cut off on every tile at 1440, 390 and 320 (fine at 1024). Examples: 'Skowhegan, Ma' (clientWidth 88 of scrollWidth 109) and 'Presque Isle, M' (88 of 114). Because the span is display:flex, no ellipsis shows; the text simply stops mid-word. The town and number also pick up the overlay's dark text-shadow. The cause is the same leak as in round 1: style.css still has unscoped stepper rules `.who span{display:flex;...}` and `.who span b,.who span{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}`, and these match the roster's .who .n and .who .town spans. Fix: scope them to `.stage .who`, `.panel .pv .who` and `.slide .fr .who`, or rename the roster span.
  evidence: /tmp/claude-0/wptest/work/r2-editor/data/r2-e01-roster-8503.txt, /tmp/claude-0/wptest/work/r2-editor/data/r2-e01-roster-8513.txt, /tmp/claude-0/wptest/work/r2-editor/data/r2-e01-town-clipping.txt
- E08 [partly] Colors are fixed: Styles has no Colors panel, and blocks have no Color panel. Type is not off, although README line 57 says 'the color and type controls are turned off in Styles'. Styles > Typography still offers Manage fonts, a Font picker for Text, Links, Headings (each level), Captions and Buttons, and Font size presets. Styles > Blocks offers Font for Paragraph, Heading, Button and Group, plus Border radius, Shadow and an Outline variation for Button. Each block's Typography menu offers Font, Line indent and Fit text. The round 1 mismatch remains: after the heading font change the canvas draws every h1 and h2 in DM Sans, but the live page keeps Bricolage Grotesque. The paragraph font change does reach the live page: the hero lede and every paragraph turn Michroma. Border radius 24 is saved but ignored in both the editor and the front (0px). Styles > More > Reset styles returns {"styles":[]} on both. Fix: turn off typography.fontFamilies selection in theme.json, or make style.css and editor.css agree; otherwise change the README sentence.
  evidence: /tmp/claude-0/wptest/work/r2-editor/data/r2-e08-styles-8503.txt, /tmp/claude-0/wptest/work/r2-editor/data/r2-styles-look-8503.txt, /tmp/claude-0/wptest/work/r2-editor/data/r2-styles-headfont-8503.txt
- E10 [partly] Fixed part: the sections now run full width (section 0+1440 and 0+390), text starts at 140 px at 1440 and 20 px at 390 like the title, and there is no overflow. About is identical to the home page (aim 42px, goal 17px). Remaining: in Follow, the page's reading styles override the section. The h2 'Where to find it' is 34px with a 61px top margin at 1440 (52px with 0 margin on the home page) and 26px with a 47px margin at 390 (34px on home). The lede is 21px instead of 19px at 1440. The cause is `.gm-entry h2{font-size:clamp(26px,3vw,34px);...;margin-top:1.8em}` (style.css:415) and `main.gm-page .lede{...}` (style.css:439), which also match headings and ledes inside inserted sections.
  evidence: /tmp/claude-0/wptest/work/r2-editor/data/r2-e10-h2size.txt, /tmp/claude-0/wptest/work/r2-editor/shots/r2-e10-follow-8513-page-1440.png, /tmp/claude-0/wptest/work/r2-editor/shots/r2-e10-about-8503-page-1440.png
- E16 [partly] Fixed part: the three nav labels stay inline and visible at 810 and 762 (nav display:flex), and the hamburger stays hidden. Remaining: the newsletter button ('Get the newsletter' / 'Join the list') disappears from the bar whenever the canvas is that narrow. .gm-bar .cta .wp-block-button__link computes to display:none (0x0) in both the Front Page and the Header part editor, which is where the client edits that text. The cause is editor.css line 98, a phone rule `.top nav,.gm-bar nav,.top .cta>.wp-block-button__link,.gm-bar .cta>.wp-block-button__link{display:none}`. The later editor override restores nav and .cta-wrap but not the link inside .cta.
  evidence: /tmp/claude-0/wptest/work/r2-editor/data/r2-e16-8503.txt, /tmp/claude-0/wptest/work/r2-editor/data/r2-e16-8513.txt, /tmp/claude-0/wptest/work/r2-editor/shots/r2-e16-listview-8503.png

### EDI-N01 [medium] A period after a bold or linked last word becomes the gold 'word': the word stays white and the headline ends in a gold period plus the gold dot
- template: seeded71
- steps: wpt new <name> <port> seeded71, log in, Appearance > Editor > Templates > Front Page / Click the hero headline, select all and type 'Young Mainers', Shift+Enter, 'on staying here.' (ending in a period) / Press ArrowLeft once, then Ctrl+Shift+ArrowLeft to select only 'here' (double-clicking the word does the same), then Ctrl+B. Variant: Ctrl+K and link it to #about / Save and view the front at 1440 and 390
- expected: README line 49: 'The last word of the headline turns gold with the dot after it, even if it is bold or a link.' With a plain final period the theme turns the period into the dot, so 'here' should be gold with one dot after it.
- actual: The front prints `on staying <strong>here</strong><span class="here">.<i class="d pulse"></i></span></h1>`, and the link variant prints the same with <a href="#about">here</a>. 'here' stays white, and a gold period sits next to the gold pulsing dot ('here..'). Reproduced on 8513 and 8503 at 1440 and 390. The canvas shows only the white word and the one gold dot, so the client sees nothing wrong.
- likely cause: gm_render_marks() in functions.php (line 147) matches `([^\s<>]+)((?:\s*</(?:strong|b|em|i|a|span|mark|u|s|code)>)*)(\s*</h[1-6]>\s*)$`. When the period sits outside </strong> or </a>, the last text run before </h1> is just '.', so '.' is wrapped as the gold word, and the strlen>1 test keeps it. Fix: remove a final period (and any whitespace) before </h1> first, remember that the dot is wanted, then find the last word, including inside inline tags.
- evidence: /tmp/claude-0/wptest/work/r2-editor/shots/r2-e05-boldperiod-8513-hero-1440-crop.png, /tmp/claude-0/wptest/work/r2-editor/shots/r2-e05-boldperiod-8503-hero-1440.png, /tmp/claude-0/wptest/work/r2-editor/shots/r2-e05-linkperiod-8513-hero-1440-crop.png, /tmp/claude-0/wptest/work/r2-editor/data/r2-e05-8513-b.txt

### EDI-N02 [low] Roster layout logs 'Undefined variable $town' on every render and labels each tile 'Maya, , Maine'
- template: seeded71
- steps: Front Page > List View > Creators > Edit pattern > select the Creators block > Layout: Roster, Most creators to show: 6 > Save / Load the front, then run wpt themelog <name> and view the front HTML
- expected: No PHP warnings, and each tile's accessible label reads 'Maya, Skowhegan, Maine'.
- actual: Each front or editor render logs 'PHP Warning: Undefined variable $town in .../inc/creators.php on line 449' once per tile (6 per view; 339 and 387 lines over the session on the two instances). Every tile prints <div class="tile" aria-label="Maya, , Maine">. The aria-label also sits on a div with no role, where screen readers mostly ignore it. On a host with display_errors on, the warning would print on the page. No warnings appear in Stepper mode. Reproduced on 8503 and 8513.
- likely cause: gm_render_roster() in inc/creators.php line 449 uses `$town`, which is never defined; the town is in `$place` (or `$c['town']`). Use esc_attr( $c['name'] . ', ' . $place ), or drop the aria-label, since the visible text already names the tile.
- evidence: /tmp/claude-0/wptest/work/r2-editor/data/themelog-r2ed1.txt, /tmp/claude-0/wptest/work/r2-editor/data/themelog-r2ed2.txt, /tmp/claude-0/wptest/work/r2-editor/data/r2-e01-town-clipping.txt

### EDI-N03 [low] Locked theme blocks can still be duplicated; a duplicated Creators block renders a second, broken stepper with duplicate ids
- template: seeded71
- steps: Front Page > List View > Creators > Edit pattern > select the Creators block > Options (menu: Copy, Duplicate, Add before, Add after, Unlock, Rename, Hide, Create pattern) > Duplicate > Save / Load the front at 1440 and scroll to the second stepper
- expected: The locked blocks stop the client from breaking the page by accident: no Duplicate, or a second copy that works.
- actual: The page gets two steppers (6588 px each on 8513), with duplicate ids for stories, stage, panels, wnext, segs, viewer, cpause and others. The second stepper is broken: the clip frame is an empty navy box with a broken-image icon and Maya's handle, while the text shows the last creator (Sam on 8513, Priya on 8503 with limit 3), and the counter reads '01 / 09' with the last segment active. Reproduced on 8513 and 8503. The Logo, Phone menu button and Maine mural Part blocks also offer Duplicate and Hide (they have no Unlock); I did not check a duplicated Part block on the front.
- likely cause: The lock attribute only covers move and remove. blocks/creators, follow, newsletter and part do not set "supports": {"multiple": false} (only site-footer does), so WordPress offers Duplicate, Ctrl+Shift+D and copy/paste.
- evidence: /tmp/claude-0/wptest/work/r2-editor/shots/r2-dup-8513-copy1-1440.png, /tmp/claude-0/wptest/work/r2-editor/shots/r2-dup-8503-copy1-1440.png, /tmp/claude-0/wptest/work/r2-editor/data/r2-parts-8503.txt

### EDI-N04 [low] The editor draws the gold dot after a headline that ends in '?' or '!', which the page leaves out
- template: seeded71
- steps: Front Page > hero headline > type 'Young Mainers', Shift+Enter, 'why do we stay?' / Look at the canvas, then save and view the front
- expected: The canvas matches the README rule 'A headline that ends in a question mark or an exclamation mark keeps it and gets no dot'.
- actual: The canvas shows 'stay?' followed by a gold dot (h1.gm-here::after has background rgb(250,200,0), width 14.4px), but the front shows a gold 'stay?' with no dot. The same happens with 'here!'. Reproduced on 8513 and 8503.
- likely cause: assets/css/editor.css always adds `.gm-here::after{...background:var(--mg)}`, whatever the text ends with. CSS cannot see the last character, so either note it in the README ('the editor always shows the dot') or have the edit script toggle a class on the heading when its text ends in ? or !.
- evidence: /tmp/claude-0/wptest/work/r2-editor/shots/r2-s1-edge-question-editor-8513.png, /tmp/claude-0/wptest/work/r2-editor/shots/r2-s1-edge-question-editor-8503.png, /tmp/claude-0/wptest/work/r2-editor/shots/r2-e05-question-8513-hero-1440-crop.png, /tmp/claude-0/wptest/work/r2-editor/data/r2-e05-8513-a.txt

### EDI-N05 [info] The Hero pattern description contradicts the README about a bold or linked last word
- template: seeded71
- steps: Front Page > click any hero text: the sidebar shows the Hero pattern description. It also appears in the inserter under Patterns > Generation Maine > Hero
- expected: The in-editor help and the README give the same rule.
- actual: The pattern description says: '...The last word of the headline turns gold and gets the pulsing dot on the page. Keep it plain text: no bold or link on the last word.' README line 49 says: 'The last word of the headline turns gold with the dot after it, even if it is bold or a link.' Seen in the sidebar and the pattern list on 8503 and in the inserter pattern list on 8513.
- likely cause: The patterns/hero.php Description header (line 6) was not updated when gm_render_marks() started handling bold and links.
- evidence: /home/user/Generation-Maine/generation-maine/patterns/hero.php, /home/user/Generation-Maine/generation-maine/README.md, /tmp/claude-0/wptest/work/r2-editor/data/r2-blockpanels-8503.txt

### EDI-N06 [info] In the Header part editor, the Content panel lists only Logo and Phone menu button, which have nothing to edit; the labels and the button are not listed
- template: seeded71
- steps: Front Page > click the bar > Edit original / Look at the Template Part tab > Content, then click 'Logo'
- expected: The Content list leads to what the client edits in the bar (the three labels and the button text), or leaves out the theme-drawn pieces.
- actual: Content lists 'Logo' and 'Phone menu button' (globe icons) and nothing else. Clicking Logo selects the Part block, and the sidebar shows only 'Generation Maine Part', its generic description and Advanced. The editable labels are reachable only in the canvas or List View. Reproduced on 8503 and 8513.
- likely cause: I suspect WordPress lists childless, non-structural custom blocks in the template part's Content panel, so generation-maine/part shows up while the core paragraph and button blocks inside groups do not. Not confirmed in WordPress source. Removing the Part blocks from that list (or giving the labels block bindings or a content role) would make it useful.
- evidence: /tmp/claude-0/wptest/work/r2-editor/shots/r2-content-panel-logo-8503.png, /tmp/claude-0/wptest/work/r2-editor/shots/r2-content-panel-logo-8513.png, /tmp/claude-0/wptest/work/r2-editor/shots/r2-e02-header-original-8503.png

not tested: Roster tiles as links: every seeded creator is a placeholder with no social links, so the <a class="tile roster-tile"> markup was not seen.; WordPress 6.5 and PHP 7.4 editor behavior (left to the compat tester).; The front-end rendering of a duplicated Logo, Phone menu button or Maine mural Part block (only the Duplicate menu item was seen).; Per-block Typography > Font on a single block, and the front effect of Styles > Layout (content width), Background, Shadows and the Button 'Outline' variation.; Uploading a font through Styles > Typography > Manage fonts.; Revisions UI and Style Book, dragging blocks in List View, keyboard-only and screen-reader editing, and real phones.; The newsletter form with a Substack address set (no settings filled in, as on a fresh site).

## visitor (front page as a visitor: phone menu, creators stepper and carousel, tap-to-expand viewer, pause control, motion, keyboard, no-JS, admin bar), round 2 retest after fixes
retest: {'fixed': 13, 'partly': 1, 'not_fixed': 2}; new findings: 8
- V05 [partly] Screen readers: #panels is now aria-live=polite, and after Enter on segment 2 Devin's heading is the exposed one, so a story change is announced (speech itself not heard). The tree still has 1 of 9 creator headings at 1440, as allowed by the 'or announced' alternative. Without JS: still broken on desktop. The panels are now static and visible, but their children keep opacity:0 from '.panel>*{opacity:0}' (only '.panel.on>*' sets 1). At 1440 and 1024, stories 2 to 9 have text opacity 0, leaving 8 empty tinted blocks (section 2487px at 1440). v2 is the same. Phones: all 9 readable.
  evidence: /tmp/claude-0/wptest/work/r2-visitor/logs/nojs2-r1.log, -r2.log ('lowest text opacity per story [1,0,0,0,0,0,0,0,0]'), /tmp/claude-0/wptest/work/r2-visitor/logs/nojs-r1.log (panels h2/bio visible false for Devin..Sam at 1440), /tmp/claude-0/wptest/work/r2-visitor/nojs/sbs-1440-nojs-story5-r1.png (WP left, v2 right: blank where Jess's story should be)
- V12 [not_fixed] Unchanged: the nine segment buttons measure 28x44, 32x44, 34x44, 35x44 and 40x44, identical on v2. The README only covers more than twelve creators ('past twelve, the position row on phones is a progress bar and visitors swipe'). It does not mention that nine segments are under 44px wide or that swiping and arrow keys are the alternative. Knowingly left; not covered by the README.
  evidence: /tmp/claude-0/wptest/work/r2-visitor/logs/measure-wp-r1.json, measure-wp-r2.json, measure-v2-r1.json (msum.py summary), /home/user/Generation-Maine/generation-maine/README.md line 73
- V16 [not_fixed] Info items remain as recorded, and the README covers none of them. (1) WP still prints Institute&#8217;s where v2 has a straight apostrophe (about 0.09% of pixels at 1440). (4) Header nav hit boxes are 40px against v2's 35px (1440 bar 0.86% differ, text rows only). (3) Desktop story h2 is 303/317 against v2's 286. (2) and (5) are expected placeholder effects. Section heights at 1440 match v2 exactly. Phone stories are 759 vs 807 and follow 813 vs 981 (no social rows or form). Hero, creators head and phone bar are 0.00% different. The phone footer is 2px taller.
  evidence: /tmp/claude-0/wptest/work/r2-visitor/logs/compare-r1.log, compare-r2.log, python3 secdiff.py compare r1 output, /tmp/claude-0/wptest/work/r2-visitor/compare/sbs-390-footer-r1.png

### VIS-N01 [medium] Paused clip of a creator with no avatar shows a broken-image icon (and stray alt text in the viewer) instead of a still
- template: seeded71
- steps: wpt new <name> <port> seeded71 / wpt wp <name> post meta delete 14 _thumbnail_id   (Cole, creator 4, keeps his GIF clip; README says Contributors cannot set an avatar, so this is a normal state) / Open http://127.0.0.1:<port>/ at 1440x900 with prefers-reduced-motion: reduce (the clips start paused), scroll the stepper to story 4 / Repeat at 390x844 with touch: tap segment 4, then tap the card to open the viewer / Or with no reduced motion: press the pause button, then go to story 4
- expected: A paused clip shows a still (the portrait, or the placeholder figure or a plain frame when there is no portrait), never a broken image.
- actual: Story 4's clip <img> loses its src: no data-still, and setSrc removes src. Chromium draws a broken-image icon at the top left of the desktop stage. The viewer shows the broken icon plus the alt text 'Clip by Cole, Machias, Maine' running into the handle chip. The phone card is an empty navy box. Every reduced-motion visitor sees this for any creator without an avatar.
- likely cause: inc/creators.php line 412 sets $still = portrait ?: avatar and omits data-still when both are empty (the placeholder avatar is not used as a still). assets/js/site.js line 32 setSrc: when paused and the element is an IMG, want = dataset.still || '', and an empty want runs el.removeAttribute('src'), leaving an <img> with alt text and no source. Fall back to the placeholder figure or hide the img when there is no still.
- evidence: /tmp/claude-0/wptest/work/r2-visitor/logs/noavatar-r1.log, noavatar-r2.log ('src':null,'hasStill':false), /tmp/claude-0/wptest/work/r2-visitor/pause/sbs-noavatar-r1.png (stage 1440, card 390, viewer 390), /tmp/claude-0/wptest/work/r2-visitor/pause/noavatar-390-viewer-r2.png

### VIS-N02 [medium] Menu sheet stays open and the page cannot scroll after rotating a tablet from portrait to landscape
- template: seeded71
- steps: wpt new <name> <port> seeded71 / Open http://127.0.0.1:<port>/ at 768x1024 with touch (iPad portrait) and tap Menu / Rotate to 1024x768 (Playwright setViewportSize), which switches to the desktop layout / Try to scroll (wheel 900px), then rotate back to 768x1024
- expected: Crossing to the desktop layout closes the menu (as the viewer already does on the same media query change) and releases the scroll lock.
- actual: At 1024x768 the sheet is display:none and the Menu button is hidden, but the sheet keeps class 'open' and body keeps overflow:hidden. A 900px wheel leaves scrollY at 0, and there is no visible control to undo it (Escape works only with a keyboard). Back at 768x1024 the sheet is still open with aria-expanded true. Same on v2. Reproduced in edge-r1 and edge-r2.
- likely cause: assets/js/site.js lines 111-124: setMenu sets document.body.style.overflow, but nothing listens for the (max-width: 900px) change to call setMenu(false). The viewer has such a listener (line 97); the menu needs the same.
- evidence: /tmp/claude-0/wptest/work/r2-visitor/logs/edge-r1.log, edge-r2.log ('menu open at 768x1024, then rotated to 1024x768' ... 'bodyOverflow':'hidden','scrollY':0), /tmp/claude-0/wptest/work/r2-visitor/edge/wp-rotate-r1.png

### VIS-N03 [low] Pause control changes its accessible name together with aria-pressed, so screen readers hear 'Play the clips, toggle button, pressed' while paused
- template: seeded71
- steps: wpt new <name> <port> seeded71 / Open http://127.0.0.1:<port>/ at 1440x900 or 390x844, Tab to the pause button (stop 9 at 1440, 15 at 390), press Space, then Enter / Read the button's role, name and pressed state from the accessibility tree (CDP Accessibility.getPartialAXTree) or a screen reader. With reduced motion, read the state at load.
- expected: A toggle keeps one label and lets aria-pressed carry the state (for example 'Pause the clips', pressed true while paused). Or it swaps the label and drops aria-pressed. Not both.
- actual: Playing: name 'Pause the clips', pressed false. Paused: name 'Play the clips', pressed true, which reads as 'Play' being on while the clips are stopped. Reduced-motion visitors meet 'Play the clips, pressed' first. Keyboard operation works: Space and Enter toggle, the focus ring is a 2px blue outline, and the button is 44x44 with no overlap. Same on v2.
- likely cause: assets/js/site.js line 66 setPaused sets both aria-pressed and aria-label ('Play the clips' / 'Pause the clips'). Keep one of the two mechanisms.
- evidence: /tmp/claude-0/wptest/work/r2-visitor/logs/pause-ax-r1.log, pause-ax-r2.log, /tmp/claude-0/wptest/work/r2-visitor/logs/pause-r1.log (ariaSnapshot 'button "Play the clips" [pressed]'), /tmp/claude-0/wptest/work/r2-visitor/pause/stack-where-r1.png

### VIS-N04 [low] Tab past the last link of the open phone menu moves focus behind the opaque sheet and scrolls the hidden page
- template: seeded71
- steps: wpt new <name> <port> seeded71 / Open http://127.0.0.1:<port>/ at 390x844 (or a 1280 window at 200 percent zoom, emulated as 640x400 at DSF 2), focus Menu, press Enter / Press Tab 7 times
- expected: After Get the newsletter, focus either wraps to the Menu button (or stays in the bar and sheet), or the sheet closes when focus leaves it. Focus is never hidden under the sheet.
- actual: Tabs 1-4 reach the four sheet links. Tab 5 focuses 'Follow along' at y=689, covered by the sheet (elementFromPoint is inside #sheet). Tab 6 focuses the creators carousel and scrolls the page behind the open sheet to 1470 (1801 at 640x400). Tab 7 lands on a card that is also covered. The sheet stays open throughout. Same on v2.
- likely cause: assets/js/site.js lines 111-124: the sheet is now after the bar in tab order and inert while closed, but while open nothing contains focus or closes the sheet on focusout. body overflow:hidden does not stop focus-driven scrolling.
- evidence: /tmp/claude-0/wptest/work/r2-visitor/logs/menu-open-tab-r1.log, menu-open-tab-r2.log ('hiddenBehindSheet':true), /tmp/claude-0/wptest/work/r2-visitor/logs/menu-r1.log, menu-r2.log ('tab x6 after open'), /tmp/claude-0/wptest/work/r2-visitor/menu/wp-390x844-kbd-open-tab5-r1.png

### VIS-N05 [low] At 768x1024 and 844x390, swiping one card at a time skips creator 8: the counter jumps from 07 to 09
- template: seeded71
- steps: wpt new <name> <port> seeded71 / Open http://127.0.0.1:<port>/ at 768x1024 (or 844x390) with touch and scroll to The creators / Swipe left one card at a time and read the counter after each swipe / Optional, to see the video effect: set creator 8 (post 26) to a WebM clip (gm_clip_id 0, gm_clip_url to a .webm) and watch which card plays
- expected: Every creator becomes current in turn (01 ... 08, 09), or the last two cards share the end state without skipping a number.
- actual: Counter values seen: 01 02 03 04 05 06 07 09. The seventh swipe hits the end of the track (cards 8 and 9 both fully visible), and the end rule makes 09 current, so Noah (08) is never current by swiping. His segment never lights and his video never plays unless segment 8 is tapped. At 390 every value 01-09 appears. Same on v2. Reproduced in carousel.mjs, carousel-end.mjs (8512, video) and carousel-end2.mjs, both runs.
- likely cause: assets/js/site.js line 49 nearest(): at scrollLeft >= max - 2 it returns want or the last card, so a swipe that reaches the end selects 9 even though 8 was the next card. One alternative is to step to cur+1 when the track reaches its end from a single forward swipe.
- evidence: /tmp/claude-0/wptest/work/r2-visitor/logs/carousel-end-r1.log, carousel-end-r2.log ('counter values seen while swiping one card at a time: 01 02 03 04 05 06 07 09', swipe 7 'vids ... 8:P 9:PLAY'), /tmp/claude-0/wptest/work/r2-visitor/logs/carousel-end2-r1.log, -r2.log (swipe x9 sequence), /tmp/claude-0/wptest/work/r2-visitor/logs/carousel-r1.log ('wp 768 swipe left 6' -> 07, 'swipe left 7' -> 09)

### VIS-N06 [low] Duration chip over a bright frame is under 4.5:1 (3.96:1 on phone cards, 4.31:1 on the desktop stage)
- template: seeded71
- steps: wpt new <name> <port> seeded71 / Open http://127.0.0.1:<port>/ at 390x844, scroll to The creators (Maya's card), look at the '0:52' chip at the top right over the bright window / At 1440x900, scroll into story 1 and look at the stage's duration chip / Measure: hide the chip text and compute white-text contrast against the pixels behind it (durchip.mjs)
- expected: At least 4.5:1 for this 11-12px semibold text on any frame, as the handle chip now achieves (6.93:1 minimum).
- actual: Story 1: the median and worst pixels behind the '0:52' text give 3.96:1 on the 390 and 320 cards (all 3 frames) and 4.31:1 on the 1440 and 1024 stage. That is exactly the chip's colour over pure white: rgba(15,46,77,.6) over white is 3.98:1 and rgba(17,35,55,.6) is 4.31:1. Viewer chips measure 4.6-5.2:1. Same on v2. Not reported in round 1 (round 1 measured only the handle overlay).
- likely cause: style.css: .panel .pv .dur and .slide .fr .dur use background rgba(15,46,77,.6) (lines 255, 263), and the stage .vid .dur uses rgba(17,35,55,.6) (line 213). The fix raised .who to .78 but left the duration chip at .6; .78 gives 6.9:1 over white.
- evidence: /tmp/claude-0/wptest/work/r2-visitor/logs/durchip-r1.log, durchip-r2.log (SUMMARY lines), /tmp/claude-0/wptest/work/r2-visitor/durchip/dur-r1.json, /tmp/claude-0/wptest/work/r2-visitor/durchip/wp-390-card1-dur-zoom.png, wp-1440-stage1-dur-zoom.png

### VIS-N07 [low] Paused still uses the 300px 'medium' avatar size, so a real avatar is upscaled 3.7x to 6.4x and looks soft
- template: seeded71
- steps: wpt new <name> <port> seeded71 / Give a creator a large square avatar, e.g. wpt wp <name> media import <1080x1080.jpg> --post_id=17 --featured_image / Open the page with reduced motion (clips start paused) at 1440x900 with device scale 2, go to story 5; then at 390x844 with device scale 3, open card 5 in the viewer
- expected: The still is sharp at the size it is shown (the stage is 315x560 CSS px, the viewer frame 358x636).
- actual: The still is big-avatar-300x300.jpg (natural 300x300). It is drawn at 3.73x on the 2x desktop stage, 3.71x on the 3x phone card and 6.36x in the 3x viewer. A 12px stripe pattern in the test image turns visibly smeared. v2 uses the full portrait file (300x400 placeholder, 2.8x to 4.8x). The seeded placeholders use the 225x300 crop.
- likely cause: inc/creators.php line 373: 'portrait' => get_the_post_thumbnail_url( $id, 'medium' ), reused as data-still and the video poster (line 412). A larger size (medium_large, large or full) or a srcset would keep the still sharp.
- evidence: /tmp/claude-0/wptest/work/r2-visitor/logs/still-quality-r1.log, still-quality-r2.log, /tmp/claude-0/wptest/work/r2-visitor/still/crop-wp8512-1440-stage5-r1.png, /tmp/claude-0/wptest/work/r2-visitor/still/wp8512-390-viewer5-paused-r1.png

### VIS-N08 [info] The pulsing gold dot in the hero headline keeps animating when the clips are paused
- template: seeded71
- steps: wpt new <name> <port> seeded71 / Open http://127.0.0.1:<port>/ at 1440x900 without reduced motion, press the pause button, and list running animations (document.getAnimations())
- expected: Informational: the page's one infinite animation is either stopped by the visitor's pause or judged decorative and exempt.
- actual: The only infinite animation is 'pulse' on the headline dot (.lean h1 .d::after, 2.4s, infinite). The pause button stops only the clips. Reduced motion does turn it off (0 running animations under reduce). Same on v2.
- likely cause: style.css line 311: animation:pulse ... infinite, disabled only in @media (prefers-reduced-motion: reduce) (line 313).
- evidence: /tmp/claude-0/wptest/work/r2-visitor/logs/reduced-r1.log, reduced-r2.log ('wp no-preference infinite anims [pulse on d pulse::after]')

not tested: Screen reader speech (NVDA, VoiceOver, TalkBack): the aria-live announcement on story change (V05) and the pause button's spoken name and state were checked only in Chromium's accessibility tree.; Real iOS Safari and Android Chrome, including a real device rotation (the rotation finding used setViewportSize in Chromium) and iOS scroll locking.; Firefox and WebKit (only Playwright Chromium is installed).; H.264 MP4 playback: this Chromium has no proprietary codecs, so the video checks used the WebM sample.; measure.mjs and contrast.mjs for v2 ran on the local copy, which is byte-identical to the live page (cmp). The Playwright scripts loaded the live v2 URL.; Newsletter form and creators' social links (no Substack address or channels set on seeded71: expected placeholders).; Hero background video and CSS plates fallback (this build renders no hero video).; WordPress 6.5 and PHP 7.4 (compatibility tester's area); Lighthouse scores (performance tester's area).

## settings
retest: {'partly': 2, 'fixed': 7}; new findings: 5
- S01 [partly] Fixed for the newsletter and channel fields. http:// is saved as https://, 'Settings saved.' shows, and visitors keep the signup form and the Substack row. Every channel URL and Contact are upgraded the same way. A refused value (javascript:, data:, ftp:) shows a red notice: '"javascript:alert(1)" is not a web address, so the address saved before was kept.' The previous value stays in the field and in the option, and the page is unchanged. Through REST, http is stored as https, and javascript: returns 200 and keeps the old value. Still broken in one place: when the Contact link has never been changed from its default (a fresh site), a refused value wipes the default. The notice says the old address was kept, but the option becomes '' and the footer loses its Contact link. This is reported as a new finding.
  evidence: /tmp/claude-0/wptest/work/r2-settings/s01-a.json, /tmp/claude-0/wptest/work/r2-settings/s01-b.json, /tmp/claude-0/wptest/work/r2-settings/s01-a-http-subscribe.png
- S02 [partly] The S02 steps are fixed. With the long emails in the legal line and the fine print, scrollWidth equals the viewport at 320, 360 and 390 (the legal paragraph is 280 px wide at 320). Unbroken 300- and 2000-character legal lines and notes now wrap. The footer line beside the mark still does not wrap, though the brief named it too. 'Young Mainers on the rules that shape their lives. Write to generationmaineinformation@mainepolicyinstitute.org' makes the page 399 px wide at 320, 360 and 390, and the page can be scrolled sideways (screenshot). 300 unbroken characters in that line still give scrollWidth 2837, the same as round 1. The lede's computed overflow-wrap is 'normal'; the fix at style.css:362 covers only '.site .ffine p' and '.follow .fine'. At 1280 px, a 300-character unbroken handle still overflows its follow row (document 3447 px wide). Realistic handles fit.
  evidence: /tmp/claude-0/wptest/work/r2-settings/t2E-a-320-legal.png, /tmp/claude-0/wptest/work/r2-settings/s02-a-lede-320.png, /tmp/claude-0/wptest/work/r2-settings/s02-b-lede-390.png

### SET-N01 [medium] On a fresh site, a refused Contact link erases the default Contact link while the notice says the old address was kept
- template: seeded71
- steps: wpt new t 8515 seeded71; log in as admin/adminpass / Open the home page as a visitor: the footer shows 'Contact' linking to https://mainepolicy.org/contact/?utm_source=generationmaine&utm_medium=site / Settings > Generation Maine: the Contact link field shows the default https://mainepolicy.org/contact/. Replace it with mailto:info@mainepolicy.org (the browser accepts it as a URL) or javascript:alert(1), and click Save Changes / Read the red notice, the Contact link field, `wpt wp t option get gm_contact_url`, and the visitor's footer
- expected: The notice is true: the Contact link stays https://mainepolicy.org/contact/ and the footer keeps its Contact link
- actual: The red notice reads '"mailto:info@mainepolicy.org" is not a web address, so the address saved before was kept.' But the field is now empty, the option holds '', and visitors no longer see a Contact link. This was reproduced on two freshly built instances, with mailto: and with javascript:alert(1). Once Contact has been saved with a value other than the default, a refused value keeps it correctly.
- likely cause: generation-maine/inc/settings.php gm_clean_url() returns `(string) get_option( $key, '' )` on refusal. Saving the default value never creates the option row, because update_option sees no change from the registered default. Passing '' as the second argument to get_option overrides register_setting's default (https://mainepolicy.org/contact/), so '' is returned and stored. Calling get_option( $key ) without the second argument would keep the default. This was introduced by the round 1 fix for S01.
- evidence: /tmp/claude-0/wptest/work/r2-settings/s01c-a.json, /tmp/claude-0/wptest/work/r2-settings/s01c-b.json, /tmp/claude-0/wptest/work/r2-settings/s01c-b-field-after.png, /tmp/claude-0/wptest/work/r2-settings/s01-a.json (step refuse-contact-js: fieldAfter '', stored '')

### SET-N02 [low] A mailto: address is no longer accepted as the Contact link
- template: seeded71
- steps: wpt new t 8505 seeded71; Settings > Generation Maine: set Contact link to https://mainepolicy.org/contact-test/ and save / Change Contact link to mailto:info@mainepolicy.org and click Save Changes
- expected: As in round 1, where it was a passed check: mailto: is stored and the footer's Contact link opens an email. An email address is a normal target for 'Contact', and the field help ('Where "Contact" in the footer goes.') does not rule it out.
- actual: A red notice says '"mailto:info@mainepolicy.org" is not a web address, so the address saved before was kept.' The old https link remains. On a fresh site this also triggers the Contact wipe in the finding above. Seen in both matrix runs (case C3) and in both s01 runs.
- likely cause: generation-maine/inc/settings.php gm_clean_url() runs esc_url_raw( $value, array( 'https' ) ) for every URL field, gm_contact_url included. Contact could allow array( 'https', 'mailto' ), or the README and help could say that only web addresses are allowed. This is a regression from the round 1 passed check 'mailto: in Contact is stored and rendered as a mailto link without UTM'.
- evidence: /tmp/claude-0/wptest/work/r2-settings/t2-a.json (C3), /tmp/claude-0/wptest/work/r2-settings/t2-b.json (C3), /tmp/claude-0/wptest/work/r2-settings/s01-b.json (contact-mailto), /tmp/claude-0/wptest/work/r2-settings/s01-a-contact-mailto.png

### SET-N03 [low] A handle taken from an address uses the last part of the path, so a tab or video link shows the wrong handle
- template: seeded71
- steps: wpt new t 8505 seeded71; Settings > Generation Maine: clear Instagram, TikTok and YouTube handles / Set YouTube address to https://www.youtube.com/@generationmaine/videos (as copied from the channel's Videos tab), save, and open the home page as a visitor / Repeat with https://www.instagram.com/generationmaine/reels/, https://www.tiktok.com/@generationmaine/video/7312345678901234567, https://www.youtube.com/@GenerationMaine/featured and https://www.youtube.com/channel/UC1a2B3c4D5e6F7g8H9i0J
- expected: The row shows the account handle (@generationmaine), or falls back to a placeholder or the host when no handle can be found in the address
- actual: The rows show '@videos', '@reels', '@7312345678901234567', '@featured' and '@UC1a2B3c4D5e6F7g8H9i0J' as the handle, and visitors see them as live links. A plain profile address (/generationmaine/, /@generationmaine, ?hl=en) works. Reproduced on two instances.
- likely cause: generation-maine/inc/follow.php gm_handle_from_url() takes end( $seg ), the last path segment. Better: use the first segment that starts with @ (YouTube, TikTok), else the first segment (Instagram), skipping channel/c/user forms; or fall back to the placeholder. The flaw is in the new code added for S05.
- evidence: /tmp/claude-0/wptest/work/r2-settings/s05-a.json, /tmp/claude-0/wptest/work/r2-settings/s05-b.json, /tmp/claude-0/wptest/work/r2-settings/s05-b-tt-url-video.png, /tmp/claude-0/wptest/work/r2-settings/s05-a-yt-url-videos-tab.png

### SET-N04 [low] With a static front page and a posts page, the posts page gets the front page's title, description, canonical, og:url and Organization schema
- template: seeded71
- steps: wpt new t 8515 seeded71; create and publish a page named Blog / Settings > Reading: 'Your homepage displays' = A static page, Homepage = Sample Page, Posts page = Blog, Save Changes / curl -s http://127.0.0.1:8515/blog/ and read the head
- expected: The posts page has its own title and its own canonical and og:url (/blog/), or none, and no front-page description or Organization schema
- actual: /blog/ prints <title>Generation Maine: young Mainers on the rules that shape their lives</title>, the front-page meta description, <link rel="canonical" href="http://127.0.0.1:8515/">, og:url = the home URL, and the Organization JSON-LD. Search engines would treat /blog/ as a copy of the home page. Same on two fetches. README Install step 2 tells the client to keep 'Your latest posts', so a site that follows the README does not hit this. This was not caused by the round 1 fixes.
- likely cause: generation-maine/inc/seo.php uses `is_front_page() || is_home()` in both gm_document_title() and gm_seo_head(). is_home() is true on the posts page when a static front page is set. Using is_front_page() alone, or adding 'posts' === get_option( 'show_on_front' ), would scope these tags to the real front page.
- evidence: /tmp/claude-0/wptest/work/r2-settings/n5-blog-a.html, /tmp/claude-0/wptest/work/r2-settings/n5-blog-b.html, /tmp/claude-0/wptest/work/r2-settings/n5-reading-Sample Page.png

### SET-N05 [low] A Site Title with & or an apostrophe appears HTML-encoded in the Organization JSON-LD name
- template: seeded71
- steps: wpt new t 8505 seeded71; Settings > General: Site Title = Generation Maine & Friends' Hub, Save Changes / View the home page source and read the application/ld+json name
- expected: "name":"Generation Maine & Friends' Hub"
- actual: "name":"Generation Maine &amp; Friends&#039; Hub". JSON-LD is not HTML-decoded, so search engines read the entities literally. The <title>, og:site_name and og:title are correct, since HTML decodes them. Same on two fetches. The real name 'Generation Maine' is not affected.
- likely cause: generation-maine/inc/seo.php gm_seo() uses get_bloginfo( 'name' ), which returns the stored, HTML-escaped blogname. wp_json_encode keeps the entities. Wrapping it in html_entity_decode( ..., ENT_QUOTES, 'UTF-8' ) for the schema would fix it. This came with the round 1 change that reads the Site Title.
- evidence: /tmp/claude-0/wptest/work/r2-settings/s07-amp-a.html, /tmp/claude-0/wptest/work/r2-settings/s07-amp-b.html

not tested: Rank Math with a connected account (the wizard's account step was skipped).; SEOPress and All in One SEO.; Loading the real Substack page after submit (substack.com was stubbed; only the popup URL was checked).; Site Icon through the Customizer, and the crop step for a non-square image.; WordPress 6.5 (seeded65) and PHP 7.4. Settings were retested on 7.1.3 only; the compat tester covers the others.; The Contact default wipe through the REST API: it was confirmed through the settings form only, though it follows the same code path.; Multisite, where site admins lack unfiltered_html.

## creators (round 2 retest after fixes)
retest: {'fixed': 14, 'partly': 1}; new findings: 6
- X12 [partly] Picker route: the warning appears as soon as the clip is chosen ('This clip is larger than 10 MB…') and after reload ('This clip is 11.9 MB. Visitors download all of it…'). It hides when a smaller clip is chosen or Remove is clicked. 6.5 behaves the same. Round 1 route (link to a big upload): no warning anywhere, neither in Media > Add New nor in the meta box after Update and reload. The README says 'A clip over 10 MB gets a warning.' with no exception for links.
  evidence: /tmp/claude-0/wptest/work/r2-creators/logs/x12-priya-run1.txt, /tmp/claude-0/wptest/work/r2-creators/logs/x12-priya65-run1.txt, /tmp/claude-0/wptest/work/r2-creators/logs/x12-priya-small.txt

### CRE-N01 [medium] 'Place on the page' goes stale after the first Update: changing it back is ignored, and it overwrites WordPress's own Order on later saves
- template: seeded71 (also seeded65)
- steps: wpt new t1 <port> seeded71, log in as admin / Open Creators > Cole (Place 3), open the Meta Boxes drawer, set Place on the page to 20, click Update ('Post updated.'; menu_order is 20) / Without reloading, set Place back to 3 and click Update: 'Post updated.', but menu_order stays 20 and Cole is still last on the page. After a reload the field shows 20 / Second case: in one session set Place to 12, Update; then use the sidebar's Actions > Order and set 2 ('Order updated.', menu_order 2); edit the title and Update: menu_order goes back to 12 / On 6.5: set Place to 9, Update; then set Post Attributes > Order to 2 and Update. The sidebar shows 2 but menu_order stays 9. Changing both in one save also keeps the Place value while the sidebar shows the other
- expected: The value the editor last saved is what the page uses. Changing Place back to an earlier number works, and changing Order with WordPress's own control is not undone by the next Update.
- actual: Reproduced twice on each version. On 7.1: Cole 3→20→3 stayed 20 and Tyler 5→9→5 stayed 9. Actions > Order 1 and 2 were reverted to 20 and 12 on the next Update. On 6.5: Tyler 5→9→5 stayed 9, Sam 8→12→8 stayed 12, and the sidebar Order values 2 and 1 were overwritten by Place 9 and 11. The Order control works when Place is not touched in that session (control runs).
- likely cause: inc/creators.php lines 185 and 221-231: gm_creator_order saves gm_order only when it differs from the hidden gm_order_was field, and that field is printed once at page load. The block editor does not re-render meta boxes after a save, so gm_order_was keeps the load-time value. The box's own field also does not follow changes made with the core Order control or the REST save. Every later meta-box post compares against stale values. A fix is to update both inputs after each save from wp.data (core/editor menu_order), or to drive the field from the editor store instead of a separate POST value.
- evidence: /tmp/claude-0/wptest/work/r2-creators/logs/order71-back-run1.txt, /tmp/claude-0/wptest/work/r2-creators/logs/order71-back-run2.txt, /tmp/claude-0/wptest/work/r2-creators/logs/order71-run1.txt, /tmp/claude-0/wptest/work/r2-creators/logs/order71-run2.txt

### CRE-N02 [medium] Roster layout: PHP warning 'Undefined variable $town' on every tile without a link, and the tile is labeled 'Maya, , Maine' (regression from the Maine, Maine fix)
- template: seeded71
- steps: wpt new t2 <port> seeded71, log in / Pages > Add New Page, title 'Roster test', type /creators and press Enter, then in the block's Settings set Layout to 'Roster: a tile per creator, linking to their feeds'. Publish / Open the page and run wpt themelog t2 / Inspect a placeholder tile's aria-label
- expected: No PHP notices, and the tile reads 'Maya, Skowhegan, Maine' (or 'Maya, Maine' with no hometown), as before the fix.
- actual: Each placeholder tile, and each tile of a creator with no social link, logs 'PHP Warning: Undefined variable $town in …/inc/creators.php on line 449' on every render, in the editor preview too. Its aria-label is 'Maya, , Maine' and '@aroostook.county.potatoes, , Maine', so a screen reader loses the town. There were 40 warnings on c71 and 96 on s71 from a single page each. On a host that shows PHP warnings, the warning text would be printed into the page. Reproduced on two instances.
- likely cause: inc/creators.php line 449 (gm_render_roster). The fix renamed the local $town to $place (line 443) but the aria-label still concatenates $c['name'] . ', ' . $town . ', Maine'. It should use $place, for example esc_attr( $c['name'] . ', ' . $place ).
- evidence: /tmp/claude-0/wptest/work/r2-creators/logs/roster-run1.txt, /tmp/claude-0/wptest/work/r2-creators/logs/roster-run2.txt, /tmp/claude-0/wptest/work/r2-creators/logs/themelog-final.txt, /tmp/claude-0/wptest/work/r2-creators/shots/roster-page.png

### CRE-N03 [low] Placeholders seeded by theme 3.0.0 are invisible to the 3.1.0 seed cleanup: seed 0 removes none and a re-seed doubles them
- template: seeded71
- steps: wpt new t3 <port> seeded71 / Run the 3.0.0 seed script (git show 037d4f3:generation-maine/bin/seed-creators.php, with its creators-placeholder.json, copied to a work folder): wp eval-file <that file> 3 <media folder> / Run the 3.1.0 script from the theme: wp eval-file wp-content/themes/generation-maine/bin/seed-creators.php 0 / Then run it with 3
- expected: README: 'Run it with 0 to remove the creators the script made that are still placeholders.' A site seeded before the update gets its placeholders removed, or the README says how to remove them.
- actual: 'Success: Removed 0 placeholder creator(s) made by this script. Kept 6 seeded media item(s) that a creator still uses.' Maya, Devin and Priya from the 3.0.0 run stay on the page. A following seed 3 adds three more, so Maya, Devin and Priya appear twice. I reproduced this with the real 3.0.0 script, and once more by deleting gm_seeded from two 3.1.0-seeded creators, which matches what 3.0.0 left behind.
- likely cause: bin/seed-creators.php line 83 now selects creators by meta_key gm_seeded. The 3.0.0 script set gm_seeded only on attachments, and marked creators with gm_placeholder alone. Creators that have gm_placeholder, no gm_seeded, and the exact title, bio and handle of an entry in creators-placeholder.json (or that own a gm_seeded attachment as a child) could be treated as seeded. Or the README could tell existing sites to delete the old placeholders by hand.
- evidence: /tmp/claude-0/wptest/work/r2-creators/logs/seed71-upgrade-run2.txt, /tmp/claude-0/wptest/work/r2-creators/logs/seed71-upgrade-run1.txt, /tmp/claude-0/wptest/work/r2-creators/old-seed/seed-creators.php

### CRE-N04 [low] If a creator's chosen clip is deleted from the Media Library, the box shows a bare 'Remove' and a pasted clip link is ignored (navy field on the page)
- template: seeded71
- steps: wpt new t4 <port> seeded71, log in / Give a creator a clip with 'Choose or upload a clip' and Publish (Clip Pick Gif / Clip Pick New) / Media > Library (list view): Delete Permanently that file / Open the creator: next to 'Choose or upload a clip' there is only 'Remove' with no file name. Paste https://mchljns.github.io/Generation-Maine/v2/media/creator-4.gif into 'Or a clip link' and click Update / Open the front page
- expected: With no clip file left, the box shows no chosen clip and the link is used (or the box says the chosen clip is missing).
- actual: gm_clip_id still holds the deleted id (39, and 35 in the second run), the box shows 'Remove' with an empty name, and the card renders <div class="clip noclip"> although a link is saved. Reproduced on two creators.
- likely cause: inc/creators.php line 355: $clip = $clip_id ? wp_get_attachment_url( $clip_id ) : get_post_meta( …'gm_clip_url'… ). A non-zero id of a missing attachment returns false and never falls back to the link. The meta box prints Remove whenever $clip_id is non-zero (line 172). It would help to fall back when wp_get_attachment_url() returns false, and to treat a missing attachment as no clip in the box.
- evidence: /tmp/claude-0/wptest/work/r2-creators/shots/x-deleted-box.png, /tmp/claude-0/wptest/work/r2-creators/shots/x-deleted2-box.png, /tmp/claude-0/wptest/work/r2-creators/logs/x-deleted-front.txt

### CRE-N05 [low] When the title is the creator's handle and the Handle field is filled, the clip header shows the handle twice
- template: seeded71
- steps: wpt new t5 <port> seeded71, log in / Creators > Add creator: title '@aroostook.county.potatoes' (README step 2 allows the handle as the title), Handle '@aroostook.county.potatoes', a clip link, Publish / Open the page at 320 and 1440 and step to that creator; open the viewer at 320
- expected: The handle once, as the X09 fix does for a missing handle.
- actual: The header on the stage, the card and the viewer reads '@aroostook.county.potatoes / @aroostook.county.potatoes'. The same happens with '@thelongesthandleonthewholeinternetfrommaine'.
- likely cause: inc/creators.php line 392 (gm_who) prints the handle and then the name without checking whether they are the same. Compare them (case-insensitive, ignoring a leading @) and print one line when they match.
- evidence: /tmp/claude-0/wptest/work/r2-creators/logs/x03a-run1.json, /tmp/claude-0/wptest/work/r2-creators/logs/x03b-run1.json, /tmp/claude-0/wptest/work/r2-creators/shots/x03a-320.png

### CRE-N06 [low] Contributors get a working-looking 'Choose or upload a clip' button whose library is empty and whose uploads fail
- template: seeded71
- steps: wpt new t6 <port> seeded71; wpt wp t6 user create tcontributor c@x.test --role=contributor --user_pass=... / Log in as tcontributor, Creators > Add creator, open the Meta Boxes drawer, click 'Choose or upload a clip' / Open Media Library, then Upload files and pick sample-clip.webm
- expected: Like the avatar (core hides 'Set avatar' for contributors), the picker is hidden or replaced with a note, and the README mentions it.
- actual: The dialog 'Choose a clip' opens with an empty library. The upload fails with 'Sorry, you are not allowed to upload files.', and 'Use this clip' stays disabled. Reproduced twice. The README says only that contributors 'cannot set an avatar'.
- likely cause: inc/creators.php line 171 prints the picker button for everyone, and gm_creator_admin_assets enqueues the media frame without a current_user_can( 'upload_files' ) check. Wrap the button in that check (leaving the link field), and add the clip to the README's Contributor sentence.
- evidence: /tmp/claude-0/wptest/work/r2-creators/logs/contrib-clip-run1.txt, /tmp/claude-0/wptest/work/r2-creators/logs/contrib-clip-run2.txt, /tmp/claude-0/wptest/work/r2-creators/shots/x-contributor-clip-upload.png, /tmp/claude-0/wptest/work/r2-creators/logs/p17-roles.txt

not tested: MP4 (H.264) playback: Playwright's Chromium has no H.264 decoder, so the MP4 stays at readyState 0. Only its markup and the new poster were checked, and WebM playback was verified instead.; Real iOS Safari and Android (playsinline, autoplay, swiping the 24-creator progress bar with a finger). Only headless Chromium with mobile emulation was used; carousel swipes were simulated by scrolling the panels row.; Switching the Creators block to Roster in Appearance > Editor (Site Editor). The Roster regression was reproduced with the same block placed on a normal page and set to Roster in the block sidebar, plus wp eval of gm_render_creators.; Roles, the Place field with the Quick Edit Order, and the seed script on PHP 7.4 (the compat tester's Playground). Roles were not rerun on 6.5.; Running bin/seed-creators.sh. Only wp eval-file was used, as the README shows.; Whether 'Place' (a sort number starting at 0 for the seeded creators) confuses editors, since the page counts positions from 01. I noted it but did not report it; the README describes the field as a sort order.

## security
retest: {}; new findings: 7

### SEC-N01 [medium] Saving a creator in the editor makes whoever saved it the creator's author, so an Author loses edit access to their own creator
- template: seeded71
- steps: wpt new <name> <port> seeded71, then add an Author user (wpt wp <name> user create author a@example.test --role=author --user_pass=authorpass) / Log in as the Author. Go to Creators > Add creator, type a name, set Hometown in the Creator details box and click Publish. WP-CLI shows post_author = the Author's ID / Log in as admin, open that creator, change Hometown in the Creator details box and click Save / Read post_author with WP-CLI: it is now 1 (admin) / Log in as the Author and open the creator again
- expected: The creator keeps its author. The Author can still edit the creator they made after an administrator fixes a field.
- actual: After the admin's save, post_author goes from 3 to 1. The Author then gets HTTP 403 'Sorry, you are not allowed to edit this item.', and the creator has no row actions in their list. The same happens with no post lock involved: seeded creators 8 and 11 went from author 0 to 1 after a plain admin save. A Contributor's pending creator becomes the admin's when the admin publishes it (post 34 and post 70: author 2 to 1). Creators have no Author panel, so there is no screen to put it back.
- likely cause: The gm_creator type does not support 'author' (inc/creators.php:62). The theme's Creator details meta box (inc/creators.php:124) makes the block editor post the meta box form after each save, and that form carries no post_author for a type without author support (metaBoxPostHasAuthor=false in the evidence). Core's _wp_translate_postdata (wp-admin/includes/post.php:79-86) then sets post_author to the current user. Minimal fix, either one: add 'author' to supports at inc/creators.php:62, so the editor sends the author and shows an Author panel; or print <input type="hidden" name="post_author" value="(int) $post->post_author"> for gm_creator from the 'block_editor_meta_box_hidden_fields' action.
- evidence: /tmp/claude-0/wptest/work/r2-security/t2/author-owner-1.json, /tmp/claude-0/wptest/work/r2-security/t2/author-owner-2.json, /tmp/claude-0/wptest/work/r2-security/t2/owner-nolock-1.json, /tmp/claude-0/wptest/work/r2-security/t2/owner-nolock-2.json

### SEC-N02 [low] A refused Contact link on a fresh site deletes the default Contact link, while the notice says the old address was kept
- template: seeded71
- steps: wpt new <name> <port> seeded71. gm_contact_url has never been saved, and the footer shows Contact linking to https://mainepolicy.org/contact/ / Open Settings > Generation Maine as admin. The Contact link field shows https://mainepolicy.org/contact/ / Replace it with mailto:info@mainepolicy.org (or any address that is not https) and click Save Changes / Read the notice, the field, `wpt wp <name> option get gm_contact_url`, and the footer
- expected: The address is refused and the previous address (the default) stays, as the notice says.
- actual: The notice reads '"mailto:info@mainepolicy.org" is not a web address, so the address saved before was kept.' But the field is now empty, the stored option is '', and the footer's Contact link is gone. A data: URL does the same. A mailto: Contact link, which a client may well want, is refused because the field takes https only.
- likely cause: inc/settings.php:159 returns (string) get_option( $key, '' ). Passing '' explicitly overrides the default given to register_setting (inc/settings.php:84), so a first save that is refused stores ''. Minimal fix: return (string) get_option( $key ); at inc/settings.php:159, which uses the registered default. Optionally allow mailto: for gm_contact_url, or say 'https only' in the field help.
- evidence: /tmp/claude-0/wptest/work/r2-security/t2/contact-1.json, /tmp/claude-0/wptest/work/r2-security/t2/contact-2.json, /tmp/claude-0/wptest/work/r2-security/t2/settings-ui-1.json (data: URL refused, footerLinks has no Contact), /tmp/claude-0/wptest/work/r2-security/t2/settings-ui-2.json

### SEC-N03 [low] JSON-LD Organization name shows HTML entities when the Site Title has an ampersand or apostrophe
- template: seeded71
- steps: Settings > General: set Site Title to Generation & Maine's Youth and save / View the front page source and parse the application/ld+json script
- expected: "name":"Generation & Maine's Youth"
- actual: "name":"Generation &amp; Maine&#039;s Youth". Search engines read the name literally. og:site_name and <title> are correct. No breakout: with </script><i data-gmprobe> in the Site Title, and with a raw stored channel address holding </script>, JSON_HEX_TAG kept the script whole and the JSON parsed.
- likely cause: inc/seo.php:98 takes get_bloginfo('name'), which WordPress stores HTML-escaped (sanitize_option for blogname). The JSON-LD at inc/seo.php:180 and 193 encodes it unchanged. Minimal fix: 'name' => wp_specialchars_decode( $s['name'], ENT_QUOTES ) at inc/seo.php:180. JSON_HEX_TAG keeps it safe.
- evidence: /tmp/claude-0/wptest/work/r2-security/t2/ldname-1.json, /tmp/claude-0/wptest/work/r2-security/t2/ldname-2.json, /tmp/claude-0/wptest/work/r2-security/t2/ld-1.json, /tmp/claude-0/wptest/work/r2-security/t2/ld-2.json

### SEC-N04 [low] Roster layout: undefined $town logs a PHP warning for every placeholder tile and gives the wrong aria-label
- template: seeded71
- steps: Put the Creators block with the Roster layout, or [gm_creators layout="roster"], in a post or page / View it, then check wpt themelog <name>
- expected: Each tile without a link is labelled with its name and town, for example 'Maya, Skowhegan, Maine', and nothing is logged.
- actual: Each such tile is <div class="tile" aria-label="Maya, , Maine"> while its visible text reads 'Skowhegan, Maine'. All nine seeded placeholders render this way. debug.log gets 'PHP Warning: Undefined variable $town in .../inc/creators.php on line 449' once per tile per view (48 lines over two runs).
- likely cause: gm_render_roster() builds $place (inc/creators.php:437) but line 449 uses $town, which only exists in gm_render_creators(). Fix at inc/creators.php:449: esc_attr( $c['name'] . ', ' . $place ).
- evidence: /tmp/claude-0/wptest/work/r2-security/t2/contrib-content-1.json (tiles), /tmp/claude-0/wptest/work/r2-security/t2/contrib-content-2.json, /tmp/claude-0/wptest/work/r2-security/t2/contrib-content-render-2.html, /tmp/claude-0/wptest/work/r2-security/t2/debug-final.log

### SEC-N05 [low] A gold-word heading with a long run of spaces, line breaks or &nbsp; disappears from the page
- template: seeded71
- steps: As a Contributor, write a post in the code editor with a heading block with className gm-here whose text is 'Alpha', then 9000 spaces, then 'Omega here.' Add a second gm-here heading as a control / Save a draft and preview it as admin, at desktop and phone width / Check wpt themelog <name>
- expected: The heading renders with its last word in gold, or at worst unchanged.
- actual: The heading is missing from the page; only the control heading renders. debug.log: 'preg_replace_callback(): Passing null to parameter #3 ($subject) ... functions.php on line 146'. The earlier bench puts the threshold at 8192 repeats of space, newline, <br> or &nbsp; (JIT stack limit exhausted). Content is lost; no markup injection.
- likely cause: functions.php:143 assigns preg_replace()'s result to $html without checking it. On a PCRE failure that result is null, and line 146 then turns null into ''. Minimal fix: $t = preg_replace( ... ); if ( null !== $t ) { $html = $t; } at functions.php:143, and return the original $html when preg_replace_callback at line 146 returns null.
- evidence: /tmp/claude-0/wptest/work/r2-security/t2/longgap-1.json, /tmp/claude-0/wptest/work/r2-security/t2/longgap-2.json, /tmp/claude-0/wptest/work/r2-security/t2/longgap-render-2.html, /tmp/claude-0/wptest/work/r2-security/t2/debug-final.log

### SEC-N06 [low] The front-page <title> from the documented gm_seo filter is printed unescaped
- template: seeded71
- steps: On your own instance, add an mu-plugin: add_filter( 'gm_seo', function ( $s ) { $s['title'] = 'Q&A </title><i data-gmprobe="seo">x</i>'; return $s; } ); / Load the front page as a visitor
- expected: The title is escaped like og:title and the description, so the value stays text.
- actual: The source shows <title>Q&A </title> and then a real <i data-gmprobe="seo"> element in the document. og:title and meta description from the same filter are escaped. With stock data this is safe, because WordPress stores the Site Title escaped; the only path is the gm_seo filter that the file header points developers to.
- likely cause: gm_document_title() (inc/seo.php:133) returns gm_seo()['title'] from pre_get_document_title. A non-empty value there makes wp_get_document_title() return early, skipping its own esc_html. Fix at inc/seo.php:133: return esc_html( gm_seo()['title'] ); (esc_html does not double-encode the stored &amp;).
- evidence: /tmp/claude-0/wptest/work/r2-security/t2/seo-filter-1.json, /tmp/claude-0/wptest/work/r2-security/t2/seo-filter-2.json

### SEC-N07 [info] Three pattern files return HTTP 500 with a PHP fatal when requested directly
- template: seeded71
- steps: curl http://<host>/wp-content/themes/generation-maine/patterns/about.php, also patterns/not-found.php and patterns/no-results.php / Check the PHP server log
- expected: A quiet empty response, like functions.php, inc/*.php, blocks/*/render.php and bin/seed-creators.php, which all return 200 with 0 bytes through their ABSPATH guard.
- actual: HTTP 500 with partial block markup. Server log: 'PHP Fatal error: Uncaught Error: Call to undefined function esc_url() in .../patterns/about.php:16', and esc_html_e() in not-found.php:13 and no-results.php:13. On a host with display_errors on, the fatal prints the server path.
- likely cause: The pattern files call WordPress functions but have no direct-access guard. Add if ( ! defined( 'ABSPATH' ) ) { exit; } after the header docblock and before ?> in patterns/about.php (line 10), patterns/not-found.php (line 11) and patterns/no-results.php (line 11). The other patterns are pure markup and harmless.
- evidence: /tmp/claude-0/wptest/work/r2-security/t2/direct-access-1.txt, /tmp/claude-0/wptest/work/r2-security/t2/direct-access-2.txt, /tmp/claude-0/wptest/work/r2-security/t2/server-fatals.txt

not tested: Multisite, where administrators lack unfiltered_html, so the header part and settings go through kses; Editor role (only Contributor, Author and Administrator); Header customization through the Site Editor UI: the customized header part was set up with WP-CLI as the admin, holding what the Site Editor would save; The Latest Newsletter Posts block's feed fetch (no real Substack address configured, by the rules), and the block-renderer REST endpoint called directly; PHP 7.4 and WordPress 6.5 (the compat tester's area); Mixed content from an http: clip link on an HTTPS site (local sites are http). The clip link field accepts http:, as esc_url_raw allows it.; The classic editor, and Quick Edit of creators

## compat (retest after fixes)
retest: {'fixed': 6, 'partly': 2, 'not_fixed': 1}; new findings: 4
- C05 [partly] style.css now says Version 3.1.0, Tested up to: 7.1, Requires at least 6.5, Requires PHP 7.4. theme.json $schema is wp/7.1. README.md line 31 (source and zip) still says 'Tested on WordPress 7.2 (alpha) with PHP 8.4', so README and header still disagree. This round passed on 6.5.13 and 7.1.3 with PHP 8.4, and on 6.5.13 and 7.1.3 with PHP 7.4.33.
  evidence: /tmp/claude-0/wptest/work/r2-compat/zipx/generation-maine/style.css, /tmp/claude-0/wptest/work/r2-compat/zipx/generation-maine/README.md (line 31)
- C06 [not_fixed] This was left as is and is still harmless. version is still 3 while Requires at least is 6.5, and the README does not mention it. Against the 6.5 schema there are now 3 errors: version 3, settings.typography.defaultFontSizes, and settings.color.caption, which is new in 3.1.0. Against trunk and 7.1 there are 0 errors. On 6.5 there is still no visible effect:
- Styles has no Colors entry.
- Effective fontSizes is [] with no font size picker.
- The palette is the theme's 5 colors with custom colors off.
- The 6.5 and 7.1 front pages are pixel-identical (0 px at 1440 and at 390).
  evidence: /tmp/claude-0/wptest/work/r2-compat/schema/validate.txt, /tmp/claude-0/wptest/work/r2-compat/styles/wp65-styles.json, /tmp/claude-0/wptest/work/r2-compat/fontsize/wp65-inspector.png
- C08 [partly] Theme Check still reports:
- REQUIRED: no readme.txt
- REQUIRED: seed-creators.sh shell script
- REQUIRED: favicon.ico
- WARNING: no copyright notice
- INFO: no Tags
The README now covers the seed script (bin/ and the Placeholder creators section) and the favicon ('The theme ships a favicon either way'). The one actionable suggestion, a copyright line in style.css or the README, was not added. readme.txt is not needed for a private theme. None of this affects the client site.
  evidence: /tmp/claude-0/wptest/work/r2-compat/themecheck/wp71-run1-themecheck.txt, /tmp/claude-0/wptest/work/r2-compat/themecheck/wp65-run1-themecheck.txt

### COM-N01 [medium] Roster layout uses an undefined $town: a PHP warning (notice on 7.4) for every tile and an aria-label like 'Maya, , Maine'
- template: seeded71 and seeded65 (also pg74 and PHP 7.4 + WP 7.1.3)
- steps: wpt new t71 <port> seeded71, log in as admin / adminpass / Pages > Add New, type a title, press Enter, type /Creators and press Enter / In the block sidebar set Layout to 'Roster', then Publish / Open the page as a logged-out visitor / Run wpt themelog t71, and inspect a tile's aria-label
- expected: The roster renders without PHP warnings, and each placeholder tile's label names the town, for example 'Maya, Skowhegan, Maine'. This is what round 1 rendered.
- actual: Every tile logs 'PHP Warning: Undefined variable $town in .../inc/creators.php on line 449' on PHP 8.4 under WP 7.1.3 and 6.5.13: 36 lines after the 7.1 run and 27 after the 6.5 run, 45 per instance by the end. On PHP 7.4.33 it logs 'PHP Notice: Undefined variable: town' under WP 6.5 (pg74) and under WP 7.1.3 (9483), when the block renderer REST route draws the roster. Every placeholder tile gets aria-label 'Maya, , Maine', 'Priya, , Maine' and so on in the editor canvas and on the front end, while the visible caption is correct ('Compatville, Maine'). With WP_DEBUG_DISPLAY on, the warnings would print into the page. Reproduced on 7.1 (8506) and 6.5 (8516) through the UI, and on both PHP 7.4 sites.
- likely cause: inc/creators.php gm_render_roster(): the 'No Maine, Maine' fix renamed the local variable to $place (line 437, '%s, Maine'), but line 449 still builds the tile label from the old variable: esc_attr( $c['name'] . ', ' . $town . ', Maine' ). Round 1 defined $town in this function. Use $c['name'] . ', ' . $place, or the town itself.
- evidence: /tmp/claude-0/wptest/work/r2-compat/roster/wp71-run1-roster.json, /tmp/claude-0/wptest/work/r2-compat/roster/r2c71-themelog-run1.txt, /tmp/claude-0/wptest/work/r2-compat/roster/wp65-run2-roster.json, /tmp/claude-0/wptest/work/r2-compat/roster/r2c65-themelog-run2.txt

### COM-N02 [low] Place on the page: changing the number back to its original value in the same editing session is silently dropped
- template: seeded71 and seeded65
- steps: wpt new t71 <port> seeded71, log in, Creators > Jess (Place 4) / Open the Meta Boxes drawer, set Place on the page to 6, click Save ('Post updated.') / Without reloading, set Place on the page back to 4 and click Save again / Reload the editor, then look at the Creators list and the front page
- expected: Jess is back at 4, matching what the box showed when the editor saved.
- actual: The second save is ignored: the box shows 6 after reload, WP-CLI menu_order is 6, and the list and page order keep Jess at 6. On 6.5 the second save even shows 'Post updated.'. The captured meta box POST on the second save carries gm_order=5&gm_order_was=5 (Tyler run) or gm_order=4&gm_order_was=4 (Jess run). Reproduced twice on 7.1.3 (Jess 4>6>4, Tyler 5>9>5) and twice on 6.5.13 (same two). Control: a second change to a new value (Amara 6>10>3) is saved (3).
- likely cause: inc/creators.php line 185 prints a hidden gm_order_was with the menu_order at page load. The block editor saves meta boxes in the background and never re-renders the box, so gm_order_was stays at the load-time value. gm_creator_order() (line 229) only writes menu_order when gm_order differs from gm_order_was, so returning to the load-time number looks like 'no change'. Fix: after each successful save, have a small script copy the field's value into gm_order_was (subscribe to core/editor isSavingPost), or set a 'changed' flag on input instead of comparing values.
- evidence: /tmp/claude-0/wptest/work/r2-compat/order/wp71-boxtwice-run1-order.json, /tmp/claude-0/wptest/work/r2-compat/order/wp71-boxtwice-run2-order.json, /tmp/claude-0/wptest/work/r2-compat/order/wp65-boxtwice-run1-order.json, /tmp/claude-0/wptest/work/r2-compat/order/wp65-boxtwice-run2-order.json

### COM-N03 [low] WP 7.1: once Creator details is opened, the Meta Boxes drawer fills the editor and hides the Title, also on every next Add creator
- template: seeded71
- steps: wpt new t71 <port> seeded71, log in as admin (fresh user preferences) / Creators > Add creator: 'Add title' and the story are visible, and the Meta Boxes bar is collapsed at the bottom / Click the Meta Boxes bar to reach Creator details (README step 5) / Open Creators > Add creator again
- expected: The title field stays reachable while Creator details is open, or the README says how to get back to it.
- actual: After the click the drawer spans top 96 to 967 and the editor canvas is 0 px tall: no title and no story are visible. The open state persists, so the next Add creator also opens with the canvas at 0 px and 'Add title' hidden until the drawer is collapsed or dragged down. Reproduced twice, with user preferences reset before each run. The earlier run's automation also had to collapse the drawer to reach the title (p74latest/extra.log: collapsedDrawerToReachTitle true).
- likely cause: In core WP 7.x (MetaBoxesMain in wp-includes/js/dist/edit-post.js), the pane opens at 'auto' height when no height is stored. The theme's Creator details box is about 870 px tall, so it takes the whole editor. Options: a README line ('click Meta Boxes to close the drawer, or drag its handle, to get back to the title'), or a shorter box with the links and clip fields grouped or moved to the sidebar.
- evidence: /tmp/claude-0/wptest/work/r2-compat/drawer/drawer.log, /tmp/claude-0/wptest/work/r2-compat/drawer/d71-run1-first-open.png, /tmp/claude-0/wptest/work/r2-compat/drawer/d71-run1-after-click-meta-boxes.png, /tmp/claude-0/wptest/work/r2-compat/drawer/d71-run2-next-add-creator.png

### COM-N04 [low] Site Editor Mobile preview: bar labels spill out of the navy bar (worst on 6.5) and the Get the newsletter button disappears
- template: seeded65 and seeded71
- steps: wpt new t65 <port> seeded65, log in / Open Site Editor > Front Page template (edit) and close the guide / Use the device preview dropdown and choose Mobile / Look at the bar
- expected: In a narrow canvas the bar keeps its labels inside the 68 px bar (or shows the phone bar as the front end does), with the button visible. The front end at 390 is correct.
- actual: WP 6.5.13 (358 px canvas): the three labels stack vertically. About sits above the top edge, at y -41 to -1, so it cannot be seen. Follow drops below the bar onto the hero (y 68 to 108) and covers the 'A Maine Policy Institute project' kicker (y 100). The Get the newsletter button is display:none, and the phone menu button is hidden too. WP 7.1.3 (479 px canvas): About and Creators are clipped 14 px at the top, Follow wraps below them, and the button is hidden. Reproduced on two 6.5 instances (8526, 8516) and twice on 7.1 (8506).
- likely cause: assets/css/editor.css now keeps the desktop nav labels visible and hides the menu button at every canvas width, so editors can reach the labels (round 1 E16). Nothing lets the labels wrap inside, or the bar grow past, its fixed 68 px height, and the CTA is hidden below the phone breakpoint. 6.5's 358 px Mobile canvas makes the overflow worse than 7.1's.
- evidence: /tmp/claude-0/wptest/work/r2-compat/semobile/wp65-run1-se-mobile.png, /tmp/claude-0/wptest/work/r2-compat/semobile/wp65-run2-se-mobile.png, /tmp/claude-0/wptest/work/r2-compat/semobile/wp71-run1-se-mobile.png, /tmp/claude-0/wptest/work/r2-compat/semobile/semobile.log

not tested: WebKit and Firefox: /opt/pw-browsers has only Chromium builds and playwright install is forbidden, so Safari and Firefox behavior of the carousel, viewer, pause control and scroll snapping is still unverified.; A real Apache or nginx subdirectory or multisite-path install: simulated with WP_HOME and WP_SITEURL set to /gm plus a symlink, because php -S serves only a document root.; The same-session revert of Place on the page was not run on PHP 7.4. The code path is version-independent, and the plain box change was verified there.; Theme Check was not run on PHP 7.4 (it was run on 6.5.13 and 7.1.3 with PHP 8.4).; Live Preview from the upload result page on WP 7.1 (install was tested on 6.5 only, where the result page has no Live Preview link; the theme card's Live Preview worked).; Stopping pg74 completely: pg74 stop left its node server (pid 443, port 9474) running. I did not start it, so I left it for the main session.

## perf
retest: {}; new findings: 12

### PER-N01 [medium] The about photo loads early at Medium priority: Lighthouse mobile LCP is 5.18 s against 2.93 s on v2 (score 79 against 90)
- template: seeded71
- steps: wpt new r2perf 8508 seeded71; serve the v2 copy on 8518 / Run /tmp/claude-0/wptest/work/r2-perf/run-lh.sh twice (sets lh-a and lh-b): 3 mobile and 3 desktop runs on each page, interleaved / Compare the about image markup: grep -o '<img[^>]*about.jpg[^>]*>' on both front pages / Network inventory: node net.mjs at 390x844 and 1440x900, two runs each, and read the priority of about.jpg / Experiment: run-lh-exp.sh mobile and desktop with ?exp=0 against ?exp=about. The test-only render_block filter in perf-exp.php gives the about img width=1200 height=1600 loading=lazy decoding=async, as v2 has / Applied throttling: run-lh-dt.sh (v2, WP ?exp=0, WP ?exp=about), 3 runs each / Library replacement: import about.jpg to the Media Library and use ?exp=lib (perf-exp-lib.php rewrites the img as the editor saves a library image, class wp-image-32), then run net.mjs twice
- expected: As on v2, `<img src="media/about.jpg" ... width="1200" height="1600" loading="lazy">`. The below-the-fold photo should be fetched at Low priority after layout, and the mobile Lighthouse LCP and score should be in line with v2.
- actual: WordPress prints `<img src=".../assets/img/about.jpg" alt="Lisbon Street, Lewiston, Maine"/>` with no width, height or loading. On every run (4 inventories, 24 Lighthouse traces) Chrome fetches the 247,998-byte photo at Medium priority, at the same moment as style.css and the preloaded fonts (89 to 133 ms). On v2 it is Low priority. Lighthouse medians, set A and set B:
- Mobile: score 79 and 79 (v2 90 and 90); LCP 5176 and 5177 ms (v2 2937 and 2927); FCP 2101 and 2101 ms (v2 2759 and 2760).
- Desktop: score 99 and 99 (v2 100 and 100); LCP 1021 and 1041 ms (v2 580 and 582).
- The LCP element is the hero lede paragraph on both pages.

With only the about img fixed (?exp=about): mobile LCP 3526 ms and score 89 (baseline in the same set: 5265 ms, 78); desktop LCP 800 ms (baseline 1040). Under applied throttling, WordPress already beats v2 (LCP 3622 ms against 4202, score 87 against 81), and the fix still saves about 260 ms (LCP 3362, FCP 2084 against 2343).

Replacing the photo through the Media Library does not fix it. Core adds width, height and srcset but no loading attribute, and the image stays Medium priority (2 of 2 runs).
- likely cause: The img in patterns/about.php has no width, height or loading attribute. Core never adds loading attributes to images placed directly in a block template: wp_get_loading_optimization_attributes() returns early for the 'template' context (wp-includes/media.php around line 6178). Without an explicit attribute, Chrome's boost for the first large images gives the photo Medium priority, and Lighthouse's simulation then counts its 248 KB as part of the path to LCP. Suggested fix: add a render_block_core/image filter in the theme (WP_HTML_Tag_Processor) that sets loading="lazy", decoding="async", and width and height when they are missing, using getimagesize() for theme assets. This keeps working after a client swaps the photo in the editor. Writing raw attributes into the pattern's block markup might fail block validation in the editor. The photo also has no srcset: a 1200x1600 file is shown at 350x263 on a phone and 460x613 at 1440, and Lighthouse estimates 202 to 206 KiB of savings (the same on v2).
- evidence: /tmp/claude-0/wptest/work/r2-perf/lh-a/summary.txt, /tmp/claude-0/wptest/work/r2-perf/lh-b/summary.txt, /tmp/claude-0/wptest/work/r2-perf/lh-exp-m/summary.txt (wp_0 and wp_about), /tmp/claude-0/wptest/work/r2-perf/lh-exp-d/summary.txt

### PER-N02 [low] The lede's face (DM Sans) is not preloaded, so it is requested 25 to 75 ms after the other fonts; preloading it cuts simulated mobile FCP by about 400 ms
- template: seeded71
- steps: Load the front page at 390x844 (net.mjs, 2 runs), read the request start times and getComputedStyle of .lede, h1, .k and the hero button / Run run-lh-exp.sh mobile with ?exp=about against ?exp=about,preloaddm (3 runs each). preloaddm adds a font preload for dm-sans-var.ttf
- expected: Every face the first screen uses arrives without a discovery delay, as on v2, where all faces are in the first response.
- actual: gm_preload_fonts() preloads Bricolage (h1) and Michroma (.k and buttons) only. The hero lede, which is the mobile LCP element, uses DM Sans (computed font-family checked on both pages). DM Sans is found only after style.css and the head's wp-fonts-local style are parsed. It starts at 116, 122 and 133 ms against 88 to 105 ms for the preloads in the inventories, and at 207 against 132 ms in the Lighthouse trace. Simulated mobile FCP with the about fix: 2101 ms, 1693 ms with DM Sans preloaded (runs 1763, 1693, 1606). LCP is unchanged (3526 against 3530). The earlier attempt measured 2160 to 1661 ms.
- likely cause: The preload list predates the lede being the LCP element. The first screen uses three faces, not two. Fix: add assets/fonts/dm-sans-var.ttf to gm_preload_fonts(), or preferably a WOFF2 version (see the font format finding).
- evidence: /tmp/claude-0/wptest/work/r2-perf/lh-exp-m/summary.txt (wp_about against wp_about+preloaddm), /tmp/claude-0/wptest/work/r2-perf-cutoff2/lh-exp/summary.txt, /tmp/claude-0/wptest/work/r2-perf/net/wp-390x844-r1.json and r2.json (atLoad.res start times), /tmp/claude-0/wptest/work/r2-perf/lh-a/wp-mobile-1.report.json (network-requests)

### PER-N03 [low] DM Sans and Michroma ship as TTF: 165 KB where WOFF2 would be 70 KB
- template: seeded71
- steps: Network inventory at 390 and 1440 (net.mjs): read the font transfer sizes / Convert assets/fonts/dm-sans-var.ttf and michroma-regular.ttf with fontTools (flavor woff2) into /tmp/claude-0/wptest/work/r2-perf/woff2/
- expected: Self-hosted fonts in WOFF2, like the Bricolage face the theme already ships as woff2.
- actual: dm-sans-var.ttf is 100,672 bytes (100,817 on the wire) and michroma-regular.ttf is 64,344 bytes (64,488 on the wire), and both are fetched on every first view. As WOFF2 they are 43,940 and 26,464 bytes, 94.6 KB less (57%). Even gzip only reaches 54,308 and 33,635. This is not a regression against v2, which inlines the same TTFs as base64 (larger still), but it is avoidable.
- likely cause: The fonts were copied from the v2 build as TTF. Fix: ship WOFF2 files, point the theme.json fontFace src at them, and preload them with type font/woff2.
- evidence: /tmp/claude-0/wptest/work/r2-perf/woff2/ (converted files), /tmp/claude-0/wptest/work/r2-perf/net/tables.txt, /tmp/claude-0/wptest/work/r2-perf-cutoff2/woff2/ (earlier conversion, same result within 1%)

### PER-N04 [low] The creators block runs 36 single-row queries for portraits and clips (41 queries, about 19 ms); priming the caches brings the page from 69 to 35 queries
- template: seeded71
- steps: With perf-stats.php in my instance, request the front page 10 times and read the per-block timings / Request /?qlog=front (perf-qlog.php, SAVEQUERIES) and group the queries by caller / Compare ?exp=0 with ?exp=prime, 10 requests each, twice. prime calls _prime_post_caches() on the creators' thumbnail and clip attachment ids, in a the_posts filter, test only / Diff the markup with and without prime
- expected: A fixed, small number of queries for the roster, whatever the number of creators.
- actual: The query log shows that gm_get_creators() calls wp_get_attachment_url() for each clip and get_the_post_thumbnail_url() twice for each portrait. Each call costs one `SELECT * FROM wp_posts WHERE ID = n` and one postmeta query, so 9 creators cost 36 queries, 4 per creator. The creators block measures 17.45 ms and 41 queries (median of 10), or 18.77 and 19.45 ms in the two sets. With priming it measures 7.36 and 7.21 ms with 7 queries. The whole page goes from 69 to 35 queries, and PHP time from a median of 81.1 and 72.4 ms to 59.8 and 61.5 ms. The markup is byte-identical with and without priming.
- likely cause: The WP_Query primes the creators' own meta but not their attachments. Fix: after the query, call update_post_thumbnail_cache( $query ), and prime the gm_clip_id attachments with _prime_post_caches( $ids, false, true ), or one get_posts( post__in ) call with the meta cache on.
- evidence: /tmp/claude-0/wptest/work/r2-perf/qlog-front.json, /tmp/claude-0/wptest/work/r2-perf/prime-cost.txt, /tmp/claude-0/wptest/work/r2-perf/blocks-cost-all.txt, /tmp/claude-0/wptest/work/r2-perf/perf-exp.php (prime experiment)

### PER-N05 [low] The inline mural JSON (6.2 KB) is still printed, although the mural is drawn on the server; the script uses only its stagger value
- template: seeded71
- steps: Compare the front page HTML with ?exp=0 and with ?exp=nojson (perf-exp.php removes gm_mural_data) / Run mural-check.mjs twice at 1440 and 390: path count, transition delays, the 'on' class and console errors, with and without the JSON / Read assets/js/site.js lines 8 to 21
- expected: Since the server draws the mural, the page carries the geometry once, in the SVG.
- actual: `<script id="maine-data" type="application/json">` prints all 6,215 bytes of mural.json: a 5,414-character clip path and 17 lines. The same geometry is already in the server-drawn SVG. site.js skips building the SVG when one exists and reads only d.stagger, which is 90. Without the JSON the HTML drops from 96,743 to 90,469 bytes, and the mural still draws with the same 17 paths, the 'on' class and no errors. But the desktop stagger falls from 90 ms to the script's default of 35 ms. At 390 it is 35 ms either way.
- likely cause: gm_mural_data() was kept from when the script drew the mural. Fix: when gm_part_mural() has drawn the SVG, print only {"stagger":90}, or put data-stagger on #mural and drop the script tag. Removing the JSON outright would change the desktop animation timing.
- evidence: /tmp/claude-0/wptest/work/r2-perf/exp-0.html and exp-nojson.html, /tmp/claude-0/wptest/work/r2-perf/mural-check.txt, /home/user/Generation-Maine/generation-maine/functions.php gm_mural_data(), /home/user/Generation-Maine/generation-maine/inc/parts.php gm_part_mural()

### PER-N06 [low] Paused and reduced-motion stills use the 225x300 portrait size but are shown at up to 315x560 CSS px (smaller than displayed)
- template: seeded71
- steps: Run REDUCE=1 node net.mjs at 390x844 on both pages, twice / Compare the natural and rendered size of the visible .clip stills
- expected: A still at least as sharp as v2's and close to its displayed size at common pixel ratios.
- actual: gm_get_creators() uses get_the_post_thumbnail_url( $id, 'medium' ) for data-still. Medium caps at 300 px, so the stills are 225x300. At 390 they render at 304x371 CSS px, which is 912x1113 device px on a 3x phone, and at 1440 the stage clip is 315x560. On v2 the stills are 300x400. Data at open is fine (WordPress 639,265 bytes against v2's 707,698 with reduced motion), and no portrait is larger than displayed. The issue is the opposite: with real uploaded portraits the still will look soft.
- likely cause: 'medium' was chosen for weight. Suggested fix: use 'medium_large' (768w) or 'large' for data-still and the video poster. Only the current card and the next one load a still, so the extra bytes are bounded.
- evidence: /tmp/claude-0/wptest/work/r2-perf/net/wp-390-reduce-r1.json and wp-390-reduce-r2.json, /tmp/claude-0/wptest/work/r2-perf/net/v2-390-reduce-r1.json and v2-390-reduce-r2.json, /tmp/claude-0/wptest/work/r2-perf/net/tables.txt, /home/user/Generation-Maine/generation-maine/inc/creators.php ('portrait' => 'medium')

### PER-N07 [info] Core block CSS and global styles add 31 KB of inline CSS that v2 does not have (WordPress-inherent)
- template: seeded71
- steps: Inventory the head of the WordPress front page (style blocks and sizes) / Price it with run-lh-exp.sh mobile ?exp=nobc, which dequeues the wp-block-* styles and global-styles. This is test only and breaks some styling
- expected: Informational: the cost of the block-theme stack against the hand-built page.
- actual: Nine inline style blocks total 31,013 bytes:
- global-styles: 11,414 (41 preset variables and 67 has-* classes)
- wp-block-image: 8,891 (includes lightbox rules)
- wp-block-library: 4,273
- wp-block-button: 2,640
- wp-block-buttons: 1,477
- wp-block-heading: 1,247
- wp-block-paragraph: 739
- wp-block-group: 197
- wp-img-auto-sizes-contain: 135

There is also wp-fonts-local (641 bytes), a 386-byte speculationrules script with conservative eagerness (no load cost), two RSS alternate links and the REST API link. Without the block CSS the HTML is 65,286 bytes against 96,743. Simulated mobile FCP goes from 2160 to 1860 ms and LCP from 5265 to 5115 ms (3 runs). Not present: emoji script or styles (the theme removes them), jQuery, dashicons, interactivity or module scripts, classic-theme-styles.
- likely cause: WordPress prints the CSS for each core block used, plus theme.json global styles. The only candidate to trim is the image block's lightbox CSS (about 8.9 KB), for example by turning off the lightbox in theme.json or styling the about figure without core/image. The rest is expected for a block theme.
- evidence: /tmp/claude-0/wptest/work/r2-perf/wp-front.html, /tmp/claude-0/wptest/work/r2-perf/exp-nobc.html, /tmp/claude-0/wptest/work/r2-perf/lh-exp-m/summary.txt (wp_nobc)

### PER-N08 [info] style.css is the one render-blocking request (37.9 KB); v2 has none (informational)
- template: seeded71
- steps: Read renderBlockingStatus from Resource Timing in the net.mjs runs / Run run-lh-exp.sh mobile and desktop with ?exp=about,preloaddm,inline (style.css printed inline)
- expected: Informational.
- actual: On WordPress only style.css?ver=3154ae3 is render-blocking (37,865 bytes). site.js sits at the end of the body and is non-blocking in Chrome, but Lighthouse desktop lists it too, estimating 80 ms. v2 inlines all its CSS and JS. Lighthouse mobile estimates 150 to 300 ms of savings. Inlining the stylesheet in the test moved simulated mobile FCP from 1693 to 1571 ms and LCP from 3530 to 3376 ms, and desktop LCP to 720 ms against 800 with only the about fix. The earlier attempt measured the same direction.
- likely cause: This is the normal enqueued-stylesheet model, where the file is cacheable across views, so it is not a defect. A cheap optional step is to enqueue site.js with array( 'in_footer' => true, 'strategy' => 'defer' ) (WordPress 6.3+).
- evidence: /tmp/claude-0/wptest/work/r2-perf/net/wp-390x844-r1.json and wp-390x844-r2.json, /tmp/claude-0/wptest/work/r2-perf/lh-exp-m/summary.txt, /tmp/claude-0/wptest/work/r2-perf/lh-exp-d/summary.txt, /tmp/claude-0/wptest/work/r2-perf/lh-a/summary.txt (render-blocking items)

### PER-N09 [info] Server time: TTFB is 69 to 74 ms on WordPress against 1.3 ms on v2; 69 queries, 70 to 80 ms of PHP, 6.1 MB (WordPress-inherent)
- template: seeded71
- steps: Run /tmp/claude-0/wptest/work/r2-perf/ttfb.sh twice: 10 curl -w runs per site per set / Read the perf-stats.php comment (get_num_queries, timer_stop, per-block timings) over 10 requests
- expected: Informational.
- actual: Median TTFB for WordPress is 74.1 ms in set A (68.4 to 102.2) and 68.8 ms in set B (64.8 to 84.6). For v2 it is 1.3 and 1.4 ms. PHP time medians are 75.4 and 69.8 ms with 69 queries on every request and a 6.1 MB peak. Block medians:
- creators: 17.45 ms, 41 queries
- header part: 5.84 ms, 2 queries
- footer part: 6.01 ms, 6 queries (including the footer block, 4.17 ms and 5 queries)
- follow: 2.08 ms, 7 queries

Ten of the queries are single-row lookups for theme settings that do not exist yet on a fresh site: 7 from the follow block and 3 from the footer. Core caches each miss for the rest of the request.
- likely cause: PHP and SQLite render every request, with no page cache. A page cache on the host would bring this close to static. The avoidable part is the creators priming (separate finding).
- evidence: /tmp/claude-0/wptest/work/r2-perf/ttfb-a.txt, /tmp/claude-0/wptest/work/r2-perf/ttfb-b.txt, /tmp/claude-0/wptest/work/r2-perf/blocks-cost-all.txt, /tmp/claude-0/wptest/work/r2-perf/qlog-front.json

### PER-N10 [info] The footer's second read of the header part costs about 2.8 ms and 1 query per request (informational)
- template: seeded71
- steps: Load perf-hdr.php, which times from the first get_block_template('...//header') call to the end of the footer block, and request the front page 10 times, twice / Run hdrcost.php through `wpt wp r2perf eval-file` twice
- expected: Informational: the footer now builds its links from the header part.
- actual: There is one extra header read per request (header-part-reads=1, so the static cache in gm_header_links() works). Inside the footer it costs a median of 2.81 ms (2.47 to 4.66) and 1 query in the 10-request set; the TTFB sets agree (2.4 to 2.9 ms). That is about 4% of PHP time. The header blocks are rendered twice per request, once by core and once by do_blocks() in gm_header_links(). Measured on its own, a cold read costs 6.3 to 9.6 ms for get_block_template plus 6.6 to 9.0 ms for do_blocks, with 3 queries. Warm repeats cost 0.6 ms plus 1.1 to 1.7 ms. gm_render_footer() on its own costs 6.8 to 7.2 ms with 11 queries.
- likely cause: This is by design. If it matters, the parsed links could be cached in a transient keyed on the header part's post_modified, or parsed from the block tree with parse_blocks() instead of a full do_blocks() render.
- evidence: /tmp/claude-0/wptest/work/r2-perf/blocks-cost.txt, /tmp/claude-0/wptest/work/r2-perf/ttfb-a.txt and ttfb-b.txt (header-in-footer column), /tmp/claude-0/wptest/work/r2-perf/hdr-cost.txt, /home/user/Generation-Maine/generation-maine/inc/parts.php gm_header_links()

### PER-N11 [info] The stage avatars all load at open: 9 requests (46 KB) at 1440 and 4 at 390, though one shows at a time (informational, content-dependent)
- template: seeded71
- steps: Run net.mjs at 1440x900 and 390x844 twice, and list the .av images with their rendered size and visibility
- expected: Informational. v2 uses the placeholder figure, so it has no avatar requests.
- actual: At 1440, portrait-1 to portrait-9 at 150x150 (4,208 to 5,656 bytes each) load at page open. All 9 stage .who avatars are laid out at 36x36 within lazy-load distance, while only the current creator's is shown. At 390, 4 load at open and the rest load one per swipe. A 150 px file for a 36 CSS px avatar is fine on a 3x screen (108 px) and 4 times too large at 1x, but tiny in bytes. Desktop Lighthouse lists the avatars under responsive images at about 5 KiB each.
- likely cause: The stage holds one .who per creator, stacked, and core lazy loading does not know they are hidden. This could be left as is, or the script could set the avatar src the way it sets data-src on the clips.
- evidence: /tmp/claude-0/wptest/work/r2-perf/net/tables.txt, /tmp/claude-0/wptest/work/r2-perf/net/wp-1440x900-r1.json and wp-1440x900-r2.json

### PER-N12 [info] WordPress fetches two favicons (icon.svg and favicon.ico, 8.3 KB); v2 fetches one
- template: seeded71
- steps: Run net.mjs at 390 and 1440, two runs each
- expected: Informational.
- actual: Every WordPress run requests both /assets/img/icon.svg (4,687 bytes) and /assets/img/favicon.ico (3,612 bytes) at load. v2 requests only favicon.svg (4,731 bytes).
- likely cause: gm_favicon_fallback() prints an .ico with sizes="any" and an SVG icon, and Chromium fetches both. This is negligible; it could drop the .ico link or keep it only for old browsers.
- evidence: /tmp/claude-0/wptest/work/r2-perf/net/tables.txt

not tested: Real hosting: gzip or brotli, HTTP/2, cache headers, CDN, and MySQL instead of SQLite. Query time and TTFB will differ on a real host.; A page cache plugin, and the effect of object caching on the 69 queries.; Performance on WordPress 6.5 or PHP 7.4 (compat area).; Video clips (MP4 or WebM) instead of GIFs: the seeded data has GIFs only, and this Chromium has no H.264.; Real devices, field data and INP. Firefox and Safari.; Pages other than the front page (single, archive, 404).; Effect of preloading DM Sans under applied throttling: measured only with Lighthouse's simulated throttling.; Replacing the about photo was simulated with a test-only render_block filter that produces the markup the editor saves for a library image, not through the editor UI.; The live v2 URL: the local copy was served by python http.server, as instructed.
