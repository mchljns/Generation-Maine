<?php
/**
 * Creators: a private post type and the stepper that shows them.
 *
 * Everything about a creator lives on the Creator post, under "Creators" in the dashboard:
 *   name (title), bio (content), avatar (featured image), handle, hometown, clip (a video upload or a link),
 *   clip length, and Instagram, TikTok and YouTube links. The Creators block renders the pinned clip with the
 *   creator's avatar and handle on it, their details beside it, and the position row under both.
 *
 * Creators have no public pages, archive or feed. They appear only where the block is placed.
 *
 * @package generation-maine
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

/**
 * Social fields shown with each creator, in display order.
 *
 * @return array<string,string> meta key => label
 */
function gm_creator_link_fields() {
	return array(
		'gm_instagram' => 'Instagram',
		'gm_tiktok'    => 'TikTok',
		'gm_youtube'   => 'YouTube',
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
				'featured_image'     => __( 'Avatar (square photo, shown in a circle)', 'generation-maine' ),
				'set_featured_image' => __( 'Set avatar', 'generation-maine' ),
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
			'template'            => array( array( 'core/paragraph', array( 'placeholder' => __( 'Two or three sentences in your own words: who you are, what you do, how long you have lived here.', 'generation-maine' ) ) ) ),
		)
	);

	$fields = array(
		'gm_handle'   => 'sanitize_text_field',
		'gm_hometown' => 'sanitize_text_field',
		'gm_clip_url' => 'esc_url_raw',
		'gm_clip_len' => 'sanitize_text_field',
	);
	foreach ( array_keys( gm_creator_link_fields() ) as $key ) {
		$fields[ $key ] = 'esc_url_raw';
	}
	foreach ( $fields as $key => $sanitize ) {
		register_post_meta(
			'gm_creator',
			$key,
			array(
				'type'              => 'string',
				'single'            => true,
				'show_in_rest'      => true,
				'sanitize_callback' => $sanitize,
				'auth_callback'     => static function () {
					return current_user_can( 'edit_posts' );
				},
			)
		);
	}
	register_post_meta(
		'gm_creator',
		'gm_clip_id',
		array(
			'type'              => 'integer',
			'single'            => true,
			'show_in_rest'      => true,
			'sanitize_callback' => 'absint',
			'auth_callback'     => static function () {
				return current_user_can( 'edit_posts' );
			},
		)
	);
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
 * The details box on the Creator screen.
 */
function gm_creator_meta_box() {
	add_meta_box( 'gm_creator_details', __( 'Creator details', 'generation-maine' ), 'gm_creator_meta_box_html', 'gm_creator', 'normal', 'high' );
}
add_action( 'add_meta_boxes', 'gm_creator_meta_box' );

/**
 * One text or url field in the box.
 *
 * @param int    $post_id Post.
 * @param string $key     Meta key.
 * @param string $label   Label.
 * @param string $help    Help text.
 * @param string $type    Input type.
 * @param string $ph      Placeholder.
 */
function gm_creator_field( $post_id, $key, $label, $help, $type = 'text', $ph = '' ) {
	$val = get_post_meta( $post_id, $key, true );
	printf(
		'<p><label for="%1$s"><strong>%2$s</strong></label><br><input type="%3$s" class="widefat" id="%1$s" name="%1$s" value="%4$s" placeholder="%5$s">%6$s</p>',
		esc_attr( $key ),
		esc_html( $label ),
		esc_attr( $type ),
		esc_attr( $val ),
		esc_attr( $ph ),
		$help ? '<span class="description">' . esc_html( $help ) . '</span>' : ''
	);
}

/**
 * The box.
 *
 * @param WP_Post $post Current creator.
 */
