<?php
// php reset.php : clears the test channel and newsletter values and any test video clip addresses
$_SERVER['HTTP_HOST'] = '127.0.0.1:8080';
require '/tmp/claude-0/wp/core/wp-load.php';
foreach ( array( 'gm_newsletter_url', 'gm_instagram_url', 'gm_instagram_handle', 'gm_tiktok_url', 'gm_tiktok_handle', 'gm_youtube_url', 'gm_youtube_handle' ) as $o ) { delete_option( $o ); }
$cs = get_posts( array( 'post_type' => 'gm_creator', 'post_status' => 'any', 'numberposts' => -1, 'orderby' => 'menu_order', 'order' => 'ASC' ) );
foreach ( $cs as $c ) {
	wp_update_post( array( 'ID' => $c->ID, 'post_status' => 'publish' ) );
	delete_post_meta( $c->ID, 'gm_clip_url' );
	echo $c->post_title, ' status=', get_post_status( $c->ID ), ' clip_id=', get_post_meta( $c->ID, 'gm_clip_id', true ), ' thumb=', get_post_thumbnail_id( $c->ID ), "\n";
}
echo 'newsletter=', var_export( get_option( 'gm_newsletter_url', '' ), true ), "\n";
