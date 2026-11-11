"""Shared global class definitions and element helpers
for the Touchline Coaching website (Elementor v4 atomic elements).
Same component system as John's other site; colours and fonts come from the site's own global variables
(see ../design-tokens.json), so the brand is Touchline's own.

Output: <page>_payload.json  { "classes": [...], "page": {...} }
Classes are written as CSS declaration strings per breakpoint/state;
the server converts them to atomic props with Elementor's own CSS converter.
Colours and fonts reference global variables via var(--label).
"""
import json, hashlib

# ---------------------------------------------------------------- classes
# Order matters: Elementor gives classes EARLIER in the list higher priority.
# So modifier classes (on-navy, feature, ...) come first, base classes after.
CLASSES = []

def cls(label, desktop, tablet=None, mobile=None, hover=None, mobile_hover=None):
    CLASSES.append({
        "label": label,
        "variants": {k: v for k, v in {
            "desktop": desktop, "tablet": tablet, "mobile": mobile,
            "desktop:hover": hover,
        }.items() if v},
    })

TRANS = "transition: background-color 180ms ease-out, border-color 180ms ease-out, color 180ms ease-out, transform 180ms ease-out;"
LIFT = "transform: translateY(-3px);"
P0 = "padding: 0px;"
SANS = "font-family: var(--font-sans);"
SERIF = "font-family: var(--font-serif);"

# ---- modifiers (highest priority first)
cls("tc-card-feature",
    "flex: 1 1 100%; background-color: var(--color-navy); border-color: var(--color-navy);",
    hover="background-color: var(--color-navy); border-color: var(--color-brass);")
cls("tc-eyebrow-on-navy", "color: var(--color-brass);")
cls("tc-title-on-navy", "color: var(--color-on-navy);")
cls("tc-text-on-navy", "color: var(--color-on-navy);")
cls("tc-bullet-item-on-navy", "color: var(--color-on-navy);")
cls("tc-link-arrow-on-navy", "color: var(--color-brass);", hover="color: var(--color-brass);")
cls("tc-icon-box-on-navy", "background-color: var(--color-navy-raised); color: var(--color-brass);")
cls("tc-callout-text", "color: var(--color-navy);")
cls("tc-button-primary",
    "background-color: var(--color-pitch); border-color: var(--color-pitch); color: var(--color-on-pitch);",
    mobile="flex: 1 1 100%;",
    hover="background-color: var(--color-pitch-hover); border-color: var(--color-pitch-hover); color: var(--color-on-pitch);")
cls("tc-button-on-navy",
    "background-color: var(--color-transparent); border-color: var(--color-on-navy); color: var(--color-on-navy);",
    mobile="flex: 1 1 100%;",
    hover="background-color: var(--color-navy-raised); border-color: var(--color-on-navy); color: var(--color-on-navy);")
cls("tc-section-navy", "background-color: var(--color-navy); color: var(--color-on-navy);")
cls("tc-section-raised",
    "background-color: var(--color-surface); border-width: 1px 0px 1px 0px; border-style: solid; border-color: var(--color-line);")
cls("tc-section-booking",
    "background-color: var(--color-pitch-soft); padding-top: 64px; padding-bottom: 64px;",
    tablet="padding-top: 48px; padding-bottom: 48px;",
    mobile="padding-top: 40px; padding-bottom: 40px;")
cls("tc-section-tight",
    "padding-top: 64px; padding-bottom: 64px;",
    tablet="padding-top: 48px; padding-bottom: 48px;",
    mobile="padding-top: 40px; padding-bottom: 40px;")

cls("tc-card-principle", "flex: 1 1 220px;", tablet="flex: 1 1 300px;", mobile="flex: 1 1 100%;")
cls("tc-section-intro",
    "padding-top: 80px; padding-bottom: 64px;",
    tablet="padding-top: 64px; padding-bottom: 48px;",
    mobile="padding-top: 40px; padding-bottom: 40px;")
cls("tc-gallery-wide", "flex: 2 1 220px;", mobile="flex: 2 1 140px;")
cls("tc-photo-top", "object-position: top center;")
cls("tc-caption-on-navy", "color: var(--color-on-navy-muted);")

cls("tc-text-on-navy-muted", "color: var(--color-on-navy-muted);")

