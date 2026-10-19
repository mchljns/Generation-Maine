<?php
/**
 * Generation Maine theme setup.
 *
 * The stylesheet, the script, the footer markup and the mural are generated from the approved v2 page by
 * brand/src/build_theme.py. Fonts are self-hosted and declared in style.css. No Google Fonts call, no build step, no plugin.
 *
 * @package generation-maine
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

require_once get_theme_file_path( 'inc/build.php' );
require_once get_theme_file_path( 'inc/marks.php' );
require_once get_theme_file_path( 'inc/settings.php' );
require_once get_theme_file_path( 'inc/creators.php' );
require_once get_theme_file_path( 'inc/newsletter.php' );
require_once get_theme_file_path( 'inc/follow.php' );
require_once get_theme_file_path( 'inc/footer.php' );
require_once get_theme_file_path( 'inc/seo.php' );
require_once get_theme_file_path( 'inc/parts.php' );
require_once get_theme_file_path( 'inc/home.php' );
require_once get_theme_file_path( 'inc/code.php' );
require_once get_theme_file_path( 'inc/admin.php' );

/**
 * Theme supports. Layout styles are off because the page's own stylesheet lays out every section; the editor gets the
 * same rules through assets/css/editor.css.
 */
function gm_setup() {
	add_theme_support( 'editor-styles' );
	add_theme_support( 'post-thumbnails' );
	add_theme_support( 'responsive-embeds' );
	add_theme_support( 'disable-layout-styles' );
	add_editor_style( 'assets/css/editor.css' );
	remove_theme_support( 'core-block-patterns' );
	register_block_pattern_category( 'generation-maine', array( 'label' => __( 'Generation Maine', 'generation-maine' ) ) );
}
add_action( 'after_setup_theme', 'gm_setup' );

/**
 * No font library: the page's three faces are fixed, so Styles offers no screen to install or pick other fonts.
 *
 * @param array $settings Block editor settings.
 * @return array
 */
function gm_editor_settings( $settings ) {
	$settings['fontLibraryEnabled'] = false;
	return $settings;
}
add_filter( 'block_editor_settings_all', 'gm_editor_settings' );

/**
 * Fonts saved in Styles do not apply: a font installed and switched on under Appearance > Fonts (WordPress 7), or a face picked
 * in Styles under theme 3.1.0, which offered the three faces as presets that no longer exist. Either would bring back font
 * pickers and change the editor but not the page. They are left out wherever the styles are read, so nothing needs a reset;
 * the next save in Styles stores the styles without them.
 *
 * @param WP_Theme_JSON_Data $theme_json The user's global styles.
 * @return WP_Theme_JSON_Data
 */
function gm_user_fonts( $theme_json ) {
	$data  = $theme_json->get_data();
	$clean = gm_without_fonts( $data );
	return $clean === $data ? $theme_json : new WP_Theme_JSON_Data( $clean, 'custom' );
}
add_filter( 'wp_theme_json_data_user', 'gm_user_fonts' );

/**
 * The same for Styles in the Site Editor, which reads the saved styles and their revisions over the REST API.
 *
 * @param WP_REST_Response|WP_Error|mixed $response Response.
 * @param array                           $handler  Route handler.
 * @param WP_REST_Request                 $request  Request.
 * @return WP_REST_Response|WP_Error|mixed
 */
function gm_rest_user_fonts( $response, $handler, $request ) {
	if ( ! $response instanceof WP_REST_Response || ! preg_match( '#^/wp/v2/global-styles/\d+(/revisions(/\d+)?)?$#', $request->get_route() ) ) {
		return $response;
	}
	$data  = $response->get_data();
	$items = isset( $data[0] ) ? $data : array( $data );
	foreach ( $items as $i => $item ) {
		foreach ( array( 'settings', 'styles' ) as $key ) {
			if ( isset( $item[ $key ] ) && is_array( $item[ $key ] ) ) {
				$clean               = gm_without_fonts( array( $key => $item[ $key ] ) );
				$items[ $i ][ $key ] = empty( $clean[ $key ] ) ? new stdClass() : $clean[ $key ];
			}
		}
	}
	$response->set_data( isset( $data[0] ) ? $items : $items[0] );
	return $response;
}
add_filter( 'rest_request_after_callbacks', 'gm_rest_user_fonts', 10, 3 );

/**
 * Global styles without font families or font choices (a font, and the weight and style picked with it; the theme offers no
 * weight or style control of its own).
 *
 * @param array $data Global styles: settings and styles.
 * @return array
 */
