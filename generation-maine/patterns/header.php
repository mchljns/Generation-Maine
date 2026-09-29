<?php
/**
 * Title: Header
 * Slug: generation-maine/header
 * Categories: generation-maine
 * Inserter: no
 *
 * @package generation-maine
 */
?>
<!-- wp:group {"align":"full","className":"gm-header","backgroundColor":"primary","textColor":"base","style":{"spacing":{"padding":{"top":"0.75rem","bottom":"0.75rem"}}},"layout":{"type":"constrained","contentSize":"1200px"}} -->
<div class="wp-block-group alignfull gm-header has-base-color has-primary-background-color has-text-color has-background" style="padding-top:0.75rem;padding-bottom:0.75rem"><!-- wp:group {"layout":{"type":"flex","flexWrap":"nowrap","justifyContent":"space-between"}} -->
<div class="wp-block-group"><!-- wp:html -->
<a class="gm-logo" href="<?php echo esc_url( home_url( '/' ) ); ?>" rel="home"><?php echo gm_wordmark_svg(); // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped ?></a>
<!-- /wp:html -->

<!-- wp:html -->
<nav aria-label="<?php esc_attr_e( 'Sections', 'generation-maine' ); ?>"><ul class="gm-nav"><li><a href="#about">About</a></li><li><a href="#creators">Creators</a></li><li><a href="#follow">Follow</a></li></ul></nav>
<!-- /wp:html --></div>
<!-- /wp:group --></div>
<!-- /wp:group -->
