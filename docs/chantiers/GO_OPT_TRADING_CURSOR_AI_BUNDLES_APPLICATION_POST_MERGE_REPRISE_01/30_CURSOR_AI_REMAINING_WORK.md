# 30_CURSOR_AI_REMAINING_WORK

## Branches cursor-ai restantes

| Branche | Statut | Decision |
|---|---|---|
| `ALERT_WEBHOOK_TEMPLATE_01` | PASS_DOC_ONLY, branche a merger | Prochain GO : merge |
| `PARENT_CLOSEOUT_01` | PASS, branche a merger | Apres ALERT_WEBHOOK merge |

## Chantiers cursor-ai optionnels

| Chantier | Priorite | Note |
|---|---|---|
| `MACHINE_MAP_STALE_LINES_REVIEW_01` | P2 | Nettoyage map cursor-ai |
| `BUNDLES_APPLICATION_VALIDATION_01` | P2 | Dry-run validation bundle |
| Cleanup ALERT_WEBHOOK + PARENT_CLOSEOUT | P1 | Merge des dernieres branches TV MCP |

## Prochain GO

**`GO_OPT_TRADING_CURSOR_AI_OBSERVER_TRADINGVIEW_MCP_ALERT_WEBHOOK_TEMPLATE_MERGE_01`**

Merger ALERT_WEBHOOK dans sot/mainline. Ensuite PARENT_CLOSEOUT.

## Regle

- Ne pas lancer PARENT_CLOSEOUT avant merge d'ALERT_WEBHOOK.
- Admin-trading non ouvert.
- Bundles pas ferme produit.
