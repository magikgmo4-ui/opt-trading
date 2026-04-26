---
doc_id: OPT_TRADING_MULTI_AGENTS_NEXT_01
doc_type: next_step
repo: opt-trading
project: opt-trading
module: multi_agents
go_id: GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01
status: open
lifecycle_stage: next
topic_keys:
  - opt-trading
  - multi_agents
  - next
  - continuity
  - parent_continuity
search_tags:
  - surface:chantier
  - doc_role:next_step
  - governance:parent_continuity
  - index:local_first
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
point_de_reprise: "ACTIVE.md"
updated_at: 2026-04-26
links:
  - docs/chantiers/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01/PARENT_STATE.md
  - docs/chantiers/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01/ACTIVE.md
  - docs/chantiers/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01/INDEX_PATCH.md
---

# NEXT — GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01

## Next action primaire

Créer la continuité parent locale complète sans toucher directement aux quatre index globaux.

## Séquence immédiate

1. Créer `PARENT_STATE.md`.
2. Créer `NEXT.md`.
3. Créer `ACTIVE.md`.
4. Créer `DECISIONS.md`.
5. Créer `INDEX_PATCH.md`.
6. Créer `docs/index/inbox/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01.md`.
7. Vérifier que le parent est autosuffisant pour la reprise.

## Next GO recommandé après ce parent

```text
GO_OPT_TRADING_PARENT_CONTINUITY_INDEX_INBOX_METHOD_01
```

Objectif : canoniser la méthode parent-local + inbox + batch dans une surface gouvernance ou architecture.

## Dépendances

- `08_PARENT_CONTINUITY_WITHOUT_GLOBAL_INDEX_METHOD.md` validé par GO utilisateur.
- Aucun patch direct requis sur `GO_INDEX.md`, `ACTIVE_STREAMS.md`, `NEXT_GO_CANDIDATES.md`, `REPRISE.md` à cette étape.

## Critère de passage

La continuité locale est complète si les fichiers suivants existent :

- `PARENT_STATE.md`
- `NEXT.md`
- `ACTIVE.md`
- `DECISIONS.md`
- `INDEX_PATCH.md`
- `docs/index/inbox/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01.md`

## Blocages

Aucun blocage runtime.

Blocage technique partiel : les index globaux volumineux ne doivent pas être modifiés via connecteur si contenu tronqué ou risque de remplacement excessif.
