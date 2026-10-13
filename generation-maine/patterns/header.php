<?php
/**
 * Title: Header
 * Slug: generation-maine/header
 * Categories: generation-maine
 * Inserter: no
 * Description: The bar: the lockup, three section links and the newsletter button. Edit the link labels and the button text here; the phone menu copies them.
 *
 * @package generation-maine
 */
?>
<!-- wp:group {"className":"w","layout":{"type":"default"}} -->
<div class="wp-block-group w"><!-- wp:html -->
<a href="#top" aria-label="<?php esc_attr_e( 'Generation Maine, home', 'generation-maine' ); ?>"><?php echo gm_logo( 'lockup-compact-reversed', 'lk' ); // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped ?></a>
<!-- /wp:html -->

<!-- wp:group {"tagName":"nav","ariaLabel":"Page","layout":{"type":"default"}} -->
<nav class="wp-block-group" aria-label="Page"><!-- wp:paragraph -->
<p><a href="#about">About</a></p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p><a href="#creators">Creators</a></p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p><a href="#follow">Follow</a></p>
<!-- /wp:paragraph --></nav>
<!-- /wp:group -->

<!-- wp:buttons {"className":"cta-wrap"} -->
<div class="wp-block-buttons cta-wrap"><!-- wp:button {"className":"b2 cta"} -->
<div class="wp-block-button b2 cta"><a class="wp-block-button__link wp-element-button" href="#newsletter">Get the newsletter</a></div>
<!-- /wp:button --></div>
<!-- /wp:buttons -->

<!-- wp:html -->
<button class="menu" id="menu" aria-label="<?php esc_attr_e( 'Menu', 'generation-maine' ); ?>" aria-expanded="false" aria-controls="sheet"><svg width="24" height="24" viewBox="0 0 24 24" aria-hidden="true"><path d="M3 7h18M3 12h18M3 17h18" stroke="currentColor" stroke-width="2"/></svg></button>
<!-- /wp:html --></div>
<!-- /wp:group -->
