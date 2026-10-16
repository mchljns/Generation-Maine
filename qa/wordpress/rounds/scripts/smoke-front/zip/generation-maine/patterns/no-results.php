<?php
/**
 * Title: No results
 * Slug: generation-maine/no-results
 * Categories: generation-maine
 * Inserter: no
 * Description: What an archive or a search shows when nothing matches.
 *
 * @package generation-maine
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}
?>
<!-- wp:paragraph -->
<p><?php esc_html_e( 'Nothing here matches.', 'generation-maine' ); ?> <a href="<?php echo esc_url( home_url( '/' ) ); ?>"><?php esc_html_e( 'Go to the home page', 'generation-maine' ); ?></a>.</p>
<!-- /wp:paragraph -->
