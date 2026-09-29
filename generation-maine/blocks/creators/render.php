<?php
/**
 * Server render for generation-maine/creators.
 *
 * @package generation-maine
 *
 * @var array $attributes Block attributes.
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}
?>
<div <?php echo get_block_wrapper_attributes(); // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped ?>>
	<?php echo gm_render_creators( array( 'limit' => isset( $attributes['limit'] ) ? (int) $attributes['limit'] : 24 ) ); // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped ?>
</div>
