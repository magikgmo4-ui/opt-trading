---
doc_id: GO_AUTOMATION_OPS_OPT_TRADING_CHILD_ARCHITECTURE_MAP_01_FLOW_MAP
doc_type: flow_map
repo: opt-trading
go_id: GO_AUTOMATION_OPS_OPT_TRADING_CHILD_ARCHITECTURE_MAP_01
updated_at: 2026-05-28
---

# 20_FLOW_MAP

## Flux 1 — Signal trading (production)

```
TradingView alert
  → POST /tv (webhook_server:8000)
  → risk_engine (GO_LONG/GO_SHORT, tier FULL/HALF/MICRO/NONE)
  → execution_engine (trade lifecycle)
  → position_engine (position tracking)
  → perf_engine (candidat → actif → clos)
  → POST /perf/event (perf_app:8010)
  → perf.db (SQLite WAL)
  → Telegram notify (shared/telegram_notify.py)
```

Déclencheur : webhook externe  
Gate humain : configuration risk_engine (seuils, guardrails)  
Artefact : `state/events.jsonl`, `perf/perf.db`

---

## Flux 2 — Desk Pro (opérateur)

```
Opérateur
  → desk_pro_runner (modules/desk_pro_runner/)
  → desk_pro_orchestrator (import dynamique: portfolio_engine, probability_engine, desk_pro_dashboard)
  → desk_pro_dashboard (API données + UI)
  → perf_app:8010 (lecture résultats)
  → localcms:8700 (cockpit navigation)
```

Déclencheur : manuel opérateur  
Gate humain : lancement runner + décisions dashboard  
Artefact : aucun écrit — lecture seule (localcms, dashboard)

---

## Flux 3 — OpenClaw ops

```
Opérateur / IDE ChatGPT
  → GO_PROMPT émis
  → openclaw_config_modulaire apply_safe.sh
    → ~/.openclaw/config.d/ (agents.json5, tools.json5)
    → gateway_openclaw start.sh (session tmux openclaw-gateway)
    → openclaw_tmux_operator (commandes tmux)
  → rollback.sh si besoin
```

Déclencheur : manuel opérateur (jamais automatique)  
Gate humain : apply_safe.sh + validation résultat + rollback si besoin  
Artefact : `~/.openclaw/config.d/` modifié

---

## Flux 4 — CI/CD GitHub Actions

```
git push / PR → sot/mainline
  → gated-pr.yml (gate principal)
  → [si paths concernés] :
      openclaw-mcp-policy-static-validator.yml
      openclaw-skill-policy-warning-only.yml
      gh-actions-registry-validation.yml
      strict-workers-validate.yml
      strict-workers-smoke.yml
  → [cron lundi 08:00] :
      strict-workers-schedule.yml
```

Déclencheur : git event (push/PR) ou cron  
Gate humain : review PR + merge  
Artefact : CI status checks, rapports validators

---

## Flux 5 — AI Workers (semi-automatisé)

```
ChatGPT gouvernance
  → GO_PROMPT validé par opérateur
  → IDE / Claude Code (run_task.sh)
    → job_packets/<GO_ID>*.json (30 packets)
    → workers Python spécialisés
      (ledger_*, doc_ops_*, strict_worker_*, signal_*, repo_*, ops)
    → git commits + PR créée
  → tests CI automatiques
  → opérateur review screenshot + 7_CANONICAL_STATE
  → gh pr merge (sur instruction)
  → next GO
```

Déclencheur : GO_PROMPT validé par opérateur  
Gate humain : validation GO_PROMPT + merge PR + post-merge audit  
Artefact : commits git, docs chantiers, PR, rapports

---

## Flux 6 — Fleet health

```
[schedule ou manuel]
  → runtime_health/healthcheck.py (tmux lecture seule)
  → fleet_orchestrator.py (SSH cursor-ai + fantome)
  → Telegram notify (état fleet)
```

Déclencheur : schedule ou manuel  
Gate humain : réaction aux alertes Telegram  
Artefact : logs healthcheck, alertes Telegram

---

## Flux 7 — Data collection

```
[manuel ou schedule]
  → collector_binance_spot (oneshot, public API)
  → derivatives_collector
      → bot_vision_step2 (headless Playwright)
      → Coinglass (données OI/Funding/Liq)
  → artifacts/ (résultats JSON)
```

Déclencheur : manuel ou schedule opérateur  
Gate humain : lancement + validation données  
Artefact : `artifacts/` JSON

---

## Dépendances transversales

| Consommateur | Dépend de | Nature |
|---|---|---|
| Tous modules | `modules/env/env.py` | load_env + ensure_dirs |
| Tous modules | `shared/logger.py` | setup_logger |
| Desk Pro | `portfolio_engine`, `probability_engine` | import dynamique |
| Telegram | `shared/telegram_notify.py` | alertes métriques |
| Perf | `adapters/webhook_to_perf.py` | normalisation boundary |
| AI workers | `run_task.sh` + `_validate_job.py` | entry point unique |
| OpenClaw | `openclaw_config_modulaire` | config base apply/rollback |
