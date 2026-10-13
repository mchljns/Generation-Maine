<?php
/**
 * Newsletter: the Substack hand-off, and the latest-posts feed kept for later.
 *
 * The signup form sends the visitor's address to the publication's subscribe page on Substack, which fills its field from the
 * query string, sends the confirmation email and keeps the list. The address lives in Settings > Generation Maine.
 *
 * @package generation-maine
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

/**
 * The publication's home, worked out from the subscribe page. Empty when none is set.
 *
 * @return string
 */
function gm_newsletter_home() {
	$url   = gm_setting( 'gm_newsletter_url' );
	$parts = $url ? wp_parse_url( $url ) : array();
	return empty( $parts['host'] ) ? '' : 'https://' . $parts['host'] . '/';
}

/**
 * The signup form, the same markup as the v2 page. Visitors see nothing until a subscribe page is set; editors see a note.
 *
 * @return string HTML
 */
function gm_render_newsletter_form() {
	$url = gm_setting( 'gm_newsletter_url' );
	if ( '' === $url ) {
		return current_user_can( 'manage_options' )
			? '<p class="gm-newsletter-missing">' . sprintf(
				/* translators: %s: link to the settings page */
				esc_html__( 'Only you can see this. The signup form appears once a Substack subscribe page is set under %s.', 'generation-maine' ),
				'<a href="' . esc_url( gm_settings_url() ) . '">' . esc_html__( 'Settings > Generation Maine', 'generation-maine' ) . '</a>'
			) . '</p>'
			: '';
	}
	$note = gm_setting( 'gm_newsletter_note' );
	return '<form id="nl" action="' . esc_url( gm_utm( $url ) ) . '" method="get" target="_blank" rel="noopener">'
		. '<label for="em" style="position:absolute;left:-9999px">' . esc_html__( 'Email', 'generation-maine' ) . '</label>'
		. '<input id="em" name="email" type="email" placeholder="you@example.com" autocomplete="email" required inputmode="email">'
		. '<button class="btn b1" type="submit">' . esc_html__( 'Sign up', 'generation-maine' ) . '</button>'
		. ( $note ? '<p class="fine">' . esc_html( $note ) . '</p>' : '' )
		. '</form>';
}

/**
 * The latest posts from the publication, read from its feed and cached for an hour. Not on the page today; the block stays
 * registered for when the newsletter has posts worth showing.
 *
 * @param int $count Posts to show.
 * @return string HTML
 */
function gm_render_posts( $count = 3 ) {
	$count = max( 1, min( 6, (int) $count ) );
	$home  = gm_newsletter_home();
	if ( ! $home ) {
		return current_user_can( 'edit_posts' ) ? '<p class="gm-empty">' . esc_html__( 'The latest posts appear once a Substack subscribe page is set.', 'generation-maine' ) . '</p>' : '';
	}
	include_once ABSPATH . WPINC . '/feed.php';
	add_filter( 'wp_feed_cache_transient_lifetime', 'gm_feed_lifetime' );
	$rss = fetch_feed( $home . 'feed' );
	remove_filter( 'wp_feed_cache_transient_lifetime', 'gm_feed_lifetime' );
	if ( is_wp_error( $rss ) ) {
		return '';
	}
	$html = '<div class="list">';
	foreach ( $rss->get_items( 0, $count ) as $it ) {
		$html .= '<a class="row" href="' . esc_url( gm_utm( (string) $it->get_permalink() ) ) . '" target="_blank" rel="noopener">' . gm_mark( 'substack' )
			. '<span class="name">' . esc_html( $it->get_title() ) . '</span><span class="h">' . esc_html( $it->get_date( 'M j' ) ) . '</span></a>';
	}
	return $html . '</div>';
}

/**
 * Cache the feed for an hour.
 *
 * @return int
 */
function gm_feed_lifetime() {
	return HOUR_IN_SECONDS;
}

/**
 * The two blocks.
 */
function gm_register_newsletter_blocks() {
	register_block_type( get_theme_file_path( 'blocks/newsletter' ) );
	register_block_type( get_theme_file_path( 'blocks/posts' ) );
}
add_action( 'init', 'gm_register_newsletter_blocks' );
