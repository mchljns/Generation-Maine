<?php
// REST users as each role, through the real REST server (rest_do_request runs the same filters as an HTTP request).
foreach ( array( 0 => 'visitor', 2 => 'author1', 3 => 'editor1', 4 => 'contrib1', 1 => 'admin' ) as $uid => $label ) {
	wp_set_current_user( $uid );
	$out = array();
	foreach ( array( array( '/wp/v2/users', array() ), array( '/wp/v2/users', array( 'who' => 'authors' ) ), array( '/wp/v2/users', array( 'has_published_posts' => array( 'gm_creator' ) ) ), array( '/wp/v2/users/2', array() ), array( '/wp/v2/users/4', array() ), array( '/wp/v2/users/3', array() ), array( '/wp/v2/users/me', array() ) ) as $q ) {
		$r = new WP_REST_Request( 'GET', $q[0] );
		foreach ( $q[1] as $k => $v ) { $r->set_param( $k, $v ); }
		$res  = rest_do_request( $r );
		$data = $res->get_data();
		$ids  = isset( $data['code'] ) ? $data['code'] : ( isset( $data['id'] ) ? 'id ' . $data['id'] : implode( ',', wp_list_pluck( (array) $data, 'slug' ) ) );
		$out[] = $q[0] . ( $q[1] ? '?' . http_build_query( $q[1] ) : '' ) . ' => ' . $res->get_status() . ' ' . $ids;
	}
	echo "== $label\n  " . implode( "\n  ", $out ) . "\n";
}
