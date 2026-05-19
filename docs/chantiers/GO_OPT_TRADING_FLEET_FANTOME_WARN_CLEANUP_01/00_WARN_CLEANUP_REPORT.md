---
go_id: GO_OPT_TRADING_FLEET_FANTOME_WARN_CLEANUP_01
doc_type: warn_cleanup_report
status: CLOSED / MERGED
closed_at: 2026-05-19
---

# GO_OPT_TRADING_FLEET_FANTOME_WARN_CLEANUP_01

## 1_MASTER_TARGET

Corriger les WARNs fantome issus de defaults admin-trading incorrectement appliqués.
Avant : HTTP/ARTIFACTS/LOGS/ORCHESTRATOR WARN sur checks qui n'appartiennent pas à fantome.

---

## 7_CANONICAL_STATE

```text
WARN_CLEANUP = CLOSED / MERGED
CODE_CHANGES = modules/runtime_health/machine_map.py + config/machine_runtime_map.yml
UNITTEST = 111/111 PASS
HTTP = WARN → PASS
ARTIFACTS = WARN → PASS
LOGS = WARN → PASS
REMAINING_WARN = SYSTEMD_SERVICES + ENV + PORTS + ORCHESTRATOR (gaps réels)
```

## Root cause

`build_config_from_scope` dans `machine_map.py` n'overridait pas `http`, `artifacts`,
`logs.log_files` et `orchestrator` — ils tombaient sur `DEFAULT_CONFIG` (admin-trading).

## Fix

**`modules/runtime_health/machine_map.py`** — `build_config_from_scope` :
ajout de 4 overrides conditionnels activés par des clés YAML dans le scope machine :

| Clé YAML scope | Bloc overridé | Comportement |
|---|---|---|
| `optional_http_checks` | `http.optional` | Vide = aucun check HTTP |
| `required_http_checks` | `http.required` | — |
| `optional_artifact_paths` | `artifacts.optional` | Vide = aucun check artifact |
| `optional_log_files` | `logs.log_files.optional` | Vide = aucun check log file |
| `optional_tmux_sessions` | `orchestrator.tmux_sessions.optional` | Réduit à `[openclaw]` |

**`config/machine_runtime_map.yml`** — section `fantome` :

```yaml
optional_http_checks: []
optional_artifact_paths: []
optional_log_files: []
optional_tmux_sessions:
  - openclaw
```

## Résultat post-fix (fantome live)

| Bloc | Avant | Après |
|---|---|---|
| HTTP | WARN (webhook_health, perf_summary) | **PASS** |
| ARTIFACTS | WARN (desk_pro/vision, desk/snapshots) | **PASS** |
| LOGS | WARN (webhook.log, perf.log, bot_vision.log) | **PASS** |
| ORCHESTRATOR | WARN (openclaw, trading, desk) | WARN (openclaw seul — non déployé) |

## WARNs restants — gaps réels

| Bloc | Raison | Action requise |
|---|---|---|
| SYSTEMD_SERVICES | `openclaw-gateway.service` optional, inactive | Déployer openclaw sur fantome |
| ENV | `TELEGRAM_BOT_TOKEN` absent dans `.env` fantome | Configurer si Telegram requis |
| PORTS | port 18789 non bound (suit openclaw) | Suit SYSTEMD_SERVICES |
| ORCHESTRATOR | tmux `openclaw` session absent | Démarre avec openclaw |

## Compatibilité

admin-trading : **inchangé** — aucune clé override présente → DEFAULT_CONFIG preservé.
Toutes les autres machines : inchangées.

## Corrections additionnelles (fantome map scope)

Suite à clarification : `openclaw-gateway` est sur db-layer (pas fantome), tmux sessions
orchestrées depuis db-layer via openclaw (non démarrées localement), `TELEGRAM_BOT_TOKEN`
non requis sur fantome. Map nettoyé :

| Clé | Avant | Après |
|---|---|---|
| `optional_services` | `[openclaw-gateway.service]` | `[]` |
| `optional_ports` | `[{openclaw_gateway, 18789}]` | `[]` |
| `optional_env` | `[TELEGRAM_BOT_TOKEN]` | `[]` |
| `optional_tmux_sessions` | `[openclaw]` | `[]` |

## Résultat final (fantome live)

```
overall_status: PASS
  ✓ MACHINE_IDENTITY: PASS
  ✓ SYSTEMD_SERVICES: PASS
  ✓ SYSTEMD_TIMERS: PASS
  ✓ FORBIDDEN_SERVICES: PASS
  ✓ VENV: PASS
  ✓ ENV: PASS
  ✓ PORTS: PASS
  ✓ HTTP: PASS
  ✓ PATHS: PASS
  ✓ ARTIFACTS: PASS
  ✓ LOGS: PASS
  ✓ ORCHESTRATOR: PASS
```

## VERDICT

```text
PASS — 12/12 blocs PASS sur fantome

HTTP/ARTIFACTS/LOGS fixes  : PASS
Map scope nettoyé           : PASS
overall_status fantome      : PASS (was WARN)
admin-trading unaffected    : PASS
Tests 111/111               : PASS
```
