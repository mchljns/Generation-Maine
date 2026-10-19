/* Follow List editor script. Plain JS, no build step: the editor shows the same server-rendered rows.
 * The sidebar edits the channel addresses and handles in place. They are site settings (shared with the footer icons, the
 * search listing and Settings > Generation Maine), so WordPress saves them with the page: Save lists them under "Site". */
( function ( wp ) {
	var el = wp.element.createElement;
	var TextControl = wp.components.TextControl, PanelBody = wp.components.PanelBody, Notice = wp.components.Notice;
	var CHANNELS = [ [ 'instagram', 'Instagram', 'https://www.instagram.com/generationmaine/' ], [ 'tiktok', 'TikTok', 'https://www.tiktok.com/@generationmaine' ], [ 'youtube', 'YouTube', 'https://www.youtube.com/@generationmaine' ] ];
	wp.blocks.registerBlockType( 'generation-maine/follow', {
		edit: function ( props ) {
			var site = {}, preview = {};
			// the same hooks in the same order on every render
			CHANNELS.forEach( function ( c ) {
				[ 'url', 'handle' ].forEach( function ( f ) {
					var key = 'gm_' + c[ 0 ] + '_' + f, prop = wp.coreData.useEntityProp( 'root', 'site', key );
					site[ key ] = prop;
					if ( undefined !== prop[ 0 ] ) {
						preview[ key ] = prop[ 0 ];
					}
				} );
			} );
			site.gm_newsletter_url = wp.coreData.useEntityProp( 'root', 'site', 'gm_newsletter_url' );
			if ( undefined !== site.gm_newsletter_url[ 0 ] ) {
				preview.gm_newsletter_url = site.gm_newsletter_url[ 0 ];
			}
			var allowed = undefined !== site.gm_instagram_url[ 0 ];
			var field = function ( key, label, help, ph ) {
				return el( TextControl, { key: key, label: label, help: help, placeholder: ph, value: site[ key ][ 0 ] || '', onChange: site[ key ][ 1 ], __nextHasNoMarginBottom: true, __next40pxDefaultSize: true } );
			};
			var panels = allowed
				? CHANNELS.map( function ( c ) {
					return el( PanelBody, { key: c[ 0 ], title: c[ 1 ], initialOpen: true },
						field( 'gm_' + c[ 0 ] + '_url', 'Link to the account', 'Paste the address from the browser.', c[ 2 ] ),
						el( 'div', { style: { height: 12 } } ),
						field( 'gm_' + c[ 0 ] + '_handle', 'Handle', 'As it shows on the account, with the @.', '@generationmaine' ) );
				} ).concat( [ el( PanelBody, { key: 'substack', title: 'Substack', initialOpen: true },
					field( 'gm_newsletter_url', 'Subscribe page', 'The newsletter\'s subscribe page, ending in /subscribe. The signup form uses it too.', 'https://name.substack.com/subscribe' ) ) ] )
				: [ el( PanelBody, { key: 'note', title: 'Channels' }, el( 'p', null, 'An administrator sets the links and handles here or under Settings > Generation Maine.' ) ) ];
			// inside the Home page's locked section WordPress shows no block sidebar, so the fields also open on the page itself
			var box = props.isSelected && el( 'div', { className: 'gm-follow-edit', style: { background: '#fff', color: '#1e1e1e', borderRadius: 8, padding: 20, margin: '16px 0', fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif', fontSize: 13, letterSpacing: 'normal', textTransform: 'none' } },
				el( 'p', { style: { margin: '0 0 12px', fontSize: 15, fontWeight: 600 } }, 'Edit the channel links and handles' ),
				allowed
					? el( 'div', null,
						el( 'div', { style: { display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: 16 } },
							CHANNELS.map( function ( c ) {
								return el( 'div', { key: c[ 0 ] },
									el( 'p', { style: { margin: '0 0 6px', fontWeight: 600 } }, c[ 1 ] ),
									field( 'gm_' + c[ 0 ] + '_url', 'Link to the account', '', c[ 2 ] ),
									el( 'div', { style: { height: 8 } } ),
									field( 'gm_' + c[ 0 ] + '_handle', 'Handle, with the @', '', '@generationmaine' ) );
							} ),
							el( 'div', { key: 'substack' },
								el( 'p', { style: { margin: '0 0 6px', fontWeight: 600 } }, 'Substack' ),
								field( 'gm_newsletter_url', 'Subscribe page', 'Ends in /subscribe. The signup form uses it too.', 'https://name.substack.com/subscribe' ) ) ),
						el( 'p', { style: { margin: '12px 0 0', color: '#757575' } }, 'The rows above update as you type. Click Save at the top to publish. WordPress may ask you to confirm saving "Site" settings too: leave it ticked. These links also feed the footer icons.' ) )
					: el( 'p', { style: { margin: 0 } }, 'An administrator sets these under Settings > Generation Maine.' ) );
			return el( 'div', wp.blockEditor.useBlockProps(),
				el( wp.blockEditor.InspectorControls, null,
					allowed && el( 'div', { style: { padding: '0 16px' } }, el( Notice, { status: 'info', isDismissible: false }, 'These links and handles are shared with the footer icons. Click Save to publish them; WordPress lists them under "Site" when it asks what to save.' ) ),
					panels ),
				el( wp.serverSideRender, { block: 'generation-maine/follow', attributes: { preview: preview } } ),
				box );
		},
		save: function () { return null; },
	} );
} )( window.wp );
