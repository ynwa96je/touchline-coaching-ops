# Chiron Leadership: operating instructions for Claude

Chiron Leadership is John Evans's coaching business. This repository is for Chiron Leadership only. Never
use, read or mention anything from Evans Wealth Partners here (its clients, data, website, connectors or
compliance material), and never mix the two brands in any content.

## Business facts (John to complete in `business/about.md`; never invent details)
- What we teach, who for, where, prices, schedule: see `business/about.md`.
- Brand: **Chiron Leadership** (renamed from Touchline Coaching on 12 Nov 2026; the repository name and some
  internal technical names, such as the `tc-` class prefix, still use the old name).
- Domain: **https://chironleadership.com** (connected in Hostinger on 12 Nov 2026; WordPress home and site URL
  are https://chironleadership.com). Business email: john@chironleadership.com. The old temporary address
  lightgoldenrodyellow-lemur-230998.hostingersite.com is retired. The cloud environment is still named
  "Touchline Coaching".

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
- Calendly: session availability and booking links (check which event types belong to Chiron).
- Website: the **`novamira-chironleadership`** claude.ai connector (Novamira plugin on the Chiron site; it replaced
  `novamira-lightgoldenrodye` when the domain was connected). Use
  it for every site change; the server scripts in `site/server/` are written for its `novamira/execute-php`
  and `novamira/create-upload-link` abilities. (`.mcp.json` also defines `touchline-website`, the site's
  cowboy-mcp endpoint, as a backup.) Never use the `novamira-evanswealthpartn` connector in this repo: it is
  the other business's website.
- OpenSEO: keyword and local search research (use a separate OpenSEO project for Chiron).

## Where things are
- `site/` website build kit: rules, class library, server scripts, design tokens (read `site/README.md` first).
- `business/` targets, about, voice, safeguarding, pricing.
- `programme/` course and session design.
- `.claude/agents/` the team. Start with `chief-revenue-officer` when unsure which agent to use.
