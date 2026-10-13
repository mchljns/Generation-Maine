<?php
/**
 * Settings > Generation Maine: the facts the page repeats in several places, kept in one place.
 *
 * Channels (Instagram, TikTok, YouTube addresses and handles) feed the follow list and the site's schema.
 * The newsletter's subscribe page feeds the signup form and the Substack row. The footer lines feed the footer.
 * Anything left empty shows as a [CONFIRM] placeholder on the page, or stays hidden where a placeholder would break something.
 *
 * @package generation-maine
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

/**
 * Every setting, grouped by section, with its default and how to clean it.
 *
 * @return array<string,array<string,array{label:string,default:string,type:string,help:string}>>
 */
function gm_settings_fields() {
	return array(
		'channels'   => array(
			'gm_instagram_url'    => array( 'label' => __( 'Instagram address', 'generation-maine' ), 'default' => '', 'type' => 'url', 'help' => __( 'For example https://www.instagram.com/generationmaine/', 'generation-maine' ) ),
			'gm_instagram_handle' => array( 'label' => __( 'Instagram handle', 'generation-maine' ), 'default' => '', 'type' => 'text', 'help' => __( 'With the @, as it shows on the account.', 'generation-maine' ) ),
			'gm_tiktok_url'       => array( 'label' => __( 'TikTok address', 'generation-maine' ), 'default' => '', 'type' => 'url', 'help' => '' ),
			'gm_tiktok_handle'    => array( 'label' => __( 'TikTok handle', 'generation-maine' ), 'default' => '', 'type' => 'text', 'help' => '' ),
			'gm_youtube_url'      => array( 'label' => __( 'YouTube address', 'generation-maine' ), 'default' => '', 'type' => 'url', 'help' => '' ),
			'gm_youtube_handle'   => array( 'label' => __( 'YouTube handle', 'generation-maine' ), 'default' => '', 'type' => 'text', 'help' => '' ),
		),
		'newsletter' => array(
			'gm_newsletter_url'  => array( 'label' => __( 'Substack subscribe page', 'generation-maine' ), 'default' => '', 'type' => 'subscribe', 'help' => __( 'The publication\'s subscribe page, for example https://name.substack.com/subscribe. The Substack row in the follow list uses the same address. Until it is set, visitors see no signup form and you see a note in its place.', 'generation-maine' ) ),
			'gm_newsletter_note' => array( 'label' => __( 'Small print under the form', 'generation-maine' ), 'default' => __( 'Runs on Substack. Unsubscribe in one click.', 'generation-maine' ), 'type' => 'text', 'help' => '' ),
		),
		'footer'     => array(
			'gm_footer_line'  => array( 'label' => __( 'Line beside the footer mark', 'generation-maine' ), 'default' => __( 'Young Mainers on the rules that shape their lives. Short videos and a newsletter, made in Maine.', 'generation-maine' ), 'type' => 'text', 'help' => '' ),
			'gm_legal_line'   => array( 'label' => __( 'Legal line', 'generation-maine' ), 'default' => __( 'Generation Maine. [CONFIRM: legal name, address and contact]', 'generation-maine' ), 'type' => 'text', 'help' => __( 'Shown after the copyright sign and the year, which the page fills in.', 'generation-maine' ) ),
			'gm_contact_url'  => array( 'label' => __( 'Contact link', 'generation-maine' ), 'default' => 'https://mainepolicy.org/contact/', 'type' => 'url', 'help' => __( 'Where "Contact" in the footer goes. The privacy link uses the page set under Settings > Privacy.', 'generation-maine' ) ),
		),
	);
}

/**
 * A setting's value, falling back to its default.
 *
 * @param string $key Option name.
 * @return string
 */
function gm_setting( $key ) {
	foreach ( gm_settings_fields() as $fields ) {
		if ( isset( $fields[ $key ] ) ) {
			return (string) get_option( $key, $fields[ $key ]['default'] );
		}
	}
	return (string) get_option( $key, '' );
}

/**
 * Section titles and the line under each.
 *
 * @return array<string,array{0:string,1:string}>
 */
function gm_settings_sections() {
	return array(
		'channels'   => array( __( 'Channels', 'generation-maine' ), __( 'The follow list on the page and the site\'s search listing read these. Leave a channel empty until the account exists; the page shows a placeholder in its row.', 'generation-maine' ) ),
		'newsletter' => array( __( 'Newsletter', 'generation-maine' ), __( 'The signup form sends the address to Substack, which sends the confirmation email and keeps the list. Nothing is stored on this site.', 'generation-maine' ) ),
		'footer'     => array( __( 'Footer', 'generation-maine' ), '' ),
	);
}

