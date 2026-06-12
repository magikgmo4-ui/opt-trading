---
doc_id: GO_OPT_TRADING_CONSOLIDATION_UI_CLUSTER_01_INVENTORY
doc_type: cluster_inventory
repo: opt-trading
project: opt-trading
module: product
go_id: GO_OPT_TRADING_CONSOLIDATION_UI_CLUSTER_01
status: draft_for_review
lifecycle_stage: child_inventory
parent_go_id: GO_OPT_TRADING_AUDIT_ORPHAN_MODULES_01
topic_keys:
  - opt-trading
  - consolidation
  - ui
  - desk-pro
  - inventory
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_CONSOLIDATION_UI_CLUSTER_01/01_UI_CLUSTER_INVENTORY.md
point_de_reprise: "Inventaire complet des 6 composants UI avec cross-références et fichiers."
updated_at: 2026-05-07
links:
  - docs/chantiers/GO_OPT_TRADING_CONSOLIDATION_UI_CLUSTER_01/00_CADRAGE.md
---

# 01_UI_CLUSTER_INVENTORY

## 1_HUB — modules/desk_pro/ (existant)

```text
Fichiers  : 11
Rôle      : API FastAPI partagée, modèles Pydantic, scoring, UI HTML
Dépendances : aucune externe → desk_pro (auto-référentiel)
Atlas     : USABLE_LIMITED (déjà dans l'Atlas)

Structure :
  __init__.py           (docstring)
  README.md             (doc du hub)
  models.py             (DeskForm, Snapshot, Metric, ScoreResult)
  mount.py              (helper FastAPI mount)
  api/routes.py         (215 lignes, 6 endpoints /desk/*)
  service/aggregator.py (build_snapshot_mock)
  service/scoring.py    (compute_probability)
  ui/page.py            (render_ui_html, 213 lignes)
  scripts/              (cmd.sh, menu.sh, sanity_check.sh, install_shortcuts.sh)
```

## 2_RUNNER — modules/desk_pro_runner/

```text
Fichiers  : 7
Rôle      : Façade opérateur, lance orchestrateur + dashboard
Dépendances : desk_pro_orchestrator (string), desk_pro_dashboard (string)
Atlas     : dans Desk Pro (USABLE_LIMITED)

Structure :
  app/desk_pro_runner.py    (178 lignes)
  config/runner_config.example.json
  scripts/ (cmd.sh, menu.sh, sanity_check.sh)
  README.md

Imports à fixer :
  L23: ORCHESTRATOR_MOD = "modules.desk_pro_orchestrator.app.desk_pro_orchestrator"
  L24: DASHBOARD_MOD     = "modules.desk_pro_dashboard.app.desk_pro_dashboard"
```

## 3_ORCHESTRATOR — modules/desk_pro_orchestrator/

```text
Fichiers  : 7
Rôle      : Chef d'orchestre du pipeline 11 étapes
Dépendances : market_scanner (string dans MODULE_REGISTRY)
Atlas     : dans Desk Pro (USABLE_LIMITED)

Structure :
  app/desk_pro_orchestrator.py  (261 lignes)
  config/run_config.example.json
  scripts/ (cmd.sh, menu.sh, sanity_check.sh)
  README.md

Imports à fixer :
  L34: "market_scanner": "modules.market_scanner.app.market_scanner"
```

## 4_DASHBOARD — modules/desk_pro_dashboard/

```text
Fichiers  : 5
Rôle      : Rendu terminal/JSON/HTML des runs d'orchestration
Dépendances : aucune import Python externe (lit data/desk_runs/)
Atlas     : USABLE_LIMITED (déjà dans l'Atlas)

Structure :
  app/desk_pro_dashboard.py   (355 lignes)
  config/sample_dashboard_input.json
  scripts/ (cmd.sh, menu.sh, sanity_check.sh)
  README.md

Pas d'import à fixer (auto-référentiel, lit le filesystem).
```

## 5_SCANNER — modules/market_scanner/

```text
Fichiers  : 5
Rôle      : Scanner d'opportunités, 1er étage du pipeline
Dépendances : aucune import Python externe
Atlas     : KEEP_CANDIDATE

Structure :
  app/market_scanner.py       (215 lignes, scoring pondéré)
  config/sample_markets.json  (4 assets)
  scripts/ (cmd.sh, menu.sh, sanity_check.sh)
  README.md

Pas d'import Python à fixer.
Le nom est référencé en string dans desk_pro_orchestrator.
```

## 6_REGISTRY — modules/ui_registry_msi/

```text
Fichiers  : 5 + .gitignore
Rôle      : Registre central des 21 surfaces UI
Dépendances : lit registry/ui_surfaces_registry.yaml
Atlas     : KEEP_CANDIDATE

Structure :
  app/ui_registry_msi.py      (186 lignes)
  config/ui_registry_seed.json (21 surfaces)
  scripts/ (cmd.sh, menu.sh, sanity_check.sh)
  README.md

Pas d'import Python à fixer.
Le registre référence d'autres modules par nom (pas par import).
```

## 7_LOCALCMS — externe

```text
Statut   : EXTERNE, ne sera pas déplacé.
Atlas    : DOC_ONLY (déjà dans l'Atlas)
Action   : aucun. Référencé comme dépendance optionnelle.
```

## 8_MATRICE_CROSS_REFERENCES

| Consommateur | Cible | Type | Ligne |
|---|---|---|---|
| desk_pro_runner/app/desk_pro_runner.py | desk_pro_orchestrator | string path | L23 |
| desk_pro_runner/app/desk_pro_runner.py | desk_pro_dashboard | string path | L24 |
| desk_pro_orchestrator/app/desk_pro_orchestrator.py | market_scanner | string path (MODULE_REGISTRY) | L34 |
| desk_pro/api/routes.py | desk_pro.models | import Python | L8 |
| desk_pro/api/routes.py | desk_pro.service.aggregator | import Python | L9 |
| desk_pro/api/routes.py | desk_pro.service.scoring | import Python | L10 |
| desk_pro/api/routes.py | desk_pro.ui.page | import Python | L11 |
| ui_surfaces_registry.yaml | desk_pro_dashboard, desk_pro_runner, market_scanner | nom | - |

## 9_RESUME

```text
6 composants : 1 hub + 5 migrants
2 fichiers Python à modifier (desk_pro_runner.py, desk_pro_orchestrator.py)
1 fichier YAML à mettre à jour (ui_surfaces_registry.yaml)
~15 scripts shell à mettre à jour
Les imports Python internes à desk_pro (routes.py, etc.) ne changent pas (déjà sous le hub)
```

## RISKS

- À qualifier.