function gm_creator_meta_box_html( $post ) {
	wp_nonce_field( 'gm_creator_save', 'gm_creator_nonce' );
	echo '<p class="description">' . esc_html__( 'The name is the title above. The bio is the text in the editor. The avatar is the featured image on the right: a square photo, shown in a circle on the clip.', 'generation-maine' ) . '</p>';
	gm_creator_field( $post->ID, 'gm_handle', __( 'Handle', 'generation-maine' ), __( 'As it appears on their feed, with the @.', 'generation-maine' ), 'text', '@handle' );
	gm_creator_field( $post->ID, 'gm_hometown', __( 'Hometown', 'generation-maine' ), __( 'Town only. "Maine" is added on the page.', 'generation-maine' ), 'text', 'Skowhegan' );

	$clip_id  = (int) get_post_meta( $post->ID, 'gm_clip_id', true );
	$clip_url = $clip_id ? wp_get_attachment_url( $clip_id ) : '';
	echo '<p><strong>' . esc_html__( 'Clip', 'generation-maine' ) . '</strong><br>';
	echo '<span class="description">' . esc_html__( 'A short vertical video (9:16), muted, that loops. Keep it under 10 MB and about ten seconds. Upload one, or paste a direct link to an .mp4 or .webm below.', 'generation-maine' ) . '</span></p>';
	echo '<p><input type="hidden" id="gm_clip_id" name="gm_clip_id" value="' . esc_attr( $clip_id ) . '">';
	echo '<button type="button" class="button" id="gm_clip_pick">' . esc_html__( 'Choose or upload a clip', 'generation-maine' ) . '</button> ';
	echo '<button type="button" class="button-link" id="gm_clip_clear"' . ( $clip_id ? '' : ' hidden' ) . '>' . esc_html__( 'Remove', 'generation-maine' ) . '</button> ';
	echo '<span id="gm_clip_name" class="description">' . ( $clip_url ? esc_html( wp_basename( $clip_url ) ) : '' ) . '</span></p>';
	gm_creator_field( $post->ID, 'gm_clip_url', __( 'Or a clip link', 'generation-maine' ), __( 'Used only when no clip is uploaded.', 'generation-maine' ), 'url', 'https://' );
	gm_creator_field( $post->ID, 'gm_clip_len', __( 'Clip length', 'generation-maine' ), __( 'Shown on the clip, for example 0:52. Leave empty to hide it.', 'generation-maine' ), 'text', '0:52' );

	foreach ( gm_creator_link_fields() as $key => $label ) {
		gm_creator_field( $post->ID, $key, $label, '', 'url', 'https://' );
	}
	$ph = (bool) get_post_meta( $post->ID, 'gm_placeholder', true );
	echo '<p><label><input type="checkbox" name="gm_placeholder" value="1" ' . checked( $ph, true, false ) . '> ';
	echo esc_html__( 'Placeholder, not a real creator yet', 'generation-maine' ) . '</label></p>';
	echo '<p class="description">' . esc_html__( 'Order: use the Order field under Page Attributes. Lower numbers come first.', 'generation-maine' ) . '</p>';
	?>
	<script>
	(function(){var pick=document.getElementById('gm_clip_pick'),clr=document.getElementById('gm_clip_clear'),id=document.getElementById('gm_clip_id'),nm=document.getElementById('gm_clip_name');if(!pick||!window.wp||!wp.media){return;}
	var frame;pick.addEventListener('click',function(){if(!frame){frame=wp.media({title:'Choose a clip',library:{type:'video'},multiple:false,button:{text:'Use this clip'}});frame.on('select',function(){var a=frame.state().get('selection').first().toJSON();id.value=a.id;nm.textContent=a.filename||a.url;clr.hidden=false;});}frame.open();});
	clr.addEventListener('click',function(){id.value='';nm.textContent='';clr.hidden=true;});})();
	</script>
	<?php
}

