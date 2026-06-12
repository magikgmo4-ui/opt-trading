---
doc_id: OPT_TRADING_MULTI_AGENTS_INDEX_PATCH_01
doc_type: index_patch
repo: opt-trading
project: opt-trading
module: multi_agents
go_id: GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01
status: ready
lifecycle_stage: index_patch
topic_keys:
  - opt-trading
  - multi_agents
  - index_patch
  - go_index
  - active_streams
  - next_go_candidates
  - reprise
search_tags:
  - surface:chantier
  - doc_role:index_patch
  - index:ready
  - aggregation:pending
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
point_de_reprise: "docs/index/inbox/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01.md"
updated_at: 2026-04-26
links:
  - docs/chantiers/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01/PARENT_STATE.md
  - docs/chantiers/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01/NEXT.md
  - docs/chantiers/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01/ACTIVE.md
  - docs/chantiers/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01/DECISIONS.md
---

# INDEX_PATCH — GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01

## Statut de propagation

- statut : `READY`
- propagation globale : `PENDING_AGGREGATION`
- modification directe des gros index : non faite volontairement

## Entrée proposée — GO_INDEX.md

```markdown
| GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01 | GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01 | — | OPEN | oui | `docs/chantiers/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01/00_INITIAL_PROJECT_DOC.md`<br>`docs/chantiers/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01/PARENT_STATE.md`<br>`docs/chantiers/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01/INDEX_PATCH.md` |
```

## Entrée proposée — ACTIVE_STREAMS.md

```markdown
### GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01
- statut : active
- repo : opt-trading
- branche : `go/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01`
- dernier point établi : chantier parent doc-only ouvert pour canoniser la doctrine multi-agents, avec continuité parent locale sans modification systématique des index globaux
- prochaine action : ouvrir `GO_OPT_TRADING_PARENT_CONTINUITY_INDEX_INBOX_METHOD_01` ou agréger ce patch dans un batch d'indexation
- blocages : aucun runtime ; propagation globale différée volontairement
```

## Entrée proposée — NEXT_GO_CANDIDATES.md

```markdown
| `GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01` | open | P1 | `GO_OPT_TRADING_PARENT_CONTINUITY_INDEX_INBOX_METHOD_01` | canoniser la méthode parent-local + inbox + batch, puis appliquer un premier batch d'agrégation | `docs/chantiers/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01/PARENT_STATE.md` |
```

## Entrée proposée — REPRISE.md

```markdown
| `GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01` | open | P1 | `docs/chantiers/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01/PARENT_STATE.md`; `docs/chantiers/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01/INDEX_PATCH.md` | continuité parent locale complète posée ; méthode local-first documentée | index globaux à agréger par batch ; closeout à produire après validation | ouvrir `GO_OPT_TRADING_PARENT_CONTINUITY_INDEX_INBOX_METHOD_01` ou exécuter un batch d'agrégation |
```

## Entrée proposée — docs/index/BRANCH_STATE.md

```markdown
| `go/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01` | `sot/mainline` | `GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01` | OPEN | branche dédiée doc-only pour canonisation doctrine multi-agents | `docs/chantiers/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01/BRANCH_STATE.md` |
```

## Notes d'agrégation

- appliquer uniquement depuis un environnement local ou outil capable de lire les fichiers complets ;
- produire un diff minimal ;
- ne pas remplacer les index globaux entiers ;
- après application, passer ce fichier à `APPLIED` ou créer un closeout d'agrégation.

## RISKS

- À qualifier.
