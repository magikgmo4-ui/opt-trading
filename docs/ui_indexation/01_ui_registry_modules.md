# UI Registry — Modules

## Candidats UI / surfaces déjà visibles

### Operator-facing probable
- `modules/ops_menu_hub` — hub opérateur MSI validé
- `modules/desk_pro_dashboard` — surface dashboard opérateur / statut / rendu
- `modules/desk_pro_runner` — exécution principale
- `modules/desk_capture_inputs` — saisie opérateur
- `modules/desk_analyze` — analyse à la demande
- `modules/perf` — monitoring/perf côté opérateur ou semi-technique
- `modules/vision_bot` — vision / screenshots / analyse assistée
- `modules/bot_vision` / `bot_vision_step2` — pipeline capture → analyse → artefacts

### Semi-operator / backend-visible
- `modules/desk_state`
- `modules/desk_snapshot_ingest`
- `modules/desk_retention`
- `modules/desk_pro_orchestrator`
- `modules/desk_pro`

### Analysis / probability / trades
- `modules/derivatives_analyzer`
- `modules/probability_engine`
- `modules/decision_engine`
- `modules/risk_engine`
- `modules/market_scanner`
- `modules/liquidation_analyzer`
- `modules/portfolio_engine`
- `modules/position_engine`

### Dev / debug / admin
- `modules/ops_super_menu`
- `modules/ops_wrappers`
- `modules/perf_engine`
- `modules/journal_engine`
- `modules/marketdata`
- `modules/desk_common`

## Lecture initiale
- Le vrai point d’entrée UI opérateur existe déjà : `ops_menu_hub`.
- `desk_pro_dashboard` semble être la meilleure candidate pour une UI de synthèse utilisateur.
- `perf` semble être une surface existante mais encore plus wrapper/générique que vraiment “MSI-friendly”.
- Les moteurs probability/trades sont prêts à être **indexés visuellement** avant d’être transformés en UI dédiées.

## RISKS

- À qualifier.
