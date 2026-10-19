<?php
/**
 * Creators: a private post type, and the stepper and roster that show them.
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
		'gm_handle'   => 'gm_sanitize_handle',
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
		'gm_on_home',
		array(
			'type'          => 'boolean',
			'single'        => true,
			'default'       => true,
			'show_in_rest'  => true,
			'auth_callback' => static function () {
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
 * Creators have no public pages, so owning one does not make an account public. Through the REST API WordPress shows
 * visitors every account with published content of any type the API serves, creators included. For anyone who cannot edit
 * other people's creators, the users list leaves creators out of that test; authors of posts and pages are listed as before.
 *
 * @param array $args WP_User_Query arguments of the users route.
 * @return array
 */
function gm_creator_rest_users( $args ) {
	if ( empty( $args['has_published_posts'] ) || current_user_can( 'edit_others_posts' ) ) {
		return $args;
	}
	$types = true === $args['has_published_posts'] ? get_post_types( array( 'show_in_rest' => true ), 'names' ) : (array) $args['has_published_posts'];
	$types = array_values( array_diff( $types, array( 'gm_creator' ) ) );
	if ( $types ) {
		$args['has_published_posts'] = $types;
	} else {
		$args['include'] = array( 0 ); // only creators were asked for: list nobody
	}
	return $args;
}
add_filter( 'rest_user_query', 'gm_creator_rest_users' );

/**
 * The same test for one account, /wp/v2/users/<id>, which WordPress checks on its own. It goes by the handler WordPress
 * matched, not the address as typed: WordPress matches routes in any letter case (/WP/V2/Users/2), answers HEAD with the
 * GET handler, and reads the account from an id in the query string ahead of the one in the address, as this test does.
 *
 * @param mixed           $response Result so far; null to go on.
 * @param array           $handler  Route handler.
 * @param WP_REST_Request $request  Request.
 * @return mixed
 */
