# WordPress QA scripts

The checks run on the Generation Maine theme in a local WordPress before it went to the client's site (Oct 13, 2026). They expect WordPress at http://127.0.0.1:8080 on SQLite at /tmp/claude-0/wp/core, the theme folder linked into its themes, a local admin account (admin, adminpass), and Playwright's Chromium at /opt/pw-browsers/chromium.

| Script | Run line | What it checks |
| --- | --- | --- |
| `setup.php` | `php setup.php 9 brand/identity/splash-lean-a/media` | Activates the theme, clears saved template edits, seeds nine placeholder creators with media |
| `reset.php` | `php reset.php` | Clears the test channel and newsletter values and any test video clip addresses |
| `wpstate.php` | `php wpstate.php video\|empty\|full\|nonews\|news` | Puts the site in one state: video clips, no creators, all creators, no newsletter, newsletter and a channel set |
| `compare.mjs` | `node compare.mjs <outdir>` | The v2 page and the WordPress page side by side at 1440 and 390: section heights, fonts, overflow, errors |
| `qa.mjs` | `URL=http://127.0.0.1:8080/ OUT=<dir> node qa.mjs` | The phone carousel at seven sizes: snapping, the position row, segment taps, arrow keys |
| `qa4.mjs` | `URL=http://127.0.0.1:8080/ OUT=<dir> node qa4.mjs` | The tap to expand viewer: frame ratio, close button, focus, scroll lock, Escape, back button |
| `states.mjs` | `node states.mjs <outdir>` | The phone menu, the logged-in bar under the admin bar, console errors; saves a login to `<outdir>/auth.json` |
| `states2.mjs` | `node states2.mjs <outdir> <label> [auth.json]` | Screens of the current state at 1440 and 390, as a visitor or logged in |
| `editor.mjs`, `editor2.mjs`, `editor3.mjs` | `node editor.mjs <outdir> <auth.json>` and so on | The site editor: block count, invalid blocks, the canvas fonts, the settings screen |

The skill's `measure.mjs`, `contrast.mjs` and `copy_check.py` in `.claude/skills/website-build/scripts/` cover overflow, tap targets, contrast and copy.
