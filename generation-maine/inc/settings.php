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
			'gm_newsletter_button'      => array( 'label' => __( 'Button text', 'generation-maine' ), 'default' => __( 'Sign up', 'generation-maine' ), 'type' => 'text', 'help' => '' ),
			'gm_newsletter_placeholder' => array( 'label' => __( 'Hint in the email field', 'generation-maine' ), 'default' => 'you@example.com', 'type' => 'text', 'help' => '' ),
			'gm_newsletter_embed'       => array( 'label' => __( 'Substack embed (optional)', 'generation-maine' ), 'default' => '', 'type' => 'code', 'help' => __( 'To use Substack\'s own signup box instead of the theme\'s form, paste the embed code from Substack (Settings > Growth features > Embed, an <iframe>). It takes the form\'s place on the page. Leave empty to keep the theme\'s form.', 'generation-maine' ) ),
		),
		'seo'        => array(
			'gm_seo_title'       => array( 'label' => __( 'Title in search results', 'generation-maine' ), 'default' => '', 'type' => 'text', 'help' => __( 'Leave empty for "Generation Maine: young Mainers on the rules that shape their lives". Ignored when an SEO plugin is active.', 'generation-maine' ) ),
			'gm_seo_description' => array( 'label' => __( 'Description in search results and shares', 'generation-maine' ), 'default' => '', 'type' => 'textarea', 'help' => __( 'One or two sentences, under about 160 characters. Leave empty for the theme\'s line.', 'generation-maine' ) ),
			'gm_seo_image'       => array( 'label' => __( 'Share image', 'generation-maine' ), 'default' => '', 'type' => 'image', 'help' => __( 'The picture shown when the page is shared on social media or in a text message. Best at 1200 by 630 pixels. Leave empty for the theme\'s share card.', 'generation-maine' ) ),
		),
		'footer'     => array(
			'gm_footer_line'  => array( 'label' => __( 'Line beside the footer mark', 'generation-maine' ), 'default' => __( 'Young Mainers on the rules that shape their lives. Short videos and a newsletter, made in Maine.', 'generation-maine' ), 'type' => 'text', 'help' => '' ),
			'gm_legal_line'   => array( 'label' => __( 'Legal line', 'generation-maine' ), 'default' => __( 'Generation Maine. [CONFIRM: legal name, address and contact]', 'generation-maine' ), 'type' => 'text', 'help' => __( 'Shown after the copyright sign and the year, which the page fills in.', 'generation-maine' ) ),
			'gm_contact_url'  => array( 'label' => __( 'Contact link', 'generation-maine' ), 'default' => 'https://mainepolicy.org/contact/', 'type' => 'url', 'help' => __( 'Where "Contact" in the footer goes: a web page, or an email address written as mailto:name@example.org. The privacy link uses the page set under Settings > Privacy.', 'generation-maine' ) ),
		),
		'code'       => array(
			'gm_code_head' => array( 'label' => __( 'Code in the page head', 'generation-maine' ), 'default' => '', 'type' => 'code', 'help' => __( 'Printed in <head> on every page of the site: analytics tags, a site verification tag, a script a service asks for. Only administrators can change it.', 'generation-maine' ) ),
			'gm_code_body' => array( 'label' => __( 'Code at the end of the page', 'generation-maine' ), 'default' => '', 'type' => 'code', 'help' => __( 'Printed just before </body> on every page of the site, for scripts that should load after the page. To put an embed in one spot on a page instead, add a Custom HTML block there in the page editor.', 'generation-maine' ) ),
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
			$value = (string) get_option( $key, $fields[ $key ]['default'] );
			// a cleared line with a default goes back to the default, so the footer is never left with an empty line
			return '' === trim( $value ) && in_array( $key, array( 'gm_footer_line', 'gm_legal_line', 'gm_newsletter_button', 'gm_newsletter_placeholder' ), true ) ? (string) $fields[ $key ]['default'] : $value;
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
		'seo'        => array( __( 'Search and sharing', 'generation-maine' ), __( 'What search engines and social posts show for the home page.', 'generation-maine' ) ),
		'footer'     => array( __( 'Footer', 'generation-maine' ), '' ),
		'code'       => array( __( 'Code and embeds', 'generation-maine' ), __( 'For code a service gives you to paste into the site. Code here runs on every page, so paste only code from a service you trust.', 'generation-maine' ) ),
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
					// code is for administrators on this screen, not for the REST API
					'show_in_rest'      => 'code' !== $field['type'],
					'sanitize_callback' => gm_setting_sanitizer( $key, $field['type'] ),
				)
			);
		}
	}
}
add_action( 'admin_init', 'gm_register_setting_options' );
add_action( 'rest_api_init', 'gm_register_setting_options' );