/**
 * Save the box.
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
	foreach ( array( 'gm_handle', 'gm_hometown', 'gm_clip_len' ) as $key ) {
		if ( isset( $_POST[ $key ] ) ) {
			update_post_meta( $post_id, $key, sanitize_text_field( wp_unslash( $_POST[ $key ] ) ) );
		}
	}
	foreach ( array_merge( array( 'gm_clip_url' ), array_keys( gm_creator_link_fields() ) ) as $key ) {
		if ( isset( $_POST[ $key ] ) ) {
			update_post_meta( $post_id, $key, esc_url_raw( wp_unslash( $_POST[ $key ] ) ) );
		}
	}
	if ( isset( $_POST['gm_clip_id'] ) ) {
		update_post_meta( $post_id, 'gm_clip_id', absint( $_POST['gm_clip_id'] ) );
	}
	update_post_meta( $post_id, 'gm_placeholder', ! empty( $_POST['gm_placeholder'] ) );
}
add_action( 'save_post_gm_creator', 'gm_creator_save' );

/**
 * Let the editor upload video (WordPress allows mp4 and webm by default; this makes sure).
 *
 * @param array $mimes Allowed types.
 * @return array
 */
function gm_allow_video( $mimes ) {
	$mimes['mp4']  = 'video/mp4';
	$mimes['webm'] = 'video/webm';
	return $mimes;
}
add_filter( 'upload_mimes', 'gm_allow_video' );

/**
 * Published creators in order, as plain arrays the block can render.
 *
 * @param int $limit Most to return.
 * @return array<int,array<string,mixed>>
 */
function gm_get_creators( $limit = 24 ) {
	$query = new WP_Query(
		array(
			'post_type'              => 'gm_creator',
			'post_status'            => 'publish',
			'posts_per_page'         => max( 1, (int) $limit ),
			'orderby'                => array(
				'menu_order' => 'ASC',
				'title'      => 'ASC',
			),
			'no_found_rows'          => true,
			'update_post_term_cache' => false,
		)
	);
	$out = array();
	while ( $query->have_posts() ) {
		$query->the_post();
		$id      = get_the_ID();
		$clip_id = (int) get_post_meta( $id, 'gm_clip_id', true );
		$clip    = $clip_id ? wp_get_attachment_url( $clip_id ) : get_post_meta( $id, 'gm_clip_url', true );
		$links   = array();
		foreach ( gm_creator_link_fields() as $key => $label ) {
			$url = get_post_meta( $id, $key, true );
			if ( $url ) {
				$links[ str_replace( 'gm_', '', $key ) ] = array( 'label' => $label, 'url' => $url );
			}
		}
		$out[] = array(
			'id'          => $id,
			'name'        => get_the_title(),
			'handle'      => get_post_meta( $id, 'gm_handle', true ),
			'town'        => get_post_meta( $id, 'gm_hometown', true ),
			'bio'         => wp_strip_all_tags( get_the_content() ),
			'clip'        => $clip ? $clip : '',
			'len'         => get_post_meta( $id, 'gm_clip_len', true ),
			'avatar'      => has_post_thumbnail( $id ) ? get_the_post_thumbnail_url( $id, 'thumbnail' ) : '',
			'links'       => $links,
			'placeholder' => (bool) get_post_meta( $id, 'gm_placeholder', true ),
		);
	}
	wp_reset_postdata();
	return $out;
}

/**
 * The social header that sits on the clip: avatar, handle, name.
 *
 * @param array $c Creator.
 * @param bool  $on Current.
 * @return string
 */
function gm_who( $c, $on ) {
	$av = $c['avatar'] ? '<img class="av" src="' . esc_url( $c['avatar'] ) . '" alt="" width="36" height="36" loading="lazy">' : gm_avatar_placeholder();
	return '<div class="who' . ( $on ? ' on' : '' ) . '">' . $av . '<span><b>' . esc_html( $c['handle'] ? $c['handle'] : $c['name'] ) . '</b>' . esc_html( $c['name'] ) . '</span></div>';
}

/**
 * Render the creators section: the pinned clip, the details that step with the scroll, and the position row.
 * With no creators it shows a short empty state. The markup matches the splash mockup so the shared CSS and script apply.
 *
 * @param array $args Optional. 'limit' (int), 'next' (string), 'last' (string).
 * @return string HTML
 */
