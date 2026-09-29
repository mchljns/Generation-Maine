<?php
/**
 * Creates placeholder creators for testing the grid. Every one is flagged as a placeholder.
 *
 * Usage:  wp eval-file bin/seed-creators.php 12
 * Remove: wp eval-file bin/seed-creators.php 0   (deletes all placeholder creators)
 *
 * @package generation-maine
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit( 1 );
}

$gm_count = isset( $args[0] ) ? (int) $args[0] : ( defined( 'GM_SEED_COUNT' ) ? (int) GM_SEED_COUNT : 12 );

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

$gm_words = array( 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Eleven', 'Twelve' );
for ( $gm_i = 0; $gm_i < $gm_count; $gm_i++ ) {
	$gm_id = wp_insert_post(
		array(
			'post_type'    => 'gm_creator',
			'post_status'  => 'publish',
			'post_title'   => 'Creator ' . ( isset( $gm_words[ $gm_i ] ) ? $gm_words[ $gm_i ] : ( $gm_i + 1 ) ),
			'post_content' => 'Placeholder bio. The creator will write two or three sentences here about where they live and what their videos are about.',
			'menu_order'   => $gm_i,
		)
	);
	update_post_meta( $gm_id, 'gm_hometown', 'Hometown, Maine' );
	update_post_meta( $gm_id, 'gm_placeholder', true );
	if ( 0 === $gm_i % 2 ) {
		update_post_meta( $gm_id, 'gm_instagram', 'https://example.com/instagram' );
		update_post_meta( $gm_id, 'gm_tiktok', 'https://example.com/tiktok' );
	}
}

if ( defined( 'WP_CLI' ) && WP_CLI ) {
	WP_CLI::success( sprintf( 'Seeded %d placeholder creators.', $gm_count ) );
}