function gm_creator_rest_user( $response, $handler, $request ) {
	$cb = isset( $handler['callback'] ) ? $handler['callback'] : null;
	if ( null !== $response || ! is_array( $cb ) || ! isset( $cb[0], $cb[1] ) || ! ( $cb[0] instanceof WP_REST_Users_Controller ) || 'get_item' !== $cb[1] ) {
		return $response;
	}
	$id    = (int) $request['id'];
	$types = array_diff( get_post_types( array( 'show_in_rest' => true ), 'names' ), array( 'gm_creator' ) );
	if ( get_user_by( 'id', $id ) && get_current_user_id() !== $id && ! current_user_can( 'edit_others_posts' ) && ! current_user_can( 'edit_user', $id ) && ! count_user_posts( $id, $types ) ) {
		return new WP_Error( 'rest_user_cannot_view', __( 'Sorry, you are not allowed to list users.', 'generation-maine' ), array( 'status' => rest_authorization_required_code() ) );
	}
	return $response;
}
add_filter( 'rest_request_before_callbacks', 'gm_creator_rest_user', 10, 3 );

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
	// a chosen clip that was deleted from the Media Library counts as none, so the box offers the link and the next save clears it
	if ( ! $clip_url ) {
		$clip_id = 0;
	}
	// people who cannot upload (Contributors) get the link field only: the library would be empty and an upload would fail
	$can_upload = current_user_can( 'upload_files' );
	echo '<p><strong>' . esc_html__( 'Clip', 'generation-maine' ) . '</strong><br>';
	echo '<span class="description">' . ( $can_upload
		? esc_html__( 'A short vertical video (9:16) or GIF, muted, that loops. Keep it under 10 MB and about ten seconds. Choose or upload one, or paste a direct link to an .mp4, .webm or .gif below.', 'generation-maine' )
		: esc_html__( 'A short vertical video (9:16) or GIF, muted, that loops. Keep it under 10 MB and about ten seconds. Paste a direct link to an .mp4, .webm or .gif below.', 'generation-maine' ) ) . '</span></p>';
	// the size is known for a chosen clip and for a link to a file in this site's Media Library, with or without a query string
	// after it; a link elsewhere is not checked. The link's own warning rides along, for the picker script to show when the
	// chosen clip is removed and the link is still the one saved.
	$link      = (string) get_post_meta( $post->ID, 'gm_clip_url', true );
	$link_id   = $link ? attachment_url_to_postid( (string) preg_replace( '/[?#].*$/', '', $link ) ) : 0;
	$link_size = $link_id ? (int) @filesize( get_attached_file( $link_id ) ) : 0; // phpcs:ignore WordPress.PHP.NoSilencedErrors.Discouraged
	$size      = $clip_id ? (int) @filesize( get_attached_file( $clip_id ) ) : $link_size; // phpcs:ignore WordPress.PHP.NoSilencedErrors.Discouraged
	/* translators: %s: file size */
	$warn = __( 'This clip is %s. Visitors download all of it, so a clip under 10 MB loads much faster on a phone.', 'generation-maine' );
	echo '<p id="gm_clip_big" class="notice notice-warning inline"' . ( $size > 10 * MB_IN_BYTES ? '' : ' hidden' )
		. ' data-link="' . esc_attr( $link_size > 10 * MB_IN_BYTES ? sprintf( $warn, size_format( $link_size, 1 ) ) : '' ) . '"><span>' . esc_html( sprintf( $warn, size_format( $size, 1 ) ) ) . '</span></p>';
	echo '<p><input type="hidden" id="gm_clip_id" name="gm_clip_id" value="' . esc_attr( $clip_id ) . '">';
	echo $can_upload
		? '<button type="button" class="button" id="gm_clip_pick">' . esc_html__( 'Choose or upload a clip', 'generation-maine' ) . '</button> '
		: '<span id="gm_clip_noupload" class="description">' . esc_html__( 'Your account cannot upload files. An editor can upload the clip for you.', 'generation-maine' ) . '</span> ';
	echo '<button type="button" class="button-link" id="gm_clip_clear"' . ( $clip_id ? '' : ' hidden' ) . '>' . esc_html__( 'Remove', 'generation-maine' ) . '</button> ';
	echo '<span id="gm_clip_name" class="description">' . ( $clip_url ? esc_html( wp_basename( $clip_url ) ) : '' ) . '</span></p>';
	gm_creator_field( $post->ID, 'gm_clip_url', __( 'Or a clip link', 'generation-maine' ), __( 'Used only when no clip is chosen above. Remove the chosen clip to use a link.', 'generation-maine' ), 'url', 'https://' );
	gm_creator_field( $post->ID, 'gm_clip_len', __( 'Clip length', 'generation-maine' ), __( 'Shown on the clip, for example 0:52. Leave empty to hide it.', 'generation-maine' ), 'text', '0:52' );

	foreach ( gm_creator_link_fields() as $key => $label ) {
		gm_creator_field( $post->ID, $key, $label, '', 'url', 'https://' );
	}
	$on = (bool) get_post_meta( $post->ID, 'gm_on_home', true );
	echo '<p><label><input type="checkbox" name="gm_on_home" value="1" ' . checked( $on, true, false ) . '> <strong>';
	echo esc_html__( 'Show on the home page', 'generation-maine' ) . '</strong></label><br><span class="description">';
	echo esc_html__( 'Untick to take the creator off the page and keep the post for later. Creators never get a page of their own, so search engines cannot list them.', 'generation-maine' ) . '</span></p>';
	$ph = (bool) get_post_meta( $post->ID, 'gm_placeholder', true );
	echo '<p><label><input type="checkbox" name="gm_placeholder" value="1" ' . checked( $ph, true, false ) . '> ';
	echo esc_html__( 'Placeholder, not a real creator yet', 'generation-maine' ) . '</label></p>';
	echo '<p><label for="gm_order"><strong>' . esc_html__( 'Place on the page', 'generation-maine' ) . '</strong></label><br>';
	echo '<input type="number" id="gm_order" name="gm_order" value="' . esc_attr( (int) $post->menu_order ) . '" step="1" style="width:6em"> ';
	echo '<input type="hidden" name="gm_order_was" value="' . esc_attr( (int) $post->menu_order ) . '">';
	echo '<span class="description">' . esc_html__( 'Lower numbers come first. Creators with the same number are in alphabetical order.', 'generation-maine' ) . '</span></p>';
}

/**
 * The block editor saves this box in a second request, and for a post type with no Author panel that request carries no
 * author, so WordPress would make whoever saved the creator its author. Send the current author along, as Quick Edit does.
 *
 * @param WP_Post $post Post being edited.
 */
function gm_creator_keep_author( $post ) {
	if ( 'gm_creator' === $post->post_type ) {
		echo '<input type="hidden" name="post_author" value="' . esc_attr( (int) $post->post_author ) . '">';
	}
}
add_action( 'block_editor_meta_box_hidden_fields', 'gm_creator_keep_author' );

/**
 * The clip picker on the Creator screen. It needs the media library, which loads after the box is printed, so it runs from
 * an enqueued script and listens on the document.
 *
 * @param string $hook Admin page.
 */