function gm_without_fonts( $data ) {
	if ( isset( $data['settings'] ) && is_array( $data['settings'] ) ) {
		$blocks = isset( $data['settings']['blocks'] ) && is_array( $data['settings']['blocks'] ) ? array_keys( $data['settings']['blocks'] ) : array();
		foreach ( array_merge( array( null ), $blocks ) as $name ) {
			$set = null === $name ? $data['settings'] : $data['settings']['blocks'][ $name ];
			if ( isset( $set['typography'] ) && is_array( $set['typography'] ) && isset( $set['typography']['fontFamilies'] ) ) {
				unset( $set['typography']['fontFamilies'] );
				if ( ! $set['typography'] ) {
					unset( $set['typography'] );
				}
				if ( null === $name ) {
					$data['settings'] = $set;
				} else {
					$data['settings']['blocks'][ $name ] = $set;
				}
			}
		}
	}
	if ( isset( $data['styles'] ) && is_array( $data['styles'] ) ) {
		$data['styles'] = gm_without_font_choice( $data['styles'] );
	}
	return $data;
}

/**
 * A styles tree without a font choice, at the root and in every element, block, variation and state below it.
 *
 * @param array $styles Styles.
 * @return array
 */
function gm_without_font_choice( $styles ) {
	foreach ( $styles as $key => $value ) {
		if ( ! is_array( $value ) || ! $value ) {
			continue;
		}
		if ( 'typography' === $key ) {
			unset( $value['fontFamily'], $value['fontWeight'], $value['fontStyle'] );
		}
		$value = gm_without_font_choice( $value );
		// a group left empty by this goes too
		if ( $value ) {
			$styles[ $key ] = $value;
		} else {
			unset( $styles[ $key ] );
		}
	}
	return $styles;
}

/**
 * No Fonts screen: WordPress 7 adds Appearance > Fonts, and a Fonts button on the theme's details, to install and switch on
 * fonts that this theme does not use. A saved link to the screen gets a short note instead.
 */
function gm_no_fonts_screen() {
	remove_submenu_page( 'themes.php', 'font-library.php' );
}
add_action( 'admin_menu', 'gm_no_fonts_screen', 99 );

/**
 * The note on the Fonts screen.
 */
function gm_fonts_screen_note() {
	wp_die(
		esc_html__( 'Generation Maine uses its own three fonts, so the font library is turned off.', 'generation-maine' ),
		esc_html__( 'Fonts', 'generation-maine' ),
		array(
			'response'  => 403,
			'link_url'  => admin_url( 'themes.php' ),
			'link_text' => esc_html__( 'Back to Themes', 'generation-maine' ),
		)
	);
}
add_action( 'load-font-library.php', 'gm_fonts_screen_note' );

/**
 * No Fit text switch on paragraphs and headings (newer WordPress versions have one): theme.json cannot turn it off, and it
 * would resize the page's type.
 *
 * @param array  $args Block type arguments.
 * @param string $name Block name.
 * @return array
 */
function gm_block_supports( $args, $name ) {
	if ( in_array( $name, array( 'core/paragraph', 'core/heading' ), true ) && isset( $args['supports']['typography']['fitText'] ) ) {
		$args['supports']['typography']['fitText'] = false;
	}
	return $args;
}
add_filter( 'register_block_type_args', 'gm_block_supports', 10, 2 );

/**
 * The page's root classes. The v2 page sets them on <html>; several rules depend on two of them sitting on one element.
 *
 * @param string $output Attributes for the html tag.
 * @return string
 */
function gm_html_classes( $output ) {
	if ( is_admin() ) {
		return $output;
	}
	return $output . ' class="static lean euro"';
}
add_filter( 'language_attributes', 'gm_html_classes' );

/**
 * The js class goes on before first paint, so hidden-until-loaded states never flash and transitions never run at load.
 */
function gm_js_class() {
	echo '<script>document.documentElement.classList.add("js")</script>' . "\n";
}
add_action( 'wp_head', 'gm_js_class', 0 );

/**
 * Stylesheet and script. The version is the build hash, so a new build is never served from a stale cache.
 */
function gm_enqueue() {
	wp_enqueue_style( 'generation-maine', get_stylesheet_uri(), array(), GM_BUILD_HASH );
	wp_enqueue_script( 'generation-maine', get_theme_file_uri( 'assets/js/site.js' ), array(), GM_BUILD_HASH, array( 'in_footer' => true ) );
}
add_action( 'wp_enqueue_scripts', 'gm_enqueue' );

/**
 * The hero mural's timing, read by the page script. The mural itself is drawn on the server (gm_part_mural), so only the
 * delay between its lines is printed, not the geometry.
 */
