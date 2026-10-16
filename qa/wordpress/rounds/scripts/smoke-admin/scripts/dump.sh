#!/usr/bin/env bash
# List every creator with its placeholder and seeded marks, media and author: dump.sh <instance>
wpt wp "$1" eval '
foreach ( get_posts( array( "post_type" => "gm_creator", "post_status" => array_keys( get_post_stati() ), "numberposts" => -1, "orderby" => "ID", "order" => "ASC" ) ) as $p ) {
  if ( "auto-draft" === $p->post_status ) continue;
  $t = (int) get_post_meta( $p->ID, "_thumbnail_id", true ); $c = (int) get_post_meta( $p->ID, "gm_clip_id", true );
  printf( "%d|%s|%s|ph=%s|seeded=%s|thumb=%d(%s)|clip=%d(%s)|link=%s|ig=%s|handle=%s|town=%s|author=%d\n", $p->ID, $p->post_title, $p->post_status, get_post_meta( $p->ID, "gm_placeholder", true ), get_post_meta( $p->ID, "gm_seeded", true ), $t, $t ? get_post_meta( $t, "gm_seeded", true ) : "", $c, $c ? get_post_meta( $c, "gm_seeded", true ) : "", get_post_meta( $p->ID, "gm_clip_url", true ), get_post_meta( $p->ID, "gm_instagram", true ), get_post_meta( $p->ID, "gm_handle", true ), get_post_meta( $p->ID, "gm_hometown", true ), $p->post_author );
}
echo "seeded media: " . count( get_posts( array( "post_type" => "attachment", "post_status" => "any", "numberposts" => -1, "meta_key" => "gm_seeded", "fields" => "ids" ) ) ) . "\n";
echo "trash count: " . count( get_posts( array( "post_type" => "gm_creator", "post_status" => "trash", "numberposts" => -1, "fields" => "ids" ) ) ) . "\n";
' 2>/dev/null
