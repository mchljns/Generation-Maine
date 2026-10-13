<?php
/**
 * Creates placeholder creators so the page can be reviewed before anyone is cast. Every one is flagged as a placeholder.
 *
 * Usage:  wp eval-file bin/seed-creators.php 9 [media]
 * Remove: wp eval-file bin/seed-creators.php 0   (deletes every placeholder creator and the media this script imported)
 *
 * [media] is a folder on this server or a web address holding portrait-1.jpg … portrait-9.jpg and creator-1.gif … creator-9.gif,
 * for example the v2 preview's media folder: https://mchljns.github.io/Generation-Maine/v2/media
 * Each portrait becomes the creator's avatar and each GIF their clip, imported into the media library. Without [media] the
 * creators have no avatar and no clip, and the page shows the placeholder figure on a navy field.
 *
 * @package generation-maine
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit( 1 );
}

require_once ABSPATH . 'wp-admin/includes/media.php';
require_once ABSPATH . 'wp-admin/includes/file.php';
require_once ABSPATH . 'wp-admin/includes/image.php';

$gm_count = isset( $args[0] ) ? (int) $args[0] : ( defined( 'GM_SEED_COUNT' ) ? (int) GM_SEED_COUNT : 9 );
$gm_media = isset( $args[1] ) ? rtrim( (string) $args[1], '/' ) : ( defined( 'GM_SEED_MEDIA' ) ? rtrim( GM_SEED_MEDIA, '/' ) : '' );

/**
 * Import one file into the media library from a folder or an address. Returns the attachment id, or 0.
 *
 * @param string $base    Folder or address.
 * @param string $name    File name.
 * @param int    $post_id Creator post the file belongs to.
 * @return int
 */
function gm_seed_import( $base, $name, $post_id ) {
	if ( '' === $base ) {
		return 0;
	}
	if ( is_dir( $base ) ) {
		if ( ! file_exists( $base . '/' . $name ) ) {
			return 0;
		}
		$tmp = wp_tempnam( $name );
		copy( $base . '/' . $name, $tmp );
	} else {
		$tmp = download_url( $base . '/' . $name, 60 );
		if ( is_wp_error( $tmp ) ) {
			if ( defined( 'WP_CLI' ) && WP_CLI ) {
				WP_CLI::warning( $name . ': ' . $tmp->get_error_message() );
			}
			return 0;
		}
	}
	$id = media_handle_sideload( array( 'name' => $name, 'tmp_name' => $tmp ), $post_id );
	if ( is_wp_error( $id ) ) {
		@unlink( $tmp ); // phpcs:ignore WordPress.PHP.NoSilencedErrors.Discouraged
		return 0;
	}
	update_post_meta( $id, 'gm_seeded', 1 );
	return (int) $id;
}

// Remove what an earlier run made: the placeholder creators, then the media this script imported.
$gm_existing = get_posts(
	array(
		'post_type'   => 'gm_creator',
		'post_status' => 'any',
		'numberposts' => -1,
		'meta_key'    => 'gm_placeholder', // phpcs:ignore WordPress.DB.SlowDBQuery.slow_db_query_meta_key
		'meta_value'  => '1', // phpcs:ignore WordPress.DB.SlowDBQuery.slow_db_query_meta_value
		'fields'      => 'ids',
	)
);
foreach ( $gm_existing as $gm_id ) {
	wp_delete_post( $gm_id, true );
}
$gm_old_media = get_posts(
	array(
		'post_type'   => 'attachment',
		'post_status' => 'any',
		'numberposts' => -1,
		'meta_key'    => 'gm_seeded', // phpcs:ignore WordPress.DB.SlowDBQuery.slow_db_query_meta_key
		'fields'      => 'ids',
	)
);
foreach ( $gm_old_media as $gm_id ) {
	wp_delete_attachment( $gm_id, true );
}

$gm_json = __DIR__ . '/creators-placeholder.json';
$gm_list = file_exists( $gm_json ) ? json_decode( (string) file_get_contents( $gm_json ), true ) : null; // phpcs:ignore WordPressVIPMinimum.Performance.FetchingRemoteData.FileGetContentsUnknown
$gm_list = isset( $gm_list['creators'] ) ? $gm_list['creators'] : array();
$gm_towns = array( 'Skowhegan', 'Presque Isle', 'Biddeford', 'Machias', 'Lewiston', 'Rumford', 'Belfast', 'Fort Kent', 'Sanford', 'Bangor', 'Rockland', 'Farmington' );
for ( $gm_i = 0; $gm_i < $gm_count; $gm_i++ ) {
	$gm_c  = isset( $gm_list[ $gm_i ] ) ? $gm_list[ $gm_i ] : array();
	$gm_n  = ( $gm_i % 9 ) + 1;
	$gm_id = wp_insert_post(
		array(
			'post_type'    => 'gm_creator',
			'post_status'  => 'publish',
			'post_title'   => isset( $gm_c['name'] ) ? $gm_c['name'] : '[Creator name]',
			'post_content' => isset( $gm_c['bio'] ) ? $gm_c['bio'] : '[Two or three sentences in the creator\'s words.]',
			'menu_order'   => $gm_i,
		)
	);
	update_post_meta( $gm_id, 'gm_handle', isset( $gm_c['handle'] ) ? $gm_c['handle'] : '@handle' );
	update_post_meta( $gm_id, 'gm_hometown', isset( $gm_c['town'] ) ? $gm_c['town'] : $gm_towns[ $gm_i % count( $gm_towns ) ] );
	update_post_meta( $gm_id, 'gm_clip_len', isset( $gm_c['len'] ) ? $gm_c['len'] : '' );
	update_post_meta( $gm_id, 'gm_placeholder', true );
	$gm_avatar = gm_seed_import( $gm_media, 'portrait-' . $gm_n . '.jpg', $gm_id );
	if ( $gm_avatar ) {
		set_post_thumbnail( $gm_id, $gm_avatar );
	}
	$gm_clip = gm_seed_import( $gm_media, 'creator-' . $gm_n . '.gif', $gm_id );
	if ( $gm_clip ) {
		update_post_meta( $gm_id, 'gm_clip_id', $gm_clip );
	}
}

if ( defined( 'WP_CLI' ) && WP_CLI ) {
	WP_CLI::success( sprintf( 'Seeded %d placeholder creators%s.', $gm_count, $gm_media ? ' with media from ' . $gm_media : '' ) );
}