function gm_mural_data() {
	$file = get_theme_file_path( 'assets/data/mural.json' );
	if ( ! file_exists( $file ) ) {
		return;
	}
	$data = json_decode( (string) file_get_contents( $file ), true ); // phpcs:ignore WordPressVIPMinimum.Performance.FetchingRemoteData.FileGetContentsUnknown
	if ( empty( $data['stagger'] ) ) {
		return;
	}
	echo '<script id="maine-data" type="application/json">' . wp_json_encode( array( 'stagger' => absint( $data['stagger'] ) ) ) . '</script>' . "\n"; // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped
}
add_action( 'wp_footer', 'gm_mural_data', 1 );

/**
 * The page's own skip link replaces the one WordPress adds to block themes.
 */
function gm_skip_link() {
	echo '<a class="skip" href="#main">' . esc_html__( 'Skip to content', 'generation-maine' ) . '</a>' . "\n";
	// the phone menu sits outside the bar, as on the v2 page; the page script copies the bar's links and button into it
	echo '<div class="sheet" id="sheet" aria-hidden="true"><nav aria-label="' . esc_attr__( 'Page', 'generation-maine' ) . '"></nav></div>' . "\n";
}
add_action( 'wp_body_open', 'gm_skip_link', 1 );
remove_action( 'wp_footer', 'the_block_template_skip_link' );
remove_action( 'wp_enqueue_scripts', 'wp_enqueue_block_template_skip_link' );

/**
 * Preload the three faces the first screen uses on every page: the headline, the text (the hero lede) and the labels.
 */
function gm_preload_fonts() {
	foreach ( array( 'bricolage-grotesque-800.woff2' => 'font/woff2', 'dm-sans-var.woff2' => 'font/woff2', 'michroma-regular.woff2' => 'font/woff2' ) as $file => $type ) {
		printf( '<link rel="preload" href="%s" as="font" type="%s" crossorigin>' . "\n", esc_url( get_theme_file_uri( 'assets/fonts/' . $file ) ), esc_attr( $type ) );
	}
}
add_action( 'wp_head', 'gm_preload_fonts', 1 );

/**
 * One palette in every theme: the page commits to its own colors.
 */
function gm_color_scheme() {
	echo '<meta name="color-scheme" content="light">' . "\n";
	echo '<meta name="theme-color" content="#0F2E4D">' . "\n";
}
add_action( 'wp_head', 'gm_color_scheme', 0 );

/**
 * Favicon fallback. WordPress prints its own tags once a Site Icon is set in Settings > General.
 * The .ico is marked 32x32 rather than "any", so a browser that reads the SVG fetches only the SVG.
 */
function gm_favicon_fallback() {
	if ( has_site_icon() ) {
		return;
	}
	printf( '<link rel="icon" href="%s" sizes="32x32">' . "\n", esc_url( get_theme_file_uri( 'assets/img/favicon.ico' ) ) );
	printf( '<link rel="icon" href="%s" type="image/svg+xml">' . "\n", esc_url( get_theme_file_uri( 'assets/img/icon.svg' ) ) );
	printf( '<link rel="apple-touch-icon" href="%s">' . "\n", esc_url( get_theme_file_uri( 'assets/img/icon-180.png' ) ) );
}
add_action( 'wp_head', 'gm_favicon_fallback', 2 );

/**
 * Kickers with the family's bars: a paragraph with the class "k-bars" gets the three bars before its text.
 * The hero headline with the class "gm-here" gets its last word in gold and the pulsing dot after it.
 * Both are added as the page renders, so they survive any rewrite of the words in the editor. If a pattern fails on
 * unusual markup, the block is shown as it was saved.
 *
 * @param string $html  Block HTML.
 * @param array  $block Block.
 * @return string
 */
function gm_render_marks( $html, $block ) {
	$class = isset( $block['attrs']['className'] ) ? ' ' . $block['attrs']['className'] . ' ' : '';
	if ( 'core/paragraph' === $block['blockName'] && false !== strpos( $class, ' k-bars ' ) ) {
		$out = preg_replace( '/^(\s*<p\b[^>]*>)/', '$1' . gm_bars(), $html, 1 );
		return null === $out ? $html : $out;
	}
	if ( 'core/heading' === $block['blockName'] && false !== strpos( $class, ' gm-here ' ) ) {
		return gm_mark_here( $html );
	}
	if ( 'core/group' === $block['blockName'] && $class ) {
		// the bar and the footer link to these sections by id, so the ids stay whatever an editor does to the anchor field
		foreach ( array( ' hero ' => 'top', ' about ' => 'about', ' stories-head ' => 'creators', ' follow ' => 'follow', ' nl ' => 'newsletter' ) as $token => $id ) {
			if ( false !== strpos( $class, $token ) ) {
				if ( preg_match( '/^(\s*<[a-z]+\b[^>]*?)\sid="[^"]*"/i', $html ) ) {
					$out = preg_replace( '/^(\s*<[a-z]+\b[^>]*?)\sid="[^"]*"/i', '$1 id="' . $id . '"', $html, 1 );
				} else {
					$out = preg_replace( '/^(\s*<[a-z]+\b)/i', '$1 id="' . $id . '"', $html, 1 );
				}
				return null === $out ? $html : $out;
			}
		}
	}
	return $html;
}
add_filter( 'render_block', 'gm_render_marks', 10, 2 );

