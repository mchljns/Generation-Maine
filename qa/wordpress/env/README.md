# WordPress test environment

The setup used to test the theme on fresh WordPress sites (Oct 13 and 14, 2026). Each tester gets its own copy of WordPress, on SQLite, on its own port, so tests that change settings or content do not collide.

| File | What it is |
| --- | --- |
| `build-templates.sh` | Downloads WordPress 7.1.3 and 6.5.13, WP-CLI and the SQLite and Theme Check plugins, and builds four templates: `clean71`, `seeded71`, `clean65`, `seeded65`. Seeded means the theme zip installed with WP-CLI, post-name permalinks, and nine placeholder creators with media. Also prepares the PHP 7.4 Playground site |
| `wpt` | Starts and stops instances from the templates: `wpt new <name> <port> <template>`, `wpt wp <name> <wp-cli args>`, `wpt log`, `wpt themelog`, `wpt rm` |
| `pg74` | WordPress 6.5 on PHP 7.4.33 in WordPress Playground at port 9474, with the theme zip and the creators. Every response carries `X-Test-PHP` with the PHP version actually used |
| `playground-php74.json` | The blueprint `pg74` runs |
| `playground-public.json` | The blueprint behind the public test link, https://mchljns.github.io/Generation-Maine/test/ (copy of `test/blueprint.json` on gh-pages) |
| `check-test-link.mjs` | Opens the public test link in Chromium, waits for the theme with nine creators, saves a screenshot and the console. `PROXY_SPKI=<hash> OUT=<dir> node check-test-link.mjs` |
| `ENV.md` | The brief every tester read: ground rules, the templates, the tools, the severity scale |

Run lines:

```
WPT_ROOT=/tmp/claude-0/wptest bash qa/wordpress/env/build-templates.sh
export PATH="$PWD/qa/wordpress/env:$PATH" WPT_ROOT=/tmp/claude-0/wptest
wpt new site1 8101 seeded71          # http://127.0.0.1:8101, admin / adminpass
pg74 start                           # http://127.0.0.1:9474, logs in as admin on first visit
```

Notes from building it:

- The Playground CLI printed "PHP 7.4" while serving PHP 8.5 until the blueprint also pinned `preferredVersions`. Check the `X-Test-PHP` header, not the banner.
- WordPress 6.5 on PHP 8.4 logs deprecations from core itself; only lines naming generation-maine concern the theme (`wpt themelog`).
- PHP's built-in server has no URL rewriting, so choosing Post name under Settings > Permalinks saves `/index.php/%postname%/`; the templates set `/%postname%/` with WP-CLI.
- In a sandbox whose HTTPS goes through a proxy, Chromium must trust only that proxy's CA: `--ignore-certificate-errors-spki-list=<sha256 of its public key, base64>`.
- The public test link first imported and resized nine GIFs in the browser at start-up, which failed in at least one browser. It now uses clip links to the preview site and placeholder avatars, and loads in about 16 seconds.
