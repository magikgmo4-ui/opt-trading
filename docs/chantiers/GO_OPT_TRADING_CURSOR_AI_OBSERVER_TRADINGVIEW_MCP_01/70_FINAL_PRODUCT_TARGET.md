# 70_FINAL_PRODUCT_TARGET — TradingView Desktop Observer for opt-trading

## Nom produit

**TradingView Desktop Observer for opt-trading**

## Usage final

Permettre a opt-trading/OpenClaw de voir et auditer TradingView Desktop localement, en read-only, sans pont admin-trading actif.

## Capacites finales

| # | Capacite | Statut |
|---|----------|--------|
| 1 | Lire le symbole courant | PASS |
| 2 | Lire le timeframe courant | PASS |
| 3 | Lire OHLC / quote | PASS |
| 4 | Lire indicateurs visibles | PASS (3/7 visibles en test) |
| 5 | Lister les alertes (inventaire REST API) | PASS |
| 6 | Auditer statut des alertes (active/expired) | PASS |
| 7 | Exporter JSON structure (6 fichiers) | PASS |
| 8 | Exporter bridge packet V1 (synthese) | PASS |
| 9 | Donner a OpenClaw une vue exploitable | PASS (via skill) |
| 10 | Sanity check automatise (7 checks) | PASS |
| 11 | Product sanity global (12 checks) | PASS |
| 12 | Garder admin-trading separe (webhook canonique) | PASS |

## Non-objectifs

- Pas de trading autonome.
- Pas de remplacement webhook.
- Pas de dependance a une session ChatGPT.
- Pas de port CDP expose au LAN.
- Pas de mutation de production sans GO explicite.
- Pas de pont admin-trading actif (Phase 5 = Option A).
- Pas de transfert automatise vers shared folder.

## Architecture finale

```
cursor-ai (Windows)
├── TradingView Desktop (:9222 localhost)
├── tradingview-mcp (C:\Users\ghost\.claude\tools\tradingview-mcp)
│
opt-trading repo
├── modules/tradingview_observer/          (wrapper lecteur)
│   ├── cmd.ps1                            (CLI principal)
│   ├── sanity_check.ps1                   (7 checks runtime)
│   ├── product_sanity.ps1                 (12 checks produit)
│   ├── export_bridge_packet.ps1           (bridge V1 dry-run)
│   ├── app/observer_runner.ps1            (runner export JSON)
│   ├── README.md                          (documentation operateur)
│   └── output/                            (exports JSON, ignores git)
│       ├── .gitignore
│       ├── latest_status.json
│       ├── latest_quote.json
│       ├── latest_state.json
│       ├── latest_alert_inventory.json
│       ├── latest_values.json
│       ├── latest_report.json
│       └── latest_bridge_packet.json
│
├── modules/tradingview_observer_openclaw/ (skill OpenClaw)
│   ├── run.ps1                            (orchestrateur safe)
│   ├── skill.md                           (definition allowed/forbidden)
│   └── README.md                          (usage OpenClaw)
│
admin-trading (serveur distant, NON CONNECTE)
├── webhook TradingView                    (canonique, inchange)
└── desk                                   (interface utilisateur)
```

## Definition finale de Done

- [x] Documentation complete (00-90)
- [x] Installation locale reproductible (tradingview-mcp hors repo)
- [x] Smoke PASS (Phase 1)
- [x] Alertes inventoriees (Phase 2)
- [x] Wrapper opt-trading PASS (Phase 3)
- [x] OpenClaw skill documente (Phase 4)
- [x] Bridge packet V1 defini (Phase 5)
- [x] Hardening produit PASS (Phase 6)
- [x] Product sanity 12/12 defini
- [ ] Closeout final PASS (Phase 7 — FINAL_CLOSEOUT)
- [x] Reprise possible depuis docs/chantiers uniquement

## RISKS

- À qualifier.
