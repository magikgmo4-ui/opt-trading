---
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_BOT_VISION_P0_PAGE_SELECTION_SMOKE_01
surface: ADMIN_TRADING
source_kind: inbox
updated_at: 2026-05-19
---

# GO_OPT_TRADING_ADMIN_TRADING_BOT_VISION_P0_PAGE_SELECTION_SMOKE_01

## Resume

Smoke manuel des pages P0 via profil separe non utilise par le timer.

## Etat 2026-05-19

- Branche : `go/GO_OPT_TRADING_ADMIN_TRADING_BOT_VISION_P0_PAGE_SELECTION_SMOKE_01`.
- Base validee : audit commit `203b1cc2c`, runtime repair record commit `1777a721`.
- Playwright runtime : `playwright:OK`.
- Profil smoke separe : `modules/bot_vision/headless_capture/profiles.p0.smoke.local.json`.
- `profiles.example.json` non modifie.
- Smoke manuel execute : `2026-05-19T03:28:31-04:00` a `2026-05-19T03:29:45-04:00`.

## Resultat par page

| Page ID | Capture | Ingestion | Extraction | Lisibilite humaine | Verdict |
| --- | --- | --- | --- | --- | --- |
| `tv_btc_h1` | PASS | PASS | PASS | PASS | PASS |
| `tv_xau_h1` | BLOCKED timeout networkidle | n/a | n/a | n/a | BLOCKED |
| `cg_btc_flow` | BLOCKED timeout networkidle | n/a | n/a | n/a | BLOCKED |

## Decision

Ne pas promouvoir le profil P0 vers le timer. Corriger ou contourner le timeout `networkidle` sur pages dynamiques avant un nouveau smoke.

## Point de reprise

```text
docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_BOT_VISION_P0_PAGE_SELECTION_SMOKE_01/00_INITIAL_PROJECT_DOC.md
```

Verdict courant : `BLOCKED_WITH_REASON_PARTIAL_P0_TIMEOUT_XAU_COINGLASS`.
