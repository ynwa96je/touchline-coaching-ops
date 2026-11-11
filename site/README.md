# Touchline Coaching website build kit

Same build method as John's other site, with Touchline's own brand: Elementor 4 atomic pages on WordPress +
Astra, hosted on Hostinger. Temporary address: https://lightgoldenrodyellow-lemur-230998.hostingersite.com

## Binding build rules (from John's brief)
- Elementor 4 **atomic elements only** (e-flexbox, e-heading, e-paragraph, e-button, e-image, e-svg).
  No HTML widget anywhere, and no shortcode to embed markup.
- **Page content only.** The header and footer are built in Astra's Header/Footer Builder.
- Every style lives in an **Elementor global class**, an **Elementor global variable**, or the element's own
  settings. No stylesheet, no Additional CSS, no child theme. If a style cannot be expressed that way, tell
  John instead of writing CSS.
- Every colour and font is a global variable (`design-tokens.json`); every repeated style is a global class
  (`build/site_lib.py`, prefix `tc-`). Reference those; never set values on individual elements.
- **Set colour explicitly on any class that styles a heading.**
- **Photos:** WebP, longest edge at most 1600px, under 400 KB, converted **on the server**
  (`server/convert-photos.php`). Never upload a photo over 400 KB. Logos and anything with transparency stay PNG.
- **Real image widgets** for photos; never a photo as a background on an empty container; never leave a
  container empty (a deliberately empty form slot is the one exception, and John must be told where it is).
- Every page: template **Elementor Full Width**; Astra per-page settings full-width container, no sidebar,
  title hidden (build-pages.php sets these).
- Responsive behaviour uses Elementor's per-device controls (tablet ≤1024px, mobile ≤767px).
- Children: no child's name or photo without written parental consent (see ../business/safeguarding.md).

## Before the first build (one-time setup on the Touchline site)
1. In WordPress: install and activate **Astra** (theme) and **Elementor** (version 4.x, free). The site's MCP
   server is the `touchline-website` entry in the repo's `.mcp.json` (cowboy-mcp plugin). The server scripts
   here were written for a PHP-execution and upload-link ability set; check which abilities `touchline-website`
   offers and adapt the upload/run steps to them.
2. Agree the brand with John: replace the starter values in `design-tokens.json` (colours and two fonts),
   then upload it to `wp-content/uploads/tc-source/design-tokens.json` and run `server/setup-design-system.php`.
3. Design the pages (John's design export if he has one, otherwise propose a design for approval first).

## Building a page
1. Copy `build/page_template.py` to `build/<slug>.py`; write the sections with the helpers in `site_lib.py`
   (`section`, `box`, `heading`, `para`, `button`, `image`, `svg`, `bullets`, `numbered`, `faq_section`, ...).
   Add or change classes only in `site_lib.py`.
2. `cd build && python3 <slug>.py` writes `<slug>_payload.json` ({classes, pages}).
3. Upload it to `wp-content/uploads/tc-source/bundle.json` (Novamira create-upload-link + `curl -X PUT`),
   then run `server/build-pages.php` through Novamira execute-php. It saves the **whole** class set every
   time (keep every class in `site_lib.py`), creates or updates the page, and applies the template settings.
   Pages are drafts until the payload has an approved `seo` block, which publishes them.
4. Check with `node verification/check.js <url> <prefix>` at 1440 / 834 / 390px, clear the Hostinger cache
   (`rest_do_request(new WP_REST_Request('DELETE','/hostinger-tools-plugin/v1/clear-cache'))` as an admin),
   and commit the page script.

## Photos
Upload `{ "<key>": "<base64 original>" }` to `wp-content/uploads/tc-source/photos.json`, fill `$meta` (file
name, title, alt text) in `server/convert-photos.php`, run it. Each attachment gets a `_tc_key` meta that page
scripts reference as `image("<key>", "large", ...)`.

## Known limits of the method (accepted on John's other site)
- Hover effects where hovering one element restyles another are not expressible in classes.
- `prefers-reduced-motion` and `:focus-within` rules are not expressible.
- Size/spacing variables need Elementor Pro, so sizes are literal values inside classes.
- Astra's mobile header switches at 921px.
