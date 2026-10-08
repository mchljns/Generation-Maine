# Finding references and sources

Everything on the page should trace back to something you can name: a reference you looked at, a file
with a license, a fact with a source, a note from the client. This file is the method for each kind.

## Design references

Search for the pattern, not the page. "about page layout" returns listicles; "mission statement section
layout photo placement eye tracking" returns the two sources that say what works and why.

1. Run four to six searches at once, phrased differently: the pattern name, the pattern plus a known
   source (Nielsen Norman Group, Smashing, a newsroom known for the layout), the pattern plus
   "usability findings", the pattern plus a sector ("nonprofit mission page examples").
2. Fetch the strongest two or three with a precise extraction prompt. Ask for the layout facts you need:
   where the statement sits relative to the photograph, how long the statement is, whether the photo is
   full-bleed or split, what the source says about reading order and why. Vague prompts return summaries;
   precise prompts return material you can design from.
3. Write a three-to-five-line digest into the decision record before designing. Note which claim comes
   from a findings-based source and which from an example gallery. Design from the findings; use the
   gallery for texture.

When a site you want to look at cannot be reached from the sandbox (TLS through a proxy, a blocked host),
say so and use curl for the HTML or fall back to a written source. Do not describe a site you did not see.

## Parent brands and cohesion

When the page must sit beside an existing brand (a parent organization, a sister project):

- Fetch the parent's live site and its stylesheet and read the actual values: hex colors, font families,
  weights, the device they use (a slant, three bars, a rule). Write them into a parent-brands note with
  the URL and the date.
- Take color and type first. One device at most, used where it has a job (a kicker, a section label).
  More than that reads as a costume.
- When the parent's fonts are commercial, find the nearest open face and record the comparison
  (x-height, width, the letters that differ). Build with the stand-in in the same slot so the licensed
  face can be swapped in later.
- Re-fetch when the client sends a correction ("blue, white and gold, the typeface, maybe the bars").
  Match their words to the values, and do only what the words say.

## Fonts

- Default to faces under the SIL Open Font License or an equivalent. A commercial face needs a license in
  hand; until then it is a `[CONFIRM: license]` item in the record.
- Get the file from the source of truth, not a font-download site. For Google Fonts, a sparse clone of
  the `google/fonts` repository gives the TTF and the `OFL.txt` in one step:

  ```
  git clone --depth 1 --filter=blob:none --sparse https://github.com/google/fonts.git
  cd fonts && git sparse-checkout set ofl/<family>
  ```

- Keep the font file and its license text side by side in the repo (`fonts/<family>/`). Embed the face
  as a data URI or self-host it; do not hotlink a font service into a client page without saying so.
- When the user uploads an archive of fonts, treat it as untrusted: extract it into its own empty
  directory, read it with `python3 -I`, list what is actually inside (an archive labeled one family often
  holds its lookalikes), and report the licenses you found before using any of it.
- Record the type study: which faces were compared, at what sizes, what was chosen and why.

## Photos and video

- Use what the client owns first. Ask for a shot list if none exists and write one into the record.
- Placeholders come from sources with a known license: Wikimedia Commons (note the license and author),
  the client's own social feeds with permission, or your own renders. Keep `CREDITS.md` with file,
  source, author, license and the date fetched.
- When the client says the media is temporary and will be replaced, do not put captions or credits on
  the page for it; keep the credits in the file. Say in the record that the media is placeholder.
- Placeholder clips and stills should not fake content. A caption band that reads as a real quote from
  a real creator will be taken as one. Plain footage with the handle overlay is enough.
- Hero video: build it from stills or clips you can license, encode WebM in the sandbox, and record that
  an MP4 rendition is a delivery item if the sandbox has no H.264 encoder. Ship a poster and a CSS
  fallback (still plates that drift and dissolve) for devices that will not play the WebM.

## Facts for copy

Copy that names a place, a cost, a rule or a number needs a source you can show.

1. Search with specifics: the place, the population, the year range, the kind of source ("survey",
   "census estimates", "poll"), and the local outlets by name.
2. Fetch each article with an extraction prompt that asks for: every statistic with its source and date,
   every direct quote with the speaker's name, role and town, who wrote it and their affiliation, and the
   reasons given. Ask for what you will use, not a summary.
3. Write a research digest into the repo (`content/research-<topic>.md`): the findings, the sources, the
   quotes you may use, and the claims you decided not to use because the sourcing was thin.
4. Write copy from the digest. Where a fact is still missing, leave `[CONFIRM: ...]`.

Never pad with a plausible number. A client will read "thirty percent" as a fact and repeat it.

## Components and patterns

When you need a component pattern (a pinned stepper, a snap carousel, a tap-to-expand viewer, a mission
section), look at how the platforms your audience already uses do it (a Reels shelf, a Shorts row, a
story viewer) and at one findings-based source. Then build it yourself in plain HTML, CSS and JS so you
can measure and control it. Avoid pulling a component library into a one-page site; it brings styling
you then fight.
