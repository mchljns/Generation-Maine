<?php
/**
 * Title: Header
 * Slug: generation-maine/header
 * Categories: generation-maine
 * Inserter: no
 * Description: The bar: the logo, three section links and the newsletter button. Edit the link labels and the button text here; the phone menu and the footer copy them. To edit, click the bar and choose Edit original.
 *
 * @package generation-maine
 */
?>
<!-- wp:group {"metadata":{"name":"Bar"},"className":"gm-bar","layout":{"type":"default"}} -->
<div class="wp-block-group gm-bar"><!-- wp:group {"className":"w","layout":{"type":"default"}} -->
<div class="wp-block-group w"><!-- wp:generation-maine/part {"name":"logo","lock":{"move":true,"remove":true}} /-->

<!-- wp:group {"tagName":"nav","metadata":{"name":"Section links"},"ariaLabel":"Page","layout":{"type":"default"}} -->
<nav class="wp-block-group" aria-label="Page"><!-- wp:paragraph {"metadata":{"name":"Link to About"}} -->
<p><a href="#about">About</a></p>
<!-- /wp:paragraph -->

<!-- wp:paragraph {"metadata":{"name":"Link to Creators"}} -->
<p><a href="#creators">Creators</a></p>
<!-- /wp:paragraph -->

<!-- wp:paragraph {"metadata":{"name":"Link to Follow"}} -->
<p><a href="#follow">Follow</a></p>
<!-- /wp:paragraph --></nav>
<!-- /wp:group -->

<!-- wp:buttons {"metadata":{"name":"Newsletter button"},"className":"cta-wrap"} -->
<div class="wp-block-buttons cta-wrap"><!-- wp:button {"className":"b2 cta"} -->
<div class="wp-block-button b2 cta"><a class="wp-block-button__link wp-element-button" href="#newsletter">Get the newsletter</a></div>
<!-- /wp:button --></div>
<!-- /wp:buttons -->

<!-- wp:generation-maine/part {"name":"menu","lock":{"move":true,"remove":true}} /--></div>
<!-- /wp:group --></div>
<!-- /wp:group -->
