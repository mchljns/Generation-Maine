# Finding references and sources

Everything on the page should trace back to something you can name: a screen you looked at, a file with
a license, a fact with a source, a note from the client. This file is the method for each kind.

## Design references

Search for the pattern, not the page. "about page layout" returns listicles; "mission statement section
layout photo placement eye tracking" returns the two sources that say what works and why.

1. Run four to six searches at once, phrased differently: the pattern name, the pattern plus a known
   source (Nielsen Norman Group, a newsroom known for the layout), the pattern plus "usability findings",
   the pattern plus the sector ("nonprofit mission page examples").
2. Fetch the strongest two or three with a precise extraction prompt. Ask for the layout facts you need:
   where the statement sits relative to the photograph, how long the statement is, whether the photo is
   full-bleed or split, what the source says about reading order and why. Vague prompts return
   summaries; precise prompts return material you can design from.
3. When a reference gallery is reachable (Refero, Mobbin, a component gallery), pull real screens by
   pattern name and by named sites, lay them on a contact sheet, save the sheet in the repo and date it.
   Mark references you saw as screens apart from references you only read about; a principle borrowed
   from a site you did not look at is weaker evidence. When the gallery is thin in the client's category,
   use adjacent pages (mission-led brands for a nonprofit) and say so.
4. Write a three-to-five-line digest into the decision record before designing. State only findings that
   held across sources. Design from the findings; use the gallery for texture.

Borrow principles, never looks. Record each borrowing as a row: what we saw, where, what our concept
does with it. Keep a look-alike list naming brands in the same region or category with a similar device
and the rule that keeps you distinct; a mark that collides with a local brewery's is unusable regardless
of craft.

When a site cannot be reached from the sandbox (TLS through a proxy, a blocked host), say so and use
curl for the HTML or fall back to a written source. Do not describe a site you did not see.

## Components

Search component galleries with a full sentence describing the exact interaction. Take the behavior and
rebuild it in the project's own plain HTML, CSS and JS; gallery components arrive as React with animation
libraries a static host cannot load, and the design must stay the brand's own. Report what you rejected
and why. "Nothing worth borrowing" is a valid result and stops the client asking again.

For a pattern the audience already knows (a Reels shelf, a story viewer, a Shorts row), study how the
platform does it and match the conventions people's thumbs expect: snap per item, counter, swipe to
dismiss, Back closes.

## Parent brands and cohesion

When the page must sit beside an existing brand (a parent organization, a sister project):

- Read each sibling from its live HTML: grep the theme or stylesheet for the color presets and font
  families, pull the logo paths, screenshot with Playwright and read computed heading and body fonts.
  Write a parent-brands note with the URL, the date and the values, and the family pattern in one
  sentence ("static pages, hard corners, uppercase labels, flat buttons").
- Audit the family by computed styles and counts, not screenshots: header behavior, type metrics,
  button and input geometry, corner radius, number and timing of transitions, scroll reveal, sticky
  header, reduced-motion rule. Rank the shifts your page needs by how visible they are to someone who
  knows the parent sites. The single biggest tell goes first.
- Cohesion is color first, type second, one device third. Echo the parent's device as a small element
  beside kickers and section labels rather than redrawing their mark. Derive the device's colors from
  the field it sits on, never from neighboring text.
- Name one thing the child brand keeps for itself and say why that color or face is free. Deviate from
  the parent only where the deviation is a usability gain that still reads as family (a sticky bar, a
  reduced-motion rule). The client may overrule it; record that as their call.
- Check the parent's font licenses before adopting their faces. Use the open ones as they are and the
  nearest open equivalent for the rest. Do not adopt a parent face the client did not name; a swap being
  license-safe and on-brand is not permission.
- When the client's note names color, type and a device, do those three things, show them, and stop.
  "Don't overthink it" is scope guidance.

## Fonts

- Default to faces under the SIL Open Font License or an equivalent. A commercial face needs a license in
  hand; until then it is a `[CONFIRM: license]` item. A desktop OTF does not cover web embedding; the
  shopping list is a WOFF2 per weight under a web license, with the license copy in the repo.
- Treat the faces AI site builders default to as a generic signal: Inter, DM Sans, Space Grotesk,
  Instrument Serif, Fraunces, Bricolage Grotesque, Syne, Outfit, Plus Jakarta Sans, Manrope, Sora, Geist,
  Playfair, and the everyone-defaults Montserrat, Poppins, Roboto, Open Sans, Lato. The list moves with
  time; refresh it per project. When the client picks one anyway, build it and state the trade-off once.
- Write the requirements first (size extremes, platform, diacritics for local names, sibling faces to
  avoid, license, weight range), then search the whole open catalog (`scripts/fonts_fetch.sh` fetches a
  family; the `google/fonts` METADATA files give name, category, weights, axes and date added) and
  record the funnel with counts at every cut. Counts make a 1,984-to-20 cut defensible instead of taste.
