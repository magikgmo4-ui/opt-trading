---
doc_id: OPT_TRADING_GUIDE_TRADINGVIEW_TELEGRAM_PIPELINE
doc_type: user_guide
repo: opt-trading
status: reference
lifecycle_stage: product_usage
source_kind: canonical
updated_at: 2026-05-07
links:
  - docs/index/MACHINE_WORK_SPLIT_ANTI_CONFLICT_01.md
  - docs/chantiers/GO_OPT_TRADING_CURSOR_AI_OBSERVER_TRADINGVIEW_MCP_01/90_CLOSEOUT.md
  - docs/chantiers/GO_OPT_TRADING_CURSOR_AI_OBSERVER_TRADINGVIEW_MCP_ALERT_WEBHOOK_APPLICATION_ACTIVE_01/
---

# Guide utilisateur - TradingView / Telegram Alert Pipeline

## Ce que c'est

Le pipeline TradingView / Telegram recoit des alertes depuis TradingView, les route via webhook, les observe, et les notifie vers Telegram.

## A quoi ca sert

Il sert a connecter les alertes TradingView au repo opt-trading, les observer, les journaliser et les faire remonter vers l'operateur via Telegram.

## Quand l'utiliser

- pour recevoir et router des alertes TradingView dans le repo ;
- pour observer les signaux entrants avant toute action ;
- pour tester le bridge packet en dry-run.

## Quand ne pas l'utiliser

- comme moteur de trading automatique ;
- pour executer des ordres sans validation humaine ;
- comme source canonique de decision.

## Prerequis

- acces au repo et aux modules `tradingview_observer`, `webhook` ;
- le parent observer est merge (PR #200) ;
- l'alert webhook est en continuite active (PR #203) ;
- `webhook_server.py` (racine) est un runtime historique ; le module canonique est `modules/webhook/`.

## Commandes / acces

- Observer : `modules/tradingview_observer/`
- Observer OpenClaw : `modules/tradingview_observer_openclaw/`
- Webhook : `modules/webhook/`
- Bridge packet dry-run : `docs/chantiers/GO_OPT_TRADING_CURSOR_AI_OBSERVER_TRADINGVIEW_MCP_01/50_PHASE_5_ADMIN_TRADING_BRIDGE_OPTIONAL.md`

## Procedure simple

1. Verifier que l'alert webhook est actif et en continuite.
2. Recevoir une alerte TradingView via le webhook.
3. Observer le signal via `tradingview_observer`.
4. Consulter le bridge packet en dry-run avant toute action.
5. Notifier l'operateur via Telegram si l'integration est active.

## Verification PASS

- les alertes TradingView arrivent dans le repo ;
- l'observer produit des rapports lisibles ;
- le bridge packet dry-run fonctionne ;
- aucun ordre automatique n'est declenche.

## Limites

- l'alert webhook n'est pas ferme (closeout en attente) ;
- l'integration Telegram reelle n'est pas complete ;
- l'export reel reste a consolider ;
- `webhook_server.py` (racine) est un runtime historique, a ne pas confondre avec le module.

## Depannage

- Si les alertes n'arrivent pas : verifier le webhook et les logs.
- Si l'observer ne produit rien : relire `MACHINE_WORK_SPLIT_ANTI_CONFLICT_01.md`.
- Si le bridge packet echoue : utiliser uniquement le dry-run.

## Source canonique

- `docs/index/MACHINE_WORK_SPLIT_ANTI_CONFLICT_01.md`
- `docs/chantiers/GO_OPT_TRADING_CURSOR_AI_OBSERVER_TRADINGVIEW_MCP_01/90_CLOSEOUT.md`

## NEXT_GO

Poursuite du GO alert webhook actif, puis closeout de la continuite.
