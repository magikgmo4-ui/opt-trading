---
doc_id: GO_STRATEGY_SMC_ICT_CHILD_OBS_EVENT_AUTOMATION_01_INITIAL
doc_type: initial_project_doc
go_id: GO_STRATEGY_SMC_ICT_CHILD_OBS_EVENT_AUTOMATION_01
parent_go: GO_STRATEGY_SMC_ICT_CHILD_LIVE_OBSERVATION_01
status: CLOSED
created_at: 2026-05-30
---

# GO_STRATEGY_SMC_ICT_CHILD_OBS_EVENT_AUTOMATION_01

## 1_CONTEXTE

Gap G02 du GO parent `GO_STRATEGY_SMC_ICT_CHILD_LIVE_OBSERVATION_01` :

> Le posting des ObservationEvents est manuel. Il n'existe pas de pipeline
> qui lit automatiquement un screenshot bot_vision et produit un ObservationEvent
> SMC_ICT.

Sans ObsEvents postés, la promotion gate (`sample_size >= 30`) ne peut pas être
atteinte avant la fenêtre paper close (2026-06-13).

## 2_OBJECTIF

Créer `modules/smc_ict_obs_processor/` — module standalone qui :

1. `score_confidence(detail)` — formule `60_SCORING_INITIAL.md` (max 1.0)
2. `build_obs_event(...)` — construit et valide l'ObsEvent complet
3. `from_summary_json(path, ...)` — pont semi-auto vers bot_vision_step2 outputs
4. `post_obs_event(event, base_url)` — POST vers `/perf/observation_event`
5. CLI `post` + `from-summary`

## 3_PÉRIMÈTRE

In scope : `modules/smc_ict_obs_processor/`, tests, scripts 4x

Out of scope : intégration LLM automatique (Phase 2), Telegram watch signal

## 4_LIVRABLES

| Fichier | Rôle |
|---------|------|
| `modules/smc_ict_obs_processor/app/smc_ict_obs_processor.py` | Core logic |
| `modules/smc_ict_obs_processor/scripts/cmd.sh` | CLI entry point |
| `modules/smc_ict_obs_processor/scripts/menu.sh` | Interactive menu |
| `modules/smc_ict_obs_processor/scripts/sanity_check.sh` | Sanity check |
| `modules/smc_ict_obs_processor/scripts/install_shortcuts.sh` | Install wrappers |
| `tests/test_smc_ict_obs_processor.py` | 17 tests |
