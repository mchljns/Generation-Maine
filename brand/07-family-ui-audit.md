# UI, components and motion: the family against our concepts

Measured from the live sites (computed styles, October 5, 2026) and from our four pages. Maine Education Initiative is still unreachable from this environment. [CONFIRM: its site]

## 1. What the family actually does

| | Maine Policy | Maine Civic Action | The Maine Wire |
|---|---|---|---|
| Header | Not sticky. Navy utility bar (search, uppercase menu), then the logo row on the hero. Scrolls away. | Same theme, same behavior. | Black ticker bar, logo row, white uppercase nav bar. Not sticky. |
| Headline type | Clash Grotesk 600, 64px, line height 1.0, +1px tracking, title case | Gotham 700, 64px, 1.0, +1px | Futura PT 700 masthead; Hind 500 article titles |
| Body | Red Hat Display 16px (hero kicker in Antarctican Mono) | Gotham 16px, Bricolage Grotesque for nav and some body | Futura PT 14px, Lato |
| Nav and labels | Uppercase, +1px tracking, 14 to 15px, weight 600 to 700 | Same | Libre Franklin uppercase, +1.15px |
| Buttons | 16px by 32px padding, radius 0, uppercase mono 15px, 2px border in the button color, 0.3s ease-in-out on color only | 16 by 32, radius 0, uppercase Gotham 14px, no border | Small, radius 2px, Lato uppercase 12px |
| Inputs | 48px tall, radius 0, 2px grey border | 48px, radius 0, no border | 38px, radius 2px |
| Cards and images | No cards, no shadows, no rounded corners. 0 of 6 images rounded. | Same. | Grid of white cards, 10px radius, soft shadow. 12 of 40 images rounded. |
| Section parts | Full width colored bands, a navy sign up band under the hero, three columns with icons, small boxed section label with a rule to the right, slash kicker | Same skeleton, coral instead of yellow | News grid, sidebar, newsletter box |
| Motion | 64 transitions, all 0.3s ease-in-out on color, background and border. 0 keyframe animations running. No scroll reveal (0 elements changed opacity or transform on scroll). No sticky header. Three background videos in the hero. No reduced motion rule. | 38 transitions, same. No scroll reveal. Has a reduced motion rule. | 316 transitions (theme sprawl), 0.25s ease-in-out "all". Mobile menu slides. Reduced motion rule. |

In one sentence: the family is static pages with hard corners, uppercase labels, flat buttons, color-only hover transitions at 0.3s, no scroll choreography, and a header that does not follow you.

## 2. What our concepts do

| | Signature | Bark & Sky |
|---|---|---|
| Header | Fixed. Full bar on the hero, then shrinks into a floating frosted capsule (max width 880, blur, shadow) on scroll, hides on scroll down, returns on scroll up. Progress bar. Logo swaps light to dark. | Same mechanics, transparent at rest over the video. |
| Headline | Bricolage 800, 112px, line height 0.92, tracking -3.4px, title case, marigold dot | Hedvig Letters Serif 400, 92px, 1.02, lowercase |
| Body | DM Sans 19 to 23px | Hedvig Letters Sans 19 to 21px, Plex Mono for numbers |
| Nav and labels | Sentence case, 14px, 600, no tracking | Lowercase, 14px, 400 |
| Buttons | Pills (radius 999), 16 by 26 padding, sentence case, lift 2px on hover (transform 0.25s) | Pills, lowercase |
| Inputs | Pill, 53px, 1px hairline border, tinted fill | Same, Mist fill |
| Cards and images | No cards. Column heads carry a 1.5px rule that draws itself in. Clips are 9:16 with 14px radius. | Same, plus 16 of 26 images rounded (strip, thumbnails, stills). |
| Section parts | Hero with the drawn mural, three columns, nine clip stepper pinned with crossfade, Marigold quote band, newsletter with posts, follow row, footer with the ping | Full bleed video hero with scrim, photo band, strip of nine portraits, same stepper |
| Motion | 159 transitions. Page background cross fades between sections (0.7s). Hero type rises in on load. Sections reveal on intersection (translate and opacity, 0.9s cubic bezier). Column rules draw in with staggered delays. Header morphs into capsule (0.45s). Stepper crossfades clips and panels. Footer logo draws itself and pings. Reduced motion rule present and honored. | 126 transitions, same choreography, plus the 13s hero loop. |

