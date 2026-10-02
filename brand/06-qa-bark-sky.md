# Bark & Sky splash: strict QA

October 2, 2026. Reviewed `brand/identity/splash-bark-sky/index.html` at 1440x900, 1280x650, 1024x700, 820x1180 and 390x844, through every section and state: bar at rest, capsule, sheet, keyboard focus, hover, the scroll scrub, stepper first and last, the form empty and submitted, follow, footer. Measured contrast, tap sizes, type sizes, overflow, console errors and font loading. No console errors, no horizontal overflow, both fonts load.

Severity: **P1** fix before anyone outside the team sees it. **P2** fix before launch. **P3** a judgment call, decide once.

## Brand design

| # | Finding | Why it matters | Fix |
| --- | --- | --- | --- |
| B1 **P1** | The hero is centered and every other section is left-aligned. The kit's Bark & Sky direction centered everything: the end card, the Substack header, the covers. The site mixes the two. | The concept's one layout idea is "centered and airy." Breaking it after the first screen makes the page read as Signature's layout with a different coat. | Decide once. Recommended: center the section headings and their ledes (about, creators, in their words, newsletter, follow) and keep the two-column stepper and the posts list as they are. Alternative: left-align the hero. Not both. |
| B2 **P1** | The placeholder clips carry Signature's brand into the page: the Pine caption band and the Marigold dot sit inside the Bark & Sky stepper. | Marigold is the one color this concept has no place for. The comparison the client is making is contaminated by it. | Build a Bark & Sky set of placeholder GIFs (Bark band, no dot, Hedvig Sans caption) with the same script and a palette switch. |
| B3 **P2** | The nav lockup is small and pale. At 24 px the solid state is a 21 px smudge beside a 20 px serif, and the lockup is 186 px wide, so the bar feels empty. | The lockup is the only brand presence on 80 percent of the scroll. | Set the nav lockup to 28 px at rest and 24 px in the capsule. Consider the compact lockup instead of the horizontal in the bar. |
| B4 **P2** | Straight quotation marks in the in-their-words section. | A serif concept at one weight lives on typographic detail. Straight quotes are the first thing a type-literate reader sees. | Curly quotes, hanging punctuation on the opening quote, and the closing quote inside the sentence. Applies to Signature too. |
| B5 **P2** | Hierarchy is weak where the concept forbids bold. The quote footer sets name and town in the same size and nearly the same color on Bark. The clip header does the same with handle and name. | One weight means hierarchy must come from size or color. Here it comes from neither. | Name in the serif at 17 px, town in the sans at 13 px in Sky at 70 percent. Same move on the posts list and the clip header. |
| B6 **P3** | Brand names are lowercased: tiktok, youtube, instagram, substack. The concept says all lowercase for nav and labels. | These are trademarks. Lowercasing them is a voice choice some partners will object to, and the platforms' own guidelines ask for their casing. | Decide once. Recommended: keep the lowercase rule for the brand's own words and exempt third-party names. |
| B7 **P3** | The hero carries the state twice in one screen: the lockup in the bar and the mark above the headline. | Not wrong, but the kit's version used the wordmark alone in the bar. | If the mark stays in the hero, the bar could carry the wordmark alone until the capsule forms. |

## UX

| # | Finding | Why it matters | Fix |
| --- | --- | --- | --- |
| U1 **P1** | On common laptop screens the hero's call to action is below the fold. At 1280x650 the headline is cut and neither the lede nor the buttons show. At 1024x700 the buttons sit 63 px under the fold. | The first screen on a 13 inch laptop shows a mark and half a headline. | Size the hero to the viewport: mark `height:min(200px,22vh)`, headline `clamp(44px, min(7.4vw, 11vh), 104px)`, lede margins tightened, so the buttons sit above the fold down to 650 px tall. |
| U2 **P1** | The signup form gives no message on an invalid submit. The field gets a focus ring and `aria-invalid`, nothing else. | A blank reaction to a tap reads as broken. | Show one line under the field: "Enter an email address like you@example.com." Announce it with `aria-live`. Same fix for Signature. |
| U3 **P2** | After a successful submit the button stays "subscribe," disabled with no visual change, and the field stays editable. | The confirmation line appears, but the control contradicts it. | Button text becomes "sent," field becomes read-only, and the note line hides. |
| U4 **P2** | On phones the three platform marks under each creator are 22 px icons with no label and a 22 px hit area. | Below the 44 px minimum and nothing says which link is which until the screen reader reads the label. | Pad each to a 44 px target and keep the icon at 22 px. |
| U5 **P2** | The position row text is 11 px on phones and the clip duration badge is 10 px. | Under the 12 px floor the project set for itself. | 12 px minimum everywhere. |
| U6 **P3** | The phone menu sheet is four links and a button, with most of the screen empty. | Works, but the concept's calm reads as unfinished here. | Add the one-line disclosure and the three platform marks under the links, as the end card does. |
| U7 **P3** | Section reveals (rules drawing, rows rising) fire late when a user jumps by anchor from the bar. The follow row arrives after the screen does. | Visible as a flash of empty section on fast navigation. | Lower the reveal threshold for anchor jumps, or reveal on first paint when the section is the scroll target. |

