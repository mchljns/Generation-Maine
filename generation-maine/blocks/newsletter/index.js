/* Newsletter Signup editor script. Plain JS, no build step: the editor shows the same server-rendered output. */
( function ( wp ) {
	var el = wp.element.createElement;
	wp.blocks.registerBlockType( 'generation-maine/newsletter', {
		edit: function () {
			return el( 'div', wp.blockEditor.useBlockProps(), el( wp.serverSideRender, { block: 'generation-maine/newsletter' } ) );
		},
		save: function () {
			return null;
		},
	} );
} )( window.wp );
