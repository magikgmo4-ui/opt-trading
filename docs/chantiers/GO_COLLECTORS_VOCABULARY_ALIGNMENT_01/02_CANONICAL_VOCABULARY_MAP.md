---
doc_id: GO_COLLECTORS_VOCABULARY_ALIGNMENT_01_CANONICAL_VOCABULARY_MAP
doc_type: canonical_vocabulary_map
repo: opt-trading
project: opt-trading
module: product
go_id: GO_COLLECTORS_VOCABULARY_ALIGNMENT_01
status: draft_for_review
lifecycle_stage: child_vocabulary_map
parent_go_id: GO_COLLECTORS_BASELINE_INVENTORY_01
topic_keys:
  - opt-trading
  - collectors
  - vocabulary
  - canonical-map
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_COLLECTORS_VOCABULARY_ALIGNMENT_01/02_CANONICAL_VOCABULARY_MAP.md
point_de_reprise: "Fixer le vocabulaire canonique a reutiliser dans tous les runbooks collectors."
updated_at: 2026-05-07
links:
  - docs/chantiers/GO_COLLECTORS_VOCABULARY_ALIGNMENT_01/01_VOCABULARY_BASELINE.md
---

# 02_CANONICAL_VOCABULARY_MAP

## 1_MODULE IDENTITY

```text
module_id      = identite canonique du module (ex: derivatives_collector)
family_id      = collectors
provider_id    = coingecko | binance_spot | bitget | binance | mock | etc.
collector_type = derivatives | spot
```

## 2_RUN IDENTITY

```text
run_id         = identifiant unique du run
generated_at   = timestamp de generation d'artefact
collected_at   = timestamp de collecte de donnees
written_at     = timestamp d'ecriture disque si distinct
```

## 3_STATE / FRESHNESS

```text
state          = idle | running | partial | success | degraded | failed
freshness      = fresh | stale | unknown
latest         = dernier artefact valide
status         = photo synthetique du run courant/dernier run
manifest       = contexte structurel du run + outputs produits
```

## 4_ERROR VOCABULARY

```text
error_class    = network | auth | parse | validation | provider | filesystem | unknown
error_stage    = fetch | normalize | write | export | lifecycle
error_code     = code stable lisible machine
errors.jsonl   = journal append-only des erreurs
events.jsonl   = journal append-only des evenements de run
```
