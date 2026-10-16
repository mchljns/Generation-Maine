<?php
/**
 * The pieces of the bar and the hero that are drawn by the theme rather than typed in the editor: the logo link, the phone
 * menu button and the Maine mural. They are one small block, generation-maine/part, so the editor shows them as they look on
 * the page instead of as raw HTML. Also: links to the page's sections keep working from every other page.
 *
 * @package generation-maine
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

/**
 * Where a link to one of the page's sections should point from the page being shown: a bare #anchor on the front page,
 * the front page plus the anchor everywhere else.
 *
 * @param string $anchor Anchor without the #.
 * @return string
 */
function gm_section_url( $anchor ) {
	if ( is_front_page() && ! is_paged() ) {
		return '#' . $anchor;
	}
	return home_url( '/#' . $anchor );
}

/**
 * The logo, linking to the top of the front page.
 *
 * @return string HTML
 */
function gm_part_logo() {
	$href = is_front_page() ? '#top' : home_url( '/' );
	return '<a href="' . esc_url( $href ) . '" aria-label="' . esc_attr__( 'Generation Maine, home', 'generation-maine' ) . '">' . gm_logo( 'lockup-compact-reversed', 'lk' ) . '</a>';
}

/**
 * The phone menu button.
 *
 * @return string HTML
 */
function gm_part_menu() {
	return '<button class="menu" id="menu" type="button" aria-label="' . esc_attr__( 'Menu', 'generation-maine' ) . '" aria-expanded="false" aria-controls="sheet"><svg width="24" height="24" viewBox="0 0 24 24" aria-hidden="true"><path d="M3 7h18M3 12h18M3 17h18" stroke="currentColor" stroke-width="2"/></svg></button>';
}

/**
 * The Maine mural, drawn on the server so it shows in the editor and without JavaScript. The page script only animates it.
 *
 * @return string HTML
 */
function gm_part_mural() {
	$file = get_theme_file_path( 'assets/data/mural.json' );
	$data = file_exists( $file ) ? json_decode( (string) file_get_contents( $file ), true ) : null; // phpcs:ignore WordPressVIPMinimum.Performance.FetchingRemoteData.FileGetContentsUnknown
	if ( empty( $data['lines'] ) || empty( $data['clip'] ) ) {
		return '<div class="mural" id="mural" aria-hidden="true"></div>';
	}
	$paths = '';
	foreach ( $data['lines'] as $line ) {
		list( $x0, $y0, $x1, $y1, $w ) = $line;
		$color  = ! empty( $line[5] ) ? $line[5] : '#FFFFFF';
		$paths .= sprintf( '<path d="M%s %s L%s %s" stroke="%s" stroke-width="%s" fill="none" pathLength="1"/>', (float) $x0, (float) $y0, (float) $x1, (float) $y1, esc_attr( $color ), (float) $w );
	}
	return '<div class="mural" id="mural" aria-hidden="true"><svg viewBox="0 0 720 720" aria-hidden="true" focusable="false"><defs><clipPath id="muralclip"><path d="' . esc_attr( $data['clip'] ) . '"/></clipPath></defs><g clip-path="url(#muralclip)">' . $paths . '</g></svg></div>';
}

/**
 * Render one part by name. Each part shows once per page: a duplicated Logo, Phone menu button or Maine mural (the editor
 * marks the copy) renders nothing, so the page never carries two menus or two mural ids.
 *
 * @param string $name logo, menu or mural.
 * @return string HTML
 */
function gm_render_part( $name ) {
	static $done = array();
	if ( isset( $done[ $name ] ) ) {
		return '';
	}
	$done[ $name ] = true;
	switch ( $name ) {
		case 'logo':
			return gm_part_logo();
		case 'menu':
			return gm_part_menu();
		case 'mural':
			return gm_part_mural();
	}
	return '';
}

/**
 * The block.
 */
function gm_register_part_block() {
	register_block_type( get_theme_file_path( 'blocks/part' ) );
}
add_action( 'init', 'gm_register_part_block' );

/**
 * The bar and the footer link to the page's sections by anchor. Away from the front page those anchors do not exist, so
 * point them at the front page instead.
 *
 * @param string $html  Block output.
 * @param array  $block Block.
 * @return string
 */
function gm_absolute_section_links( $html, $block ) {
	if ( is_front_page() && ! is_paged() ) {
		return $html;
	}
	if ( empty( $block['attrs']['slug'] ) || ! in_array( $block['attrs']['slug'], array( 'header', 'footer' ), true ) ) {
		return $html;
	}
	return preg_replace_callback(
		'/href="#([A-Za-z][\w-]*)"/',
		function ( $m ) {
			return 'href="' . esc_url( home_url( '/#' . $m[1] ) ) . '"';
		},
		$html
	);
}
add_filter( 'render_block_core/template-part', 'gm_absolute_section_links', 10, 2 );

/**
 * The bar's section links as the editor left them, for the footer and the phone menu: [ [ href, label ], ... ].
 * Read from the header template part, customized or not. On a page the bar has already been drawn by the time the footer
 * asks, so its markup is read from that render (gm_capture_header_links) instead of rendering the part a second time.
 *
 * @param string|null $rendered The header part as it was just rendered, when called from the capture below.
 * @return array<int,array{0:string,1:string}>
 */
function gm_header_links( $rendered = null ) {
	static $links = null;
	if ( null !== $links ) {
		return $links;
	}
	$links = array();
	if ( null !== $rendered ) {
		$html = $rendered;
	} else {
		$part = function_exists( 'get_block_template' ) ? get_block_template( get_stylesheet() . '//header', 'wp_template_part' ) : null;
		$html = $part && ! empty( $part->content ) ? do_blocks( $part->content ) : '';
	}
	if ( $html && preg_match( '/<nav\b[^>]*>(.*?)<\/nav>/s', $html, $nav ) && preg_match_all( '/<a\s[^>]*href="([^"]*)"[^>]*>(.*?)<\/a>/s', $nav[1], $found, PREG_SET_ORDER ) ) {
		foreach ( $found as $a ) {
			$label = trim( wp_strip_all_tags( $a[2] ) );
			if ( '' !== $label ) {
				$links[] = array( html_entity_decode( $a[1], ENT_QUOTES ), $label );
			}
		}
	}
	return $links;
}

/**
 * Keep the header part's links from its own render, before section links are made absolute away from the front page.
 *
 * @param string $html  Block output.
 * @param array  $block Block.
 * @return string
 */
function gm_capture_header_links( $html, $block ) {
	if ( isset( $block['attrs']['slug'] ) && 'header' === $block['attrs']['slug'] ) {
		gm_header_links( $html );
	}
	return $html;
}
add_filter( 'render_block_core/template-part', 'gm_capture_header_links', 9, 2 );
