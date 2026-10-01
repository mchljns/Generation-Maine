/* Latest Newsletter Posts editor script. Plain JS, no build step. */
( function ( wp ) {
	var el = wp.element.createElement;
	wp.blocks.registerBlockType( 'generation-maine/posts', {
		edit: function ( props ) {
			return el( 'div', wp.blockEditor.useBlockProps(),
				el( wp.blockEditor.InspectorControls, null, el( wp.components.PanelBody, { title: 'Settings' },
					el( wp.components.RangeControl, { label: 'Posts to show', min: 1, max: 6, value: props.attributes.count, onChange: function ( v ) { props.setAttributes( { count: v } ); } } ) ) ),
				el( wp.serverSideRender, { block: 'generation-maine/posts', attributes: props.attributes } ) );
		},
		save: function () { return null; },
	} );
} )( window.wp );
