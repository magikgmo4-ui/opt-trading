---
doc_id: OPT_TRADING_MULTI_AGENTS_CANON_PARENT_GAP_INDEXATION_01
doc_type: gap_indexation
repo: opt-trading
project: opt-trading
module: multi_agents
go_id: GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01
status: open
lifecycle_stage: indexation_gap
topic_keys:
  - opt-trading
  - multi_agents
  - indexation
  - go_index
  - active_streams
  - reprise
  - branch_state
search_tags:
  - surface:chantier
  - doc_role:gap_indexation
  - governance:indexation
  - branch:go/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
point_de_reprise: "propager proprement dans docs/index/* au lot d'alignement suivant"
updated_at: 2026-04-26
links:
  - docs/chantiers/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01/00_INITIAL_PROJECT_DOC.md
  - docs/chantiers/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01/BRANCH_STATE.md
  - docs/index/GO_INDEX.md
  - docs/index/NEXT_GO_CANDIDATES.md
  - docs/index/ACTIVE_STREAMS.md
  - docs/index/REPRISE.md
---

# GAP_INDEXATION — GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01

## Objet

Ce fichier pose explicitement le gap d'indexation du chantier parent multi-agents.

Le chantier est ouvert et documente sur branche dediee, mais la propagation vers les index globaux `docs/index/*` doit etre faite proprement dans un lot dedie, pour eviter de reecrire partiellement des fichiers volumineux ou tronques.

## Etat etabli

- branche dediee creee : `go/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01`
- dossier chantier cree : `docs/chantiers/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01/`
- document initial autonome cree : `00_INITIAL_PROJECT_DOC.md`
- branch state local cree : `BRANCH_STATE.md`
- phase courante : doc-only
- runtime mutation : interdite

## Propagation attendue

### `docs/index/GO_INDEX.md`

Ajouter une ligne canonique :

```text
| GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01 | GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01 | — | OPEN | oui | `docs/chantiers/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01/00_INITIAL_PROJECT_DOC.md`<br>`docs/chantiers/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01/BRANCH_STATE.md` |
```

### `docs/index/NEXT_GO_CANDIDATES.md`

Ajouter le parent actif avec next primaire :

```text
parent: GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01
status: open
priority: P1
next GO primaire: aucun nouveau GO
next action: produire `01_EXISTING_SOCLE_READOUT.md`, puis `02_AGENT_SKILL_PROVIDER_MATRIX.md`
refs: docs/chantiers/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01/00_INITIAL_PROJECT_DOC.md
```

### `docs/index/ACTIVE_STREAMS.md`

Ajouter le flux actif :

```text
GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01
- statut : open
- repo : opt-trading
- branche : go/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01
- dernier point etabli : chantier parent doc-only ouvert pour canoniser la doctrine multi-agents Codex / Claude / Trae / Ollama avec OpenClaw orchestrateur borne
- prochaine action : produire `01_EXISTING_SOCLE_READOUT.md`, puis matrice agents/skills/providers
- blocages : aucun blocage runtime ; propagation index globale encore a faire proprement
```

### `docs/index/REPRISE.md`

Ajouter une entree de reprise :

```text
GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01
- status : open
- priority : P1
- canonical refs : `docs/chantiers/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01/00_INITIAL_PROJECT_DOC.md`; `docs/chantiers/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01/BRANCH_STATE.md`
- etat etabli : socle GitHub lu, workflow_ai / validated_prompt_factory / deploy_module_multi_machine reconnus, OpenClaw borne comme orchestrateur experimental/provider cloisonne
- gap restant : recherche approfondie + matrice agents/skills/providers + doctrine frontmatter/search_tags/naming + plan bundle execution
- next action : produire `01_EXISTING_SOCLE_READOUT.md`
```

### `docs/index/BRANCH_STATE.md`

Si la surface globale `docs/index/BRANCH_STATE.md` est creee ou reactivee, ajouter :

```text
branch: go/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01
base: sot/mainline
base_commit_observe: 4934eefcbc373e0f33167a24f35443fad46a8c80
go_id: GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01
status: open
role: branche dediee doc-only pour doctrine multi-agents
```

## Decision de prudence

Ne pas patcher les index globaux dans ce commit tant que le contenu complet n'est pas relu et manipule localement sans risque de troncature.

Cette `GAP_INDEXATION` satisfait l'exigence minimale d'indexation explicite pour une branche parent ouverte, tout en preservant l'integrite des surfaces globales.

## Point de reprise

Prochaine action : produire `01_EXISTING_SOCLE_READOUT.md` puis appliquer proprement les propagations d'indexation lors du lot d'alignement suivant.

## RISKS

- À qualifier.