/**
 * The hero headline: the last word in gold with the pulsing dot after it. The word is found past any trailing space, line
 * break or no-break space, and inside bold, emphasis or a link. A final period becomes the dot, inside or outside the tag
 * and inside quote marks ("home." gets the dot after the quote); a question mark, an exclamation mark or an ellipsis stays
 * and gets no dot. The markup is walked tag by tag from the end instead of matched with one pattern, so no length of
 * spacing can make it fail; anything it cannot read is shown unchanged.
 *
 * @param string $html Heading block HTML.
 * @return string
 */
function gm_mark_here( $html ) {
	// a tag ends at the first > outside quotes, as in the browser
	$parts = preg_split( '/(<(?:[^>"\']++|"[^"]*+"|\'[^\']*+\')*+>)/', $html, -1, PREG_SPLIT_DELIM_CAPTURE );
	$last  = is_array( $parts ) ? count( $parts ) - 1 : 0;
	// text and tags alternate, so the closing heading tag is the last tag, with nothing but space after it
	if ( $last < 2 || '' !== trim( $parts[ $last ] ) || ! preg_match( '#^</h[1-6]>$#i', $parts[ $last - 1 ] ) ) {
		return $html;
	}
	// bold, emphasis and links can sit inside the word or around it
	$inline = '#^</?(?:strong|b|em|i|a|span|mark|u|s|code)\b#i';
	// first the last visible character, past spacing, stray line breaks and closing quote marks (outside the bold or link
	// too): a single period goes, as the dot takes its place; anything else stays
	$dot    = true;
	$quoted = false;
	for ( $i = $last - 2; $i >= 0; $i-- ) {
		$text = $parts[ $i ];
		if ( 1 === $i % 2 ) {
			if ( preg_match( $inline, $text ) ) {
				continue;
			}
			if ( ! $quoted && preg_match( '#^<br\b#i', $text ) ) {
				$parts[ $i ] = '';
				continue;
			}
			break;
		}
		$end         = $quoted ? strlen( $text ) : gm_trim_gap( $text, strlen( $text ) );
		$text        = substr( $text, 0, $end );
		$parts[ $i ] = $text;
		for ( $q = gm_quote_before( $text, $end ); $q; $q = gm_quote_before( $text, $end ) ) {
			$end   -= $q;
			$quoted = true;
		}
		if ( $end < 1 ) {
			continue;
		}
		if ( '.' === $text[ $end - 1 ] && ( $end < 2 || '.' !== $text[ $end - 2 ] ) ) {
			$parts[ $i ] = substr( $text, 0, gm_trim_gap( $text, $end - 1 ) ) . substr( $text, $end );
		} elseif ( preg_match( '/(?:[?!.]|\xE2\x80\xA6|&hellip;|&#0*8230;|&#x0*2026;)$/i', substr( $text, max( 0, $end - 12 ), min( $end, 12 ) ) ) ) {
			$dot = false;
		}
		break;
	}
	// then the word, back to the space before it
	$pieces = array();
	for ( $i = $last - 2; $i >= 0; $i-- ) {
		$text = $parts[ $i ];
		if ( 1 === $i % 2 ) {
			// a stray line break after the word is dropped; a line break before it, or any other tag, ends it
			if ( '' === $text || preg_match( $inline, $text ) ) {
				continue;
			}
			if ( ! $pieces && preg_match( '#^<br\b#i', $text ) ) {
				$parts[ $i ] = '';
				continue;
			}
			break;
		}
		$end = strlen( $text );
		if ( ! $pieces ) {
			$end         = gm_trim_gap( $text, $end );
			$text        = substr( $text, 0, $end );
			$parts[ $i ] = $text;
		}
		$start = $end;
		while ( $start > 0 && ! gm_gap_before( $text, $start ) ) {
			--$start;
		}
		if ( $start < $end ) {
			$pieces[] = array( $i, $start, $end );
		}
		// a space ends the word; a word that fills its text goes on before the tag in front of it
		if ( $start > 0 ) {
			break;
		}
	}
	if ( ! $pieces ) {
		return $html;
	}
	// a word split by a tag is gold on both sides; the dot follows its last letter, and the two share a span that does not
	// wrap (.hero h1 .nw), so the dot never goes onto a line of its own
	foreach ( $pieces as $n => $p ) {
		list( $i, $start, $end ) = $p;
		$word = substr( $parts[ $i ], $start, $end - $start );
		if ( 0 === $n && $dot ) {
			$cut  = gm_last_char( $word );
			$word = substr( $word, 0, $cut ) . '<span class="nw">' . substr( $word, $cut ) . '<i class="d pulse" aria-hidden="true"></i></span>';
		}
		$parts[ $i ] = substr( $parts[ $i ], 0, $start ) . '<span class="here">' . $word . '</span>' . substr( $parts[ $i ], $end );
	}
	return implode( '', $parts );
}

