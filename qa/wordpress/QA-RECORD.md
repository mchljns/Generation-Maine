# WordPress theme QA record

The Generation Maine block theme (generation-maine/) was tested in four rounds on local WordPress 7.1.3 and 6.5.13 (PHP 8.4, SQLite) and on WordPress 6.5 with PHP 7.4 (WordPress Playground). Each round's testers worked on their own fresh sites, reproduced every finding twice, and saved their scripts. Fixes were made by separate agents in their own git worktrees, each reproducing the defect first and verifying the fix on 7.1 and 6.5 before the main session merged it. The test environment is in `env/` (see `env/README.md`).

## Rounds

| Round | Build | Tested | Result |
| --- | --- | --- | --- |
| 1 | 3.1.0 before fixes | install, visitor, editor, settings, creators (compat, security and speed cut off by usage limits) | 74 findings, all fixed in 432732d |
| 2 | 3.1.0, build 3154ae3 | all eight areas, retesting round 1 | 60 fixed, 11 partly, 3 not fixed (accepted); 53 new: 10 medium, 33 low, 10 info. Fixed in f777c43, 001f01e, 53e8f58, c45e34b, 3672e10 (theme 3.2.0) |
| 3 | 3.2.0, build 95b10f6 | front, editor, admin, platform and security | 61 of 73 round 2 items fixed, 12 partly; 20 new: 4 medium, 12 low, 4 info. Fixed in 2c71d0e, 68cc514, 7231af4, bd02fd7 |
| 4 (final) | 3.2.0, build 31259db | front, editor, admin and platform | 23 of 31 round 3 items fixed, 7 partly, 1 not fixed; 10 new, all low or info. Fixed in c5087da, d69d527, 65fd6b0 |
| Smoke | 3.2.0, build bd9243a (65fd6b0) | every acceptance script from rounds 3 and 4 on the merged build | admin 15 of 15 pass; front and editor 13 of 14, the editor dot on 7.1, fixed in c67ac01 and checked with the tester's probe |

Each round's findings, with steps, evidence and causes, are in `rounds/`: `findings-round2.md`, `fixes-round2.md`, `findings-round3.md`, `findings-round3-platform.md`, `fixes-round3.md`, `findings-round4.md`. The final acceptance scripts are in `rounds/scripts/smoke-front/` and `rounds/scripts/smoke-admin/`; they expect the environment in `env/` and take the site address and port as arguments.

## Known and accepted

- The nine position segments above the phone cards are 44 px tall but 28 to 40 px wide with nine creators (35 px on a 390 px screen). That passes WCAG 2.5.8 (24 px) but not the 44 px the rest of the page uses. Same on v2. Swiping and the arrow keys are the other ways through. In the README.
- WordPress 6.5 reads theme.json schema 3 and skips the settings it does not know; the page looks the same. In the editor a paragraph or heading shows an empty Typography panel. In the README.
- Small differences from the v2 preview: 40 px header link areas (WordPress wraps links in paragraphs), no social rows and no signup form until Settings > Generation Maine is filled in, portraits in the handle chips. In the README.
- The Creators block works full width when placed straight in a page, not inside a Group or Columns. In the README.
- A Group's Content width does nothing in posts and pages; the reading column sets the width. In the README.
- On WordPress 7, a copied Logo, menu button or mural inside the hero needs Edit pattern before Remove. In the README.
- In the editor (not on the page): the headline dot can sit alone on a line at some widths; on 6.5 it sits at the corner while the headline itself is selected; while the headline is selected, typed trailing spaces stay until you click away.
- Theme Check lists the Creators post type, the blocks and the settings screen as plugin territory, no readme.txt and favicon.ico. Expected for a theme built for one site. In the README.
- Only Chromium was available: WebKit, Firefox and real phones (iOS Safari momentum and focus) are untested.

## Waiting on the client

- The copyright line (style.css and README) and the Author URI.
- The `[CONFIRM]` items on the page: the Substack address, the channel handles, the aim in their own words, the legal line, the privacy page, the domain.
- The about photo: a credit on the page or a replacement.
- The real creators, to replace the placeholders.

## Deployed

Theme 3.2.0, build bd9243a, went to gh-pages in commit 8e917a4 on Oct 16, 2026: the v2 page (https://mchljns.github.io/Generation-Maine/v2/) and the test link's zip (https://mchljns.github.io/Generation-Maine/test/).
