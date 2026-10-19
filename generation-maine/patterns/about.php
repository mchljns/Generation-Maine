<?php
/**
 * Title: About
 * Slug: generation-maine/about
 * Categories: generation-maine
 * Description: What the project hopes to achieve: a photograph of a real Maine street beside one statement and the paragraph behind it. Replace the photograph and the draft statement before launch.
 *
 * @package generation-maine
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}
?>
<!-- wp:group {"templateLock":"contentOnly","lock":{"move":true,"remove":true},"tagName":"section","metadata":{"name":"About"},"anchor":"about","className":"block about","layout":{"type":"default"}} -->
<section id="about" class="wp-block-group block about"><!-- wp:group {"className":"w","layout":{"type":"default"}} -->
<div class="wp-block-group w"><!-- wp:group {"className":"body","layout":{"type":"default"}} -->
<div class="wp-block-group body"><!-- wp:group {"className":"media","layout":{"type":"default"}} -->
<div class="wp-block-group media"><!-- wp:image {"sizeSlug":"full","linkDestination":"none","metadata":{"name":"Photo"},"className":"ph"} -->
<figure class="wp-block-image size-full ph"><img src="<?php echo esc_url( get_theme_file_uri( 'assets/img/about.jpg' ) ); ?>" alt="<?php esc_attr_e( 'Lisbon Street, Lewiston, Maine', 'generation-maine' ); ?>"/></figure>
<!-- /wp:image --></div>
<!-- /wp:group -->

<!-- wp:group {"className":"aim","layout":{"type":"default"}} -->
<div class="wp-block-group aim"><!-- wp:paragraph {"metadata":{"name":"Kicker"},"className":"k k-bars"} -->
<p class="k k-bars">What we hope to achieve</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph {"metadata":{"name":"Aim"},"className":"big"} -->
<p class="big">Everyone who leaves Maine has a reason. We want the people who stay to show what it costs, one rule at a time.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph {"metadata":{"name":"Note (draft marker)"},"className":"note"} -->
<p class="note">[CONFIRM: the aim, in Maine Policy Institute's words. This is a draft to edit.]</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph {"metadata":{"name":"Goal"},"className":"goal"} -->
<p class="goal">Generation Maine wants young people in Maine to see the rules behind what their lives cost, and to say so in public. Young Mainers film where they live. Each clip takes one rule, a lease clause, a license fee, a permit, a line on a pay stub, and shows what it says and what it costs. The clips go out on the creators' own accounts, where their friends already are. The newsletter follows the paperwork behind each one, with the numbers. The more people see the same rule from different towns, the harder it gets to ignore.</p>
<!-- /wp:paragraph --></div>
<!-- /wp:group --></div>
<!-- /wp:group --></div>
<!-- /wp:group --></section>
<!-- /wp:group -->
