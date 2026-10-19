<?php
/**
 * The dashboard for the people who keep the site up to date: a "Start here" box with the three places they edit, the share
 * image picker and the description counter on Settings > Generation Maine, and comments turned off, since the site takes none.
 *
 * @package generation-maine
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

/**
 * The "Start here" box, first on the dashboard.
 */
function gm_dashboard_widget() {
	wp_add_dashboard_widget( 'gm_start', __( 'Generation Maine: start here', 'generation-maine' ), 'gm_dashboard_widget_html' );
	// first in the first column
	global $wp_meta_boxes;
	if ( isset( $wp_meta_boxes['dashboard']['normal']['core']['gm_start'] ) ) {
		$box = array( 'gm_start' => $wp_meta_boxes['dashboard']['normal']['core']['gm_start'] );
		unset( $wp_meta_boxes['dashboard']['normal']['core']['gm_start'] );
		$wp_meta_boxes['dashboard']['normal']['core'] = $box + $wp_meta_boxes['dashboard']['normal']['core']; // phpcs:ignore WordPress.WP.GlobalVariablesOverride.Prohibited
	}
}
add_action( 'wp_dashboard_setup', 'gm_dashboard_widget' );

/**
 * The box.
 */
function gm_dashboard_widget_html() {
	$home  = 'page' === get_option( 'show_on_front' ) ? (int) get_option( 'page_on_front' ) : 0;
	$items = array();
	if ( $home && current_user_can( 'edit_post', $home ) ) {
		$items[] = array( get_edit_post_link( $home ), __( 'Edit the home page', 'generation-maine' ), __( 'The words, buttons and photo on the front page. Click any text and type. The sections are locked, so they cannot be moved or deleted by accident. Click Save when done.', 'generation-maine' ) );
	}
	if ( current_user_can( 'edit_posts' ) ) {
		$items[] = array( admin_url( 'edit.php?post_type=gm_creator' ), __( 'Creators', 'generation-maine' ), __( 'Add a creator with their photo, clip and links. Untick "Show on the home page" to take one off the page without deleting them.', 'generation-maine' ) );
	}
	if ( current_user_can( 'manage_options' ) ) {
		$items[] = array( gm_settings_url(), __( 'Settings > Generation Maine', 'generation-maine' ), ( gm_seo_plugin_active() ? __( 'The channel links, the newsletter and the footer lines. What Google and social posts show is in the Yoast SEO box on the Home page.', 'generation-maine' ) : __( 'The channel links, the newsletter, what Google and social posts show, and the footer lines.', 'generation-maine' ) ) );
	}
	echo '<ul style="margin:0">';
	foreach ( $items as $item ) {
		echo '<li style="margin:0 0 12px"><a href="' . esc_url( $item[0] ) . '" style="font-size:14px;font-weight:600">' . esc_html( $item[1] ) . '</a><br><span class="description">' . esc_html( $item[2] ) . '</span></li>';
	}
	echo '</ul>';
}

/**
 * The share image picker and the description counter on the settings screen.
 *
 * @param string $hook Screen.
 */
function gm_settings_assets( $hook ) {
	if ( 'settings_page_generation_maine' !== $hook ) {
		return;
	}
	wp_enqueue_media();
	wp_register_script( 'gm-settings', false, array( 'jquery' ), GM_BUILD_HASH, true );
	wp_enqueue_script( 'gm-settings' );
	wp_add_inline_script(
		'gm-settings',
		'jQuery(function($){
	$(".gm-image-field").each(function(){var box=$(this),input=box.find("input"),img=box.find("img"),frame;
		var show=function(){var v=input.val();img.attr("src",v||"").toggle(!!v);box.find(".gm-image-clear").toggle(!!v);};
		box.on("click",".gm-image-pick",function(e){e.preventDefault();if(!frame){frame=wp.media({title:' . wp_json_encode( __( 'Choose the share image', 'generation-maine' ) ) . ',library:{type:"image"},multiple:false,button:{text:' . wp_json_encode( __( 'Use this image', 'generation-maine' ) ) . '}});frame.on("select",function(){input.val(frame.state().get("selection").first().toJSON().url);show();});}frame.open();});
		box.on("click",".gm-image-clear",function(e){e.preventDefault();input.val("");show();});input.on("input",show);show();});
	var d=$("#gm_seo_description");if(d.length){var c=$("<p class=\"description\"></p>").insertAfter(d);var n=function(){var l=d.val().length;c.text(l+' . wp_json_encode( __( ' characters. Aim for 120 to 160.', 'generation-maine' ) ) . ').css("color",l>160?"#b32d2e":"");};d.on("input",n);n();}
});'
	);
}
add_action( 'admin_enqueue_scripts', 'gm_settings_assets' );

/**
 * The site takes no comments: closed everywhere, and the Comments screens and links are hidden.
 */
function gm_no_comments() {
	foreach ( array( 'post', 'page' ) as $type ) {
		remove_post_type_support( $type, 'comments' );
		remove_post_type_support( $type, 'trackbacks' );
	}
}
add_action( 'init', 'gm_no_comments', 100 );
add_filter( 'comments_open', '__return_false', 20 );
add_filter( 'pings_open', '__return_false', 20 );
add_filter( 'comments_array', '__return_empty_array', 10 );

/**
 * Hide the Comments menu.
 */
function gm_no_comments_menu() {
	remove_menu_page( 'edit-comments.php' );
}
add_action( 'admin_menu', 'gm_no_comments_menu', 99 );

/**
 * Hide the comments bubble in the toolbar.
 *
 * @param WP_Admin_Bar $bar Toolbar.
 */
function gm_no_comments_bar( $bar ) {
	$bar->remove_node( 'comments' );
}
add_action( 'admin_bar_menu', 'gm_no_comments_bar', 999 );

/**
 * Drop the comments box from the dashboard.
 */
function gm_no_comments_dashboard() {
	remove_meta_box( 'dashboard_recent_comments', 'dashboard', 'normal' );
}
add_action( 'wp_dashboard_setup', 'gm_no_comments_dashboard' );
