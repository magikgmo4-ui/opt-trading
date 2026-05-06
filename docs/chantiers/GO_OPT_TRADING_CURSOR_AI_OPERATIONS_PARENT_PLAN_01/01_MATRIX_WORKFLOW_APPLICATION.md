---
doc_id: OPT_TRADING_CURSOR_AI_OPERATIONS_PARENT_PLAN_01_MATRIX_WORKFLOW_APPLICATION
doc_type: matrix_workflow_application
repo: opt-trading
project: opt-trading
module:
go_id: GO_OPT_TRADING_CURSOR_AI_OPERATIONS_PARENT_PLAN_01
status: active
lifecycle_stage: parent_opening
topic_keys:
  - cursor-ai
  - matrix
  - workflow
  - active_continuity
surface: chantiers
source_kind: canonical
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_CURSOR_AI_OPERATIONS_PARENT_PLAN_01/00_INITIAL_PROJECT_DOC.md
point_de_reprise: "Section Decision appliquee"
updated_at: 2026-05-06
links:
  - docs/chantiers/GO_OPT_TRADING_CURSOR_AI_OPERATIONS_PARENT_PLAN_01/00_INITIAL_PROJECT_DOC.md
  - docs/index/MACHINE_WORK_SPLIT_ANTI_CONFLICT_01.md
  - docs/index/GO_INDEX.md
---

# Application matrice / workflow — cursor-ai

## Décision appliquée

Les blocs suivants sont rattachés au parent `GO_OPT_TRADING_CURSOR_AI_OPERATIONS_PARENT_PLAN_01` comme continuités actives `cursor-ai` :

| Bloc | Statut appliqué | Note |
| --- | --- | --- |
| `alert_webhook` | `ACTIVE_CONTINUITY` | application non fermée, déjà active |
| `Bundles` | `ACTIVE_CONTINUITY` | application documentée, validée comme continuité active à suivre dans le workflow |
| `Claude / Live artifacts` | `ACTIVE_CONTINUITY` | support artefacts / IDE / cowork actif |

## Portée

Cette application est documentaire et opératoire.

Elle ne modifie pas :
- le runtime ;
- les services ;
- les secrets ;
- les blocs machine `admin-trading`, `db-layer`, `student`, `fantome`.

## Workflow retenu

1. Reprendre depuis le parent `GO_OPT_TRADING_CURSOR_AI_OPERATIONS_PARENT_PLAN_01`.
2. Pour chaque action concrète, ouvrir un child dédié si la modification dépasse le simple routage documentaire.
3. Garder le parent comme surface de continuité active `cursor-ai`.
4. Reporter tout changement de statut dans `docs/index/MACHINE_WORK_SPLIT_ANTI_CONFLICT_01.md` et `docs/index/GO_INDEX.md`.

## État validé

- `Bundles` n'est plus seulement `APPLICATION_DOCUMENTED_NOT_PRODUCT_CLOSED` : il est retenu comme `ACTIVE_CONTINUITY` dans ce parent.
- `Claude / Live artifacts` n'est plus seulement `MERGED` : il est retenu comme `ACTIVE_CONTINUITY` dans ce parent.
- `alert_webhook` reste `ACTIVE_CONTINUITY`.

## Prochain GO possible

`GO_OPT_TRADING_CURSOR_AI_OPERATIONS_CHILD_BUNDLES_WORKFLOW_VALIDATION_01`

But : verrouiller le workflow opératoire `Bundles` si une action concrète devient nécessaire.
