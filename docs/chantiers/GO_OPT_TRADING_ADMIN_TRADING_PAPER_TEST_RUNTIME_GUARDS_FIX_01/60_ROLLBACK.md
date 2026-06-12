---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_PAPER_TEST_RUNTIME_GUARDS_FIX_01_60_ROLLBACK
doc_type: chantier/rollback
repo: opt-trading
machine: cursor-ai
go_id: GO_OPT_TRADING_ADMIN_TRADING_PAPER_TEST_RUNTIME_GUARDS_FIX_01
status: active
scope: bounded-runtime-guard
checked_at: 2026-05-13
---

# 60_ROLLBACK

## Rollback Git

Cette modification est bornee a:

- `modules/webhook/paper_guards.py`;
- `webhook_server.py`;
- `tests/test_paper_test_runtime_guards.py`;
- docs du GO.

Rollback:

```bash
git revert <commit-runtime-guards-fix>
```

ou fermeture de la PR sans merge.

## Rollback runtime cible

Ce GO ne modifie pas directement `admin-trading:/opt/trading`, ne redemarre aucun service et n'envoie aucun payload. Aucun rollback runtime cible n'est requis pour les actions effectuees localement.

Si le patch est deploye plus tard et bloque trop strictement `PAPER_TEST`, rollback operationnel:

1. ne pas envoyer de payload;
2. revenir au commit precedent ou deployer le revert;
3. redemarrer uniquement le service webhook dans un GO separe et documente;
4. verifier:

```bash
curl -sS http://127.0.0.1:8000/api/paper/guards
journalctl --no-pager --since '10 minutes ago' -u tv-webhook.service
```

## Secrets

Aucun secret n'a ete ajoute. Les guards ne lisent que des flags non secrets:

```text
RUNNER_MODE
SIMULATION_MODE
TRADE_ALLOWED
LEDGER_PATH
active_engine
adapter_names
```

## RISKS

- À qualifier.
