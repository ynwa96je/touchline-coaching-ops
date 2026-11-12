// Chiron Leadership: server-side photo conversion + media library import.
// Upload a JSON payload { "<key>": "<base64 of original JPEG/PNG>", ... } to
// wp-content/uploads/tc-source/photos.json, fill $meta below, then run this on the server.
//
// Rules applied (from the brief): photographs -> WebP, longest edge <= 1600px, file < 400 KB
// (quality starts at 82 and steps down by 6 until it fits). Logos / images with transparency
// stay PNG (see the crest handling in README). Each attachment gets alt text and an '_tc_key'
// meta so build-page.php can find it.
require_once ABSPATH . 'wp-admin/includes/image.php';
$up = wp_upload_dir();
$photos = json_decode( file_get_contents( $up['basedir'] . '/tc-source/photos.json' ), true );

// key => [file name (without extension), title, alt text]
$meta = [
	// 'about-example' => [ 'tc-about-example', 'Example title', 'Describe the photo for screen readers' ],
];

$out = [];
foreach ( $photos as $key => $b64 ) {
	[ $name, $title, $alt ] = $meta[ $key ];
	$im = new Imagick();
	$im->readImageBlob( base64_decode( $b64 ) );
	$im->autoOrient();
	$im->stripImage();
	$w = $im->getImageWidth(); $h = $im->getImageHeight();
	if ( max( $w, $h ) > 1600 ) {
		if ( $w >= $h ) $im->resizeImage( 1600, 0, Imagick::FILTER_LANCZOS, 1 );
		else $im->resizeImage( 0, 1600, Imagick::FILTER_LANCZOS, 1 );
	}
	$im->setImageFormat( 'webp' );
	$q = 82;
	do {
		$c = clone $im; $c->setImageCompressionQuality( $q ); $c->setOption( 'webp:method', '6' );
		$blob = $c->getImageBlob(); $c->clear(); $q -= 6;
	} while ( strlen( $blob ) >= 400 * 1024 && $q > 30 );
	$dest = $up['path'] . '/' . $name . '.webp';
	file_put_contents( $dest, $blob );
	$aid = wp_insert_attachment( [ 'post_mime_type' => 'image/webp', 'post_title' => $title, 'post_status' => 'inherit' ], $dest );
	$md  = wp_generate_attachment_metadata( $aid, $dest );
	wp_update_attachment_metadata( $aid, $md );
	update_post_meta( $aid, '_wp_attachment_image_alt', $alt );
	update_post_meta( $aid, '_tc_key', $key );
	$out[ $key ] = [ 'id' => $aid, 'orig' => "{$w}x{$h}", 'final' => $md['width'] . 'x' . $md['height'], 'kb' => round( filesize( $dest ) / 1024 ), 'quality' => $q + 6 ];
	$im->clear();
}
unlink( $up['basedir'] . '/tc-source/photos.json' );
return $out;
