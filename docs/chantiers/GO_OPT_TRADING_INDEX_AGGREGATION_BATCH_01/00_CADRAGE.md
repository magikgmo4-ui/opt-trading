---
doc_id: OPT_TRADING_INDEX_AGGREGATION_BATCH_01_CADRAGE
doc_type: chantier_cadrage
repo: opt-trading
project: opt-trading
module: indexation
go_id: GO_OPT_TRADING_INDEX_AGGREGATION_BATCH_01
status: open
lifecycle_stage: cadrage
topic_keys:
  - opt-trading
  - indexation
  - aggregation
  - go_index
  - active_streams
  - next_go_candidates
  - reprise
  - index_inbox
search_tags:
  - surface:chantier
  - doc_role:cadrage
  - aggregation:batch
  - index:global_synced
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
point_de_reprise: "scripts/APPLY_INDEX_AGGREGATION_BATCH_01.ps1"
updated_at: 2026-04-26
links:
  - docs/governance/PARENT_CONTINUITY_INDEX_INBOX_METHOD_01.md
  - docs/chantiers/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01/INDEX_PATCH.md
  - docs/index/inbox/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01.md
---

# 00_CADRAGE — GO_OPT_TRADING_INDEX_AGGREGATION_BATCH_01

## Objet

Appliquer le premier batch d'agrégation des entrées `INDEX_PATCH.md` et `docs/index/inbox/<GO_ID>.md` vers les index globaux.

## Entrée batch cible

```text
GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01
```

Sources :

```text
docs/chantiers/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01/INDEX_PATCH.md
docs/index/inbox/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01.md
```

## Index globaux ciblés

```text
docs/index/GO_INDEX.md
docs/index/ACTIVE_STREAMS.md
docs/index/NEXT_GO_CANDIDATES.md
docs/index/REPRISE.md
```

## Règle de prudence

Les gros index globaux doivent être patchés depuis un environnement local qui lit les fichiers complets.

Le connecteur ne doit pas remplacer manuellement des fichiers volumineux si le risque de troncature existe.

## Stratégie retenue

Utiliser un script local :

```text
docs/chantiers/GO_OPT_TRADING_INDEX_AGGREGATION_BATCH_01/scripts/APPLY_INDEX_AGGREGATION_BATCH_01.ps1
```

Le script :

- vérifie que le repo est sur la branche batch ;
- applique les entrées du batch dans les quatre index globaux ;
- met à jour l'inbox en `applied` ;
- produit un diff local reviewable ;
- ne touche pas au runtime.

## Non-objectifs

- aucune mutation runtime ;
- aucun changement OpenClaw ;
- aucun trading live ;
- aucun patch hors documentation ;
- aucune agrégation d'autres GO non listés explicitement.

## Critère PASS

PASS si :

- les quatre index globaux contiennent l'entrée `GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01` ;
- l'inbox atomique est marquée `applied` ;
- un closeout batch est produit ;
- le diff reste doc-only.
