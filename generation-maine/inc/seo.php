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
	return apply_filters(
		'gm_seo',
		array(
			'title'       => 'Generation Maine | Young Mainers on building a life here',
			'description' => 'Short videos by young Maine creators about housing, jobs and staying in Maine. An initiative of Maine Policy Institute.',
			'image'       => get_theme_file_uri( 'assets/img/share-card.jpg' ),
			'image_alt'   => 'Generation Maine. Young Mainers on building a life here. An initiative of Maine Policy Institute.',
			'parent_name' => 'Maine Policy Institute',
			'parent_url'  => 'https://mainepolicy.org/', // [CONFIRM: Maine Policy Institute URL].
			'same_as'     => array(), // Add channel URLs once handles exist, e.g. 'https://www.instagram.com/HANDLE/'.
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
 * Front page title.
 *
 * @param string $title Title WordPress would use.
 * @return string
 */
function gm_document_title( $title ) {
	if ( gm_seo_plugin_active() || ! ( is_front_page() || is_home() ) ) {
		return $title;
	}
	return gm_seo()['title'];
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
	$front = is_front_page() || is_home();
	$title = $front ? $s['title'] : wp_get_document_title();

	if ( $front ) {
		printf( '<meta name="description" content="%s">' . "\n", esc_attr( $s['description'] ) );
		if ( ! is_singular() ) {
			printf( '<link rel="canonical" href="%s">' . "\n", esc_url( $url ) );
		}
	}

	$tags = array(
		'og:type'        => 'website',
		'og:site_name'   => 'Generation Maine',
		'og:locale'      => str_replace( '-', '_', get_bloginfo( 'language' ) ),
		'og:title'       => $title,
		'og:description' => $s['description'],
		'og:url'         => $front ? $url : get_permalink(),
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
		$schema = array(
			'@context'           => 'https://schema.org',
			'@type'              => 'Organization',
			'name'               => 'Generation Maine',
			'url'                => $url,
			'logo'               => get_theme_file_uri( 'assets/img/icon-192.png' ),
			'description'        => $s['description'],
			'parentOrganization' => array(
				'@type' => 'Organization',
				'name'  => $s['parent_name'],
				'url'   => $s['parent_url'],
			),
		);
		if ( ! empty( $s['same_as'] ) ) {
			$schema['sameAs'] = array_values( $s['same_as'] );
		}
		echo '<script type="application/ld+json">' . wp_json_encode( $schema, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE ) . '</script>' . "\n";
	}
}
add_action( 'wp_head', 'gm_seo_head', 2 );
