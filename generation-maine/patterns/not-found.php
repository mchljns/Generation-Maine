<?php
/**
 * Title: Not found
 * Slug: generation-maine/not-found
 * Categories: generation-maine
 * Inserter: no
 * Description: The line under "This page does not exist", with a link to the home page wherever the site is installed.
 *
 * @package generation-maine
 */
?>
<!-- wp:paragraph {"className":"lede"} -->
<p class="lede"><?php esc_html_e( 'Generation Maine is a one-page site.', 'generation-maine' ); ?> <a href="<?php echo esc_url( home_url( '/' ) ); ?>"><?php esc_html_e( 'Go to the home page', 'generation-maine' ); ?></a>.</p>
<!-- /wp:paragraph -->
