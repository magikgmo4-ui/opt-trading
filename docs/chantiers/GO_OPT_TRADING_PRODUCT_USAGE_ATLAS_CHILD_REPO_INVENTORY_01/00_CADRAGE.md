---
doc_id: GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_REPO_INVENTORY_01_CADRAGE
doc_type: cadrage
repo: opt-trading
go_id: GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_REPO_INVENTORY_01
parent_go: GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_PARENT_01
status: reference
lifecycle_stage: cadrage
source_kind: canonical
updated_at: 2026-05-07
links:
  - docs/product/PRODUCT_USAGE_MATRIX.md
  - docs/product/PRODUCT_USAGE_ATLAS.md
  - docs/product/FINAL_TARGET_GAPS.md
  - docs/chantiers/GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_PARENT_01/90_CLOSEOUT.md
  - docs/chantiers/GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_USAGE_VIEW_01/90_CLOSEOUT.md
  - docs/index/GO_INDEX.md
  - docs/index/BRANCH_STATE.md
  - docs/architecture/REPO_SURFACES_MAP.md
  - docs/architecture/PROJECT_SNAPSHOT_GLOBAL_2026-04-18.md
---

# 00_CADRAGE - GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_REPO_INVENTORY_01

## 1_MASTER_TARGET

Etendre l'inventaire du Product Usage Atlas au-dela des 6 produits du socle initial deja classes, sans modifier le runtime ni promouvoir artificiellement des surfaces non prouvees.

## 2_BASE_STATE

Point de depart : `sot/mainline` au merge `8425078` (PR #238, child usage view PASS).

Etat deja etabli :
- Atlas parent : PR #237 PASS, merge `570a2dd`
- Usage View child : PR #238 PASS, merge `8425078`
- 6 produits classes dans 5 buckets :
  - `USABLE_NOW` : Repo KG
  - `USABLE_LIMITED` : ClickUp Cockpit
  - `DOC_ONLY` : Airtable Orchestration Layer, OpenClaw Docs Library
  - `SIMULATED_ONLY` : Botpress Adapter
  - `FORBIDDEN_LIVE` : BTC COIN-M Accumulation Engine
- Le plan initial apps (ClickUp -> Repo KG -> Airtable -> Botpress) n'est pas rouvert.

## 3_INITIAL_NEED

Le repo contient de nombreuses surfaces importantes au-dela du socle initial : Desk Pro, Bot Vision, Trading Dual Stack, pipeline TradingView/Telegram, OpenClaw runtime, collecteurs, moteurs d'analyse, wrappers operatoires, etc.

Le besoin est de les inventorier, de les classer prudemment, et de proposer les ajouts a l'Atlas qui sont suffisamment prouves, sans confondre module technique et produit utilisateur.

## 4_MASTER_PROJECT_PLAN

1. Partir des produits deja presents dans l'Atlas.
2. Chercher les surfaces importantes absentes du socle initial.
3. Pour chaque candidat, determiner : produit ou module ? runtime ou doc-only ? wrapper generique ou produit utilisateur ? preuve d'usage ou simple presence technique ? closeout / PR / test / smoke disponible ?
4. Classer avec les buckets existants.
5. Proposer une entree dans l'Atlas seulement si la source est prouvee.
6. Laisser en candidat/HYPOTHESIS ce qui n'est pas assez prouve.
7. Documenter les gaps et NEXT_GO.
8. Marquer ARCHIVE_ONLY ou DO_NOT_PROMOTE les surfaces qui ne doivent pas entrer dans l'Atlas.

## 7_CANONICAL_STATE

Les surfaces suivantes ont ete scannees dans le repo :

| Surface | Module(s) principal(aux) | Preuve la plus forte trouvee |
| --- | --- | --- |
| Desk Pro | `modules/desk_pro*` (10 modules) + `scripts/admin_trading/desk_pro_cmd.sh` | Fiche statut canonique + runbooks + project card |
| Bot Vision | `modules/vision_bot` + `modules/bot_vision_step2` | Fiche statut canonique + synthese produit |
| Trading Dual Stack V1 / XAUUSD | `modules/trading_lab_v1/` + `modules/trading_realtime_v1/` | Synthese canonique produit (TRADING_DUAL_STACK_CANONICAL_PRODUCT_SYNTH_01) |
| TradingView / Telegram Alert Pipeline | `modules/tradingview_observer*` + `modules/webhook/` | MACHINE_WORK_SPLIT (CURSOR_AI), closeouts PR #200, PR #203 |
| OpenClaw Runtime | `modules/gateway_openclaw`, `modules/configure_openclaw`, `modules/install_module_openclaw` (9 modules) | Cible canonique + cartographie 77 sources |
| LocalCMS | `localcms` (projet externe, consommateur UI) | GO_LOCALCMS_FORMS_INTEGRATION_DOC_01 |
| derivates_collector | `modules/derivatives_collector/` | Doctrine famille + migration map |
| derivates_analyzer | `modules/derivatives_analyzer/` | Lie au collector, mentionne dans docs |
| probability_engine | `modules/probability_engine/` | Mentionne dans PROJECT_SNAPSHOT |
| risk_engine | `modules/risk_engine/` | Mentionne dans PROJECT_SNAPSHOT |
| market_scanner | `modules/market_scanner/` | Mentionne dans ui_indexation |
| desk_pro_dashboard | `modules/desk_pro_dashboard/` | Mentionne dans docs/status/desk_pro_stack_canonique.md |
| validated_prompt_factory | `modules/validated_prompt_factory/` | Mentionne dans OT_OPS_01_AUDIT (PARTIEL) |
| Deepseek Student | `modules/deepseek_hub/` + `scripts/student/` | Fiche statut canonique + runbook |
| Collectors spot (coingecko, binance) | `modules/collector_coingecko/`, `modules/collector_binance_spot/` | Doctrine famille (validated) |
| Simex Bitget Bridge | `modules/simex_bitget_bridge/` | SIMEX_PRESETS.md + SIMEX_UNITS_CONTRACT.md |
| Git Fleet Guard | `modules/git_fleet_guard/` | Runbook + module overview |
| Module contextuals shell | `modules/module_contextuals_shell/` | Module present, peu de preuve produit |
| Ops wrappers / menus / registry | `modules/ops_wrappers/`, `modules/ops_menu_hub/`, `modules/ops_super_menu/` | Wrappers generiques, pas de produit utilisateur |

## 11_KEY_DECISIONS

- Un module n'est pas automatiquement un produit.
- Un wrapper generique n'entre pas dans l'Atlas produit.
- Une surface historique ne doit pas etre promue.
- Un PASS technique ne suffit pas a classer une surface comme `USABLE_NOW`.
- Les buckets existants (5) ne sont pas etendus.
- Aucune app externe ne devient source canonique.
- Le repo reste la preuve.

## 12_INVARIANTS

- Doc-only uniquement.
- Aucun runtime modifie.
- Aucun secret expose.
- Aucun nouveau bucket cree.
- Aucune promotion sans preuve repo.
- Aucun guide live pour une surface non validee.
- Ne pas toucher a une logique trading reelle.

## 17_RESUME_POINT

```text
docs/chantiers/GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_REPO_INVENTORY_01/02_CLASSIFICATION_MATRIX.md
docs/chantiers/GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_REPO_INVENTORY_01/03_ATLAS_UPDATE_PROPOSAL.md
```
