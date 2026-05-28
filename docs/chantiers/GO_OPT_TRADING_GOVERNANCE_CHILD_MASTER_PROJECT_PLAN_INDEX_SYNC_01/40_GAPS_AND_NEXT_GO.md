# 40_GAPS_AND_NEXT_GO

## Gaps identifiés

| Gap | Traitement | Priorité |
|---|---|---|
| Parents PF absents (Telegram Screener, Telegram Ingestion, Perf Engine, Data Center) | Créer parents + MPP | Haute |
| `PF_OPENCLAW_ORCHESTRATOR_FULL` (PASS) — parent reste OPEN | Garder ouvert jusqu'à child datasheet_writer merged | Moyenne |
| `PF_FIGMA_FINANCIAL_COCKPIT` (TBD_DECISION) | Attendre décision produit | Basse |
| `GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01` non rattaché à MPP | Rattacher à `MPP_STRICT_WORKERS_AI_TEAM` ou créer MPP dédié | Moyenne |
| Parents machines listés mais pas de PF P3 actif dans index | Garder en section hors pilotage | Basse |

## NEXT_GO candidats

| Candidat | Condition |
|---|---|
| `GO_OPT_TRADING_GOVERNANCE_CHILD_PRODUCT_SURFACE_GAP_REMEDIATION_01` | Après ce GO — appliquer remédiation des écarts PF/MPP |
| `GO_OPT_TRADING_DATA_CENTER_PARENT_OPEN_01` | Créer parent Data Center + MPP |
| `GO_OPT_TRADING_TELEGRAM_SCREENER_PARENT_OPEN_01` | Promouvoir Telegram Screener en surface finale |
| `GO_OPT_TRADING_TELEGRAM_INGESTION_PARENT_OPEN_01` | Créer parent Telegram Ingestion |
| `GO_OPT_TRADING_PERF_ENGINE_TRADING_LAB_PARENT_OPEN_01` | Créer parent Perf Engine / Trading Lab |
| `GO_OPT_TRADING_GOVERNANCE_CHILD_MASTER_PROJECT_PLAN_CREATION_RULE_MATRIX_01` | Inscrire rôles structurels dans matrice |

## Recommandation

Next GO primaire : `GO_OPT_TRADING_GOVERNANCE_CHILD_PRODUCT_SURFACE_GAP_REMEDIATION_01` (remédiation des écarts PF/MPP).
Next GO secondaire : `GO_OPT_TRADING_DATA_CENTER_PARENT_OPEN_01` (création parent Data Center).
