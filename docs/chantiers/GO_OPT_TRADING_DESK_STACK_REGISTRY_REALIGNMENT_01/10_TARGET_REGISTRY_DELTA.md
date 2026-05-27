---
doc_id: GO_OPT_TRADING_DESK_STACK_REGISTRY_REALIGNMENT_01_TARGET_REGISTRY_DELTA
doc_type: registry_delta
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_DESK_STACK_REGISTRY_REALIGNMENT_01
status: draft_for_review
lifecycle_stage: implementation
topic_keys:
  - opt-trading
  - modules
  - desk
  - registry
surface: registry
source_kind: canonical_draft
updated_at: 2026-05-25
links:
  - docs/chantiers/GO_OPT_TRADING_DESK_STACK_REGISTRY_REALIGNMENT_01/00_INITIAL_PROJECT_DOC.md
---

# 10_TARGET_REGISTRY_DELTA

## Ajouts

| Module | Role registry retenu |
| --- | --- |
| `desk_pro` | coeur partage et owner canonique de stack |
| `desk_pro_orchestrator` | backbone d'execution |
| `desk_common` | support shared minimal |

## Requalifications

| Module | Avant | Apres |
| --- | --- | --- |
| `desk_pro_runner` | orchestreur principal implicite | facade operateur canonique |
| `desk_pro_dashboard` | dashboard generique | surface dashboard/export du stack |
| `desk_capture_inputs` | saisie manuelle | extraction d'inputs depuis snapshots |
| `desk_analyze` | analyse a la demande generique | satellite d'analyse locale |
| `desk_state` | etat rapide du desk | satellite de state canonique |
| `desk_snapshot_ingest` | ingestion d'historique | satellite d'ingestion snapshots |
| `desk_retention` | nettoyage historique | satellite retention/hygiene |

## Recalage wrappers_expected

Les modules concernes exposent reellement des scripts `cmd/menu/sanity` a l'echelle module.
Le registry a ete aligne sur cet etat pour les surfaces Desk ciblees.
