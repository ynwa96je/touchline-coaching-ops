// Chiron Leadership: save global classes + build/update one Elementor v4 page.
// Run on the server (e.g. Novamira "execute-php", or `wp eval-file`) after uploading
// a payload produced by build/<page>.py to wp-content/uploads/tc-source/payload.json.
//
// Payload: { "classes": [...all classes...], "page": {title, slug, titles, elements}, "svgs": {name: svg} }
// IMPORTANT: Global_Classes_Repository::put() REPLACES the whole class set, so the payload
// must always carry every class (site_lib.CLASSES does). Class ids are 'g-' + md5(label)[0:7],
// so they stay stable between runs.
use Elementor\Plugin;
use Elementor\Modules\AtomicWidgets\Parsers\Props_Parser;
use Elementor\Modules\AtomicWidgets\CssConverter as CC;
use Elementor\Modules\Variables\Services\Variables_Service;
use Elementor\Modules\Variables\Storage\Variables_Repository;
use Elementor\Modules\Variables\Services\Batch_Operations\Batch_Processor;
use Elementor\Modules\GlobalClasses\Global_Classes_Repository;
use Elementor\Modules\GlobalClasses\Global_Classes_Parser;

$up    = wp_upload_dir();
$build = json_decode( file_get_contents( $up['basedir'] . '/tc-source/payload.json' ), true );

// 1. SVG icons -> media library (sanitised with Elementor's sanitizer; skipped if present)
$san = new \Elementor\Core\Utils\Svg\Svg_Sanitizer();
$svgout = [];
foreach ( $build['svgs'] ?? [] as $name => $content ) {
	$exists = get_posts( [ 'post_type' => 'attachment', 'post_mime_type' => 'image/svg+xml', 'numberposts' => 1, 'meta_key' => '_wp_attached_file', 'meta_value' => _wp_relative_upload_path( $up['path'] . '/' . $name ) ] );
	if ( $exists ) { $svgout[ $name ] = 'exists'; continue; }
	$clean = $san->sanitize( $content );
	$dest  = $up['path'] . '/' . $name;
	file_put_contents( $dest, $clean );
	$aid = wp_insert_attachment( [ 'post_mime_type' => 'image/svg+xml', 'post_title' => ucwords( str_replace( [ 'tc-', '-', '.svg' ], [ '', ' ', '' ], $name ) ), 'post_status' => 'inherit' ], $dest );
	update_post_meta( $aid, '_elementor_inline_svg', $clean );
	$svgout[ $name ] = $aid;
}

// 2. Global classes: CSS declarations -> atomic props via Elementor's own CSS converter.
//    var(--color-*) / var(--font-*) resolve to the global colour/font variables.
$kit  = Plugin::$instance->kits_manager->get_active_kit();
$svc  = new Variables_Service( new Variables_Repository( $kit ), new Batch_Processor() );
$conv = new CC\Css_Converter( CC\Converter_Registry_Factory::create( $svc ), new CC\Metrics\Null_Failure_Reporter(), CC\Expander_Registry_Factory::create( $svc ), new CC\Variable_Prop_Value_Transformer( $svc ) );
// The converter writes raw rgba() into gradient stops; map them back to the scrim colour variables.
$byval = [];
foreach ( $svc->get_variables_list() as $id => $v ) {
	if ( 'global-color-variable' === $v['type'] && false !== strpos( $v['label'], 'scrim' ) ) {
		$byval[ strtolower( str_replace( ' ', '', $v['value'] ) ) ] = $id;
	}
}
$patch = function ( &$node ) use ( &$patch, $byval ) {
	if ( ! is_array( $node ) ) return;
	if ( ( $node['$$type'] ?? null ) === 'color-stop' && ( $node['value']['color']['$$type'] ?? '' ) === 'color' ) {
		$k = strtolower( str_replace( ' ', '', $node['value']['color']['value'] ) );
		if ( isset( $byval[ $k ] ) ) $node['value']['color'] = [ '$$type' => 'global-color-variable', 'value' => $byval[ $k ] ];
	}
	foreach ( $node as &$ch ) $patch( $ch );
};
$items = []; $order = []; $problems = [];
foreach ( $build['classes'] as $c ) {
	$id = 'g-' . substr( md5( $c['label'] ), 0, 7 );
	$variants = [];
	foreach ( $c['variants'] as $k => $css ) {
		[ $bp, $state ] = array_pad( explode( ':', $k ), 2, null );   // e.g. "desktop", "tablet", "desktop:hover"
		$r = $conv->convert( $css );
		if ( '' !== $r['customCss'] || ! empty( $r['rejected'] ) ) $problems[ $c['label'] . ' ' . $k ] = [ $r['customCss'], $r['rejected'] ];
		$props = $r['props'];
		$patch( $props );
		$variants[] = [ 'meta' => [ 'breakpoint' => $bp, 'state' => $state ], 'props' => $props, 'custom_css' => null ];
	}
	$items[ $id ] = [ 'id' => $id, 'label' => $c['label'], 'type' => 'class', 'variants' => $variants ];
	$order[] = $id;   // earlier in the order = higher priority (modifiers come first)
}
if ( $problems ) return [ 'ABORT: CSS the converter could not express' => $problems ];
$parsed = Global_Classes_Parser::make()->parse( [ 'items' => $items, 'order' => $order ] );
if ( ! $parsed->is_valid() ) return [ 'INVALID' => $parsed->errors()->to_string() ];
$d = $parsed->unwrap();
$repo = Global_Classes_Repository::make( $kit );
$repo->put( $d['items'], $d['order'] );

