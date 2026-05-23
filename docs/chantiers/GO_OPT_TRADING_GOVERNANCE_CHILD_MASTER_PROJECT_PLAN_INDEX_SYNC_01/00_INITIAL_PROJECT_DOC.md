# GO_OPT_TRADING_GOVERNANCE_CHILD_MASTER_PROJECT_PLAN_INDEX_SYNC_01

## Contexte

Synchronisation documentaire structurée des surfaces PF_* avec la matrice MASTER_TARGET > MASTER_PROJECT_PLAN > umbrella parent/dédié

Branche : go/GO_OPT_TRADING_GOVERNANCE_CHILD_MASTER_PROJECT_PLAN_INDEX_SYNC_01

Réf. cible :
TARGET_MASTER_PROJECT_PLAN_INDEX_SYNC_WITH_UMBRELLA_PARENT_01

## Objectif

- Aligner toutes les surfaces PF_* avec le plan projet master (MPP), rattacher chaque PF à un parent umbrella si existant, sinon dédié
- Appliquer la règle : pas d’ouverture automatique de parent PF_* sans vérification umbrella (GO_OPT_TRADING_ADMIN_TRADING_SIGNAL_CHAIN_TOTAL_PRODUCT_PARENT_01)

## Surfaces PF_*

- PF_DESK_PRO
- PF_DATA_CENTER
- PF_TELEGRAM_SCREENER
- PF_TELEGRAM_INGESTION
- PF_BOT_VISION_HEADLESS
- PF_SIGNAL_CHAIN_PRODUCT
- PF_OPENCLAW_ORCHESTRATOR_FULL
- PF_OPERATOR_RUNTIME
- PF_LOCALCMS_COCKPIT
- PF_STRATEGY_FRAMEWORK_REGISTRY
- PF_PERF_ENGINE_TRADING_LAB
- PF_GOOGLE_SHEETS_CONSUMER
- PF_STRICT_WORKERS_AI_TEAM
- PF_FIGMA_FINANCIAL_COCKPIT

## Règle forte

Avant d’ouvrir un parent PF, vérifier la couverture par GO_OPT_TRADING_ADMIN_TRADING_SIGNAL_CHAIN_TOTAL_PRODUCT_PARENT_01.

- Si PF couvert umbrella : rattacher au parent, identifier next item, documenter gap
- Si non couvert : chercher parent dédié existant, sinon proposer parent continuité et MPP minimal
- Si optionnel : marquer TBD_DECISION

## Table d’audit des surfaces (draft, à compléter :)

