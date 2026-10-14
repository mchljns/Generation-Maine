# Generation Maine theme test environment

You are testing the Generation Maine WordPress block theme. The theme source is at /home/user/Generation-Maine/generation-maine/ (README.md there is the client-facing install and editing guide; read it). The installable zip is /home/user/Generation-Maine/dist/generation-maine.zip. The approved design it must match is the static page at https://mchljns.github.io/Generation-Maine/v2/ (local copy: /home/user/Generation-Maine/brand/identity/splash-lean-a/index.html).

## Ground rules

- Do NOT edit anything under /home/user/Generation-Maine. Do not commit, push, or touch git. You report findings; you do not fix them.
- Do not contact any real client site, WPVibe, or GitHub. Only the local test sites below and public read-only fetches.
- Put all your scratch files, scripts and screenshots under /tmp/claude-0/wptest/work/<your-label>/ and cite their paths as evidence.
- Use only the ports you are given. Create your own instance; never use another agent's.
- The machine has 4 CPUs shared with another agent. Keep Playwright to one browser at a time and close it when done.
- Never use `pkill -f php` or kill processes you did not start. Use `wpt stop <name>`.

## Test WordPress instances (PHP 8.4, SQLite)

`wpt` is on PATH:

```
wpt new <name> <port> <template>   copy a template and start it at http://127.0.0.1:<port>
wpt stop <name> | start <name> | rm <name> | list
wpt wp <name> <wp-cli args...>     WP-CLI against that instance (e.g. wpt wp a1 option get stylesheet)
wpt log <name>                     WordPress debug.log plus server errors
wpt themelog <name>                only log lines from the theme, or fatals
```

Templates:

| Template | What it is |
| --- | --- |
| clean71 | WordPress 7.1.3 (latest stable), freshly installed, default content, Twenty Twenty-Five active, theme NOT installed, plain permalinks |
| seeded71 | clean71 plus the theme installed from the zip with `wp theme install`, activated, post-name permalinks, nine placeholder creators seeded with portraits and GIF clips via the README's seed command. No settings filled in (no channels, no Substack address), as a fresh client site would be |
| clean65 | WordPress 6.5.13 (the theme's stated minimum), fresh, theme not installed |
| seeded65 | clean65 plus the theme and nine seeded creators, like seeded71 |

Login on every instance: admin / adminpass at /wp-login.php. WP_DEBUG is on, WP_DEBUG_DISPLAY off, errors go to wp-content/debug.log (`wpt log`). Note: WordPress 6.5 itself logs PHP 8.4 deprecations from core; only lines naming generation-maine (`wpt themelog`) concern the theme.
Outbound HTTP from WordPress works (plugins can be installed from wordpress.org with `wpt wp <name> plugin install <slug> --activate`). The Theme Check plugin is already installed (inactive) on the 7.1.3 templates (clean71, seeded71); on 6.5 install it with `wpt wp <name> plugin install theme-check`.
Instance files live at /tmp/claude-0/wptest/inst/<name>/core (theme at wp-content/themes/generation-maine). You may add mu-plugins to your own instance for testing (for example a filter), never to the theme folder.

## PHP 7.4

`pg74 start | stop | log` runs WordPress 6.5 on PHP 7.4.33 in WordPress Playground at http://127.0.0.1:9474 with the theme zip installed and nine creators seeded. The first visit logs in as admin automatically (cookie). Every response carries an `X-Test-PHP` header with the PHP version. PHP notices go to /tmp/claude-0/wptest/pg/mu/debug.log (`pg74 log`). Only the compatibility tester uses it. It is slow (WebAssembly); allow 30 to 120 seconds per request.

## The public test link

https://mchljns.github.io/Generation-Maine/test/ opens WordPress Playground with https://mchljns.github.io/Generation-Maine/test/blueprint.json. That blueprint is deliberately light: it installs the theme zip and seeds nine creators with no media import; each creator's clip is a clip link (gm_clip_url) to the GIFs on the preview site, and avatars are the placeholder figure, as on v2. Missing avatars there are expected.

## Browsers and tools

- Playwright: `import { chromium } from '/home/user/Generation-Maine/node_modules/playwright/index.mjs'` and `chromium.launch({ executablePath: '/opt/pw-browsers/chromium' })`. Never run `playwright install`.
- To open any external https site in Chromium (the live v2 page, playground.wordpress.net), the browser must trust the sandbox proxy's certificate: launch with `args: ['--ignore-certificate-errors-spki-list=PS48cX347wDVcRynzq+DFqswl2PLNE1sG6uQvxMCOS0=']` (this trusts only the proxy's CA, nothing else). Local http://127.0.0.1 sites need nothing. Do not use ignoreHTTPSErrors.
- Lighthouse: /home/user/Generation-Maine/node_modules/.bin/lighthouse (use `--chrome-path=/opt/pw-browsers/chromium --chrome-flags="--headless=new --no-sandbox"`).
- axe-core: /home/user/Generation-Maine/node_modules/axe-core/axe.min.js (inject with page.addScriptTag({ path }) then `await page.evaluate(() => axe.run())`).
- The website-build skill's scripts in /home/user/Generation-Maine/.claude/skills/website-build/scripts/: `measure.mjs <url> --out <dir> --viewports 320x568,390x844,...` (overflow, tap targets, text overflow, alt, fonts, media at load, errors) and `contrast.mjs <url>`; run both with `PLAYWRIGHT_DIR=/home/user/Generation-Maine/node_modules/playwright PW_CHROMIUM=/opt/pw-browsers/chromium`. `copy_check.py <file>` checks copy rules.
- Earlier QA scripts for reference: /home/user/Generation-Maine/qa/wordpress/ (README there has run lines; they point at port 8080, so pass your own URL).
- Sample media for uploads: /tmp/claude-0/wptest/media/sample-clip.mp4 (H.264), sample-clip.webm, sample-clip.gif, sample-portrait.jpg.
- PHP 8.4 CLI, composer, node 22, python3 with Pillow. No ffmpeg.

## Project rules the copy and design must follow

Plain-spoken copy, no em dashes, no italics, never the word "earn" in any tense, US spelling. Unknown facts are marked `[CONFIRM: ...]` on purpose; those are expected, not bugs. The about photo and the creators are placeholders on purpose. The footer build stamp is on purpose during review.

## Severity

- critical: a fatal error, data loss, a security hole, or the site cannot be installed or shown
- high: a main flow is broken or a visitor sees something clearly wrong (layout broken, content missing, a control that does not work)
- medium: a real defect with a workaround, or a mismatch with the approved v2 page a client would notice
- low: polish, minor inconsistency, edge case
- info: an observation or a documentation gap, not a defect
