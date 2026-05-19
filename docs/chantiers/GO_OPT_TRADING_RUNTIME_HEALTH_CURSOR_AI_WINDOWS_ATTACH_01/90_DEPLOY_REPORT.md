# GO_OPT_TRADING_RUNTIME_HEALTH_CURSOR_AI_WINDOWS_ATTACH_01 — Deploy Report

Date: 2026-05-19

## Verdict : PATCH MERGED — awaiting cursor-ai first run

---

## Contexte

`cursor-ai` existait dans `machine_runtime_map.yml` avec des chemins Linux hardcodés
(`/opt/trading`, `/opt/trading/venv`, systemd) incompatibles avec la machine Windows réelle.
Repo confirmé : `C:\Users\ghost\opt-trading`.

---

## Patch mergé — PR #592

| Fichier | Changement |
|---------|-----------|
| `config/machine_runtime_map.yml` | `os_family: windows`, `repo_root_candidates`, `data_dir_candidates`, `required_paths: []`, `required_venvs: []` |
| `modules/runtime_health/machine_map.py` | `build_config_from_scope` résout `data_dir` depuis candidates ; `check_forbidden_services` → PASS sans `systemctl` |
| `modules/runtime_health/healthcheck.py` | `_IS_WINDOWS = platform.system() == "Windows"` ; `check_venv` supporte `Scripts/python.exe` |
| `modules/runtime_health/fleet_orchestrator.py` | `_collect_via_ssh_windows` (SSH + PowerShell) ; dispatch sur `os_family` ; `run_fleet` passe le scope |
| `tests/runtime_health/test_cursor_ai_windows.py` | 25/25 PASS |

---

## Fleet dry-run post-merge (2026-05-19T11:08:01Z)

```json
{
  "fleet_status": "WARN",
  "healthy": ["fantome"],
  "warning": ["admin-trading", "db-layer", "cursor-ai", "student"],
  "unreachable": ["cursor-ai"]
}
```

**cursor-ai = WARN/unreachable** — comportement attendu : `latest.json` n'existe pas encore
sur la machine Windows. Le dispatch PowerShell est actif ; plus aucune commande
`cat /opt/trading/...` n'est envoyée à cursor-ai.

---

## Action requise sur cursor-ai Windows

```powershell
# 1. Aller dans le repo
cd C:\Users\ghost\opt-trading

# 2. Synchroniser sot/mainline
git fetch origin
git checkout sot/mainline
git pull

# 3. Exécuter le healthcheck (premier run)
python modules\runtime_health\healthcheck.py --no-telegram

# 4. Vérifier la sortie
Get-Content data\runtime_health\latest.json | ConvertFrom-Json | Select overall_status, block_statuses
```

Résultat attendu :
- `overall_status` = PASS ou WARN (pas FAIL bloquant)
- `data\runtime_health\latest.json` créé
- Pas d'erreur systemd (SYSTEMD_SERVICES/TIMERS vides → PASS)

---

## Validation fleet après run cursor-ai

Depuis db-layer ou admin-trading :

```bash
python3 modules/runtime_health/fleet_orchestrator.py --dry-run
```

Résultat cible :

```
"healthy": [..., "cursor-ai"]   # ou "warning" si WARN — acceptable
"unreachable": []               # cursor-ai plus dans unreachable
```

---

## Next GO

Si cursor-ai passe reachable dans le fleet → closeout `GO_OPT_TRADING_FLEET_HEALTH_GLOBAL_CLOSEOUT_01`.
