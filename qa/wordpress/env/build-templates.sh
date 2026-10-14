#!/usr/bin/env bash
# Rebuilds the WordPress test templates used to test the theme (Oct 2026): WordPress 7.1.3 (latest stable) and 6.5.13 (the
# theme's minimum), each on SQLite, clean and seeded. Run from the repository root after building dist/generation-maine.zip.
#   WPT_ROOT=/tmp/claude-0/wptest bash qa/wordpress/env/build-templates.sh
# Then: wpt new <name> <port> <clean71|seeded71|clean65|seeded65>   (put qa/wordpress/env/wpt on PATH)
# Needs php (8.x), curl, unzip, node for the PHP 7.4 Playground step. In a sandbox whose outbound HTTPS goes through a proxy,
# WordPress is pointed at that proxy and its CA (see the mu-plugin below); elsewhere drop those two lines.
set -euo pipefail
REPO="$(cd "$(dirname "$0")/../../.." && pwd)"
T="${WPT_ROOT:-/tmp/claude-0/wptest}"; export WPT_ROOT="$T"
WPT="$REPO/qa/wordpress/env/wpt"
ZIP="$REPO/dist/generation-maine.zip"
MEDIA="$REPO/brand/identity/splash-lean-a/media"
mkdir -p "$T/dl" "$T/tpl" "$T/inst" "$T/media" "$T/work"
cd "$T/dl"
[ -f wordpress-7.1.3.zip ] || curl -sS -o wordpress-7.1.3.zip https://wordpress.org/wordpress-7.1.3.zip
[ -f wordpress-6.5.13.zip ] || curl -sS -o wordpress-6.5.13.zip https://wordpress.org/wordpress-6.5.13.zip
[ -f wp-cli.phar ] || curl -sS -o wp-cli.phar https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar
[ -f sqlite.zip ] || curl -sSL -o sqlite.zip https://downloads.wordpress.org/plugin/sqlite-database-integration.zip
[ -f theme-check.zip ] || curl -sSL -o theme-check.zip https://downloads.wordpress.org/plugin/theme-check.zip