cls("tc-pill-active",
    "background-color: var(--color-navy); border-color: var(--color-navy); color: var(--color-on-navy);",
    hover="background-color: var(--color-navy); border-color: var(--color-navy); color: var(--color-on-navy);")
cls("tc-tag-on-navy", "background-color: var(--color-navy-raised); color: var(--color-brass);")

# ---- sections and containers
cls("tc-section",
    f"display: flex; flex-direction: row; justify-content: center; width: 100%; padding: 96px 32px; "
    f"background-color: var(--color-paper); color: var(--color-slate); {SANS} font-size: 17px; font-weight: 400; line-height: 1.65;",
    tablet="padding: 64px 32px;",
    mobile="padding: 48px 16px;")
cls("tc-wrap",
    f"display: flex; flex-direction: column; gap: 48px; width: 100%; max-width: 1200px; {P0}",
    mobile="gap: 32px;")
cls("tc-section-head",
    f"display: flex; flex-direction: column; gap: 12px; max-width: 68ch; {P0}")

# ---- type
cls("tc-eyebrow",
    f"{SANS} font-size: 13px; font-weight: 600; line-height: 1.25; letter-spacing: 0.14em; text-transform: uppercase; color: var(--color-brass-deep); margin: 0px;")
cls("tc-banner-title",
    f"{SERIF} font-size: 76px; font-weight: 600; line-height: 1.1; letter-spacing: -0.01em; color: var(--color-on-navy); max-width: 12ch; margin: 0px;",
    tablet="font-size: 58px;",
    mobile="font-size: 44px;")
cls("tc-title-section",
    f"{SERIF} font-size: 30px; font-weight: 600; line-height: 1.27; color: var(--color-navy); margin: 0px; {TRANS}",
    mobile="font-size: 26px;")
cls("tc-title-card",
    f"{SERIF} font-size: 22px; font-weight: 600; line-height: 1.27; color: var(--color-navy); margin: 0px; {TRANS}",
    mobile="font-size: 20px;")
cls("tc-fact-title",
    f"{SERIF} font-size: 22px; font-weight: 600; line-height: 1.27; color: var(--color-navy); margin: 0px; {TRANS}",
    mobile="font-size: 20px;")
cls("tc-step-number",
    f"{SERIF} font-size: 34px; font-weight: 600; line-height: 1.1; color: var(--color-brass); margin: 0px; {TRANS}")
cls("tc-text-lead",
    f"{SANS} font-size: 19px; line-height: 1.65; max-width: 68ch; margin: 0px;",
    mobile="font-size: 18px;")
cls("tc-text-body",
    f"{SANS} font-size: 17px; line-height: 1.65; max-width: 68ch; margin: 0px;")
cls("tc-banner-lead",
    f"{SANS} font-size: 19px; line-height: 1.65; color: var(--color-on-navy); max-width: 52ch; margin: 0px;")
cls("tc-banner-note",
    f"{SANS} font-size: 15px; line-height: 1.65; color: var(--color-on-navy-muted); margin: 0px;")
cls("tc-inline-label", "margin: 0px;")

# ---- buttons and links
cls("tc-button",
    f"display: inline-flex; align-items: center; justify-content: center; gap: 8px; min-height: 44px; padding: 12px 24px; "
    f"border-width: 1px; border-style: solid; border-radius: 4px; {SANS} font-size: 16px; font-weight: 600; line-height: 1.25; "
    f"text-decoration: none; cursor: pointer;")
cls("tc-action-row",
    f"display: flex; flex-direction: row; flex-wrap: wrap; align-items: center; gap: 16px; {P0}")
cls("tc-link-arrow",
    f"display: inline-flex; flex-direction: row; align-items: center; gap: 8px; width: auto; min-height: 44px; {P0} "
    f"{SANS} font-size: 16px; font-weight: 600; line-height: 1.25; color: var(--color-pitch); text-decoration: none;",
    hover="color: var(--color-pitch-hover); text-decoration: underline;")