// 3. Page elements: class labels -> class ids, __HOME__ -> site URL, __ATT__key -> attachment id.
//    Photos are looked up by their '_tc_key' post meta; SVGs by file name.
$att = [];
foreach ( get_posts( [ 'post_type' => 'attachment', 'numberposts' => -1, 'meta_key' => '_tc_key' ] ) as $p ) $att[ get_post_meta( $p->ID, '_tc_key', true ) ] = $p->ID;
foreach ( get_posts( [ 'post_type' => 'attachment', 'post_mime_type' => 'image/svg+xml', 'numberposts' => -1 ] ) as $p ) $att[ basename( get_attached_file( $p->ID ) ) ] = $p->ID;
$home = untrailingslashit( home_url() );
$errors = [];
$fix = function ( &$el ) use ( &$fix, $att, $home, &$errors ) {
	$s = &$el['settings'];
	if ( isset( $s['classes'] ) ) $s['classes']['value'] = array_map( fn( $l ) => 'g-' . substr( md5( $l ), 0, 7 ), $s['classes']['value'] );
	array_walk_recursive( $s, function ( &$v ) use ( $att, $home, &$errors ) {
		if ( ! is_string( $v ) ) return;
		if ( 0 === strpos( $v, '__HOME__' ) ) $v = $home . substr( $v, 8 );
		elseif ( 0 === strpos( $v, '__ATT__' ) ) { $k = substr( $v, 7 ); if ( ! isset( $att[ $k ] ) ) $errors[] = 'missing attachment ' . $k; $v = $att[ $k ] ?? 0; }
	} );
	$type = 'widget' === $el['elType'] ? $el['widgetType'] : $el['elType'];
	$cls  = 'widget' === $el['elType'] ? Plugin::$instance->widgets_manager->get_widget_types( $type ) : Plugin::$instance->elements_manager->get_element_types( $type );
	$r = Props_Parser::make( $cls::get_props_schema() )->validate( $s );
	if ( ! $r->is_valid() ) $errors[] = $type . ' ' . $el['id'] . ': ' . $r->errors()->to_string();
	foreach ( $el['elements'] as &$c ) $fix( $c );
};
$elements = $build['page']['elements'];
foreach ( $elements as $i => &$e ) { $fix( $e ); $e['editor_settings'] = [ 'title' => $build['page']['titles'][ $i ] ]; }
unset( $e );
if ( $errors ) return [ 'svgs' => $svgout, 'ERRORS' => $errors ];

$slug = $build['page']['slug'];
$existing = get_page_by_path( $slug, OBJECT, 'page' );
$pid = $existing ? $existing->ID : wp_insert_post( [ 'post_type' => 'page', 'post_title' => $build['page']['title'], 'post_name' => $slug, 'post_status' => 'draft', 'post_content' => '' ] );
update_post_meta( $pid, '_elementor_edit_mode', 'builder' );
update_post_meta( $pid, '_elementor_template_type', 'wp-page' );
update_post_meta( $pid, '_wp_page_template', 'elementor_header_footer' );   // Elementor Full Width
Plugin::$instance->documents->get( $pid, false )->save( [ 'elements' => $elements, 'settings' => [ 'template' => 'elementor_header_footer' ] ] );
// Astra per-page: full-width container, no sidebar, title hidden
foreach ( [ 'ast-site-content-layout' => 'full-width-container', 'site-content-style' => 'unboxed', 'site-sidebar-style' => 'unboxed', 'site-sidebar-layout' => 'no-sidebar', 'site-post-title' => 'disabled', 'ast-banner-title-visibility' => 'disabled' ] as $k => $v ) update_post_meta( $pid, $k, $v );
Plugin::$instance->files_manager->clear_cache();
unlink( $up['basedir'] . '/tc-source/payload.json' );
return [ 'svgs' => $svgout, 'classes' => count( $repo->all( true )->get()['items'] ), 'page_id' => $pid, 'status' => get_post_status( $pid ) ];

// To publish afterwards:  wp_update_post(['ID'=>$pid,'post_status'=>'publish']);
// then clear Hostinger's CDN:  rest_do_request(new WP_REST_Request('DELETE','/hostinger-tools-plugin/v1/clear-cache'))  (as an admin user)
