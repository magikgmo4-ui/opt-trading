# GO_OPT_TRADING_RUNTIME_HEALTH_FLEET_WARN_CLASSIFICATION_01

Date: 2026-05-19  
Verdict: **CLOSED — scope nettoyé, WARN résiduels classifiés EXPECTED**

---

## Contexte

Post `cursor-ai PASS`, fleet état : `healthy=[cursor-ai, fantome]`, `warning=[admin-trading, db-layer, student]`.  
Objectif : classifier chaque WARN et supprimer les faux positifs du scope.

---

## Classification détaillée

### admin-trading

| Check | Statut | Classification | Action |
|-------|--------|---------------|--------|
| `service:simex-bitget` | WARN | **EXPECTED** | Optional, non requis Phase 1 |
| `service:mimo_open_observer` | WARN | **EXPECTED** | Optional, non requis |
| `timer:bot_vision_step2_send` | WARN | **EXPECTED** | Optional timer non actif |
| `timer:macro_xau` | WARN | **EXPECTED** | Optional timer non actif |
| `env:TV_WEBHOOK_KEY` | WARN | **EXPECTED** | Optional env var |
| `port:openclaw_gateway` | WARN | **EXPECTED** | Optional, openclaw non actif |
| `http:webhook_health` (404) | WARN | **FALSE_POSITIVE** | `/health` non implémenté sur tv-webhook → supprimé |
| `artifact:desk_vision_dir` (76j stale) | WARN | **EXPECTED** | Dry-run Phase 1, artifacts non mis à jour |
| `logfile_errors:/var/log/trading/*.log` | WARN | **FALSE_POSITIVE** | Logs dans journald (log_units), pas fichiers → supprimé |
| `tmux:openclaw/trading/desk` | WARN | **EXPECTED** | Sessions présentes en normal ops, down Phase 1 — conservées pour visibilité |

### db-layer

| Check | Statut | Classification | Action |
|-------|--------|---------------|--------|
| `venv:main` | WARN | **EXPECTED** | Optional (`required:false`), non installé sur db-layer |
| `env:TELEGRAM_BOT_TOKEN/ALLOWED_CHAT_ID` | WARN | **EXPECTED** | Optional env vars |
| `port:openclaw_gateway` | WARN | **EXPECTED** | Optional, openclaw non actif |
| `http:webhook_health` (404) | WARN | **FALSE_POSITIVE** | Pas de webhook sur db-layer → supprimé |
| `path:/var/log/trading` | WARN | **EXPECTED** | Optional path, non créé sur db-layer |
| `artifact:desk_vision_dir/snapshots` | WARN | **FALSE_POSITIVE** | Desk sur admin-trading, pas db-layer → supprimé |
| `logfile_errors:/var/log/trading/*.log` | WARN | **FALSE_POSITIVE** | Journald uniquement sur db-layer → supprimé |
| `tmux:openclaw/trading/desk` | WARN | **FALSE_POSITIVE** | Sessions trading pas sur db-layer → supprimé |

### student

| Check | Statut | Classification | Action |
|-------|--------|---------------|--------|
| `service:snap.ollama.listener` | WARN | **EXPECTED** | Optional, ollama non actif |
| `env:TELEGRAM_BOT_TOKEN/OPENAI_API_KEY` | WARN | **EXPECTED** | Optional env vars |
| `http:webhook_health/perf_summary` | WARN | **FALSE_POSITIVE** | Pas de webhook/perf sur student → supprimé |
| `artifact:desk_vision_dir` (80j stale) | WARN | **FALSE_POSITIVE** | Desk sur admin-trading, pas student → supprimé |
| `artifact:desk_snapshots_dir` | WARN | **FALSE_POSITIVE** | Idem → supprimé |
| `logfile_errors:/var/log/trading/*.log` | WARN | **FALSE_POSITIVE** | Journald uniquement → supprimé |
| `tmux:openclaw/trading/desk` | WARN | **FALSE_POSITIVE** | Sessions trading pas sur student → supprimé |

---

## Patch appliqué — `machine_runtime_map.yml`

### admin-trading
```yaml
optional_http_checks: []      # /health non implémenté
optional_log_files: []        # logs via journald (log_units)
optional_tmux_sessions:       # explicite (conservé pour visibilité)
  - openclaw
  - trading
  - desk
```

### db-layer
```yaml
optional_http_checks: []
optional_artifact_paths: []
optional_log_files: []
optional_tmux_sessions: []
```

### student
```yaml
optional_http_checks: []
optional_artifact_paths: []
optional_log_files: []
optional_tmux_sessions: []
```

---

## WARN résiduels attendus post-patch

| Machine | WARN restants | Nature |
|---------|--------------|--------|
| admin-trading | services opt down, timers opt down, env opt absent, port openclaw down, artifact stale, tmux down | Tous EXPECTED — Phase 1 dry-run |
| db-layer | venv opt absent, env opt absent, port openclaw down, path opt absent | Tous EXPECTED — machine data |
| student | service ollama down, env opt absent | Tous EXPECTED — sandbox |

---

## Next GO

Aucun WARN_ACTIONABLE identifié. État fleet acceptable pour Phase 1.

Prochaine décision : `GO_OPT_TRADING_RUNTIME_HEALTH_FLEET_TIMER_STUDENT_01` si besoin de timer healthcheck sur student, ou attendre seuil Phase 1.