# ---- icons
cls("tc-icon", "display: flex; width: 24px; height: 24px; flex: 0 0 auto;")
cls("tc-icon-small", "display: flex; width: 20px; height: 20px; flex: 0 0 auto;")
cls("tc-icon-box",
    f"display: flex; align-items: center; justify-content: center; flex: 0 0 auto; width: 48px; height: 48px; {P0} "
    f"border-radius: 4px; background-color: var(--color-pitch-soft); color: var(--color-pitch); {TRANS}")

# ---- banner (photo is a real image element under a scrim container that holds the copy)
cls("tc-banner",
    f"position: relative; display: flex; flex-direction: row; align-items: stretch; width: 100%; min-height: 680px; {P0} "
    f"overflow: hidden; background-color: var(--color-navy); color: var(--color-on-navy); {SANS} font-size: 17px; line-height: 1.65;",
    tablet="min-height: 560px;",
    mobile="min-height: 620px;")
cls("tc-banner-photo",
    "position: absolute; top: 0px; left: 0px; width: 100%; height: 100%; object-fit: cover; object-position: center center; z-index: 0;")
cls("tc-banner-scrim",
    "position: relative; z-index: 1; display: flex; flex-direction: row; align-items: center; justify-content: center; "
    "flex: 1 1 100%; width: 100%; padding: 80px 32px; "
    "background-image: linear-gradient(90deg, var(--color-scrim-strong) 0%, var(--color-scrim-soft) 100%);",
    tablet="padding: 64px 32px;",
    mobile="align-items: flex-end; padding: 48px 16px; "
           "background-image: linear-gradient(0deg, var(--color-scrim-mobile) 0%, var(--color-scrim-mobile) 100%);")
cls("tc-banner-inner",
    f"display: flex; flex-direction: column; align-items: flex-start; gap: 24px; width: 100%; max-width: 1200px; {P0}",
    mobile="gap: 20px;")

# ---- facts strip
cls("tc-fact-list", f"display: flex; flex-direction: row; flex-wrap: wrap; gap: 32px; {P0}", mobile="gap: 24px;")
cls("tc-fact",
    f"display: flex; flex-direction: column; gap: 8px; flex: 1 1 220px; padding: 20px 0px 0px 0px; "
    f"border-width: 1px 0px 0px 0px; border-style: solid; border-color: var(--color-brass); {TRANS}",
    tablet="flex: 1 1 300px;",
    mobile="flex: 1 1 100%;",
    hover="border-color: var(--color-pitch);")

# ---- cards
cls("tc-card-list", f"display: flex; flex-direction: row; flex-wrap: wrap; gap: 32px; {P0}", mobile="gap: 24px;")
cls("tc-card-service",
    "display: flex; flex-direction: column; align-items: flex-start; gap: 12px; flex: 1 1 320px; padding: 24px; "
    f"background-color: var(--color-surface); border-width: 1px; border-style: solid; border-color: var(--color-line); border-radius: 8px; {TRANS}",
    mobile="flex: 1 1 100%;",
    hover=f"background-color: var(--color-pitch-soft); border-color: var(--color-pitch); {LIFT}")
cls("tc-card-audience",
    "display: flex; flex-direction: column; gap: 16px; flex: 1 1 420px; padding: 24px; "
    f"background-color: var(--color-surface); border-width: 1px; border-style: solid; border-color: var(--color-line); border-radius: 8px; {TRANS}",
    tablet="flex: 1 1 300px;",
    mobile="flex: 1 1 100%;",
    hover=f"background-color: var(--color-pitch-soft); border-color: var(--color-pitch); {LIFT}")
cls("tc-card-navy",
    "display: flex; flex-direction: column; gap: 16px; flex: 1 1 420px; padding: 32px; "
    f"background-color: var(--color-navy); color: var(--color-on-navy); border-width: 1px; border-style: solid; border-color: var(--color-transparent); border-radius: 8px; {TRANS}",
    tablet="flex: 1 1 300px; padding: 24px;",
    mobile="flex: 1 1 100%; padding: 24px;",
    hover=f"background-color: var(--color-navy); border-color: var(--color-brass); {LIFT}")
cls("tc-photo-card",
    "width: 100%; height: 280px; object-fit: cover; object-position: center center; border-radius: 4px;",
    mobile="height: 220px;")
