# Round 3 verification findings (theme 3.2.0, build 95b10f6)


## ED: editor (Site Editor, hero gold word, Styles, locked and Part blocks, bar in narrow canvases) plus the page and post blocks, patterns and editor canvas items from install (INS-N01..N05, I08), SEC-N05 and SEC-N07

- EDI-N03 [partly] Fixed part: Creators, Follow List and Newsletter Signup have no Duplicate (menu: Copy, Add before/after, Unlock, Rename, Hide, Create pattern), Ctrl+Shift+D leaves 1, the inserter shows them disabled; a second Creators block gets 'Creators: This block can only be used once. Find original / Remove' and renders as the roster on the page with no duplicate ids. Still failing on both versions: Logo, Phone menu button and Maine mural still offer Duplicate and Ctrl+Shift+D duplicates them (2 to 3 to 4). Saved, the page shows two logos in the bar, two phone menu buttons at 390 where the second does nothing when tapped (aria-expanded stays false), a second mural, and duplicate ids menu, mural and muralclip. Duplicating a whole Creators or Follow section still copies the locked blocks; the editor marks each copy, but saved, the page has duplicate ids creators, follow and newsletter.
  evidence: /tmp/claude-0/wptest/work/r3-editor/data/s71-locks.json, /tmp/claude-0/wptest/work/r3-editor/data/s65-locks.json, /tmp/claude-0/wptest/work/r3-editor/data/s71-dupparts.json, /tmp/claude-0/wptest/work/r3-editor/data/s65-dupparts.json

- E08 [partly] With no font installed: no Colors, no Fonts section, no font library inside Styles, elements offer only Text alignment, Paragraph/Heading/Group have no font, Button has no radius or shadow; 6.5 shows Typography and Layout only. Reset styles gives {"styles":[],"settings":[]}. Still open on 7.1: Appearance > Fonts (font-library.php, also a Fonts button on the theme details) installs a font and activates it in the user global styles, which brings back a FONT picker for Text, Links, Headings, Captions and Buttons and a Font item in each paragraph's Typography menu. A font picked there shows in the Site Editor and post editor canvases but not on the page. README line 59 says there are no font controls and no font library. Details in the new finding.
  evidence: /tmp/claude-0/wptest/work/r3-editor/data/s71-styles-survey.json, /tmp/claude-0/wptest/work/r3-editor/data/s65-styles-survey.json, /tmp/claude-0/wptest/work/r3-editor/data/c71-fontupload.json, /tmp/claude-0/wptest/work/r3-editor/data/c71-afterfont-stylestext.json

- INS-N02 [partly] The original steps pass: Columns have a 34px gap, Buttons and the pagination are flex (one row at 1440), the separator starts at the text edge (x 140), cite and table caption are not italic, Row and Stack lay out. Still failing (same missing layout styles): the Gallery wraps 2 + a full-width image on the page and stacks in one column in the editor, Button Width 50% does nothing, a Row's vertical alignment and a Grid's Columns setting are ignored. Filed as new findings.
  evidence: /tmp/claude-0/wptest/work/r3-editor/data/c71-blocks-blocks.json, /tmp/claude-0/wptest/work/r3-editor/data/c65-blocks-blocks.json, /tmp/claude-0/wptest/work/r3-editor/data/c71-layout2-layout2.json, /tmp/claude-0/wptest/work/r3-editor/data/c71-tt5-layout2-layout2.json

- I08 [partly] Fixed: README line 31 'Tested on WordPress 7.1.3 and 6.5.13 with PHP 8.4, and on WordPress 6.5 with PHP 7.4' now agrees with 'Tested up to: 7.1'; the overlay shows Version 3.2.0 and Tags (7.1: One Column, Block Editor Patterns, Editor Style, Site Editor, Template Editing; 6.5 shows the raw slugs). Theme Check no longer lists the Tags info or a copyright warning. Still open: no Author URI, so 'By Green Falls' has no link, and there is no copyright line (C08, waiting on the client). Theme Check still lists readme.txt, favicon.ico and the plugin-territory items, which the README explains.
  evidence: /tmp/claude-0/wptest/work/r3-editor/shots/c71-theme-details.png, /tmp/claude-0/wptest/work/r3-editor/shots/c65-theme-details.png, /tmp/claude-0/wptest/work/r3-editor/data/c71-themecheck.txt, /tmp/claude-0/wptest/work/r3-editor/data/c65-themecheck.txt


