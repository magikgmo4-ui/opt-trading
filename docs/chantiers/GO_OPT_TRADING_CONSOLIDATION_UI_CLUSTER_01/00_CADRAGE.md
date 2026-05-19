---
doc_id: GO_OPT_TRADING_CONSOLIDATION_UI_CLUSTER_01_CADRAGE
doc_type: cadrage
repo: opt-trading
project: opt-trading
module: product
go_id: GO_OPT_TRADING_CONSOLIDATION_UI_CLUSTER_01
status: draft_for_review
lifecycle_stage: child_cadrage
parent_go_id: GO_OPT_TRADING_AUDIT_ORPHAN_MODULES_01
topic_keys:
  - opt-trading
  - product-usage
  - atlas
  - consolidation
  - ui
  - desk-pro
  - dashboard
  - registry
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_CONSOLIDATION_UI_CLUSTER_01/00_CADRAGE.md
point_de_reprise: "Consolider les 6 composants UI éclatés sous le hub existant modules/desk_pro/."
updated_at: 2026-05-07
links:
  - docs/chantiers/GO_OPT_TRADING_AUDIT_ORPHAN_MODULES_01/02_CONSOLIDATION_PLAN.md
  - docs/chantiers/GO_OPT_TRADING_CONSOLIDATION_STRATEGY_CLUSTER_01/90_CLOSEOUT.md
---

# 00_CADRAGE — CONSOLIDATION_UI_CLUSTER_01

## 1_MASTER_TARGET

Consolider les 6 composants de la famille UI / Desk Pro sous le hub existant `modules/desk_pro/`, sans casser la chaîne d'imports ni le pipeline d'orchestration.

## 2_CONSTAT

```text
PR #247 (STRATEGY) = merged PASS.

Le cluster UI compte 6 composants éclatés :
  modules/desk_pro/                → hub API/UI/service (EXISTANT, coeur actif)
  modules/desk_pro_dashboard/      → rendu terminal/JSON/HTML des runs
  modules/desk_pro_runner/         → façade opérateur (lance orchestrateur + dashboard)
  modules/desk_pro_orchestrator/   → chef d'orchestre du pipeline 11 étapes
  modules/market_scanner/          → scanner d'opportunités
  modules/ui_registry_msi/         → registre des 21 surfaces UI
  LocalCMS                         → externe, reste où il est

Cross-références documentées :
  - desk_pro_runner importe desk_pro_orchestrator et desk_pro_dashboard (string paths)
  - desk_pro_orchestrator référence market_scanner dans son MODULE_REGISTRY
  - ui_registry_msi référence desk_pro_dashboard, desk_pro_runner, market_scanner
  - desk_pro/api/routes.py importe desk_pro.models, service, ui (internes au hub)
```

## 3_ARCHITECTURE_CIBLE

```text
modules/desk_pro/                    ← hub UI unifié (existe déjà)
├── __init__.py
├── README.md                        ← mise à jour : doc de la famille complète
├── models.py                        (existant)
├── mount.py                         (existant)
├── api/routes.py                    (existant)
├── service/
│   ├── aggregator.py                (existant)
│   └── scoring.py                   (existant)
├── ui/page.py                       (existant)
├── runner/                          ← desk_pro_runner migré
│   ├── __init__.py
│   ├── app/desk_pro_runner.py
│   ├── config/
│   └── scripts/
├── orchestrator/                    ← desk_pro_orchestrator migré
│   ├── __init__.py
│   ├── app/desk_pro_orchestrator.py
│   ├── config/
│   └── scripts/
├── dashboard/                       ← desk_pro_dashboard migré
│   ├── __init__.py
│   ├── app/desk_pro_dashboard.py
│   ├── config/
│   └── scripts/
├── scanner/                         ← market_scanner migré
│   ├── __init__.py
│   ├── README.md
│   ├── app/market_scanner.py
│   ├── config/
│   └── scripts/
└── registry/                        ← ui_registry_msi migré
    ├── __init__.py
    ├── README.md
    ├── app/ui_registry_msi.py
    ├── config/
    └── scripts/
```

## 4_IMPACT

```text
Modules à migrer    : 5 (dashboard, runner, orchestrator, scanner, registry)
Hub déjà en place   : 1 (desk_pro)
Imports string à fixer : desk_pro_runner (2 refs), desk_pro_orchestrator (1 ref)
Registres à mettre à jour : ui_surfaces_registry.yaml, modules_registry.yaml
Shell scripts à fixer : ~15
LocalCMS             : inchangé (externe, pas dans modules/)
```

## 12_INVARIANTS

```text
- 0 runtime, 0 exécution de code
- 0 modification du code métier (seulement les chemins d'import)
- 0 suppression sans backup dans _archive/
- desk_pro (le hub existant) n'est pas déplacé
- Les sous-modules migrés conservent leurs scripts et configs
- Le pipeline desk_pro_orchestrator → data/desk_runs/ → desk_pro_dashboard doit rester fonctionnel
```

## 17_RESUME_POINT

```text
CONSOLIDATION_UI_CLUSTER_01 ouvert.
6 composants → 1 hub modules/desk_pro/{runner,orchestrator,dashboard,scanner,registry}
Hub desk_pro déjà existant, 5 migrations entrantes.
Prochaine action : validation → inventaire → plan de migration → closeout.
```
