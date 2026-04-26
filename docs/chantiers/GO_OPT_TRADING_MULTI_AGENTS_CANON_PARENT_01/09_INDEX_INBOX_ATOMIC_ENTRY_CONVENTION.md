---
doc_id: OPT_TRADING_MULTI_AGENTS_INDEX_INBOX_ATOMIC_ENTRY_CONVENTION_01
doc_type: convention
repo: opt-trading
project: opt-trading
module: multi_agents
go_id: GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01
status: open
lifecycle_stage: convention
topic_keys:
  - opt-trading
  - index_inbox
  - inbox_atomic_entry
  - aggregation
  - frontmatter
  - search_tags
  - parent_continuity
  - local_first_indexation
search_tags:
  - surface:chantier
  - doc_role:convention
  - index:inbox_atomic
  - aggregation:method
  - governance:parent_continuity
  - governance:search_tags
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
point_de_reprise: "Appliquer la convention aux prochaines entrées docs/index/inbox/<GO_ID>.md"
updated_at: 2026-04-26
links:
  - docs/chantiers/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01/08_PARENT_CONTINUITY_WITHOUT_GLOBAL_INDEX_METHOD.md
  - docs/chantiers/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01/INDEX_PATCH.md
  - docs/index/inbox/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01.md
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
---

# 09_INDEX_INBOX_ATOMIC_ENTRY_CONVENTION

## 1. Objet

Définir la convention minimale pour les entrées atomiques :

```text
docs/index/inbox/<GO_ID>.md
```

Cette convention évite de recréer un gros fichier inbox global et permet une agrégation propre vers les index globaux.

## 2. Invariant principal

```text
1 GO parent = 1 fichier inbox atomique
```

Interdit :

```text
docs/index/INBOX.md
```

Raison : un fichier inbox global unique redeviendrait volumineux et créerait le même problème que les index globaux.

## 3. Rôle d'une entrée inbox

Une entrée inbox sert à signaler qu'un chantier parent possède une indexation prête ou à traiter.

Elle ne remplace pas :

- `GO_INDEX.md` ;
- `ACTIVE_STREAMS.md` ;
- `NEXT_GO_CANDIDATES.md` ;
- `REPRISE.md` ;
- `INDEX_PATCH.md` du parent ;
- `PARENT_STATE.md` du parent.

Elle sert de carte courte pour un futur batch d'agrégation.

## 4. Nom de fichier

Format obligatoire :

```text
docs/index/inbox/<GO_ID>.md
```

Exemple :

```text
docs/index/inbox/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01.md
```

## 5. Frontmatter recommandé

```yaml
doc_id: OPT_TRADING_INDEX_INBOX_<GO_ID>
doc_type: index_inbox_entry
repo: opt-trading
project: opt-trading
module: <module_or_empty>
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

## 6. Sections type

Chaque entrée inbox doit rester courte.

Sections recommandées :

```text
# INDEX INBOX — <GO_ID>

## 1. Résumé
## 2. Delta attendu
## 3. Références parent
## 4. Index globaux ciblés
## 5. Statut d'agrégation
## 6. Post-agrégation
```

## 7. Statuts frontmatter

| status | lifecycle_stage | Sens |
| --- | --- | --- |
| `pending` | `inbox` | entrée créée, pas encore prête |
| `ready` | `inbox` | prête pour agrégation |
| `applied` | `aggregated` | appliquée aux index globaux |
| `blocked` | `inbox_blocked` | bloquée par conflit, troncature ou décision manquante |
| `superseded` | `superseded` | remplacée par une autre entrée |

## 8. Tags d'agrégation

### 8.1 Pending

```yaml
search_tags:
  - surface:index_inbox
  - doc_role:index_inbox_entry
  - aggregation:pending
  - index:local_first
```

### 8.2 Ready

```yaml
search_tags:
  - surface:index_inbox
  - doc_role:index_inbox_entry
  - aggregation:ready
  - index:local_first
```

### 8.3 Applied

```yaml
search_tags:
  - surface:index_inbox
  - doc_role:index_inbox_entry
  - aggregation:applied
  - index:global_synced
```

### 8.4 Blocked

```yaml
search_tags:
  - surface:index_inbox
  - doc_role:index_inbox_entry
  - aggregation:blocked
  - index:local_first
```

### 8.5 Superseded

```yaml
search_tags:
  - surface:index_inbox
  - doc_role:index_inbox_entry
  - aggregation:superseded
  - index:local_first
```

## 9. Champs post-agrégation

Quand l'entrée est appliquée :

```yaml
status: applied
lifecycle_stage: aggregated
applied_at: YYYY-MM-DD
applied_by_go: GO_OPT_TRADING_INDEX_AGGREGATION_BATCH_XX
archive_after_apply: true
```

## 10. Politique d'archivage

Deux options sont autorisées :

### Option A — Conserver comme preuve

Garder le fichier inbox avec :

```yaml
status: applied
lifecycle_stage: aggregated
archive_after_apply: false
```

### Option B — Archiver après application

Déplacer plus tard vers :

```text
docs/index/inbox/_archive/<GO_ID>.md
```

ou une surface équivalente si la politique d'archive est canonisée.

## 11. Relation avec INDEX_PATCH.md

`INDEX_PATCH.md` reste le document détaillé.

L'inbox doit seulement pointer vers lui.

```text
INDEX_PATCH.md = détail prêt à propager
inbox/<GO_ID>.md = carte courte d'agrégation
```

## 12. Relation avec PARENT_STATE.md

`PARENT_STATE.md` est la source de reprise locale du parent.

L'inbox ne doit pas recopier tout son contenu.

Elle doit seulement exposer :

- `go_id` ;
- `status` ;
- `branch` ;
- `last_established` ;
- `next_action` ;
- `index_patch_ref`.

## 13. Modèle minimal de contenu

```markdown
# INDEX INBOX — <GO_ID>

```yaml
go_id: <GO_ID>
status: ready
priority: P1
branch: <branch>
parent_ref: docs/chantiers/<GO_ID>/PARENT_STATE.md
last_established: >-
  Résumé court du dernier point établi.
next_action: >-
  Action attendue du batch d'agrégation.
index_patch_ref: docs/chantiers/<GO_ID>/INDEX_PATCH.md
updated_at: YYYY-MM-DD
aggregation_status: pending
```

## Note

Cette entrée inbox est atomique. Elle ne remplace pas les index globaux.
```

## 14. Application au chantier courant

L'entrée existante :

```text
docs/index/inbox/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01.md
```

respecte déjà l'esprit de cette convention :

- fichier séparé ;
- entrée courte ;
- `aggregation_status: pending` ;
- lien vers `PARENT_STATE.md` ;
- lien vers `INDEX_PATCH.md`.

Amélioration future possible : aligner son frontmatter avec les champs post-agrégation `applied_at`, `applied_by_go`, `archive_after_apply`.

## 15. Décision proposée

Adopter cette convention pour les prochains chantiers parents :

```text
1 GO_ID = 1 inbox file
No global INBOX.md
Inbox = short aggregation card
INDEX_PATCH.md = detailed propagation patch
PARENT_STATE.md = local continuity source
```

## 16. Point de reprise

Prochain geste possible :

- mettre à jour l'inbox du chantier courant avec les champs post-agrégation ;
- ouvrir `GO_OPT_TRADING_PARENT_CONTINUITY_INDEX_INBOX_METHOD_01` pour promouvoir cette convention au niveau gouvernance.