/**
 * The roster: one tile per creator. A creator marked placeholder shows the numeral and the town only, no face and no link,
 * so the page can launch before the shoot. A creator with the placeholder unchecked shows the avatar, name, town and handle,
 * and the tile links to the first of their feeds. Nothing is hosted here; every tile is a door to where the clips live.
 *
 * @param array $creators From gm_get_creators().
 * @return string HTML
 */
function gm_render_roster( $creators ) {
	$out = '<div class="roster-grid">';
	foreach ( $creators as $i => $c ) {
		$n     = sprintf( '%02d', $i + 1 );
		$town  = $c['town'] ? $c['town'] : __( 'Maine', 'generation-maine' );
		$ready = ! $c['placeholder'] && ( $c['avatar'] || $c['handle'] );
		if ( ! $ready ) {
			$out .= '<div class="roster-tile" aria-label="' . esc_attr( sprintf( /* translators: 1: position, 2: town */ __( 'Creator %1$s, %2$s, Maine', 'generation-maine' ), $n, $town ) ) . '">'
				. '<span class="n">' . esc_html( $n ) . '</span><b>' . esc_html( $town ) . '</b></div>';
			continue;
		}
		$href  = '';
		foreach ( $c['links'] as $l ) {
			$href = $l['url'];
			break;
		}
		$av    = $c['avatar'] ? '<img class="av" src="' . esc_url( $c['avatar'] ) . '" alt="" width="56" height="56" loading="lazy">' : '';
		$inner = '<span class="n">' . esc_html( $n ) . '</span>' . $av . '<b>' . esc_html( $c['name'] ) . '</b><span class="town">' . esc_html( $town ) . '</span>'
			. ( $c['handle'] ? '<span class="h">' . esc_html( $c['handle'] ) . '</span>' : '' );
		$out  .= $href
			? '<a class="roster-tile ready" href="' . esc_url( $href ) . '" target="_blank" rel="noopener">' . $inner . '</a>'
			: '<div class="roster-tile ready">' . $inner . '</div>';
	}
	return $out . '</div>';
}

