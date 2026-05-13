---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_PAPER_TEST_EXECUTION_01_40_EVIDENCE
doc_type: chantier/evidence
repo: opt-trading
machine: admin-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_PAPER_TEST_EXECUTION_01
status: closed
scope: doc-only
checked_at: 2026-05-13
verdict: FAIL_CONTROLLED_NO_RUN
---

# 40_EVIDENCE

## Evidence collectee

### Etat AVANT

```text
/opt/trading/state/events.jsonl exists size=1059793
/opt/trading/state/positions.json exists size=607
/opt/trading/state/ledger_live.json missing
/opt/trading/state/ledger_paper.json missing
/data/ledger_live.json missing
/data/ledger_paper.json missing
state/positions.json exists size=607
```

Derniers evenements avant:

```text
api/events?limit=3 -> 200
engine=TV_TEST
symbol=TEST/USDT
reason=GO_TELEGRAM_TEST_REPLAY_01 / GO_TELEGRAM_TEST_REPLAY_02
```

Perf open avant:

```text
perf/open -> 200
open engine=COINM_SHORT
symbol=BTCUSDT
status=OPEN
```

### Etat APRES

```text
/opt/trading/state/events.jsonl exists size=1059793
/opt/trading/state/positions.json exists size=607
/opt/trading/state/ledger_live.json missing
/opt/trading/state/ledger_paper.json missing
/data/ledger_live.json missing
/data/ledger_paper.json missing
state/positions.json exists size=607
```

Derniers evenements apres:

```text
api/events?limit=3 -> 200
engine=TV_TEST
symbol=TEST/USDT
reason=GO_TELEGRAM_TEST_REPLAY_01 / GO_TELEGRAM_TEST_REPLAY_02
```

Perf open apres:

```text
perf/open -> 200
open engine=COINM_SHORT
symbol=BTCUSDT
status=OPEN
```

## Absence d'effet live

| Controle | Etat |
| --- | --- |
| `ledger_live.json` cree | non |
| `ledger_paper.json` cree | non |
| nouvel evenement `PAPER_TEST` | non |
| nouvelle execution paper | non |
| ordre reel | non |
| appel broker observe dans journaux du GO | non |

## Limite

La preuve positive d'une simulation paper complete n'existe pas dans ce GO, car le payload a ete bloque avant execution. Le verdict ne valide donc pas le passage `PAPER_TEST`; il valide uniquement que le test n'a pas ete lance dans un contexte non conforme.