cls("tc-bullet-list", f"display: flex; flex-direction: column; gap: 8px; {P0}")
cls("tc-bullet-item", f"display: flex; flex-direction: row; align-items: flex-start; gap: 12px; {P0}")
cls("tc-bullet-dot", "display: flex; width: 6px; height: 6px; flex: 0 0 auto; margin-top: 12px; color: var(--color-brass);")
cls("tc-card-illustration",
    "display: flex; flex-direction: row; width: 100%; margin-top: auto; padding: 24px 0px 0px 0px;")
cls("tc-illustration", "display: flex; width: 100%; height: 200px;", mobile="height: 150px;")
cls("tc-callout",
    "display: flex; flex-direction: row; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 16px; padding: 24px; "
    f"border-radius: 8px; background-color: var(--color-brass-soft); border-width: 1px; border-style: solid; border-color: var(--color-line); {TRANS}",
    hover="background-color: var(--color-pitch-soft); border-color: var(--color-pitch);")

# ---- steps
cls("tc-step-list", f"display: flex; flex-direction: row; flex-wrap: wrap; gap: 32px; {P0}", mobile="gap: 24px;")
cls("tc-step",
    "display: flex; flex-direction: column; gap: 12px; flex: 1 1 220px; padding: 20px 0px 0px 0px; "
    f"border-width: 1px 0px 0px 0px; border-style: solid; border-color: var(--color-navy-line); {TRANS}",
    tablet="flex: 1 1 300px;",
    mobile="flex: 1 1 100%;",
    hover="border-color: var(--color-brass);")

# ---- founder feature
cls("tc-feature",
    f"display: flex; flex-direction: row; flex-wrap: wrap; align-items: center; gap: 64px; {P0}",
    tablet="gap: 48px;",
    mobile="gap: 32px; align-items: flex-start;")
cls("tc-photo-portrait",
    "flex: 0 0 auto; width: 240px; height: 240px; object-fit: cover; object-position: top center; "
    "border-radius: 999px; border-width: 2px; border-style: solid; border-color: var(--color-brass);",
    tablet="width: 160px; height: 160px;",
    mobile="width: 160px; height: 160px;")
cls("tc-feature-copy",
    f"display: flex; flex-direction: column; align-items: flex-start; gap: 16px; flex: 1 1 420px; {P0}")

# ---- split
cls("tc-split",
    f"display: flex; flex-direction: row; flex-wrap: wrap; align-items: center; gap: 64px; {P0}",
    tablet="gap: 48px;",
    mobile="gap: 32px;")
cls("tc-split-media", f"display: flex; flex-direction: row; flex: 1 1 420px; {P0}")
cls("tc-split-copy",
    f"display: flex; flex-direction: column; align-items: flex-start; gap: 16px; flex: 1 1 420px; {P0}")
cls("tc-photo-band",
    "width: 100%; height: 460px; object-fit: cover; object-position: center center; border-radius: 8px;",
    mobile="height: 280px;")

# ---- booking band
cls("tc-booking",
    f"display: flex; flex-direction: row; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 32px; {P0}")
cls("tc-booking-copy", f"display: flex; flex-direction: column; gap: 12px; flex: 1 1 420px; {P0}")

# ---- page title (inner pages)
cls("tc-title-page",
    f"{SERIF} font-size: 44px; font-weight: 600; line-height: 1.1; letter-spacing: -0.01em; color: var(--color-navy); margin: 0px;",
    tablet="font-size: 38px;",
    mobile="font-size: 33px;")

# ---- intro (inner pages)
cls("tc-intro",
    f"display: flex; flex-direction: row; flex-wrap: wrap; align-items: center; gap: 64px; {P0}",
    tablet="gap: 48px;",
    mobile="gap: 32px;")
cls("tc-intro-copy",
    f"display: flex; flex-direction: column; gap: 20px; flex: 1 1 540px; {P0}",
    tablet="flex: 1 1 380px;",
    mobile="flex: 1 1 100%;")
cls("tc-intro-media",
    f"display: flex; flex-direction: row; flex: 1 1 420px; {P0}",
    tablet="flex: 1 1 300px;",
    mobile="flex: 1 1 100%;")
cls("tc-photo-intro",
    "width: 100%; height: 460px; object-fit: cover; object-position: top center; border-radius: 8px;",
    mobile="height: 300px;")

