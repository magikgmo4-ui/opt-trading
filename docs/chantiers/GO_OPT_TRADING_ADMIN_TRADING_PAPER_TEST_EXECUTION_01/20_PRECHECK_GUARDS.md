---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_PAPER_TEST_EXECUTION_01_20_PRECHECK_GUARDS
doc_type: chantier/precheck_guards
repo: opt-trading
machine: admin-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_PAPER_TEST_EXECUTION_01
status: closed
scope: doc-only
checked_at: 2026-05-13
verdict: FAIL
---

# 20_PRECHECK_GUARDS

## Gate attendue

La gate `PAPER_TEST` exige:

| Guard | Attendu |
| --- | --- |
| mode runner | `RUNNER_MODE=PAPER` |
| simulation | `SIMULATION_MODE=true` |
| trade allowed | `TRADE_ALLOWED=false` |
| ledger | ledger paper dedie, pas `ledger_live.json` |
| ordre reel | impossible |
| broker live | aucun appel API broker reel |

## Etat detecte

Flags runtime sur `admin-trading:/opt/trading`:

```text
RUNNER_MODE=unset
SIMULATION_MODE=unset
TRADE_ALLOWED=unset
TELEGRAM_ENABLED=1
PERF_URL=unset
TV_WEBHOOK_KEY=unset
TELEGRAM_BOT_TOKEN=set
TELEGRAM_CHAT_ID=set
```

Les secrets Telegram etaient seulement detectes comme presents. Ils n'ont pas ete affiches ni copies.

## Runtime guard

```text
VERDICT: FAIL -- main cause: tv-bitget-runner.service not active
FAIL: tv-bitget-runner.service -> activating
PASS: tv-webhook.service active
PASS: ngrok-tv.service active
PASS: tv-perf.service active
PASS: dash -> 200
PASS: perf/open -> 200
PASS: desk/health -> 200
PASS: no recent critical runtime journal pattern detected
VERDICT: FAIL (warn=0 fail=1)
```

## Code guard check

Recherche sur la cible:

```text
webhook_server.py:469:    if engine == "PAPER_TEST":
webhook_server.py:486:        res = executor.execute(order, "paper")
```

Les motifs suivants ne sont pas presents dans les surfaces runtime inspectees, hors documentation de gate:

```text
RUNNER_MODE
SIMULATION_MODE
TRADE_ALLOWED
ledger_paper
ledger_live
isReal
UNAUTHORIZED_MODE
CRITICAL_SECURITY
```

## Conclusion

Le chemin `PAPER_TEST` force bien l'adaptateur `paper`, mais les guards obligatoires de la gate ne sont pas actifs comme checks runtime detectables. Critere FAIL atteint: `Guard absent ou ambigu`.

Decision: aucun payload `PAPER_TEST` envoye.
