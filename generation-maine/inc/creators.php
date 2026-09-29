<?php
/**
 * Creators: a private post type and the [gm_creators] grid.
 *
 * Creators are managed in wp-admin under "Creators" and shown only in the grid on the
 * front page. They have no public profile pages, no archive and no feed.
 *
 * Fields: name (title), portrait (featured image), bio (content), hometown and social links (meta box).
 *
 * @package generation-maine
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

/**
 * Social fields shown on each card, in display order.
 *
 * @return array<string,string> meta key => label
 */
function gm_creator_link_fields() {
	return array(
		'gm_instagram' => 'Instagram',
		'gm_tiktok'    => 'TikTok',
		'gm_youtube'   => 'YouTube',
		'gm_website'   => 'Website',
	);
}

/**
 * Register the post type and its meta.
 */
function gm_register_creators() {
	register_post_type(
		'gm_creator',
		array(
			'labels'              => array(
				'name'               => __( 'Creators', 'generation-maine' ),
				'singular_name'      => __( 'Creator', 'generation-maine' ),
				'add_new_item'       => __( 'Add creator', 'generation-maine' ),
				'edit_item'          => __( 'Edit creator', 'generation-maine' ),
				'new_item'           => __( 'New creator', 'generation-maine' ),
				'search_items'       => __( 'Search creators', 'generation-maine' ),
				'not_found'          => __( 'No creators yet', 'generation-maine' ),
				'featured_image'     => __( 'Portrait', 'generation-maine' ),
				'set_featured_image' => __( 'Set portrait', 'generation-maine' ),
			),
			'public'              => false,
			'publicly_queryable'  => false,
			'exclude_from_search' => true,
			'show_ui'             => true,
			'show_in_menu'        => true,
			'show_in_nav_menus'   => false,
			'show_in_rest'        => true,
			'has_archive'         => false,
			'rewrite'             => false,
			'query_var'           => false,
			'menu_icon'           => 'dashicons-video-alt2',
			'menu_position'       => 5,
			'supports'            => array( 'title', 'editor', 'thumbnail', 'page-attributes', 'custom-fields' ),
			'template'            => array( array( 'core/paragraph', array( 'placeholder' => 'Two or three sentences about this creator, in their own words.' ) ) ),
		)
	);

	$string_meta = array_merge( array( 'gm_hometown' => 'Hometown' ), gm_creator_link_fields() );
	foreach ( array_keys( $string_meta ) as $key ) {
		register_post_meta(
			'gm_creator',
			$key,
			array(
				'type'              => 'string',
				'single'            => true,
				'show_in_rest'      => true,
				'sanitize_callback' => 'gm_hometown' === $key ? 'sanitize_text_field' : 'esc_url_raw',
				'auth_callback'     => static function () {
					return current_user_can( 'edit_posts' );
				},
			)
		);
	}
	register_post_meta(
		'gm_creator',
		'gm_placeholder',
		array(
			'type'          => 'boolean',
			'single'        => true,
			'default'       => false,
			'show_in_rest'  => true,
			'auth_callback' => static function () {
				return current_user_can( 'edit_posts' );
			},
		)
	);
}
add_action( 'init', 'gm_register_creators' );

/**
 * Meta box for hometown, links and the placeholder flag. Works in the block editor with no build step.
 */
function gm_creator_meta_box() {
	add_meta_box( 'gm_creator_details', __( 'Creator details', 'generation-maine' ), 'gm_creator_meta_box_html', 'gm_creator', 'normal', 'high' );
}
add_action( 'add_meta_boxes', 'gm_creator_meta_box' );

/**
 * Meta box markup.
 *
 * @param WP_Post $post Current creator.
 */
function gm_creator_meta_box_html( $post ) {
	wp_nonce_field( 'gm_creator_save', 'gm_creator_nonce' );
	$hometown = get_post_meta( $post->ID, 'gm_hometown', true );
	echo '<p><label for="gm_hometown"><strong>' . esc_html__( 'Hometown', 'generation-maine' ) . '</strong></label><br>';
	echo '<input type="text" class="widefat" id="gm_hometown" name="gm_hometown" value="' . esc_attr( $hometown ) . '" placeholder="Lewiston"></p>';
	foreach ( gm_creator_link_fields() as $key => $label ) {
		$val = get_post_meta( $post->ID, $key, true );
		echo '<p><label for="' . esc_attr( $key ) . '"><strong>' . esc_html( $label ) . ' URL</strong></label><br>';
		echo '<input type="url" class="widefat" id="' . esc_attr( $key ) . '" name="' . esc_attr( $key ) . '" value="' . esc_attr( $val ) . '" placeholder="https://"></p>';
	}
	$ph = (bool) get_post_meta( $post->ID, 'gm_placeholder', true );
	echo '<p><label><input type="checkbox" name="gm_placeholder" value="1" ' . checked( $ph, true, false ) . '> ';
	echo esc_html__( 'This is a placeholder, not a real creator (shows a "Placeholder" label on the site)', 'generation-maine' ) . '</label></p>';
	echo '<p class="description">' . esc_html__( 'Name is the title. Portrait is the featured image (a 4:5 photo works best). Bio is the text above. Use the Order field under Page Attributes to sort.', 'generation-maine' ) . '</p>';
}

/**
 * Save meta box fields.
 *
 * @param int $post_id Post ID.
 */
