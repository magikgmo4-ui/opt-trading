---
doc_id: GO_OPT_TRADING_PERF_DB_RELOCATION_IMPL_01_IMPLEMENTATION_NOTES
doc_type: implementation_notes
repo: opt-trading
project: opt-trading
module: product
go_id: GO_OPT_TRADING_PERF_DB_RELOCATION_IMPL_01
status: draft_for_review
lifecycle_stage: child_implementation_notes
parent_go_id: GO_OPT_TRADING_PERF_DB_RELOCATION_PLAN_01
topic_keys:
  - opt-trading
  - perf
  - db
  - implementation
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_PERF_DB_RELOCATION_IMPL_01/01_IMPLEMENTATION_NOTES.md
point_de_reprise: "Tracer l’outillage DB relocation ajouté."
updated_at: 2026-05-07
links:
  - docs/chantiers/GO_OPT_TRADING_PERF_DB_RELOCATION_IMPL_01/00_CADRAGE.md
---

# 01_IMPLEMENTATION_NOTES

## 1_FICHIERS AJOUTES

```text
modules/perf/data/README.md
modules/perf/scripts/perf_db_relocate.sh
```

## 2_COMPORTEMENT

```text
status    -> montre état legacy/canonical DB
copy      -> copie perf.db (+wal/+shm) vers modules/perf/data/perf.db
show-env  -> imprime l'override PERF_DB_PATH à utiliser pour la bascule
```

## 3_NON CHANGÉ

```text
- le runtime par défaut reste sur le chemin historique tant que PERF_DB_PATH n'est pas exporté
- aucune DB n'est déplacée automatiquement
```

## RISKS

- À qualifier.
