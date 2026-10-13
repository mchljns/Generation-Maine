<?php
// Local QA setup for the Generation Maine theme: run with  php setup.php [count] [media-folder]
$_SERVER['HTTP_HOST'] = '127.0.0.1:8080'; $_SERVER['REQUEST_URI'] = '/';
require '/tmp/claude-0/wp/core/wp-load.php';
require_once ABSPATH . 'wp-admin/includes/upgrade.php';
switch_theme( 'generation-maine' );
update_option( 'show_on_front', 'posts' );
// template edits saved in the database override the theme's files; clear them so the files are what renders
foreach ( get_posts( array( 'post_type' => array( 'wp_template', 'wp_template_part', 'wp_global_styles' ), 'post_status' => 'any', 'numberposts' => -1, 'fields' => 'ids' ) ) as $id ) { wp_delete_post( $id, true ); }
wp_set_current_user( 1 );
$args = array( isset( $argv[1] ) ? (int) $argv[1] : 9, isset( $argv[2] ) ? $argv[2] : '' );
define( 'WP_CLI', false );
include get_theme_file_path( 'bin/seed-creators.php' );
$c = get_posts( array( 'post_type' => 'gm_creator', 'numberposts' => -1 ) );
echo 'theme: ' . get_option( 'stylesheet' ) . ' | creators: ' . count( $c ) . ' | with clip: ' . count( array_filter( $c, fn( $p ) => get_post_meta( $p->ID, 'gm_clip_id', true ) ) ) . ' | with avatar: ' . count( array_filter( $c, fn( $p ) => has_post_thumbnail( $p ) ) ) . "\n";
