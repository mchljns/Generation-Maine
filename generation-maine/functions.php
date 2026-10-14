<?php
/**
 * Generation Maine theme setup.
 *
 * The stylesheet, the script, the footer markup and the mural are generated from the approved v2 page by
 * brand/src/build_theme.py. Fonts are self-hosted and declared in theme.json. No Google Fonts call, no build step, no plugin.
 *
 * @package generation-maine
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

require_once get_theme_file_path( 'inc/build.php' );
require_once get_theme_file_path( 'inc/marks.php' );
require_once get_theme_file_path( 'inc/settings.php' );
require_once get_theme_file_path( 'inc/creators.php' );
require_once get_theme_file_path( 'inc/newsletter.php' );
require_once get_theme_file_path( 'inc/follow.php' );
require_once get_theme_file_path( 'inc/footer.php' );
require_once get_theme_file_path( 'inc/seo.php' );
require_once get_theme_file_path( 'inc/parts.php' );

/**
 * Theme supports. Layout styles are off because the page's own stylesheet lays out every section; the editor gets the
 * same rules through assets/css/editor.css.
 */
function gm_setup() {
	add_theme_support( 'editor-styles' );
	add_theme_support( 'post-thumbnails' );
	add_theme_support( 'responsive-embeds' );
	add_theme_support( 'disable-layout-styles' );
	add_editor_style( 'assets/css/editor.css' );
	remove_theme_support( 'core-block-patterns' );
	register_block_pattern_category( 'generation-maine', array( 'label' => __( 'Generation Maine', 'generation-maine' ) ) );
}
add_action( 'after_setup_theme', 'gm_setup' );

/**
 * The page's root classes. The v2 page sets them on <html>; several rules depend on two of them sitting on one element.
 *
 * @param string $output Attributes for the html tag.
 * @return string
 */
function gm_html_classes( $output ) {
	if ( is_admin() ) {
		return $output;
	}
	return $output . ' class="static lean euro"';
}
add_filter( 'language_attributes', 'gm_html_classes' );

/**
 * The js class goes on before first paint, so hidden-until-loaded states never flash and transitions never run at load.
 */
function gm_js_class() {
	echo '<script>document.documentElement.classList.add("js")</script>' . "\n";
}
add_action( 'wp_head', 'gm_js_class', 0 );

/**
 * Stylesheet and script. The version is the build hash, so a new build is never served from a stale cache.
 */
function gm_enqueue() {
	wp_enqueue_style( 'generation-maine', get_stylesheet_uri(), array(), GM_BUILD_HASH );
	wp_enqueue_script( 'generation-maine', get_theme_file_uri( 'assets/js/site.js' ), array(), GM_BUILD_HASH, array( 'in_footer' => true ) );
}
add_action( 'wp_enqueue_scripts', 'gm_enqueue' );

/**
 * The hero mural's data, read by the page script.
 */
function gm_mural_data() {
	$file = get_theme_file_path( 'assets/data/mural.json' );
	if ( ! file_exists( $file ) ) {
		return;
	}
	echo '<script id="maine-data" type="application/json">' . file_get_contents( $file ) . '</script>' . "\n"; // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped, WordPressVIPMinimum.Performance.FetchingRemoteData.FileGetContentsUnknown
}
add_action( 'wp_footer', 'gm_mural_data', 1 );

/**
 * The page's own skip link replaces the one WordPress adds to block themes.
 */
function gm_skip_link() {
	echo '<a class="skip" href="#main">' . esc_html__( 'Skip to content', 'generation-maine' ) . '</a>' . "\n";
	// the phone menu sits outside the bar, as on the v2 page; the page script copies the bar's links and button into it
	echo '<div class="sheet" id="sheet" aria-hidden="true"><nav aria-label="' . esc_attr__( 'Page', 'generation-maine' ) . '"></nav></div>' . "\n";
}
add_action( 'wp_body_open', 'gm_skip_link', 1 );
remove_action( 'wp_footer', 'the_block_template_skip_link' );
remove_action( 'wp_enqueue_scripts', 'wp_enqueue_block_template_skip_link' );

/**
 * Preload the two faces the first screen uses: the headline and the labels.
 */
function gm_preload_fonts() {
	foreach ( array( 'bricolage-grotesque-800.woff2' => 'font/woff2', 'michroma-regular.ttf' => 'font/ttf' ) as $file => $type ) {
		printf( '<link rel="preload" href="%s" as="font" type="%s" crossorigin>' . "\n", esc_url( get_theme_file_uri( 'assets/fonts/' . $file ) ), esc_attr( $type ) );
	}
}
add_action( 'wp_head', 'gm_preload_fonts', 1 );