### ED-R1 [medium] A Gallery block in a post or page lays out wrong: three images become two plus a full-width third, one per row on phones, and the editor stacks them in one column
- template: clean71 (UI install); also clean65
- steps: Install the zip through Appearance > Themes, import three images / Pages > Add New, Code editor (Ctrl+Shift+Alt+M), paste a Gallery with three images (default columns) and one with Columns 3 (markup in /tmp/claude-0/wptest/work/r3-editor/markup/rest.html and extra.html), publish / View the page at 1440 and 390, then open it in the editor / Baseline: switch the same site to Twenty Twenty-Five and view the same page
- expected: Images lay out as WordPress intends (Twenty Twenty-Five, same page: three in one row; 2 per row at 390; the same in the editor). README line 63 says other row blocks lay out as WordPress intends.
- actual: 7.1 page: images 391, 391 and 791px wide (the third is full width, 1054px tall); the 3-column gallery does the same; at 390 one image per row. 7.1 editor: the gallery is display:block and the images stack in one 258px column. 6.5 page: 395, 395, 791; 6.5 editor: each image 791px wide, stacked. Reproduced on clean71 and clean65.
- likely cause: theme.json styles.spacing.blockGap is "0" with no unit, so --wp--style--block-gap and the gallery's --wp--style--unstable-gallery-gap are a unitless 0, and core's widths calc(33.33% - var(--wp--style--unstable-gallery-gap,16px)*.667) become invalid (figures fall back to width auto and wrap). On 7.1 the theme's re-added :where(main.gm-page .is-layout-flex){gap:.5em} also adds an 8.5px gap that the widths leave out. In the browser, block gap '0px' alone fixed 6.5; 7.1 also needed .wp-block-gallery.is-layout-flex{gap:var(--wp--style--unstable-gallery-gap)} (galfix-console.txt). In the editor, core's :root :where(figure.wp-block-gallery){display:block} (specificity 0,1,0) beats the theme's zero-specificity flex rule. This was already broken before 3.2.0, but the 3.2.0 README now promises it works.
- evidence: /tmp/claude-0/wptest/work/r3-editor/shots/c71-gallery-front-1440-crop.png, /tmp/claude-0/wptest/work/r3-editor/shots/c71-grid-gallery-front-1440-crop.png, /tmp/claude-0/wptest/work/r3-editor/shots/c71-tt5-grid-gallery-front-1440-crop.png, /tmp/claude-0/wptest/work/r3-editor/shots/c71-layout2-editor-1440.png, /tmp/claude-0/wptest/work/r3-editor/shots/c65-gallery-front-1440-crop.png


### ED-R2 [low] Button Width 25/50/75% does nothing: two 50% buttons stay 110px wide
- template: clean71; also seeded65 and seeded71
- steps: Pages > Add New, a Buttons block with two Button blocks set to Width 50% and one set to 100% (markup /tmp/claude-0/wptest/work/r3-editor/markup/btnwidth.html, pasted through the Code editor), publish / View at 1440 and 390
- expected: Each 50% button takes half the row, as the Width control promises.
- actual: Both 50% buttons are 110px (their content width) at 1440 and 390; 100% works. Same on 7.1 and 6.5.
- likely cause: Same unitless blockGap "0": core's .wp-block-buttons>.wp-block-button.wp-block-button__width-50{width:calc(50% - var(--wp--style--block-gap, .5em)*.5)} becomes invalid. Setting blockGap to "0px" (or a real gap) should fix it.
- evidence: /tmp/claude-0/wptest/work/r3-editor/data/bw-console.txt, /tmp/claude-0/wptest/work/r3-editor/data/c71-bw-mkpage.json, /tmp/claude-0/wptest/work/r3-editor/data/s65-bw-mkpage.json


### ED-R3 [low] A Row's vertical alignment and a Grid's Columns setting have no effect, on the page or in the editor
- template: clean71; also clean65
- steps: In a page add Group > Row with justification Space between and vertical alignment Top, holding a three-line paragraph and a short one / Add Group > Grid with Columns 2 and four paragraphs / Publish, view at 1440 and 390, and look at the editor; baseline the same page under Twenty Twenty-Five
- expected: The short item sits at the top, and the grid shows 2 columns (Twenty Twenty-Five: both, page and editor).
- actual: align-items stays center (the short item is 29px lower), and the 2-column grid shows 3 columns at 1440 (auto-fill 12rem) and 1 at 390. The editor shows the same. Both versions. Justification, nowrap and the vertical stack do work.
- likely cause: disable-layout-styles: the theme re-adds the class-based layout rules but not the per-block wp-container styles (verticalAlignment, columnCount, minimumColumnWidth), as the fixer noted. The controls are still shown, so a client gets a setting that silently does nothing. Hide them, or print those values.
- evidence: /tmp/claude-0/wptest/work/r3-editor/data/c71-blocks-blocks.json, /tmp/claude-0/wptest/work/r3-editor/data/c65-blocks-blocks.json, /tmp/claude-0/wptest/work/r3-editor/data/c71-layout2-layout2.json, /tmp/claude-0/wptest/work/r3-editor/data/c71-tt5-blocks-blocks.json, /tmp/claude-0/wptest/work/r3-editor/data/c71-tt5-layout2-layout2.json


