# Deploy and verify

A push is not a deploy. Never say "live" until you have proved that what is served matches what you
built, from every address the client might open, after the host's cache window has passed. Clients open
the link on a phone the moment you say "live". If the old page is there, you have spent a round of
trust, and the next "it's live" is doubted too.

## Hosting a preview

- Use the simplest static host the user can authorize. On GitHub Pages that is a branch holding a
  standalone copy of the built page and its media, served directly with a `.nojekyll` file and no
  workflow; a workflow-based deploy fails on a private repo and a stray workflow can block branch
  serving. Check repo visibility and plan before promising a Pages URL.
- Making anything public (a branch, repo visibility) is the user's explicit call. When the permission
  system blocks it, explain the one tap and wait. Afterwards disclose the side effects: the brand files
  and theme source are now public too, and a public URL is not a link-gated artifact.
- Publish each concept under its own stable path key and keep that address through the project. Record
  the URL and the exact refresh steps in the decision record.

## Caches

- **GitHub Pages** sits behind a CDN with `cache-control: max-age=600`. After a deploy, edges and
  browsers can serve the previous copy for up to ten minutes. The Pages build itself can also sit in
  "waiting" for many minutes.
- **Netlify, Vercel, Cloudflare Pages** invalidate on deploy, but browsers still hold copies for the
  `max-age` they were given. Read the headers rather than assuming.

## The verification loop

`scripts/verify_deploy.sh <local-file> <public-url> [cache-seconds] [max-wait]`

1. Confirm the push landed: fetch and compare local HEAD with the remote deploy branch.
2. Hash the local built file. Fetch the served file with a throwaway query (`?n=$RANDOM`) so no cache
   answers, hash it, compare. Loop every fifteen seconds until it matches or the wait runs out. Compare
   hashes; do not grep status codes (a proxy's `200 Connection Established` fools a grep) and do not
   stop at a 200 (a 200 on the old page proves nothing). Check each media file's status and byte count.
3. Wait out the cache window (ten minutes for GitHub Pages).
4. Fetch again from every address form without a query: the directory, `index.html`, and with a query.
   All must match. Print `age`, `last-modified` and `x-cache` beside each so a stale edge is visible.
5. Only then say "Deployed and verified against the server", with the link, the build stamp and the
   elapsed time.

Screenshot the live URL itself at desktop and phone when the sandbox browser can reach it (pin the
proxy's CA with the browser's own flag; never disable verification). When it cannot, screenshot the
identical local build and say so, relying on the hash match. Confirm the live page serves this
concept's own assets, not a sibling's.

When the served hash does not move, inspect the Pages deployment through the API:

```
gh api repos/<owner>/<repo>/actions/runs?per_page=3
```

A run stuck in `waiting` far beyond the usual minute is cancelled (`.../runs/<id>/cancel`) and a fresh
commit pushed. Run long polls in the background and read their output before continuing.

## Build stamps

During the preview phase, put a small stamp in the footer legal row: the first seven characters of the
built file's hash and the UTC time. Muted color, tabular numerals, right-aligned. When the client says
"I'm not seeing the update", ask for the stamp. It settles in one message whether the server or their
browser is behind. Remove the stamp at delivery.

## Iframes and toggles

A concept toggle that loads pages in an iframe shows the previous build for a full cache window unless
the iframe source carries a version: `../v2/index.html?v=<hash>`. Replace the placeholder at build time.
Browsers cache framed documents more stubbornly than top-level pages. Retire the toggle as soon as the
client picks, and serve the page directly.

## Retiring addresses

When a path is retired (a concept dropped, a variant folded in, a rename), leave a one-line page at the
old path:

```
<!doctype html><meta charset="utf-8"><meta http-equiv="refresh" content="0; url=../v2/">
<link rel="canonical" href="https://host/site/v2/"><title>Moved</title><p>Moved to <a href="../v2/">/v2/</a>.</p>
```

Old links in messages and client notes keep working. Update canonical and share URLs. Keep earlier
previews reachable at their own paths for comparison until the client says otherwise. Remove deploy
scaffolding once it is no longer needed.

## When the client still sees the old page

The server side is settled by the loop above. If it passes and the client still sees the old page:

1. Ask what the footer stamp says and what device and width they are on.
2. Say which changes only show at some widths. A carousel or a tap-to-expand viewer is invisible in a
   desktop window wider than the breakpoint, and a desktop-only change is invisible on a phone.
3. If the stamp is old, the copy is in their browser. Give the private-tab or hard-reload step. Explain
   once that the plain address serves the current build. Do not hand out cache-busting links as if they
   were a second address; they read as a second site.
4. Do not redeploy to "fix" it; a redeploy restarts the cache window.

## Delivery

Before handing over: remove the build stamp, resolve or list every `[CONFIRM]`, confirm fonts and media
licenses are in the repo, record the MP4 or other renditions still owed, and write the final record
entry with the live address and the commit.
