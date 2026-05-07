---
doc_id: GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_APPLY_REPO_INVENTORY_01_APPLY_PLAN
doc_type: apply_plan
repo: opt-trading
go_id: GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_APPLY_REPO_INVENTORY_01
parent_go: GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_PARENT_01
status: reference
lifecycle_stage: cadrage
source_kind: canonical
updated_at: 2026-05-07
links:
  - docs/chantiers/GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_REPO_INVENTORY_01/02_CLASSIFICATION_MATRIX.md
  - docs/chantiers/GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_REPO_INVENTORY_01/03_ATLAS_UPDATE_PROPOSAL.md
  - docs/product/PRODUCT_USAGE_MATRIX.md
  - docs/product/PRODUCT_USAGE_ATLAS.md
  - docs/product/FINAL_TARGET_GAPS.md
  - docs/product/PRODUCT_USAGE_GRAPH.mmd
---

# 01_APPLY_PLAN - Plan d'application des 7 ADD_TO_ATLAS

## Regle stricte

Ce child applique uniquement les 7 entrees `ADD_TO_ATLAS` validees par l'inventaire.
Aucune entree `KEEP_CANDIDATE`, `DO_NOT_PROMOTE`, `ARCHIVE_ONLY`, `A AUDITER` ou `UNKNOWN` n'est promue.

## Entrees a appliquer

| Surface | Bucket | Sources canoniques | NEXT_GO |
| --- | --- | --- | --- |
| Desk Pro | `USABLE_LIMITED` | `docs/status/desk_pro_stack_canonique.md`, `docs/desk_pro_multi_machine_quick_reference.md`, `docs/governance/DESK_PRO_CANONICAL_PRODUCT_SYNTH_01.md` | `GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01` |
| Bot Vision | `USABLE_LIMITED` | `docs/status/bot_vision_canonique.md`, `docs/governance/BOT_VISION_CANONICAL_PRODUCT_SYNTH_01.md` | `VISION_FAMILY_SURVIVOR_DECISION` |
| TradingView / Telegram Alert Pipeline | `USABLE_LIMITED` | `docs/index/MACHINE_WORK_SPLIT_ANTI_CONFLICT_01.md`, `docs/chantiers/GO_OPT_TRADING_CURSOR_AI_OBSERVER_TRADINGVIEW_MCP_01/90_CLOSEOUT.md` | Poursuite GO alert webhook actif |
| OpenClaw Runtime | `USABLE_LIMITED` | `docs/product_targets/OPENCLAW_TARGET_CANON.md`, `docs/chantiers/GO_OPENCLAW_DBLAYER_DOCS_RESEARCH_LIBRARY_PARENT_01/`, `docs/chantiers/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01/` | `GO_OPENCLAW_OPT_TRADING_CHILD_GATEWAY_SUPERVISION_TMUX_RUNTIME_01` |
| derivatives_collector | `USABLE_LIMITED` | `docs/COLLECTORS_FAMILY_DOCTRINE_01.md`, `docs/COLLECTORS_MIGRATION_MAP_01.md` | `GO_COLLECTORS_BASELINE_INVENTORY_01` |
| Trading Dual Stack V1 / XAUUSD | `DOC_ONLY` | `docs/governance/TRADING_DUAL_STACK_CANONICAL_PRODUCT_SYNTH_01.md` | `GO_OT_TRADING_REALTIME_V1_CHAIN_CLOSED_01` |
| LocalCMS | `DOC_ONLY` | `docs/chantiers/GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01/`, `docs/chantiers/GO_LOCALCMS_FORMS_INTEGRATION_DOC_01/` | `GO_LOCALCMS_FORMS_INTEGRATION_DOC_01` |

## Fichiers modifies

| Fichier | Modification |
| --- | --- |
| `docs/product/PRODUCT_USAGE_MATRIX.md` | Ajouter 7 entrees dans chaque table, actualiser Repo KG NEXT_GO |
| `docs/product/PRODUCT_USAGE_ATLAS.md` | Ajouter 7 entrees detaillees avec usage_view, operator_read, canonical_sources |
| `docs/product/FINAL_TARGET_GAPS.md` | Ajouter 7 gaps, actualiser la lecture par vue usage |
| `docs/product/PRODUCT_USAGE_GRAPH.mmd` | Ajouter 7 noeuds dans les buckets, NEXT_GO edges |

## Fichiers NON modifies

| Fichier | Raison |
| --- | --- |
| `docs/product/UPDATE_PROTOCOL.md` | Les regles restent identiques |
| `docs/product/guides/*` | Les guides utilisateur sont ulterieurs (USER_GUIDES child) |
| `docs/product/PROJECT_PRESENTATION.md` | Suffisant en l'etat, reference la matrice deja |

## Verification pre-application

- Les 6 produits du socle initial restent inchanges dans leurs buckets.
- Aucun bucket n'est ajoute.
- Aucune promotion de KEEP_CANDIDATE.
- Repo KG NEXT_GO actualise (l'inventaire est fait, l'application est en cours).