function gm_render_creators( $args = array() ) {
	$layout   = isset( $args['layout'] ) && 'stepper' === $args['layout'] ? 'stepper' : 'roster';
	$limit    = isset( $args['limit'] ) ? (int) $args['limit'] : 24;
	$next     = isset( $args['next'] ) && '' !== $args['next'] ? $args['next'] : __( 'Next: ', 'generation-maine' );
	$last     = isset( $args['last'] ) && '' !== $args['last'] ? $args['last'] : __( 'Last one', 'generation-maine' );
	$creators = gm_get_creators( $limit );
	if ( ! $creators ) {
		return '<section class="stories gm-empty" data-bg="var(--bi)"><div class="w"><p>' . esc_html__( 'The creators are being cast. Their clips and stories will appear here.', 'generation-maine' ) .
			( current_user_can( 'edit_posts' ) ? ' <a href="' . esc_url( admin_url( 'post-new.php?post_type=gm_creator' ) ) . '">' . esc_html__( 'Add the first creator.', 'generation-maine' ) . '</a>' : '' ) . '</p></div></section>';
	}
	if ( 'roster' === $layout ) {
		return '<section class="roster" data-bg="var(--sand)"><div class="w">' . gm_render_roster( $creators ) . '</div></section>';
	}
	$n = count( $creators );
	$vids = $whos = $panels = $segs = '';
	foreach ( $creators as $i => $c ) {
		$on = 0 === $i;
		if ( $c['clip'] && preg_match( '/\.(gif|png|jpe?g|webp)(\?|$)/i', $c['clip'] ) ) {
			$vids .= sprintf( '<img class="clip%1$s" data-i="%2$d" data-dur="%3$s" src="%4$s" alt="" loading="%5$s">', $on ? ' on' : '', $i, esc_attr( $c['len'] ), esc_url( $c['clip'] ), $i < 2 ? 'eager' : 'lazy' );
		} elseif ( $c['clip'] ) {
			$vids .= sprintf(
				'<video data-i="%1$d" data-dur="%2$s" src="%3$s" muted loop playsinline preload="%4$s" aria-label="%5$s"%6$s></video>',
				$i,
				esc_attr( $c['len'] ),
				esc_url( $c['clip'] ),
				$i < 2 ? 'auto' : 'metadata',
				/* translators: 1: creator name, 2: town */
				esc_attr( sprintf( __( 'Clip by %1$s, %2$s, Maine', 'generation-maine' ), $c['name'], $c['town'] ) ),
				$on ? ' class="on"' : ''
			);
		} else {
			$vids .= '<div class="noclip' . ( $on ? ' on' : '' ) . '" data-i="' . $i . '" data-dur=""></div>';
		}
		$whos .= gm_who( $c, $on );
		$segs .= sprintf( '<button type="button" aria-label="%1$s" data-name="%2$s"%3$s></button>', esc_attr( sprintf( '%d, %s', $i + 1, $c['name'] ) ), esc_attr( $c['name'] ), $on ? ' class="on"' : '' );
		$soc   = '';
		foreach ( $c['links'] as $key => $l ) {
			$soc .= '<a href="' . esc_url( $l['url'] ) . '" target="_blank" rel="noopener" aria-label="' . esc_attr( $l['label'] ) . '">' . gm_mark( $key ) . '<span>' . esc_html( $c['handle'] ? $c['handle'] : $l['label'] ) . '</span></a>';
		}
		$panels .= '<article class="panel' . ( $on ? ' on' : '' ) . '" id="creator-' . (int) $c['id'] . '" data-i="' . $i . '">';
		if ( $c['town'] ) {
			$panels .= '<p class="k">' . esc_html( $c['town'] ) . ', Maine<i class="d pulse"></i></p>';
		}
		$panels .= '<h2>' . esc_html( $c['name'] ) . '</h2>';
		if ( $c['bio'] ) {
			$panels .= '<p class="bio">' . esc_html( $c['bio'] ) . '</p>';
		}
		if ( $soc ) {
			$panels .= '<div class="soc">' . $soc . '</div>';
		}
		$panels .= '</article>';
	}
	$first_len = $creators[0]['len'];
	return '<section class="stories" id="stories" data-bg="var(--bi)" style="--n:' . (int) $n . '"><div class="pinw"><div class="w">'
		. '<div class="stage"><div class="vid" id="stage">' . $vids . $whos . '<span class="dur" id="dur"' . ( $first_len ? '' : ' hidden' ) . '>' . esc_html( $first_len ) . '</span></div></div>'
		. '<div class="panels" id="panels">' . $panels . '</div>'
		. '<div class="where" id="where"><span class="n" id="wn">01 / ' . esc_html( str_pad( (string) $n, 2, '0', STR_PAD_LEFT ) ) . '</span><span class="segs" id="segs">' . $segs . '</span>'
		. '<span class="next" id="wnext" data-next="' . esc_attr( $next ) . '" data-last="' . esc_attr( $last ) . '"></span></div>'
		. '</div></div></section>';
}

/**
 * [gm_creators limit="24"]
 *
 * @param array $atts Shortcode attributes.
 * @return string
 */
function gm_creators_shortcode( $atts ) {
	$atts = shortcode_atts( array( 'limit' => 24, 'layout' => 'roster' ), $atts, 'gm_creators' );
	return gm_render_creators( $atts );
}
add_shortcode( 'gm_creators', 'gm_creators_shortcode' );

/**
 * The block.
 */
function gm_register_creators_block() {
	register_block_type( get_theme_file_path( 'blocks/creators' ) );
}
add_action( 'init', 'gm_register_creators_block' );
