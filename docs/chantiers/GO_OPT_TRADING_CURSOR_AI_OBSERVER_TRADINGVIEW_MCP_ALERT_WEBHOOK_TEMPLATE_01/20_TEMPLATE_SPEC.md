# 20_TEMPLATE_SPEC

## Fichier

`modules/tradingview_observer/templates/alert_webhook_template_v1.json`

## Spec

- **Schema**: `opt_trading_tradingview_alert_template_v1`
- **Source**: tradingview
- **Mode**: test_only
- **Machine owner**: cursor-ai
- **Signal**: TEST_ONLY
- **Side**: NONE
- **Trade allowed**: false
- **Admin trading runtime**: false

## Champs

| Champ | Valeur | Note |
|---|---|---|
| `schema` | `opt_trading_tradingview_alert_template_v1` | Identifiant de schema |
| `source` | `tradingview` | Source de l'alerte |
| `mode` | `test_only` | Mode non production |
| `machine_owner` | `cursor-ai` | Machine proprietaire |
| `symbol` | `{{ticker}}` | Placeholder TradingView |
| `exchange` | `{{exchange}}` | Placeholder TradingView |
| `interval` | `{{interval}}` | Placeholder TradingView |
| `price` | `{{close}}` | Placeholder TradingView |
| `time` | `{{time}}` | Placeholder TradingView |
| `alert_name` | `{{alert_name}}` | Placeholder TradingView |
| `strategy` | `manual_test_template` | Strategie de test |
| `signal` | `TEST_ONLY` | Signal non operationnel |
| `side` | `NONE` | Pas de direction |
| `risk.trade_allowed` | `false` | Aucun trade |
| `risk.live_order` | `false` | Aucun ordre |
| `risk.max_risk_pct` | `0` | Risque zero |
| `routing.target` | `manual_review` | Cible review manuelle |
| `routing.admin_trading_runtime` | `false` | Non route vers admin-trading |
| `routing.desk_ingestion` | `false` | Non route vers desk |
| `routing.telegram_notify` | `false` | Non route vers Telegram |
| `notes` | `Non-critical TradingView webhook template for cursor-ai observer testing only.` | Description |

## Placeholders TradingView

Les champs `{{ticker}}`, `{{exchange}}`, `{{interval}}`, `{{close}}`, `{{time}}`, `{{alert_name}}` sont des placeholders standard TradingView. Ils seront remplaces automatiquement par TradingView au moment de l'envoi.
