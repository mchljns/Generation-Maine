<?php
/**
 * Generation Maine theme setup.
 *
 * Fonts are self-hosted and declared in theme.json. There is no Google Fonts call, no build step and no plugin.
 *
 * @package generation-maine
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

define( 'GM_THEME_VERSION', '2.0.0' );

require_once get_theme_file_path( 'inc/marks.php' );
require_once get_theme_file_path( 'inc/creators.php' );
require_once get_theme_file_path( 'inc/newsletter.php' );
require_once get_theme_file_path( 'inc/seo.php' );

/**
 * Theme supports and editor styles.
 */
function gm_setup() {
	add_theme_support( 'wp-block-styles' );
	add_theme_support( 'editor-styles' );
	add_theme_support( 'post-thumbnails' );
	add_theme_support( 'responsive-embeds' );
	remove_theme_support( 'core-block-patterns' );
	register_block_pattern_category( 'generation-maine', array( 'label' => __( 'Generation Maine', 'generation-maine' ) ) );
}
add_action( 'after_setup_theme', 'gm_setup' );

/**
 * Front-end stylesheet and the page's one script, with the mural data.
 */
function gm_enqueue() {
	wp_enqueue_style( 'generation-maine', get_stylesheet_uri(), array(), GM_THEME_VERSION );
	wp_enqueue_script( 'generation-maine', get_theme_file_uri( 'assets/js/site.js' ), array(), GM_THEME_VERSION, array( 'in_footer' => true ) );
	$data = array();
	$file = get_theme_file_path( 'assets/data/mural.json' );
	if ( file_exists( $file ) ) {
		$data = json_decode( (string) file_get_contents( $file ), true ); // phpcs:ignore WordPressVIPMinimum.Performance.FetchingRemoteData.FileGetContentsUnknown
	}
	wp_add_inline_script( 'generation-maine', 'window.GMDATA = ' . wp_json_encode( $data ? $data : new stdClass() ) . ';', 'before' );
}
add_action( 'wp_enqueue_scripts', 'gm_enqueue' );

/**
 * The same stylesheet inside the editor canvas, so the page looks in the editor as it does on the site.
 */
function gm_editor_assets() {
	if ( is_admin() ) {
		wp_enqueue_style( 'generation-maine-editor', get_stylesheet_uri(), array(), GM_THEME_VERSION );
	}
}
add_action( 'enqueue_block_assets', 'gm_editor_assets' );

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
 * One palette in every theme: the page commits to its own colors.
 */
function gm_color_scheme() {
	echo '<meta name="color-scheme" content="light">' . "\n";
	echo '<meta name="theme-color" content="#0B2B21">' . "\n";
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
 * The lockup for the header: both colorways, so the bar can swap as it scrolls.
 *
 * @return string
 */
function gm_header_lockups() {
	return gm_logo( 'lockup-compact-reversed', 'lk light' ) . gm_logo( 'lockup-compact', 'lk dark' );
}

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
