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
 * The hero mural's data, read by the page script.
 */
function gm_mural_data() {
	$file = get_theme_file_path( 'assets/data/mural.json' );
	if ( ! file_exists( $file ) ) {
		return;
	}
	echo '<script id="maine-data" type="application/json">' . file_get_contents( $file ) . '</script>' . "\n"; // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped, WordPressVIPMinimum.Performance.FetchingRemoteData.FileGetContentsUnknown
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
 * break or no-break space, and inside bold, emphasis or a link. A final period becomes the dot, inside or outside the tag;
 * a question mark or an exclamation mark stays and gets no dot. The markup is walked tag by tag from the end instead of
 * matched with one pattern, so no length of spacing can make it fail; anything it cannot read is shown unchanged.
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
	$dot    = true;
	$read   = false;
	$pieces = array();
	for ( $i = $last - 2; $i >= 0; $i-- ) {
		$text = $parts[ $i ];
		if ( 1 === $i % 2 ) {
			// bold, emphasis and links can sit inside the word or around it; a stray line break after the word is dropped;
			// a line break before it, or any other tag, ends it
			if ( preg_match( '#^</?(?:strong|b|em|i|a|span|mark|u|s|code)\b#i', $text ) ) {
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
			$end = gm_trim_gap( $text, $end );
			if ( ! $read && $end > 0 ) {
				$read = true;
				if ( '.' === $text[ $end - 1 ] ) {
					$end = gm_trim_gap( $text, $end - 1 );
				} elseif ( '?' === $text[ $end - 1 ] || '!' === $text[ $end - 1 ] ) {
					$dot = false;
				}
			}
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
	// a word split by a tag is gold on both sides; the dot follows its last letter
	foreach ( $pieces as $n => $p ) {
		list( $i, $start, $end ) = $p;
		$parts[ $i ] = substr( $parts[ $i ], 0, $start ) . '<span class="here">' . substr( $parts[ $i ], $start, $end - $start )
			. ( 0 === $n && $dot ? '<i class="d pulse" aria-hidden="true"></i>' : '' ) . '</span>' . substr( $parts[ $i ], $end );
	}
	return implode( '', $parts );
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
 * that ends in a question mark or an exclamation mark gets the class gm-nodot in the canvas, so the dot is left out there
 * as it is on the page.
 */
function gm_editor_here_mark() {
	wp_register_script( 'generation-maine-editor', false, array( 'wp-hooks', 'wp-compose', 'wp-element' ), GM_BUILD_HASH, true );
	wp_enqueue_script( 'generation-maine-editor' );
	wp_add_inline_script(
		'generation-maine-editor',
		'( function ( wp ) {
	var el = wp.element.createElement;
	wp.hooks.addFilter( "editor.BlockListBlock", "generation-maine/here-mark", wp.compose.createHigherOrderComponent( function ( BlockListBlock ) {
		return function ( props ) {
			var a = props.attributes || {};
			if ( "core/heading" !== props.name || ! /(^|\s)gm-here(\s|$)/.test( a.className || "" ) ) {
				return el( BlockListBlock, props );
			}
			var text = String( a.content || "" ).replace( /<[^>]*>/g, "" ).replace( /&nbsp;|&#160;/g, " " ).trim();
			if ( ! /[?!]$/.test( text ) ) {
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
	$in_post = doing_filter( 'the_content' );
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
