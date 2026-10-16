/* Generation Maine Part editor script. Plain JS, no build step: the editor shows the same server-rendered markup as the page. */
( function ( wp ) {
	var el = wp.element.createElement;
	var NAMES = { logo: 'Logo', menu: 'Phone menu button', mural: 'Maine mural' };
	wp.blocks.registerBlockType( 'generation-maine/part', {
		__experimentalLabel: function ( a ) { return NAMES[ a.name ] || 'Part'; },
		edit: function ( props ) {
			var name = props.attributes.name;
			// each part shows once on the page (gm_render_part); the first one in the editor is the one that shows
			var original = wp.data.useSelect( function ( select ) {
				var s = select( 'core/block-editor' ), ids = s.getClientIdsWithDescendants();
				for ( var i = 0; i < ids.length; i++ ) {
					if ( 'generation-maine/part' === s.getBlockName( ids[ i ] ) && name === ( s.getBlockAttributes( ids[ i ] ) || {} ).name ) {
						return ids[ i ];
					}
				}
				return null;
			}, [ name ] );
			var copy = !! original && original !== props.clientId;
			var dispatch = wp.data.useDispatch( 'core/block-editor' );
			// a copy is never hidden like the phone menu button, so its note shows in the bar
			var blockProps = wp.blockEditor.useBlockProps( { className: 'gm-part gm-part-' + ( copy ? 'copy' : name ) } );
			if ( copy ) {
				return el( 'div', blockProps, el( wp.blockEditor.Warning, { actions: [
					el( wp.components.Button, { key: 'find', variant: 'secondary', onClick: function () { dispatch.selectBlock( original ); } }, 'Find original' ),
					el( wp.components.Button, { key: 'remove', variant: 'secondary', onClick: function () {
						// a copy of a locked part is locked too
						dispatch.updateBlockAttributes( props.clientId, { lock: {} } );
						dispatch.removeBlock( props.clientId );
					} }, 'Remove' ),
				] }, ( NAMES[ name ] || 'Part' ) + ': this piece can only be used once. The page leaves this copy out.' ) );
			}
			return el( 'div', blockProps, el( wp.serverSideRender, { block: 'generation-maine/part', attributes: props.attributes } ) );
		},
		save: function () { return null; },
	} );
} )( window.wp );
