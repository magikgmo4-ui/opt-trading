---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_PAPER_TEST_EXECUTION_01_30_EXECUTION_LOG
doc_type: chantier/execution_log
repo: opt-trading
machine: cursor-ai + admin-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_PAPER_TEST_EXECUTION_01
status: closed
scope: doc-only
checked_at: 2026-05-13
verdict: FAIL_CONTROLLED_NO_RUN
---

# 30_EXECUTION_LOG

## Resume

Le paper test n'a pas ete execute. Le GO s'est arrete apres prechecks, avant tout POST `/tv`.

## Commandes effectuees

1. Synchronisation locale deja effectuee avant ce GO:

```text
sot/mainline -> origin/sot/mainline
HEAD: 589be4ce
```

2. Branche locale dediee:

```text
go/GO_OPT_TRADING_ADMIN_TRADING_PAPER_TEST_EXECUTION_01
```

3. Etat cible AVANT:

```text
branch=go/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_DESK_SNAPSHOT_INPUT_01
head=0bc9bdb
status_count=0
```

4. Prechecks services/endpoints:

```text
tv-webhook.service=active
tv-bitget-runner.service=activating
ngrok-tv.service=active
tv-perf.service=active
api/state -> 200
api/events?limit=3 -> 200
perf/open -> 200
desk/health -> 200
```

5. Prechecks guards:

```text
RUNNER_MODE=unset
SIMULATION_MODE=unset
TRADE_ALLOWED=unset
```

6. Verification code:

```text
webhook_server.py:469: if engine == "PAPER_TEST":
webhook_server.py:486: res = executor.execute(order, "paper")
```

7. Etat cible APRES:

```text
branch=go/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_DESK_SNAPSHOT_INPUT_01
head=0bc9bdb
status_count=0
```

## Commandes non effectuees

Le POST `/tv` avec `engine=PAPER_TEST` n'a pas ete effectue.

Raison: les guards paper requis etaient absents ou ambigus avant execution.

## Side effects

| Surface | Resultat |
| --- | --- |
| ordre reel | aucun |
| trade live | aucun |
| POST `/tv` | non effectue |
| Telegram paper notification | non envoyee par ce GO |
| `events.jsonl` | taille inchangee |
| `positions.json` | taille inchangee |
| `ledger_live.json` | absent avant/apres |
| `ledger_paper.json` | absent avant/apres |
| worktree cible | propre avant/apres |

## RISKS

- À qualifier.
