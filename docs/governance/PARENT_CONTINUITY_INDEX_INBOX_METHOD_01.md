---
doc_id: OPT_TRADING_PARENT_CONTINUITY_INDEX_INBOX_METHOD_01
doc_type: governance_method
repo: opt-trading
project: opt-trading
module: governance
go_id: GO_OPT_TRADING_PARENT_CONTINUITY_INDEX_INBOX_METHOD_01
status: proposed
lifecycle_stage: governance_candidate
topic_keys:
  - opt-trading
  - governance
  - parent_continuity
  - index_inbox
  - indexation
  - go_index
  - active_streams
  - next_go_candidates
  - reprise
search_tags:
  - surface:governance
  - doc_role:governance_method
  - governance:parent_continuity
  - governance:index_inbox
  - index:local_first
  - aggregation:batch
surface: governance
source_kind: canonical
reference_canonique_principale: docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
point_de_reprise: "Section 12 - Méthode canonique proposée"
updated_at: 2026-04-26
links:
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
  - docs/chantiers/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01/08_PARENT_CONTINUITY_WITHOUT_GLOBAL_INDEX_METHOD.md
  - docs/chantiers/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01/09_INDEX_INBOX_ATOMIC_ENTRY_CONVENTION.md
  - docs/chantiers/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01/INDEX_PATCH.md
  - docs/index/inbox/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01.md
---

# PARENT_CONTINUITY_INDEX_INBOX_METHOD_01

## 1. Objet

Proposer une méthode canonique pour garder la continuité dans chaque chantier parent sans modifier systématiquement les gros index globaux.

Cette méthode vise à réduire :

- les conflits Git ;
- les diffs massifs ;
- les remplacements accidentels de fichiers volumineux ;
- la friction liée aux connecteurs ou outils qui peuvent tronquer de longs fichiers.

## 2. Problème ciblé

Les fichiers suivants restent nécessaires comme vues consolidées globales :

- `docs/index/GO_INDEX.md`
- `docs/index/ACTIVE_STREAMS.md`
- `docs/index/NEXT_GO_CANDIDATES.md`
- `docs/index/REPRISE.md`

Mais ils ne doivent plus être utilisés comme fichiers de travail quotidien par chaque chantier.

## 3. Principe directeur

```text
Parent continuity first
→ index inbox atomique
→ batch d'agrégation
→ index globaux consolidés
```

Chaque parent porte sa reprise locale complète. Les index globaux restent canoniques, mais ils sont mis à jour par lots contrôlés.

## 4. Structure locale parent recommandée

Pour chaque parent significatif :

```text
docs/chantiers/<GO_ID>/
  00_INITIAL_PROJECT_DOC.md
  PARENT_STATE.md
  NEXT.md
  ACTIVE.md
  DECISIONS.md
  INDEX_PATCH.md
  BRANCH_STATE.md si branche dédiée
  GAP_INDEXATION.md si propagation non faite
  90_CLOSEOUT.md ou 90_CLOSEOUT_DRAFT.md
```

## 5. Rôle des fichiers locaux

| Fichier | Rôle |
| --- | --- |
| `PARENT_STATE.md` | état canonique courant du parent |
| `NEXT.md` | prochaine action locale du parent |
| `ACTIVE.md` | statut actif/bloqué local |
| `DECISIONS.md` | décisions, refus, hypothèses, invariants |
| `INDEX_PATCH.md` | entrées prêtes à agréger vers les index globaux |
| `BRANCH_STATE.md` | trace Git locale si branche dédiée |
| `GAP_INDEXATION.md` | écart documenté si propagation différée |

## 6. Index inbox atomique

Format obligatoire :

```text
docs/index/inbox/<GO_ID>.md
```

Règle :

```text
1 GO_ID = 1 fichier inbox atomique
```

Interdit :

```text
docs/index/INBOX.md
```

Raison : un fichier inbox global unique recréerait un gros fichier conflictuel.

## 7. Frontmatter minimal inbox

```yaml
doc_id: OPT_TRADING_INDEX_INBOX_<GO_ID>
doc_type: index_inbox_entry
repo: opt-trading
project: opt-trading
module:
go_id: <GO_ID>
status: ready
lifecycle_stage: inbox
topic_keys:
  - opt-trading
  - index_inbox
  - aggregation
  - parent_continuity
search_tags:
  - surface:index_inbox
  - doc_role:index_inbox_entry
  - aggregation:ready
  - index:local_first
surface: index
source_kind: derived
reference_canonique_principale: docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
point_de_reprise: docs/chantiers/<GO_ID>/INDEX_PATCH.md
updated_at: YYYY-MM-DD
applied_at:
applied_by_go:
archive_after_apply: false
links:
  - docs/chantiers/<GO_ID>/PARENT_STATE.md
  - docs/chantiers/<GO_ID>/INDEX_PATCH.md
```

## 8. Tags d'agrégation

Tags autorisés :

```text
aggregation:pending
aggregation:ready
aggregation:applied
aggregation:blocked
aggregation:superseded
index:local_first
index:global_synced
surface:index_inbox
doc_role:index_inbox_entry
```

## 9. Statuts d'agrégation

| status | lifecycle_stage | Sens |
| --- | --- | --- |
| `pending` | `inbox` | entrée créée, pas encore prête |
| `ready` | `inbox` | prête pour agrégation |
| `applied` | `aggregated` | appliquée aux index globaux |
| `blocked` | `inbox_blocked` | conflit, troncature ou décision manquante |
| `superseded` | `superseded` | remplacée par une entrée plus récente |

## 10. Batch d'agrégation

Un GO dédié applique les entrées locales vers les index globaux, par exemple :

```text
GO_OPT_TRADING_INDEX_AGGREGATION_BATCH_01
```

Ce batch doit :

- lire les `INDEX_PATCH.md` ;
- lire `docs/index/inbox/<GO_ID>.md` ;
- appliquer les entrées dans les gros index ;
- produire un diff minimal ;
- marquer les entrées inbox comme `applied` ou documenter le blocage ;
- produire un closeout.

## 11. Conditions pour modifier directement les index globaux

Modification directe autorisée seulement si :

- le fichier complet est disponible ;
- le diff est minimal ;
- le chantier est court ou non concurrent ;
- aucun risque de troncature ;
- la modification est liée à un closeout ou batch d'agrégation ;
- le changement est journalisé.

Sinon, utiliser la continuité locale parent et l'inbox atomique.

## 12. Méthode canonique proposée

Pour tout nouveau chantier parent :

```text
1. Créer docs/chantiers/<GO_ID>/00_INITIAL_PROJECT_DOC.md.
2. Créer PARENT_STATE.md, NEXT.md, ACTIVE.md, DECISIONS.md.
3. Créer INDEX_PATCH.md avec les entrées prêtes à agréger.
4. Créer docs/index/inbox/<GO_ID>.md comme carte courte atomique.
5. Ne pas modifier systématiquement GO_INDEX / ACTIVE_STREAMS / NEXT_GO_CANDIDATES / REPRISE.
6. Agréger par GO batch dédié.
```

## 13. Application pilote

Application pilote :

```text
GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01
```

Fichiers pilotes :

- `docs/chantiers/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01/PARENT_STATE.md`
- `docs/chantiers/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01/INDEX_PATCH.md`
- `docs/index/inbox/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01.md`

## 14. Statut

Statut actuel : `proposed`.

Cette méthode devient canonique globale après validation humaine et merge de la PR associée.

## 15. Point de reprise

Prochaine action après merge : ouvrir ou exécuter :

```text
GO_OPT_TRADING_INDEX_AGGREGATION_BATCH_01
```