/**
 * How each kind of setting is cleaned.
 *
 * @param string $key  Option.
 * @param string $type Field type.
 * @return callable
 */
function gm_setting_sanitizer( $key, $type ) {
	if ( 'subscribe' === $type ) {
		return 'gm_sanitize_subscribe';
	}
	if ( 'url' === $type || 'image' === $type ) {
		return gm_url_sanitizer( $key );
	}
	if ( 'code' === $type ) {
		return 'gm_sanitize_code';
	}
	if ( 'textarea' === $type ) {
		return 'sanitize_textarea_field';
	}
	return false !== strpos( $key, '_handle' ) ? 'gm_sanitize_handle' : 'sanitize_text_field';
}

/**
 * True for administrators WordPress trusts with scripts. Editors on a single site may post unfiltered HTML too, so the
 * settings capability is checked as well.
 *
 * @return bool
 */
function gm_can_save_code() {
	return current_user_can( 'manage_options' ) && current_user_can( 'unfiltered_html' );
}

/**
 * Code fields keep scripts and iframes as pasted for administrators WordPress trusts with them (gm_can_save_code()).
 * Anyone else gets the code with scripts and other unsafe markup taken out.
 *
 * @param string $value Raw value.
 * @return string
 */
function gm_sanitize_code( $value ) {
	$value = trim( (string) $value );
	return gm_can_save_code() ? $value : wp_kses_post( $value );
}

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
		// with an SEO plugin the theme steps aside (gm_seo_plugin_active()), so its fields would do nothing; say where to go instead
		if ( 'seo' === $section && gm_seo_plugin_active() ) {
			add_settings_field( 'gm_seo_plugin', '', 'gm_seo_plugin_note', 'generation_maine', 'gm_seo' );
			continue;
		}
		foreach ( $fields as $key => $field ) {
			add_settings_field( $key, $field['label'], 'gm_settings_field', 'generation_maine', 'gm_' . $section, array( 'key' => $key, 'field' => $field, 'label_for' => $key ) );
		}
	}
}
add_action( 'admin_init', 'gm_register_settings_ui' );

/**
 * One notice per field and save, even though WordPress runs the sanitizer twice on an option's first save.
 *
 * @param string $key  Option.
 * @param string $msg  Message.
 * @param string $type error or warning.
 */
function gm_settings_notice( $key, $msg, $type ) {
	if ( ! function_exists( 'add_settings_error' ) ) {
		return;
	}
	foreach ( get_settings_errors( $key ) as $e ) {
		if ( $e['message'] === $msg ) {
			return;
		}
	}
	add_settings_error( $key, $key . '_' . $type, $msg, $type );
}

/**
 * Clean a web address. Plain http becomes https; anything that is not a web address is refused with a notice, and the
 * value saved before stays in place. The Contact link may also be an email address (mailto:).
 *
 * @param string $key   Option.
 * @param string $value Raw value.
 * @return string
 */
function gm_clean_url( $key, $value ) {
	$value = trim( (string) $value );
	if ( '' === $value ) {
		return '';
	}
	if ( 'gm_contact_url' === $key && 0 === stripos( $value, 'mailto:' ) ) {
		// the address before any ?subject= has to be a real email address
		$value = 'mailto:' . substr( $value, 7 );
		$addr  = explode( '?', substr( $value, 7 ), 2 );
		$clean = is_email( rawurldecode( $addr[0] ) ) ? esc_url_raw( $value, array( 'mailto' ) ) : '';
	} else {
		if ( 0 === stripos( $value, 'http://' ) ) {
			$value = 'https://' . substr( $value, 7 );
		} elseif ( ! preg_match( '#^[a-z][a-z0-9+.-]*:#i', $value ) && preg_match( '#^[\w-]+(\.[\w-]+)+(/|$)#', $value ) ) {
			$value = 'https://' . $value;
		}
		$clean = esc_url_raw( $value, array( 'https' ) );
	}
	if ( '' === $clean ) {
		$msg = 'gm_contact_url' === $key
			/* translators: %s: what was typed */
			? __( '"%s" is not a web address or an email address, so the address saved before was kept.', 'generation-maine' )
			/* translators: %s: what was typed */
			: __( '"%s" is not a web address, so the address saved before was kept.', 'generation-maine' );
		gm_settings_notice( $key, sprintf( $msg, wp_strip_all_tags( $value ) ), 'error' );
		// no second argument, so an option never saved keeps its registered default (the Contact link has one)
		return (string) get_option( $key );
	}
	return $clean;
}

/**
 * A sanitizer for one url option.
 *
 * @param string $key Option.
 * @return callable
 */
function gm_url_sanitizer( $key ) {
	return static function ( $value ) use ( $key ) {
		return gm_clean_url( $key, $value );
	};
}