function gm_creator_admin_assets( $hook ) {
	$screen = get_current_screen();
	if ( ! $screen || 'gm_creator' !== $screen->post_type || ! in_array( $hook, array( 'post.php', 'post-new.php' ), true ) ) {
		return;
	}
	wp_enqueue_media();
	// with no clip chosen, the warning follows the link: it shows only while the link is the one the box opened with and that
	// one is over 10 MB; a changed link is checked when the creator is opened again
	$limit = 10 * MB_IN_BYTES;
	$js    = "(function(){var frame;function el(i){return document.getElementById(i);}
function link(){var b=el('gm_clip_big'),u=el('gm_clip_url');if(!b||el('gm_clip_id').value!=='0'){return;}var m=b.getAttribute('data-link')||'',on=!!m&&!!u&&u.value.trim()===u.defaultValue.trim();b.hidden=!on;if(on){b.querySelector('span').textContent=m;}}
document.addEventListener('input',function(e){if(e.target.id==='gm_clip_url'){link();}});
document.addEventListener('click',function(e){
 if(e.target.closest('#gm_clip_pick')){e.preventDefault();if(!window.wp||!wp.media){return;}
  if(!frame){frame=wp.media({title:" . wp_json_encode( __( 'Choose a clip', 'generation-maine' ) ) . ",library:{type:['video','image/gif']},multiple:false,button:{text:" . wp_json_encode( __( 'Use this clip', 'generation-maine' ) ) . "}});
   frame.on('select',function(){var a=frame.state().get('selection').first().toJSON();el('gm_clip_id').value=a.id;el('gm_clip_name').textContent=a.filename||a.url;el('gm_clip_clear').hidden=false;var b=el('gm_clip_big');if(b){var big=(a.filesizeInBytes||0)>" . (int) $limit . ";b.hidden=!big;if(big){b.querySelector('span').textContent=" . wp_json_encode( __( 'This clip is larger than 10 MB. Visitors download all of it, so a smaller clip loads much faster on a phone.', 'generation-maine' ) ) . ";}}});}
  frame.open();}
 if(e.target.closest('#gm_clip_clear')){e.preventDefault();el('gm_clip_id').value='0';el('gm_clip_name').textContent='';el('gm_clip_clear').hidden=true;var b=el('gm_clip_big');if(b){b.hidden=true;}link();}
});})();";
	wp_add_inline_script( 'media-editor', $js );
}
add_action( 'admin_enqueue_scripts', 'gm_creator_admin_assets' );

/**
 * In the block editor the place on the page is the post's own Order. The box's field shows it and changes it in the editor,
 * which saves it with the post, so the field, WordPress's Order control and Quick Edit always agree; the box no longer sends
 * it. On WordPress 7 the Meta Boxes drawer also opens at part of the window, not the full height of Creator details, so the
 * title stays in view until the person drags the drawer to a height of their own. The box's other fields are saved by its own
 * request, which the editor sends only when it knows the post has changed. So a field changed there (a clip chosen or removed
 * too) is passed to the editor as the post's meta: Ctrl+S then saves it, and leaving the editor warns, as for the title. It is
 * kept out of the editor's Undo, which could change only the editor's copy and never the box. The box's fields have the
 * browser's own Ctrl+Z instead, as WordPress 7 gives every meta box (on 6.5 the editor took those keys), and the editor then
 * gets the undone value like any other change.
 */
function gm_creator_editor_assets() {
	$screen = get_current_screen();
	if ( ! $screen || 'gm_creator' !== $screen->post_type ) {
		return;
	}
	wp_register_script( 'gm-creator-editor', false, array( 'wp-data', 'wp-dom-ready', 'wp-editor', 'wp-preferences' ), null, true ); // phpcs:ignore WordPress.WP.EnqueuedResourceParameters.MissingVersion
	wp_enqueue_script( 'gm-creator-editor' );
	wp_add_inline_script(
		'gm-creator-editor',
		"(function(d){d.dispatch('core/preferences').setDefaults('core/edit-post',{metaBoxesMainOpenHeight:Math.max(240,Math.round(window.innerHeight*.4))});
wp.domReady(function(){var f=document.getElementById('gm_order'),was=document.querySelector('input[name=\"gm_order_was\"]'),ed=function(){return d.select('core/editor');},last;if(!f){return;}
 f.removeAttribute('name');if(was){was.removeAttribute('name');}
 f.addEventListener('input',function(){d.dispatch('core/editor').editPost({menu_order:parseInt(f.value,10)||0});});
 f.addEventListener('change',function(){f.value=ed().getEditedPostAttribute('menu_order');});
 d.subscribe(function(){var v=ed().getEditedPostAttribute('menu_order');if(v===last||undefined===v){return;}last=v;if(document.activeElement!==f){f.value=v;}});
 var box=document.getElementById('gm_creator_details'),told={},val=function(i){return 'checkbox'===i.type?i.checked:('gm_clip_id'===i.name?parseInt(i.value,10)||0:i.value);};
 var sync=function(){var m=ed().getEditedPostAttribute('meta'),e={},n=0;if(!m){return;}
  box.querySelectorAll('input[name]').forEach(function(i){var k=i.name,v=val(i);if(k in m&&v!==told[k]){e[k]=told[k]=v;n++;}});
  if(n){d.dispatch('core/editor').editPost({meta:e},{undoIgnore:true});}};
 if(!box){return;}box.querySelectorAll('input[name]').forEach(function(i){told[i.name]=val(i);});
 box.addEventListener('keydown',function(e){if((e.ctrlKey||e.metaKey)&&/^[yz]$/i.test(e.key)){e.stopPropagation();}});
 box.addEventListener('input',sync);box.addEventListener('change',sync);document.addEventListener('click',function(){setTimeout(sync,0);});
});})(wp.data);"
	);
}
add_action( 'enqueue_block_editor_assets', 'gm_creator_editor_assets' );

