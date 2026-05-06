---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_TELEGRAM_NOTIFICATION_EXECUTE_TEST_01_00_START
doc_type: chantier/start
repo: opt-trading
branch: go/GO_OPT_TRADING_ADMIN_TRADING_TELEGRAM_NOTIFICATION_EXECUTE_TEST_01
machine: admin-trading
status: active
lifecycle_stage: telegram_execute_test
links:
  - docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_TELEGRAM_NOTIFICATION_ENABLE_TEST_01/10_TELEGRAM_ENABLE_PROCEDURE.md
  - docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_TELEGRAM_NOTIFICATION_ENABLE_TEST_01/20_SAFE_PAYLOAD_TEST.md
  - docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_TV_TEST_RUNTIME_CONFIG_CANONICALIZE_01/30_SAFE_CONFIG_PATTERN.md
---

# 00_START — GO_OPT_TRADING_ADMIN_TRADING_TELEGRAM_NOTIFICATION_EXECUTE_TEST_01

## Objet

Executer le test Telegram reel controle sur admin-trading, avec credentials
appliques localement, en suivant la procedure deja mergee (PR #218).

## Pre-requis

- [ ] Procedure PR #218 lue (`10_TELEGRAM_ENABLE_PROCEDURE.md`)
- [ ] `TELEGRAM_BOT_TOKEN` et `TELEGRAM_CHAT_ID` disponibles (hors repo)
- [ ] Pattern `TV_TEST` canonise (PR #219, `30_SAFE_CONFIG_PATTERN.md`)
- [ ] `trade_allowed=false`, `admin_trading_runtime=false` confirmes
- [ ] Machine admin-trading accessible

## Structure

| Fichier | Contenu |
| --- | --- |
| `00_START.md` | Ce fichier |
| `10_EXECUTION_RUNBOOK.md` | Runbook d'execution pas-a-pas |
| `90_CLOSEOUT.md` | Verdict et closeout |

## Contraintes

- Credentials uniquement dans `/opt/trading/.env` sur admin-trading
- Ne pas coller les credentials dans ChatGPT ni dans le repo
- Preuves locales hors repo
- `trade_allowed=false`, `admin_trading_runtime=false`
- Engine `TV_TEST` exclusivement
- Aucun trade reel
