<?php
/**
 * Newsletter: the Substack hand-off and its settings.
 *
 * The signup form on the front page sends the address to the publication's subscribe page on Substack,
 * which fills its field from the query string, sends the confirmation email and shows its own confirmation.
 * The publication address lives in Settings > Newsletter, so nobody edits a template to change it.
 *
 * Settings: subscribe URL, open in a new tab, the line shown on the page after submit, the small print under the form.
 *
 * @package generation-maine
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

/**
 * The settings and their defaults.
 *
 * @return array<string,array{label:string,default:string,type:string,help:string}>
 */
function gm_newsletter_fields() {
	return array(
		'gm_newsletter_url'     => array(
			'label'   => __( 'Subscribe page URL', 'generation-maine' ),
			'default' => '',
			'type'    => 'url',
			'help'    => __( 'The publication\'s subscribe page, for example https://name.substack.com/subscribe. The visitor\'s address is added to it on submit. Leave empty to hide the form.', 'generation-maine' ),
		),
		'gm_newsletter_new_tab' => array(
			'label'   => __( 'Open in a new tab', 'generation-maine' ),
			'default' => '1',
			'type'    => 'checkbox',
			'help'    => __( 'Keeps the site open while Substack confirms the signup.', 'generation-maine' ),
		),
		'gm_newsletter_confirm' => array(
			'label'   => __( 'Line shown after submit', 'generation-maine' ),
			'default' => __( 'Check your inbox. The confirmation is on its way.', 'generation-maine' ),
			'type'    => 'text',
			'help'    => '',
		),
		'gm_newsletter_note'    => array(
			'label'   => __( 'Small print under the form', 'generation-maine' ),
			'default' => __( 'Runs on Substack. Unsubscribe in one click.', 'generation-maine' ),
			'type'    => 'text',
			'help'    => '',
		),
	);
}

/**
 * Register the settings and the Settings > Newsletter page.
 */
function gm_newsletter_settings() {
	foreach ( gm_newsletter_fields() as $key => $field ) {
		register_setting(
			'gm_newsletter',
			$key,
			array(
				'type'              => 'string',
				'default'           => $field['default'],
				'show_in_rest'      => true,
				'sanitize_callback' => 'url' === $field['type'] ? 'gm_newsletter_sanitize_url' : ( 'checkbox' === $field['type'] ? 'gm_newsletter_sanitize_flag' : 'sanitize_text_field' ),
			)
		);
	}
	add_settings_section( 'gm_newsletter_main', __( 'Substack hand-off', 'generation-maine' ), 'gm_newsletter_section_text', 'gm_newsletter' );
	foreach ( gm_newsletter_fields() as $key => $field ) {
		add_settings_field( $key, $field['label'], 'gm_newsletter_field', 'gm_newsletter', 'gm_newsletter_main', array( 'key' => $key, 'field' => $field, 'label_for' => $key ) );
	}
}
add_action( 'admin_init', 'gm_newsletter_settings' );

/**
 * Only https Substack-style URLs, or empty.
 *
 * @param string $value Raw value.
 * @return string
 */
function gm_newsletter_sanitize_url( $value ) {
	$value = esc_url_raw( trim( (string) $value ), array( 'https' ) );
	if ( '' !== $value && ! str_contains( $value, '/subscribe' ) ) {
		add_settings_error( 'gm_newsletter_url', 'gm_newsletter_url', __( 'The address should be the publication\'s subscribe page, ending in /subscribe.', 'generation-maine' ) );
	}
	return $value;
}

/**
 * Checkbox to "1" or "".
 *
 * @param mixed $value Raw value.
 * @return string
 */
function gm_newsletter_sanitize_flag( $value ) {
	return $value ? '1' : '';
}

/**
 * Intro text on the settings page.
 */
function gm_newsletter_section_text() {
	echo '<p>' . esc_html__( 'The signup form sends the address to Substack. Substack sends the confirmation email and keeps the list. Nothing is stored on this site.', 'generation-maine' ) . '</p>';
}

/**
 * One settings field.
 *
 * @param array $args key, field.
 */
function gm_newsletter_field( $args ) {
	$key   = $args['key'];
	$field = $args['field'];
	$value = get_option( $key, $field['default'] );
	if ( 'checkbox' === $field['type'] ) {
		printf( '<label><input type="checkbox" id="%1$s" name="%1$s" value="1" %2$s> %3$s</label>', esc_attr( $key ), checked( '1', $value, false ), esc_html( $field['help'] ) );
		return;
	}
	printf( '<input type="%1$s" id="%2$s" name="%2$s" value="%3$s" class="regular-text">', esc_attr( $field['type'] ), esc_attr( $key ), esc_attr( $value ) );
	if ( $field['help'] ) {
		printf( '<p class="description">%s</p>', esc_html( $field['help'] ) );
	}
}

/**
 * Settings > Newsletter.
 */
function gm_newsletter_menu() {
	add_options_page( __( 'Newsletter', 'generation-maine' ), __( 'Newsletter', 'generation-maine' ), 'manage_options', 'gm_newsletter', 'gm_newsletter_page' );
}
add_action( 'admin_menu', 'gm_newsletter_menu' );

/**
 * The settings page.
 */
function gm_newsletter_page() {
	?>
	<div class="wrap">
		<h1><?php esc_html_e( 'Newsletter', 'generation-maine' ); ?></h1>
		<form action="options.php" method="post">
			<?php
			settings_fields( 'gm_newsletter' );
			do_settings_sections( 'gm_newsletter' );
			submit_button();
			?>
		</form>
	</div>
	<?php
}

