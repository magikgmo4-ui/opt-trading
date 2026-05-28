---
doc_id: GO_AUTOMATION_OPS_OPT_TRADING_PARENT_ARCHITECTURE_JOBS_SEMIAUTO_REFACTOR_01_ARCH_SCOPE
doc_type: architecture_scope
repo: opt-trading
go_id: GO_AUTOMATION_OPS_OPT_TRADING_PARENT_ARCHITECTURE_JOBS_SEMIAUTO_REFACTOR_01
status: open
updated_at: 2026-05-28
---

# 10_ARCHITECTURE_REFACTOR_SCOPE

## Objectif

Définir ce que "refactor architecture" signifie dans ce chantier.
Ce document est un cadre de scope, pas un inventaire. L'inventaire réel est produit par le child GO.

## Périmètre

### Surfaces à cartographier

| Surface | Description | Type |
|---|---|---|
| FastAPI services | webhook_server, perf_app, localcms | runtime |
| Modules runtime | risk_engine, execution_engine, position_engine, decision_engine, perf_engine | runtime |
| Modules desk | desk_pro, desk_pro_runner, desk_pro_orchestrator, desk_pro_dashboard | runtime |
| OpenClaw suite | gateway_openclaw, openclaw_config_modulaire, openclaw_tmux_operator | ops |
| GitHub Actions | 7 workflows GHA (.github/workflows/) | CI/CD |
| Scripts opérateurs | scripts/ai/workers/, scripts/deploy_*, scripts/smoke.sh | ops |
| AI workers | scripts/ai/workers/*.json, run_task.sh | automation |
| Collectors | collector_binance_spot, derivatives_collector | data |
| Vision family | vision_bot, bot_vision_step2 | data |
| Tools | tools/strategy/*, tools/governance/* | tooling |

### Flux à cartographier

| Flux | De | Vers | Déclencheur |
|---|---|---|---|
| Signal trading | TradingView → webhook_server | risk_engine → execution_engine | webhook |
| Perf tracking | execution_engine → perf_app | perf.db | event |
| Desk Pro | desk_pro_runner → orchestrator → dashboard | localcms UI | cron/manual |
| OpenClaw gate | IDE / ChatGPT → openclaw_config | gateway_openclaw | manual |
| CI validation | PR push → GHA | tests / validators | git event |
| AI workers | ChatGPT GO_PROMPT → run_task.sh | git / PR | manual |
| Fleet health | runtime_health → cursor-ai, fantome | Telegram | schedule |

### Ce qui N'est PAS dans le scope

- Logique trading (signals, stratégies, risk sizing)
- Base de données perf (schema, migrations)
- UI Desk Pro (layout, CSS)
- Contenu des registres stratégie

## Méthode d'inventaire

Pour chaque surface :
1. lister les fichiers d'entrée et de sortie ;
2. identifier les consommateurs (imports, exec, curl) ;
3. identifier les déclencheurs (webhook, schedule, manual, PR) ;
4. identifier les artefacts produits (jsonl, db, logs, markdown) ;
5. noter les points de contrôle humain.

## Livrable child GO

```text
GO_AUTOMATION_OPS_OPT_TRADING_CHILD_ARCHITECTURE_MAP_01
→ ARCHITECTURE_AUTOMATION_MAP.md
```

## Contraintes

- Cartographie uniquement — aucune mutation.
- Pas de suppression de surface avant registre des jobs.
- Préserver les chemins existants (docs/ARCHITECTURE.md, docs/RUNBOOK.md) comme référence.