/**
 * Save the place on the page from the box, only when it was changed there. This is for the classic editor, whose page
 * reloads after each save; the block editor saves the place with the post (see gm_creator_editor_assets()).
 *
 * @param array $data    Post data about to be saved.
 * @param array $postarr Raw post data.
 * @return array
 */
function gm_creator_order( $data, $postarr ) {
	if ( 'gm_creator' !== $data['post_type'] || ! isset( $_POST['gm_order'], $_POST['gm_order_was'], $_POST['gm_creator_nonce'] ) ) {
		return $data;
	}
	if ( ! wp_verify_nonce( sanitize_text_field( wp_unslash( $_POST['gm_creator_nonce'] ) ), 'gm_creator_save' ) || empty( $postarr['ID'] ) || ! current_user_can( 'edit_post', (int) $postarr['ID'] ) ) {
		return $data;
	}
	$order = (int) $_POST['gm_order'];
	if ( (int) $_POST['gm_order_was'] !== $order ) {
		$data['menu_order'] = $order;
	}
	return $data;
}
add_filter( 'wp_insert_post_data', 'gm_creator_order', 10, 2 );

/**
 * The Creators list shows what is on the page and in what order.
 *
 * @param array $cols Columns.
 * @return array
 */
function gm_creator_columns( $cols ) {
	$out = array();
	foreach ( $cols as $key => $label ) {
		if ( 'date' === $key ) {
			$out['gm_on_home']     = __( 'On the page', 'generation-maine' );
			$out['gm_order']       = __( 'Place', 'generation-maine' );
			$out['gm_hometown']    = __( 'Hometown', 'generation-maine' );
			$out['gm_placeholder'] = __( 'Placeholder', 'generation-maine' );
		}
		$out[ $key ] = $label;
	}
	return $out;
}
add_filter( 'manage_gm_creator_posts_columns', 'gm_creator_columns' );

/**
 * Column values.
 *
 * @param string $col     Column.
 * @param int    $post_id Creator.
 */
function gm_creator_column( $col, $post_id ) {
	if ( 'gm_on_home' === $col ) {
		echo get_post_meta( $post_id, 'gm_on_home', true ) ? esc_html__( 'Yes', 'generation-maine' ) : esc_html__( 'Hidden', 'generation-maine' );
	} elseif ( 'gm_order' === $col ) {
		echo (int) get_post_field( 'menu_order', $post_id );
	} elseif ( 'gm_hometown' === $col ) {
		echo esc_html( get_post_meta( $post_id, 'gm_hometown', true ) );
	} elseif ( 'gm_placeholder' === $col ) {
		echo get_post_meta( $post_id, 'gm_placeholder', true ) ? esc_html__( 'Yes', 'generation-maine' ) : '';
	}
}
add_action( 'manage_gm_creator_posts_custom_column', 'gm_creator_column', 10, 2 );

/**
 * The list opens in page order.
 *
 * @param WP_Query $q Query.
 */
function gm_creator_list_order( $q ) {
	if ( is_admin() && $q->is_main_query() && 'gm_creator' === $q->get( 'post_type' ) && ! $q->get( 'orderby' ) ) {
		$q->set( 'orderby', array( 'menu_order' => 'ASC', 'title' => 'ASC' ) );
	}
}
add_action( 'pre_get_posts', 'gm_creator_list_order' );

/**
 * Bulk actions on the Creators list: show the ticked creators on the home page, or take them off it.
 *
 * @param array $actions Actions.
 * @return array
 */
