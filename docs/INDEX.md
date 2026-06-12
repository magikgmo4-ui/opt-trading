# INDEX — Documentation Magikgmo

- **docs/ROADMAP.md** : roadmap annotée + critères Done
- **docs/simex/SIMEX_PRESETS.md** : presets opérateur (SIMEX_* env) + commandes Bitget→Perf
- **docs/simex/SIMEX_UNITS_CONTRACT.md** : contrat canonique des unités SimEx (`SIMEX_UNITS_V1`) + compat legacy
- **docs/ot/kanban/opt_trading_kanban_source_of_truth.md** : kanban (source of truth) + points de reprise
- **docs/ot/trading/00_TRADING_DUAL_STACK_LAB_REALTIME_V1.md** : cadrage canonique dual Lab + Real-Time V1, analyse multi-rôles, garde-fous, et trigger `GO_OT_TRADING_DUAL_STACK_V1_01`
- **docs/master_pack/mission_starter_pack/00_mission_start_guide.md** : point d’entrée unique (ouverture de session)
- **docs/governance/CHATGPT_PROFILE_BASELINE_2026_04_19.md** : baseline datée des custom instructions et de la mémoire sauvegardée retenues pour la continuité ChatGPT
- **docs/ot/trae/08_MULTI_STEP_MISSION_CHECKLIST_V1.txt** : modèle officiel missions longues / multi-étapes
- **docs/ARCHITECTURE.md** : architecture (flux, persistance, composants)
- **docs/architecture/REPO_SURFACES_MAP.md** : carte humaine des surfaces top-level (référence ; `registry/*` reste machine-readable)
- **docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md** : matrice maître canonique souveraine (produit, parent/sous-GO, support Git, propagation, placement)
- **docs/governance/MATRICE_DOC_OPS_MASTER_PLAN_01.md** : plan historique rattaché à la matrice maître
- **docs/governance/MATRICE_GOUVERNANTE_V2.md** : annexe stable secondaire relue sous la matrice maître
- **docs/governance/MATRICE_GOUVERNANTE_METADATA_DERIVATION_01.md** : doctrine légère de dérivation contrôlée pour frontmatter enrichi, `search_tags`, groupes d’objets et registry dérivé
- **docs/governance/PRODUCT_CONTINUITY_HIERARCHY_01.md** : annexe stable de continuité produit relue sous la matrice maître
- **docs/governance/REPO_ROOT_POLICY.md** : politique racine canonique interne du repo
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

## RISKS

- À qualifier.
