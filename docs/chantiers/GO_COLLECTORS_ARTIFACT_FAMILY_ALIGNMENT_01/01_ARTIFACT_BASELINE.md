---
doc_id: GO_COLLECTORS_ARTIFACT_FAMILY_ALIGNMENT_01_ARTIFACT_BASELINE
doc_type: artifact_baseline
repo: opt-trading
project: opt-trading
module: product
go_id: GO_COLLECTORS_ARTIFACT_FAMILY_ALIGNMENT_01
status: draft_for_review
lifecycle_stage: child_artifact_baseline
parent_go_id: GO_COLLECTORS_VOCABULARY_ALIGNMENT_01
topic_keys:
  - opt-trading
  - collectors
  - artifacts
  - baseline
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_COLLECTORS_ARTIFACT_FAMILY_ALIGNMENT_01/01_ARTIFACT_BASELINE.md
point_de_reprise: "Poser le baseline actuel des sorties collectors."
updated_at: 2026-05-07
links:
  - docs/chantiers/GO_COLLECTORS_BASELINE_INVENTORY_01/01_DERIVATIVES_BASELINE.md
---

# 01_ARTIFACT_BASELINE

## 1_DERIVATIVES_COLLECTOR

```text
Sorties historiques confirmées :
- JSON legacy exports
- CSV legacy exports

Sorties famille déjà prévues dans la doctrine :
- manifest.json
- status.json
- latest.json
- events.jsonl
- errors.jsonl
```

## 2_SPOT COLLECTORS

```text
collector_coingecko / collector_binance_spot :
- outputs/raw/
- outputs/normalized/
- outputs/snapshots/

Leur convergence vers la famille d’artefacts doit être exprimée
dans le même vocabulaire sans casser leurs payloads spot.
```

## 3_RULE OF READING

```text
artifact family doctrine = enveloppe lifecycle commune
payload semantics        = restent spécifiques spot ou derives
```