/**
 * Where the last character of $text begins: one character with any marks that combine with it, or one entity, together
 * with the closing quote marks after it (core's wptexturize reads a quote mark that starts a text as an opening one).
 *
 * @param string $text The gold word's last piece.
 * @return int Byte offset.
 */
function gm_last_char( $text ) {
	$at = strlen( $text );
	for ( $q = gm_quote_before( $text, $at ); $q && $q < $at; $q = gm_quote_before( $text, $at ) ) {
		$at -= $q;
	}
	if ( preg_match( '/(?:&(?:#[0-9]+|#x[0-9a-f]+|[a-z][a-z0-9]*);|\X)\z/iu', substr( $text, 0, $at ), $m ) ) {
		return $at - strlen( $m[0] );
	}
	// not UTF-8: a byte is a character
	return max( 0, $at - 1 );
}

/**
 * Length of the space, line break or no-break space that ends at byte $at of $text, or 0.
 *
 * @param string $text Text between tags.
 * @param int    $at   Byte offset.
 * @return int
 */
function gm_gap_before( $text, $at ) {
	if ( $at < 1 ) {
		return 0;
	}
	if ( false !== strpos( " \t\n\r\f\v", $text[ $at - 1 ] ) ) {
		return 1;
	}
	foreach ( array( '&nbsp;', '&#160;', "\xC2\xA0" ) as $gap ) {
		$len = strlen( $gap );
		if ( $at >= $len && 0 === substr_compare( $text, $gap, $at - $len, $len, true ) ) {
			return $len;
		}
	}
	return 0;
}

/**
 * Length of the closing quote mark that ends at byte $at of $text, or 0: straight, curly or angled, typed or as an entity.
 *
 * @param string $text Text between tags.
 * @param int    $at   Byte offset.
 * @return int
 */
function gm_quote_before( $text, $at ) {
	if ( $at < 1 ) {
		return 0;
	}
	if ( '"' === $text[ $at - 1 ] || "'" === $text[ $at - 1 ] ) {
		return 1;
	}
	if ( preg_match( '/(?:\xE2\x80[\x98\x99\x9C\x9D\xB9\xBA]|\xC2[\xAB\xBB]|&(?:quot|apos|[lr](?:s?aquo|[sd]quo)|#0*(?:34|39|171|187|8216|8217|8220|8221|8249|8250)|#x0*(?:22|27|ab|bb|2018|2019|201c|201d|2039|203a));)$/i', substr( $text, max( 0, $at - 12 ), min( $at, 12 ) ), $m ) ) {
		return strlen( $m[0] );
	}
	return 0;
}

/**
 * Where $text ends once the spacing before byte $end is left out.
 *
 * @param string $text Text between tags.
 * @param int    $end  Byte offset.
 * @return int
 */
function gm_trim_gap( $text, $end ) {
	for ( $gap = gm_gap_before( $text, $end ); $gap; $gap = gm_gap_before( $text, $end ) ) {
		$end -= $gap;
	}
	return $end;
}

/**
 * The editor draws the dot with CSS (assets/css/editor.css), which cannot read the headline's last character. A headline
 * that ends in a question mark, an exclamation mark or an ellipsis, also inside quote marks, gets the class gm-nodot in the
 * canvas, so the dot is left out there as it is on the page. Spaces and line breaks after the last word are taken out when
 * the headline is left, as the page leaves them out, so the dot follows the word in the canvas too; while the headline is
 * being written they stay, so a next word can follow them.
 */
