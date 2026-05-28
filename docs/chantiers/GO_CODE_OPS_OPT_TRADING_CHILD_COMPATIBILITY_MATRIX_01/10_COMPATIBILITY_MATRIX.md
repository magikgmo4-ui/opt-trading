---
doc_id: GO_CODE_OPS_OPT_TRADING_CHILD_COMPATIBILITY_MATRIX_01_MATRIX
doc_type: compatibility_matrix
repo: opt-trading
project: opt-trading
module: code_ops
go_id: GO_CODE_OPS_OPT_TRADING_CHILD_COMPATIBILITY_MATRIX_01
status: open
lifecycle_stage: matrix_v1_complete
topic_keys: [compatibility, debian, windows, wsl, tmux, gha, json, utf8, code_ops]
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-05-28
---

# 10_COMPATIBILITY_MATRIX — v1

Matrice de compatibilité `opt-trading` — audit du 2026-05-28.

Légende :
- `PASS` — compatible, vérifié
- `PASS_WITH_LIMITS` — compatible avec limite documentée
- `REWORK` — correction requise avant usage durable
- `N/A` — surface non concernée
- `UNKNOWN` — non audité dans cette passe

---

## Section 1 — Services FastAPI (entrées production)

| path | debian_bash | windows | wsl | tmux | gha | json_out | utf8 | verdict |
|---|---|---|---|---|---|---|---|---|
| `webhook_server.py` | PASS | PASS_WITH_LIMITS¹ | PASS | N/A | N/A | PASS_WITH_LIMITS² | PASS | PASS_WITH_LIMITS |
| `perf/perf_app.py` | PASS | PASS_WITH_LIMITS¹ | PASS | N/A | N/A | PASS_WITH_LIMITS² | PASS | PASS_WITH_LIMITS |
| `bitget_bridge.py` | PASS | PASS_WITH_LIMITS¹ | PASS | N/A | N/A | N/A | PASS | PASS_WITH_LIMITS |

¹ Python portable, mais Bash wrappers nécessitent WSL ou Git Bash sur Windows.
² `json.dumps` sans `ensure_ascii=False` — safe pour données trading ASCII.

---

## Section 2 — Moteurs runtime

| path | debian_bash | windows | wsl | tmux | gha | json_out | utf8 | verdict |
|---|---|---|---|---|---|---|---|---|
| `modules/risk_engine/app/risk_engine.py` | PASS | PASS_WITH_LIMITS¹ | PASS | N/A | PASS | PASS_WITH_LIMITS² | PASS | PASS_WITH_LIMITS |
| `modules/execution_engine/app/execution_engine.py` | PASS | PASS_WITH_LIMITS¹ | PASS | N/A | PASS | PASS_WITH_LIMITS² | PASS | PASS_WITH_LIMITS |
| `modules/execution_engine/executor.py` | PASS | PASS_WITH_LIMITS¹ | PASS | N/A | N/A | PASS | PASS | PASS_WITH_LIMITS |
| `modules/position_engine/app/position_engine.py` | PASS | PASS_WITH_LIMITS¹ | PASS | N/A | N/A | PASS | PASS | PASS_WITH_LIMITS |
| `modules/decision_engine/app/decision_engine.py` | PASS | PASS_WITH_LIMITS¹ | PASS | N/A | N/A | PASS_WITH_LIMITS² | PASS | PASS_WITH_LIMITS |
| `modules/decision_engine/app/strategy_logic.py` | PASS | PASS_WITH_LIMITS¹ | PASS | N/A | N/A | N/A | PASS | PASS_WITH_LIMITS |
| `modules/perf_engine/app/perf_engine.py` | PASS | PASS_WITH_LIMITS¹ | PASS | N/A | N/A | PASS_WITH_LIMITS² | PASS | PASS_WITH_LIMITS |
| `modules/journal_engine/app/journal_engine.py` | PASS | PASS_WITH_LIMITS¹ | PASS | N/A | N/A | PASS | PASS | PASS_WITH_LIMITS |
| `modules/engines/router.py` | PASS | PASS_WITH_LIMITS¹ | PASS | N/A | N/A | N/A | PASS | PASS_WITH_LIMITS |
| `modules/trade_executor/app/executor.py` | PASS | PASS_WITH_LIMITS¹ | PASS | N/A | N/A | PASS | PASS | PASS_WITH_LIMITS |

---

## Section 3 — Scripts shell (audit shebang)

| path | shebang | debian_bash | windows | wsl | verdict |
|---|---|---|---|---|---|
| `modules/desk_pro/desk_pro_dry_run.sh` | `#!/bin/bash` | PASS | N/A | PASS_WITH_LIMITS | **REWORK** — migrer vers `#!/usr/bin/env bash` |
| `scripts/ai/workers/run_task.sh` | `#!/bin/bash` | PASS | N/A | PASS_WITH_LIMITS | **REWORK** — migrer vers `#!/usr/bin/env bash` |
| Tous autres scripts (771) | `#!/usr/bin/env bash` | PASS | N/A | PASS | PASS |

