---
doc_id: GO_OPT_TRADING_RUNTIME_ORCHESTRATOR_BOOT_HEALTHCHECK_CLOSEOUT_01
doc_type: closeout
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_RUNTIME_ORCHESTRATOR_BOOT_HEALTHCHECK_01
parent_go: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01
status: closed
lifecycle_stage: closed
surface: chantier
source_kind: canonical
created_at: 2026-05-19
closed_at: 2026-05-19
commit: 46d2e6ef
---

# GO_OPT_TRADING_RUNTIME_ORCHESTRATOR_BOOT_HEALTHCHECK_CLOSEOUT_01

## Statut final

**CLOS.** Phase 1 diagnostic-only déployée et validée sur toutes les machines cibles.

## Machines validées

| Machine | overall_status | FAIL bloquants | Notes |
|---|---|---|---|
| db-layer | WARN | 0 | WARNs optionnels attendus |
| admin-trading | WARN | 0 | WARNs optionnels attendus |

## Commit de référence

```
46d2e6ef — fix(runtime_health): admin-trading map and service corrections
```

Inclut tous les livrables du chantier :
- `modules/runtime_health/healthcheck.py`
- `modules/runtime_health/machine_map.py`
- `modules/runtime_health/fleet_orchestrator.py`
- `modules/runtime_health/config/runtime_health.yml`
- `config/machine_runtime_map.yml`
- `scripts/runtime_healthcheck.sh`
- `deploy/systemd/opt-trading-runtime-health.service`
- `deploy/systemd/opt-trading-runtime-health.timer`

## WARNs résiduels — tous optionnels, attendus

Les WARNs observés sur les deux machines sont `required: false`. Exemples :

- `simex-bitget.service` — optional, intentionnellement arrêté
- `mimo_open_observer.service` — optional, non déployé
- `bot_vision_step2_send.timer` — optional, disabled intentionnellement
- `macro_xau.timer` — optional, not-found (non installé sur admin-trading)
- `openclaw_gateway` port 18789 — optional
- sessions tmux (openclaw, trading, desk) — optional
- logs `/var/log/trading/*.log` — optional (rotation/absence normale)
- artifacts age — optional, stale si non actif

Invariant : **un WARN sur un check `required: false` n'est pas un FAIL.**

## Faux FAILs corrigés

| Symptôme | Cause | Fix |
|---|---|---|
| `ALLOWED_CHAT_ID` FAIL | Clé incorrecte dans `required_env` | Remplacée par `TELEGRAM_CHAT_ID` |
| `macro_xau.timer` FAIL | En `required_timers` mais absent | Déplacé en `optional_timers` |
| `bot_vision_step2_send.timer` FAIL | En `required_timers` mais disabled | Déplacé en `optional_timers` |
| `daily-session.service` FAIL | Type=oneshot, inactive normal | Déplacé en `optional_services` (db-layer) |
| `OPENAI_API_KEY` absent | Pas de `bot_vision.env` dans le service | Ajouté `EnvironmentFile=-/opt/trading/modules/bot_vision_step2/config/bot_vision.env` |

## Invariants de phase confirmés

- **diagnostic-only** : aucun restart automatique
- **aucun secret dans les logs** : les checks ENV rapportent uniquement présent/absent
- **MACHINE_IDENTITY** : PASS sur les deux machines (hostname résolution correcte)
- **FORBIDDEN_SERVICES** : PASS sur les deux machines (aucun service interdit actif)

## Déploiement systemd actif

| Machine | Unité | État |
|---|---|---|
| db-layer | `opt-trading-runtime-health.timer` | active, runs every 5min |
| admin-trading | `opt-trading-runtime-health.service` | oneshot, manuel ou via timer |

## Prochaine étape recommandée

```
GO_OPT_TRADING_RUNTIME_ORCHESTRATOR_FLEET_STATUS_AGGREGATOR_01
```

Objectif :
- Collecter `latest.json` de chaque machine connue (sshfs → ssh → local)
- Produire `fleet_status.json` agrégé
- Détecter machine absente ou stale (> 15min)
- Notifier Telegram/Desk si une machine attendue ne répond pas
- `fleet_orchestrator.py` est déjà implémenté — il s'agit de le câbler en timer systemd sur db-layer

## RISKS

- À qualifier.
