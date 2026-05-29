---
doc_id: OPT_TRADING_REPRISE
doc_type: reprise
repo: opt-trading
project: opt-trading
module:
go_id:
status: reference
lifecycle_stage: reprise
topic_keys:
  - opt-trading
  - reprise
  - continuity
  - master_project_plan
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
point_de_reprise: "Section MASTER_PROJECT_PLAN reprise"
updated_at: 2026-05-23
links:
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
  - docs/governance/PRODUCT_FINAL_SURFACE_REGISTRY_01.md
  - docs/index/GO_INDEX.md
  - docs/index/ACTIVE_STREAMS.md
---

# REPRISE — opt-trading

## Point de reprise global

Base de pilotage active : `MASTER_PROJECT_PLAN_INDEX` dans `GO_INDEX.md` + correction structurante `PRODUCT_FINAL_SURFACE_REGISTRY_01.md`.

Canon décisionnel : état réel du repo `opt-trading`, relu sous la matrice maître et le registre des produits/surfaces finales `PF_*`.

## Correction active

`GO_OPT_TRADING_GOVERNANCE_CHILD_MASTER_PROJECT_PLAN_INDEX_SYNC_01` synchronise les index globaux existants avec la liste validée des surfaces finales P1/P2 et leur continuité master project plan.

## Chaîne de reprise canonique

```text
PF_* -> 1_MASTER_TARGET -> 4_MASTER_PROJECT_PLAN -> GO_PARENT_ATTACHED_TO_MASTER_PROJECT_PLAN -> GO_CHILD_ATTACHED_TO_PARENT -> BUNDLE_TARGET / NEXT_GO / CLOSE_GATE
```

Rôles structurels à appliquer à la création :

```text
GO_CHILD
GO_CHILD_ATTACHED_TO_PARENT
GO_PARENT
GO_PARENT_ATTACHED_TO_MASTER_PROJECT_PLAN
GO_MASTER_PROJECT_PLAN
```

## MASTER_PROJECT_PLAN reprise

