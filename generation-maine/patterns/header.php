<?php
/**
 * Title: Header
 * Slug: generation-maine/header
 * Categories: generation-maine
 * Inserter: no
 * Description: The bar. A Pine band over the hero that folds into a floating capsule on the first scroll. Edit the link labels and the button text here.
 *
 * @package generation-maine
 */
?>
<!-- wp:group {"tagName":"header","className":"top","anchor":"topbar","layout":{"type":"default"}} -->
<header id="topbar" class="wp-block-group top"><!-- wp:group {"className":"w","layout":{"type":"default"}} -->
<div class="wp-block-group w"><!-- wp:html -->
<a href="#top" aria-label="<?php esc_attr_e( 'Generation Maine, home', 'generation-maine' ); ?>"><?php echo gm_header_lockups(); // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped ?></a>
<!-- /wp:html -->

<!-- wp:group {"tagName":"nav","ariaLabel":"Page","layout":{"type":"flex","flexWrap":"nowrap"}} -->
<nav class="wp-block-group" aria-label="Page"><!-- wp:paragraph -->
<p><a href="#about">About</a></p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p><a href="#creators">Creators</a></p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p><a href="#words">In their words</a></p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p><a href="#follow">Follow</a></p>
<!-- /wp:paragraph --></nav>
<!-- /wp:group -->

<!-- wp:buttons {"className":"cta"} -->
<div class="wp-block-buttons cta"><!-- wp:button -->
<div class="wp-block-button"><a class="wp-block-button__link wp-element-button" href="#news">Get the newsletter</a></div>
<!-- /wp:button --></div>
<!-- /wp:buttons -->

<!-- wp:html -->
<button class="menu" id="menu" aria-expanded="false" aria-controls="sheet" aria-label="<?php esc_attr_e( 'Menu', 'generation-maine' ); ?>"><i></i><i></i><i></i></button><span class="prog" id="prog" aria-hidden="true"></span>
<!-- /wp:html --></div>
<!-- /wp:group --></header>
<!-- /wp:group -->

<!-- wp:html -->
<div class="sheet" id="sheet" aria-hidden="true"><nav aria-label="<?php esc_attr_e( 'Page', 'generation-maine' ); ?>"></nav><div class="foot"><a class="cta" href="#news"><?php esc_html_e( 'Get the newsletter', 'generation-maine' ); ?></a></div></div>
<!-- /wp:html -->
