# 90_CLOSEOUT — GO_OPT_TRADING_COLLECTORS_BOT_VISION_PARENT_01

## Statut

**INVALIDÉ** — ce closeout a été révoqué. PF_BOT_VISION_HEADLESS reste `OPEN /
ACTIVE_EXPANSION`.

La fermeture initiale était prématurée : elle ne couvrait que des briques
historiques de capture/runtime, pas le pipeline produit complet visé jusqu'à
DeskPro.

## Workstream bot_vision_headless

11 GO totaux sous le workstream admin-trading, dont 4 child GOs principaux directement
rattachés à cette surface produit :

| # | GO | Rôle |
|---|---|---|
| 1 | `...BOT_VISION_HEADLESS_IMPL_01` | capture_headless.js, Playwright 1.59.1, Chromium 147, atomic write |
| 2 | `...BOT_VISION_HEADLESS_SYSTEMD_01` | Timer 10 min + 30s jitter, oneshot |
| 3 | `...INTEGRATION_SMOKE_01` | Pipeline complet automatique, 10+ cycles, desk_bridge exit 0 |
| 4 | `...BRIDGE_GUARD_ADD_01` | 3 guards anti 0-byte/.uploading |
| 5 | `...STATUS_AWARE_INGESTION_GATE_01` | Skip blocked/invalid → rejected/ + orphan cleanup |

## Modules runtime

- `modules/bot_vision/headless_capture/` — Playwright-based headless capture
- `modules/bot_vision_step2/` — Operational capture point (systemd)
- `modules/vision_bot/` — Inbox/outbox processor
- `modules/bot_vision/` — Legacy step1, preserved

## Établi

- Headless capture: Node.js + Playwright + Chromium, atomic writes
- Automation: systemd timer every 10 min
- Bridge: Desk Pro integration with anti-corruption guards
- Premier run texte / premières preuves faibles sur la chaîne vision

## Gaps restants avant close gate parent

| Gap | Priorité |
|---|---|
| Catalogue canonique des inputs | P1 |
| Spécification de capture (viewport/sections/multi-capture) | P1 |
| Spécification d'analyse structurée | P1 |
| Matrice outputs/payloads | P1 |
| Schéma max data out vers Data Center | P1 |
| Contrat de consommation DeskPro | P1 |

## Reprise valide

Le prochain GO de cadrage est
`GO_OPT_TRADING_BOT_VISION_HEADLESS_CHILD_INPUT_CAPTURE_ANALYSIS_OUTPUT_PIPELINE_01`.
