<?php
/**
 * Code and embeds from Settings > Generation Maine: code for <head>, code for the end of the page, and Substack's own
 * signup embed, which the Newsletter Signup block shows in place of the theme's form when it is set.
 *
 * The code is printed as it was saved. Only users WordPress trusts with scripts can save it (gm_sanitize_code()).
 *
 * @package generation-maine
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

/**
 * Code in <head>.
 */
function gm_code_head() {
	$code = gm_setting( 'gm_code_head' );
	if ( '' !== $code ) {
		echo "\n" . $code . "\n"; // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped -- saved by an administrator, see gm_can_save_code()
	}
}
add_action( 'wp_head', 'gm_code_head', 99 );

/**
 * Code before </body>.
 */
function gm_code_body() {
	$code = gm_setting( 'gm_code_body' );
	if ( '' !== $code ) {
		echo "\n" . $code . "\n"; // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped -- saved by an administrator, see gm_can_save_code()
	}
}
add_action( 'wp_footer', 'gm_code_body', 99 );

/**
 * Keep a pasted embed inside its column on a phone.
 */
function gm_embed_style() {
	if ( '' !== gm_setting( 'gm_newsletter_embed' ) ) {
		wp_add_inline_style( 'generation-maine', '.gm-newsletter-embed iframe{display:block;max-width:100%;border:0}' );
	}
}
add_action( 'wp_enqueue_scripts', 'gm_embed_style', 11 );
