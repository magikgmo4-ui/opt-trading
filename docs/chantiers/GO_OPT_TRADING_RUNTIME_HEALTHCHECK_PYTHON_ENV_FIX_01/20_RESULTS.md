---
doc_id: GO_OPT_TRADING_RUNTIME_HEALTHCHECK_PYTHON_ENV_FIX_01_RESULTS
doc_type: evidence
repo: opt-trading
go_id: GO_OPT_TRADING_RUNTIME_HEALTHCHECK_PYTHON_ENV_FIX_01
parent_go_id: GO_OPT_TRADING_RUNTIME_ORCHESTRATOR_TMUX_FLEET_MOBILE_DEPLOY_01
status: open
source_kind: canonical
updated_at: 2026-05-26
---

# 20 — Results: healthcheck Python env fix (PyYAML)

[7_CANONICAL_STATE]

```text
base = sot/mainline@a90b2ed3
patch = scripts/fleet_orchestrator.sh
```

[13_ESTABLISHED]

- `scripts/runtime_healthcheck.sh` resolve deja un python capable de `import yaml` avant d'executer `modules/runtime_health/healthcheck.py`.
- `scripts/fleet_orchestrator.sh` etait plus permissif (prenait le premier python trouve) et pouvait selectionner un python sans PyYAML, entrainant une machine map vide (`_load_map` => `{}`) et un WARN STEP 5.

[9_SELECTED_SOLUTION]

Aligner `scripts/fleet_orchestrator.sh` sur la meme resolution que `scripts/runtime_healthcheck.sh` : choisir un python3 qui passe `import yaml`, sinon fail explicite.

[12_PROOFS]

```text
git diff --stat
scripts/fleet_orchestrator.sh | 14 +++++++++++---
1 file changed, 11 insertions(+), 3 deletions(-)
```

```text
python -m pytest tests/runtime_health/test_warn_classification.py tests/runtime_health/test_cursor_ai_windows.py -q -p no:cacheprovider
46 passed
```

```text
"C:\Program Files\Git\bin\bash.exe" -n scripts/runtime_healthcheck.sh = rc 0
"C:\Program Files\Git\bin\bash.exe" -n scripts/fleet_orchestrator.sh = rc 0
```

[15_REMAINING_GAP]

| Surface | Etat | Impact |
|---|---:|---|
| Runtime deploy | NOT_PROVEN | le correctif repo n'implique pas un redeploy systemd sur les hosts |
| Fleet stale/unreachable | OUT_OF_SCOPE | ce GO ne traite pas `student` unreachable ni `cursor-ai`/`fantome` stale |
| Parent closeout | CLOSEOUT_BLOCKED | close-gate interdit tant que le STEP 5 n'est pas rejoue sur runtime et tant que fleet reste `WARN` |

[17_CLOSE_GATE_STATUS]

```text
CHILD_GO_STATUS = PATCH_READY
PARENT_STATUS = CLOSEOUT_BLOCKED
```
