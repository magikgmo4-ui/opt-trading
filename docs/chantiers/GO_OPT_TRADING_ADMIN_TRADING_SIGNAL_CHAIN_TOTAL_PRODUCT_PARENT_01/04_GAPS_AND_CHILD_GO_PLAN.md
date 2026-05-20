---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_SIGNAL_CHAIN_TOTAL_PRODUCT_PARENT_01_GAPS_AND_CHILD_GO_PLAN
doc_type: gaps_and_child_plan
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_SIGNAL_CHAIN_TOTAL_PRODUCT_PARENT_01
status: open
source_kind: canonical
updated_at: 2026-05-20
links:
  - docs/chantiers/GO_STRATEGY_SIGNAL_MONITORING_REPO_INVENTORY_01/20_REUSE_MATRIX_AND_CONSTRAINTS.md
  - docs/chantiers/GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01/40_GAPS_AND_NEXT_GO.md
---

# 04_GAPS_AND_CHILD_GO_PLAN

## MASTER_TARGET

Le produit final total reste ouvert jusqu'a livraison ou blocage explicite de toutes les chaines majeures.

## Gaps par chaine

### Runtime operateur distant

- `GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01` non localise sous ce nom exact
- preuves disponibles surtout documentaires cote `TMUX_IDE`
- sous-lots runtime (OpenClaw operator + mobile smoke) recales sur preuves
  locales Python, mais les validations distantes SSH et le device mobile reel
  restent PENDING

### TradingView alert chain

- chaine vers Desk Pro prouvee partiellement, mais closeout umbrella absent
- scoring transverse final non recroise a ce niveau parent

### Bot Vision / headless screener

- paire canonique documentee, mais raccord umbrella complet restant a poser
- survivant unique et bridge Desk Pro/Telegram encore a stabiliser hors de ce parent

### Telegram screener inbound

- registry channels documente
- aucun parser inbound trades/setups prouve a ce stade

### Telegram notification outbound

- dispatcher present
- routing multi-chats/bots/topics pas encore fixe au niveau final umbrella

### Google Sheets global

- schema global documente en cours
- pas d'implementation globale ni de single writer transverse

### Strategy Registry / Perf / replay / paper

- surfaces presentes
- gates de promotion/block/retire et lien latency transverse encore a consolider

### E2E dry-run / closeout final

- un dry-run chaine existe
- le dry-run total umbrella et le closeout final restent ouverts

## Child GO plan

| Priorite | GO enfant | Raison |
| --- | --- | --- |
| P0 | `GO_OPT_TRADING_RUNTIME_ORCHESTRATOR_TMUX_FLEET_MOBILE_DEPLOY_01` | meilleur mapping local du runtime operateur distant `phone / SSH / tmux / OpenClaw / repo` |
| P1 | `GO_STRATEGY_SIGNAL_MONITORING_REPO_INVENTORY_01` | baseline repo-first deja alignee, a garder comme preuve transverse |
| P1 | `GO_EVENT_TAXONOMY_01` | envelope transverse deja alignee |
| P1 | `GO_TELEGRAM_EVENT_ROUTING_MAP_01` | outbound multi-destinations deja aligne |
| P1 | `GO_DESKPRO_INPUT_EXPANSION_01` | hub consumer final Desk Pro, encore incomplet cote collectors |
| P1 | `GO_TELEGRAM_SCREENER_CHANNEL_REGISTRY_01` | pre-requis inbound separe, parser encore absent |
| P1 | `GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01` | schema avant toute implementation write |
| P2 | `GO_TELEGRAM_LATENCY_BACKTEST_01` | mesure publique/latency deja alignee avant promotion strategie |
| P2 | `GO_OPT_TRADING_OPENCLAW_TMUX_OPERATOR_IMPL_01` | sous-lot runtime reel (avant mobile), aligne sur preuves Python locales ; validations distantes encore PENDING |
| P2 | `GO_OPT_TRADING_MOBILE_TMUX_OPERATOR_SMOKE_01` | sous-lot runtime mobile (apres OpenClaw), tests Python OK (skips si bash indisponible), device reel PENDING |

## Prochain item Kanban a faire

`GO_OPT_TRADING_RUNTIME_ORCHESTRATOR_TMUX_FLEET_MOBILE_DEPLOY_01`

## Gaps encore ouverts

- bundle exact absent sous noms initiaux
- GO runtime bundle exact absent sous son nom ; mapping local retenu sur `GO_OPT_TRADING_RUNTIME_ORCHESTRATOR_TMUX_FLEET_MOBILE_DEPLOY_01`
- collectors Coinglass / exchange API a raffiner dans `GO_DESKPRO_INPUT_EXPANSION_01`
- closeout final umbrella reste bloque tant que runtime, Bot Vision/headless et implementation globale Sheets ne sont pas fermes ou bloques explicitement
