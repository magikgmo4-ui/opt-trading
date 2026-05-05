# 10_ACTIVE_SCOPE

## trading_view_mcp_alert_webhook — continuité active

### Ce qui est fait

- Template JSON `alert_webhook_template_v1.json` intégré dans `sot/mainline`
- Documentation template (spec, test procedure, limits, security) intégrée
- Tous les flags de sécurité actifs (`trade_allowed: false`, `admin_trading_runtime: false`)
- Aucun secret, aucun endpoint webhook réel dans le template

### Ce qui reste actif

- Application réelle du template (test avec endpoint, validation)
- Intégration conditionnelle éventuelle (seulement si besoin prouvé)
- L'application n'est pas fermée — elle est en continuité active

### Ce qui n'est pas ouvert

- Admin-trading
- Webhook production
- Alerte réelle

### Statut du parent

- Parent cursor-ai TradingView MCP : FERME (transport/docs)
- Ce GO garde la continuité alert_webhook sans rouvrir le parent

### Machine

cursor-ai