### ED-R4 [medium] Appearance > Fonts brings back font pickers: a font installed there shows up in Styles and in blocks, and a font picked in Styles changes the editor but not the page
- template: clean71 (UI install); also seeded71
- steps: Appearance > Fonts (font-library.php; the theme details also show a Fonts button) > Upload: LiberationSerif-Regular.ttf ('Fonts were installed successfully') / Site Editor > Styles > Typography > Text: a FONT picker is now there (also Links, Headings, Captions, Buttons); a paragraph's Typography menu in the post editor now offers Font / Pick Liberation Serif for Text and Headings, Review changes > Save / View the front page, then reopen the Front Page in the Site Editor and a post in the editor
- expected: README line 59: Styles has no color or font controls and no font library, and blocks have no font controls. Either fonts cannot be installed and offered, or the editor and the page agree.
- actual: After saving, the Site Editor canvas shows the h1, lede, About goal and body in Liberation Serif, and the post editor shows paragraphs in it, while the page keeps Bricolage Grotesque and DM Sans. The global styles post now holds settings.typography.fontFamilies.custom (the font) and styles.typography.fontFamily. Styles > Reset styles clears it. 6.5 has no Appearance > Fonts.
- likely cause: gm_editor_settings() sets fontLibraryEnabled false only in the block editor settings. WordPress 7's standalone Appearance > Fonts screen still installs fonts and activates them in the user's global styles. Once fontFamilies is non-empty, core shows the pickers again. On the page the theme's own font rules win; in the canvas the global styles win. Remove the Fonts screen and menu item, or filter user fontFamilies out (wp_theme_json_data_user), or make editor.css win as style.css does.
- evidence: /tmp/claude-0/wptest/work/r3-editor/data/c71-fontupload.json, /tmp/claude-0/wptest/work/r3-editor/data/c71-afterfont-stylestext.json, /tmp/claude-0/wptest/work/r3-editor/data/c71-font-pickfont.json, /tmp/claude-0/wptest/work/r3-editor/data/c71-font-canvasfont.json, /tmp/claude-0/wptest/work/r3-editor/data/s71-fontupload.json


### ED-R5 [low] The hero headline does not wrap a long word: a web address as the last word runs past the hero on phones and the page scrolls sideways
- template: seeded71; also seeded65
- steps: Site Editor > Front Page, hero headline: Ctrl+A, type 'Young Mainers', Shift+Enter, 'at generationmaine.org.', save / View the front page at 390 and 320
- expected: The headline wraps inside the blue hero (page titles already use overflow-wrap:anywhere), and the dot stays with the word.
- actual: The page scrolls sideways by 16px at 390 and 86px at 320. The gold '.org' runs past the blue background onto white, and the dot wraps alone onto the next line. Same on 7.1 and 6.5. A pasted run of no-break spaces in the headline (SEC-N05 check) makes the page 69,933px wide at 390.
- likely cause: style.css '.hero h1{font-size:clamp(44px,6.2vw,84px);line-height:1;margin:0 0 24px}' has no overflow-wrap, and the front page has no overflow clip. Add overflow-wrap:anywhere (or break-word) to .hero h1; v2 has the same rule but its copy is fixed.
- evidence: /tmp/claude-0/wptest/work/r3-editor/shots/s71-gw6-url-front-320.png, /tmp/claude-0/wptest/work/r3-editor/shots/s65-gw2-url-front-320.png, /tmp/claude-0/wptest/work/r3-editor/data/s71-gw6-goldword.json, /tmp/claude-0/wptest/work/r3-editor/data/s65-gw2-goldword.json, /tmp/claude-0/wptest/work/r3-editor/data/s71-sec05-nbsp.json


### ED-R6 [low] In the editor, the dot sits apart from the word after trailing spaces, and alone on a new line after a trailing line break
- template: seeded71; also seeded65
- steps: Site Editor > Front Page, hero headline: Ctrl+A, type 'Young Mainers', Shift+Enter, 'on staying here', then Shift+Enter (or 7 spaces) / Look at the canvas, then save and view the page
- expected: The canvas dot follows the last letter, as on the page (the README says the editor shows the dot).
- actual: After a trailing line break, the canvas draws the dot alone on a third line. After trailing spaces, it sits about 90px to the right of 'here'. The page shows 'here' with the dot right after it. Same on 7.1 and 6.5.
- likely cause: editor.css draws the dot as .gm-here::after after all of the heading's content, including the trailing <br> and spaces; the editor script only handles ? and !.
- evidence: /tmp/claude-0/wptest/work/r3-editor/shots/s71-gw3-trailingBreak-canvas.png, /tmp/claude-0/wptest/work/r3-editor/shots/s65-gw2-trailingBreak-canvas.png, /tmp/claude-0/wptest/work/r3-editor/shots/s71-gw3-trailingSpaces-canvas.png, /tmp/claude-0/wptest/work/r3-editor/shots/s71-gw3-trailingBreak-front-1440.png


