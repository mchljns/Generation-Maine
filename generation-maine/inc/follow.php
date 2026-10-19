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
 * Every platform the follow list can show, in display order: key => name, an example address, and whether it is on the
 * page until someone changes it. The first three and Substack were on the page from the start; the rest start off.
 * Substack's address is the newsletter's subscribe page, so it has no address of its own here.
 *
 * @return array<string,array{name:string,example:string,on:bool}>
 */
function gm_platforms() {
	return array(
		'instagram' => array( 'name' => 'Instagram', 'example' => 'https://www.instagram.com/generationmaine/', 'on' => true ),
		'tiktok'    => array( 'name' => 'TikTok', 'example' => 'https://www.tiktok.com/@generationmaine', 'on' => true ),
		'youtube'   => array( 'name' => 'YouTube', 'example' => 'https://www.youtube.com/@generationmaine', 'on' => true ),
		'x'         => array( 'name' => 'X', 'example' => 'https://x.com/generationmaine', 'on' => false ),
		'facebook'  => array( 'name' => 'Facebook', 'example' => 'https://www.facebook.com/generationmaine', 'on' => false ),
		'threads'   => array( 'name' => 'Threads', 'example' => 'https://www.threads.net/@generationmaine', 'on' => false ),
		'bluesky'   => array( 'name' => 'Bluesky', 'example' => 'https://bsky.app/profile/generationmaine.bsky.social', 'on' => false ),
		'linkedin'  => array( 'name' => 'LinkedIn', 'example' => 'https://www.linkedin.com/company/generationmaine', 'on' => false ),
		'substack'  => array( 'name' => 'Substack', 'example' => '', 'on' => true ),
	);
}

/**
 * True when a platform is switched on for the follow list and the footer icons.
 *
 * @param string $key Platform.
 * @return bool
 */
function gm_platform_on( $key ) {
	return '1' === gm_setting( 'gm_' . $key . '_show' );
}

/**
 * The channels switched on, in display order, with what the page shows for each.
 *
 * @return array<int,array{key:string,name:string,url:string,handle:string}>
 */
function gm_channels() {
	$out = array();
	foreach ( gm_platforms() as $key => $p ) {
		if ( ! gm_platform_on( $key ) ) {
			continue;
		}
		if ( 'substack' === $key ) {
			$home  = gm_newsletter_home();
			$out[] = array(
				'key'    => 'substack',
				'name'   => 'Substack',
				'url'    => $home,
				'handle' => $home ? (string) wp_parse_url( $home, PHP_URL_HOST ) : '',
			);
			continue;
		}
		$name  = $p['name'];
		$out[] = array(
			'key'    => $key,
			'name'   => $name,
			'url'    => gm_setting( 'gm_' . $key . '_url' ),
			// cleaned again here, so a handle saved before the rules for spaces and a lone @ shows as a new save would keep it
			'handle' => gm_sanitize_handle( gm_setting( 'gm_' . $key . '_handle' ) ),
		);
	}
	return $out;
}

/**
 * A handle worked out from an account address, for a channel whose handle field was left empty. TikTok and YouTube put the
 * @handle first and a tab or a video after it; Instagram puts the bare name first. An address with no handle in it (a
 * YouTube channel id, an Instagram post or share link) shows the site's address instead, for example youtube.com.
 *
 * @param string $url Account address.
 * @param string $key Channel: instagram, tiktok or youtube.
 * @return string
 */
function gm_handle_from_url( $url, $key = '' ) {
	$path = trim( (string) wp_parse_url( $url, PHP_URL_PATH ), '/' );
	$seg  = '' === $path ? array() : array_map( 'rawurldecode', explode( '/', $path ) );
	foreach ( $seg as $s ) {
		if ( strlen( $s ) > 1 && '@' === $s[0] ) {
			return $s;
		}
	}
	// an Instagram name: letters, numbers, periods and underscores, alone or before a profile tab or one of the account's
	// posts, and not one of Instagram's own pages (a post, a reel, stories, a share link)
	if ( 'instagram' === $key && $seg && preg_match( '/^[A-Za-z0-9._]{1,30}$/', $seg[0] )
		&& ( 1 === count( $seg ) || in_array( strtolower( $seg[1] ), array( 'reels', 'tagged', 'saved', 'guides', 'p', 'reel', 'tv' ), true ) )
		&& ! in_array( strtolower( $seg[0] ), array( 'p', 'reel', 'reels', 'tv', 'stories', 'explore', 'accounts', 'direct', 's', 'share', 'about', 'legal', 'developer', 'web' ), true ) ) {
		return '@' . $seg[0];
	}
	// x.com/name, bsky.app/profile/name.bsky.social, facebook.com/name, linkedin.com/company/name or /in/name
	$reserved = array( 'home', 'search', 'explore', 'share', 'sharer', 'intent', 'i', 'settings', 'login', 'pages', 'groups', 'watch', 'events', 'profile.php' );
	if ( 'x' === $key && $seg && preg_match( '/^[A-Za-z0-9_]{1,15}$/', $seg[0] ) && ! in_array( strtolower( $seg[0] ), $reserved, true ) ) {
		return '@' . $seg[0];
	}
	if ( 'bluesky' === $key && 2 <= count( $seg ) && 'profile' === strtolower( $seg[0] ) && preg_match( '/^[A-Za-z0-9.-]+$/', $seg[1] ) ) {
		return '@' . $seg[1];
	}
	if ( 'facebook' === $key && $seg && preg_match( '/^[A-Za-z0-9.]{2,50}$/', $seg[0] ) && ! in_array( strtolower( $seg[0] ), $reserved, true ) ) {
		return $seg[0];
	}
	if ( 'linkedin' === $key && 2 <= count( $seg ) && in_array( strtolower( $seg[0] ), array( 'company', 'in', 'school', 'showcase' ), true ) ) {
		return $seg[1];
	}
	return preg_replace( '/^www\./', '', (string) wp_parse_url( $url, PHP_URL_HOST ) );
}

/**
 * The rows.
 *
 * @return string HTML
 */
function gm_render_follow() {
	$rows = '';
	foreach ( gm_channels() as $c ) {
		$handle = $c['handle'] ? $c['handle'] : ( $c['url'] ? gm_handle_from_url( $c['url'], $c['key'] ) : ( 'substack' === $c['key'] ? '[name].substack.com' : '[@handle]' ) );
		$inner  = gm_mark( $c['key'] ) . '<span class="name">' . esc_html( $c['name'] ) . '</span><span class="h">' . gm_bdi( $handle ) . '</span>';
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
	$list = array();
	foreach ( gm_platforms() as $key => $p ) {
		$list[] = array( 'key' => $key, 'name' => $p['name'], 'example' => $p['example'] );
	}
	wp_add_inline_script( 'generation-maine-follow-editor-script', 'window.gmPlatforms = ' . wp_json_encode( $list ) . ';', 'before' );
}
add_action( 'init', 'gm_register_follow_block' );
