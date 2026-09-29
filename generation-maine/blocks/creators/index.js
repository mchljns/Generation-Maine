/* Creators Grid editor script. Plain JS, no build step: the editor shows the same server-rendered output. */
( function ( wp ) {
	var el = wp.element.createElement;
	var ServerSideRender = wp.serverSideRender;
	var InspectorControls = wp.blockEditor.InspectorControls;
	var useBlockProps = wp.blockEditor.useBlockProps;
	var PanelBody = wp.components.PanelBody;
	var RangeControl = wp.components.RangeControl;

	wp.blocks.registerBlockType( 'generation-maine/creators', {
		edit: function ( props ) {
			return el(
				'div',
				useBlockProps(),
				el(
					InspectorControls,
					null,
					el(
						PanelBody,
						{ title: 'Settings' },
						el( RangeControl, {
							label: 'Most creators to show',
							min: 1,
							max: 48,
							value: props.attributes.limit,
							onChange: function ( v ) {
								props.setAttributes( { limit: v } );
							},
						} )
					)
				),
				el( ServerSideRender, { block: 'generation-maine/creators', attributes: props.attributes } )
			);
		},
		save: function () {
			return null;
		},
	} );
} )( window.wp );
