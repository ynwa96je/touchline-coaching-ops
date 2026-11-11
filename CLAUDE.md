# Touchline Coaching: operating instructions for Claude

Touchline Coaching is John Evans's coaching business. This repository is for Touchline Coaching only. Never
use, read or mention anything from Evans Wealth Partners here (its clients, data, website, connectors or
compliance material), and never mix the two brands in any content.

## Business facts (John to complete in `business/about.md`; never invent details)
- What we teach, who for, where, prices, schedule: see `business/about.md`.
- Website: temporary address https://lightgoldenrodyellow-lemur-230998.hostingersite.com (WordPress on Hostinger).
  The permanent domain is not registered yet; update this line and the "Touchline Coaching" environment's
  allowed hosts when it is.

## Rules every agent follows
1. **Nothing leaves without John.** Agents draft; John approves and sends or publishes.
2. **Children and parents' data:** if players are under 18, collect only what is needed, keep it in the
   booking system, never in this repository, and never use children's names or photos in marketing
   without written parental consent. Follow `business/safeguarding.md`.
3. **Honest marketing:** no made-up testimonials, results or credentials. Prices and terms exactly as in
   `business/about.md`. Marketing email needs consent and an unsubscribe (CAN-SPAM; GDPR/PECR for UK contacts).
4. **Quarterly targets** live in `business/targets.md`; the `chief-revenue-officer` agent reads them first.
5. Plain, energetic, encouraging tone (see `business/voice.md`).

## Connected tools
- Calendly: session availability and booking links (check which event types belong to Touchline).
- Website: the **`novamira-lightgoldenrodye`** claude.ai connector (Novamira plugin on the Touchline site). Use
  it for every site change; the server scripts in `site/server/` are written for its `novamira/execute-php`
  and `novamira/create-upload-link` abilities. (`.mcp.json` also defines `touchline-website`, the site's
  cowboy-mcp endpoint, as a backup.) Never use the `novamira-evanswealthpartn` connector in this repo: it is
  the other business's website.
- OpenSEO: keyword and local search research (use a separate OpenSEO project for Touchline).

## Where things are
- `site/` website build kit: rules, class library, server scripts, design tokens (read `site/README.md` first).
- `business/` targets, about, voice, safeguarding, pricing.
- `programme/` course and session design.
- `.claude/agents/` the team. Start with `chief-revenue-officer` when unsure which agent to use.