---

## Section 4 — GitHub Actions workflows

| path | ubuntu | windows | macos | python_version | verdict |
|---|---|---|---|---|---|
| `.github/workflows/gated-pr.yml` | PASS | N/A | N/A | 3.x | PASS |
| `.github/workflows/gh-actions-registry-validation.yml` | PASS | N/A | N/A | 3.11 | PASS |
| `.github/workflows/openclaw-mcp-policy-static-validator.yml` | PASS | N/A | N/A | 3.11 | PASS |
| `.github/workflows/openclaw-skill-policy-warning-only.yml` | PASS | N/A | N/A | 3.11 | PASS |
| `.github/workflows/strict-workers-schedule.yml` | PASS | N/A | N/A | 3.11 | PASS |
| `.github/workflows/strict-workers-smoke.yml` | PASS | N/A | N/A | 3.11 | PASS |
| `.github/workflows/strict-workers-validate.yml` | PASS | N/A | N/A | 3.11 | PASS |

Note : tous les workflows utilisent `ubuntu-latest`. Aucun CI Windows/macOS déclaré.
La version Python varie entre `3.x` (floating) et `3.11` (pinned) selon le workflow.
Recommandation : homogénéiser sur `3.11` dans un batch dédié.

---

## Section 5 — Modules tmux-dépendants

| path | debian_bash | windows_native | wsl | tmux_requis | verdict |
|---|---|---|---|---|---|
| `modules/gateway_openclaw/scripts/start.sh` | PASS | N/A | PASS | oui | PASS_WITH_LIMITS³ |
| `modules/gateway_openclaw/scripts/attach.sh` | PASS | N/A | PASS | oui | PASS_WITH_LIMITS³ |
| `modules/localcms/app/main.py` | PASS | N/A | PASS | lecture seule | PASS_WITH_LIMITS³ |
| `modules/openclaw_tmux_operator/scripts/` | PASS | N/A | PASS | oui | PASS_WITH_LIMITS³ |
| `modules/runtime_health/healthcheck.py` | PASS | N/A | PASS | lecture seule | PASS_WITH_LIMITS³ |

³ tmux non disponible sur Windows natif — Windows = N/A pour ces surfaces.

---

## Section 6 — JSON outputs et UTF-8

| surface | ensure_ascii | utf8_safe | verdict | note |
|---|---|---|---|---|
| `adapters/webhook_to_perf.py` | `False` (explicite) | oui | PASS | conforme |
| `modules/risk_engine/` | absent | oui (données ASCII) | PASS_WITH_LIMITS | safe pour trading data |
| `modules/execution_engine/` | absent | oui (données ASCII) | PASS_WITH_LIMITS | safe pour trading data |
| `modules/decision_engine/` | absent | oui (données ASCII) | PASS_WITH_LIMITS | safe pour trading data |
| `modules/perf_engine/` | absent | oui (données ASCII) | PASS_WITH_LIMITS | safe pour trading data |
| `deploy_module_multi_machine/` | `False` (explicite) | oui | PASS | conforme |
| Logs Telegram | `False` (explicite) | oui | PASS | conforme |

---

## Section 7 — Chemins et path handling

| surface | pathlib / os.path.join | hardcoded sep | verdict |
|---|---|---|---|
| Modules Python (329 fichiers) | oui | non | PASS |
| `modules/runtime_health/fleet_orchestrator.py:122` | oui | `\\latest.json` (intentionnel PowerShell) | PASS_WITH_LIMITS⁴ |
| Scripts e2e (line-continuation `\\`) | N/A (docstring) | non | PASS |

⁴ Le `\\` dans `fleet_orchestrator.py` est intentionnel — il construit un chemin PowerShell
pour la machine `cursor-ai` (Windows). À préserver lors de tout refactor.

---

## Contraintes à respecter dans les refactors futurs

| Contrainte | Scope | Action si violation |
|---|---|---|
| Ne pas changer `#!/bin/bash` en `#!/usr/bin/env bash` sans tester sur CI | scripts | tester avant merge |
| Préserver `\\latest.json` dans fleet_orchestrator | Windows path | ne pas "corriger" vers `/` |
| Ne pas supprimer tmux checks dans localcms/healthcheck | runtime | verrouiller par test |
| Homogénéiser python-version GHA sur 3.11 | CI | batch dédié |
| `ensure_ascii` dans modules HIGH si données non-ASCII introduites | JSON | ADD si besoin prouvé |
