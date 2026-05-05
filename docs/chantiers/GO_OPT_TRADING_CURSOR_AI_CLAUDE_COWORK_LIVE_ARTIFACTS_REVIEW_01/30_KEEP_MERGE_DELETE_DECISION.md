# 30_KEEP_MERGE_DELETE_DECISION

## Table de decision

| Element | Source | Statut | Decision | Justification | Prochaine action |
|---|---|---|---|---|---|
| `LIVE_ARTIFACTS_CLAUDE_COWORK_IDE_BUNDLE_01` | branche remote | Non merge, 2 fichiers/205 lignes | **REVIEW_MERGE** | Doc-only, manifeste + handoff IDE utiles pour cursor-ai | Merger dans sot/mainline |
| `CLAUDE_COWORK_PARENT_LIVE_ARTIFACTS_01` | branche remote | Non merge, 3 fichiers/1179 lignes | **REVIEW_MERGE** | Doc-only, cadrage methodologique Claude cowork | Merger dans sot/mainline |
| Fichiers live/output | repo | Inexistant | **AUCUN** | Aucun fichier live/output identifie | Aucun |
| Scripts runtime | repo | Inexistant dans ces branches | **AUCUN** | Branches doc-only | Aucun |

## Resume

- 2 branches cursor-ai a merger (REVIEW_MERGE).
- Aucune suppression necessaire.
- Contenu 100% doc-only, aucun risque runtime.

## Prochain GO apres merge

`GO_OPT_TRADING_CURSOR_AI_CLAUDE_COWORK_LIVE_ARTIFACTS_MERGE_01` — Merger les deux branches dans sot/mainline.