## UI and visual

| # | Finding | Fix |
| --- | --- | --- |
| V1 **P2** | The focus ring on the email field doubles the pill: a 2 px Clay outline 3 px outside a 1.5 px border. On phones it reads as two rings. | Use the border itself as the focus state (border-color Bark) and drop the outline on inputs only. |
| V2 **P2** | The stepper's clip column is wider than the clip. At 1440 the clip is 315 px in a column of about 490, which leaves an empty gutter before the text. | Set the column to the clip's width (`auto`) and let the text column take the rest, or center the clip in its column. |
| V3 **P2** | The lede under "the creators" and the pinned block are 300 px apart on desktop. | Reduce the stories padding on the first step so the clip is in view when the heading is. |
| V4 **P3** | The hero mark's bottom lines are heavier than the top (the drawing's weight gradient). Centered over a light serif it reads as top-light. | Try the mid cut at this size, or the full cut at 160 px. |
| V5 **P3** | The follow row icons are 28 px with 14 px below them, the platform name at 15 px and the handle at 17 px. The handle outranks the name. | Name at 15 px in Bark, handle at 15 px in Clay. |

## Accessibility

| # | Finding | Fix |
| --- | --- | --- |
| A1 **P2** | Clay on Sky measures 4.97 to 1. It passes AA for text but not for the 11 to 13 px kickers if any land on Sky. | Keep Clay text off Sky, or darken Clay to #5E4E43 (about 5.8 to 1). |
| A2 **P2** | Nav links in the bar are 26 px tall. Fine for a pointer, tight for touch on tablets where the bar still shows. | Pad to 40 px. |
| A3 **P3** | The lowercase is a CSS transform, so screen readers get the source casing. Good. The forced single weight (`font-weight:400!important`) also strips `<b>` from bios and quotes. | Keep the transform. Replace the universal weight rule with a list of the elements that set weight, so `<b>` in a creator's own words can still mean something. |

## Measured

| Check | Result |
| --- | --- |
| Bark on Sky | 11.89 to 1 |
| Clay on Paper | 6.57 to 1 |
| Clay on Mist | 5.92 to 1 |
| Clay on Sky | 4.97 to 1 |
| Sky at 70 percent on Bark | 7.03 to 1 |
| Horizontal overflow | none at 390, 1440 |
| Console errors | none |
| Fonts | both Hedvig faces loaded |
| Hero CTA above fold | 1440x900 yes, 820x1180 yes, 1024x700 no, 1280x650 no |

## Not a problem

- The capsule, the scroll scrub from Sky to Paper, the sheet, keyboard focus on links and buttons, reduced motion, and the stepper's first and last steps all behave.
- A blank frame appeared once when scrolling up inside the stepper. It did not reproduce on two further runs on either concept. Treat as a screenshot artifact unless seen in a browser.

## Order of work

1. U1 hero fit, B1 alignment decision, B2 placeholder clips in the concept's colors.
2. U2 and U3 form states, B3 nav lockup size, B5 hierarchy without bold, U4 and U5 touch and type minimums, V1 focus ring, V2 stepper column.
3. B4 quotes, B6 trademark casing, the P3 list.

Items U2, U3, B4 and A3 apply to Signature as well and should be fixed in the shared template.
