/* Creators block editor script. Plain JS, no build step: the editor shows the same server-rendered output. */
( function ( wp ) {
	var el = wp.element.createElement, ServerSideRender = wp.serverSideRender, InspectorControls = wp.blockEditor.InspectorControls;
	var PanelBody = wp.components.PanelBody, RangeControl = wp.components.RangeControl, TextControl = wp.components.TextControl, SelectControl = wp.components.SelectControl;
	wp.blocks.registerBlockType( 'generation-maine/creators', {
		edit: function ( props ) {
			var a = props.attributes, set = props.setAttributes;
			return el( 'div', wp.blockEditor.useBlockProps(),
				el( InspectorControls, null, el( PanelBody, { title: 'Settings' },
					el( SelectControl, { label: 'Layout', value: a.layout || 'roster', options: [ { label: 'Roster: a tile per creator, linking to their feeds', value: 'roster' }, { label: 'Stepper: one pinned clip at a time', value: 'stepper' } ], onChange: function ( v ) { set( { layout: v } ); } } ),
					el( RangeControl, { label: 'Most creators to show', min: 1, max: 48, value: a.limit, onChange: function ( v ) { set( { limit: v } ); } } ),
					el( TextControl, { label: 'Label before the next name', help: 'Default: "Next: "', value: a.next, onChange: function ( v ) { set( { next: v } ); } } ),
					el( TextControl, { label: 'Label on the last creator', help: 'Default: "Last one"', value: a.last, onChange: function ( v ) { set( { last: v } ); } } )
				) ),
				el( ServerSideRender, { block: 'generation-maine/creators', attributes: a } ) );
		},
		save: function () { return null; },
	} );
} )( window.wp );
