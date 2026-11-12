"""Chiron Leadership: Home page (DRAFT copy, awaiting John's approval; no "seo" block, so it stays a draft).
Run: python3 home.py -> home_payload.json
"""
from site_lib import *
import site_lib, json, glob, os

SLUG = "home"
site_lib.PAGE[0] = SLUG
BOOK = "https://calendly.com/john-chironleadership"  # Chiron Calendly booking page (John, 12 Nov 2026)

hero = section(["tc-section-navy", "tc-section-intro", "tc-section"], [
    box(["tc-banner-inner"], [
        para("Sports · Life · Executives · Entrepreneurs", "tc-eyebrow-on-navy", "tc-eyebrow"),
        heading("Every Hero Needs a Coach", "h1", "tc-banner-title"),
        para("Coaching heroes since Achilles.", "tc-tagline"),
        para("One-to-one online coaching with John Evans for athletes and coaches, life coaching clients, "
             "executives and business owners. High standards, fused with the right plan and the right process, "
             "done consistently and measured over time.", "tc-banner-lead"),
        box(["tc-action-row"], [
            button("Book a discovery call", BOOK, "tc-button-gold", "tc-button"),
            button("Meet John", "/about/", "tc-button-on-navy", "tc-button"),
        ]),
    ]),
], "hero")

programs = [
    ("Sports Coaching & Performance", "For coaches and athletes who want better performance and results on the field, "
     "including personal training.", "From $150 a month", "/sports-performance-coaching/"),
    ("Life Coaching", "Self-development and financial literacy: budgeting, debt payoff, money habits "
     "and goal setting.", "From $250 a month", "/life-coaching/"),
    ("Executive Coaching", "Leadership coaching for executives who want their team to follow them, "
     "not just report to them.", "From $350 a month", "/executive-coaching/"),
    ("Entrepreneurs & Business Owners", "Coaching to drive your business forward, from a coach who has founded "
     "four businesses and sold two.", "From $450 a month", "/business-owner-coaching/"),
]
program_sec = section(["tc-section"], [
    box(["tc-section-head"], [
        para("Coaching programs", "tc-eyebrow"),
        heading("Four Ways to Work With John", "h2", "tc-title-section"),
        para("Every program is one-to-one, online and built around your goals. Choose the one that fits where you "
             "want to win.", "tc-text-lead"),
    ]),
    box(["tc-card-list"], [
        box(["tc-card-audience"], [
            heading(t, "h3", "tc-title-card"),
            para(d, "tc-text-body"),
            para(price, "tc-detail-title"),
            link_arrow("Explore the program", href),
        ]) for t, d, price, href in programs
    ]),
], "programs")

steps = [
    ("Watch", "Watch John's short introduction to the program you're interested in."),
    ("Talk", "Book a free 30-minute discovery call to talk through your goals and see if it's the right fit."),
    ("Plan", "Agree your short-, medium- and long-term goals and the process to reach them."),
    ("Work", "Meet for one-hour sessions on Zoom: weekly, twice a month or monthly."),
]
how = section(["tc-section-navy", "tc-section"], [
    box(["tc-section-head"], [
        para("How it works", "tc-eyebrow-on-navy", "tc-eyebrow"),
        heading("From First Call to Results", "h2", "tc-title-on-navy", "tc-title-section"),
    ]),
    box(["tc-step-list"], [
        box(["tc-step"], [
            para(str(i), "tc-step-number"),
            heading(t, "h3", "tc-title-on-navy", "tc-title-card"),
            para(d, "tc-text-on-navy", "tc-text-body"),
        ]) for i, (t, d) in enumerate(steps, 1)
    ]),
], "how")

john = section(["tc-section"], [
    box(["tc-feature"], [
        box(["tc-feature-copy"], [
            para("Meet your coach", "tc-eyebrow"),
            heading("John Evans", "h2", "tc-title-section"),
            para("Originally from England, John has been coaching since 1999. He holds a U.S. Soccer National C "
                 "Coaching License and a BA (Hons) in Sport Development with Physical Education, coaches at the "
                 "Hartford Athletic Youth Academy and in the CJSA Olympic Development Program, and has worked with "
                 "Major League Soccer.", "tc-text-body"),
            para("Off the field, he has founded four businesses, two of which he sold, and led teams of up to 30 "
                 "people. He coaches the individual: no two people start in the same place.", "tc-text-body"),
            link_arrow("Read John's story", "/about/"),
        ]),
    ]),
], "john")

facts = [
    ("One-hour sessions", "Online on Zoom, wherever you are."),
    ("Monthly plans", "Weekly, twice a month or once a month."),
    ("3-month minimum", "Then month to month. Save 10% when you pay 3 months upfront."),
    ("Teams and companies", "Online groups of up to 10, and in-person programs for larger groups."),
]
plans = section(["tc-section-raised", "tc-section-tight", "tc-section"], [
    box(["tc-section-head"], [
        para("Plans at a glance", "tc-eyebrow"),
        heading("Simple, Monthly Coaching", "h2", "tc-title-section"),
    ]),
    box(["tc-fact-list"], [
        box(["tc-fact"], [heading(t, "h3", "tc-fact-title"), para(d, "tc-text-body")]) for t, d in facts
    ]),
    link_arrow("See all plans and prices", "/plans/"),
], "plans")

booking = section(["tc-section-booking", "tc-section"], [
    box(["tc-booking"], [
        box(["tc-booking-copy"], [
            heading("Ready to Raise Your Standards?", "h2", "tc-title-section"),
            para("Book a free 30-minute discovery call. We'll talk about your goals and whether coaching with "
                 "Chiron Leadership is the right fit for you.", "tc-text-body"),
        ]),
        button("Book a discovery call", BOOK, "tc-button-primary", "tc-button"),
    ]),
], "booking")

page = {"title": "Home", "slug": SLUG,
        "titles": ["Hero", "Programs", "How it works", "Meet John", "Plans at a glance", "Booking band"],
        "elements": [hero, program_sec, how, john, plans, booking]}

defined = {c["label"] for c in CLASSES}
used = set()
def walk(e):
    used.update(e["settings"].get("classes", {}).get("value", []))
    for c in e["elements"]:
        walk(c)
for e in page["elements"]:
    walk(e)
assert used <= defined, used - defined
svgs = {os.path.basename(f): open(f).read() for f in glob.glob("../assets/svg/*.svg")}
json.dump({"classes": CLASSES, "pages": [page], "svgs": svgs}, open(f"{SLUG}_payload.json", "w"))
print(SLUG, "payload written; classes used", len(used), "of", len(defined))