# ---- story and milestones (about)
cls("tc-story",
    f"display: flex; flex-direction: row; flex-wrap: wrap; gap: 64px; {P0}",
    tablet="gap: 48px;",
    mobile="gap: 32px;")
cls("tc-story-copy", f"display: flex; flex-direction: column; gap: 16px; flex: 3 1 420px; {P0}")
cls("tc-milestone-list", f"display: flex; flex-direction: column; flex: 2 1 320px; {P0}")
cls("tc-milestone",
    "display: flex; flex-direction: row; align-items: flex-start; gap: 16px; padding: 16px 0px; "
    "border-width: 0px 0px 1px 0px; border-style: solid; border-color: var(--color-line);")
cls("tc-milestone-marker", "display: flex; width: 12px; height: 12px; flex: 0 0 auto; margin-top: 8px; color: var(--color-brass);")
cls("tc-milestone-body", f"display: flex; flex-direction: column; gap: 4px; {P0}")
cls("tc-milestone-place",
    f"{SANS} font-size: 13px; font-weight: 600; line-height: 1.25; letter-spacing: 0.14em; text-transform: uppercase; color: var(--color-brass-deep); margin: 0px;")
cls("tc-milestone-text",
    f"{SERIF} font-size: 22px; font-weight: 600; line-height: 1.27; color: var(--color-navy); margin: 0px; {TRANS}",
    mobile="font-size: 20px;")
cls("tc-milestone-note",
    f"{SANS} font-size: 15px; font-weight: 600; line-height: 1.25; color: var(--color-pitch); margin: 0px;")

# ---- gallery
cls("tc-gallery", f"display: flex; flex-direction: row; flex-wrap: wrap; gap: 16px; {P0}")
cls("tc-gallery-item",
    f"display: flex; flex-direction: column; gap: 8px; flex: 1 1 220px; {P0}",
    mobile="flex: 1 1 140px;")
cls("tc-photo-gallery",
    "width: 100%; height: 280px; object-fit: cover; object-position: center center; border-radius: 8px; "
    f"outline-width: 2px; outline-style: solid; outline-color: var(--color-transparent); outline-offset: 2px; {TRANS}",
    mobile="height: 180px;",
    hover="outline-color: var(--color-brass);")
cls("tc-caption", f"{SANS} font-size: 15px; line-height: 1.65; color: var(--color-slate-muted); margin: 0px; {TRANS}")
cls("tc-badge-tile",
    "display: flex; flex-direction: row; align-items: center; justify-content: center; width: 100%; height: 280px; padding: 32px; "
    "background-color: var(--color-surface); border-radius: 8px;",
    mobile="height: 180px; padding: 16px;")
cls("tc-photo-badge", "width: 100%; height: 100%; object-fit: contain; object-position: center center;")

# ---- services
cls("tc-pill-list", f"display: flex; flex-direction: row; flex-wrap: wrap; gap: 12px; {P0}", mobile="gap: 8px;")
cls("tc-pill",
    f"display: inline-flex; align-items: center; min-height: 44px; padding: 8px 16px; border-width: 1px; border-style: solid; "
    f"border-color: var(--color-slate-muted); border-radius: 4px; background-color: var(--color-surface); color: var(--color-navy); "
    f"{SANS} font-size: 16px; font-weight: 600; line-height: 1.65; text-decoration: none; cursor: pointer; {TRANS}",
    hover="background-color: var(--color-pitch-soft); border-color: var(--color-pitch); color: var(--color-navy);")
cls("tc-photo-wide",
    "width: 100%; height: 300px; object-fit: cover; object-position: center center; border-radius: 8px;",
    mobile="height: 160px;")
cls("tc-service-list", f"display: flex; flex-direction: column; gap: 64px; {P0}", mobile="gap: 48px;")
cls("tc-service-block",
    "display: flex; flex-direction: row; flex-wrap: wrap; gap: 48px; padding: 48px 0px 0px 0px; "
    f"border-width: 1px 0px 0px 0px; border-style: solid; border-color: var(--color-line); {TRANS}",
    mobile="gap: 24px; padding: 32px 0px 0px 0px;",
    hover="border-color: var(--color-pitch);")
