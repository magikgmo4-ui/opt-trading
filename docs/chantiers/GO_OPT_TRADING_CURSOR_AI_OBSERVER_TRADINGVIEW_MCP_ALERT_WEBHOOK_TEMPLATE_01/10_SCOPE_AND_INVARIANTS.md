# 10_SCOPE_AND_INVARIANTS

## Scope

Creer et documenter un template JSON d'alerte webhook TradingView non critique cote cursor-ai, sans remplacer le webhook existant et sans modifier admin-trading.

## In scope

- Template JSON `alert_webhook_template_v1.json` dans `modules/tradingview_observer/templates/`
- Documentation de la procedure de test safe
- Documentation des limites et regles de securite
- Mise a jour du parent cursor-ai

## Out of scope

- Remplacer le webhook TradingView -> admin-trading
- Modifier admin-trading
- Modifier webhook_server.py
- Modifier systemd
- Modifier risk engine
- Creer une alerte de production
- Supprimer une alerte existante
- Faire un trade

## Invariants

- Pas de secret dans le template
- Pas de vraie cle API
- Pas d'ordre
- `trade_allowed: false`
- `admin_trading_runtime: false`
- Pas d'URL webhook secrete complete (placeholder si necessaire)
- Aucun output live JSON tracke
- Aucun .env touche

## Machine owner

cursor-ai
