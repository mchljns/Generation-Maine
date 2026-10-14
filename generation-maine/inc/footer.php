<?php
/**
 * The family footer: the drawn mark, the line beside it, the page links, the channels, the parent and the family,
 * the legal line. The markup is generated from the v2 page into assets/data/footer.html; the theme fills its tokens from
 * Settings > Generation Maine and the privacy page set under Settings > Privacy.
 *
 * @package generation-maine
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

/**
 * The footer's inner markup.
 *
 * @return string HTML
 */
function gm_render_footer() {
	$file = get_theme_file_path( 'assets/data/footer.html' );
	if ( ! file_exists( $file ) ) {
		return '';
	}
	$privacy = get_privacy_policy_url();
	$contact = gm_setting( 'gm_contact_url' );
	/**
	 * Whether to show the preview build stamp in the footer. On while the site is in review; turn it off at launch with
	 * add_filter( 'gm_show_build', '__return_false' ).
	 */
	$build  = apply_filters( 'gm_show_build', true );
	$tokens = array(
		'{{LINE}}'    => esc_html( gm_setting( 'gm_footer_line' ) ),
		'{{YEAR}}'    => esc_html( wp_date( 'Y' ) ),
		'{{LEGAL}}'   => esc_html( gm_setting( 'gm_legal_line' ) ),
		'{{PRIVACY}}' => $privacy
			? '<a href="' . esc_url( $privacy ) . '">' . esc_html__( 'Privacy', 'generation-maine' ) . '</a>'
			: '<span class="ph" title="' . esc_attr__( '[CONFIRM: privacy policy page]', 'generation-maine' ) . '">' . esc_html__( 'Privacy', 'generation-maine' ) . '</span>',
		'{{CONTACT}}' => $contact ? '<a href="' . esc_url( gm_utm( $contact ) ) . '" rel="noopener">' . esc_html__( 'Contact', 'generation-maine' ) . '</a>' : '',
		'{{BUILD}}'   => $build ? '<span class="ph build" aria-label="' . esc_attr__( 'Preview build', 'generation-maine' ) . '">Build ' . esc_html( GM_BUILD ) . '</span>' : '',
	);
	$html = strtr( (string) file_get_contents( $file ), $tokens ); // phpcs:ignore WordPressVIPMinimum.Performance.FetchingRemoteData.FileGetContentsUnknown
	$html = str_replace( 'utm_medium=splash', 'utm_medium=site', $html );

	// the page links follow the bar: the same targets and labels the editor gave the header, then the newsletter
	$links = gm_header_links();
	if ( $links ) {
		$nav = '';
		foreach ( $links as $l ) {
			$nav .= '<a href="' . esc_url( $l[0] ) . '">' . esc_html( $l[1] ) . '</a>';
		}
		$nav .= '<a href="#newsletter">' . esc_html__( 'Newsletter', 'generation-maine' ) . '</a>';
		$html = preg_replace( '/(<nav class="flinks"[^>]*>).*?(<\/nav>)/s', '$1' . str_replace( array( '\\', '$' ), array( '\\\\', '\\$' ), $nav ) . '$2', $html, 1 );
	}

	// the channel icons open the accounts once their addresses are set; until then they lead to the follow list
	foreach ( gm_channels() as $c ) {
		if ( $c['url'] ) {
			$html = str_replace( '<a href="#follow" aria-label="' . $c['name'] . '">', '<a href="' . esc_url( gm_utm( $c['url'] ) ) . '" target="_blank" rel="noopener" aria-label="' . esc_attr( $c['name'] ) . '">', $html );
		}
	}
	// the wrapper lets the editor style the footer when it is edited on its own
	return '<div class="gm-foot">' . $html . '</div>';
}

/**
 * The block.
 */
function gm_register_footer_block() {
	register_block_type( get_theme_file_path( 'blocks/site-footer' ) );
}
add_action( 'init', 'gm_register_footer_block' );
