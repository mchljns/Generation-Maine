/* Follow List editor script. Plain JS, no build step: the editor shows the same server-rendered rows.
 * Selecting the list opens "Edit the channels" under it: a switch per platform (on the page or not), and a link and a
 * handle for each one that is on. They are site settings (shared with the footer icons, the search listing and
 * Settings > Generation Maine), so WordPress saves them with the page: Save lists them under "Site". The rows preview
 * what is typed before it is saved. The platforms come from gm_platforms() (window.gmPlatforms). */
( function ( wp ) {
	var el = wp.element.createElement;
	var TextControl = wp.components.TextControl, ToggleControl = wp.components.ToggleControl, PanelBody = wp.components.PanelBody;
	var PLATFORMS = window.gmPlatforms || [];
	var useSetting = function ( key ) {
		return wp.coreData.useEntityProp( 'root', 'site', key );
	};
	wp.blocks.registerBlockType( 'generation-maine/follow', {
		edit: function ( props ) {
			var site = {}, preview = {};
			// the same hooks in the same order on every render
			PLATFORMS.forEach( function ( p ) {
				( 'substack' === p.key ? [ 'show' ] : [ 'show', 'url', 'handle' ] ).forEach( function ( f ) {
					var key = 'gm_' + p.key + '_' + f;
					site[ key ] = useSetting( key );
					if ( undefined !== site[ key ][ 0 ] ) {
						preview[ key ] = site[ key ][ 0 ];
					}
				} );
			} );
			site.gm_newsletter_url = useSetting( 'gm_newsletter_url' );
			if ( undefined !== site.gm_newsletter_url[ 0 ] ) {
				preview.gm_newsletter_url = site.gm_newsletter_url[ 0 ];
			}
			var allowed = PLATFORMS.length && undefined !== site[ 'gm_' + PLATFORMS[ 0 ].key + '_show' ][ 0 ];
			var text = function ( key, label, help, ph ) {
				return el( TextControl, { key: key, label: label, help: help, placeholder: ph, value: site[ key ][ 0 ] || '', onChange: site[ key ][ 1 ], __nextHasNoMarginBottom: true, __next40pxDefaultSize: true } );
			};
			var platform = function ( p ) {
				var show = site[ 'gm_' + p.key + '_show' ], on = '1' === show[ 0 ];
				return el( 'div', { key: p.key, style: { padding: '12px 0', borderTop: '1px solid #e0e0e0' } },
					el( ToggleControl, { label: el( 'strong', null, p.name ), help: on ? 'On the page' : 'Not on the page', checked: on, onChange: function ( v ) { show[ 1 ]( v ? '1' : '0' ); }, __nextHasNoMarginBottom: true } ),
					on && el( 'div', { style: { display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: 12, marginTop: 10 } },
						'substack' === p.key
							? text( 'gm_newsletter_url', 'Subscribe page', 'Ends in /subscribe. The signup form uses it too.', 'https://name.substack.com/subscribe' )
							: [ text( 'gm_' + p.key + '_url', 'Link to the account', '', p.example ), text( 'gm_' + p.key + '_handle', 'Handle', 'As it shows on the account. Leave empty to show it from the link.', '@generationmaine' ) ] ) );
			};
			var help = 'Switch a platform on to add it to this list and the footer icons, or off to take it off. The rows above update as you type. Click Save at the top to publish; WordPress then asks you to confirm the "Site" changes too.';
			var box = props.isSelected && el( 'div', { className: 'gm-follow-edit', style: { background: '#fff', color: '#1e1e1e', borderRadius: 8, padding: 20, margin: '16px 0', fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif', fontSize: 13, letterSpacing: 'normal', textTransform: 'none' } },
				el( 'p', { style: { margin: '0 0 4px', fontSize: 15, fontWeight: 600 } }, 'Edit the channels' ),
				allowed
					? el( 'div', null, el( 'p', { style: { margin: '0 0 8px', color: '#757575' } }, help ), PLATFORMS.map( platform ) )
					: el( 'p', { style: { margin: 0 } }, 'An administrator sets these under Settings > Generation Maine.' ) );
			return el( 'div', wp.blockEditor.useBlockProps(),
				el( wp.blockEditor.InspectorControls, null,
					el( PanelBody, { title: 'Channels' }, el( 'p', null, allowed ? 'Click the list on the page to switch platforms on or off and edit their links and handles.' : 'An administrator sets these under Settings > Generation Maine.' ) ) ),
				el( wp.serverSideRender, { block: 'generation-maine/follow', attributes: { preview: preview } } ),
				box );
		},
		save: function () { return null; },
	} );
} )( window.wp );
