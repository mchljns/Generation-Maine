<?php
/**
 * Creates placeholder creators so the page can be reviewed before anyone is cast. Every one is flagged as a placeholder.
 *
 * Usage:  wp eval-file bin/seed-creators.php 9 [media]
 * Remove: wp eval-file bin/seed-creators.php 0   (deletes the creators this script made that are still placeholders, and the
 *         media it imported that no other creator uses. A creator you made yourself is never touched, even if it is marked
 *         Placeholder; neither is a seeded creator you turned into a real one by unticking Placeholder. Creators made by the
 *         theme 3.0.0 script, which did not mark them, count as made by this script while they are unchanged.)
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
 * A warning on the command line.
 *
 * @param string $msg Message.
 */
function gm_seed_warn( $msg ) {
	if ( defined( 'WP_CLI' ) && WP_CLI ) {
		WP_CLI::warning( $msg );
	}
}

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
			gm_seed_warn( $name . ': ' . $tmp->get_error_message() );
			return 0;
		}
	}
	$id = media_handle_sideload( array( 'name' => $name, 'tmp_name' => $tmp ), $post_id );
	if ( is_wp_error( $id ) ) {
		@unlink( $tmp ); // phpcs:ignore WordPress.PHP.NoSilencedErrors.Discouraged
		gm_seed_warn( $name . ': ' . $id->get_error_message() );
		return 0;
	}
	update_post_meta( $id, 'gm_seeded', 1 );
	return (int) $id;
}

$gm_json  = __DIR__ . '/creators-placeholder.json';
$gm_list  = file_exists( $gm_json ) ? json_decode( (string) file_get_contents( $gm_json ), true ) : null; // phpcs:ignore WordPressVIPMinimum.Performance.FetchingRemoteData.FileGetContentsUnknown
$gm_list  = isset( $gm_list['creators'] ) ? $gm_list['creators'] : array();
$gm_towns = array( 'Skowhegan', 'Presque Isle', 'Biddeford', 'Machias', 'Lewiston', 'Rumford', 'Belfast', 'Fort Kent', 'Sanford', 'Bangor', 'Rockland', 'Farmington' );

/**
 * Whether a creator is one the theme 3.0.0 script made and nobody has changed. That script marked its creators Placeholder
 * but not gm_seeded, so they are known by what it wrote: a seed's exact name, handle, hometown and story, still marked
 * Placeholder, with no avatar or clip other than media the script imported. A creator a person made never matches all of it.
 *
 * @param int   $id      Creator.
 * @param array $entries Entries of creators-placeholder.json.
 * @param array $towns   Towns the script used past the end of the list.
 * @return bool
 */
function gm_seed_is_old( $id, $entries, $towns ) {
	$norm = static function ( $s ) {
		return trim( preg_replace( '/\s+/', ' ', html_entity_decode( wp_strip_all_tags( (string) $s ), ENT_QUOTES, 'UTF-8' ) ) );
	};
	$post = get_post( $id );
	if ( ! $post || ! get_post_meta( $id, 'gm_placeholder', true ) || get_post_meta( $id, 'gm_seeded', true ) ) {
		return false;
	}
	foreach ( array( '_thumbnail_id', 'gm_clip_id' ) as $key ) {
		$file = (int) get_post_meta( $id, $key, true );
		if ( $file && ! get_post_meta( $file, 'gm_seeded', true ) ) {
			return false;
		}
	}
	$handle = get_post_meta( $id, 'gm_handle', true );
	$town   = get_post_meta( $id, 'gm_hometown', true );
	foreach ( $entries as $c ) {
		if ( isset( $c['name'], $c['handle'], $c['town'], $c['bio'] ) && $norm( $post->post_title ) === $norm( $c['name'] ) && $handle === $c['handle'] && $town === $c['town'] && $norm( $post->post_content ) === $norm( $c['bio'] ) ) {
			return true;
		}
	}
	// past the end of the list the script wrote fixed placeholder text
	return '[Creator name]' === $norm( $post->post_title ) && '@handle' === $handle && in_array( $town, $towns, true )
		&& $norm( $post->post_content ) === $norm( '[Two or three sentences in the creator\'s words.]' );
}

