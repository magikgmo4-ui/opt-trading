---
doc_id: GO_OPT_TRADING_CONSOLIDATION_PERF_CLUSTER_01_CADRAGE
doc_type: cadrage
repo: opt-trading
project: opt-trading
module: product
go_id: GO_OPT_TRADING_CONSOLIDATION_PERF_CLUSTER_01
status: draft_for_review
lifecycle_stage: child_cadrage
parent_go_id: GO_OPT_TRADING_AUDIT_ORPHAN_MODULES_01
topic_keys:
  - opt-trading
  - product-usage
  - atlas
  - consolidation
  - perf
  - docs-only
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_CONSOLIDATION_PERF_CLUSTER_01/00_CADRAGE.md
point_de_reprise: "Consolidation documentaire du cluster PERF : inventaire, carte, gaps. Pas de migration."
updated_at: 2026-05-07
links:
  - docs/chantiers/GO_OPT_TRADING_AUDIT_ORPHAN_MODULES_01/02_CONSOLIDATION_PLAN.md
  - docs/chantiers/GO_OPT_TRADING_CONSOLIDATION_STRATEGY_CLUSTER_01/90_CLOSEOUT.md
  - docs/chantiers/GO_OPT_TRADING_CONSOLIDATION_UI_CLUSTER_01/90_CLOSEOUT.md
---

# 00_CADRAGE — CONSOLIDATION_PERF_CLUSTER_01

## 1_MASTER_TARGET

Consolider l'inventaire, la carte des relations et les gaps du cluster PERF, **sans migrer, déplacer ni refactorer aucun code**.

## 2_CONSTAT

```text
PR #247 (STRATEGY) = merged PASS.
PR #248 (UI) = merged PASS.

Le cluster PERF compte 4 composants éclatés :
  modules/perf_engine/         → CLI standalone, produit perf_engine.json
  modules/perf/                → façade shell mince
  perf/perf_app.py             → FastAPI + SQLite, runtime actif (racine)
  adapters/webhook_to_perf.py  → adaptateur standalone, aucun caller trouvé

Ces 4 composants sont découplés en Python (zéro import croisé).
Ils communiquent via :
  - fichiers JSON (perf_engine.json → desk_pro_orchestrator)
  - HTTP (POST /perf/event → perf_app)
  - orchestration shell (scripts qui lancent uvicorn perf.perf_app:app)
```

## 3_PERIMETRE

```text
INCLUS :
  - Inventaire complet des 4 composants
  - Carte des relations (imports, data flow, orchestration)
  - Gaps documentaires et risques de restructuration
  - Proposition de NEXT_GO séparé si migration utile

EXCLUS :
  - Déplacement de fichiers
  - Changement d'imports
  - Changement uvicorn path
  - Changement SQLite path
  - Modification de desk_pro
  - Modification de webhook
  - Toute exécution de code
```

## 4_ARCHITECTURE_ACTUELLE

```text
[webhook] ──> adapters/webhook_to_perf.py ──> POST /perf/event ──> perf/perf_app.py (FastAPI :8010)
                 (aucun caller trouvé)                                   │
                                                                         ├── SQLite perf/perf.db
 modules/perf_engine/                                                    ├── /perf/ui HTML dashboard
 (CLI: python -m modules.perf_engine...)                                 ├── /perf/summary, /perf/trades...
     │                                                                   ├── Desk Pro mount /desk
     │ produit perf_engine.json                                          └── Telegram alerts
     └──> consommé par desk_pro_orchestrator
          et desk_pro_dashboard

 modules/perf/  (façade shell uniquement, pointe vers perf/perf_app.py)
```

## 12_INVARIANTS (stricts)

```text
- 0 migration de fichiers
- 0 déplacement de perf/perf_app.py
- 0 déplacement de modules/perf_engine/
- 0 déplacement d'adapters/webhook_to_perf.py
- 0 modification d'imports Python
- 0 changement de uvicorn module path
- 0 changement de SQLite path
- 0 modification de desk_pro
- 0 runtime
- 0 secret
- Documentation + inventaire + carte uniquement
```

## 17_RESUME_POINT

```text
CONSOLIDATION_PERF_CLUSTER_01 ouvert.
Docs-only. Inventaire → carte → gaps → closeout.
Toute restructuration → GO séparé PERF_MODULE_RESTRUCTURE_PLAN_01.
```

## RISKS

- À qualifier.
