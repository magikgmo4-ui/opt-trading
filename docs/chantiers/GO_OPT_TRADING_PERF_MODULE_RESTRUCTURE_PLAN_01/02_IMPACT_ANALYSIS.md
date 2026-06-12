---
doc_id: GO_OPT_TRADING_PERF_MODULE_RESTRUCTURE_PLAN_01_IMPACT_ANALYSIS
doc_type: impact_analysis
repo: opt-trading
project: opt-trading
module: product
go_id: GO_OPT_TRADING_PERF_MODULE_RESTRUCTURE_PLAN_01
status: draft_for_review
lifecycle_stage: child_impact_analysis
parent_go_id: GO_OPT_TRADING_CONSOLIDATION_PERF_CLUSTER_01
topic_keys:
  - opt-trading
  - perf
  - impact
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_PERF_MODULE_RESTRUCTURE_PLAN_01/02_IMPACT_ANALYSIS.md
point_de_reprise: "Lister tous les impacts connus d'une restructuration PERF."
updated_at: 2026-05-07
links:
  - docs/chantiers/GO_OPT_TRADING_PERF_MODULE_RESTRUCTURE_PLAN_01/01_TARGET_SHAPE.md
---

# 02_IMPACT_ANALYSIS

## 1_IMPACTS DIRECTS

```text
I1. uvicorn path actuel : perf.perf_app:app
I2. SQLite path actuel : perf/perf.db
I3. shell facade actuelle : modules/perf/
I4. subprocess actuel desk_pro_orchestrator : modules.perf_engine.app.perf_engine
I5. webhook adapter actuel : adapters/webhook_to_perf.py
```

## 2_IMPACTS A VERIFIER AU GO D'IMPLEMENTATION

```text
- scripts de lancement / restart perf
- verify_all.sh et autres sanity scripts
- docs qui referencent perf/perf_app.py
- callers futurs ou externes de webhook_to_perf
- backup et migration de la base SQLite
```

## 3_RISQUES

```text
R1. casser le service perf actif
R2. casser les scripts d'exploitation
R3. perdre ou deplacer la DB sans migration propre
R4. casser le mount desk_pro
R5. laisser des references melangees entre ancien et nouveau layout
```

## RISKS

- À qualifier.
