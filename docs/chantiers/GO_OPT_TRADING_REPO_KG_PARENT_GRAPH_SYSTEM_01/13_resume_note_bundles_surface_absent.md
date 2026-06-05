---
doc_id: GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01_RESUME_NOTE_BUNDLES_SURFACE_ABSENT
doc_type: resume_note
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01
status: OPEN
lifecycle_stage: reprise
topic_keys:
  - repo-graph
  - bundles
  - reprise
  - ide-bundle
search_tags:
  - surface:bundles_absent
  - reprise:note
  - bundle:ide
source_kind: canonical
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01/12_indexation_alignment_gap_and_patch.md
point_de_reprise: "Ne pas supposer l'existence de /bundles/ tant que la surface n'est pas créée et canonisée"
created_at: 2026-04-24
---

# 13 — Note de reprise : surface `/bundles/` absente

## 13_ESTABLISHED

La surface repo `/bundles/` n'est pas présente actuellement dans le repo `opt-trading`.

Le bundle IDE du chantier `GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01` est donc posé provisoirement sous :

```text
docs/chantiers/GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01/ide_bundle/
```

## 11_KEY_DECISIONS

- Ne pas créer `/bundles/` implicitement dans ce lot.
- Ne pas supposer que `/bundles/` est une surface canonique existante.
- Conserver le bundle IDE dans le dossier chantier tant que la surface `/bundles/` n'est pas explicitement créée, cadrée et indexée.

## 15_REMAINING_GAP

Si une surface `/bundles/` devient souhaitée plus tard, ouvrir un GO dédié pour :

- cadrer son rôle ;
- définir son placement ;
- définir ses règles de contenu ;
- définir son lien avec `/shared/_bundles/` ;
- mettre à jour les surfaces d'indexation selon la matrice.

## 17_RESUME_POINT

Pour la reprise immédiate :

```text
Surface /bundles/ : ABSENTE
Bundle IDE courant : docs/chantiers/GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01/ide_bundle/
Action : ne pas déplacer avant GO dédié ou validation explicite
```

## RISKS

- À qualifier.
