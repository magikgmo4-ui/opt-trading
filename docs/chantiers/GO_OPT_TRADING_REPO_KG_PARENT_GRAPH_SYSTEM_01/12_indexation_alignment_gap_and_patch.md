---
doc_id: GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01_INDEXATION_ALIGNMENT_GAP_AND_PATCH
doc_type: indexation_gap_and_patch
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01
status: OPEN
lifecycle_stage: indexation_alignment
topic_keys:
  - repo-graph
  - indexation
  - go-index
  - branch-state
  - matrice-doc-ops
search_tags:
  - indexation:gap_explicit
  - branch:dedicated
  - surface:continuity
source_kind: canonical
reference_canonique_principale: docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
point_de_reprise: "Appliquer les lignes exactes ci-dessous dans les surfaces souveraines via patch local contrôlé"
created_at: 2026-04-24
---

# 12 — Indexation alignment gap and patch

## 1_MASTER_TARGET

Tracer proprement l'indexation du chantier parent `GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01` sans corrompre les surfaces souveraines `GO_INDEX.md`, `REPRISE.md` ou `BRANCH_STATE.md`.

## 7_CANONICAL_STATE

- Branche dédiée réelle : `go/GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01`
- Dossier chantier réel : `docs/chantiers/GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01/`
- Documents parent déjà présents : `01` à `08`, puis `12` présent document
- `GO_INDEX.md` a été restauré après tentative d'écriture invalide ; le contenu canonique n'est pas modifié dans ce lot tant qu'un patch complet contrôlé n'est pas disponible.

## 13_ESTABLISHED

La matrice impose que l'ouverture d'un parent significatif soit propagée vers les surfaces de continuité adéquates.

Dans ce lot, le connecteur disponible remplace les fichiers complets et ne permet pas de patch ligne-à-ligne fiable. Pour éviter une nouvelle corruption, cette fiche tient lieu de `GAP_INDEXATION` explicite et fournit les lignes exactes à intégrer via patch local contrôlé.

## 15_REMAINING_GAP

### GAP_INDEXATION

Les surfaces suivantes doivent encore être modifiées dans un passage contrôlé :

- `docs/index/GO_INDEX.md`
- `docs/index/BRANCH_STATE.md`
- `docs/index/REPRISE.md` si le parent devient point de reprise opératoire principal
- `docs/index/ACTIVE_STREAMS.md` uniquement si le flux devient actif au sens opératoire strict

## 16_TODO

### Patch GO_INDEX.md

Insérer dans le tableau canonique des chantiers non clos :

```markdown
| GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01 | GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01 | — | OPEN | oui | `docs/chantiers/GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01/01_cadrage_parent.md`<br>`docs/chantiers/GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01/05_master_plan_final_product.md`<br>`docs/chantiers/GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01/06_graph_schema_v1.md` |
```

Ajouter dans la section `Entrées` :

```markdown
### GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01
- repo : opt-trading
- type : gouvernance / repo graph / producer-consumer / doc-only
- statut : open
- titre court : parent repo knowledge graph system
- dernier état connu : parent ouvert sur branche dédiée ; cadrage, recherche, plan final, schéma, Producer spec et Consumer Ace KG method documentés ; indexation canonique finale à appliquer via patch contrôlé
- lien utile : `docs/chantiers/GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01/01_cadrage_parent.md`, `docs/chantiers/GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01/05_master_plan_final_product.md`, `docs/chantiers/GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01/06_graph_schema_v1.md`, `docs/chantiers/GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01/07_producer_spec_v1.md`, `docs/chantiers/GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01/08_consumer_ace_kg_method_v1.md`
```

### Patch BRANCH_STATE.md

Ajouter une ligne au tableau canonique :

```markdown
| `go/GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01` | remote | AHEAD_ONLY | TBD | 0 | `KEEP_ACTIVE` | `keep_under_review` | Branche dédiée parent ouverte pour cadrage repo knowledge graph producer-consumer ; doc-only ; à revoir au closeout | `GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01` |
```

Note : `AHEAD_BY` doit être recalculé localement avec `git rev-list --left-right --count origin/sot/mainline...origin/go/GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01` avant écriture définitive.

### Patch REPRISE.md

Ajouter une entrée de reprise :

```markdown
### GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01
- statut : OPEN
- branche : `go/GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01`
- dossier : `docs/chantiers/GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01/`
- point de reprise : lire `05_master_plan_final_product.md`, `06_graph_schema_v1.md`, `07_producer_spec_v1.md`, `08_consumer_ace_kg_method_v1.md`
- prochaine action : produire `09_graph_views_v1.md`, puis `10_acceptance_tests_v1.md`
```

## 11_KEY_DECISIONS

- Ne pas réécrire une surface souveraine tronquée.
- Ne pas injecter de placeholder dans `GO_INDEX.md`.
- Préférer une trace `GAP_INDEXATION` explicite à une fausse conformité.
- Reprendre l'indexation via patch local contrôlé ou outil Git line-aware.

## 12_INVARIANTS

- `GO_INDEX.md` reste la vérité de liste.
- Cette fiche ne remplace pas `GO_INDEX.md`.
- Cette fiche documente le gap et les lignes exactes à intégrer.
- Le repo réel et la matrice priment.

## 17_RESUME_POINT

Reprise : appliquer les patches ci-dessus dans l'ordre :

1. `GO_INDEX.md`
2. `BRANCH_STATE.md`
3. `REPRISE.md`
4. `ACTIVE_STREAMS.md` seulement si le flux est déclaré actif

Puis créer `09_graph_views_v1.md`.

## RISKS

- À qualifier.
