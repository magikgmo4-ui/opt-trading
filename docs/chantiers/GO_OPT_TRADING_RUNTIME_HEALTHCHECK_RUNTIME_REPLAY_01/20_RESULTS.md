---
doc_id: GO_OPT_TRADING_RUNTIME_HEALTHCHECK_RUNTIME_REPLAY_01_RESULTS
doc_type: evidence
repo: opt-trading
go_id: GO_OPT_TRADING_RUNTIME_HEALTHCHECK_RUNTIME_REPLAY_01
parent_go_id: GO_OPT_TRADING_RUNTIME_ORCHESTRATOR_TMUX_FLEET_MOBILE_DEPLOY_01
status: open
source_kind: canonical
updated_at: 2026-05-27
---

# 20 — Results: runtime replay (healthcheck PyYAML fix)

[7_CANONICAL_STATE]

```text
base = sot/mainline@de76e947
parent = GO_OPT_TRADING_RUNTIME_ORCHESTRATOR_TMUX_FLEET_MOBILE_DEPLOY_01
previous_child = GO_OPT_TRADING_RUNTIME_HEALTHCHECK_PYTHON_ENV_FIX_01 (MERGED)
```

[13_ESTABLISHED]

- SSH `db-layer` joignable (read-only).
- `modules/runtime_health/fleet_orchestrator.py --dry-run` et `modules/runtime_health/healthcheck.py --dry-run` executables en runtime, donc `python3` peut importer `yaml` sur `db-layer`.
- Le repo `/opt/trading` sur `db-layer` n'est pas aligne sur `sot/mainline@de76e947` : il est sur une branche GO et contient des modifications + untracked. Le wrapper `scripts/fleet_orchestrator.sh` present sur `db-layer` ne contient pas le guard PyYAML, donc le fix PR #864 n'est pas prouve comme deploye sur ce host.

[12_PROOFS]

```text
ssh db-layer 'hostname; whoami; pwd'
db-layer / ghost / /home/ghost

ssh db-layer 'cd /opt/trading && git status --short --branch'
branch = go/GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_TRADING_LAB_EXIT_OUTCOME_ENGINE_01
modified = modules/trading_lab_v1/app/trading_lab_v1.py, modules/trading_lab_v1/data/sample_xauusd_m1_real_like.csv
untracked = .claude/, artifacts/backtests/, secrets/, ...

ssh db-layer 'cd /opt/trading && git log -1 --oneline --decorate'
HEAD = 3a1f6b0d (sot/mainline)

ssh db-layer 'cd /opt/trading && sed -n "1,80p" scripts/fleet_orchestrator.sh'
wrapper = ancien (pas de test import yaml)

ssh db-layer 'cd /opt/trading && sed -n "1,80p" scripts/runtime_healthcheck.sh'
wrapper = avec test import yaml

ssh db-layer '... PyYAML probe ...'
venv_import_yaml = OK (yaml 6.0.3)
usr_import_yaml = OK (yaml 6.0.1)
python3_import_yaml = OK (yaml 6.0.1)

ssh db-layer 'cd /opt/trading && python3 modules/runtime_health/fleet_orchestrator.py --map config/machine_runtime_map.yml --dry-run --no-telegram'
fleet_status = WARN (stale=[cursor-ai,fantome])

ssh db-layer 'cd /opt/trading && python3 modules/runtime_health/healthcheck.py --dry-run --no-telegram'
overall_status = FAIL (SYSTEMD_SERVICES/TIMERS/ENV/PATHS en FAIL)
```

[15_REMAINING_GAP]

| Surface | Etat | Impact |
|---|---:|---|
| Fix `fleet_orchestrator.sh` deploye sur db-layer | NOT_PROVEN | wrapper `scripts/fleet_orchestrator.sh` vu sur host ne contient pas le guard PyYAML |
| Runtime healthcheck (STEP 5) | FAIL (dry-run) | plusieurs blocks FAIL sur `db-layer` (non analyses ici) |
| Fleet stale/unreachable | OUT_OF_SCOPE | `student`, `cursor-ai`, `fantome` |
| Telegram allowlist | OUT_OF_SCOPE | pas traite ici |
| Repo hygiene / secrets | OUT_OF_SCOPE | pas traite ici |

[17_CLOSE_GATE_STATUS]

```text
RUNTIME_REPLAY_STATUS = PARTIAL_READ_ONLY_PROVEN (dry-run executed)
RUNTIME_DEPLOY = NOT_PROVEN
PARENT_STATUS = CLOSEOUT_BLOCKED
```
