<?php
/**
 * Server render for generation-maine/newsletter.
 *
 * @package generation-maine
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}
?>
<div <?php echo get_block_wrapper_attributes(); // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped ?>>
	<?php echo gm_render_newsletter_form(); // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped ?>
</div>
