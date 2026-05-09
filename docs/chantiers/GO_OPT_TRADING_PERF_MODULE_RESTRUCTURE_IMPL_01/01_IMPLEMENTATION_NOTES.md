---
doc_id: GO_OPT_TRADING_PERF_MODULE_RESTRUCTURE_IMPL_01_IMPLEMENTATION_NOTES
doc_type: implementation_notes
repo: opt-trading
project: opt-trading
module: product
go_id: GO_OPT_TRADING_PERF_MODULE_RESTRUCTURE_IMPL_01
status: draft_for_review
lifecycle_stage: child_implementation_notes
parent_go_id: GO_OPT_TRADING_PERF_MODULE_RESTRUCTURE_PLAN_01
topic_keys:
  - opt-trading
  - perf
  - implementation
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_PERF_MODULE_RESTRUCTURE_IMPL_01/01_IMPLEMENTATION_NOTES.md
point_de_reprise: "Tracer les nouveaux shims et la compatibilite preservee."
updated_at: 2026-05-07
links:
  - docs/chantiers/GO_OPT_TRADING_PERF_MODULE_RESTRUCTURE_IMPL_01/00_CADRAGE.md
---

# 01_IMPLEMENTATION_NOTES

## 1_FICHIERS AJOUTES

```text
modules/perf/app.py
modules/perf/webhook.py
modules/perf/engine/README.md
modules/perf/engine/__init__.py
modules/perf/engine/app/__init__.py
modules/perf/engine/app/perf_engine.py
```

## 2_FICHIERS MODIFIES

```text
modules/perf/README.md
modules/perf/__init__.py
```

## 3_COMPATIBILITE PRESERVEE

```text
Ancien chemin conserve : perf.perf_app:app
Nouveau chemin disponible : modules.perf.app:app

Ancien chemin conserve : modules.perf_engine.app.perf_engine
Nouveau chemin disponible : modules.perf.engine.app.perf_engine

Ancien chemin conserve : adapters.webhook_to_perf
Nouveau chemin disponible : modules.perf.webhook
```

## 4_DECISION DIFFEREE

```text
Le deplacement physique des fichiers et de la DB reste differe.
Ce lot installe la structure canonique sans casser l'existant.
```