## 3. What would have to shift

Ranked by how visible the difference is to someone who knows the parent sites.

### Shift, for both concepts
1. **Corners.** Pills to radius 0 on buttons, inputs and the newsletter form. Clip and image corners to 0 or a small 4px. This is the single biggest tell. Done on the family pages for buttons and inputs; images still rounded.
2. **Labels and navigation.** Uppercase, +1px tracking, 14px, weight 600 or 700. Done on the family pages.
3. **Button hover.** The lift (translateY -2px) goes; the family only changes color, 0.3s ease-in-out. Ours still lifts.
4. **The header.** The morphing capsule is the most un-family thing we do. The parents' headers scroll away. Options: (a) keep a fixed bar but drop the capsule morph, the hide on scroll and the progress bar, so it is a plain navy bar that stays; (b) match the parent and let it scroll away. I would do (a): a sticky bar is a usability gain the parents lack, and a plain navy bar still reads as family.
5. **Scroll reveal and background cross fade.** The parents have none. Ours is restrained (0.9s, one axis, honors reduced motion), and it is the main thing that makes the pages feel made this decade. Recommendation: keep the section reveal, drop the page background cross fade (the family keeps white pages with colored bands, not a page that changes color), and drop the drawing column rules in favor of static marigold rules.
6. **Section label.** Add the boxed label with a rule running to the right ("What it is" in a tag). Done on the family pages.
7. **Sign up band.** The parents put a full width navy sign up band under the hero. Ours puts the form in a section. For a splash page that only points to Substack, a band under the hero with one field and one button is the family move and the shortest path to the one action.
8. **Column heads with icons.** The parents' three columns use line icons over each head. We use a rule and a bold head. Icons would be a step toward the family; I would not take it, they date fast and we have none in the system.

### Shift, Signature only
9. **Headline scale and tracking.** 112px with -3.4px tracking against the parent's 64px with +1px. Ours is a poster, theirs is a page. Bring the hero down to a 72 to 84px clamp and loosen tracking to -1px. The second line in marigold (done) matches the parent's hero exactly.
10. **The marigold dot.** The dot at the end of every headline is Signature's signature and nothing in the family does it. Keep on the hero only, drop from section heads.
11. **The footer ping.** The footer logo draws itself and the dot pulses. Drop; nothing in the family moves after load.

### Shift, Bark & Sky only
12. **Lowercase.** The family is title case headlines and uppercase labels. Lowercase serif headlines are the whole concept; keeping them is the one non-negotiable if Bark & Sky survives. Labels and buttons already went uppercase sans on Family B.
13. **The serif itself.** No parent uses a serif anywhere except the Wire's article bylines. A serif headline will always read as the odd sibling. That is the trade.
14. **Full bleed video hero.** Maine Policy also runs background video in its hero, so this is in family. Keep, with the navy scrim.
15. **Rounded portraits and thumbnails.** Square them.

### Keep, both concepts
- The stepper. It is the only place content lives and nothing in the family has an equivalent. Square the clip corners, keep the crossfade.
- Sentence case body copy and plain voice. The parents write in slogans; the contrast is the point of the project.
- The reduced motion rule, which Maine Policy lacks.

## 4. Animation audit, in detail

Our pages, measured: 0 keyframe animations running at rest, 1 keyframe rule (the ping), 125 to 159 transitions. Every transition is 0.25s to 0.9s on a cubic bezier (0.2, 0.7, 0.2, 1) or ease. All motion stops under prefers-reduced-motion. No JavaScript animation library.

