"""Template for one Chiron Leadership page. Copy to build/<slug>.py, replace the sections with approved copy,
then: python3 <slug>.py  -> <slug>_payload.json (see ../README.md for upload and build).
Pages without "seo" are created as DRAFTS by server/build-pages.php; add "seo" only when John has approved the page.
"""
from site_lib import *
import site_lib, json

SLUG = "example"
site_lib.PAGE[0] = SLUG

intro = section(["tc-section-intro", "tc-section"], [
    box(["tc-section-head"], [
        para("Eyebrow", "tc-eyebrow"),
        heading("Page title from approved copy", "h1", "tc-title-page"),
        para("Lead paragraph from approved copy.", "tc-text-lead"),
    ]),
], "intro")

booking = section(["tc-section-booking", "tc-section"], [
    box(["tc-booking"], [
        box(["tc-booking-copy"], [
            heading("Call to action heading", "h2", "tc-title-section"),
            para("One line that says what happens next.", "tc-text-body"),
        ]),
        button("Book a session", "/contact/", "tc-button-primary", "tc-button"),
    ]),
], "booking")

page = {"title": "Example", "slug": SLUG, "titles": ["Intro", "Booking band"], "elements": [intro, booking]}
# page["seo"] = {"title": "...", "description": "..."}   # only after approval: publishes the page

defined = {c["label"] for c in CLASSES}
used = set()
def walk(e):
    used.update(e["settings"].get("classes", {}).get("value", []))
    for c in e["elements"]:
        walk(c)
for e in page["elements"]:
    walk(e)
assert used <= defined, used - defined
import glob, os
# Icons used by the helpers (arrow links, bullets, ...). build-pages.php uploads any that are not on the site yet.
svgs = {os.path.basename(f): open(f).read() for f in glob.glob("../assets/svg/*.svg")}
json.dump({"classes": CLASSES, "pages": [page], "svgs": svgs}, open(f"{SLUG}_payload.json", "w"))
print(SLUG, "payload written; classes used", len(used), "of", len(defined))
