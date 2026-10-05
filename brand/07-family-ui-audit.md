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
