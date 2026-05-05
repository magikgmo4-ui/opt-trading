# 40_ALERT_WEBHOOK_TEMPLATE — GO child 3

## GO ID

`GO_OPT_TRADING_CURSOR_AI_OBSERVER_TRADINGVIEW_MCP_ALERT_WEBHOOK_TEMPLATE_01`

## Phase

Phase 10 — Alert webhook template non critique

## Objectif

Tester la creation d'un template d'alerte webhook non critique depuis TradingView via MCP, valider le format JSON genere, sans remplacer les alertes existantes ni brancher de flux de production.

## Contexte

- Phase 2 a documente que `alert_create` fonctionne via DOM workaround.
- Les webhooks/payloads ne sont pas visibles via l'API MCP.
- Un template webhook peut etre teste sans impacter les alertes existantes.

## Actions attendues

1. Creer un template d'alerte test (symbol fictif ou non critique).
2. Valider le format JSON du payload webhook.
3. Documenter les champs presents/absents.
4. Supprimer l'alerte test apres validation (si possible).
5. Ne pas connecter le webhook a une URL de production.
6. Ne pas remplacer les alertes existantes.
7. Commit + push (documentation seulement).

## Invariants

- Flag `-AllowMutation` requis (mode mutation explicite).
- Alerte test uniquement, suppression apres test.
- Aucun webhook de production connecte.
- Aucun admin-trading touche.
- Aucun trade.

## Statut

PASS_DOC_ONLY — Template cree, procedure documentee, securite verifiee. Aucun envoi reel.
