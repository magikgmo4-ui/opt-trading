---
doc_id: GO_COLLECTORS_ARTIFACT_FAMILY_ALIGNMENT_01_CADRAGE
doc_type: cadrage
repo: opt-trading
project: opt-trading
module: product
go_id: GO_COLLECTORS_ARTIFACT_FAMILY_ALIGNMENT_01
status: draft_for_review
lifecycle_stage: child_cadrage
parent_go_id: GO_COLLECTORS_VOCABULARY_ALIGNMENT_01
topic_keys:
  - opt-trading
  - collectors
  - artifacts
  - alignment
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_COLLECTORS_ARTIFACT_FAMILY_ALIGNMENT_01/00_CADRAGE.md
point_de_reprise: "Aligner la famille d'artefacts collectors sans casser les sorties existantes."
updated_at: 2026-05-07
links:
  - docs/COLLECTORS_MIGRATION_MAP_01.md
  - docs/COLLECTORS_FAMILY_DOCTRINE_01.md
---

# 00_CADRAGE — GO_COLLECTORS_ARTIFACT_FAMILY_ALIGNMENT_01

## 1_MASTER_TARGET

Aligner les artefacts de la famille COLLECTORS autour de la doctrine :
`manifest.json`, `status.json`, `latest.json`, `events.jsonl`, `errors.jsonl`.

## 2_REGLE CENTRALE

```text
Ne pas retirer les exports JSON / CSV historiques.
Ajouter la doctrine famille de façon additive uniquement.
```

## 3_SCOPE

```text
INCLUS : baseline, mapping doctrine, règles d’adoption additive.
EXCLUS : changement runtime, suppression d’artefacts legacy, schema unification.
```

## 12_INVARIANTS

```text
- docs only
- 0 runtime
- 0 suppression legacy outputs
- 0 changement de semantics derives
```
