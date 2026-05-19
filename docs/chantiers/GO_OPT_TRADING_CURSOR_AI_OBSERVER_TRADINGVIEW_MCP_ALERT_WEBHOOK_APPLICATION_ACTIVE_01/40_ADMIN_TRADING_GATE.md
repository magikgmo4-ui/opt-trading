# 40_ADMIN_TRADING_GATE

## Admin-trading — gate fermée

### Conditions avant toute ouverture future

| Condition | Requis |
|---|---|
| Demande explicite "chantiers pour admin-trading" | OBLIGATOIRE |
| Validation que le bloc ADMIN_TRADING dans MACHINE_WORK_SPLIT est le bon contexte | OBLIGATOIRE |
| alert_webhook application validée côté cursor-ai | RECOMMANDE |
| Template JSON testé et validé sans admin-trading | RECOMMANDE |

### Interdictions actuelles

- Ne pas router le template vers `webhook_server.py`
- Ne pas modifier le webhook admin-trading existant
- Ne pas ajouter d'URL webhook de production
- Ne pas activer `admin_trading_runtime: true`
- Ne pas modifier `trade_allowed: false`

### Éléments interdits tant qu'admin-trading n'est pas demandé

- webhook_server.py
- systemd services
- risk engine
- tout module sous `modules/admin-trading/`
- toute intégration runtime entre cursor-ai et admin-trading