/**
 * One palette in every theme: the page commits to its own colors.
 */
function gm_color_scheme() {
	echo '<meta name="color-scheme" content="light">' . "\n";
	echo '<meta name="theme-color" content="#0F2E4D">' . "\n";
}
add_action( 'wp_head', 'gm_color_scheme', 0 );

/**
 * Favicon fallback. WordPress prints its own tags once a Site Icon is set in Settings > General.
 */
function gm_favicon_fallback() {
	if ( has_site_icon() ) {
		return;
	}
	printf( '<link rel="icon" href="%s" sizes="any">' . "\n", esc_url( get_theme_file_uri( 'assets/img/favicon.ico' ) ) );
	printf( '<link rel="icon" href="%s" type="image/svg+xml">' . "\n", esc_url( get_theme_file_uri( 'assets/img/icon.svg' ) ) );
	printf( '<link rel="apple-touch-icon" href="%s">' . "\n", esc_url( get_theme_file_uri( 'assets/img/icon-180.png' ) ) );
}
add_action( 'wp_head', 'gm_favicon_fallback', 2 );

/**
 * Kickers with the family's bars: a paragraph with the class "k-bars" gets the three bars before its text.
 * The hero headline with the class "gm-here" gets its last word in gold and the pulsing dot after it.
 * Both are added as the page renders, so they survive any rewrite of the words in the editor.
 *
 * @param string $html  Block HTML.
 * @param array  $block Block.
 * @return string
 */
function gm_render_marks( $html, $block ) {
	$class = isset( $block['attrs']['className'] ) ? ' ' . $block['attrs']['className'] . ' ' : '';
	if ( 'core/paragraph' === $block['blockName'] && false !== strpos( $class, ' k-bars ' ) ) {
		return preg_replace( '/^(\s*<p\b[^>]*>)/', '$1' . gm_bars(), $html, 1 );
	}
	if ( 'core/heading' === $block['blockName'] && false !== strpos( $class, ' gm-here ' ) ) {
		// a stray line break at the end does not count
		$html = preg_replace( '#(?:\s|&nbsp;|<br\s*/?>)+(</h[1-6]>\s*)$#i', '$1', $html );
		// the last word turns gold even inside bold, emphasis or a link; a final period becomes the dot, and a question or an
		// exclamation keeps its mark and gets no dot
		return preg_replace_callback(
			'#([^\s<>]+)((?:\s*</(?:strong|b|em|i|a|span|mark|u|s|code)>)*)(\s*</h[1-6]>\s*)$#i',
			static function ( $m ) {
				$word = $m[1];
				$dot  = '<i class="d pulse" aria-hidden="true"></i>';
				if ( preg_match( '/[?!]$/', $word ) ) {
					return '<span class="here">' . $word . '</span>' . $m[2] . $m[3];
				}
				if ( strlen( $word ) > 1 && '.' === substr( $word, -1 ) ) {
					$word = substr( $word, 0, -1 );
				}
				return '<span class="here">' . $word . $dot . '</span>' . $m[2] . $m[3];
			},
			$html,
			1
		);
	}
	if ( 'core/group' === $block['blockName'] && $class ) {
		// the bar and the footer link to these sections by id, so the ids stay whatever an editor does to the anchor field
		foreach ( array( ' hero ' => 'top', ' about ' => 'about', ' stories-head ' => 'creators', ' follow ' => 'follow', ' nl ' => 'newsletter' ) as $token => $id ) {
			if ( false !== strpos( $class, $token ) ) {
				if ( preg_match( '/^(\s*<[a-z]+\b[^>]*?)\sid="[^"]*"/i', $html ) ) {
					return preg_replace( '/^(\s*<[a-z]+\b[^>]*?)\sid="[^"]*"/i', '$1 id="' . $id . '"', $html, 1 );
				}
				return preg_replace( '/^(\s*<[a-z]+\b)/i', '$1 id="' . $id . '"', $html, 1 );
			}
		}
	}
	return $html;
}
add_filter( 'render_block', 'gm_render_marks', 10, 2 );

/**
 * Trim the things a one-page site does not use.
 */
function gm_trim_head() {
	remove_action( 'wp_head', 'print_emoji_detection_script', 7 );
	remove_action( 'wp_print_styles', 'print_emoji_styles' );
	remove_action( 'wp_head', 'wp_generator' );
	remove_action( 'wp_head', 'rsd_link' );
	remove_action( 'wp_head', 'wlwmanifest_link' );
}
add_action( 'init', 'gm_trim_head' );
