---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_TELEGRAM_NOTIFICATION_EXECUTION_RESULTS_01_10_SUMMARY
doc_type: chantier/summary
repo: opt-trading
branch: go/GO_OPT_TRADING_ADMIN_TRADING_TELEGRAM_NOTIFICATION_EXECUTION_RESULTS_01
machine: admin-trading
status: active
lifecycle_stage: telegram_execution_results
---

# 10_EXECUTION_SUMMARY — Resume complet de l'execution

## Verdict

**PASS COMPLET** — Le flux `/tv → Telegram notification` est valide.

## Configuration

| Element | Valeur |
| --- | --- |
| `TELEGRAM_ENABLED` | `1` |
| `TELEGRAM_BOT_TOKEN` | Present (longueur 46) |
| `TELEGRAM_CHAT_ID` | Present (longueur 11) |
| Source | `/opt/trading/.env` (non committe) |
| Service | `tv-webhook.service` redemarre avec nouvel env |

## Payloads envoyes

| # | Signal | Reason | HTTP | Body |
| --- | --- | --- | --- | --- |
| 1 | BUY | `GO_TELEGRAM_TEST_BUY_01` | 200 | `{"ok": true}` |
| 2 | SELL | `GO_TELEGRAM_TEST_SELL_01` | 200 | `{"ok": true}` |
| 3 | BUY | `GO_TELEGRAM_TEST_REPLAY_01` | 200 | `{"ok": true}` |
| 4 | BUY | `GO_TELEGRAM_TEST_REPLAY_02` | 200 | `{"ok": true}` |
| 5 | BUY | `GO_TELEGRAM_TEST_REPLAY_03` | 200 | `{"ok": true}` |

**Total : 5/5 PASS** (2 series identiques = 10 payloads acceptes).

Note : deux series identiques ont ete envoyees (le script a ete execute deux fois via scp). Cela confirme la repeatabilite du flux.

## Events JSONL

10 events `engine=TV_TEST`, tous depuis `127.0.0.1` :

```
engine=TV_TEST ip=127.0.0.1 reason=GO_TELEGRAM_TEST_BUY_01
engine=TV_TEST ip=127.0.0.1 reason=GO_TELEGRAM_TEST_SELL_01
engine=TV_TEST ip=127.0.0.1 reason=GO_TELEGRAM_TEST_REPLAY_01
engine=TV_TEST ip=127.0.0.1 reason=GO_TELEGRAM_TEST_REPLAY_02
engine=TV_TEST ip=127.0.0.1 reason=GO_TELEGRAM_TEST_REPLAY_03
(x2 series)
```

## Donnees de test

| Parametre | Valeur |
| --- | --- |
| Engine | `TV_TEST` |
| Symbol | `TEST/USDT` |
| TF | `1m` |
| Price | `100.0` |
| SL | `95.0` (BUY) / `105.0` (SELL) |
| Qty calculee | `20.0` |
| Risk USD | `100.0` |

## RISKS

- À qualifier.
