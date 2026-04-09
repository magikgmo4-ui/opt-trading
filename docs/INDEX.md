# INDEX — Documentation Magikgmo

- **docs/ROADMAP.md** : roadmap annotée + critères Done
- **docs/simex/SIMEX_PRESETS.md** : presets opérateur (SIMEX_* env) + commandes Bitget→Perf
- **docs/ot/kanban/opt_trading_kanban_source_of_truth.md** : kanban (source of truth) + points de reprise
- **docs/ot/trading/00_TRADING_DUAL_STACK_LAB_REALTIME_V1.md** : cadrage canonique dual Lab + Real-Time V1, analyse multi-rôles, garde-fous, et trigger `GO_OT_TRADING_DUAL_STACK_V1_01`
- **docs/master_pack/mission_starter_pack/00_mission_start_guide.md** : point d’entrée unique (ouverture de session)
- **docs/ot/trae/08_MULTI_STEP_MISSION_CHECKLIST_V1.txt** : modèle officiel missions longues / multi-étapes
- **docs/ARCHITECTURE.md** : architecture (flux, persistance, composants)
- **docs/API.md** : endpoints + exemples `curl`
- **docs/RUNBOOK.md** : ops/debug (systemd, logs, réseau Windows/LAN)
- **docs/SCHEMAS.md** : schéma unique Event → Trade → Perf + adaptateur
- **docs/deploy_module_multi_machine_continuity.md** : continuité de déploiement multi-machine, modules validés, prochain candidat
- **docs/ops_wrappers_source_layout_refresh_runbook.md** : runbook de refresh source-layout pour `ops_wrappers`
- **schemas/webhook_event_v1.json** : JSON Schema v1 (source de vérité)

## Code — repères
- `webhook_server.py` : webhook `/tv` + UI `/dash` + persistance JSONL
- `perf/perf_app.py` : API perf + SQLite + UI `/perf/ui`
- `adapters/webhook_to_perf.py` : mapping webhook → perf_event
- `shared/telegram_notify.py` : notifications Telegram
- `tools/journal_from_paste.py` : génération d’entrées `journal.md`
