/* Generation Maine Part editor script. Plain JS, no build step: the editor shows the same server-rendered markup as the page. */
( function ( wp ) {
	var el = wp.element.createElement;
	var NAMES = { logo: 'Logo', menu: 'Phone menu button', mural: 'Maine mural' };
	wp.blocks.registerBlockType( 'generation-maine/part', {
		__experimentalLabel: function ( a ) { return NAMES[ a.name ] || 'Part'; },
		edit: function ( props ) {
			return el( 'div', wp.blockEditor.useBlockProps( { className: 'gm-part gm-part-' + props.attributes.name } ),
				el( wp.serverSideRender, { block: 'generation-maine/part', attributes: props.attributes } ) );
		},
		save: function () { return null; },
	} );
} )( window.wp );
