<?php
/**
 * Server render for generation-maine/creators.
 *
 * @package generation-maine
 *
 * @var array $attributes Block attributes.
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}
echo gm_render_creators( // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped
	array(
		'limit' => isset( $attributes['limit'] ) ? (int) $attributes['limit'] : 24,
		'next'  => isset( $attributes['next'] ) ? $attributes['next'] : '',
		'last'  => isset( $attributes['last'] ) ? $attributes['last'] : '',
	)
);
