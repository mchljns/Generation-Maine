<?php
/**
 * The home page: a normal page called Home, under Pages, edited in the page editor like any other page.
 *
 * templates/front-page.html prints the content of the page set as the homepage under Settings > Reading. When the theme is
 * activated on a site still showing its latest posts, it makes the Home page from the page's sections (the hero, About, the
 * creators heading and block, Follow and the newsletter), puts the about photo in the Media Library and sets the page as the
 * homepage. On a site where the theme is already active, a notice in the dashboard offers the same with one click.
 *
 * Until a page is set as the homepage, the front page shows the same sections straight from the theme's patterns, so the
 * site never shows an empty front page.
 *
 * @package generation-maine
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

/**
 * The sections of the home page, in order: pattern files in patterns/.
 *
 * @return string[]
 */
function gm_home_sections() {
	return array( 'hero', 'about', 'creators', 'follow' );
}

/**
 * The block markup of the home page's sections, read from the pattern files.
 *
 * @return string
 */
function gm_home_markup() {
	$out = array();
	foreach ( gm_home_sections() as $slug ) {
		$file = get_theme_file_path( 'patterns/' . $slug . '.php' );
		if ( ! is_file( $file ) ) {
			continue;
		}
		ob_start();
		include $file;
		$out[] = trim( (string) ob_get_clean() );
	}
	return implode( "\n\n", $out );
}

/**
 * True when a page is set as the homepage under Settings > Reading.
 *
 * @return bool
 */
function gm_home_is_set() {
	return 'page' === get_option( 'show_on_front' ) && (int) get_option( 'page_on_front' ) && get_post( (int) get_option( 'page_on_front' ) );
}

/**
 * Copy the theme's about photo into the Media Library, so the Home page uses an image the editor can see, crop and replace,
 * and a move to another host carries it along with the rest of the uploads.
 *
 * @return int Attachment ID, or 0 if it could not be copied.
 */
function gm_home_import_photo() {
	$src = get_theme_file_path( 'assets/img/about.jpg' );
	if ( ! is_file( $src ) ) {
		return 0;
	}
	$bits = wp_upload_bits( 'generation-maine-about.jpg', null, (string) file_get_contents( $src ) ); // phpcs:ignore WordPress.WP.AlternativeFunctions.file_get_contents_file_get_contents
	if ( ! empty( $bits['error'] ) ) {
		return 0;
	}
	$id = wp_insert_attachment(
		array(
			'post_mime_type' => 'image/jpeg',
			'post_title'     => __( 'Lisbon Street, Lewiston, Maine', 'generation-maine' ),
			'post_status'    => 'inherit',
		),
		$bits['file'],
		0,
		true
	);
	if ( is_wp_error( $id ) ) {
		return 0;
	}
	require_once ABSPATH . 'wp-admin/includes/image.php';
	wp_update_attachment_metadata( $id, wp_generate_attachment_metadata( $id, $bits['file'] ) );
	update_post_meta( $id, '_wp_attachment_image_alt', __( 'Lisbon Street, Lewiston, Maine', 'generation-maine' ) );
	return (int) $id;
}

/**
 * Make the Home page and set it as the homepage. Does nothing when the page the theme made before still exists.
 *
 * @return int Page ID, or 0 on failure.
 */
function gm_home_create() {
	$id = (int) get_option( 'gm_home_page' );
	if ( ! $id || ! get_post( $id ) || 'trash' === get_post_status( $id ) ) {
		$markup = gm_home_markup();
		$photo  = gm_home_import_photo();
		if ( $photo ) {
			$url    = (string) wp_get_attachment_url( $photo );
			$markup = str_replace( '<!-- wp:image {"sizeSlug":"full"', '<!-- wp:image {"id":' . $photo . ',"sizeSlug":"full"', $markup );
			$markup = preg_replace( '#<img src="' . preg_quote( esc_url( get_theme_file_uri( 'assets/img/about.jpg' ) ), '#' ) . '" alt="([^"]*)"/>#', '<img src="' . esc_url( $url ) . '" alt="$1" class="wp-image-' . $photo . '"/>', $markup );
		}
		$id = wp_insert_post(
			array(
				'post_type'      => 'page',
				'post_status'    => 'publish',
				'post_title'     => __( 'Home', 'generation-maine' ),
				'post_name'      => 'home',
				'post_content'   => wp_slash( $markup ),
				'comment_status' => 'closed',
				'ping_status'    => 'closed',
			),
			true
		);
		if ( is_wp_error( $id ) ) {
			return 0;
		}
		update_option( 'gm_home_page', (int) $id, false );
	}
	update_option( 'show_on_front', 'page' );
	update_option( 'page_on_front', (int) $id );
	return (int) $id;
}

/**
 * On activation, make the Home page when the site still shows its latest posts. A site that already has a homepage keeps it.
 */
function gm_home_on_activate() {
	if ( ! gm_home_is_set() ) {
		gm_home_create();
	}
}
add_action( 'after_switch_theme', 'gm_home_on_activate' );

/**
 * Until a page is set as the homepage, the front page's content block shows the sections from the theme's patterns.
 *
 * @param string|null $pre    Output to use instead, or null.
 * @param array       $parsed The block about to render.
 * @return string|null
 */
function gm_home_fallback( $pre, $parsed ) {
	if ( null !== $pre || 'core/post-content' !== $parsed['blockName'] || empty( $parsed['attrs']['gmHome'] ) || ! is_front_page() || gm_home_is_set() ) {
		return $pre;
	}
	return do_blocks( gm_home_markup() );
}
add_filter( 'pre_render_block', 'gm_home_fallback', 10, 2 );

/**
 * A notice for admins on a site where the homepage is not a page yet, with a button that makes the Home page.
 */
function gm_home_notice() {
	if ( ! current_user_can( 'manage_options' ) || gm_home_is_set() ) {
		return;
	}
	$url = wp_nonce_url( admin_url( 'admin-post.php?action=gm_home_create' ), 'gm_home_create' );
	echo '<div class="notice notice-info"><p><strong>' . esc_html__( 'Generation Maine:', 'generation-maine' ) . '</strong> '
		. esc_html__( 'Make a Home page under Pages to edit the front page in the page editor. It starts with the page\'s sections and becomes the homepage under Settings > Reading.', 'generation-maine' )
		. '</p><p><a class="button button-primary" href="' . esc_url( $url ) . '">' . esc_html__( 'Make the Home page', 'generation-maine' ) . '</a></p></div>';
}
add_action( 'admin_notices', 'gm_home_notice' );

/**
 * The notice's button.
 */
function gm_home_create_action() {
	if ( ! current_user_can( 'manage_options' ) ) {
		wp_die( esc_html__( 'Sorry, you are not allowed to do that.', 'generation-maine' ) );
	}
	check_admin_referer( 'gm_home_create' );
	$id = gm_home_create();
	wp_safe_redirect( $id ? admin_url( 'post.php?post=' . $id . '&action=edit' ) : admin_url() );
	exit;
}
add_action( 'admin_post_gm_home_create', 'gm_home_create_action' );

/**
 * Mark the Home page in the Pages list, as WordPress marks the privacy page.
 *
 * @param string[] $states States.
 * @param WP_Post  $post   Page.
 * @return string[]
 */
function gm_home_state( $states, $post ) {
	if ( (int) get_option( 'page_on_front' ) === $post->ID && 'page' === get_option( 'show_on_front' ) ) {
		$states['gm_home'] = __( 'Edit the front page here', 'generation-maine' );
	}
	return $states;
}
add_filter( 'display_post_states', 'gm_home_state', 10, 2 );