function gm_creator_save( $post_id ) {
	if ( ! isset( $_POST['gm_creator_nonce'] ) || ! wp_verify_nonce( sanitize_text_field( wp_unslash( $_POST['gm_creator_nonce'] ) ), 'gm_creator_save' ) ) {
		return;
	}
	if ( defined( 'DOING_AUTOSAVE' ) && DOING_AUTOSAVE ) {
		return;
	}
	if ( ! current_user_can( 'edit_post', $post_id ) ) {
		return;
	}
	if ( isset( $_POST['gm_hometown'] ) ) {
		update_post_meta( $post_id, 'gm_hometown', sanitize_text_field( wp_unslash( $_POST['gm_hometown'] ) ) );
	}
	foreach ( array_keys( gm_creator_link_fields() ) as $key ) {
		if ( isset( $_POST[ $key ] ) ) {
			update_post_meta( $post_id, $key, esc_url_raw( wp_unslash( $_POST[ $key ] ) ) );
		}
	}
	update_post_meta( $post_id, 'gm_placeholder', ! empty( $_POST['gm_placeholder'] ) );
}
add_action( 'save_post_gm_creator', 'gm_creator_save' );

/**
 * Initials for a creator with no portrait.
 *
 * @param string $name Full name.
 * @return string
 */
function gm_initials( $name ) {
	$parts    = preg_split( '/\s+/', trim( wp_strip_all_tags( $name ) ) );
	$initials = '';
	foreach ( array_slice( (array) $parts, 0, 2 ) as $p ) {
		$initials .= function_exists( 'mb_substr' ) ? mb_substr( $p, 0, 1 ) : substr( $p, 0, 1 );
	}
	return strtoupper( $initials );
}

/**
 * Render the creators grid, or the "coming soon" state when there are none.
 *
 * @param array $args Optional. 'limit' (int).
 * @return string HTML.
 */
function gm_render_creators( $args = array() ) {
	$limit = isset( $args['limit'] ) ? max( 1, (int) $args['limit'] ) : 24;
	$query = new WP_Query(
		array(
			'post_type'              => 'gm_creator',
			'post_status'            => 'publish',
			'posts_per_page'         => $limit,
			'orderby'                => array(
				'menu_order' => 'ASC',
				'title'      => 'ASC',
			),
			'no_found_rows'          => true,
			'update_post_term_cache' => false,
		)
	);

	if ( ! $query->have_posts() ) {
		$html  = '<div class="gm-coming-soon">';
		$html .= '<h3>' . esc_html__( 'Creators coming soon', 'generation-maine' ) . '</h3>';
		$html .= '<p>' . esc_html__( 'We are choosing 8 to 12 young creators from across Maine. Their profiles will appear here.', 'generation-maine' ) . '</p>';
		$html .= '<div class="gm-slots" aria-hidden="true">' . str_repeat( '<span></span>', 6 ) . '</div>';
		$html .= '</div>';
		return $html;
	}

	$html = '<ul class="gm-creators">';
	$i    = 0;
	while ( $query->have_posts() ) {
		$query->the_post();
		$id          = get_the_ID();
		$name        = get_the_title();
		$town        = get_post_meta( $id, 'gm_hometown', true );
		$placeholder = (bool) get_post_meta( $id, 'gm_placeholder', true );
		$bio         = wp_trim_words( wp_strip_all_tags( get_the_content() ), 60 );

		$html .= '<li class="gm-creator' . ( $placeholder ? ' gm-creator--placeholder' : '' ) . '">';
		if ( has_post_thumbnail( $id ) ) {
			$html .= '<div class="gm-creator__photo">' . get_the_post_thumbnail(
				$id,
				'medium_large',
				array(
					'alt'      => $name,
					'loading'  => $i < 4 ? 'eager' : 'lazy',
					'decoding' => 'async',
					'sizes'    => '(min-width: 1200px) 280px, (min-width: 600px) 45vw, 100vw',
				)
			) . '</div>';
		} else {
			$html .= '<div class="gm-creator__photo gm-creator__photo--empty"><span class="gm-creator__initials" aria-hidden="true">' . esc_html( gm_initials( $name ) ) . '</span></div>';
		}
		$html .= '<div class="gm-creator__body">';
		if ( $placeholder ) {
			$html .= '<span class="gm-badge">' . esc_html__( 'Placeholder', 'generation-maine' ) . '</span>';
		}
		$html .= '<h3 class="gm-creator__name">' . esc_html( $name ) . '</h3>';
		if ( $town ) {
			$html .= '<p class="gm-creator__town">' . esc_html( $town ) . '</p>';
		}
		if ( $bio ) {
			$html .= '<p class="gm-creator__bio">' . esc_html( $bio ) . '</p>';
		}
		$links = '';
		foreach ( gm_creator_link_fields() as $key => $label ) {
			$url = get_post_meta( $id, $key, true );
			if ( $url ) {
				$links .= sprintf(
					'<li><a href="%1$s" rel="noopener" target="_blank">%2$s<span class="screen-reader-text"> %3$s</span></a></li>',
					esc_url( $url ),
					esc_html( $label ),
					/* translators: %s: creator name. */
					esc_html( sprintf( __( 'for %s (opens in a new tab)', 'generation-maine' ), $name ) )
				);
			}
		}
		if ( $links ) {
			$html .= '<ul class="gm-creator__links">' . $links . '</ul>';
		}
		$html .= '</div></li>';
		++$i;
	}
	wp_reset_postdata();
	$html .= '</ul>';
	return $html;
}

/**
 * [gm_creators limit="24"]
 *
 * @param array $atts Shortcode attributes.
 * @return string
 */
function gm_creators_shortcode( $atts ) {
	$atts = shortcode_atts( array( 'limit' => 24 ), $atts, 'gm_creators' );
	return gm_render_creators( $atts );
}
add_shortcode( 'gm_creators', 'gm_creators_shortcode' );

/**
 * Register the server-rendered Creators Grid block (no build step).
 */
function gm_register_creators_block() {
	register_block_type( get_theme_file_path( 'blocks/creators' ) );
}
add_action( 'init', 'gm_register_creators_block' );
