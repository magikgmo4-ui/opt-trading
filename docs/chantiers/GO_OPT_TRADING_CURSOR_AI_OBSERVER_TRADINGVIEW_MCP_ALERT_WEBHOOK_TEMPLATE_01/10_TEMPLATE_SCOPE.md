# 10_TEMPLATE_SCOPE — Scope du template

## Contexte

Phase 2 a documente que `alert_create` fonctionne via DOM workaround (tradingview-mcp). Les webhooks/payloads ne sont pas visibles via l'API MCP (limitation TradingView). Un template webhook peut etre teste sans impacter les alertes existantes.

## Ce que ce GO produit

- Template JSON `alert_webhook_template_v1.json` dans `modules/tradingview_observer/templates/`
- Exemple de payload webhook documente
- Note de test safe (pas d'envoi vers admin-trading)

## Ce qui n'est PAS active

- Aucune alerte creee automatiquement
- Aucun webhook connecte a une URL de production
- Aucune modification des alertes existantes
- Aucun admin-trading touche
- Aucun trade

## Mode mutation

Toute creation d'alerte necessite le flag `-AllowMutation` sur `cmd.ps1`. Sans ce flag, le wrapper refuse toute operation d'ecriture.

## Template

Le template definit :
- La structure JSON d'une alerte webhook TradingView
- Les champs obligatoires (symbol, condition, actions, webhook URL)
- Un exemple de payload recu par le webhook
- La procedure de test safe