cls("tc-service-intro", f"display: flex; flex-direction: column; align-items: flex-start; gap: 16px; flex: 1 1 360px; {P0}")
cls("tc-service-detail", f"display: flex; flex-direction: row; flex-wrap: wrap; gap: 32px; flex: 1 1 480px; {P0}")
cls("tc-detail-col",
    "display: flex; flex-direction: column; gap: 16px; flex: 1 1 220px; padding: 24px; "
    f"background-color: var(--color-surface); border-width: 1px; border-style: solid; border-color: var(--color-line); border-radius: 8px; {TRANS}",
    mobile="padding: 20px;",
    hover=f"background-color: var(--color-pitch-soft); border-color: var(--color-pitch); {LIFT}")
cls("tc-detail-title",
    f"{SANS} font-size: 13px; font-weight: 600; line-height: 1.25; letter-spacing: 0.14em; text-transform: uppercase; color: var(--color-brass-deep); margin: 0px;")
cls("tc-service-note", f"{SANS} font-size: 15px; line-height: 1.65; color: var(--color-slate-muted); max-width: 68ch; margin: 0px;")
cls("tc-card-raised",
    "display: flex; flex-direction: column; align-items: flex-start; gap: 12px; flex: 1 1 320px; padding: 24px; "
    f"background-color: var(--color-navy-raised); border-width: 1px; border-style: solid; border-color: var(--color-transparent); border-radius: 8px; {TRANS}",
    mobile="flex: 1 1 100%;",
    hover=f"background-color: var(--color-navy-hover); border-color: var(--color-brass); {LIFT}")

# ---- resources
cls("tc-text-small", f"{SANS} font-size: 15px; line-height: 1.65; color: var(--color-slate-muted); margin: 0px;")
cls("tc-tag",
    f"display: inline-flex; align-items: center; padding: 4px 8px; border-radius: 4px; background-color: var(--color-pitch-soft); "
    f"color: var(--color-pitch); {SANS} font-size: 13px; font-weight: 600; letter-spacing: 0.14em; line-height: 1.25; text-transform: uppercase; margin: 0px;")
cls("tc-card-meta", f"display: flex; flex-direction: row; flex-wrap: wrap; align-items: center; gap: 12px; {P0}")
cls("tc-feature-card",
    "display: flex; flex-direction: row; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 32px; padding: 48px; "
    f"background-color: var(--color-navy); color: var(--color-on-navy); border-width: 1px; border-style: solid; border-color: var(--color-transparent); border-radius: 8px; {TRANS}",
    tablet="padding: 32px;",
    mobile="padding: 24px; gap: 24px;",
    hover="background-color: var(--color-navy); border-color: var(--color-brass);")
cls("tc-feature-card-copy", f"display: flex; flex-direction: column; align-items: flex-start; gap: 16px; flex: 1 1 480px; {P0}")
cls("tc-download-list", f"display: flex; flex-direction: row; flex-wrap: wrap; gap: 16px; {P0}")
cls("tc-card-download",
    "display: flex; flex-direction: row; align-items: flex-start; gap: 16px; flex: 1 1 320px; padding: 24px; "
    f"background-color: var(--color-surface); border-width: 1px; border-style: solid; border-color: var(--color-line); border-radius: 8px; "
    f"color: var(--color-slate); text-decoration: none; {TRANS}",
    mobile="flex: 1 1 100%;",
    hover=f"background-color: var(--color-pitch-soft); border-color: var(--color-pitch); color: var(--color-slate); {LIFT}")
cls("tc-download-body", f"display: flex; flex-direction: column; gap: 4px; {P0}")
cls("tc-download-title",
    f"{SERIF} font-size: 22px; font-weight: 600; line-height: 1.27; color: var(--color-navy); margin: 0px; {TRANS}",
    mobile="font-size: 20px;")
cls("tc-download-meta", f"{SANS} font-size: 15px; font-weight: 600; line-height: 1.65; color: var(--color-pitch); margin: 0px;")
cls("tc-checklist-panel",
    "display: flex; flex-direction: row; flex-wrap: wrap; gap: 48px; padding: 48px; "
    f"background-color: var(--color-surface); border-width: 1px; border-style: solid; border-color: var(--color-line); border-radius: 8px; {TRANS}",
    tablet="padding: 32px;",
    mobile="padding: 24px; gap: 24px;",
    hover="background-color: var(--color-pitch-soft); border-color: var(--color-pitch);")
