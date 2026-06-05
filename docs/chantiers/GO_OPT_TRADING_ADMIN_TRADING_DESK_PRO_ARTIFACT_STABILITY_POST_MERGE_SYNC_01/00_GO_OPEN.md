---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_ARTIFACT_STABILITY_POST_MERGE_SYNC_01_00_GO_OPEN
doc_type: chantier/go_open
repo: opt-trading
machine: cursor-ai
go_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_ARTIFACT_STABILITY_POST_MERGE_SYNC_01
status: active
scope: doc-only
opened_at: 2026-05-12
base: sot/mainline
branch: go/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_ARTIFACT_STABILITY_POST_MERGE_SYNC_01
links:
  - docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_ARTIFACT_STABILITY_POST_MERGE_SYNC_01/10_SOURCE_STATE.md
  - docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_ARTIFACT_STABILITY_POST_MERGE_SYNC_01/20_SYNC_EXECUTION.md
  - docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_ARTIFACT_STABILITY_POST_MERGE_SYNC_01/30_TEST_VALIDATION.md
  - docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_ARTIFACT_STABILITY_POST_MERGE_SYNC_01/40_NEXT_DECISION.md
  - docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_ARTIFACT_STABILITY_POST_MERGE_SYNC_01/90_CLOSEOUT.md
  - docs/index/inbox/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_ARTIFACT_STABILITY_POST_MERGE_SYNC_01.md
---

# 00_GO_OPEN

## Objectif

Synchroniser `admin-trading:/opt/trading` sur `sot/mainline` apres merge de la PR fonctionnelle desk-pro artifact stability, puis valider les tests/gates desk-pro post-merge.

## Contexte

| Element | Etat |
| --- | --- |
| PR `#316` | merged, `ea85e227` |
| PR `#318` | merged, `edfff717` |
| branche fonctionnelle integree | `go/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_ARTIFACT_STABILITY_WINDOW_01` |
| suite `tmux-ide` | toujours gatee avant validation post-merge |

## Regles

- Pas de reset.
- Pas de force push.
- Pas de modification runtime applicative hors sync Git demande.
- Pas d'installation `tmux-ide`.
- Pas de creation `ide.yml`.
- Documentation locale uniquement dans cette PR.

## RISKS

- À qualifier.