raw() { # $1 template name, $2 WordPress zip: unpacked core wired to SQLite, with __WPT_PORT__ and __WPT_CORE__ placeholders
  local d="$T/tpl/$1"; rm -rf "$d"; mkdir -p "$d"; (cd "$d" && unzip -q "$T/dl/$2" && mv wordpress core)
  unzip -q "$T/dl/sqlite.zip" -d "$d/core/wp-content/plugins/"
  sed -e "s#{SQLITE_IMPLEMENTATION_FOLDER_PATH}#__WPT_CORE__/wp-content/plugins/sqlite-database-integration#" -e "s#{SQLITE_PLUGIN}#sqlite-database-integration/load.php#" \
    "$d/core/wp-content/plugins/sqlite-database-integration/db.copy" > "$d/core/wp-content/db.php"
  mkdir -p "$d/core/wp-content/mu-plugins"
  if [ -f /root/.ccr/ca-bundle.crt ]; then
    printf '%s\n' '<?php' '// Test sandbox only: outbound requests go through the session proxy, which re-signs TLS with its own CA.' \
      "add_filter( 'http_request_args', function ( \$args ) { \$args['sslcertificates'] = '/root/.ccr/ca-bundle.crt'; return \$args; } );" > "$d/core/wp-content/mu-plugins/sandbox-net.php"
  fi
  local proxy=""
  if [ -n "${HTTPS_PROXY:-}" ]; then
    local hp="${HTTPS_PROXY#*://}"; hp="${hp%/}"; hp="${hp##*@}"
    proxy="define( 'WP_PROXY_HOST', '${hp%:*}' ); define( 'WP_PROXY_PORT', '${hp##*:}' ); define( 'WP_PROXY_BYPASS_HOSTS', 'localhost, 127.0.0.1' );"
  fi
  cat > "$d/core/wp-config.php" <<PHP
<?php
define( 'DB_NAME', 'wp' ); define( 'DB_USER', '' ); define( 'DB_PASSWORD', '' ); define( 'DB_HOST', '' ); define( 'DB_CHARSET', 'utf8' ); define( 'DB_COLLATE', '' );
define( 'DB_ENGINE', 'sqlite' );
define( 'AUTH_KEY', 'test-a' ); define( 'SECURE_AUTH_KEY', 'test-b' ); define( 'LOGGED_IN_KEY', 'test-c' ); define( 'NONCE_KEY', 'test-d' ); define( 'AUTH_SALT', 'test-e' ); define( 'SECURE_AUTH_SALT', 'test-f' ); define( 'LOGGED_IN_SALT', 'test-g' ); define( 'NONCE_SALT', 'test-h' );
\$table_prefix = 'wp_';
define( 'WP_HOME', 'http://127.0.0.1:__WPT_PORT__' ); define( 'WP_SITEURL', 'http://127.0.0.1:__WPT_PORT__' );
define( 'WP_DEBUG', true ); define( 'WP_DEBUG_DISPLAY', false ); define( 'WP_DEBUG_LOG', __DIR__ . '/wp-content/debug.log' );
define( 'SCRIPT_DEBUG', false ); define( 'DISABLE_WP_CRON', true ); define( 'WP_ENVIRONMENT_TYPE', 'local' ); define( 'FS_METHOD', 'direct' );
$proxy
if ( ! defined( 'ABSPATH' ) ) { define( 'ABSPATH', __DIR__ . '/' ); }
require_once ABSPATH . 'wp-settings.php';
PHP
}
snap() { # $1 instance, $2 template: save an instance back as a template, restoring the placeholders
  "$WPT" stop "$1" >/dev/null; rm -rf "$T/tpl/$2"; cp -a "$T/inst/$1" "$T/tpl/$2"; local p; p=$(cat "$T/tpl/$2/port")
  sed -i "s#127.0.0.1:$p#127.0.0.1:__WPT_PORT__#g" "$T/tpl/$2/core/wp-config.php"
  sed -i "s#$T/inst/$1/core#__WPT_CORE__#g" "$T/tpl/$2/core/wp-content/db.php"
  rm -f "$T/tpl/$2/port" "$T/tpl/$2/pid" "$T/tpl/$2/server.log" "$T/tpl/$2/core/wp-content/debug.log"
}
build() { # $1 version tag (71 or 65), $2 zip, $3 port
  local v=$1 n="build$1"
  raw "raw$v" "$2"
  "$WPT" rm "$n" >/dev/null 2>&1 || true
  "$WPT" new "$n" "$3" "raw$v"
  "$WPT" wp "$n" core install --title="Generation Maine" --admin_user=admin --admin_password=adminpass --admin_email=admin@example.com --skip-email
  "$WPT" wp "$n" plugin activate sqlite-database-integration
  [ "$v" = 71 ] && "$WPT" wp "$n" plugin install "$T/dl/theme-check.zip"
  snap "$n" "clean$v"; "$WPT" start "$n" >/dev/null
  "$WPT" wp "$n" theme install "$ZIP" --activate
  "$WPT" wp "$n" rewrite structure '/%postname%/' --hard
  "$WPT" wp "$n" eval-file "$T/inst/$n/core/wp-content/themes/generation-maine/bin/seed-creators.php" 9 "$MEDIA"
  snap "$n" "seeded$v"; "$WPT" rm "$n" >/dev/null
}
build 71 wordpress-7.1.3.zip 8990
build 65 wordpress-6.5.13.zip 8991

# Sample media for upload tests
cp "$MEDIA/portrait-1.jpg" "$T/media/sample-portrait.jpg"; cp "$MEDIA/creator-1.gif" "$T/media/sample-clip.gif"
unzip -p "$T/dl/wordpress-6.5.13.zip" wordpress/wp-content/themes/twentytwentytwo/assets/videos/birds.mp4 > "$T/media/sample-clip.mp4"

# PHP 7.4 in WordPress Playground
mkdir -p "$T/pg/mu" "$T/playground"
cp "$ZIP" "$T/pg/generation-maine.zip"; cp "$REPO/qa/wordpress/env/playground-php74.json" "$T/pg/local74.json"
printf '%s\n' '<?php' '// Test only: report the PHP version that served each request.' "if ( ! headers_sent() ) { header( 'X-Test-PHP: ' . PHP_VERSION ); }" > "$T/pg/mu/php-version-header.php"
[ -x "$T/playground/node_modules/.bin/wp-playground-cli" ] || (cd "$T/playground" && npm init -y >/dev/null && npm install @wp-playground/cli >/dev/null)
cp "$REPO/qa/wordpress/env/ENV.md" "$T/ENV.md"
echo "templates: $(ls "$T/tpl" | tr '\n' ' ')"
