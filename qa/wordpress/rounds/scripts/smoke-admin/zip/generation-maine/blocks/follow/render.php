<?php
/**
 * Server render for generation-maine/follow.
 *
 * @package generation-maine
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}
?>
<div <?php echo get_block_wrapper_attributes( array( 'class' => 'list' ) ); // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped ?>><?php echo gm_render_follow(); // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped ?></div>