/**
 * The signup form, rendered from the settings. Empty when no address is set.
 *
 * @return string HTML
 */
function gm_render_newsletter_form() {
	$url = get_option( 'gm_newsletter_url', '' );
	if ( '' === $url ) {
		return current_user_can( 'manage_options' )
			? '<p class="gm-newsletter-missing">' . sprintf(
				/* translators: %s: link to the settings page */
				esc_html__( 'The signup form is hidden until a subscribe page is set under %s.', 'generation-maine' ),
				'<a href="' . esc_url( admin_url( 'options-general.php?page=gm_newsletter' ) ) . '">' . esc_html__( 'Settings > Newsletter', 'generation-maine' ) . '</a>'
			) . '</p>'
			: '';
	}
	$new_tab = '1' === get_option( 'gm_newsletter_new_tab', '1' );
	$id      = wp_unique_id( 'gm-email-' );
	ob_start();
	?>
	<form class="gm-newsletter" method="get" action="<?php echo esc_url( $url ); ?>"<?php echo $new_tab ? ' target="_blank" rel="noopener"' : ''; ?> data-confirm="<?php echo esc_attr( get_option( 'gm_newsletter_confirm', '' ) ); ?>">
		<label class="gm-newsletter__label" for="<?php echo esc_attr( $id ); ?>"><?php esc_html_e( 'Email', 'generation-maine' ); ?></label>
		<div class="gm-newsletter__row">
			<input id="<?php echo esc_attr( $id ); ?>" type="email" name="email" placeholder="you@example.com" autocomplete="email" required>
			<button type="submit" class="wp-element-button"><?php esc_html_e( 'Subscribe', 'generation-maine' ); ?></button>
		</div>
		<p class="gm-newsletter__note"><?php echo esc_html( get_option( 'gm_newsletter_note', '' ) ); ?></p>
		<p class="gm-newsletter__ok" hidden></p>
	</form>
	<?php
	return (string) ob_get_clean();
}

/**
 * The block.
 */
function gm_register_newsletter_block() {
	register_block_type( get_theme_file_path( 'blocks/newsletter' ) );
}
add_action( 'init', 'gm_register_newsletter_block' );


/**
 * The publication's feed address, worked out from the subscribe URL in settings. Empty when none is set.
 *
 * @return string
 */
function gm_newsletter_feed_url() {
	$url = get_option( 'gm_newsletter_url', '' );
	if ( '' === $url ) {
		return '';
	}
	$parts = wp_parse_url( $url );
	if ( empty( $parts['host'] ) ) {
		return '';
	}
	return 'https://' . $parts['host'] . '/feed';
}

/**
 * The latest posts from the publication, read from its feed and cached for an hour. Placeholders until an address is set
 * or when the feed cannot be read.
 *
 * @param int $count Posts to show.
 * @return string HTML
 */
function gm_render_posts( $count = 3 ) {
	$count = max( 1, min( 6, (int) $count ) );
	$items = array();
	$feed  = gm_newsletter_feed_url();
	if ( $feed ) {
		include_once ABSPATH . WPINC . '/feed.php';
		add_filter( 'wp_feed_cache_transient_lifetime', 'gm_feed_lifetime' );
		$rss = fetch_feed( $feed );
		remove_filter( 'wp_feed_cache_transient_lifetime', 'gm_feed_lifetime' );
		if ( ! is_wp_error( $rss ) ) {
			foreach ( $rss->get_items( 0, $count ) as $it ) {
				$author  = $it->get_author();
				$items[] = array(
					'title' => $it->get_title(),
					'line'  => wp_trim_words( wp_strip_all_tags( (string) $it->get_description() ), 22 ),
					'by'    => $author ? $author->get_name() : '',
					'date'  => $it->get_date( get_option( 'date_format' ) ),
					'url'   => $it->get_permalink(),
				);
			}
		}
	}
	if ( ! $items ) {
		$towns = array( 'Belfast', 'Machias', 'Lewiston', 'Rumford', 'Sanford', 'Fort Kent' );
		for ( $i = 0; $i < $count; $i++ ) {
			$items[] = array(
				'title' => '[Post title, plain words]',
				'line'  => '[One line on what the creator found out.]',
				'by'    => '[Creator name] ' . $towns[ $i % count( $towns ) ] . ', Maine',
				'date'  => '[Date]',
				'url'   => '#',
			);
		}
	}
	$html = '<span class="rule" aria-hidden="true"></span>';
	foreach ( $items as $p ) {
		$html .= '<a class="post row-in" href="' . esc_url( $p['url'] ) . '"' . ( '#' === $p['url'] ? '' : ' target="_blank" rel="noopener"' ) . '><div><h3>' . esc_html( $p['title'] ) . '</h3>';
		if ( $p['line'] ) {
			$html .= '<p>' . esc_html( $p['line'] ) . '</p>';
		}
		if ( $p['by'] ) {
			$html .= '<p class="by">' . esc_html( $p['by'] ) . '</p>';
		}
		$html .= '</div><span class="dt">' . esc_html( $p['date'] ) . '</span></a>';
	}
	return $html;
}

/**
 * Cache the feed for an hour.
 *
 * @return int
 */
function gm_feed_lifetime() {
	return HOUR_IN_SECONDS;
}

/**
 * The posts block.
 */
function gm_register_posts_block() {
	register_block_type( get_theme_file_path( 'blocks/posts' ) );
}
add_action( 'init', 'gm_register_posts_block' );
