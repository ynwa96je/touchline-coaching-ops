wp_set_current_user( 1 );
// Chiron Leadership: save global classes + build/update SEVERAL Elementor v4 pages in one run.
// Payload wp-content/uploads/tc-source/bundle.json = { classes, pages:[{title, slug, parent?, id?, titles, elements, seo?}] }.
// Existing pages are addressed by 'id'; new pages are created (published) under 'parent' (a slug).
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
$build = json_decode( file_get_contents( $up['basedir'] . '/tc-source/bundle.json' ), true );

// 1. SVG icons (none in a bundle; kept for parity) -> media library (sanitised with Elementor's sanitizer; skipped if present)
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

// 3. Pages
$att = [];
foreach ( get_posts( [ 'post_type' => 'attachment', 'numberposts' => -1, 'meta_key' => '_tc_key' ] ) as $p ) $att[ get_post_meta( $p->ID, '_tc_key', true ) ] = $p->ID;
foreach ( get_posts( [ 'post_type' => 'attachment', 'post_mime_type' => 'image/svg+xml', 'numberposts' => -1 ] ) as $p ) $att[ basename( get_attached_file( $p->ID ) ) ] = $p->ID;
$home = untrailingslashit( home_url() );
$report = [];
foreach ( $build['pages'] as $pg ) {
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
	$elements = $pg['elements'];
	foreach ( $elements as $i => &$e ) { $fix( $e ); $e['editor_settings'] = [ 'title' => $pg['titles'][ $i ] ]; }
	unset( $e );
	if ( $errors ) { $report[ $pg['slug'] ] = [ 'ERRORS' => $errors ]; continue; }
	if ( ! empty( $pg['id'] ) ) {
		$pid = (int) $pg['id'];
	} else {
		$parent = ! empty( $pg['parent'] ) ? get_page_by_path( $pg['parent'], OBJECT, 'page' ) : null;
		$path = ( $parent ? $pg['parent'] . '/' : '' ) . $pg['slug'];
		$existing = get_page_by_path( $path, OBJECT, 'page' );
		$pid = $existing ? $existing->ID : wp_insert_post( [ 'post_type' => 'page', 'post_title' => $pg['title'], 'post_name' => $pg['slug'], 'post_parent' => $parent ? $parent->ID : 0, 'post_status' => 'draft', 'post_content' => '' ] );
	}
	update_post_meta( $pid, '_elementor_edit_mode', 'builder' );
	update_post_meta( $pid, '_elementor_template_type', 'wp-page' );
	update_post_meta( $pid, '_wp_page_template', 'elementor_header_footer' );   // Elementor Full Width
	Plugin::$instance->documents->get( $pid, false )->save( [ 'elements' => $elements, 'settings' => [ 'template' => 'elementor_header_footer' ] ] );
	foreach ( [ 'ast-site-content-layout' => 'full-width-container', 'site-content-style' => 'unboxed', 'site-sidebar-style' => 'unboxed', 'site-sidebar-layout' => 'no-sidebar', 'site-post-title' => 'disabled', 'ast-banner-title-visibility' => 'disabled' ] as $k => $v ) update_post_meta( $pid, $k, $v );
	if ( ! empty( $pg['seo'] ) ) {
		wp_update_post( [ 'ID' => $pid, 'post_status' => 'publish', 'post_excerpt' => $pg['seo']['description'] ] );
		// SEO title/description through the Visibility SEO plugin, when it is installed.
		$ab = function_exists( 'wp_get_ability' ) ? wp_get_ability( 'native-aeo-pack/update-post-seo' ) : null;
		$r = ! $ab ? new WP_Error( 'no_seo_plugin', 'Visibility SEO plugin not active: set the SEO title and description another way' ) : $ab->execute( [ 'post_id' => $pid, 'title' => $pg['seo']['title'], 'description' => $pg['seo']['description'], 'og_title' => $pg['seo']['title'], 'og_description' => $pg['seo']['description'] ] );
		if ( is_wp_error( $r ) ) $errors[] = 'seo: ' . $r->get_error_message();
	}
	$report[ $pg['slug'] ] = [ 'id' => $pid, 'status' => get_post_status( $pid ), 'url' => get_permalink( $pid ), 'errors' => $errors ];
}
Plugin::$instance->files_manager->clear_cache();
unlink( $up['basedir'] . '/tc-source/bundle.json' );
rest_do_request( new WP_REST_Request( 'DELETE', '/hostinger-tools-plugin/v1/clear-cache' ) );
return [ 'classes' => count( $repo->all( true )->get()['items'] ), 'pages' => $report ];
