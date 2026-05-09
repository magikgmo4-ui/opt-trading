---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_WEBHOOK_RUNTIME_REVIEW_REPRISE_01_GAPS_NEXT_DECISION
doc_type: gaps_next_decision
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_WEBHOOK_RUNTIME_REVIEW_REPRISE_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-05
---

# 50_GAPS_AND_NEXT_DECISION - Webhook Runtime Gaps And Next Decision

## Gaps runtime

- l'ancien constat "webhook idle depuis 33 jours" n'est plus vrai au moment de cette reprise; l'etat historique stale doit etre considere obsolete
- des `400 Bad Request` recents sont visibles dans le statut `tv-webhook`, sans diagnostic detaille dans ce GO
- `ngrok-tv` montre des erreurs transitoires de reconnexion reseau avant retablissement de session

## Gaps endpoint

- aucun endpoint `/health` n'est documente ni trouve dans le code webhook
- le contrat public exact de `signal_event` n'est pas encore canonise; seul un brouillon existe ici
- les endpoints `perf/*` sont documentes comme surfaces adjacentes mais pas audites fonctionnellement ici

## Gaps safety

- aucune verification externe TradingView -> ngrok -> webhook n'est autorisee dans ce GO
- aucune verification HMAC reelle n'est executee ici
- aucun test de `POST /api/reset_lock` ni de `POST /perf/event` n'est autorise dans ce perimetre

## Decision

**PASS** vers `GO_OPT_TRADING_ADMIN_TRADING_WEBHOOK_SIGNAL_DIAG_01`

Justification :

- la surface webhook est clairement active et observable
- les ports et endpoints principaux sont cartographies
- la frontiere de test sure est documentee
- un brouillon de contrat `signal_event` existe desormais pour le diagnostic suivant

## Point de reprise

Si la suite est confirmee, ouvrir :

`GO_OPT_TRADING_ADMIN_TRADING_WEBHOOK_SIGNAL_DIAG_01`
