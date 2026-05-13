---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_PAPER_TEST_RUNTIME_GUARDS_FIX_01_50_VALIDATION_PLAN
doc_type: chantier/validation
repo: opt-trading
machine: cursor-ai
go_id: GO_OPT_TRADING_ADMIN_TRADING_PAPER_TEST_RUNTIME_GUARDS_FIX_01
status: active
scope: bounded-runtime-guard
checked_at: 2026-05-13
---

# 50_VALIDATION_PLAN

## Tests unitaires

Commande:

```powershell
python -m pytest tests/test_paper_test_runtime_guards.py -q
```

Resultat:

```text
6 passed in 0.04s
```

Cas couverts:

- guards PASS avec `RUNNER_MODE=PAPER`, `SIMULATION_MODE=true`, `TRADE_ALLOWED=false`, `LEDGER_PATH=/data/ledger_paper.json`, adaptateur `paper`;
- echec si flags absents;
- echec si `TRADE_ALLOWED=true`;
- echec si `active_engine=COINM_SHORT`;
- echec si `LEDGER_PATH` pointe vers `ledger_live.json`;
- echec si adaptateur `paper` absent.

## Tests adjacents

Commande:

```powershell
python -m pytest tests/test_paper_test_runtime_guards.py tests/test_admin_trading_contract_compatibility_smoke.py tests/test_desk_pro_dry_run.py tests/test_signal_event_adapter.py -q
```

Resultat:

```text
59 passed in 0.20s
```

## Compilation

Commande:

```powershell
python -m py_compile webhook_server.py modules/webhook/paper_guards.py tests/test_paper_test_runtime_guards.py
```

Resultat: PASS.

## Validation a faire avant prochaine execution paper

Sur `admin-trading`, avant tout POST `/tv` avec `engine=PAPER_TEST`:

```bash
curl -sS http://127.0.0.1:8000/api/paper/guards | python3 -m json.tool
```

Critere:

```text
ok=true
```

Si `ok=false`, aucun payload `PAPER_TEST` ne doit etre envoye.

## Non execute dans ce GO

- Aucun POST `/tv`.
- Aucun payload `PAPER_TEST`.
- Aucun ordre reel.
- Aucun live trading.
- Aucun test systemd cible.
