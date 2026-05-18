---
go_id: GO_OPT_TRADING_UI_DUAL_SURFACE_EXTERNAL_LIVE_SOURCE_INGESTION_01
doc_type: closeout
repo: opt-trading
status: DELIVERED
commit: 3233706c
---

# GO_OPT_TRADING_UI_DUAL_SURFACE_EXTERNAL_LIVE_SOURCE_INGESTION_01 — CLOSEOUT

## Cycle livré

```text
TradingView alert → POST /tv (webhook_server:8000) → POST /perf/event → SQLite perf.db → Desk Pro UI (8010)
```

## Tests validés

| Scénario | Résultat |
|---|---|
| TV_TEST (test engine) | `200` — accepté, perf exclu |
| ECHO_TEST BUY | `200` — trade OPEN dans perf.db |
| ECHO_TEST SELL | `200` — trade CLOSED dans perf.db |
| Kill switch `TRADE_ALLOWED=false` | `422` — bloqué |
| Engine non enregistré | `422` — bloqué |
| Symbol non autorisé (avant config) | `422` — bloqué |
| unittest | 92/92 PASS |

## Perf finale

- 7 trades, 5 closed, 2 open, PnL $540
- Engines : `FIXTURE_SEED` + `ECHO_TEST`

## Config locale créée (gitignored)

| Fichier | Rôle |
|---|---|
| `.env` | `TRADE_ALLOWED=true`, `PERF_URL`, `TV_WEBHOOK_KEY` |
| `state/risk_config.json` | Accounts par engine, risk 1% de $10k |

## État canonique

| Surface | Statut |
|---|---|
| Desk Pro UI (8010) | fixture snapshot + mock fallback |
| Perf SQLite | trades réels + seedés |
| Webhook ingestion (8000) | validé, kill switch, risk limits |
| pipeline webhook → perf | validé bout en bout |

## Gaps restants

| Gap | Priorité |
|---|---|
| Aucune persistence systemd sur cette machine | basse |
| TV_WEBHOOK_KEY = dev_local_only (localhost) | basse |
| Aucune observabilité temps réel du pipeline | moyenne |
| seed_perf_fixture.py manuel | basse |

## Prochain GO recommandé

`GO_OPT_TRADING_DESKPRO_RUNTIME_OBSERVABILITY_01` — ajouter une observation exploitable du pipeline : derniers webhooks, events perf, état ingestion, statut source, erreurs.
