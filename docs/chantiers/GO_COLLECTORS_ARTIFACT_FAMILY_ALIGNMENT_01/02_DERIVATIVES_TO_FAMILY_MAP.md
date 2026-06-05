---
doc_id: GO_COLLECTORS_ARTIFACT_FAMILY_ALIGNMENT_01_DERIVATIVES_TO_FAMILY_MAP
doc_type: artifact_map
repo: opt-trading
project: opt-trading
module: product
go_id: GO_COLLECTORS_ARTIFACT_FAMILY_ALIGNMENT_01
status: draft_for_review
lifecycle_stage: child_artifact_map
parent_go_id: GO_COLLECTORS_VOCABULARY_ALIGNMENT_01
topic_keys:
  - opt-trading
  - collectors
  - artifacts
  - derivatives
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_COLLECTORS_ARTIFACT_FAMILY_ALIGNMENT_01/02_DERIVATIVES_TO_FAMILY_MAP.md
point_de_reprise: "Mapper derivatives_collector vers la doctrine d'artefacts famille."
updated_at: 2026-05-07
links:
  - docs/COLLECTORS_MIGRATION_MAP_01.md
---

# 02_DERIVATIVES_TO_FAMILY_MAP

## 1_TARGET FAMILY ARTIFACTS

| Family artifact | Rôle |
|---|---|
| `manifest.json` | contexte structurel du run + outputs produits |
| `status.json` | état synthétique courant/dernier run |
| `latest.json` | dernier payload valide orienté lecture rapide |
| `events.jsonl` | journal append-only des événements |
| `errors.jsonl` | journal append-only des erreurs |

## 2_MAPPING RULES FOR DERIVATIVES

```text
R1. conserver les exports JSON / CSV historiques comme sorties downstream valides
R2. ajouter les artefacts famille en parallèle, pas à la place
R3. ne pas forcer un latest.json qui écraserait la sémantique métier derives
R4. status.json doit rester synthétique et machine-readable
R5. manifest.json doit décrire les outputs produits, pas normaliser le payload métier
```

## 3_EXPECTED RESULT

```text
derivatives_collector devient compatible famille au niveau lifecycle / artifacts,
tout en restant spécifiquement dérivés au niveau payload.
```

## RISKS

- À qualifier.