### ED-R7 [low] A headline ending in a quoted word with the period inside the quotes keeps the period and adds the dot: “home.”•
- template: seeded71; also seeded65
- steps: Site Editor > Front Page, hero headline: Ctrl+A, type 'Young Mainers', Shift+Enter, 'on a place called "home."' (US style, period inside the quotes), save / View the front page
- expected: One dot, as README line 51 describes for a final period (the period becomes the dot), or no dot.
- actual: The page prints <span class="here">“home.”<i class="d pulse"></i></span>: gold “home.” and then the gold dot, so the period and the dot both show. Through gm_mark_here(), a question inside quotes ('"home?"') also gets a dot, and 'here...' shows 'here..' plus the dot (noted by the fixer). Same on 7.1 and 6.5.
- likely cause: gm_mark_here() (functions.php) checks only the last visible character for '.', '?' or '!'. A closing quote mark (" or &#8221;) after it hides the period.
- evidence: /tmp/claude-0/wptest/work/r3-editor/shots/s71-gw8-quoted-front-1440.png, /tmp/claude-0/wptest/work/r3-editor/shots/s65-gw3-quoted-front-1440.png, /tmp/claude-0/wptest/work/r3-editor/data/s71-gw8-goldword.json, /tmp/claude-0/wptest/work/r3-editor/data/s65-gw3-goldword.json, /tmp/claude-0/wptest/work/r3-editor/data/s71-marks-cases.txt


### ED-R8 [low] After updating from 3.1.0, a font chosen in Styles under 3.1.0 turns the editor text into Times New Roman (or the headings into DM Sans), and Styles shows nothing to undo it
- template: seeded71
- steps: Upload a 3.1.0 zip (built from git 432732d) through Upload Theme > Replace installed with uploaded / Styles > Typography > Text > Font 'Michroma (labels)', Save / Upload the 3.2.0 zip and Replace installed with uploaded / Open the Front Page in the Site Editor; open Styles > Typography > Text / Second run: the same with Headings > 'DM Sans (body)'
- expected: The fixer says the canvas falls back to the base stack until Reset styles; ideally the canvas keeps the theme's fonts or Styles shows the stale choice.
- actual: Run 1: the canvas lede, About goal, Follow lede and body render in Times New Roman (the browser default). Run 2: the canvas h1 and h2 render in DM Sans instead of Bricolage. The page is unaffected. Styles > Typography > Text now offers only Text alignment, so nothing shows the stored choice; only Styles > Reset styles clears it.
- likely cause: The user global styles keep var:preset|font-family|label (or body). 3.2.0's theme.json defines no font-family presets, so var(--wp--preset--font-family--label) is undefined, the declaration is invalid at computed time, and the canvas inherits the browser default. A small migration (drop typography.fontFamily values that point at the removed presets in wp_theme_json_data_user) or a README line would cover sites that used Styles under 3.1.0.
- evidence: /tmp/claude-0/wptest/work/r3-editor/data/s71-on310-pickfont310.json, /tmp/claude-0/wptest/work/r3-editor/data/s71-after320font-pickfont310.json, /tmp/claude-0/wptest/work/r3-editor/data/s71-on310h-pickfont310.json, /tmp/claude-0/wptest/work/r3-editor/data/s71-after320h-pickfont310.json, /tmp/claude-0/wptest/work/r3-editor/shots/s71-after320font-styles-text.png


### ED-R9 [info] The Header part editor shows the bar 84px tall although everything fits on one row (68px on the page and in the Front Page canvas)
- template: seeded71; also seeded65
- steps: 7.1: Front Page > click the bar > Edit original (6.5: open the Header template part) / Measure the bar
- expected: The bar keeps one 68px row whenever everything fits (fixer's E16 note).
- actual: The bar is 84px: the Section links group is 60px tall in the part editor (its paragraphs are 26px, at one y) against 26px in the Front Page canvas. Labels and the button sit on one row. Both versions.
- likely cause: The E16 change lets .w grow (height auto, padding-block 12px). In the part editor the nav group gets extra height from the editable block wrappers, which the fixed 68px height used to hide.
- evidence: /tmp/claude-0/wptest/work/r3-editor/data/hdrdbg-console.txt, /tmp/claude-0/wptest/work/r3-editor/data/s71-header-barcanvas.json, /tmp/claude-0/wptest/work/r3-editor/shots/s71-header-part-sidebar.png


### ED-R10 [info] README line 59 does not list everything Styles still offers on WordPress 7.1
- template: seeded71
- steps: Site Editor > Design > Styles: open each top-level item and Blocks > Button, Quote, Table
- expected: The README's list of panels the theme cannot remove matches what a client sees.
- actual: Besides the listed Font size presets, Shadows, layout widths and text alignment, 7.1 also shows an empty Background panel, Button > Dimensions > Width, the Quote 'Plain' and Table 'Stripes' variations, a States section per block, and Additional CSS. The README does mention the Button Outline style.
- likely cause: Documentation gap. These are core panels the theme does not turn off.
- evidence: /tmp/claude-0/wptest/work/r3-editor/data/s71-styles-survey.json, /tmp/claude-0/wptest/work/r3-editor/data/s65-styles-survey.json


## FR: verify-front: front page as a visitor (phone menu, carousel, stepper, viewer, pause control, motion, keyboard, no-JS, admin bar), front-end performance and network, roster on the front end, WordPress against the local v2 page

- VIS-N05 [partly] The original defect is fixed. One-card swipes show 01 to 09 and back to 01 at every width, on WP 7.1, WP 6.5 and v2, in both runs. Card 8 now has its own resting place. Forward flicks carry several cards and stop at the first card of the end stretch, and the counter always matched the card on screen (0 mismatches). But the fix's settle step brings a regression: a swipe back that starts in the end stretch is pulled forward again. At 768x1024 a flick back from card 8 reached card 1 and then glided 1931px forward to card 7. At 844x390 and 768x1024 every back swipe from 7, 8 or 9 travels 2 to 3 cards back and then returns forward 427 to 688px. On phones a slow drag or flick back from card 9 is pulled forward to card 8. Details are in new findings.
  evidence: /tmp/claude-0/wptest/work/r3-front/logs/swipe-r1.log, /tmp/claude-0/wptest/work/r3-front/logs/swipe-r2.log, /tmp/claude-0/wptest/work/r3-front/logs/carousel-end2-r1.log, /tmp/claude-0/wptest/work/r3-front/logs/fling-r1.log

- V12 [partly] Left as designed (wont_fix). The README now explains the narrow segments and the alternatives, which round 2 asked for. The targets are unchanged: 28x44 at 320 and 35x44 at 390, identical on v2, and still the only targets under 44px on phones. The new README sentence misstates the numbers. It says '28 to 40 px wide with nine creators on a 390 px screen', but on a 390px screen all nine are 35px. 28px is at 320 and 40px at 430.
  evidence: /tmp/claude-0/wptest/work/r3-front/logs/measure-summary.txt, /tmp/claude-0/wptest/work/r3-front/logs/measure-wp-r1.json, /tmp/claude-0/wptest/work/r3-front/logs/measure-wp-r2.json, /tmp/claude-0/wptest/work/r3-front/w65/logs/measure-r1.json

- E01 [partly] On the front page the original defect is fixed. In two runs: 0 towns clipped, 0 mid-word breaks, no text-shadow, and every span display:block with white-space:normal at all 7 widths. The long towns wrap at spaces. The same block placed in a page fails: at 1440 nine tiles are squeezed into the 68ch column, and 6 to 7 of 9 towns break mid-word ('Skowh|egan,', 'Presqu|e Isle', 'Biddef|ord') with the numbers stacked '0|1'. This reproduced on 7.1 and 6.5. A long name at 320 squeezes its number to 0px wide. See new findings.
  evidence: /tmp/claude-0/wptest/work/r3-front/logs/roster-ui-r2script.log, /tmp/claude-0/wptest/work/r3-front/logs/roster-modfront-r1.log, /tmp/claude-0/wptest/work/r3-front/logs/roster-modfront-r2.log, /tmp/claude-0/wptest/work/r3-front/logs/roster-seed-r1.log


### FR-R1 [medium] Phone carousel: a swipe back from the last cards glides forward again. On tablets and landscape phones a flick back from card 8 can reach card 1 and then slide 1931px forward to card 7
- template: seeded71 (also seeded65 and the local v2 page)
- steps: wpt new <name> <port> seeded71 / Open http://127.0.0.1:<port>/ at 768x1024 (or 844x390) with touch emulation and scroll to The creators / Tap segment 8 (or 9, or 7) / Flick toward the start: a quick swipe right of about 650px in 4 touch moves over 32ms. Or drag right slowly across 85% of the screen / Watch the counter and the track for 2.5 s (flingback.mjs records scrollLeft and the counter every frame) / On a 390 or 320 phone, start from segment 9 and drag back slowly
- expected: The track settles where the gesture took it, at the nearest resting card in the direction of the swipe. It never moves forward after a backward swipe.
- actual: 768x1024, flick back from 08: the track reaches 01 (scrollLeft 0), then glides 1931px forward to 07. The counter reads 08 07 06 05 04 03 02 01 07 01 02 03 04 05 06 07. Every back swipe from 9, 8 or 7 at 768x1024 and 844x390 goes back 2 to 3 cards and then returns forward 427 to 688px (for example 09 08 07 06 08 06 07 08 and 07 06 05 04 06 04 05 06). In one 844x390 v2 run a flick back from 07 reached 01 and slid 1720px forward to 06. At 390x844 and 320x568, a slow drag back from 09 reaches 07 and is pulled forward to 08. One flick back from 09 reached 04 and was pulled 1272px (390) or 1054px (320) forward to 08. Visitors can never fling from the end of the track back toward the start. The results are the same on WP 7.1, WP 6.5 and v2 in two runs each.
- likely cause: assets/js/site.js settle() (from build_splash_lean.py): `else if (k < g - 1 && g - 1 >= zone) goTo(g - 1);` corrects any backward swipe that started in the end stretch and travelled more than one card, even when it ended outside that stretch (k < zone), where cards rest at the gutter and nothing needs correcting. Limit the correction to swipes that stay inside the end stretch (k >= zone), or correct only the forward overshoot the fix was meant for.
- evidence: /tmp/claude-0/wptest/work/r3-front/logs/flingback-r1.log, /tmp/claude-0/wptest/work/r3-front/logs/flingback-r2.log, /tmp/claude-0/wptest/work/r3-front/w65/logs/flingback-r1.log, /tmp/claude-0/wptest/work/r3-front/w65/logs/flingback-r2.log, /tmp/claude-0/wptest/work/r3-front/flingback/sbs-wp-768-flick-from8-r1.png


### FR-R2 [medium] The Creators block placed on its own in a page stays in the 68ch reading column: the Roster breaks towns mid-word and stacks the numbers, and the Stepper sits left-aligned at 791px
- template: seeded71 (also seeded65)
- steps: wpt new <name> <port> seeded71 / Create a page holding the Creators block with Layout Roster, the same markup the inserter saves: wpt wp <name> post create --post_type=page --post_status=publish --post_title=Roster --post_content='<!-- wp:generation-maine/creators {"layout":"roster"} /-->' / Open /roster/ at 1440x900 and read each tile's .town and .n (roster.mjs) / Repeat with the default Stepper block (<!-- wp:generation-maine/creators /-->) and open it at 1440x900
- expected: Like the Creators section on the front page, and like the Follow section and the Creators pattern inserted into a page (INS-N04 / E10), the block runs full width. Towns wrap only at spaces.
- actual: At 1440 the roster section is 791px wide, left-aligned, with white space on the right. Its 9 tiles are about 65px wide. 7 of 9 towns break mid-word ('Skowh|egan,', 'Presqu|e Isle', 'Biddef|ord', 'Machi|as', 'Lewis|ton', 'Rumfo|rd', 'Sanfo|rd'). The numbers stack on two lines ('0|1'), with .n 9/11 and 1/11 wide against its content. 1024 and below are fine. The bare Stepper block in a page is also 791px wide and left-aligned at 1440 (stage 315px, panels 269px wide), against full width on the front page. This reproduced on WP 7.1 and WP 6.5, in two runs.
- likely cause: The full-width rule in style.css (WP_ADDITIONS in build_theme.py), `.gm-entry>.wp-block-group.block,.gm-entry>.wp-block-group.hero,.gm-entry>.gm-creators{max-width:none;margin-inline:calc(50% - 50vw)}`, only matches the Creators pattern's wrapper (.gm-creators). The block's own output, section.block.roster or section.stories, falls under `.gm-entry>*{max-width:68ch}`. The E01 reset `.roster .tile .who span{...overflow-wrap:anywhere}` then lets the town break anywhere, and the .n auto column shrinks to one glyph. Add `.gm-entry>section.roster,.gm-entry>section.stories` to the full-width rule, and use overflow-wrap:break-word (or anywhere only on .town) so the number keeps its width.
- evidence: /tmp/claude-0/wptest/work/r3-front/logs/roster-seed-r1.log, /tmp/claude-0/wptest/work/r3-front/logs/roster-seed-r2.log, /tmp/claude-0/wptest/work/r3-front/roster/wp71seed-1440x900-r1.png, /tmp/claude-0/wptest/work/r3-front/w65/logs/roster-r1.log, /tmp/claude-0/wptest/work/r3-front/stepperpage/1440-r1.png


### FR-R3 [low] Roster tile with a long creator name: the number collapses to 0px and stacks, and the name runs past the tile edge at 320
- template: seeded71
- steps: wpt new <name> <port> seeded71 / wpt wp <name> post update 29 --post_title='Samantha Theriault-Ouellette' / Show the roster with all nine creators (a page with the Roster Creators block, or the Front Page block set to Roster with the default limit) / Open it at 320x568 and look at tile 9 (tileshot.mjs)
- expected: The number '09' stays on one line and the name wraps or ellipsizes inside the tile.
- actual: At 320 the .n span is 0px wide (scrollWidth 11), so '09' prints as '0' over '9'. The bold name 'Samantha' runs past the tile's right edge and is cut at the edge of the grid. At 390 the number is 12px wide but still stacks. This reproduced in two runs.
- likely cause: `.roster .tile .who{grid-template-columns:auto 1fr}`, together with the E01 reset `.roster .tile .who span{overflow-wrap:anywhere}`, lets the auto column for .n shrink to its anywhere-break min-content. The <b> name has no overflow-wrap and no min-width:0, so a long word overflows. Give .n white-space:nowrap, and give the name overflow-wrap:break-word with min-width:0.
- evidence: /tmp/claude-0/wptest/work/r3-front/roster/tile9-sbs.png, /tmp/claude-0/wptest/work/r3-front/roster/tile9-longname-320-r1.png, /tmp/claude-0/wptest/work/r3-front/roster/tile9-longname-320-r2.png, /tmp/claude-0/wptest/work/r3-front/logs/roster-modpage-r1.log, /tmp/claude-0/wptest/work/r3-front/logs/roster-modpage-r2.log


### FR-R4 [info] Rotating a tablet with keyboard focus inside the open phone menu drops focus to the page body; the next Tab skips the desktop bar
- template: seeded71 (also seeded65 and the local v2 page)
- steps: wpt new <name> <port> seeded71 / Open http://127.0.0.1:<port>/ at 768x1024 with no touch, focus Menu, press Enter, press Tab twice (focus on Creators in the sheet) / Rotate to 1024x768 (setViewportSize), then press Tab
- expected: Focus moves to a sensible visible control, such as the bar's first link, or the next Tab starts from the bar.
- actual: The sheet closes correctly, but document.activeElement becomes BODY. The next Tab goes to the hero's 'Follow along' (top 574), past the logo, the three bar links and the newsletter button. This was the same in both runs on WP 7.1 and WP 6.5 and on v2. Minor: it needs a keyboard and a rotation together.
- likely cause: The phone media-query change handler calls setMenu(false), which makes the sheet inert while it holds focus, so Chromium drops focus to body and resumes sequential navigation after the sheet. The handler could move focus to the bar's first link (or the logo) when the sheet contained the focus.
- evidence: /tmp/claude-0/wptest/work/r3-front/logs/rotate2-r1.log, /tmp/claude-0/wptest/work/r3-front/logs/rotate2-r2.log, /tmp/claude-0/wptest/work/r3-front/w65/logs/rotate2-r1.log


## AD: verify-admin: creators admin (Place on the page, clip picker, roles, seed script, drawer, duplicate blocks) and settings/SEO (Contact link, URL cleaning, handles from addresses, posts page SEO, JSON-LD, gm_seo title), plus REST exposure

- CRE-N05 [partly] The README case passes: '@aroostook.county.potatoes' shows once, different name and handle show both lines, and Lena shows only '@lena'. Still failing: a handle that WordPress's typography filter rewrites is shown twice, and altered. '@4x4.maine' renders '<b>@4&#215;4.maine</b>@4&#215;4.maine' ('@4×4.maine / @4×4.maine'), and '@gen--maine' renders '@gen–maine / @gen–maine', on both versions. The cause: gm_who() compares the raw gm_handle with get_the_title(), which wptexturize has already changed. See the typography finding in new_findings.
  evidence: /tmp/claude-0/wptest/work/r3-admin/logs/cre-n05-71-run1.json, /tmp/claude-0/wptest/work/r3-admin/logs/cre-n05-65-run1.json, /tmp/claude-0/wptest/work/r3-admin/shots/handleonce-h71-1440.png, /tmp/claude-0/wptest/work/r3-admin/shots/handleonce-h65-320.png

- X12 [partly] The original route now works. The picker warns at once ('larger than 10 MB') and after reload ('This clip is 11.9 MB'); a smaller pick and Remove hide it. A big Media Library link warns after save and reopen, as the README says: 11.9 MB for the GIF, 11.4 MB for the MP4. Still failing: the warning for a link is worked out only when the page loads. (1) After replacing the big link with a 0.9 MB library file and clicking Update, the box still says 'This clip is 11.9 MB' until reload (screenshot). (2) Remove of a picked big clip hides the warning although the saved link is also over 10 MB; it returns after reload. (3) A library link with a query string (?v=2) is not recognized, so it gets no warning. Item (1) is a new behavior from the fix and is in new_findings.
  evidence: /tmp/claude-0/wptest/work/r3-admin/logs/x12-pick71-run1.txt, /tmp/claude-0/wptest/work/r3-admin/logs/x12-link71-run1.txt, /tmp/claude-0/wptest/work/r3-admin/logs/x12-stale71-run1.txt, /tmp/claude-0/wptest/work/r3-admin/logs/x12-65-run1.txt

- SET-N03 [partly] Every shape in the brief gives the account handle or the bare host: @generationmaine from /videos, /video/id, /shorts, ?lang=; youtube.com for /channel/, /c/, /user/, /shorts/id; instagram.com for a post, reel, stories or explore link; tiktok.com or vm.tiktok.com for short links. 6.5 output is identical, with no sideways scroll at 320. Still failing: an Instagram story-highlight share link https://www.instagram.com/s/aGlnaGxpZ2h0OjE3...?story_media_id=...&igsh=... shows the handle '@s' as a live link, and /share/BAabc123/ shows '@share' (both versions). 's' and 'share' are missing from the exclusion list in gm_handle_from_url(); an allow-list approach would be safer.
  evidence: /tmp/claude-0/wptest/work/r3-admin/logs/handles-71-run1.json, /tmp/claude-0/wptest/work/r3-admin/logs/handles-65-run1.json, /tmp/claude-0/wptest/work/r3-admin/logs/handles-extra-8703.json, /tmp/claude-0/wptest/work/r3-admin/logs/handles-extra-8713.json


### AD-R1 [low] The 10 MB warning for a clip link goes stale in the editor: after the link is replaced by a small file and the creator is updated, the box still says 'This clip is 11.9 MB'
- template: seeded71 and seeded65
- steps: wpt new <name> <port> seeded71 and log in as admin. Media > Add New: upload a GIF over 10 MB (for example a copy of /tmp/claude-0/wptest/work/creators/bigmedia/big-clip-11mb.gif) and a small GIF, and copy both URLs / Creators > Noah > Meta Boxes: if a clip is chosen, click Remove. Paste the big file's URL into 'Or a clip link', click Update, then reload: the box shows 'This clip is 11.9 MB...' (correct) / Without reloading, replace the link with the small file's URL and click Update ('Post updated.') / Read the box: the yellow 11.9 MB warning is still there under a 0.9 MB link. It goes away only after a reload / Variant: with a big link saved, choose a big clip with the picker, Update, reload, then click Remove: the warning disappears although the saved link is still over 10 MB; it returns after reload
- expected: The warning matches the clip the box now holds: it hides (or says it will be rechecked) when the link is changed or cleared, and after Update it reflects what was saved
- actual: The warning for a link is decided when the box is printed and never changes during the session. On 7.1 and 6.5 the box shows 'This clip is 11.9 MB. Visitors download all of it...' next to a saved 0.9 MB link after Update. Remove hides the warning even when the remaining saved link is big.
- likely cause: inc/creators.php gm_creator_meta_box_html() works out $big from attachment_url_to_postid( $link ) only at page load (the X12 fix). The picker script in gm_creator_admin_assets() updates #gm_clip_big only on the media frame's select and on Remove, nothing listens to #gm_clip_url, and the block editor does not re-render the meta box after a save. A small fix: hide #gm_clip_big on input in #gm_clip_url when no clip is chosen (with a short 'checked after you save and reopen' line), and on Remove fall back to the link's state instead of always hiding it.
- evidence: /tmp/claude-0/wptest/work/r3-admin/logs/x12-stale71-run1.txt, /tmp/claude-0/wptest/work/r3-admin/logs/x12-65-run1.txt, /tmp/claude-0/wptest/work/r3-admin/shots/clip-stale71-stale-after-update.png, /tmp/claude-0/wptest/work/r3-admin/shots/clip-x12c65-stale65.png


### AD-R2 [low] WordPress's typography filter changes handles on the page: '@maine.4x4' shows as '@maine.4×4', '@generation--maine' as '@generation–maine', and a creator titled with such a handle shows it twice
- template: seeded71 and seeded65
- steps: wpt new <name> <port> seeded71 and log in. Settings > Generation Maine: TikTok address https://www.tiktok.com/@maine.4x4 with the TikTok handle empty, YouTube handle @generation--maine, Save Changes / Open the home page as a visitor and read the Follow rows / Creators > Add creator: title '@4x4.maine', Handle '@4x4.maine', any clip link, Publish; open the home page at 1440 and 320 and read the clip header; also put the Creators block with Layout Roster on a page
- expected: Handles appear exactly as typed (letters, digits, dots, underscores and hyphens are all valid in handles), and a creator whose title is the handle shows it once, as the CRE-N05 fix intends
- actual: Follow rows show '@maine.4×4' (from the address) and '@generation–maine' (en dash), while the links point to the right accounts. The clip header renders '<b>@4&#215;4.maine</b>@4&#215;4.maine', that is '@4×4.maine / @4×4.maine', on the stage, cards and viewer. '@gen--maine' gives '@gen–maine / @gen–maine'. The roster tiles and the card aria-label ('Open the clip from @4&#215;4.maine full size') are changed too. Same on 7.1.3 and 6.5.13.
- likely cause: Core runs wptexturize over the whole rendered block template (wp-includes/block-template.php:297, get_the_block_template_html), and the_content does the same in posts and pages, so digit-x-digit and '--' inside the theme's handle spans are rewritten. Separately, gm_get_creators() uses get_the_title(), which is already texturized, so gm_who()'s same-handle check (inc/creators.php ~line 462) compares '@4&#215;4.maine' with the raw '@4x4.maine'. Possible fixes: compare against get_post_field( 'post_title' ) decoded, and print handles in an element listed in the no_texturize_tags filter (or escape the x and hyphens as numeric entities before output).
- evidence: /tmp/claude-0/wptest/work/r3-admin/logs/follow-handles-evidence.txt, /tmp/claude-0/wptest/work/r3-admin/shots/follow-handles-8703.png, /tmp/claude-0/wptest/work/r3-admin/shots/follow-handles-8713.png, /tmp/claude-0/wptest/work/r3-admin/logs/texhandle-follow.txt, /tmp/claude-0/wptest/work/r3-admin/logs/cre-n05-71-run1.json


### AD-R3 [low] Handle fields keep a lone '@', a space after the '@', a doubled '@' or an inner space, and the follow row shows them as typed
- template: seeded71 and seeded65
- steps: wpt new <name> <port> seeded71 and log in. Settings > Generation Maine: Instagram handle ' @ generationmaine', TikTok handle '@', YouTube handle '@@generationmaine', Save Changes / Open the home page as a visitor and read the Follow rows / Repeat with Instagram handle 'generation maine'
- expected: Handles are normalized to one leading @ with no spaces (README: 'A handle gets its @ if it is missing'), and a handle of only '@' counts as empty, so the row falls back to the handle from the address or the placeholder
- actual: Stored and shown as '@ generationmaine', '@', '@@generationmaine' and '@generation maine'. With an address set, a lone '@' replaces the handle the theme would take from the address. Same on 7.1.3 and 6.5.13 (the settings fixer noted it in round 2 but left it unchanged).
- likely cause: inc/settings.php gm_sanitize_handle() only trims and adds '@' when the first character is not '@'. Stripping all whitespace and leading @/＠ signs, then adding one '@', and returning '' for an empty remainder would fix it.
- evidence: /tmp/claude-0/wptest/work/r3-admin/logs/handle-spaces.txt

