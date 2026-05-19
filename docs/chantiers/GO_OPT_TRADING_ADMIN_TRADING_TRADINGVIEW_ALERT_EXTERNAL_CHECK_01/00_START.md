---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_TRADINGVIEW_ALERT_EXTERNAL_CHECK_01_START
doc_type: chantier_start
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_TRADINGVIEW_ALERT_EXTERNAL_CHECK_01
parent: GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01
status: open
lifecycle_stage: execution
topic_keys:
  - opt-trading
  - admin_trading
  - tradingview
  - webhook
  - alert_check
surface: chantier
source_kind: canonical
updated_at: 2026-05-04
branche: go/GO_OPT_TRADING_ADMIN_TRADING_TRADINGVIEW_ALERT_EXTERNAL_CHECK_01
---

# 00_START — GO_OPT_TRADING_ADMIN_TRADING_TRADINGVIEW_ALERT_EXTERNAL_CHECK_01

## GO

`GO_OPT_TRADING_ADMIN_TRADING_TRADINGVIEW_ALERT_EXTERNAL_CHECK_01`

## Parent canonique

`GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01`

## Branche

`go/GO_OPT_TRADING_ADMIN_TRADING_TRADINGVIEW_ALERT_EXTERNAL_CHECK_01`

depuis `origin/sot/mainline` (HEAD f7ea0b4)

## Contexte établi — diagnostic signal PASS

Les deux GO précédents ont établi les faits suivants :

| GO | Résultat |
| --- | --- |
| `GO_OPT_TRADING_ADMIN_TRADING_WEBHOOK_RUNTIME_REVIEW_01` | PASS |
| `GO_OPT_TRADING_ADMIN_TRADING_WEBHOOK_SIGNAL_DIAG_01` | PASS |

Commit du diagnostic signal : **78f4635**

Faits prouvés côté serveur :
- `tv-webhook` : UP sur `admin-trading`
- `ngrok-tv` : UP
- Route `/tv` : POST-only, correcte
- URL publique ngrok : `phytogeographical-subnodulous-joycelyn.ngrok-free.dev/tv`
- Dernier POST `/tv` 200 OK : **2026-04-01 07:12**
- Métriques ngrok : **0 connections / 0 HTTP requests**

Conclusion du diagnostic : `admin-trading` est prêt à recevoir, mais **TradingView ne l'appelle plus**.

Cause confirmée par diagnostic : alertes TradingView stoppées, inactives, expirées, supprimées,
mal configurées ou stratégie/source arrêtée.

## Objectif

Vérifier manuellement dans TradingView l'état réel des alertes qui doivent appeler le webhook `/tv` :

- vérifier si les alertes existent encore
- vérifier si elles sont actives, expirées ou pausées
- vérifier si le webhook URL est correct
- vérifier si le message JSON attendu est encore configuré
- vérifier si la stratégie/indicateur source est encore attaché au chart
- vérifier symbole/timeframe
- documenter les résultats sans modifier admin-trading

## Type

Manuel / doc-only / external check

## Règles strictes

- **Doc-only** côté repo : aucun changement runtime admin-trading
- **Aucun POST manuel** vers `/tv`
- **Aucun test alert** si le message peut déclencher un vrai trade
- **Aucun ordre réel**, aucune modification de trades ouverts
- **Pas d'exposition** de secrets, tokens, credentials, webhook secret, API keys
- Pas de captures sensibles du compte TradingView
- Ne pas modifier tv-webhook, ngrok, tv-perf, bot_vision_headless, Desk Pro, OpenClaw
- Ne pas créer de nouveau parent
