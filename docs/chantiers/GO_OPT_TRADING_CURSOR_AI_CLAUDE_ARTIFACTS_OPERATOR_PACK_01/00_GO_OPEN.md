---
doc_id: GO_OPT_TRADING_CURSOR_AI_CLAUDE_ARTIFACTS_OPERATOR_PACK_01_00_GO_OPEN
doc_type: chantier/go_open
repo: opt-trading
branch: go/GO_OPT_TRADING_CURSOR_AI_CLAUDE_ARTIFACTS_OPERATOR_PACK_01
machine: cursor-ai
status: active
lifecycle_stage: operator_pack_refresh
links:
  - docs/index/MACHINE_WORK_SPLIT_ANTI_CONFLICT_01.md
  - docs/chantiers/GO_OPT_TRADING_CURSOR_AI_PARENT_OPERATIONAL_PLAN_01/20_ACTIVE_GO_LIST.md
  - docs/index/inbox/GO_OPT_TRADING_CURSOR_AI_CLAUDE_ARTIFACTS_OPERATOR_PACK_01.md
  - bundles/claude-artifacts/README.md
---

# 00_GO_OPEN — GO_OPT_TRADING_CURSOR_AI_CLAUDE_ARTIFACTS_OPERATOR_PACK_01

## Objet

Regulariser un dossier canonique doc-only pour le pack operateur Claude artifacts propre a `cursor-ai`, base sur les artefacts deja merges dans `sot/mainline`.

## Point de depart

- Source canonique de routage machine : bloc `CURSOR_AI` de `docs/index/MACHINE_WORK_SPLIT_ANTI_CONFLICT_01.md`.
- Source canonique de priorite locale : `docs/chantiers/GO_OPT_TRADING_CURSOR_AI_PARENT_OPERATIONAL_PLAN_01/20_ACTIVE_GO_LIST.md`.
- Base Git de ce passage : `sot/mainline`, branche de travail `go/GO_OPT_TRADING_CURSOR_AI_CLAUDE_ARTIFACTS_OPERATOR_PACK_01`.
- Constat au `2026-05-08` : le pack initial et plusieurs prolongements documentaires existent deja sur `sot/mainline`; ce passage ne les re-arbitre pas, il regularise le dossier du GO demande.

## Contraintes

- Ne pas ouvrir `admin-trading` sans demande explicite.
- Ne pas modifier le runtime.
- Ne pas rouvrir TradingView MCP ferme / merge.
- Ne pas toucher `GO_OPT_TRADING_DOC_OPS_CHILD_OPEN_WORK_CONTROL_01`.
- Ne pas utiliser Google Drive.
- Limiter le diff a `docs/` et `bundles/`.

## Livrables canoniques

| Fichier | Role |
| --- | --- |
| `00_GO_OPEN.md` | Ouverture canonique |
| `10_SOURCE_STATE.md` | Etat source et ecarts documentes |
| `20_OPERATOR_PACK_SPEC.md` | Spec du pack operateur |
| `30_ARTIFACTS_INDEX.md` | Index des artefacts et dependances |
| `40_USAGE_WORKFLOW.md` | Workflow d'usage |
| `90_CLOSEOUT.md` | Verdict final |

## Compatibilite documentaire

La structure legacy `00_START.md` ... `50_NO_COMMIT_RULES.md` est conservee pour ne pas casser les references deja mergees dans le repo.