cls("tc-checklist-head", f"display: flex; flex-direction: column; gap: 12px; flex: 1 1 320px; {P0}")
cls("tc-checklist", f"display: flex; flex-direction: column; gap: 12px; flex: 2 1 420px; {P0}")
cls("tc-check-item", f"display: flex; flex-direction: row; align-items: flex-start; gap: 12px; color: var(--color-slate); {P0}")
cls("tc-check-mark", "display: flex; width: 20px; height: 20px; flex: 0 0 auto; margin-top: 4px; color: var(--color-pitch);")

# ---- contact
cls("tc-contact",
    f"display: flex; flex-direction: row; flex-wrap: wrap; align-items: flex-start; gap: 48px; {P0}",
    mobile="gap: 32px;")
cls("tc-form-slot",
    "display: flex; flex-direction: column; gap: 24px; flex: 3 1 520px; padding: 32px; "
    "background-color: var(--color-surface); border-width: 1px; border-style: solid; border-color: var(--color-line); border-radius: 8px;",
    mobile="padding: 20px; gap: 20px;")
cls("tc-contact-aside", f"display: flex; flex-direction: column; gap: 32px; flex: 2 1 340px; {P0}")
cls("tc-photo-contact", "width: 100%; height: 240px; object-fit: cover; object-position: center center; border-radius: 8px;")
cls("tc-contact-card",
    "display: flex; flex-direction: column; gap: 24px; padding: 24px; "
    f"background-color: var(--color-surface); border-width: 1px; border-style: solid; border-color: var(--color-line); border-radius: 8px; {TRANS}",
    hover="background-color: var(--color-pitch-soft); border-color: var(--color-pitch);")
cls("tc-contact-item", f"display: flex; flex-direction: row; align-items: flex-start; gap: 16px; {P0}")
cls("tc-contact-item-body", f"display: flex; flex-direction: column; gap: 4px; {P0}")
cls("tc-contact-label",
    f"{SANS} font-size: 13px; font-weight: 600; line-height: 1.25; letter-spacing: 0.14em; text-transform: uppercase; color: var(--color-brass-deep); margin: 0px;")
cls("tc-photo-avatar",
    "flex: 0 0 auto; width: 64px; height: 64px; object-fit: cover; object-position: top center; border-radius: 999px;")
cls("tc-text-link", "color: var(--color-pitch); text-decoration: underline;", hover="color: var(--color-pitch-hover);")
cls("tc-next-list", f"display: flex; flex-direction: column; gap: 16px; {P0}")
cls("tc-next-item", f"display: flex; flex-direction: row; align-items: flex-start; gap: 16px; {P0}")
cls("tc-next-number",
    "display: flex; align-items: center; justify-content: center; flex: 0 0 auto; width: 48px; height: 48px; "
    f"border-width: 1px; border-style: solid; border-color: var(--color-brass); border-radius: 4px; "
    f"{SERIF} font-size: 22px; font-weight: 600; color: var(--color-navy); margin: 0px;")
# ---- guide articles (resources/*)
cls("tc-article",
    f"display: flex; flex-direction: column; gap: 48px; width: 100%; max-width: 760px; {P0}",
    mobile="gap: 40px;")
cls("tc-article-part", f"display: flex; flex-direction: column; align-items: flex-start; gap: 16px; {P0}")
# ---- FAQ
cls("tc-faq-list", f"display: flex; flex-direction: row; flex-wrap: wrap; gap: 40px; {P0}", mobile="gap: 32px;")
cls("tc-faq-item",
    "display: flex; flex-direction: column; gap: 8px; flex: 1 1 420px; padding: 24px 0px 0px 0px; "
    "border-width: 1px 0px 0px 0px; border-style: solid; border-color: var(--color-line);",
    mobile="flex: 1 1 100%;")

# ---------------------------------------------------------------- elements
_ids = set()
def eid(seed):
    h = hashlib.md5(seed.encode()).hexdigest()
    i = 0
    while h[i:i+7] in _ids:
        i += 1
    _ids.add(h[i:i+7])
    return h[i:i+7]

