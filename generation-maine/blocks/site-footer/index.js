/* Site Footer editor script. Plain JS, no build step. */
( function ( wp ) {
	var el = wp.element.createElement;
	wp.blocks.registerBlockType( 'generation-maine/site-footer', {
		edit: function () {
			return el( 'div', wp.blockEditor.useBlockProps(),
				el( wp.blockEditor.InspectorControls, null, el( wp.components.PanelBody, { title: 'Footer' },
					el( 'p', null, 'The line beside the mark, the legal line and the contact link are set under Settings > Generation Maine. The privacy link uses the page set under Settings > Privacy.' ) ) ),
				el( wp.serverSideRender, { block: 'generation-maine/site-footer' } ) );
		},
		save: function () { return null; },
	} );
} )( window.wp );
