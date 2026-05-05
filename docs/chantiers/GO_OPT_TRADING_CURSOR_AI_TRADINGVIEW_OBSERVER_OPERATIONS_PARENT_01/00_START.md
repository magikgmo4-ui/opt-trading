# 00_START — GO_OPT_TRADING_CURSOR_AI_TRADINGVIEW_OBSERVER_OPERATIONS_PARENT_01

## Role

Parent machine cursor-ai pour la continuation operationnelle du produit TradingView MCP Observer apres merge PR #200.

Ce parent organise tous les GO children cote cursor-ai sans rouvrir le parent ferme `GO_OPT_TRADING_CURSOR_AI_OBSERVER_TRADINGVIEW_MCP_01`.

## Reference fermee

| Champ | Valeur |
|-------|--------|
| Parent ferme | `GO_OPT_TRADING_CURSOR_AI_OBSERVER_TRADINGVIEW_MCP_01` |
| PR | #200 |
| Merge commit | `718490d` |
| Base canonique | `sot/mainline` |

## Source de verite

`sot/mainline` — produit TradingView MCP Observer integre.

## Arborescence

```
GO_OPT_TRADING_CURSOR_AI_TRADINGVIEW_OBSERVER_OPERATIONS_PARENT_01/
  00_START.md                    (ce fichier)
  10_CHILDREN_INDEX.md           (index des children)
  20_POST_MERGE_REPRISE.md       (GO child 1)
  30_SHARED_PACKET_OPTION_B.md   (GO child 2)
  40_ALERT_WEBHOOK_TEMPLATE.md   (GO child 3)
  90_CLOSEOUT.md                 (closeout du parent)
```

## Machine

- **Machine** : cursor-ai (Windows)
- **Produit** : TradingView MCP Observer
- **Modules** : `modules/tradingview_observer/`, `modules/tradingview_observer_openclaw/`

## Invariants parent

- Ne pas rouvrir le parent ferme.
- Ne pas modifier admin-trading.
- Ne pas activer shared folder (Option B = preparation).
- Ne pas activer ingestion (Option C = GO separe).
- Ne pas creer/modifier/supprimer d'alerte TradingView.
- Ne pas committer secrets/outputs live.
