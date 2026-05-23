---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_SIGNAL_CHAIN_TOTAL_PRODUCT_PARENT_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_SIGNAL_CHAIN_TOTAL_PRODUCT_PARENT_01
status: open
lifecycle_stage: umbrella_parent_doc_only
source_kind: canonical
updated_at: 2026-05-23
links:
  - docs/index/MACHINE_WORK_SPLIT_ANTI_CONFLICT_01.md
  - docs/product/guides/TRADINGVIEW_TELEGRAM_PIPELINE.md
  - docs/chantiers/GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_OPERATOR_WORKFLOW_MINIMAL_01/30_EXECUTION_PROTOCOL.md
  - docs/chantiers/GO_STRATEGY_CANONICAL_FRAMEWORK_PARENT_01/95_STRATEGY_REGISTRY.md
  - docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_RUNTIME_REVIEW_REPRISE_01/20_INPUT_CONSUMER_MAP.md
  - docs/chantiers/GO_STRATEGY_SIGNAL_MONITORING_REPO_INVENTORY_01/00_INITIAL_PROJECT_DOC.md
  - docs/chantiers/GO_TELEGRAM_EVENT_ROUTING_MAP_01/00_INITIAL_PROJECT_DOC.md
  - docs/chantiers/GO_TELEGRAM_SCREENER_CHANNEL_REGISTRY_01/10_CURRENT_INBOUND_SURFACES.md
  - docs/chantiers/GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01/00_INITIAL_PROJECT_DOC.md
---

# 00_INITIAL_PROJECT_DOC

## But

Poser le parent umbrella doc-only du produit final total de la chaine signal/screener/Telegram/Desk Pro/Perf/Sheets/runtime, sans implementation nouvelle a cette passe.

## MASTER_TARGET

Construire le produit final complet, separe en chaines independantes mais liees :

1. runtime operateur distant (`phone / SSH / tmux / OpenCode / OpenClaw / repo`)
2. TradingView alert chain (`TradingView -> webhook -> signal_event -> Desk Pro -> score -> Telegram/Sheets/Perf`)
3. Bot Vision / headless screener chain
4. Telegram screener inbound chain
5. Telegram notification outbound chain
6. Google Sheets global consumer transverse
7. Strategy Registry / Perf Engine transverse

## Etat de cette passe

- passe strictement `DOC_ONLY`
- aucun runtime live modifie
- aucun module nouveau cree
- aucune mutation dispatcher live
- aucune ecriture Google Sheets reelle
- aucune modification Strategy Registry runtime

## Bundle de depart

Les noms exacts du bundle fournis dans le prompt n'ont pas ete retrouves localement sous ces chemins/noms :

- `00_STRUCTURE_VALIDEE_SESSION.md`
- `01_CHAINES_PRODUIT_FINAL.md`
- `02_SURFACES_ROLES_MAPPING.md`
- `03_TELEGRAM_ROUTING_MAP.md`
- `04_DESKPRO_HUB_EXPANSION.md`
- `05_TELEGRAM_SCREENER_AND_LATENCY_STRATEGY.md`
- `06_GOOGLE_SHEETS_GLOBAL_SCHEMA.md`
- `07_STRATEGY_REGISTRY_AND_PERF_ENGINE.md`
- `08_KANBAN_ROADMAP_PRODUIT_FINAL.md`
- `09_GAPS_NEXT_STEP.md`
- `10_BUNDLE_REPRISE_POINT.md`

Le parent conserve donc ces references bundle comme cible documentaire a respecter, mais ancre l'inventaire sur les preuves locales effectivement trouvees dans le repo.

## Pieces locales relues avant creation