/**
 * Register the options, for the settings page and for the REST API.
 */
function gm_register_setting_options() {
	foreach ( gm_settings_fields() as $fields ) {
		foreach ( $fields as $key => $field ) {
			register_setting(
				'generation_maine',
				$key,
				array(
					'type'              => 'string',
					'default'           => $field['default'],
					'show_in_rest'      => true,
					'sanitize_callback' => 'subscribe' === $field['type'] ? 'gm_sanitize_subscribe' : ( 'url' === $field['type'] ? 'esc_url_raw' : 'sanitize_text_field' ),
				)
			);
		}
	}
}
add_action( 'admin_init', 'gm_register_setting_options' );
add_action( 'rest_api_init', 'gm_register_setting_options' );

/**
 * The sections and fields on Settings > Generation Maine.
 */
function gm_register_settings_ui() {
	$sections = gm_settings_sections();
	foreach ( gm_settings_fields() as $section => $fields ) {
		add_settings_section(
			'gm_' . $section,
			$sections[ $section ][0],
			static function () use ( $sections, $section ) {
				if ( $sections[ $section ][1] ) {
					echo '<p>' . esc_html( $sections[ $section ][1] ) . '</p>';
				}
			},
			'generation_maine'
		);
		foreach ( $fields as $key => $field ) {
			add_settings_field( $key, $field['label'], 'gm_settings_field', 'generation_maine', 'gm_' . $section, array( 'key' => $key, 'field' => $field, 'label_for' => $key ) );
		}
	}
}
add_action( 'admin_init', 'gm_register_settings_ui' );

/**
 * Only an https subscribe page, or empty.
 *
 * @param string $value Raw value.
 * @return string
 */
function gm_sanitize_subscribe( $value ) {
	$value = esc_url_raw( trim( (string) $value ), array( 'https' ) );
	if ( '' !== $value && false === strpos( $value, '/subscribe' ) && function_exists( 'add_settings_error' ) ) {
		add_settings_error( 'gm_newsletter_url', 'gm_newsletter_url', __( 'The address should be the publication\'s subscribe page, ending in /subscribe.', 'generation-maine' ) );
	}
	return $value;
}

/**
 * One field.
 *
 * @param array $args key, field.
 */
function gm_settings_field( $args ) {
	$key   = $args['key'];
	$field = $args['field'];
	$type  = 'text' === $field['type'] ? 'text' : 'url';
	printf( '<input type="%1$s" id="%2$s" name="%2$s" value="%3$s" class="regular-text">', esc_attr( $type ), esc_attr( $key ), esc_attr( get_option( $key, $field['default'] ) ) );
	if ( $field['help'] ) {
		printf( '<p class="description">%s</p>', esc_html( $field['help'] ) );
	}
}

/**
 * Settings > Generation Maine.
 */
function gm_settings_menu() {
	add_options_page( __( 'Generation Maine', 'generation-maine' ), __( 'Generation Maine', 'generation-maine' ), 'manage_options', 'generation_maine', 'gm_settings_page' );
}
add_action( 'admin_menu', 'gm_settings_menu' );

/**
 * The page.
 */
function gm_settings_page() {
	?>
	<div class="wrap">
		<h1><?php esc_html_e( 'Generation Maine', 'generation-maine' ); ?></h1>
		<form action="options.php" method="post">
			<?php
			settings_fields( 'generation_maine' );
			do_settings_sections( 'generation_maine' );
			submit_button();
			?>
		</form>
	</div>
	<?php
}

/**
 * The address the settings page lives at, for the notes the page shows to editors.
 *
 * @return string
 */
function gm_settings_url() {
	return admin_url( 'options-general.php?page=generation_maine' );
}

/**
 * Outbound links carry a source, so the accounts and the newsletter can see what the page sends them.
 *
 * @param string $url Address.
 * @return string
 */
function gm_utm( $url ) {
	if ( '' === $url || 0 !== strpos( $url, 'http' ) || false !== strpos( $url, 'utm_source=' ) ) {
		return $url;
	}
	return add_query_arg( array( 'utm_source' => 'generationmaine', 'utm_medium' => 'site' ), $url );
}
