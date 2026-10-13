<?php
// php wpstate.php video|novideo|empty|full|nonews|news
$_SERVER['HTTP_HOST'] = '127.0.0.1:8080';
require '/tmp/claude-0/wp/core/wp-load.php';
$mode = $argv[1];
$cs = get_posts( array( 'post_type' => 'gm_creator', 'post_status' => 'any', 'numberposts' => -1, 'orderby' => 'menu_order', 'order' => 'ASC' ) );
if ( 'video' === $mode ) { foreach ( array_slice( $cs, 0, 2 ) as $i => $c ) { update_post_meta( $c->ID, 'gm_clip_url', 'http://127.0.0.1:8080/wp-content/uploads/clips/creator-' . ( $i + 1 ) . '.webm' ); delete_post_meta( $c->ID, 'gm_clip_id' ); } }
if ( 'empty' === $mode ) { foreach ( $cs as $c ) wp_update_post( array( 'ID' => $c->ID, 'post_status' => 'draft' ) ); }
if ( 'full' === $mode ) { foreach ( $cs as $c ) wp_update_post( array( 'ID' => $c->ID, 'post_status' => 'publish' ) ); }
if ( 'nonews' === $mode ) { delete_option( 'gm_newsletter_url' ); }
if ( 'news' === $mode ) { update_option( 'gm_newsletter_url', 'https://generationmaine.substack.com/subscribe' ); update_option( 'gm_instagram_url', 'https://www.instagram.com/generationmaine/' ); update_option( 'gm_instagram_handle', '@generationmaine' ); }
echo $mode, ": creators published ", count( get_posts( array( 'post_type' => 'gm_creator', 'numberposts' => -1 ) ) ), ", newsletter '", get_option( 'gm_newsletter_url', '' ), "'\n";
