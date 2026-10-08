# Deploy and verify

The rule: never say a page is live until you have proved what is served matches what you built, from
every address the client might open, after the host's cache window has passed. Clients open the link on
a phone the moment you say "live". If the old page is there, you have spent a round of trust, and the
next "it's live" is doubted too.

## Static hosts and their caches

- **GitHub Pages** sits behind a CDN with `cache-control: max-age=600`. After a deploy, edges and
  browsers can serve the previous copy for up to ten minutes. The Pages build itself can also sit in
  "waiting" for many minutes; when it does, a fresh commit restarts it.
- **Netlify, Vercel, Cloudflare Pages** invalidate on deploy, but browsers still hold copies for the
  `max-age` they were given.

## The verification loop

`scripts/verify_deploy.sh <local-file> <public-url> [cache-seconds] [max-wait]`

1. Hash the local built file (`sha1sum`).
2. Fetch the served file with a throwaway query (`?n=$RANDOM`) so no cache answers, hash it, compare.
   Loop every fifteen seconds until it matches or the wait runs out. Compare hashes; do not grep status
   codes (a proxy's `200 Connection Established` will fool a grep).
3. Wait out the cache window (ten minutes for GitHub Pages).
4. Fetch again from every address form, without a query: the directory, `index.html`, and with a query.
   All must match. Print the `age` header beside each so a stale edge is visible.
5. Only then say "live", and name the build.

Also check the Pages deployment status with the API when a deploy seems slow:

```
gh api repos/<owner>/<repo>/actions/runs?per_page=3
```

A run stuck in `waiting` for more than ten minutes: cancel it (`.../runs/<id>/cancel`) and push a fresh
commit.

## Build stamps

During the preview phase, put a small stamp in the footer legal row: the first seven characters of the
built file's hash and the UTC time. Muted color, tabular numerals, right-aligned. When the client says
"I'm not seeing the update", ask for the stamp. It settles in one message whether the server or their
browser is behind. Remove the stamp at delivery.

## Iframes and toggles

A concept toggle that loads pages in an iframe shows the previous build for a full cache window unless
the iframe source carries a version: `../v2/index.html?v=<hash>`. Replace the placeholder at build time.
Better: retire the toggle as soon as the client picks, and serve the page directly.

## Retiring addresses

When a path is retired (a concept dropped, a variant folded in, "use v2 instead of lean"), leave a
one-line page at the old path:

```
<!doctype html><meta charset="utf-8"><meta http-equiv="refresh" content="0; url=../v2/">
<link rel="canonical" href="https://host/site/v2/"><title>Moved</title><p>Moved to <a href="../v2/">/v2/</a>.</p>
```

Old links in messages and client notes keep working.

## When the client still sees the old page

The server side is checked by the loop above. If it passes and the client still sees the old page, the
copy is in their browser. Say that plainly, give the address with a throwaway query, suggest a private
tab, and ask for the build stamp. Do not redeploy to "fix" it; a redeploy restarts the cache window.

Also check what they are looking at. Phone-only changes (a carousel, a tap-to-expand viewer) are
invisible on a desktop window wider than the breakpoint. Say which changes are phone-only when you
announce them.

## Delivery

Before handing over: remove the build stamp, resolve or list every `[CONFIRM]`, confirm fonts and media
licenses are in the repo, record the MP4 or other renditions still owed, and write the final record
entry with the live address and the commit.
