---
doc_id: RUNTIME_HEALTHCHECK_01_INITIAL
doc_type: chantier_initial
repo: opt-trading
go_id: GO_OPT_TRADING_RUNTIME_ORCHESTRATOR_BOOT_HEALTHCHECK_01
parent_go: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01
status: active
lifecycle_stage: impl
surface: chantier
source_kind: canonical
created_at: 2026-05-18
updated_at: 2026-05-18
---

# 00_INITIAL_PROJECT_DOC — Runtime Health Supervisor

## OBJECTIF

Créer une brique "Runtime Health Supervisor" diagnostic-only (Phase 1) pour opt-trading.
Fournir une visibilité complète sur l'état du runtime à chaque boot et toutes les 5 minutes,
sans aucune action corrective automatique et sans jamais exposer de secrets dans les logs.

## ÉTAT CANONIQUE

- Phase 1 : IMPL (implémentation initiale complète)
- Phase 2 (self-heal) : OPEN / backlog

## CHECKS COUVERTS

| Bloc              | Checks                                                              |
|-------------------|---------------------------------------------------------------------|
| SYSTEMD_SERVICES  | tv-webhook, tv-perf, bot_vision_step2 (required) + simex-bitget (opt)|
| SYSTEMD_TIMERS    | bot_vision_step2_prune, bot_vision_step2_send, macro_xau (required) |
| VENV              | /opt/trading/venv (required), bot_vision_step2 venv (optional)      |
| ENV               | TELEGRAM_BOT_TOKEN, ALLOWED_CHAT_ID, OPENAI_API_KEY (required)      |
| PORTS             | webhook:8000, desk_pro:8010, openclaw_gateway:18789 (optional)      |
| HTTP              | /health sur 8000, /perf/summary sur 8010 (optional)                 |
| PATHS             | /opt/trading, /var/log/trading, vision dirs (required)              |
| ARTIFACTS         | desk_vision_dir, desk_snapshots_dir age < 120min (optional)         |
| LOGS              | journalctl -p err sur unités + tail logfiles                        |
| ORCHESTRATOR      | tmux sessions openclaw, trading, desk (optional)                    |

## ARCHITECTURE

```
modules/runtime_health/
├── __init__.py
├── healthcheck.py              # Script principal (stdlib only, yaml optionnel)
├── config/
│   └── runtime_health.yml      # Config declarative des checks
├── schemas/
│   └── runtime_health.schema.json  # JSON Schema draft-07
└── README.md

scripts/
└── runtime_healthcheck.sh      # Wrapper shell systemd (résolution python)

deploy/systemd/
├── opt-trading-runtime-health.service  # Type=oneshot, User=ghost
└── opt-trading-runtime-health.timer    # OnBootSec=90s, OnUnitActiveSec=5min
```

### Flux d'exécution

1. Timer déclenche le service (boot+90s, puis toutes les 5min)
2. `runtime_healthcheck.sh` résout l'interpréteur Python (venv → système)
3. `healthcheck.py` charge `runtime_health.yml`
4. Exécute les 10 blocs de checks en séquence
5. Calcule le statut global (FAIL > WARN > PASS)
6. Écrit `latest.json` + appende à `healthcheck.jsonl`
7. Si statut change ET WARN/FAIL : notifie Telegram (token jamais loggé)
8. Exit 0 (PASS/WARN) ou 1 (FAIL)

## LIVRABLES

| Fichier | Rôle |
|---------|------|
| `modules/runtime_health/__init__.py` | Package marker |
| `modules/runtime_health/healthcheck.py` | Script principal |
| `modules/runtime_health/config/runtime_health.yml` | Config déclarative |
| `modules/runtime_health/schemas/runtime_health.schema.json` | JSON Schema |
| `modules/runtime_health/README.md` | Documentation opérationnelle |
| `scripts/runtime_healthcheck.sh` | Wrapper shell (+x) |
| `deploy/systemd/opt-trading-runtime-health.service` | Unité systemd |
| `deploy/systemd/opt-trading-runtime-health.timer` | Timer systemd |

## CONTRAINTES PHASE 1

- Diagnostic-only : zéro action corrective automatique, zéro restart
- Aucun secret dans les logs, outputs ou messages Telegram (valeurs env omises)
- Stdlib uniquement — `pyyaml` optionnel (try/except, fallback dict)
- Exit 0 pour PASS ou WARN, exit 1 pour FAIL bloquant
- Compatible Debian 12, Python 3.11+, systemd
- Notifications Telegram sur changement d'état uniquement (configurable)
- `NoNewPrivileges=true` dans le service systemd

## PHASE 2 SELF-HEAL (future)

Points prévus mais hors scope Phase 1 :
- Restart automatique de services FAIL (avec circuit breaker)
- Nettoyage artifacts stale automatique
- Alertes PagerDuty / webhook externe
- Métriques Prometheus/Grafana (exposition via HTTP)
- Corrélation cross-machine (multi-host)
- Escalade automatique si N runs consécutifs en FAIL

## POINTS D'EXTENSION

- `runtime_health.yml` : ajouter de nouveaux blocs sans modifier le code
- Chaque check retourne un dict structuré → extensible (métriques, labels)
- `healthcheck.jsonl` : exploitable par tout outil d'analyse time-series
- JSON Schema : permettra la validation CI des rapports
- Timer `Persistent=true` : rattrapage des runs manqués (reboot long)

## RISKS

- À qualifier.