| Motion | Where | Family equivalent | Verdict for the family pages |
|---|---|---|---|
| Hero type rises in on load (translate 0.9s, staggered 120ms) | h1, lede, buttons | None | Keep. Under a second, once, honors reduced motion. |
| Page background cross fade between sections (0.7s) | body | None, pages stay white | Drop. Replace with flat colored bands. |
| Section reveal on intersection (opacity and translate, 0.9s) | every section | None | Keep, shorten to 0.6s. |
| Column rules draw in with stagger | about, quotes | None | Drop. Static rules. |
| Header morphs into capsule, hides on scroll down | header | Header scrolls away | Replace with a plain sticky navy bar, no morph, no hide. |
| Scroll progress bar | header | None | Drop. |
| Button lift on hover (translateY -2px) | all buttons | Color change only, 0.3s | Drop the lift, keep a 0.3s color change. |
| Nav dot indicator (Signature) | nav | None | Drop. Underline on the current item, as Bark & Sky already does. |
| Stepper crossfade (clip and panel) | creators | None | Keep. It is content navigation, not decoration. |
| Footer logo draws itself, dot pings | footer | None | Drop. |
| Hero video loop (Bark & Sky) | hero | Maine Policy runs hero video | Keep, with poster for reduced motion. |
| Mural lines draw in (Signature) | hero | None | Already hidden on Family A. |

Net: the family pages lose the background cross fade, the capsule header, the progress bar, the drawing rules, the button lift, the nav dot and the footer ping. They keep the load rise, the section reveal, the stepper and the video. That is roughly half our motion, and what remains is the half that does a job.

## 5. Order of work, if we apply it

1. Header: plain sticky navy bar, no morph. One CSS block and three lines of script.
2. Drop page background cross fade; give each section its own flat band.
3. Square the remaining corners (clips, strip, thumbnails).
4. Button hover to color only.
5. Hero headline scale and tracking (Family A).
6. Sign up band under the hero, one field, one button.
7. Static rules, no footer ping, no nav dot, no progress bar.
8. Recut the clip placeholders with the marigold caption band.

## Footer audit, both family pages

Checked at 1400 and 390 wide after the draw finishes, against the footers of Maine Policy Institute and Maine Civic Action read from their home pages on October 5, 2026. The Maine Wire footer could not be read; its page is built by script.

What the parents put in a footer:

- Maine Policy: a support band (Donate, Sign Up), four link columns (Who We Are, What We Do, Events, Donate), a social row (Facebook, Twitter, LinkedIn, Instagram, YouTube), the copyright and a one sentence 501(c)3 statement.
- Maine Civic Action: link columns, an Our Partners column that lists Maine Policy, Maine Wire, Maine Education Initiative and Robinson Report, the copyright, Privacy Policy and Text Terms.

What ours has: the mark, one sentence, a legal line with a placeholder, and on Family B five lines of photo credits. No links of any kind.

Findings, in order of weight:

