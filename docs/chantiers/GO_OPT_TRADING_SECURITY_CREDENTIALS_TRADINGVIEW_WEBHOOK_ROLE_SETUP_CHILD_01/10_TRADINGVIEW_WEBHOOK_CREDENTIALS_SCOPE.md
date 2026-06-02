# TradingView Webhook Credentials Scope

Les credentials suivants sont nécessaires pour le rôle `webhook_receiver` :

| Credential ID | Env Var | Type | Description |
|---------------|---------|------|-------------|
| `tv_webhook_secret` | `TV_WEBHOOK_SECRET` | `webhook_secret` | Secret partagé entre TradingView et le serveur webhook pour authentifier les alertes. |

## Sécurité du Secret
Le secret doit être une chaîne complexe (UUID ou token généré) et ne doit jamais être partagé en dehors du serveur de réception et de l'interface TradingView.
