# 20 — Plan d'implémentation

## Nouveaux livrables

### A — `modules/openclaw_tmux_operator/scripts/health_aggregate.py`

Module Python standalone + importable :
- Charge la liste des machines Linux depuis `config/machine_runtime_map.yml`
- Par machine : SSH → `tmux list-sessions` + lecture `latest.json` runtime_health
- Machine locale : direct (pas SSH)
- `--dry-run` : injections, pas de SSH réel → 100% testable en CI
- Sortie JSON : timestamp, orchestrator_host, par machine (tmux_sessions, runtime_health_status, reachable)

Fonctions principales :
```
collect_tmux_sessions(machine, hostname) → dict
collect_runtime_health(machine, hostname) → dict | None
aggregate_machine(machine, hostname, injected=None) → dict
run_aggregate(machines, hostname, injected_map=None) → dict
main() → int
```

### B — Enrichissement `modules/openclaw_tmux_operator/scripts/cmd.sh`

Nouvelles commandes :
- `health-aggregate [--dry-run]` — appelle health_aggregate.py
- `openclaw-health [host=db-layer]` — SSH + gateway_openclaw cmd.sh health
- `openclaw-probe [host=db-layer]` — SSH + gateway_openclaw cmd.sh probe
- `session-logs <session> [lines=50]` — dernières N lignes du log réel (pas juste hint)

### C — `modules/openclaw_tmux_operator/docs/README.md` mise à jour

Nouvelles commandes documentées + exemples.

### D — `tests/openclaw_tmux_operator/__init__.py` + `test_health_aggregate.py`

Tests `python3 -m unittest` (même style que tests/tmux/test_health_check.py) :
- TestRunAggregateEmpty
- TestRunAggregateAllReachable
- TestRunAggregateOneUnreachable
- TestAggregateMachineLocal
- TestAggregateMachineRemoteInjected
- TestAggregateMachineWithHealthInfo
- TestOutputStructure
- TestReachableUnreachableSets

## Contraintes

- Pas de subprocess réel dans les tests (injection)
- health_aggregate.py READ_ONLY
- Aucune modification CI/CD
- Aucune modification scripts/ai/workers/