function gm_editor_here_mark() {
	wp_register_script( 'generation-maine-editor', false, array( 'wp-hooks', 'wp-compose', 'wp-element', 'wp-data', 'wp-rich-text', 'wp-block-editor' ), GM_BUILD_HASH, true );
	wp_enqueue_script( 'generation-maine-editor' );
	wp_add_inline_script(
		'generation-maine-editor',
		'( function ( wp ) {
	var el = wp.element.createElement, rt = wp.richText;
	wp.hooks.addFilter( "editor.BlockListBlock", "generation-maine/here-mark", wp.compose.createHigherOrderComponent( function ( BlockListBlock ) {
		return function ( props ) {
			var a = props.attributes || {};
			var here = "core/heading" === props.name && /(^|\s)gm-here(\s|$)/.test( a.className || "" );
			var was = wp.element.useRef( props.isSelected );
			wp.element.useEffect( function () {
				var left = was.current && ! props.isSelected;
				was.current = props.isSelected;
				if ( ! here || ! left ) {
					return;
				}
				var v = rt.create( { html: String( a.content || "" ) } ), end = v.text.replace( /\s+$/, "" ).length;
				if ( end === v.text.length ) {
					return;
				}
				var html = rt.toHTMLString( { value: rt.slice( v, 0, end ) } ), be = wp.data.dispatch( "core/block-editor" );
				// part of the edit that left them, not a step of its own in Undo
				if ( be.__unstableMarkNextChangeAsNotPersistent ) {
					be.__unstableMarkNextChangeAsNotPersistent();
				}
				props.setAttributes( { content: rt.RichTextData && rt.RichTextData.fromHTMLString ? rt.RichTextData.fromHTMLString( html ) : html } );
			}, [ props.isSelected ] );
			if ( ! here ) {
				return el( BlockListBlock, props );
			}
			// the last visible character, past spaces and closing quote marks
			var text = rt.create( { html: String( a.content || "" ) } ).text.replace( /[\s"\'\u2018\u2019\u201c\u201d\u00ab\u00bb\u2039\u203a]+$/, "" );
			if ( ! /([?!\u2026]|\.\.)$/.test( text ) ) {
				return el( BlockListBlock, props );
			}
			return el( BlockListBlock, Object.assign( {}, props, { className: ( props.className ? props.className + " " : "" ) + "gm-nodot" } ) );
		};
	}, "withHereMark" ) );
} )( window.wp );'
	);
}
add_action( 'enqueue_block_editor_assets', 'gm_editor_here_mark' );

/**
 * Posts and pages get back what a block's own layout settings add, as WordPress prints them when its layout styles are on: a
 * Row's or a Stack's alignment, a Grid's columns, minimum column width and rows. Layout styles are off for the whole theme
 * (gm_setup), because the page's stylesheet lays out every section; the rules here stop at the front page and at a front-page
 * section placed in a post, as the reading styles do. Gaps stay the theme's (build_theme.py WP_ADDITIONS).
 *
 * @param string $html  Block HTML.
 * @param array  $block Block.
 * @return string
 */
function gm_layout_values( $html, $block ) {
	$layout = isset( $block['attrs']['layout'] ) && is_array( $block['attrs']['layout'] ) ? $block['attrs']['layout'] : array();
	$type   = isset( $layout['type'] ) ? $layout['type'] : '';
	if ( ! in_array( $type, array( 'flex', 'grid' ), true ) || ! doing_filter( 'the_content' ) || ! function_exists( 'wp_get_layout_style' ) || ! class_exists( 'WP_HTML_Tag_Processor' ) ) {
		return $html;
	}
	$class = 'gm-layout-' . substr( md5( (string) wp_json_encode( $layout ) ), 0, 10 );
	$css   = wp_get_layout_style( 'main.gm-page .' . $class . ':not(:where(.gm-entry :is(.block,.hero,.stories,.gm-creators) *))', $layout, false, null, false, '0.5em' );
	if ( ! $css ) {
		return $html;
	}
	// the class goes where WordPress puts the layout's own classes, the first element carrying them
	$name = explode( '/', $block['blockName'] );
	$name = 'wp-block-' . ( 'core' === $name[0] ? end( $name ) : implode( '-', $name ) ) . '-is-layout-' . $type;
	$tags = new WP_HTML_Tag_Processor( $html );
	while ( $tags->next_tag() ) {
		if ( $tags->has_class( $name ) ) {
			$tags->add_class( $class );
			return $tags->get_updated_html();
		}
	}
	return $html;
}
add_filter( 'render_block', 'gm_layout_values', 11, 2 );

/**
 * The same values in the post editor, which leaves them out for the same reason: set on the block as WordPress would set them.
 * Templates and front-page sections are left as they are. A block's own size in a row or a grid (Fit, Grow, Fixed, column and
 * row span) shows everywhere, as it does on the page, where WordPress prints it whatever the layout styles.
 */
