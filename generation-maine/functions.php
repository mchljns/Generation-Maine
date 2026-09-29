<?php
/**
 * Generation Maine theme setup.
 *
 * Fonts are self-hosted and declared in theme.json. There is no Google Fonts call.
 *
 * @package generation-maine
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

define( 'GM_THEME_VERSION', '1.0.0' );

require_once get_theme_file_path( 'inc/creators.php' );
require_once get_theme_file_path( 'inc/seo.php' );

/**
 * Theme supports and editor styles.
 */
function gm_setup() {
	add_theme_support( 'wp-block-styles' );
	add_theme_support( 'editor-styles' );
	add_theme_support( 'post-thumbnails' );
	add_theme_support( 'responsive-embeds' );
	add_editor_style( 'style.css' );
	remove_theme_support( 'core-block-patterns' );
}
add_action( 'after_setup_theme', 'gm_setup' );

/**
 * Front-end stylesheet.
 */
function gm_enqueue() {
	wp_enqueue_style( 'generation-maine', get_stylesheet_uri(), array(), GM_THEME_VERSION );
}
add_action( 'wp_enqueue_scripts', 'gm_enqueue' );

/**
 * Preload the display font so the headline does not reflow.
 */
function gm_preload_fonts() {
	printf(
		'<link rel="preload" href="%s" as="font" type="font/woff2" crossorigin>' . "\n",
		esc_url( get_theme_file_uri( 'assets/fonts/bricolage-grotesque-800.woff2' ) )
	);
}
add_action( 'wp_head', 'gm_preload_fonts', 1 );

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
add_action( 'wp_head', 'gm_favicon_fallback', 5 );

/**
 * Theme color for mobile browser chrome.
 */
function gm_theme_color() {
	echo '<meta name="theme-color" content="#0E3B2E">' . "\n";
}
add_action( 'wp_head', 'gm_theme_color', 6 );

/**
 * Pattern category.
 */
function gm_pattern_category() {
	register_block_pattern_category( 'generation-maine', array( 'label' => __( 'Generation Maine', 'generation-maine' ) ) );
}
add_action( 'init', 'gm_pattern_category' );

/**
 * Returns the inline SVG wordmark. Letters use currentColor and the dot uses the accent color.
 *
 * @return string
 */
function gm_wordmark_svg() {
	static $svg = null;
	if ( null === $svg ) {
		$file = get_theme_file_path( 'assets/img/wordmark-inline.svg' );
		$svg  = file_exists( $file ) ? (string) file_get_contents( $file ) : ''; // phpcs:ignore WordPress.WP.AlternativeFunctions.file_get_contents_file_get_contents
	}
	return $svg;
}

/**
 * Small performance cleanups. None of these are used on a one-page site.
 */
remove_action( 'wp_head', 'print_emoji_detection_script', 7 );
remove_action( 'wp_print_styles', 'print_emoji_styles' );
remove_action( 'wp_head', 'wp_generator' );
