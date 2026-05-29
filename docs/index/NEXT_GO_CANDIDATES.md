---
doc_id: OPT_TRADING_NEXT_GO_CANDIDATES
doc_type: next_candidate
repo: opt-trading
project: opt-trading
module:
go_id:
status: reference
lifecycle_stage: next
topic_keys:
  - opt-trading
  - next
  - continuity
  - master_project_plan
search_tags:
  - surface:chantier
  - doc_role:index
  - flow:next_surface
  - closeout:reference
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
point_de_reprise: "Section MASTER_PROJECT_PLAN next candidates"
updated_at: 2026-05-23
links:
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
  - docs/governance/PRODUCT_FINAL_SURFACE_REGISTRY_01.md
  - docs/index/GO_INDEX.md
  - docs/index/ACTIVE_STREAMS.md
  - docs/index/REPRISE.md
---

# NEXT_GO_CANDIDATES — opt-trading

## Règle canonique

- 1 `MASTER_PROJECT_PLAN` -> 1 target ou 1 next GO primaire.
- `docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md` gouverne la lecture produit/parent/GO/Git.
- `docs/governance/PRODUCT_FINAL_SURFACE_REGISTRY_01.md` classe les produits/surfaces finales `PF_*`.
- `docs/index/GO_INDEX.md` reste la vérité de liste.
- support/tool/other doit être rattaché à un parent de continuité et à un `MASTER_PROJECT_PLAN`.

## NEXT_GO primaire global

```text
GO_OPT_TRADING_GOVERNANCE_CHILD_MASTER_PROJECT_PLAN_INDEX_SYNC_01
```

Condition : intégrer la liste des `PF_*` validés dans les index globaux existants, comme `MASTER_PROJECT_PLAN_INDEX`, et non comme fichier parallèle.

## MASTER_PROJECT_PLAN next candidates

