/* Follow List editor script. Plain JS, no build step: the editor shows the same server-rendered rows. */
( function ( wp ) {
	var el = wp.element.createElement;
	wp.blocks.registerBlockType( 'generation-maine/follow', {
		edit: function () {
			return el( 'div', wp.blockEditor.useBlockProps(),
				el( wp.blockEditor.InspectorControls, null, el( wp.components.PanelBody, { title: 'Channels' },
					el( 'p', null, 'Addresses and handles are set under Settings > Generation Maine.' ) ) ),
				el( wp.serverSideRender, { block: 'generation-maine/follow' } ) );
		},
		save: function () { return null; },
	} );
} )( window.wp );
