// Chiron Leadership: create or update the Elementor global variables (colours + fonts) and the kit's global
// fonts from wp-content/uploads/tc-source/design-tokens.json (a copy of ../design-tokens.json).
// Run once before the first page build, and again whenever the brand colours or fonts change.
// Font values are written as quoted stacks on purpose: Elementor writes an unquoted multi-word family name,
// which is invalid CSS.
use Elementor\Plugin;
use Elementor\Modules\Variables\Services\Variables_Service;
use Elementor\Modules\Variables\Storage\Variables_Repository;
use Elementor\Modules\Variables\Services\Batch_Operations\Batch_Processor;
$up  = wp_upload_dir();
$tok = json_decode( file_get_contents( $up['basedir'] . '/tc-source/design-tokens.json' ), true );
$kit = Plugin::$instance->kits_manager->get_active_kit();
$svc = new Variables_Service( new Variables_Repository( $kit ), new Batch_Processor() );
$existing = [];
foreach ( $svc->get_variables_list() as $id => $v ) $existing[ $v['label'] ] = $id;
$out = []; $order = count( $existing ) + 1;
$put = function ( $type, $label, $value ) use ( $svc, &$existing, &$out, &$order ) {
	try {
		if ( isset( $existing[ $label ] ) ) { $svc->update( $existing[ $label ], [ 'value' => $value ] ); $out[ $label ] = 'updated'; }
		else { $r = $svc->create( [ 'type' => $type, 'label' => $label, 'value' => $value, 'order' => $order++ ] ); $existing[ $label ] = $r['variable']['id']; $out[ $label ] = 'created'; }
	} catch ( \Throwable $e ) { $out[ $label ] = 'ERROR ' . $e->getMessage(); }
};
foreach ( $tok['colors'] as $label => $value ) $put( 'global-color-variable', $label, $value );
foreach ( $tok['fonts'] as $label => $f ) $put( 'global-font-variable', $label, $f['stack'] );
// Kit global fonts make Elementor load the Google Fonts the variables name.
$typo = $kit->get_settings( 'system_typography' );
$map  = [ 'primary' => $tok['fonts']['font-serif']['family'], 'secondary' => $tok['fonts']['font-sans']['family'], 'text' => $tok['fonts']['font-sans']['family'], 'accent' => $tok['fonts']['font-sans']['family'] ];
foreach ( $typo as &$t ) if ( isset( $map[ $t['_id'] ] ) ) $t['typography_font_family'] = $map[ $t['_id'] ];
unset( $t );
$kit->save( [ 'settings' => array_merge( $kit->get_settings(), [ 'system_typography' => $typo ] ) ] );
Plugin::$instance->files_manager->clear_cache();
unlink( $up['basedir'] . '/tc-source/design-tokens.json' );
return $out;