// Creators made by the theme 3.0.0 script, unchanged, get the mark this script now sets, so they are removed below too.
$gm_statuses  = array_keys( get_post_stati() );
$gm_old_seeds = get_posts(
	array(
		'post_type'   => 'gm_creator',
		'post_status' => $gm_statuses,
		'numberposts' => -1,
		'fields'      => 'ids',
		'meta_query'  => array( // phpcs:ignore WordPress.DB.SlowDBQuery.slow_db_query_meta_query
			array(
				'key'   => 'gm_placeholder',
				'value' => '1',
			),
			array(
				'key'     => 'gm_seeded',
				'compare' => 'NOT EXISTS',
			),
		),
	)
);
foreach ( $gm_old_seeds as $gm_id ) {
	if ( gm_seed_is_old( $gm_id, $gm_list, $gm_towns ) ) {
		update_post_meta( $gm_id, 'gm_seeded', 1 );
	}
}

// Remove what an earlier run made: the creators this script made that are still placeholders (in any status, the Trash
// included), then the media it imported that no remaining creator uses.
$gm_existing = get_posts(
	array(
		'post_type'   => 'gm_creator',
		'post_status' => $gm_statuses,
		'numberposts' => -1,
		'meta_key'    => 'gm_seeded', // phpcs:ignore WordPress.DB.SlowDBQuery.slow_db_query_meta_key
		'fields'      => 'ids',
	)
);
$gm_removed = 0;
foreach ( $gm_existing as $gm_id ) {
	if ( get_post_meta( $gm_id, 'gm_placeholder', true ) ) {
		wp_delete_post( $gm_id, true );
		++$gm_removed;
	}
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
$gm_kept = 0;
foreach ( $gm_old_media as $gm_id ) {
	$gm_users = get_posts(
		array(
			'post_type'   => 'gm_creator',
			'post_status' => $gm_statuses,
			'numberposts' => 1,
			'fields'      => 'ids',
			'meta_query'  => array( // phpcs:ignore WordPress.DB.SlowDBQuery.slow_db_query_meta_query
				'relation' => 'OR',
				array(
					'key'   => '_thumbnail_id',
					'value' => (string) $gm_id,
				),
				array(
					'key'   => 'gm_clip_id',
					'value' => (string) $gm_id,
				),
			),
		)
	);
	if ( $gm_users ) {
		++$gm_kept;
		continue;
	}
	wp_delete_attachment( $gm_id, true );
}

$gm_imported = 0;
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
	update_post_meta( $gm_id, 'gm_seeded', 1 );
	$gm_avatar = gm_seed_import( $gm_media, 'portrait-' . $gm_n . '.jpg', $gm_id );
	if ( $gm_avatar ) {
		set_post_thumbnail( $gm_id, $gm_avatar );
		++$gm_imported;
	}
	$gm_clip = gm_seed_import( $gm_media, 'creator-' . $gm_n . '.gif', $gm_id );
	if ( $gm_clip ) {
		update_post_meta( $gm_id, 'gm_clip_id', $gm_clip );
		++$gm_imported;
	}
}

if ( defined( 'WP_CLI' ) && WP_CLI ) {
	$gm_note = $gm_kept ? sprintf( ' Kept %d seeded media item(s) that a creator still uses.', $gm_kept ) : '';
	if ( 0 === $gm_count ) {
		WP_CLI::success( sprintf( 'Removed %d placeholder creator(s) made by this script.%s', $gm_removed, $gm_note ) );
	} elseif ( '' === $gm_media ) {
		WP_CLI::success( sprintf( 'Seeded %d placeholder creators with no media.%s', $gm_count, $gm_note ) );
	} else {
		$gm_msg = sprintf( 'Seeded %d placeholder creators; imported %d of %d media files from %s.%s', $gm_count, $gm_imported, $gm_count * 2, $gm_media, $gm_note );
		if ( $gm_imported < $gm_count * 2 ) {
			WP_CLI::warning( $gm_msg );
		} else {
			WP_CLI::success( $gm_msg );
		}
	}
}