| PF_ID | MASTER_PROJECT_PLAN_ID | Parent continuité | Reprise |
|---|---|---|---|
| `PF_DESK_PRO` | `MPP_DESK_PRO_OPERATIONAL` | `GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_01` | confirmer parent canonique + close gate produit |
| `PF_DATA_CENTER` | `MPP_DATA_CENTER_NORMALIZED_REGISTRY` | `GO_OPT_TRADING_DATA_CENTER_PARENT_01` | ouvrir parent Data Center normalisé |
| `PF_TELEGRAM_SCREENER` | `MPP_TELEGRAM_SCREENER_OPERATIONAL` | `GO_OPT_TRADING_TELEGRAM_SCREENER_PARENT_OPEN_01` | actif — parser + signal producer + Desk Pro adapter livrés — next: channel registry runtime |
| `PF_TELEGRAM_INGESTION` | `MPP_TELEGRAM_INGESTION_OPERATIONAL` | `GO_OPT_TRADING_TELEGRAM_INGESTION_PARENT_01` | ouvrir/promouvoir parent Telegram Ingestion |
| `PF_BOT_VISION_HEADLESS` | `MPP_BOT_VISION_HEADLESS_OPERATIONAL` | `GO_OPT_TRADING_COLLECTORS_BOT_VISION_PARENT_01` | rattacher collecteurs vision à parent produit |
| `PF_SIGNAL_CHAIN_PRODUCT` | `MPP_SIGNAL_CHAIN_PRODUCT_COMPLETE` | `GO_OPT_TRADING_SIGNAL_CHAIN_TOTAL_PRODUCT_BUNDLE_20260519` | vérifier close gate E2E |
| `PF_OPENCLAW_ORCHESTRATOR_FULL` | `MPP_OPENCLAW_ORCHESTRATOR_FULL` | `GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01` | **PASS — E2E + Sheets consumer DONE** : dry-run post-gate + bundle + registry + market_metrics consumer (21/21 + 134/134 PASS, PR #817) — prochain axe : `GO_OPT_TRADING_ORCHESTRATOR_CHILD_DATASHEET_WRITER_V1_IMPL_01` |
| `PF_OPERATOR_RUNTIME` | `MPP_OPERATOR_RUNTIME` | `GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01` | confirmer runtime opérateur distant utilisable |
| `PF_LOCALCMS_COCKPIT` | `MPP_LOCALCMS_COCKPIT` | `GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01` | reprendre inventaire LocalCMS |
| `PF_STRATEGY_FRAMEWORK_REGISTRY` | `MPP_STRATEGY_FRAMEWORK_REGISTRY` | `GO_STRATEGY_CANONICAL_FRAMEWORK_PARENT_01` | confirmer registry strategy + promotion/retrait |
| `PF_PERF_ENGINE_TRADING_LAB` | `MPP_PERF_ENGINE_TRADING_LAB` | `GO_OPT_TRADING_PERF_ENGINE_TRADING_LAB_PARENT_01` | ouvrir parent perf/lab si absent |
| `PF_GOOGLE_SHEETS_CONSUMER` | `MPP_GOOGLE_SHEETS_GLOBAL_CONSUMER` | `GO_OPT_TRADING_GOOGLE_SHEETS_CONSUMER_PARENT_01` | child market_metrics CLOSED (PR #817, 21/21 PASS) — ouvrir parent + consumer étendu (`GO_OPT_TRADING_DATA_CENTER_CHILD_GOOGLE_SHEETS_CONSUMER_01`) |
| `PF_STRICT_WORKERS_AI_TEAM` | `MPP_STRICT_WORKERS_AI_TEAM` | `GO_OPT_TRADING_STRICT_WORKERS_PARENT_01` | réaligner closeout draft_only et continuité workers |
| `PF_FIGMA_FINANCIAL_COCKPIT` | `MPP_FIGMA_FINANCIAL_COCKPIT` | `GO_OPT_TRADING_FIGMA_FINANCIAL_COCKPIT_PARENT_01` | confirmer décision produit |

## Parents produits actifs historiques

Ces parents restent utiles, mais leur pilotage doit être lu au travers de la table `MASTER_PROJECT_PLAN reprise`.

| PARENT_PRODUCT | STATUT | TARGET | NEXT ACTION |
|---|---|---|---|
| `GO_OPT_TRADING_GOVERNANCE_CHILD_PRODUCT_SURFACE_FINAL_REGISTRY_01` | OPEN | registre produits/surfaces finales `PF_*` | `GO_OPT_TRADING_GOVERNANCE_CHILD_PRODUCT_SURFACE_GAP_REMEDIATION_01` |
| `GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01` | OPEN | canoniser méthode multi-agents | surveiller prochains INDEX_PATCH / rattacher MPP |
| `GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01` | OPEN | parent machine admin-trading | ouvrir child si besoin produit / rattacher support |
| `GO_OPT_TRADING_MACHINE_DB_LAYER_PARENT_01` | OPEN | parent machine db-layer | ouvrir child si besoin produit / rattacher support |
| `GO_OPT_TRADING_RUNTIME_EXCEPTION_FAMILIES_01` | ACTIVE | consolider lignées runtime | figer survivant/transition/legacy/archive |
| `GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03` | OPEN | réduire compat réseau/ssh | ouvrir lot réduction compat |
| `GO_TMUX_IDE_OPT_TRADING_CADRAGE_01` | ACTIVE | implémentation tmux-ide | exécuter GO_TMUX_IDE_OPT_TRADING_IMPL_BASE_01 |
| `GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01` | OPEN | intégration UI producer-consumer | reprise sur GO_OPT_TRADING_UI_LOCALCMS_INVENTORY_01 |
| `GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01` | OPEN | architecture équipe d'agents | rattacher à `MPP_STRICT_WORKERS_AI_TEAM` ou MPP dédié |
| `GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01` | ACTIVE | runtime tmux/opencode/openclaw | maintenir ; ouvrir suite si besoin |

## Prochaine action forte

```text
GO_OPT_TRADING_GOVERNANCE_CHILD_MASTER_PROJECT_PLAN_CREATION_RULE_MATRIX_01
```

Objectif : inscrire dans la matrice la règle de création avec rôles structurels : `GO_CHILD`, `GO_CHILD_ATTACHED_TO_PARENT`, `GO_PARENT`, `GO_PARENT_ATTACHED_TO_MASTER_PROJECT_PLAN`, `GO_MASTER_PROJECT_PLAN`.

## Reprise architecture Mermaid

```text
Point de reprise architecture courant:
go/GO_OPT_TRADING_ARCHITECTURE_CHILD_AUDIT_FROM_MERMAID_01

Closeout canonique:
docs/chantiers/GO_OPT_TRADING_ARCHITECTURE_CHILD_AUDIT_FROM_MERMAID_01/90_CLOSEOUT.md

Chaîne consolidée:
parent Mermaid cartography
-> child audit architecture
-> child runtime critical path merged
-> child registry ownership merged
-> child hub refactor candidates merged
-> child runtime link proof merged

Dernier commit connu:
3c0a253d docs: update audit closeout after runtime proof merge
```

## Reprise opérationnelle

1. Lire `docs/governance/PRODUCT_FINAL_SURFACE_REGISTRY_01.md`.
2. Lire `docs/index/GO_INDEX.md`, section `MASTER_PROJECT_PLAN_INDEX`.
3. Lire `docs/index/ACTIVE_STREAMS.md`, section `MASTER_PROJECT_PLAN active streams`.
4. Créer ou rattacher les parents manquants selon le `MASTER_PROJECT_PLAN_ID`.
5. Ne fermer aucun parent si son produit final utilisable n'est pas atteint.
6. Pour la continuité architecture Mermaid, reprendre depuis `docs/chantiers/GO_OPT_TRADING_ARCHITECTURE_CHILD_AUDIT_FROM_MERMAID_01/90_CLOSEOUT.md`.

## Hors pilotage immédiat

- `GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01` — parent réel, chaîne TMUX close, doit être relu comme `PF_OPENCLAW_ORCHESTRATOR_FULL`
- `GO_OPT_TRADING_CLICKUP_PARENT_CONTINUITY_01` — bundle doc-only mergé, closeout produit, parent non fermé
- `GO_OPT_TRADING_STRICT_WORKERS_PARENT_01` — branche-only, continuité canonique à rattacher à `PF_STRICT_WORKERS_AI_TEAM`