function gm_creator_bulk_actions( $actions ) {
	$actions['gm_show'] = __( 'Show on the home page', 'generation-maine' );
	$actions['gm_hide'] = __( 'Take off the home page', 'generation-maine' );
	return $actions;
}
add_filter( 'bulk_actions-edit-gm_creator', 'gm_creator_bulk_actions' );

/**
 * Run a bulk action.
 *
 * @param string $to     Where to go after.
 * @param string $action Action.
 * @param int[]  $ids    Creators.
 * @return string
 */
function gm_creator_bulk_run( $to, $action, $ids ) {
	if ( ! in_array( $action, array( 'gm_show', 'gm_hide' ), true ) ) {
		return $to;
	}
	$n = 0;
	foreach ( $ids as $id ) {
		if ( current_user_can( 'edit_post', (int) $id ) ) {
			update_post_meta( (int) $id, 'gm_on_home', 'gm_show' === $action );
			++$n;
		}
	}
	return add_query_arg( 'gm_bulk', $n, $to );
}
add_filter( 'handle_bulk_actions-edit-gm_creator', 'gm_creator_bulk_run', 10, 3 );

/**
 * The note after a bulk action.
 */
function gm_creator_bulk_notice() {
	if ( ! isset( $_GET['gm_bulk'] ) || 'edit-gm_creator' !== get_current_screen()->id ) { // phpcs:ignore WordPress.Security.NonceVerification.Recommended
		return;
	}
	$n = absint( $_GET['gm_bulk'] ); // phpcs:ignore WordPress.Security.NonceVerification.Recommended
	/* translators: %d: number of creators */
	echo '<div class="notice notice-success is-dismissible"><p>' . esc_html( sprintf( _n( '%d creator updated.', '%d creators updated.', $n, 'generation-maine' ), $n ) ) . '</p></div>';
}
add_action( 'admin_notices', 'gm_creator_bulk_notice' );

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
	if ( isset( $_POST['gm_handle'] ) ) {
		update_post_meta( $post_id, 'gm_handle', gm_sanitize_handle( wp_unslash( $_POST['gm_handle'] ) ) ); // phpcs:ignore WordPress.Security.ValidatedSanitizedInput.InputNotSanitized -- gm_sanitize_handle() runs sanitize_text_field()
	}
	foreach ( array( 'gm_hometown', 'gm_clip_len' ) as $key ) {
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
	update_post_meta( $post_id, 'gm_on_home', ! empty( $_POST['gm_on_home'] ) );
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
			// a creator saved before the switch existed has no value yet, and shows, as the switch's default says
			'meta_query'             => array( // phpcs:ignore WordPress.DB.SlowDBQuery.slow_db_query_meta_query
				'relation' => 'OR',
				array(
					'key'     => 'gm_on_home',
					'compare' => 'NOT EXISTS',
				),
				array(
					'key'   => 'gm_on_home',
					'value' => '1',
				),
			),
			'no_found_rows'          => true,
			'update_post_term_cache' => false,
		)
	);
	// every avatar and clip file in one query, not a few queries per creator
	$files = array();
	foreach ( $query->posts as $creator ) {
		$files[] = (int) get_post_thumbnail_id( $creator );
		$files[] = (int) get_post_meta( $creator->ID, 'gm_clip_id', true );
	}
	_prime_post_caches( array_filter( $files ), false, true );
	$out = array();
	while ( $query->have_posts() ) {
		$query->the_post();
		$id      = get_the_ID();
		$thumb   = (int) get_post_thumbnail_id( $id );
		$clip_id = (int) get_post_meta( $id, 'gm_clip_id', true );
		$clip    = $clip_id ? wp_get_attachment_url( $clip_id ) : '';
		// a chosen clip that was deleted from the Media Library counts as none, so the clip link is used
		if ( ! $clip ) {
			$clip = get_post_meta( $id, 'gm_clip_url', true );
		}
		$links = array();
		foreach ( gm_creator_link_fields() as $key => $label ) {
			$url = get_post_meta( $id, $key, true );
			if ( $url ) {
				$links[ str_replace( 'gm_', '', $key ) ] = array( 'label' => $label, 'url' => $url );
			}
		}
		$out[] = array(
			'id'          => $id,
			// the title as typed: get_the_title() has been through the typography filter, which turns the x of 4x4 into a times sign
			'name'        => get_post_field( 'post_title', $id, 'raw' ),
			// cleaned again here, so a handle saved before the rules for spaces and a lone @ shows as a new save would keep it
			'handle'      => gm_sanitize_handle( get_post_meta( $id, 'gm_handle', true ) ),
			'town'        => get_post_meta( $id, 'gm_hometown', true ),
			// line breaks and paragraph ends become spaces, so words on either side do not run together
			'bio'         => trim( preg_replace( '/\s+/', ' ', wp_strip_all_tags( preg_replace( '#<br\s*/?>|</p>|</li>|</h[1-6]>#i', ' ', get_the_content() ) ) ) ),
			'clip'        => $clip ? $clip : '',
			'len'         => get_post_meta( $id, 'gm_clip_len', true ),
			'avatar'      => $thumb ? (string) wp_get_attachment_image_url( $thumb, 'thumbnail' ) : '',
			'portrait'    => $thumb ? (string) wp_get_attachment_image_url( $thumb, 'medium' ) : '',
			// the still a paused clip shows: the smallest size at least 1120 px tall, sharp at 2x on the largest place it is
			// shown (the desktop stage, 315 by 560), or the original when no size is that tall
			'still'       => $thumb ? (string) wp_get_attachment_image_url( $thumb, array( 0, 1120 ) ) : '',
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
 * @param array $c     Creator.
 * @param bool  $on    Current.
 * @param bool  $defer Leave the avatar to the page script, which loads it as the creator's turn nears (the stage stacks one
 *                     header per creator and shows only the current one, so the browser would load them all at once).
 * @return string
 */
function gm_who( $c, $on, $defer = false ) {
	$av = $c['avatar'] ? '<img class="av" ' . ( $defer ? 'data-src' : 'src' ) . '="' . esc_url( $c['avatar'] ) . '" alt="" width="36" height="36" loading="lazy">' : gm_avatar_placeholder();
	// the handle on top and the name under it; with no handle, or a name that is the handle, one line
	$same  = $c['handle'] && strtolower( ltrim( trim( $c['handle'] ), '@' ) ) === strtolower( ltrim( trim( html_entity_decode( $c['name'], ENT_QUOTES, 'UTF-8' ) ), '@' ) );
	$lines = $c['handle'] && ! $same ? '<b>' . gm_bdi( $c['handle'] ) . '</b>' . gm_bdi( $c['name'] ) : '<b>' . gm_bdi( $c['handle'] ? $c['handle'] : $c['name'] ) . '</b>';
	return '<div class="who' . ( $on ? ' on' : '' ) . '">' . $av . '<span>' . $lines . '</span></div>';
}

/**
 * The still for a creator with no avatar: the placeholder figure on a navy frame, so a paused clip never shows an empty image.
 *
 * @return string URL
 */
function gm_still_placeholder() {
	return get_theme_file_uri( 'blocks/creators/still.svg' );
}

/**
 * One clip element. Images and videos both carry data-src and load when their card is current or next door;
 * a creator with no clip gets a plain navy field.
 *
 * @param array  $c       Creator.
 * @param string $class   Extra classes.
 * @param string $attrs   Extra attributes.
 * @param string $alt     Accessible name for the clip.
 * @return string
 */
function gm_clip( $c, $class, $attrs, $alt ) {
	$cls = trim( 'clip ' . $class );
	if ( ! $c['clip'] ) {
		return '<div class="' . esc_attr( $cls . ' noclip' ) . '"' . $attrs . '></div>';
	}
	// a still for when the clips are paused: the creator's portrait, or the placeholder figure, never an empty image
	$still = $c['still'] ? $c['still'] : gm_still_placeholder();
	// the editor's preview has no page script to load clips, so it shows the portrait (or the clip) straight away
	if ( defined( 'REST_REQUEST' ) && REST_REQUEST ) {
		$attrs .= ' src="' . esc_url( $c['portrait'] ? $c['portrait'] : $c['clip'] ) . '"';
	}
	if ( preg_match( '/\.(gif|png|jpe?g|webp|avif)(\?|$)/i', $c['clip'] ) ) {
		return '<img class="' . esc_attr( $cls ) . '"' . $attrs . ' data-src="' . esc_url( $c['clip'] ) . '" data-still="' . esc_url( $still ) . '" alt="' . esc_attr( $alt ) . '">';
	}
	if ( defined( 'REST_REQUEST' ) && REST_REQUEST && $c['portrait'] ) {
		return '<img class="' . esc_attr( $cls ) . '"' . $attrs . ' alt="' . esc_attr( $alt ) . '">';
	}
	// a browser loads every poster at once, so the poster is the small portrait; the page script swaps in the sharp still
	// when the clip itself loads
	return '<video class="' . esc_attr( $cls ) . '"' . $attrs . ' data-src="' . esc_url( $c['clip'] ) . '" poster="' . esc_url( $c['portrait'] ? $c['portrait'] : $still ) . '" data-still="' . esc_url( $still ) . '" muted loop playsinline preload="none" aria-label="' . esc_attr( $alt ) . '"></video>';
}

/**
 * The roster: one tile per creator, the face above the name and town. A tile links to the creator's first feed once they
 * are no longer a placeholder; until then it is a plain block. Nothing is hosted here.
 *
 * @param array $creators From gm_get_creators().
 * @return string HTML
 */
function gm_render_roster( $creators ) {
	$out = '';
	foreach ( $creators as $i => $c ) {
		/* translators: %s: town */
		$place = $c['town'] ? sprintf( __( '%s, Maine', 'generation-maine' ), $c['town'] ) : __( 'Maine', 'generation-maine' );
		$inner = '<span class="ph">' . ( $c['portrait'] ? '<img src="' . esc_url( $c['portrait'] ) . '" alt="" width="300" height="400" loading="lazy">' : '' ) . '</span>'
			. '<span class="who"><span class="n">' . esc_html( sprintf( '%02d', $i + 1 ) ) . '</span><b>' . gm_bdi( $c['name'] ) . '</b><span class="town">' . esc_html( $place ) . '</span></span>';
		$href  = '';
		if ( ! $c['placeholder'] ) {
			foreach ( $c['links'] as $l ) {
				$href = $l['url'];
				break;
			}
		}
		// the tile's own text names it (number, name, town), so neither kind carries a separate label
		$out .= $href
			? '<a class="tile roster-tile" href="' . esc_url( gm_utm( $href ) ) . '" target="_blank" rel="noopener">' . $inner . '</a>'
			: '<div class="tile">' . $inner . '</div>';
	}
	return '<section class="block roster"><div class="w"><div class="grid">' . $out . '</div></div></section>';
}

/**
 * Render the creators. Stepper (the page's layout): on wide screens one pinned clip changes as each story reaches the middle
 * of the screen; on phones the stories are a left to right carousel, and a tap opens the clip full size. Roster: a grid of tiles.
 * With no creators it shows a short note. The markup matches the v2 page, so its stylesheet and script apply unchanged.
 *
 * @param array $args Optional. 'layout' (stepper|roster), 'limit' (int), 'next' (string), 'last' (string).
 * @return string HTML
 */
function gm_render_creators( $args = array() ) {
	$layout   = isset( $args['layout'] ) && 'roster' === $args['layout'] ? 'roster' : 'stepper';
	$limit    = isset( $args['limit'] ) ? (int) $args['limit'] : 24;
	$next     = isset( $args['next'] ) && '' !== $args['next'] ? $args['next'] : __( 'Next: ', 'generation-maine' );
	$last     = isset( $args['last'] ) && '' !== $args['last'] ? $args['last'] : __( 'Last one', 'generation-maine' );
	$creators = gm_get_creators( $limit );
	if ( ! $creators ) {
		return '<section class="stories gm-empty"><div class="w"><p>' . esc_html__( 'The creators are being cast. Their clips and stories will appear here.', 'generation-maine' )
			. ( current_user_can( 'edit_posts' ) ? ' <a href="' . esc_url( admin_url( 'post-new.php?post_type=gm_creator' ) ) . '">' . esc_html__( 'Add the first creator.', 'generation-maine' ) . '</a>' : '' ) . '</p></div></section>';
	}
	// the stepper's page script finds its parts by fixed ids, so a second stepper on the same page (a duplicated block, say)
	// shows as a roster instead of a broken copy
	static $steppers = 0;
	if ( 'roster' === $layout || ++$steppers > 1 ) {
		return gm_render_roster( $creators );
	}
	$n      = count( $creators );
	$expand = '<span class="ex" aria-hidden="true"><svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M9.5 2.5h4v4M13.5 2.5 9 7M6.5 13.5h-4v-4M2.5 13.5 7 9"/></svg></span>';
	$stage  = $whos = $panels = $segs = $slides = '';
	foreach ( $creators as $i => $c ) {
		$on    = 0 === $i;
		/* translators: %s: town */
		$town  = $c['town'] ? sprintf( __( '%s, Maine', 'generation-maine' ), $c['town'] ) : __( 'Maine', 'generation-maine' );
		/* translators: 1: creator name, 2: town and state */
		$alt   = sprintf( __( 'Clip by %1$s, %2$s', 'generation-maine' ), $c['name'], $town );
		$len   = $c['len'] ? '<span class="dur">' . esc_html( $c['len'] ) . '</span>' : '';
		$who   = gm_who( $c, $on );
		$stage .= gm_clip( $c, $on ? 'on' : '', ' data-i="' . $i . '" data-dur="' . esc_attr( $c['len'] ) . '"', $alt );
		$whos  .= gm_who( $c, $on, ! $on );
		/* translators: 1: position, 2: creator name, 3: town and state */
		$segs  .= '<button type="button" aria-label="' . esc_attr( sprintf( __( 'Creator %1$d, %2$s, %3$s', 'generation-maine' ), $i + 1, $c['name'], $town ) ) . '" data-name="' . esc_attr( $c['name'] ) . '"' . ( $on ? ' class="on"' : '' ) . '></button>';
		$soc    = '';
		foreach ( $c['links'] as $key => $l ) {
			$soc .= '<a href="' . esc_url( gm_utm( $l['url'] ) ) . '" target="_blank" rel="noopener" aria-label="' . esc_attr( $l['label'] ) . '">' . gm_mark( $key ) . '<span>' . ( $c['handle'] ? gm_bdi( $c['handle'] ) : esc_html( $l['label'] ) ) . '</span></a>';
		}
		/* translators: %s: creator name */
		$open    = sprintf( __( 'Open the clip from %s full size', 'generation-maine' ), $c['name'] );
		$panels .= '<article class="panel' . ( $on ? ' on' : '' ) . '" id="story-' . ( $i + 1 ) . '" data-i="' . $i . '">'
			. '<div class="pv" role="button" tabindex="0" aria-label="' . esc_attr( $open ) . '">' . gm_clip( $c, '', '', '' ) . $who . $len . $expand . '</div>'
			. '<p class="k">' . esc_html( $town ) . '</p><h2>' . gm_bdi( $c['name'] ) . '</h2>'
			// the story as typed, like the name: inside <bdi> the typography filter leaves '--' and the x of 4x4 alone
			. ( $c['bio'] ? '<p class="bio">' . gm_bdi( $c['bio'] ) . '</p>' : '' )
			. ( $soc ? '<div class="soc">' . $soc . '</div>' : '' )
			. '</article>';
		$slides .= '<div class="slide" data-i="' . $i . '"><div class="fr">' . gm_clip( $c, '', '', $alt ) . $who . $len . '</div>'
			. '<div class="cap"><span class="k">' . esc_html( $town ) . '</span><strong>' . gm_bdi( $c['name'] ) . '</strong></div></div>';
	}
	$count = str_pad( (string) $n, 2, '0', STR_PAD_LEFT );
	$first = $creators[0]['len'];
	return '<section class="stories" id="stories" style="--n:' . (int) $n . '"><div class="pinw"><div class="w">'
		. '<div class="stage"><div class="vid" id="stage">' . $stage . $whos . '<span class="dur" id="dur"' . ( $first ? '' : ' hidden' ) . '>' . esc_html( $first ) . '</span></div></div>'
		. '<div class="panels" id="panels" role="group" aria-roledescription="carousel" aria-label="' . esc_attr__( 'The creators', 'generation-maine' ) . '" aria-live="polite" tabindex="0">' . $panels . '</div>'
		. '<div class="where" id="where"><span class="n" id="wn">01 / ' . esc_html( $count ) . '</span>'
		. '<button type="button" class="cpause" id="cpause" aria-pressed="false" aria-label="' . esc_attr__( 'Pause the clips', 'generation-maine' ) . '">'
		. '<svg class="ip" viewBox="0 0 16 16" aria-hidden="true"><path d="M4 3h3v10H4zM9 3h3v10H9z" fill="currentColor"/></svg>'
		. '<svg class="ipl" viewBox="0 0 16 16" aria-hidden="true"><path d="M4.5 2.5v11l9-5.5z" fill="currentColor"/></svg></button>'
		. '<span class="segs' . ( $n > 12 ? ' many' : '' ) . '" id="segs">' . $segs . '</span>'
		. '<span class="next" id="wnext" data-next="' . esc_attr( $next ) . '" data-last="' . esc_attr( $last ) . '"></span></div>'
		. '</div></div></section>'
		. '<div class="viewer" id="viewer" role="dialog" aria-modal="true" aria-label="' . esc_attr__( 'Clip preview', 'generation-maine' ) . '" hidden>'
		. '<div class="vbar"><span class="n" id="vn">01 / ' . esc_html( $count ) . '</span><button type="button" class="vclose" id="vclose" aria-label="' . esc_attr__( 'Close', 'generation-maine' ) . '">'
		. '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M3 3l10 10M13 3 3 13"/></svg></button></div>'
		. '<div class="vtrack" id="vtrack">' . $slides . '</div></div>';
}

/**
 * [gm_creators limit="24"]
 *
 * @param array $atts Shortcode attributes.
 * @return string
 */
function gm_creators_shortcode( $atts ) {
	$atts = shortcode_atts( array( 'limit' => 24, 'layout' => 'stepper' ), $atts, 'gm_creators' );
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