/**
 * A handle shows with one @ and no spaces, however it was typed (a space after the @, two @ signs, the full-width @ that
 * some keyboards type, U+FF20). A lone @ is no handle, so the page falls back to the handle in the address.
 *
 * @param string $value Raw value.
 * @return string
 */
function gm_sanitize_handle( $value ) {
	$value = sanitize_text_field( (string) $value );
	$clean = preg_replace( array( '/[\s\p{Z}\x{200B}-\x{200D}\x{2060}\x{FEFF}]+/u', '/^[@\x{FF20}]+/u' ), '', $value );
	// text that is not valid UTF-8 cannot be read this way; it keeps the old rule
	if ( null === $clean ) {
		$value = trim( $value );
		return '' === $value || '@' === $value[0] ? $value : '@' . $value;
	}
	return '' === $clean ? '' : '@' . $clean;
}

/**
 * The subscribe page: https, and its path should end in /subscribe (a custom domain is fine).
 *
 * @param string $value Raw value.
 * @return string
 */
function gm_sanitize_subscribe( $value ) {
	$value = gm_clean_url( 'gm_newsletter_url', $value );
	$path  = $value ? (string) wp_parse_url( $value, PHP_URL_PATH ) : '';
	if ( '' !== $value && ! preg_match( '#/subscribe/?$#', $path ) ) {
		gm_settings_notice( 'gm_newsletter_url', __( 'Saved. Check the address: it should be the publication\'s subscribe page, ending in /subscribe.', 'generation-maine' ), 'warning' );
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
	$value = (string) get_option( $key, $field['default'] );
	if ( 'code' === $field['type'] || 'textarea' === $field['type'] ) {
		$code = 'code' === $field['type'];
		printf( '<textarea id="%1$s" name="%1$s" rows="%2$d" class="large-text%3$s"%4$s>%5$s</textarea>', esc_attr( $key ), $code ? 6 : 3, $code ? ' code' : '', $code ? ' spellcheck="false"' : '', esc_textarea( $value ) );
		if ( $code && ! gm_can_save_code() ) {
			printf( '<p class="description"><strong>%s</strong></p>', esc_html__( 'Your account cannot save scripts, so they will be taken out. Ask an administrator.', 'generation-maine' ) );
		}
	} elseif ( 'image' === $field['type'] ) {
		printf(
			'<div class="gm-image-field"><img src="" alt="" style="display:none;max-width:300px;height:auto;margin:0 0 8px;border:1px solid #dcdcde"><br><button type="button" class="button gm-image-pick">%1$s</button> <button type="button" class="button-link gm-image-clear">%2$s</button><input type="hidden" id="%3$s" name="%3$s" value="%4$s"></div>',
			esc_html__( 'Choose image', 'generation-maine' ),
			esc_html__( 'Use the theme\'s share card', 'generation-maine' ),
			esc_attr( $key ),
			esc_attr( $value )
		);
	} else {
		$type = 'text' === $field['type'] ? 'text' : 'url';
		printf( '<input type="%1$s" id="%2$s" name="%2$s" value="%3$s" class="regular-text">', esc_attr( $type ), esc_attr( $key ), esc_attr( $value ) );
	}
	if ( $field['help'] ) {
		printf( '<p class="description">%s</p>', esc_html( $field['help'] ) );
	}
}

/**
 * In place of the search fields while an SEO plugin is active.
 */
function gm_seo_plugin_note() {
	$home = 'page' === get_option( 'show_on_front' ) ? (int) get_option( 'page_on_front' ) : 0;
	echo '<p><strong>' . esc_html__( 'An SEO plugin (such as Yoast SEO) is handling this.', 'generation-maine' ) . '</strong> ';
	echo esc_html__( 'Set the title, description and share image for the front page in the plugin\'s box at the bottom of the Home page editor.', 'generation-maine' ) . '</p>';
	if ( $home ) {
		echo '<p><a class="button" href="' . esc_url( (string) get_edit_post_link( $home ) ) . '">' . esc_html__( 'Edit the Home page', 'generation-maine' ) . '</a></p>';
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

/**
 * A name, a handle or an address, printed as it was typed. WordPress's typography filter runs over the whole page and would
 * turn the x of 4x4 into a times sign and -- into a dash; it leaves the inside of <bdi> alone (gm_no_texturize()). <bdi>
 * also keeps a name written right to left from turning the text around it.
 *
 * @param string $text Name, handle or address.
 * @return string HTML
 */
function gm_bdi( $text ) {
	return '<bdi>' . esc_html( $text ) . '</bdi>';
}

/**
 * The typography filter skips <bdi>, as it skips <code>.
 *
 * @param string[] $tags Elements it leaves alone.
 * @return string[]
 */
function gm_no_texturize( $tags ) {
	$tags[] = 'bdi';
	return $tags;
}
add_filter( 'no_texturize_tags', 'gm_no_texturize' );
