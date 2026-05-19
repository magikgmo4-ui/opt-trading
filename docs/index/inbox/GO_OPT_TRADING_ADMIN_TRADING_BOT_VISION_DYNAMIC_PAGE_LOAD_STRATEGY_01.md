---
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_BOT_VISION_DYNAMIC_PAGE_LOAD_STRATEGY_01
surface: ADMIN_TRADING
source_kind: inbox
updated_at: 2026-05-19
---

# GO_OPT_TRADING_ADMIN_TRADING_BOT_VISION_DYNAMIC_PAGE_LOAD_STRATEGY_01

## Resume

Implementation d'une strategie de chargement configurable par profil pour `capture_headless.js`, puis smoke manuel XAU/Coinglass.

## Etat 2026-05-19

- Branche : `go/GO_OPT_TRADING_ADMIN_TRADING_BOT_VISION_DYNAMIC_PAGE_LOAD_STRATEGY_01`.
- Base : `85661ed0 docs: smoke bot vision p0 screenshot pages`.
- Code modifie : `modules/bot_vision/headless_capture/capture_headless.js`.
- Profil dynamic smoke : `modules/bot_vision/headless_capture/profiles.p0.dynamic.smoke.local.json`.
- `profiles.example.json` non modifie.
- `npm run check` : `playwright:OK`.
- Aucun restart, aucun `.env`, aucun trade.

## Resultat

| Page ID | Resultat |
| --- | --- |
| `tv_btc_h1` | PASS dans Smoke A, timeout intermittent dans Smoke B |
| `tv_xau_h1` | PNG/JSON/ingestion/extraction dans Smoke A, mais spinner non lisible |
| `cg_btc_flow` | timeout `domcontentloaded`, aucun artefact |

## Decision

Ne pas promouvoir le profil P0 vers le timer. Il faut un GO supplementaire pour fallback apres timeout, skip JSON bloque propre, ou URL/strategie alternative.

## Point de reprise

```text
docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_BOT_VISION_DYNAMIC_PAGE_LOAD_STRATEGY_01/00_INITIAL_PROJECT_DOC.md
```

Verdict courant : `BLOCKED_WITH_REASON_DYNAMIC_LOAD_PARTIAL_XAU_SPINNER_COINGLASS_TIMEOUT`.