| PF_ID                         | MASTER_TARGET                        | MASTER_PROJECT_PLAN_ID               | PARENT_CONTINUITY_GO                                 | UMBRELLA_COVERAGE        | DEDICATED_PARENT_IF_ANY                     | NEXT_KANBAN_ITEM_OR_NEXT_GO                | CLOSE_GATE          | REMAINING_GAP                                   |
|-------------------------------|--------------------------------------|--------------------------------------|------------------------------------------------------|-------------------------|---------------------------------------------|---------------------------------------------|---------------------|---------------------------------------------------|
| PF_DESK_PRO                   | Desk Pro operator                    | MPP_DESK_PRO_OPERATIONAL             | GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_01             | OUI (hub consumer)      | –                                           | TBD_MASTER_PROJECT_PLAN                    | À compléter         | close gate à prévoir, promotion registry        |
| PF_DATA_CENTER                | Data Center                          | MPP_DATA_CENTER_NORMALIZED_REGISTRY  | GO_OPT_TRADING_DATA_CENTER_PARENT_01                 | NON                    | GO_OPT_TRADING_DATA_CENTER_PARENT_01         | GO_OPT_TRADING_DATA_CENTER_PARENT_OPEN_01   | À créer             | parent MPP data registry à bâtir               |
| PF_TELEGRAM_SCREENER          | Telegram Screener operational         | MPP_TELEGRAM_SCREENER_OPERATIONAL    | GO_OPT_TRADING_TELEGRAM_SCREENER_PARENT_01           | PARTIELLE               | GO_OPT_TRADING_TELEGRAM_SCREENER_PARENT_01   | GO_OPT_TRADING_TELEGRAM_SCREENER_PARENT_OPEN_01 | À compléter        | registry inbound ok, parser inbound open       |
| PF_TELEGRAM_INGESTION         | Telegram Ingestion operational        | MPP_TELEGRAM_INGESTION_OPERATIONAL   | GO_OPT_TRADING_TELEGRAM_INGESTION_PARENT_01          | NON                    | GO_OPT_TRADING_TELEGRAM_INGESTION_PARENT_01  | GO_OPT_TRADING_TELEGRAM_INGESTION_PARENT_OPEN_01 | À créer           | parser et parent d’ingestion à ouvrir          |
| PF_BOT_VISION_HEADLESS        | Bot Vision / Headless Screener       | MPP_BOT_VISION_HEADLESS_OPERATIONAL  | GO_OPT_TRADING_COLLECTORS_BOT_VISION_PARENT_01       | OUI                    | –                                           | TBD_MASTER_PROJECT_PLAN                    | À compléter         | raccord doc umbrella à finaliser              |
| PF_SIGNAL_CHAIN_PRODUCT       | Signal Chain Product                 | MPP_SIGNAL_CHAIN_PRODUCT_COMPLETE    | GO_OPT_TRADING_SIGNAL_CHAIN_TOTAL_PRODUCT_BUNDLE_20260519 | OUI                | –                                           | TBD_CLOSE_GATE                              | En cours           | closeout E2E incomplet umbrella               |
| PF_OPENCLAW_ORCHESTRATOR_FULL | OpenClaw Orchestrator FULL           | MPP_OPENCLAW_ORCHESTRATOR_FULL       | GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01       | PARTIELLE               | GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01 | TBD_MASTER_PROJECT_PLAN                 | À compléter         | parent dedié relu, mapping umbrella à finir   |
| PF_OPERATOR_RUNTIME           | OpenClaw / OpenCode Operator Runtime | MPP_OPERATOR_RUNTIME                 | GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01                 | PARTIELLE               | GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01         | TBD_CLOSE_GATE                              | À compléter         | recroisement runtime SHH/mobile à finir       |
| PF_LOCALCMS_COCKPIT           | LocalCMS cockpit système             | MPP_LOCALCMS_COCKPIT                 | GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01        | NON                    | GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01 | GO_OPT_TRADING_UI_LOCALCMS_INVENTORY_01    | Inventaire avant    | registry/inventaire UI non finalisé           |
| PF_STRATEGY_FRAMEWORK_REGISTRY| Strategy Framework + Registry        | MPP_STRATEGY_FRAMEWORK_REGISTRY      | GO_STRATEGY_CANONICAL_FRAMEWORK_PARENT_01            | OUI                    | –                                           | TBD_CLOSE_GATE                              | À compléter         | gates registry/retire à valider               |
| PF_PERF_ENGINE_TRADING_LAB    | Perf Engine / Trading Lab            | MPP_PERF_ENGINE_TRADING_LAB          | GO_OPT_TRADING_PERF_ENGINE_TRADING_LAB_PARENT_01     | OUI                    | –                                           | GO_OPT_TRADING_PERF_ENGINE_TRADING_LAB_PARENT_OPEN_01 | À compléter         | parent perf/lab partiellement couvert         |
| PF_GOOGLE_SHEETS_CONSUMER     | Google Sheets global consumer        | MPP_GOOGLE_SHEETS_GLOBAL_CONSUMER    | GO_OPT_TRADING_GOOGLE_SHEETS_CONSUMER_PARENT_01      | PARTIELLE               | GO_OPT_TRADING_GOOGLE_SHEETS_CONSUMER_PARENT_01 | GO_OPT_TRADING_GOOGLE_SHEETS_CONSUMER_PARENT_OPEN_01 | À compléter         | implementation globale non transverse         |
| PF_STRICT_WORKERS_AI_TEAM     | Strict Workers Runner / AI Team      | MPP_STRICT_WORKERS_AI_TEAM           | GO_OPT_TRADING_STRICT_WORKERS_PARENT_01              | NON                    | GO_OPT_TRADING_STRICT_WORKERS_PARENT_01      | TBD_CLOSE_GATE                                 | À compléter         | alignment workers/closeout à sécuriser        |
| PF_FIGMA_FINANCIAL_COCKPIT    | Figma Financial Cockpit (optionnel)  | MPP_FIGMA_FINANCIAL_COCKPIT          | GO_OPT_TRADING_FIGMA_FINANCIAL_COCKPIT_PARENT_01     | NON                    | GO_OPT_TRADING_FIGMA_FINANCIAL_COCKPIT_PARENT_01 | TBD_DECISION                              | À confirmer (opt.)  | décision si cockpit Figma est promu           |


*Lot doc-only, pas d’impact runtime.*
