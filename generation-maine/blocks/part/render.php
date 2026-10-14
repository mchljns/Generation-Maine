<?php
/**
 * Server render for generation-maine/part. No wrapper: the bar's layout counts its direct children.
 *
 * @package generation-maine
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}
echo gm_render_part( isset( $attributes['name'] ) ? (string) $attributes['name'] : '' ); // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped
