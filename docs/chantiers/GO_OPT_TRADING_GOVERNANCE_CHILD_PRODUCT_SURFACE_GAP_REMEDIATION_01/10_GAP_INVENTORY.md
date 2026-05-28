# 10_GAP_INVENTORY

## Gap G1 — Parents PF absents

| PF_ID | Parent requis | MPP cible | Statut |
|---|---|---|---|
| PF_TELEGRAM_SCREENER | GO_OPT_TRADING_TELEGRAM_SCREENER_PARENT_OPEN_01 | MPP_TELEGRAM_SCREENER_OPERATIONAL | À créer |
| PF_TELEGRAM_INGESTION | GO_OPT_TRADING_TELEGRAM_INGESTION_PARENT_OPEN_01 | MPP_TELEGRAM_INGESTION_OPERATIONAL | À créer |
| PF_PERF_ENGINE_TRADING_LAB | GO_OPT_TRADING_PERF_ENGINE_TRADING_LAB_PARENT_OPEN_01 | MPP_PERF_ENGINE_TRADING_LAB | À créer |
| PF_DATA_CENTER | GO_OPT_TRADING_DATA_CENTER_PARENT_OPEN_01 | MPP_DATA_CENTER_NORMALIZED_REGISTRY | À créer |

## Gap G2 — AI Team Architecture non rattaché

| GO_ID | MPP actuel | MPP cible |
|---|---|---|
| GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01 | Aucun | MPP_STRICT_WORKERS_AI_TEAM ou MPP_AI_TEAM_DEDICATED |

## Gap G3 — Parents machines sans PF P3

| Parent GO | PF associé | Action |
|---|---|---|
| GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01 | Aucun PF P3 actif | Garder en section hors pilotage |
| GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01 | Aucun PF P3 actif | Garder en section hors pilotage |

## Gap G4 — PF_OPENCLAW_ORCHESTRATOR_FULL

Parent GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01 reste ouvert en attendant le merge du child datasheet_writer. Statut PASS — pas d'action dans ce GO.

## Gap G5 — PF_FIGMA_FINANCIAL_COCKPIT

TBD_DECISION — pas de décision produit. Reporté.