function gm_editor_layout_values() {
	wp_register_script( 'generation-maine-layout', false, array( 'wp-hooks', 'wp-compose', 'wp-element', 'wp-data' ), GM_BUILD_HASH, true );
	wp_enqueue_script( 'generation-maine-layout' );
	wp_add_inline_script(
		'generation-maine-layout',
		'( function ( wp ) {
	var el = wp.element.createElement;
	var JUSTIFY = { left: "flex-start", right: "flex-end", center: "center", "space-between": "space-between" };
	var ALIGN = { top: "flex-start", center: "center", bottom: "flex-end", stretch: "stretch" };
	var STACK_JUSTIFY = { left: "flex-start", right: "flex-end", center: "center", stretch: "stretch" };
	var STACK_ALIGN = { top: "flex-start", center: "center", bottom: "flex-end", "space-between": "space-between" };
	var SECTION = /(^|\s)(block|hero|stories|gm-creators)(\s|$)/;
	function box( l ) {
		var s = {}, n = l.columnCount, min = l.minimumColumnWidth, fill = l.autoFit ? "auto-fit" : "auto-fill";
		if ( "flex" === l.type ) {
			if ( "nowrap" === l.flexWrap ) { s.flexWrap = "nowrap"; }
			if ( "vertical" === l.orientation ) {
				s.flexDirection = "column";
				s.alignItems = STACK_JUSTIFY[ l.justifyContent ] || "flex-start";
				if ( STACK_ALIGN[ l.verticalAlignment ] ) { s.justifyContent = STACK_ALIGN[ l.verticalAlignment ]; }
			} else {
				if ( JUSTIFY[ l.justifyContent ] ) { s.justifyContent = JUSTIFY[ l.justifyContent ]; }
				if ( ALIGN[ l.verticalAlignment ] ) { s.alignItems = ALIGN[ l.verticalAlignment ]; }
			}
		} else if ( "grid" === l.type ) {
			s.gridTemplateColumns = n && min ? "repeat(" + fill + ", minmax(max(min(" + min + ", 100%), (100% - (0.5em * (" + n + " - 1))) /" + n + "), 1fr))"
				: n ? "repeat(" + n + ", minmax(0, 1fr))" : "repeat(" + fill + ", minmax(min(" + ( min || "12rem" ) + ", 100%), 1fr))";
			if ( n && l.rowCount ) { s.gridTemplateRows = "repeat(" + l.rowCount + ", minmax(1rem, auto))"; }
		}
		return s;
	}
	function child( c ) {
		var s = {};
		if ( ( "fixed" === c.selfStretch || "fixedNoShrink" === c.selfStretch ) && c.flexSize ) {
			s.flexBasis = c.flexSize;
			s.boxSizing = "border-box";
			if ( "fixedNoShrink" === c.selfStretch ) { s.flexShrink = "0"; }
		} else if ( "fill" === c.selfStretch ) {
			s.flexGrow = "1";
		}
		if ( c.columnStart || c.columnSpan ) { s.gridColumn = c.columnStart && c.columnSpan ? c.columnStart + " / span " + c.columnSpan : c.columnStart ? String( c.columnStart ) : "span " + c.columnSpan; }
		if ( c.rowStart || c.rowSpan ) { s.gridRow = c.rowStart && c.rowSpan ? c.rowStart + " / span " + c.rowSpan : c.rowStart ? String( c.rowStart ) : "span " + c.rowSpan; }
		return s;
	}
	wp.hooks.addFilter( "editor.BlockListBlock", "generation-maine/layout-values", wp.compose.createHigherOrderComponent( function ( BlockListBlock ) {
		return function ( props ) {
			var a = props.attributes || {};
			var has = !! ( a.layout && ( "flex" === a.layout.type || "grid" === a.layout.type ) );
			var apply = wp.data.useSelect( function ( select ) {
				var editor = select( "core/editor" ), type = has && editor && editor.getCurrentPostType();
				if ( ! type || /^wp_(template|template_part|navigation)$/.test( type ) ) {
					return false;
				}
				var s = select( "core/block-editor" ), ids = s.getBlockParents( props.clientId, true );
				for ( var i = 0; i < ids.length && "core/post-content" !== s.getBlockName( ids[ i ] ); i++ ) {
					if ( SECTION.test( ( s.getBlockAttributes( ids[ i ] ) || {} ).className || "" ) ) {
						return false;
					}
				}
				return true;
			}, [ has, props.clientId ] );
			var s = Object.assign( apply ? box( a.layout ) : {}, child( ( a.style && a.style.layout ) || {} ) );
			if ( ! Object.keys( s ).length ) {
				return el( BlockListBlock, props );
			}
			var w = props.wrapperProps || {};
			return el( BlockListBlock, Object.assign( {}, props, { wrapperProps: Object.assign( {}, w, { style: Object.assign( {}, w.style, s ) } ) } ) );
		};
	}, "withLayoutValues" ) );
} )( window.wp );'
	);
}
add_action( 'enqueue_block_editor_assets', 'gm_editor_layout_values' );

