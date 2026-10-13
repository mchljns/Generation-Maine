<?php
/**
 * The follow list: one row per channel, read from Settings > Generation Maine.
 *
 * A channel with an address is a link that opens the account. A channel without one is a plain row with a placeholder handle,
 * so the page never sends anyone to a dead link.
 *
 * @package generation-maine
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

/**
 * The channels in display order, with what the page shows for each.
 *
 * @return array<int,array{key:string,name:string,url:string,handle:string}>
 */
function gm_channels() {
	$out = array();
	foreach ( array( 'instagram' => 'Instagram', 'tiktok' => 'TikTok', 'youtube' => 'YouTube' ) as $key => $name ) {
		$out[] = array(
			'key'    => $key,
			'name'   => $name,
			'url'    => gm_setting( 'gm_' . $key . '_url' ),
			'handle' => gm_setting( 'gm_' . $key . '_handle' ),
		);
	}
	$home  = gm_newsletter_home();
	$out[] = array(
		'key'    => 'substack',
		'name'   => 'Substack',
		'url'    => $home,
		'handle' => $home ? (string) wp_parse_url( $home, PHP_URL_HOST ) : '',
	);
	return $out;
}

/**
 * The rows.
 *
 * @return string HTML
 */
function gm_render_follow() {
	$rows = '';
	foreach ( gm_channels() as $c ) {
		$handle = $c['handle'] ? $c['handle'] : ( 'substack' === $c['key'] ? '[name].substack.com' : '[@handle]' );
		$inner  = gm_mark( $c['key'] ) . '<span class="name">' . esc_html( $c['name'] ) . '</span><span class="h">' . esc_html( $handle ) . '</span>';
		$rows  .= $c['url']
			? '<a class="row" href="' . esc_url( gm_utm( $c['url'] ) ) . '" target="_blank" rel="noopener">' . $inner . '</a>'
			: '<div class="row">' . $inner . '</div>';
	}
	return $rows;
}

/**
 * The block.
 */
function gm_register_follow_block() {
	register_block_type( get_theme_file_path( 'blocks/follow' ) );
}
add_action( 'init', 'gm_register_follow_block' );
