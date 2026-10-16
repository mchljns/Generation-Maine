<?php
/**
 * Server render for generation-maine/posts.
 *
 * @package generation-maine
 *
 * @var array $attributes Block attributes.
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}
?>
<div <?php echo get_block_wrapper_attributes( array( 'class' => 'posts' ) ); // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped ?>>
	<?php echo gm_render_posts( isset( $attributes['count'] ) ? (int) $attributes['count'] : 3 ); // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped ?>
</div>