/**
 * On the front page, a paragraph or heading left empty prints nothing, so staff can take a line off the page (the About
 * section's note, a kicker) by clearing its text. The sections are locked, so the block itself cannot be deleted there.
 *
 * @param string $html  Block HTML.
 * @param array  $block Block.
 * @return string
 */
function gm_drop_empty_text( $html, $block ) {
	if ( ! is_front_page() || ! in_array( $block['blockName'], array( 'core/paragraph', 'core/heading' ), true ) ) {
		return $html;
	}
	return '' === trim( str_replace( '&nbsp;', '', wp_strip_all_tags( $html ) ) ) ? '' : $html;
}
add_filter( 'render_block', 'gm_drop_empty_text', 9, 2 );

/**
 * The about photo loads as on the v2 page: lazily, decoded off the main thread, with its width and height, so the browser
 * fetches it after the first screen instead of next to the fonts. WordPress adds none of these to an image placed straight
 * in a template. A photo picked from the Media Library gets its width and height from WordPress; the theme's own photo
 * gets them here. In a post or a page WordPress decides the loading itself, so there only the size is added.
 *
 * @param string $html  Block HTML.
 * @param array  $block Block.
 * @return string
 */
function gm_about_photo( $html, $block ) {
	$class = isset( $block['attrs']['className'] ) ? ' ' . $block['attrs']['className'] . ' ' : '';
	if ( false === strpos( $class, ' about ' ) || false === stripos( $html, '<img' ) || ! class_exists( 'WP_HTML_Tag_Processor' ) ) {
		return $html;
	}
	// the Home page's content is the front page, where the photo loads after the first screen as on the v2 page
	$in_post = doing_filter( 'the_content' ) && ! is_front_page();
	$tags    = new WP_HTML_Tag_Processor( $html );
	while ( $tags->next_tag( 'img' ) ) {
		if ( null === $tags->get_attribute( 'width' ) && null === $tags->get_attribute( 'height' ) ) {
			$size = gm_theme_image_size( (string) $tags->get_attribute( 'src' ) );
			if ( $size ) {
				$tags->set_attribute( 'width', (string) $size[0] );
				$tags->set_attribute( 'height', (string) $size[1] );
			}
		}
		if ( $in_post || null !== $tags->get_attribute( 'loading' ) || null !== $tags->get_attribute( 'fetchpriority' ) ) {
			continue;
		}
		$tags->set_attribute( 'loading', 'lazy' );
		if ( null === $tags->get_attribute( 'decoding' ) ) {
			$tags->set_attribute( 'decoding', 'async' );
		}
	}
	return $tags->get_updated_html();
}
add_filter( 'render_block_core/group', 'gm_about_photo', 10, 2 );

/**
 * Width and height of an image shipped in the theme, read from the file its address points to.
 *
 * @param string $src Image address.
 * @return array{0:int,1:int}|null
 */
function gm_theme_image_size( $src ) {
	foreach ( array( get_stylesheet_directory_uri() => get_stylesheet_directory(), get_template_directory_uri() => get_template_directory() ) as $uri => $dir ) {
		if ( 0 !== strpos( $src, $uri . '/' ) ) {
			continue;
		}
		$rel  = (string) wp_parse_url( substr( $src, strlen( $uri ) + 1 ), PHP_URL_PATH );
		$file = $dir . '/' . $rel;
		if ( '' === $rel || false !== strpos( $rel, '..' ) || ! is_file( $file ) ) {
			return null;
		}
		$size = wp_getimagesize( $file );
		return $size ? array( (int) $size[0], (int) $size[1] ) : null;
	}
	return null;
}

/**
 * Trim the things a one-page site does not use.
 */
function gm_trim_head() {
	remove_action( 'wp_head', 'print_emoji_detection_script', 7 );
	remove_action( 'wp_print_styles', 'print_emoji_styles' );
	remove_action( 'wp_head', 'wp_generator' );
	remove_action( 'wp_head', 'rsd_link' );
	remove_action( 'wp_head', 'wlwmanifest_link' );
}
add_action( 'init', 'gm_trim_head' );
