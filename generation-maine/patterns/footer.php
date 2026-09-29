<?php
/**
 * Title: Footer
 * Slug: generation-maine/footer
 * Categories: generation-maine
 * Inserter: no
 *
 * @package generation-maine
 */
?>
<!-- wp:group {"align":"full","className":"gm-footer","backgroundColor":"primary","textColor":"base","style":{"spacing":{"padding":{"top":"var:preset|spacing|50","bottom":"var:preset|spacing|50"}}},"layout":{"type":"constrained","contentSize":"1200px"}} -->
<div class="wp-block-group alignfull gm-footer has-base-color has-primary-background-color has-text-color has-background" style="padding-top:var(--wp--preset--spacing--50);padding-bottom:var(--wp--preset--spacing--50)"><!-- wp:group {"layout":{"type":"flex","flexWrap":"wrap","justifyContent":"space-between","verticalAlignment":"center"}} -->
<div class="wp-block-group"><!-- wp:html -->
<a class="gm-footer-logo" href="<?php echo esc_url( home_url( '/' ) ); ?>"><?php echo gm_wordmark_svg(); // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped ?></a>
<!-- /wp:html -->

<!-- wp:paragraph {"fontSize":"small"} -->
<p class="has-small-font-size">An initiative of <a href="https://mainepolicy.org/">Maine Policy Institute</a></p>
<!-- /wp:paragraph --></div>
<!-- /wp:group -->

<!-- wp:paragraph {"fontSize":"caption","style":{"spacing":{"margin":{"top":"var:preset|spacing|40"}}}} -->
<p class="has-caption-font-size" style="margin-top:var(--wp--preset--spacing--40)">© 2026 Generation Maine. Stories by young Mainers.</p>
<!-- /wp:paragraph --></div>
<!-- /wp:group -->
