---
doc_id: OPT_TRADING_MULTI_AGENTS_PARENT_STATE_01
doc_type: parent_state
repo: opt-trading
project: opt-trading
module: multi_agents
go_id: GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01
status: open
lifecycle_stage: continuity
topic_keys:
  - opt-trading
  - multi_agents
  - parent_state
  - continuity
  - governance
  - local_first_indexation
search_tags:
  - surface:chantier
  - doc_role:parent_state
  - governance:parent_continuity
  - index:local_first
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
point_de_reprise: "NEXT.md"
updated_at: 2026-04-26
links:
  - docs/chantiers/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01/00_INITIAL_PROJECT_DOC.md
  - docs/chantiers/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01/08_PARENT_CONTINUITY_WITHOUT_GLOBAL_INDEX_METHOD.md
  - docs/chantiers/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01/NEXT.md
  - docs/chantiers/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01/INDEX_PATCH.md
---

# PARENT_STATE — GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01

## Objet

Etat canonique local du parent, pour garder la continuite sans modifier systematiquement les index globaux.

## Statut

- status : `OPEN`
- phase : canonisation documentaire multi-agents
- branche : `go/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01`
- type : doc-only
- runtime mutation : interdite

## Objectif parent

Canoniser la doctrine multi-agents `Codex / Claude / Trae / Ollama` avec OpenClaw comme orchestrateur experimental borne, en alignant :

- matrice gouvernante ;
- matrice operationnelle ;
- naming ;
- frontmatter ;
- search tags ;
- indexation ;
- continuité parent locale ;
- méthode d'agrégation vers les index globaux.

## Etat établi

- branche dédiée créée ;
- document initial autonome créé ;
- socle existant lu et documenté ;
- matrice agents / skills / providers créée ;
- doctrine frontmatter / search_tags / naming créée ;
- plan d'intégration opérationnelle créé ;
- plan de bundle créé ;
- prompt de bundle créé ;
- méthode transitoire d'indexation globale documentée ;
- méthode parent-local continuity documentée.

## Décision courante

Ne pas modifier les quatre index globaux à chaque étape.

Maintenir la continuité dans le parent via :

- `PARENT_STATE.md` ;
- `NEXT.md` ;
- `ACTIVE.md` ;
- `DECISIONS.md` ;
- `INDEX_PATCH.md` ;
- `docs/index/inbox/<GO_ID>.md`.

## Gap restant

- propager la méthode dans un chantier de gouvernance dédié si validation ;
- corriger éventuellement `docs/index/BRANCH_STATE.md` frontmatter localement ;
- créer un batch d'agrégation global ;
- générer physiquement le bundle zip si nécessaire ;
- closeout parent après validation.

## Prochaine action

Lire `NEXT.md`.
