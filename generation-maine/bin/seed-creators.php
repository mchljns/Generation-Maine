<?php
/**
 * Creates placeholder creators so the page can be reviewed before anyone is cast. Every one is flagged as a placeholder.
 *
 * Usage:  wp eval-file bin/seed-creators.php 9 [clip base URL]
 * Remove: wp eval-file bin/seed-creators.php 0   (deletes all placeholder creators)
 *
 * The clip base URL is a folder holding creator-1.webm … creator-9.webm, for example the splash mockup's media folder.
 * Without it the creators have no clip and the stage shows its plain Pine field.
 *
 * @package generation-maine
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit( 1 );
}

$gm_count = isset( $args[0] ) ? (int) $args[0] : ( defined( 'GM_SEED_COUNT' ) ? (int) GM_SEED_COUNT : 9 );
$gm_clips = isset( $args[1] ) ? rtrim( (string) $args[1], '/' ) : ( defined( 'GM_SEED_CLIPS' ) ? rtrim( GM_SEED_CLIPS, '/' ) : '' );

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

$gm_json = dirname( __DIR__, 4 ) . '/brand/content/creators-placeholder.json';
$gm_json = file_exists( $gm_json ) ? $gm_json : __DIR__ . '/creators-placeholder.json';
$gm_list = file_exists( $gm_json ) ? json_decode( (string) file_get_contents( $gm_json ), true ) : null; // phpcs:ignore WordPressVIPMinimum.Performance.FetchingRemoteData.FileGetContentsUnknown
$gm_list = isset( $gm_list['creators'] ) ? $gm_list['creators'] : array();
$gm_towns = array( 'Skowhegan', 'Presque Isle', 'Biddeford', 'Machias', 'Lewiston', 'Rumford', 'Belfast', 'Fort Kent', 'Sanford', 'Bangor', 'Rockland', 'Farmington' );
for ( $gm_i = 0; $gm_i < $gm_count; $gm_i++ ) {
	$gm_c  = isset( $gm_list[ $gm_i ] ) ? $gm_list[ $gm_i ] : array();
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
	if ( $gm_clips ) {
		update_post_meta( $gm_id, 'gm_clip_url', $gm_clips . '/' . ( isset( $gm_c['clip'] ) ? $gm_c['clip'] : 'creator-' . ( ( $gm_i % 9 ) + 1 ) . '.webm' ) );
	}
	update_post_meta( $gm_id, 'gm_instagram', 'https://instagram.com/' );
	update_post_meta( $gm_id, 'gm_tiktok', 'https://tiktok.com/' );
	update_post_meta( $gm_id, 'gm_youtube', 'https://youtube.com/' );
}

if ( defined( 'WP_CLI' ) && WP_CLI ) {
	WP_CLI::success( sprintf( 'Seeded %d placeholder creators.', $gm_count ) );
}