PAGE = ["home"]  # set per page script: site_lib.PAGE[0] = "<slug>"
_counter = [0]
def _seed(kind):
    _counter[0] += 1
    return f"{PAGE[0]}-{kind}-{_counter[0]}"

def S(v):
    return {"$$type": "string", "value": v}

def classes(*labels):
    return {"$$type": "classes", "value": list(labels)}  # labels -> ids on server

def link(path):
    return {"$$type": "link", "value": {
        "destination": {"$$type": "url", "value": "__HOME__" + path},
        "isTargetBlank": {"$$type": "boolean", "value": False},
    }}

def box(cl, children, tag=None, href=None, cssid=None):
    st = {"classes": classes(*cl)}
    if cssid:
        st["_cssid"] = S(cssid)
    if tag:
        st["tag"] = S(tag)
    if href:
        st["link"] = link(href)
        st["tag"] = S("a")
    return {"id": eid(_seed("box")), "elType": "e-flexbox", "isInner": False,
            "settings": st, "elements": children, "styles": {}, "editor_settings": {}}

def widget(wtype, st):
    return {"id": eid(_seed(wtype)), "elType": "widget", "widgetType": wtype, "isInner": False,
            "settings": st, "elements": [], "styles": {}, "editor_settings": {}}

def heading(text, tag, *cl):
    return widget("e-heading", {"classes": classes(*cl), "tag": S(tag),
                                "title": {"$$type": "escaped-html", "value": text}})

def para(text, *cl, tag="p"):
    return widget("e-paragraph", {"classes": classes(*cl), "tag": S(tag),
                                  "paragraph": {"$$type": "escaped-html", "value": text}})

def button(text, href, *cl):
    return widget("e-button", {"classes": classes(*cl), "link": link(href),
                               "text": {"$$type": "escaped-html", "value": text}})

def image(att_key, size, *cl):
    return widget("e-image", {"classes": classes(*cl), "image": {"$$type": "image", "value": {
        "src": {"$$type": "image-src", "value": {"id": {"$$type": "image-attachment-id", "value": "__ATT__" + att_key}, "url": None}},
        "size": S(size)}}})

def svg(att_key, *cl):
    return widget("e-svg", {"classes": classes(*cl), "svg": {"$$type": "svg-src", "value": {
        "id": {"$$type": "image-attachment-id", "value": "__ATT__" + att_key}, "url": None}}})

def link_arrow(text, href, on_navy=False):
    cl = ["tc-link-arrow-on-navy", "tc-link-arrow"] if on_navy else ["tc-link-arrow"]
    return box(cl, [para(text, "tc-inline-label", tag="span"),
                    svg("tc-icon-arrow-right.svg", "tc-icon-small")], href=href)

def section(cl, children, label):
    return box(cl, [box(["tc-wrap"], children)], tag="section")

def bullets(items, on_navy=False):
    item_cl = ["tc-bullet-item-on-navy", "tc-bullet-item"] if on_navy else ["tc-bullet-item"]
    return box(["tc-bullet-list"], [
        box(item_cl, [svg("tc-bullet-square.svg", "tc-bullet-dot"), para(t, "tc-text-body")])
        for t in items])


def numbered(items):
    return box(["tc-next-list"], [box(["tc-next-item"], [para(str(i), "tc-next-number", tag="span"), para(t, "tc-text-body")])
                                   for i, t in enumerate(items, 1)])

def text_link(text, url, *cl):
    return widget("e-paragraph", {"classes": classes(*cl), "tag": S("p"),
                                  "paragraph": {"$$type": "escaped-html", "value": text},
                                  "link": {"$$type": "link", "value": {
                                      "destination": {"$$type": "url", "value": url},
                                      "isTargetBlank": {"$$type": "boolean", "value": False}}}})

def faq_section(qas, sec_cl, eyebrow="Questions", title="Common questions"):
    return section(sec_cl, [
        box(["tc-section-head"], [para(eyebrow, "tc-eyebrow"), heading(title, "h2", "tc-title-section")]),
        box(["tc-faq-list"], [box(["tc-faq-item"], [heading(q, "h3", "tc-title-card"), para(a, "tc-text-body")])
                               for q, a in qas]),
    ], "faq")



FAQ = {}  # Touchline FAQ copy goes here once John approves it
