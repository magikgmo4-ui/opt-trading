---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_SIGNAL_CHAIN_TOTAL_PRODUCT_PARENT_01_SURFACE_ROLE_MATRIX
doc_type: surface_role_matrix
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_SIGNAL_CHAIN_TOTAL_PRODUCT_PARENT_01
status: open
source_kind: canonical
updated_at: 2026-05-19
links:
  - docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_RUNTIME_REVIEW_REPRISE_01/20_INPUT_CONSUMER_MAP.md
  - docs/chantiers/GO_TELEGRAM_SCREENER_CHANNEL_REGISTRY_01/10_CURRENT_INBOUND_SURFACES.md
  - docs/chantiers/GO_TELEGRAM_EVENT_ROUTING_MAP_01/00_INITIAL_PROJECT_DOC.md
---

# 02_SURFACE_ROLE_MATRIX

## MASTER_TARGET

Classifier chaque surface minimale du produit final total selon la regle `producer / consumer / both / router / storage / validation`, sans inventer de surface non prouvee.

## Matrice

| Surface | Role | Preuve locale | Note |
| --- | --- | --- | --- |
| TradingView | producer | guide pipeline + templates observer | source amont, pas verite unique |
| webhook | both | `webhook_server.py`, `modules/webhook/` | recoit et normalise |
| Desk Pro | consumer | `modules/desk_pro*`, `20_INPUT_CONSUMER_MAP.md` | hub consumer final |
| Bot Vision | producer | `modules/vision_bot/`, `modules/bot_vision_step2/` | produit captures/artefacts |
| Headless Screener | producer | `modules/bot_vision/headless_capture/` | capture headless visuelle |
| Coinglass | producer | references repo/docs presentes, inventaire detaille a poursuivre | collecteur externe a confirmer chaine fine |
| exchange/API collectors | producer | collectors references docs/repo | inventaire detaille a poursuivre |
| Telegram Screener | producer | `modules/telegram_screener/` (116 tests) + `modules/telegram_ingestion/` (62 tests) | pipeline complet : ingestion → parser → route → producer → adapter |
| Telegram Notification Dispatcher | router | `modules/notification_dispatcher/` | routage outbound structure |
| Telegram bots/chats/topics | consumer | chantier routing map | destinations, pas source canonique strategie |
| Google Sheets | consumer | `GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01`, `sync_daily_session.py` | consumer transverse seulement |
| JSONL/CSV recorder | storage | `state/events.jsonl`, `data/journal/daily/*.csv` (schema doc) | stockage/journalisation |
| Strategy Registry | validation | `95_STRATEGY_REGISTRY.md` | registre/gate transverse, pas runtime auto |
| Perf Engine | consumer | `modules/perf_engine/` | scoring/perf sur events/resultats |
| Trading Lab / replay / paper | validation | `modules/trading_lab_v1/`, docs/tests paper/backtest | validation/replay borne |
| tmux/OpenCode/OpenClaw | router | protocoles runtime et orchestration docs | surface d'execution/orchestration |
| operator phone/SSH | consumer | `30_EXECUTION_PROTOCOL.md` | point d'acces operateur |

## Invariants

- ne pas melanger `Telegram Screener` et `Telegram Notification Dispatcher`
- ne pas transformer Telegram en verite strategie
- ne pas transformer TradingView en verite unique
- ne pas promouvoir Google Sheets hors role consumer a cette passe

## Kanban bundle conserve

Le tableau Kanban du bundle reste la navigation principale. Cette matrice sert de preuve de roles, pas de substitution roadmap.

## Prochain item Kanban a faire

`TBD` (all Telegram chains now CLOSED)

## Gaps encore ouverts

- Coinglass et collectors APIs a prouver plus finement surface par surface
- role exact `both` vs `producer` de certaines surfaces vision/collectors a recroiser dans le child inventaire
- topics/bots/chats Telegram multi-destinations a formaliser dans la map de routing