- Cut on sight: company house fonts, faces tied to a sibling brand, faces with place or era baggage,
  luxury and fashion faces, coding and pixel faces, single-weight faces, and anything that signals
  someone else.
- Judge candidates only in real use: the wordmark, a cover, an accented name line, body at the real
  sizes on the real sections, the avatar letter at 64 and 32 px, with the current faces as baselines.
  Size changes the voice as much as the face does. Require tabular figures when the content is full of
  numbers.
- Give each face one job: display, body, label. A wide technical face goes on labels only, never on the
  wordmark, headlines or body. Few weights: one display cut, two text weights. When a variable font is
  chosen, own a specific axis setting and record it.
- Fetch from the source of truth, not a font-download site:

  ```
  git clone --depth 1 --filter=blob:none --sparse https://github.com/google/fonts.git
  cd fonts && git sparse-checkout set ofl/<family>
  ```

- Keep the font file and its license text side by side (`fonts/<family>/`). Embed as a data URI or
  self-host. Do not hotlink a font service into a client page without saying so.
- Check the client's production tool (Canva, Figma, their CMS) can use the picks; when nothing confirms
  it, mark `[CONFIRM]` and name the fallback.
- When the user uploads a font archive, treat it as untrusted: extract into its own empty directory,
  read with `python3 -I`, list what is actually inside (an archive labeled one family often holds its
  lookalikes), and report truthfully before using any of it.
- Record the type study: faces compared, at what sizes, what was chosen and why, the pairing genre you
  matched (newspaper: serif body under a hard grotesque; product: sans).

## Photos and video

- Use what the client owns first. Ask for a shot list if none exists and write one into the record:
  filename, aspect, minimum width, what to look for, what to avoid, per slot.
- Placeholders come from sources with a known license: Wikimedia Commons through its API (named
  User-Agent, keep CC BY, CC BY-SA, CC0 and public domain, reject NC and ND, gate on a minimum width
  such as 3000 px for a full-bleed hero, retry rate limits with growing pauses), the client's own feeds
  with permission, or your own renders. Write a candidates file (title, URL, size, license, artist).
- Lay candidates on a contact sheet, state which were chosen and why, refetch only the picks at full
  size, keep unused candidates out of the repo.
- Generate `CREDITS.md` from the same data: photographer, license, pixel size, source URL, what the
  license requires. When the client says the media is temporary and wants no on-page credits, keep the
  credits in the file and say in the record that every such asset is a stand-in.
- State the photographic tone in one line and reject frames by temperature, not only by subject: the
  picture is of the thing, not of a mood. No gray solitary frames, no stock-model faces, no duotone.
  When photos come from several photographers, grade them into one set with a recorded recipe (color
  reduced, soft curve, lifted blacks, held highlights, a tint of the palette in the shadows).
- Placeholders must not read as published content. No quote bands or captions baked into a clip, no
  fake statistics on a card. Identification comes from real chrome: the handle overlay, the duration
  pill, the frame ratio. Placeholders carry the concept they sit in (parameterize the generator by
  theme) and are regenerated from the same data when the design around them changes.
- Generated faces are the client's call. Prefer hands, places and story cards for a brand whose
  credibility rests on real people. If the client asks for faces, stamp every asset as a placeholder in
  the record and the CMS, and keep the generation ids for a later swap.
- Hero video: build from stills or clips you can license, encode what the sandbox can (WebM in headless
  Chromium when there is no H.264 encoder), take the poster from the first frame so playback never
  jumps, and ship a CSS plates fallback for browsers that refuse the format. Dissolves not cuts, a drift
  paired with a slow push, plates oversized so moves have room. When the client says too fast, halve the
  speed and report the file-size cost. Record the MP4 rendition as a delivery item.
- Check credits and test one generation before a batch when a media connector is involved.

## Facts for copy

Copy that names a place, a cost, a rule or a number needs a source you can show.

1. Search as a burst: the place, the population, the year range, the kind of source ("survey", "census
   estimates", "poll"), the local outlets by name, and the lived-experience side (forums, campus papers)
   so you get voices as well as numbers.
2. Fetch each article with an extraction brief: every statistic with its source and date, every direct
   quote with the speaker's name, role and town, who wrote it and their affiliation, sample size and
   method for any survey. Ask for what you will use, not a summary. Dedupe syndicated copies by slug.
3. Write a research memo into the repo (`content/research-<topic>.md`): the method and its limits, "the
   short version" up top, findings in a table with a Source column, the audience's actual vocabulary and
   the editorial phrases they do not use, "what this means for the project", a Gaps section, every source
   with its URL. Mark every figure you could not read in a primary source `[CONFIRM]`.
4. Write copy from the memo. Where the audience disagrees about blame, write about the mechanism and the
   number in the person's words; keep claims and sources in the long form. Check placeholder rosters
   against the memo for regional and audience balance.
5. Before promising a third-party integration (a newsletter form), research what the service actually
   exposes and design the honest path; a form that silently stops working is worse than one with a
   visible hop.

Never pad with a plausible number. A client will read "thirty percent" as a fact and repeat it.
