---
doc_id: GO_COLLECTORS_CONFIG_BOUNDARY_ALIGNMENT_01_BOUNDARY_MAP
doc_type: boundary_map
repo: opt-trading
project: opt-trading
module: product
go_id: GO_COLLECTORS_CONFIG_BOUNDARY_ALIGNMENT_01
status: draft_for_review
lifecycle_stage: child_boundary_map
parent_go_id: GO_COLLECTORS_ARTIFACT_FAMILY_ALIGNMENT_01
topic_keys:
  - opt-trading
  - collectors
  - config
  - boundary-map
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_COLLECTORS_CONFIG_BOUNDARY_ALIGNMENT_01/01_BOUNDARY_MAP.md
point_de_reprise: "Fixer la target boundary config pour derives et spot collectors."
updated_at: 2026-05-07
links:
  - docs/chantiers/GO_COLLECTORS_CONFIG_BOUNDARY_ALIGNMENT_01/00_CADRAGE.md
---

# 01_BOUNDARY_MAP

## 1_TARGET BOUNDARY

```text
Layer 1 : committed defaults
  - fichiers versionnes
  - valeurs sures / non sensibles

Layer 2 : machine-local overrides
  - fichiers non versionnes machine-specifiques
  - chemins, throttling, endpoints locaux, toggles operatoires

Layer 3 : env overrides
  - surcharge ponctuelle par variables d'environnement
  - priorite la plus haute sur les valeurs non secretes

Layer 4 : secrets boundary
  - credentials / tokens / keys hors repo
  - jamais commites
```

## 2_APPLICATION FAMILLE

```text
derivatives_collector
  - temporairement sur chemin de compatibilite si son modele config differe

collector_coingecko / collector_binance_spot
  - plus proches du modele cible via collectors_core

collectors_core
  - supporte la target boundary comme fondation commune
```

## 3_NON GOALS

```text
- ne pas homogeniser de force tous les formats de config maintenant
- ne pas deplacer les secrets dans le repo
- ne pas convertir toute la famille en une seule implementation config
```

## RISKS

- À qualifier.