- `docs/index/MACHINE_WORK_SPLIT_ANTI_CONFLICT_01.md`
- `docs/product/guides/TRADINGVIEW_TELEGRAM_PIPELINE.md`
- `docs/chantiers/GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_OPERATOR_WORKFLOW_MINIMAL_01/30_EXECUTION_PROTOCOL.md`
- `docs/chantiers/GO_STRATEGY_CANONICAL_FRAMEWORK_PARENT_01/95_STRATEGY_REGISTRY.md`
- `docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_RUNTIME_REVIEW_REPRISE_01/20_INPUT_CONSUMER_MAP.md`
- `docs/chantiers/GO_STRATEGY_SIGNAL_MONITORING_REPO_INVENTORY_01/*`
- `docs/chantiers/GO_TELEGRAM_EVENT_ROUTING_MAP_01/*`
- `docs/chantiers/GO_TELEGRAM_SCREENER_CHANNEL_REGISTRY_01/*`
- `docs/chantiers/GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01/*`
- `docs/product/guides/BOT_VISION.md`

## Articulation des GOs runtime / bundles / umbrella

Ce parent umbrella distingue explicitement :

- parent umbrella produit total : `GO_OPT_TRADING_ADMIN_TRADING_SIGNAL_CHAIN_TOTAL_PRODUCT_PARENT_01` (ce dossier)
- parent bundle storage : `GO_OPT_TRADING_BUNDLES_REPO_STORAGE_PARENT_01` (stockage/retrieval des artefacts et bundles)
- runtime GO historique : `GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01` (cadrage/plan/decisions runtime OpenCode/OpenClaw)
- runtime orchestrator GO operationnel : `GO_OPT_TRADING_RUNTIME_ORCHESTRATOR_TMUX_FLEET_MOBILE_DEPLOY_01` (validation read-only SSH/tmux/mobile + fleet health)

Liens locaux :

- `docs/chantiers/GO_OPT_TRADING_BUNDLES_REPO_STORAGE_PARENT_01/00_PARENT_CADRAGE.md`
- `docs/chantiers/GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01/00_cadrage.md`
- `docs/chantiers/GO_OPT_TRADING_RUNTIME_ORCHESTRATOR_TMUX_FLEET_MOBILE_DEPLOY_01/00_INITIAL_PROJECT_DOC.md`

## Kanban de reference

Le tableau Kanban du bundle reste la carte de navigation principale du chantier umbrella. Comme `08_KANBAN_ROADMAP_PRODUIT_FINAL.md` n'est pas present localement sous ce nom, ce parent conserve :

- les items bundle comme sequence cible
- les GO locaux deja ouverts comme preuves d'avancement
- `03_PRODUCT_ROADMAP_KANBAN.md` comme miroir de continuite, et non comme roadmap concurrente

## Prochain item Kanban a faire

Le closeout final restant bloque par des surfaces encore ouvertes, le prochain
child reel a poursuivre cote parent est le meilleur mapping local du runtime
operateur distant :
`GO_OPT_TRADING_RUNTIME_ORCHESTRATOR_TMUX_FLEET_MOBILE_DEPLOY_01`

## Gaps encore ouverts

- bundle exact non retrouve localement sous les noms fournis
- runtime operator distant : `GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01` retrouve localement, mais pas encore recroise/integre proprement dans le mapping umbrella ; la validation runtime reelle SSH/tmux/mobile reste a prouver via `GO_OPT_TRADING_RUNTIME_ORCHESTRATOR_TMUX_FLEET_MOBILE_DEPLOY_01`
- Bot Vision / headless screener encore ouvert au niveau umbrella
- E2E umbrella fixture-only maintenant prouve, mais pas converti en preuves reelles par surface
- parser Telegram inbound trades/setups absent
- collectors Coinglass / exchange API encore a raccorder explicitement
- implementation globale Google Sheets encore absente
- closeout final umbrella encore bloque

## Regle de continuite obligatoire

Chaque document de cette famille doit referencer explicitement :

- la `MASTER_TARGET`
- le tableau Kanban du bundle
- le produit final total voulu
- le prochain item Kanban a faire
- les gaps encore ouverts
