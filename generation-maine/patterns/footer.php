<?php
/**
 * Title: Footer
 * Slug: generation-maine/footer
 * Categories: generation-maine
 * Inserter: no
 * Description: The two-line lockup, a line about the project and the legal line.
 *
 * @package generation-maine
 */
?>
<!-- wp:group {"tagName":"footer","className":"site","layout":{"type":"default"}} -->
<footer class="wp-block-group site"><!-- wp:group {"className":"w","layout":{"type":"default"}} -->
<div class="wp-block-group w"><!-- wp:html -->
<?php echo gm_logo( 'lockup-two-line-reversed', 'lk' ); // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped ?>
<!-- /wp:html -->

<!-- wp:group {"layout":{"type":"default"}} -->
<div class="wp-block-group"><!-- wp:paragraph -->
<p>Young Mainers on the rules that shape their lives. Short videos and a newsletter, made in Maine.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph {"className":"fine"} -->
<p class="fine">© 2026 Generation Maine. [CONFIRM: legal name, address and contact]</p>
<!-- /wp:paragraph --></div>
<!-- /wp:group --></div>
<!-- /wp:group --></footer>
<!-- /wp:group -->