| PF_ID | MASTER_PROJECT_PLAN_ID | Parent continuité | next target / next GO | condition | refs |
|---|---|---|---|---|---|
| `PF_DESK_PRO` | `MPP_DESK_PRO_OPERATIONAL` | `GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_01` | `TBD_MASTER_PROJECT_PLAN` | confirmer parent canonique + close gate produit | `docs/governance/PRODUCT_FINAL_SURFACE_REGISTRY_01.md` |
| `PF_DATA_CENTER` | `MPP_DATA_CENTER_NORMALIZED_REGISTRY` | `GO_OPT_TRADING_DATA_CENTER_PARENT_01` | `GO_OPT_TRADING_DATA_CENTER_PARENT_OPEN_01` | créer parent + MPP pour registre data normalisé | `docs/governance/PRODUCT_FINAL_SURFACE_REGISTRY_01.md` |
| `PF_TELEGRAM_SCREENER` | `MPP_TELEGRAM_SCREENER_OPERATIONAL` | `GO_OPT_TRADING_TELEGRAM_SCREENER_PARENT_OPEN_01` | `GO_OPT_TRADING_TELEGRAM_SCREENER_CHILD_CHANNEL_REGISTRY_RUNTIME_IMPL_01` | promouvoir channel registry doc-only → runtime | `docs/governance/PRODUCT_FINAL_SURFACE_REGISTRY_01.md` |
| `PF_TELEGRAM_INGESTION` | `MPP_TELEGRAM_INGESTION_OPERATIONAL` | `GO_OPT_TRADING_TELEGRAM_INGESTION_PARENT_01` | `GO_OPT_TRADING_TELEGRAM_INGESTION_PARENT_OPEN_01` | créer/qualifier ingestion Telegram -> signal_event | `docs/governance/PRODUCT_FINAL_SURFACE_REGISTRY_01.md` |
| `PF_BOT_VISION_HEADLESS` | `MPP_BOT_VISION_HEADLESS_OPERATIONAL` | `GO_OPT_TRADING_COLLECTORS_BOT_VISION_PARENT_01` | `TBD_MASTER_PROJECT_PLAN` | rattacher collecteurs vision à parent produit | `docs/governance/PRODUCT_FINAL_SURFACE_REGISTRY_01.md` |
| `PF_SIGNAL_CHAIN_PRODUCT` | `MPP_SIGNAL_CHAIN_PRODUCT_COMPLETE` | `GO_OPT_TRADING_SIGNAL_CHAIN_TOTAL_PRODUCT_BUNDLE_20260519` | `TBD_CLOSE_GATE` | fermer seulement si chaîne E2E utilisable | `docs/governance/PRODUCT_FINAL_SURFACE_REGISTRY_01.md` |
| `PF_OPENCLAW_ORCHESTRATOR_FULL` | `MPP_OPENCLAW_ORCHESTRATOR_FULL` | `GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01` | `GO_OPT_TRADING_ORCHESTRATOR_CHILD_DATASHEET_WRITER_V1_IMPL_01` | PF PASS — Sheets market_metrics consumer CLOSED (PR #817, 21/21 + 134/134 PASS) — next : câblage datasheet_writer → SheetsWriter runtime | `docs/chantiers/GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_MARKET_METRICS_CONSUMER_01/40_GAPS_AND_NEXT_GO.md` |
| `PF_OPERATOR_RUNTIME` | `MPP_OPERATOR_RUNTIME` | `GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01` | `TBD_CLOSE_GATE` | confirmer runtime opérateur distant utilisable | `docs/governance/PRODUCT_FINAL_SURFACE_REGISTRY_01.md` |
| `PF_LOCALCMS_COCKPIT` | `MPP_LOCALCMS_COCKPIT` | `GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01` | `GO_OPT_TRADING_UI_LOCALCMS_INVENTORY_01` | inventaire UI avant plan cockpit | `docs/governance/PRODUCT_FINAL_SURFACE_REGISTRY_01.md` |
| `PF_STRATEGY_FRAMEWORK_REGISTRY` | `MPP_STRATEGY_FRAMEWORK_REGISTRY` | `GO_STRATEGY_CANONICAL_FRAMEWORK_PARENT_01` | `TBD_CLOSE_GATE` | confirmer registry strategy + promotion/retrait | `docs/governance/PRODUCT_FINAL_SURFACE_REGISTRY_01.md` |
| `PF_PERF_ENGINE_TRADING_LAB` | `MPP_PERF_ENGINE_TRADING_LAB` | `GO_OPT_TRADING_PERF_ENGINE_TRADING_LAB_PARENT_01` | `GO_OPT_TRADING_PERF_ENGINE_TRADING_LAB_PARENT_OPEN_01` | créer parent perf/lab si absent | `docs/governance/PRODUCT_FINAL_SURFACE_REGISTRY_01.md` |
| `PF_GOOGLE_SHEETS_CONSUMER` | `MPP_GOOGLE_SHEETS_GLOBAL_CONSUMER` | `GO_OPT_TRADING_GOOGLE_SHEETS_CONSUMER_PARENT_01` | `GO_OPT_TRADING_DATA_CENTER_CHILD_GOOGLE_SHEETS_CONSUMER_01` | market_metrics child CLOSED (PR #817) — consumer étendu + parent à ouvrir | `docs/chantiers/GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_MARKET_METRICS_CONSUMER_01/40_GAPS_AND_NEXT_GO.md` |
| `PF_STRICT_WORKERS_AI_TEAM` | `MPP_STRICT_WORKERS_AI_TEAM` | `GO_OPT_TRADING_STRICT_WORKERS_PARENT_01` | `TBD_CLOSE_GATE` | réaligner closeout draft_only et continuité workers | `docs/governance/PRODUCT_FINAL_SURFACE_REGISTRY_01.md` |
| `PF_FIGMA_FINANCIAL_COCKPIT` | `MPP_FIGMA_FINANCIAL_COCKPIT` | `GO_OPT_TRADING_FIGMA_FINANCIAL_COCKPIT_PARENT_01` | `TBD_DECISION` | confirmer si Figma cockpit devient surface finale | `docs/governance/PRODUCT_FINAL_SURFACE_REGISTRY_01.md` |

## Matrice historique — parent actif → target / next GO

Cette section est conservée pour continuité, mais le pilotage principal est désormais la table `MASTER_PROJECT_PLAN next candidates`.

| parent produit | produit | statut | next target / next GO | condition | refs |
|---|---|---|---|---|---|
| `GO_OPT_TRADING_GOVERNANCE_CHILD_PRODUCT_SURFACE_FINAL_REGISTRY_01` | registre produits/surfaces finales | OPEN | `GO_OPT_TRADING_GOVERNANCE_CHILD_PRODUCT_SURFACE_GAP_REMEDIATION_01` | registre livré ; remédiation PF faite | `docs/governance/PRODUCT_FINAL_SURFACE_REGISTRY_01.md` |
| `GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01` | doctrine multi-agents | OPEN | surveiller prochains INDEX_PATCH | aucun runtime | `docs/chantiers/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01/PARENT_STATE.md` |
| `GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01` | parent machine admin-trading | OPEN | ouvrir child si besoin produit | besoin produit prouvé | `docs/chantiers/GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01/01_cadrage_parent.md` |
| `GO_OPT_TRADING_MACHINE_DB_LAYER_PARENT_01` | parent machine db-layer | OPEN | ouvrir child si besoin produit | besoin produit prouvé | `docs/chantiers/GO_OPT_TRADING_MACHINE_DB_LAYER_PARENT_01/01_cadrage_parent.md` |
| `GO_OPT_TRADING_RUNTIME_EXCEPTION_FAMILIES_01` | classification lignées runtime | ACTIVE | aucun nouveau GO | consolider en gap-only | `docs/chantiers/GO_OPT_TRADING_RUNTIME_EXCEPTION_FAMILIES_01/00_cadrage.md` |
| `GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03` | canonique modules/reseau_ssh | OPEN | aucun nouveau GO | réduire compat dans ce GO | `docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03/00_cadrage.md` |
| `GO_TMUX_IDE_OPT_TRADING_CADRAGE_01` | cadrage tmux-ide | ACTIVE | `GO_TMUX_IDE_OPT_TRADING_IMPL_BASE_01` | machine cible vérifiée | `docs/chantiers/GO_TMUX_IDE_OPT_TRADING_CADRAGE_01/00_cadrage.md` |
| `GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01` | intégration UI producer-consumer | OPEN | `GO_OPT_TRADING_UI_LOCALCMS_INVENTORY_01` | reprise recommandée | `docs/chantiers/GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01/01_cadrage_parent.md` |
| `GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01` | architecture équipe d'agents | OPEN | rattacher à `MPP_STRICT_WORKERS_AI_TEAM` ou MPP dédié | base pour GO enfant d'audit | `docs/chantiers/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01/00_cadrage.md` |
| `GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01` | runtime tmux/opencode/openclaw | ACTIVE | ouvrir suite si besoin produit | besoin produit prouvé | `docs/chantiers/GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01/00_cadrage.md` |
| `GO_OPT_TRADING_ARCHITECTURE_CHILD_AUDIT_FROM_MERMAID_01` | audit architecture Mermaid consolidé | ACTIVE | ouvrir un child de refactor code seulement sur boundary suffisamment prouvée | audits et preuves documentaires mergés | `docs/chantiers/GO_OPT_TRADING_ARCHITECTURE_CHILD_AUDIT_FROM_MERMAID_01/90_CLOSEOUT.md` |
