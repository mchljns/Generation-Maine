<?php
/**
 * Server render for generation-maine/follow.
 *
 * @package generation-maine
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}
// the editor's preview of links and handles not saved yet (blocks/follow/index.js); never on the page itself
$gm_preview = isset( $attributes['preview'] ) && is_array( $attributes['preview'] ) ? $attributes['preview'] : array();
if ( $gm_preview && wp_is_serving_rest_request() && current_user_can( 'manage_options' ) ) {
	gm_setting_preview( $gm_preview );
}
?>
<div <?php echo get_block_wrapper_attributes( array( 'class' => 'list' ) ); // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped ?>><?php echo gm_render_follow(); // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped ?></div>