1. **No links.** The footer is the one place both parents repeat navigation, partners, social accounts and legal pages. Ours has none. Garrick's brief for the page was to point at the social accounts and the Substack. The footer should carry them a second time, where every parent site does.
2. **The parent credit is plain text.** "An initiative of Maine Policy Institute" should link to mainepolicy.org. Civic Action links to each partner; Maine Policy links to The Maine Wire and Maine Education Initiative.
3. **No partner row.** A line naming Maine Policy, The Maine Wire, Maine Civic Action and Maine Education Initiative, each linked, is the single cheapest signal that this page belongs to the family. Civic Action does exactly this.
4. **The photo credits outweigh everything else on Family B.** Five lines at 13 px, the longest block in the footer, longer than the legal line. On a phone it runs eight lines. Keep the credit, but as one line that opens, or on a credits page linked from one line. Family A has no video, so no credits, so the two footers are different heights: 170 px against 330 px on desktop.
5. **No privacy link.** The sign up band collects email addresses. Both parents link a privacy policy. Civic Action also links text terms because it sends SMS. [CONFIRM: whether Maine Policy's privacy policy covers this project or a page is needed]
6. **The legal line is unfinished.** The placeholder for legal name, address and contact is visible. Maine Policy closes its footer with a one sentence statement of what it is. Ours should say the same in one sentence once confirmed. The year is written by hand.

What passes:

- Contrast. Body 14 px at 9.4 to 1, fine print 13 px at 8.6 to 1, both on navy.
- Type sizes match the parents' footers.
- The mark. Framed stacked at 150 px on Family B, the state lockup at 96 px on Family A, each the strongest showing of its mark on the page. The draw when the page reaches its end is the one piece of motion the family pages keep below the fold, and it is quiet.
- Stacking on a phone: mark, then text, in one column.

Proposed structure, same for both pages:

- Row one: the mark. Beside it the one sentence, then the page links (About, Creators, Follow, Newsletter), then the social row (Instagram, TikTok, YouTube, Substack) in the same icon set as the follow section.
- Row two: "A project of Maine Policy Institute" linked, then the partner row: The Maine Wire, Maine Civic Action, Maine Education Initiative, each linked.
- Row three, fine print: copyright with the year set by script, Privacy, Contact, and Photo credits as one line that opens the full list.

### Footer audit, applied

Both family pages now carry the proposed footer, built in `family_footer()` in `brand/src/build_splash_family.py` and passed to the template as `footer_html`. Row one: the mark, the sentence, the page links (About, Creators, Follow, Newsletter) and the social row in the follow section's icons. Row two: "A project of Maine Policy Institute" linked, and the partner row linking The Maine Wire, Maine Civic Action and Maine Education Initiative. Row three: the copyright with the year set by script, Privacy and Contact, and on Family B a one line Photo credits toggle that opens the full list. On a phone the partners stack. Social and legal links are placeholders until the accounts and pages exist. Bark & Sky's link color rule now excludes the footer so the links stay white on navy. Capture: `brand/identity/logo-maine/family-b/footer-built.png`.

### Bar and hero draw, corrected

The bar shifted on scroll on both family pages: the static layer still set a 60 px scrolled height against 68 px at rest, the logo took a 12 px pad once scrolled, the button changed size on Family A, and on a phone the menu button moved and the Family B mark changed height. All of it was left over from the capsule bar. Every measurement of the bar is now identical before and after scroll at 1400 and 390 wide. The Family A hero mural drew in about 1.4 seconds; it now draws over about three, the same pace as the footer.

## Spacing, padding and sizing audit, both family pages

Measured from the built pages at 1400 and 390 wide: section padding, container widths, heading and paragraph sizes, grid gaps, control sizes, and the gap between each block. Contact sheets of every section sit beside the numbers.

What holds together:

- One section rhythm. Every main section pads 112 px top and bottom on desktop and 56 on a phone. The footer pads 56 over 28. The sign up band pads 22 and is meant to read as a strip.
- One container. 1280 px, 60 px side gutters on desktop, the same on both pages.
- One bar. 68 px tall, 13 px labels, 26 px mark, identical before and after scroll.
- Column paragraphs, the creators intro, and the follow row share the same sizes on both pages: 19 over 29 body, 28 px icons, 22 px row padding.

Findings, heaviest first:

1. **Controls do not share a height.** The sign up input is 48 px. The button beside it is 49 on Family A and 47 on Family B. The hero button is 49 on A and 47 on B, and the hero text link is 45 on both. Set one control height, 48, and let the hero and sign up buttons, the input and the text link all meet it.
2. **Family A mixes two sizes in one row.** The hero button is 15 px and the text link next to it is 13. The sign up button is 15 beside a 14 px label and 12 px fine print. Family B holds 13 throughout. Pick one label size per page for buttons and links.
3. **The follow row's handle is wrong size on both.** On Family A the handle is 17 px under a 15 px label, so the secondary line is larger than the primary. On Family B the handle is 13 on desktop and 11 on a phone, under the 12 px floor the audit set. Handle 14 under a 15 label on both.
4. **The three columns are too narrow for their type.** Each column in the about section is 198 px wide with 19 px text, about 20 characters a line. The ragged edge is visible in the sheet. Either set the columns at 17 over 27 or give the column group more of the row than the heading takes.
5. **Column labels are smaller than their body.** 18 px bold over 19 px body on A, 17 regular over 19 on B. A label should sit at or above its body size. 19 or 20 on both.
6. **Family A's hero has dead space on desktop.** The text block starts 86 px below the bar and ends around 400 px, and the section runs to 825 with nothing in the lower third but blue. Either center the block on the section as Family B does, or trim the minimum height.
7. **Family A's kicker is cramped.** Zero margin between "A Maine Policy Institute project" and the headline. Family B gives it 18 px. Give A the same.
8. **The creator's name outruns the section headings.** Panel name 64 px against 52 px section headings on Family A, 62 against 60 on B. On a phone it flips: 31 against 34 on A. Settle the scale: the name can lead, but by the same step at every width. 60 and 36 on both pages.
9. **The clip fills the phone.** The clip is 536 px tall on A and 502 on B in an 844 px viewport, so the name and the story fall below the fold on every panel. Cap the clip at about 58 vh on phones.
10. **Small text sits at the floor.** Kickers, place labels and fine print are 12 px on A and 12 to 13 on B. The parents use 13 to 14 for the same jobs. Hold 13 as the minimum.
11. **Off grid values.** The phone gutter is 17.55 px (4.5 vw), the hero button row sits 19 px below the paragraph, the follow heading has 28 px below it on A and 32 on B. Fix the gutter at 18 or 20, the row at 20, the heading at one value.

Sheets: `brand/identity/splash-family-b/audit-spacing-1400.png` and `audit-spacing-390.png`.

## Usability and conversion audit, both family pages

The page has three conversions, in this order: watch a clip, follow an account, subscribe to the newsletter. Scored against a standard homepage framework adapted to that, out of 50. Both pages share one structure and one set of behaviors, so they score together; the differences are noted.

| Section | Score | Why |
|---|---|---|
| First impression | 7 of 10 | Headline under ten words and plain. Subhead gives the specifics. Clear primary button, one secondary link. Family B's video is the stronger first frame; Family A's hero leaves the lower third empty on desktop. The only trust signal above the fold is the kicker naming the parent. |
| Value communication | 7 of 10 | Three columns say what, why and where in the project's own voice. Problem to solution is there in the hero copy. The "why" column is a placeholder until the client writes it. No proof yet, by design, before the shoot. |
| Trust | 4 of 10 | Parent and partner links now carry the family's credibility. No faces, names, numbers or press yet. Seven visible placeholders. No privacy link target. |
| Usability | 6 of 10 | Alt text on every image, visible focus ring, language set, honest headings. No skip link. No favicon. Family A loads 8.8 MB and Family B 13.9 MB on first view. Nine pinned panels put the follow row more than 8,000 px down. |
| Conversion mechanics | 5 of 10 | The newsletter button goes to the wrong place. The sign up field discards what is typed. Outbound links carry no tracking. No share card for a social first project. |
| **Total** | **29 of 50, C** | A sound structure with its mechanics unfinished. |

Findings, heaviest first:

1. **The sign up field is decorative.** The input sits outside any form, has no name, and the Sign up button is a plain link to the Substack subscribe page. A visitor types an address, clicks, and lands on a page that asks for it again. Substack prefills from the address in the link, so the fix is small: a form whose submit sends the typed address to the subscribe page, or Substack's own embed. Until the publication exists the field should not be shown at all.
2. **"Get the newsletter" does not go to the newsletter.** The bar button and the hero link both go to the follow row, where Substack is one of four items. The sign up band has its own anchor now. Point both at it. The Follow item in the nav already covers the follow row.
3. **No share card.** No Open Graph or Twitter card metadata, so a link posted on Instagram, TikTok, X or in a group chat shows no image and a bare title. For a project whose audience arrives from social feeds this is the first conversion surface. Add title, description, a 1200 by 630 image from the hero loop, and the page URL.
4. **Nothing is measurable.** Every outbound link, to Substack, to the accounts, to the parents, goes out bare. Add a source parameter to each so the newsletter and the accounts can see what the page sends them, and add one analytics tag the parents already use. [CONFIRM: which analytics Maine Policy runs]
5. **Page weight.** Nine creator clips are GIFs of about a megabyte each, loaded up front. The hero loop is 4.4 MB. On a phone over cellular the first view costs 9 to 14 MB. Convert the clips to muted video, load them as their panel approaches, and keep the hero loop under 2 MB.
6. **The follow row is a long way down.** Nine pinned panels before the follow and newsletter sections. The sticky bar button mitigates it, once it points at the right place. Consider a follow strip after the fourth or fifth panel, or let a visitor leave the stepper with a visible "skip to follow" link.
7. **Placeholders are live.** Seven visible: three "[CONFIRM]" notes, "[@handle]" four times, "PLACEHOLDER" on every clip card. Every creator handle and every social link goes to "#". Expected before launch, but the page should not go to the client's board with them showing. Mark them in the build so a flag lists what is open.
8. **The title is only the name.** The browser tab, bookmarks and search results read "Generation Maine". Append the one line: "Generation Maine: young Mainers on the rules that shape their lives."
9. **No skip link, no favicon.** Both are one line each.
10. **Hidden sections remain in the page.** The quote band and the newsletter posts are hidden by CSS but still in the document with placeholder copy. Remove them from the build when lean, so they cannot leak to a reader or a crawler.

What already works: one headline, one promise, one primary action. Plain copy throughout. The hero button lands on the first clip. The bar stays visible with the newsletter action on every scroll position. Reduced motion is honored, the video is muted and has a poster, and the footer now repeats every path out.

Quick wins, under a day: 1, 2, 3, 8, 9. Strategic: 4, 5, 6.

## Phone carousel QA, Concept A creators section (Oct 7, 2026)

Measured at 320, 360, 375, 390, 430, 768 wide and 844 by 390 landscape, with a real nudge of the track, a segment tap, arrow keys and a resize across the breakpoint.

Found and fixed:

- All nine clip GIFs loaded at page open, about 8.7 MB on a phone. Clips now carry a data-src and load when their card is current or next door. Two load at open.
- The card index was derived from scroll distance divided by a fixed card width. It lagged by one on tablets and landscape phones, and a segment tap landed the card off the gutter. The current card is now the one whose left edge sits nearest the gutter, and taps scroll by measured geometry.
- Cards snapped to center, so the first card sat at the gutter and the rest did not. Cards now snap to the gutter.
- A card was 730 to 840 px tall, so the clip alone filled a phone screen and the name and story sat below the fold. The clip is a 4:5 crop capped at 44 percent of the screen height, so the name and the first lines of the story share the screen with it. Real clips will be shot knowing the top of frame shows here.
- Segment buttons were 4 to 16 px wide and 28 px tall. The position row now sits above the cards, counter and next name on one line, nine segments 44 px tall across the full width on the next.
- The three social links overflowed the card by 3 px at 320. They wrap now.
- The heading block kept the first tint while the carousel changed color, leaving a seam. Both change together.
- The track was not reachable by keyboard. It is a labeled carousel region, focusable, with left and right arrow keys, and the current segment carries aria-current.
- Resizing from phone to desktop could leave the stage clip without a source. The resize handler loads it.

Known and accepted: on a landscape phone the clip cap gives a wide crop of a vertical clip. On a 320 by 568 screen the social links of the first card sit just below the fold.

Follow-up, same day: the 4:5 crop limited the social preview, so a tap-to-expand viewer was added. Tested at 320, 375 and 390 wide: the frame holds 9:16 within 1 percent, the close button is 48 px, focus moves to it on open and back to the clip on close, body scroll locks, slides load on demand, Escape, backdrop tap and the back button all close it, and the page scroll position is unchanged after closing. On desktop the viewer is display none and a click does nothing.
