---
doc_id: GO_OPT_TRADING_CURSOR_AI_PARENT_OPERATIONAL_PLAN_01_60_ALERT_WEBHOOK_PLAN
doc_type: chantier/alert_webhook_plan
repo: opt-trading
machine: cursor-ai
status: active
links:
  - docs/index/MACHINE_WORK_SPLIT_ANTI_CONFLICT_01.md
---

# 60_ALERT_WEBHOOK_ACTIVE_PLAN

## Statut alert_webhook

- **Statut** : `ACTIVE_CONTINUITY`
- **PR mergee** : PR #203
- **Template integre** : `GO_OPT_TRADING_CURSOR_AI_OBSERVER_TRADINGVIEW_MCP_ALERT_WEBHOOK_TEMPLATE_01` (MERGE)
- **Application** : non fermee, active sur cursor-ai

## Role

L'alert_webhook est le mecanisme de continuité active entre TradingView (alertes externes) et le repo opt-trading.

Il reste :
- actif comme application documentee ;
- en continuite sans fermeture produit ;
- sous controle exclusif cursor-ai (gate admin-trading fermee).

## Ce qui est protege

- Le serveur webhook n'est pas touche.
- Les templates et configurations restent integres.
- Aucune alerte reelle n'est declenchee depuis cursor-ai sans demande explicite.
- La gate admin-trading empeche les actions runtime.

## Conditions avant ouverture admin-trading

Voir `70_ADMIN_TRADING_GATE.md` pour les conditions explicites.

## Prochains GO lies

| GO | Statut |
| --- | --- |
| `GO_OPT_TRADING_CURSOR_AI_ALERT_WEBHOOK_PRE_ADMIN_GATE_SPEC_01` | FUTURE — spec de gate avant admin-trading |
| `GO_OPT_TRADING_CURSOR_AI_OPERATOR_REPRISE_PACKET_01` | FUTURE — fiche de reprise |

## Interdictions

- Ne pas marquer alert_webhook comme ferme.
- Ne pas toucher systemd / webhook serveur / risk engine.
- Ne pas ouvrir admin-trading sans la spec de gate.
