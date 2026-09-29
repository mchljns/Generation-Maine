<?php
/**
 * QA helper for WordPress Playground. Not part of the theme.
 *
 * - Activates the theme and sets pretty permalinks on first load.
 * - /?gm_seed=12 seeds 12 placeholder creators, /?gm_seed=0 removes them.
 * - Logs every PHP error, warning and notice to qa/php-errors.log.
 */

error_reporting( E_ALL );
ini_set( 'display_errors', '1' ); // phpcs:ignore WordPress.PHP.IniSet.display_errors_Disallowed

set_error_handler(
	static function ( $no, $str, $file, $line ) {
		$log = __DIR__ . '/../php-errors.log';
		file_put_contents( $log, gmdate( 'c' ) . " [$no] $str in $file:$line\n", FILE_APPEND );
		return false;
	}
);
register_shutdown_function(
	static function () {
		$e = error_get_last();
		if ( $e && in_array( $e['type'], array( E_ERROR, E_PARSE, E_CORE_ERROR, E_COMPILE_ERROR ), true ) ) {
			file_put_contents( __DIR__ . '/../php-errors.log', gmdate( 'c' ) . " [FATAL] {$e['message']} in {$e['file']}:{$e['line']}\n", FILE_APPEND );
		}
	}
);

add_action(
	'init',
	static function () {
		if ( 'generation-maine' !== get_option( 'stylesheet' ) ) {
			switch_theme( 'generation-maine' );
			update_option( 'blogname', 'Generation Maine' );
			update_option( 'blogdescription', 'Young Mainers on building a life here' );
			update_option( 'permalink_structure', '/%postname%/' );
			foreach ( get_posts( array( 'post_type' => array( 'post', 'page' ), 'numberposts' => -1, 'post_status' => 'any' ) ) as $p ) {
				wp_delete_post( $p->ID, true );
			}
			flush_rewrite_rules();
		}
		if ( isset( $_GET['gm_seed'] ) ) { // phpcs:ignore WordPress.Security.NonceVerification.Recommended
			$args = array( (int) $_GET['gm_seed'] ); // phpcs:ignore WordPress.Security.NonceVerification.Recommended
			require get_theme_file_path( 'bin/seed-creators.php' );
			wp_safe_redirect( home_url( '/' ) );
			exit;
		}
	},
	99
);
