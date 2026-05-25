---
doc_id: GO_OPENCLAW_OPT_TRADING_TMUX_RUNTIME_SPINE_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
go_id: GO_OPENCLAW_OPT_TRADING_TMUX_RUNTIME_SPINE_01
go_structural_role: GO_INDEPENDENT
parent_go: ""
master_project_plan_id: ""
pf_id: PF_OPENCLAW_ORCHESTRATOR_FULL
status: open
lifecycle_stage: opening
surface: scripts/tmux/
source_kind: canonical
updated_at: 2026-05-25
topic_keys:
  - tmux
  - runtime
  - sessions
  - healthcheck
  - restart-policy
links:
  - docs/chantiers/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_SYSTEM_MASTER_PLAN_01/09_TMUX_RUNTIME_SPINE_PLAN.md
---

# 00_INITIAL_PROJECT_DOC — TMUX Runtime Spine

## 1_MASTER_TARGET

Implémenter la colonne vertébrale TMUX runtime — sessions canoniques, panes nommés par worker, logs standardisés, healthchecks, restart policies. Standardiser TOUS les process long-running dans TMUX.

## 2_INITIAL_PROJECT_DOC

Ce GO ouvre `GO_OPENCLAW_OPT_TRADING_TMUX_RUNTIME_SPINE_01` — premier GO après fermeture de `PF_OPENCLAW_ORCHESTRATOR_FULL`.

```text
PF_OPENCLAW_ORCHESTRATOR_FULL = PASS
GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01 = CLOSED
NEXT_GO = TMUX Runtime Spine
```

## 3_INITIAL_NEED

La chaîne produit est complète (signal_router → learning_feeder), mais l'exploitation runtime est encore ad-hoc : process lancés manuellement, pas de supervision standardisée, logs dispersés, restart policies non documentées. TMUX résout tout ça.

## 4_SCOPE

```text
scripts/tmux/
├── start_all.sh              → démarrer toutes sessions (ordre: openclaw-core first)
├── stop_all.sh               → arrêter toutes sessions (ordre inverse)
├── restart_session.sh        → restart une session par nom
├── health_aggregator.sh      → vérifier toutes sessions
├── attach.sh                 → attacher à une session nommée
├── sanity.sh                 → validation module
└── sessions/
    ├── openclaw-core.sh      → gateway + bridge + health + logs
    ├── screeners.sh          → tradingview + webhook + bot_vision + telegram
    ├── strict-workers.sh     → signal → proposition → validation → trade → result → datasheet → learning
    ├── trading-pipeline.sh   → kil_v1 + simex + execution + risk + position
    ├── market-data.sh        → collectors + analyzers + scanner + hub
    ├── apps-connectors.sh    → airtable + clickup + sheets
    ├── desk-pro.sh           → desk_pro + perf + orchestrator
    ├── kg-repo.sh            → memory_bricks + learning_feeder
    └── localcms-ui.sh        → localcms consumer
```

## 5_KEY_DECISIONS

- `trade_executor` : pas de restart automatique (safety — éviter double trade)
- `kil_v1` : pas de restart automatique (kill switch = safety device)
- Engines stateful : restart manuel uniquement
- Toutes sessions TMUX avec panes nommés
- Logs redirigés vers fichier par session/pane
- Sessions critiques : `openclaw-core`, `screeners`, `strict-workers`

## 6_INVARIANTS

```text
NO_LIVE_TRADE_WITHOUT_GATE = true
NO_DOUBLE_TRADE_RESTART = true
NO_SECRET_IN_LOGS = true
NO_MANUAL_AD_HOC_LONG_RUNNING_PROCESS = true
```

## 7_ESTABLISHED

- Base : `09_TMUX_RUNTIME_SPINE_PLAN.md` (364 lignes)
- TMUX disponible sur db-layer + admin-trading
- gateway_openclaw opérationnel

## 8_TODO

1. Créer les 9 scripts de session
2. Créer start_all.sh, stop_all.sh, restart_session.sh, health_aggregator.sh, attach.sh
3. Créer sanity.sh
4. Vérifier syntaxe bash (shellcheck compatible)
5. Produire .patch canonique
6. Ouvrir PR
