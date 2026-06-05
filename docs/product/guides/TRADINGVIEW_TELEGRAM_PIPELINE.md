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
---

# Guide - TradingView / Telegram Alert Pipeline

## 1_MASTER_TARGET

Pipeline complet d'alertes TradingView -> webhook -> observation -> Telegram -> Desk Pro, boucle fermee.

## FINAL_TARGET

Pipeline operationnel ferme avec alertes, webhook, Telegram et journalisation, pret pour la production.

## CURRENT_STATE

`USABLE_LIMITED` -- Parent observer merge (PR #200). Alert webhook en continuite active (PR #203). Dry-run bridge packet fonctionnel. Alert webhook non ferme, integration Telegram partielle.

## USAGE_ALLOWED_NOW

- Recevoir et router des alertes TradingView via webhook.
- Observer les signaux via `tradingview_observer`.
- Tester le bridge packet en dry-run.
- Notifier l'operateur (si Telegram actif).

## USAGE_FORBIDDEN_NOW

- Moteur de trading automatique.
- Execution d'ordres sans validation humaine.
- Source canonique de decision.

## IMPLEMENTATION_PATH

1. Fermer l'alert webhook (closeout).
2. Consolider l'export reel.
3. Completer l'integration Telegram.
4. Closeout de la continuite.

## CONTINUITY_STATE

Actif -- alert webhook en continuite, closeout en attente.

## MACHINE / SURFACE

`cursor-ai` (observer, alertes).

## REPRISE_POINT

```text
docs/index/MACHINE_WORK_SPLIT_ANTI_CONFLICT_01.md
docs/chantiers/GO_OPT_TRADING_CURSOR_AI_OBSERVER_TRADINGVIEW_MCP_01/90_CLOSEOUT.md
```

## TODO

1. Closeout alert webhook.
2. Export reel.
3. Integration Telegram.

## REMAINING_GAP

Alert webhook non ferme, export reel et integration Telegram a consolider.

## NEXT_GO

Poursuite du GO alert webhook actif, puis closeout de la continuite.

## PROMOTION_CONDITIONS

`USABLE_LIMITED` -> `USABLE_NOW` quand :
- alert webhook ferme,
- export reel operationnel,
- integration Telegram complete.

## Ce que c'est

Pipeline de reception d'alertes TradingView -> webhook -> observation -> Telegram.

## A quoi ca sert

Connecter les alertes TradingView au repo, les observer, les journaliser, les notifier.

## Quand l'utiliser

- Recevoir et router des alertes TradingView.
- Observer les signaux entrants avant action.
- Tester le bridge packet en dry-run.

## Quand ne pas l'utiliser

- Comme moteur de trading automatique.
- Pour executer des ordres sans validation humaine.

## Prerequis

- Parent observer merge (PR #200).
- Alert webhook en continuite active (PR #203).
- Module canonique : `modules/webhook/` (pas `webhook_server.py` racine).

## Commandes / acces

- Observer : `modules/tradingview_observer/`
- Observer OpenClaw : `modules/tradingview_observer_openclaw/`
- Webhook : `modules/webhook/`

## Procedure simple

1. Verifier l'alert webhook actif.
2. Recevoir une alerte TradingView via le webhook.
3. Observer le signal via `tradingview_observer`.
4. Consulter le bridge packet dry-run.
5. Notifier via Telegram si integre.

## Verification PASS

- Alertes TradingView arrivent dans le repo.
- Observer produit des rapports lisibles.
- Bridge packet dry-run fonctionnel.
- Aucun ordre automatique declenche.

## Limites

- Alert webhook non ferme.
- Integration Telegram reelle incomplete.
- Export reel a consolider.
- `webhook_server.py` (racine) est historique, le module canonique est `modules/webhook/`.

## Depannage

- Alertes n'arrivent pas : verifier webhook et logs.
- Observer ne produit rien : relire `MACHINE_WORK_SPLIT`.
- Bridge packet echoue : utiliser dry-run seulement.

## Source canonique

- `docs/index/MACHINE_WORK_SPLIT_ANTI_CONFLICT_01.md`
- `docs/chantiers/GO_OPT_TRADING_CURSOR_AI_OBSERVER_TRADINGVIEW_MCP_01/90_CLOSEOUT.md`

## RISKS

- À qualifier.
