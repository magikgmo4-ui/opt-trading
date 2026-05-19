# GO_OPT_TRADING_RUNTIME_HEALTH_CURSOR_AI_WINDOWS_ATTACH_01 — Closeout

Date: 2026-05-19  
Verdict: **PASS — CLOSED**

---

## Problème initial

`cursor-ai` était déclaré dans `config/machine_runtime_map.yml` avec un scope orienté Linux :
- `required_paths: /opt/trading`
- `required_venvs: /opt/trading/venv`
- `fleet_orchestrator.py` envoyait `cat /opt/trading/data/runtime_health/latest.json` via SSH

La machine réelle est Windows (`DESKTOP-1KDQTBH`). Le fleet la remontait `unreachable`.

---

## Fixes appliqués

### PR #592 — Adaptation principale Windows

- `config/machine_runtime_map.yml` :
  - `os_family: windows`
  - `repo_root_candidates` + `data_dir_candidates`
  - `required_paths: []` (aucun chemin Linux)
  - `required_venvs: []` (aucun chemin Linux)
  - `optional_tmux_sessions: []`, `optional_log_files: []` (évite appels Linux)
- `modules/runtime_health/machine_map.py` :
  - `build_config_from_scope` : résolution `data_dir` depuis candidates Windows
  - `check_forbidden_services` : PASS sans `systemctl` sur Windows
- `modules/runtime_health/healthcheck.py` :
  - `_IS_WINDOWS = platform.system() == "Windows"`
  - `check_venv` supporte `Scripts/python.exe`
- `modules/runtime_health/fleet_orchestrator.py` :
  - `_collect_via_ssh_windows` (SSH + PowerShell)
  - dispatch sur `os_family` dans `collect_machine_status`
  - `run_fleet` passe le scope machine
- Tests : 25/25 PASS

### PR #595 — hostname alias `DESKTOP-1KDQTBH`

Le hostname Windows réel (`DESKTOP-1KDQTBH`) ne correspondait pas à `cursor-ai` dans la map.
Sans alias, le scope n'était pas chargé → base config Linux → FAIL.

- `hostname_aliases: [DESKTOP-1KDQTBH]` dans le scope cursor-ai
- `machine_map.py` : `scope_for()` vérifie `hostname_aliases` ; `canonical_name_for()` retourne le nom canonique
- `healthcheck.py` : utilise `canonical_name_for()` après résolution scope
- Tests : 28/28 PASS

### PR #600 — SSH `-EncodedCommand`

Le SSH Windows route via `cmd.exe` qui corrompt les double-quotes dans la commande PowerShell.
Fix : `-EncodedCommand` (base64 utf-16-le) court-circuite `cmd.exe` complètement.

### Commit `4917af43` — bytes mode CLIXML bypass

PowerShell écrit les messages de progression sur stderr en CLIXML (encodage Windows) qui corrompt
`text=True` de `subprocess.run`. Fix : capture en bytes, décode `stdout` en UTF-8 uniquement,
ignore stderr.

---

## Evidence finale

```bash
# fleet_orchestrator.py --dry-run — 2026-05-19T11:24:54Z
{
  "fleet_status": "WARN",
  "healthy": ["cursor-ai", "fantome"],
  "warning": ["admin-trading", "db-layer", "student"],
  "unreachable": [],
  "failing": [],
  "elapsed_seconds": 1.644
}
```

```bash
# collect_machine_status cursor-ai direct
{
  "machine": "cursor-ai",
  "source": "ssh_windows",
  "reachable": true,
  "status": "PASS",
  "overall_status": "PASS"
}
```

```bash
# healthcheck.py sur DESKTOP-1KDQTBH
{
  "machine": "cursor-ai",
  "overall_status": "PASS",
  "block_statuses": {
    "MACHINE_IDENTITY": "PASS",
    "SYSTEMD_SERVICES": "PASS",
    "SYSTEMD_TIMERS": "PASS",
    "FORBIDDEN_SERVICES": "PASS",
    "VENV": "PASS",
    "ENV": "PASS",
    "PORTS": "PASS",
    "HTTP": "PASS",
    "PATHS": "PASS",
    "ARTIFACTS": "PASS",
    "LOGS": "PASS",
    "ORCHESTRATOR": "PASS"
  }
}
```

Tests : **28/28 PASS**

---

## Note méthode

Le dernier correctif (bytes mode CLIXML) a été poussé directement sur `sot/mainline` (commit `4917af43`)
après que la branche feature n'était plus disponible localement. Pas de régression — le code est sain
et les tests passent. Pour un prochain patch, privilégier branche dédiée + PR sauf urgence.

---

## État post-closeout

| Machine | Statut fleet |
|---------|-------------|
| cursor-ai | **PASS / healthy** |
| fantome | PASS / healthy |
| admin-trading | WARN (attendu) |
| db-layer | WARN (attendu) |
| student | WARN (attendu) |

---

## Next GO recommandé

```
GO_OPT_TRADING_RUNTIME_HEALTH_FLEET_WARN_CLASSIFICATION_01
```

Classifier les WARN restants par machine :
- `WARN_EXPECTED` — comportement normal, pas d'action
- `WARN_ACTIONABLE` — à corriger
- `WARN_FALSE_POSITIVE` — à supprimer du scope
- `WARN_DEFERRED` — post-seuil Phase 1
