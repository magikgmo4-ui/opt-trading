# 10_BRANCH_MATRIX — Audit cursor-ai TradingView

## Matrice de decision

| Branche | Local | Remote | Merged | Diff | Doc-only | Verdict | Next GO |
|---|---|---|---|---|---|---|---|---|
| `OBSERVER_TRADINGVIEW_MCP_01` | yes | yes | YES | 0 files | — | **DROP_MERGED** | Supprimer remote |
| `TRADINGVIEW_OBSERVER_OPERATIONS_PARENT_01` | yes | yes | NO | 5 files / 195+ | yes | **REVIEW_MERGE** | Merger si utile |
| `POST_MERGE_REPRISE_01` | yes | yes | NO | 5 files / 194+ | yes | **REVIEW_MERGE** | Merger si utile |
| `SHARED_PACKET_01` | yes | yes | NO | 5 files / 153+ + .gitignore | yes | **REVIEW_MERGE** | Merger si utile |
| `ALERT_WEBHOOK_TEMPLATE_01` | yes | yes | NO | 5 files / 195+ | yes | **KEEP_ACTIVE** | Chantier enfant actif |
| `PARENT_CLOSEOUT_01` | yes | yes | NO | 5 files / 195+ | yes | **KEEP_ACTIVE** | Chantier enfant actif |

## Notes

- **OBSERVER_TRADINGVIEW_MCP_01** : Parent merge via PR #200. Branche merged, diff vide. Supprimable.
- **OPERATIONS_PARENT_01** : Doc-only parent continuite operations. Commit `08774fd`.
- **POST_MERGE_REPRISE_01** : Doc-only post-merge reprise. Commit `73b0622`.
- **SHARED_PACKET_01** : Shared packet export (+ .gitignore). Commit `958bd5e`.
- **ALERT_WEBHOOK_TEMPLATE_01** : Meme commit `78915bb` que PARENT_CLOSEOUT_01, identical content.
- **PARENT_CLOSEOUT_01** : Meme commit `78915bb` que ALERT_WEBHOOK_TEMPLATE_01, identical content.

## Duplication identifiee

`ALERT_WEBHOOK_TEMPLATE_01` et `PARENT_CLOSEOUT_01` partagent le meme commit `78915bb`. Il s'agit du meme contenu sur deux branches. Une seule doit etre conservee. L'autre peut etre DROP_MERGED si absorbee ou DROP_DUPLICATE.

## RISKS

- À qualifier.
