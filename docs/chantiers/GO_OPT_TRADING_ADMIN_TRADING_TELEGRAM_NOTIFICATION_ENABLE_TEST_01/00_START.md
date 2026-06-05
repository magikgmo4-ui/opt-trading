---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_TELEGRAM_NOTIFICATION_ENABLE_TEST_01_00_START
doc_type: chantier/start
repo: opt-trading
branch: go/GO_OPT_TRADING_ADMIN_TRADING_TELEGRAM_NOTIFICATION_ENABLE_TEST_01
machine: admin-trading
status: active
lifecycle_stage: telegram_enable_test
links:
  - docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_TELEGRAM_WEBHOOK_REAL_USAGE_TEST_01/95_EXECUTION_RESULTS.md
  - docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_TELEGRAM_WEBHOOK_REAL_USAGE_TEST_01/30_REAL_USAGE_TEST_PLAN.md
---

# 00_START — GO_OPT_TRADING_ADMIN_TRADING_TELEGRAM_NOTIFICATION_ENABLE_TEST_01

## Objet

Activer et tester la notification Telegram dans le flux webhook admin-trading,
sans trading reel, sans secret dans le repo.

## Contexte

- `TV_TEST` flux `/tv → record_event` valide (95_EXECUTION_RESULTS.md, 11/11 PASS)
- `trade_allowed=false`, `admin_trading_runtime=false` confirmes
- `TELEGRAM_ENABLED` absent de l'environnement du service `tv-webhook.service`
- La notification Telegram est code-ready dans `webhook_server.py:459-466` mais non activee

## Machine

- **Proprietaire** : admin-trading.
- **Rattachement** : bloc ADMIN_TRADING.

## Pre-requis

- [ ] `TELEGRAM_BOT_TOKEN` connu de l'operateur (secret, hors repo)
- [ ] `TELEGRAM_CHAT_ID` connu de l'operateur (secret, hors repo)
- [ ] Canal/chat Telegram accessible pour verification

## Structure

| Fichier | Contenu |
| --- | --- |
| `00_START.md` | Ce fichier |
| `10_TELEGRAM_ENABLE_PROCEDURE.md` | Procedure d'activation pas-a-pas |
| `20_SAFE_PAYLOAD_TEST.md` | Payload TV_TEST safe avec Telegram |
| `30_EXPECTED_RESULTS.md` | Resultats attendus |
| `40_ROLLBACK.md` | Procedure de desactivation |
| `90_CLOSEOUT.md` | Verdict et closeout |

## Contraintes

- `trade_allowed=false`
- `admin_trading_runtime=false`
- `engine=TV_TEST` exclusivement
- Aucun ordre reel
- Aucun secret dans le repo (ni dans cette doc)
- `TELEGRAM_BOT_TOKEN` et `TELEGRAM_CHAT_ID` definis uniquement sur admin-trading via `.env`
- Doc-only cote repo

## Invariants

- Ne pas activer `trade_allowed=true`
- Ne pas utiliser d'engine autre que `TV_TEST`
- Ne pas modifier `webhook_server.py`
- Ne pas committer `.env`
- Ne pas committer de secrets

## RISKS

- À qualifier.
