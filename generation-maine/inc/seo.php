<?php
/**
 * Lightweight SEO for a one-page site: title, description, canonical, Open Graph,
 * and Organization schema with Maine Policy Institute as the parent organization.
 *
 * Steps aside automatically if Yoast SEO, Rank Math, SEOPress or All in One SEO is active.
 *
 * @package generation-maine
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

/**
 * Site-wide SEO values. Change them here or with the 'gm_seo' filter.
 *
 * @return array
 */
function gm_seo() {
	$same_as = array();
	foreach ( gm_channels() as $c ) {
		if ( $c['url'] ) {
			$same_as[] = $c['url'];
		}
	}
	$name  = get_bloginfo( 'name' ) ? get_bloginfo( 'name' ) : 'Generation Maine';
	$title = trim( gm_setting( 'gm_seo_title' ) );
	$desc  = trim( gm_setting( 'gm_seo_description' ) );
	$image = trim( gm_setting( 'gm_seo_image' ) );
	return apply_filters(
		'gm_seo',
		array(
			'name'        => $name,
			'title'       => '' !== $title ? $title : $name . ': young Mainers on the rules that shape their lives',
			'description' => '' !== $desc ? $desc : 'Young Mainers film the rules that shape their lives. Short videos on TikTok, Instagram and YouTube, and the full story by email. A Maine Policy Institute project.',
			'image'       => '' !== $image ? $image : get_theme_file_uri( 'assets/img/share-card.jpg' ),
			'image_alt'   => 'Generation Maine',
			'parent_name' => 'Maine Policy Institute',
			'parent_url'  => 'https://mainepolicy.org/',
			'same_as'     => $same_as,
		)
	);
}

/**
 * True when a dedicated SEO plugin is handling meta tags.
 *
 * @return bool
 */
function gm_seo_plugin_active() {
	return defined( 'WPSEO_VERSION' ) || defined( 'RANK_MATH_VERSION' ) || defined( 'SEOPRESS_VERSION' ) || defined( 'AIOSEO_VERSION' );
}

/**
 * True on the front page. With a static front page, the posts page is a page of its own, not the front page.
 *
 * @return bool
 */
function gm_seo_is_front() {
	return is_front_page() || ( is_home() && ! get_option( 'page_for_posts' ) );
}

/**
 * Front page title. A value returned here skips WordPress's own escaping, so it is escaped here.
 *
 * @param string $title Title WordPress would use.
 * @return string
 */
function gm_document_title( $title ) {
	if ( gm_seo_plugin_active() || ! gm_seo_is_front() ) {
		return $title;
	}
	return esc_html( gm_seo()['title'] );
}
add_filter( 'pre_get_document_title', 'gm_document_title' );

/**
 * Meta description, canonical, Open Graph, Twitter card and JSON-LD.
 */
function gm_seo_head() {
	if ( gm_seo_plugin_active() ) {
		return;
	}
	$s     = gm_seo();
	$url   = home_url( '/' );
	$front = gm_seo_is_front();
	$title = $front ? $s['title'] : wp_get_document_title();

	if ( $front ) {
		printf( '<meta name="description" content="%s">' . "\n", esc_attr( $s['description'] ) );
		if ( ! is_singular() ) {
			printf( '<link rel="canonical" href="%s">' . "\n", esc_url( $url ) );
		}
	}

	$tags = array(
		'og:type'        => is_singular( 'post' ) ? 'article' : 'website',
		'og:site_name'   => $s['name'],
		'og:locale'      => str_replace( '-', '_', get_bloginfo( 'language' ) ),
		'og:title'       => $title,
		'og:description' => $s['description'],
		// a page with its own address names it; an archive or a search names none rather than the first post in it
		'og:url'         => $front ? $url : ( is_singular() ? get_permalink() : '' ),
		'og:image'       => $s['image'],
		'og:image:width' => '1200',
		'og:image:height' => '630',
		'og:image:alt'   => $s['image_alt'],
	);
	foreach ( $tags as $prop => $content ) {
		if ( $content ) {
			printf( '<meta property="%s" content="%s">' . "\n", esc_attr( $prop ), esc_attr( $content ) );
		}
	}
	echo '<meta name="twitter:card" content="summary_large_image">' . "\n";

	if ( $front ) {
		// JSON is not HTML: the Site Title is stored with & and ' as entities, so they are decoded (JSON_HEX_TAG keeps it safe)
		$text   = static function ( $v ) {
			return html_entity_decode( (string) $v, ENT_QUOTES, 'UTF-8' );
		};
		$schema = array(
			'@context'           => 'https://schema.org',
			'@type'              => 'Organization',
			'name'               => $text( $s['name'] ),
			'url'                => $url,
			'logo'               => has_site_icon() ? get_site_icon_url( 512 ) : get_theme_file_uri( 'assets/img/icon-192.png' ),
			'description'        => $text( $s['description'] ),
			'parentOrganization' => array(
				'@type' => 'Organization',
				'name'  => $text( $s['parent_name'] ),
				'url'   => $s['parent_url'],
			),
		);
		if ( ! empty( $s['same_as'] ) ) {
			$schema['sameAs'] = array_values( $s['same_as'] );
		}
		echo '<script type="application/ld+json">' . wp_json_encode( $schema, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE | JSON_HEX_TAG ) . '</script>' . "\n";
	}
}
add_action( 'wp_head', 'gm_seo_head', 2 );
