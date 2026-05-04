---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_RUNTIME_REVIEW_01_STATE
doc_type: desk_pro_state
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_RUNTIME_REVIEW_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-04
---

# 10_DESK_PRO_STATE — Etat Desk Pro

## Stack Desk Pro

### Modules presents sur admin-trading

| Module | Role | Statut |
| --- | --- | --- |
| modules/desk_pro | Librairie core (API/Models/UI/Mount) | STRUCTURE |
| modules/desk_pro_runner | Orchestrateur principal (CLI) | ACTIF |
| modules/desk_pro_orchestrator | Pipeline d'execution | ACTIF |
| modules/desk_pro_dashboard | Visualisation / Export | ACTIF |
| modules/desk_analyze | Analyse a la demande | PRET |
| modules/desk_capture_inputs | Saisie manuelle signaux | PRET |
| modules/desk_snapshot_ingest | Ingestion snapshots | PRET |
| modules/desk_retention | Retention donnees | PRET |
| modules/desk_state | Vue etat desk | PRET |
| modules/desk_common | Logique partagee | PRET |
| modules/bot_vision/bot_vision_step1/desk_pro_vision | Generateur visuel placeholder | LEGACY |

### Entrypoints

| Entrypoint | Type | Localisation |
| --- | --- | --- |
| scripts/admin_trading/desk_pro_cmd.sh | ADMIN (canonique) | Scripts admin |
| scripts/desk_pro_cmd.sh | LEGACY (racine) | Scripts racine |
| scripts/desk_pro_root_cmd.sh | GENERIQUE | Scripts racine |
| cmd-desk_pro_runner | WRAPPER | /usr/local/bin |
| cmd-desk_pro_dashboard | WRAPPER | /usr/local/bin |
| menu-ops_menu_hub | HUB | /usr/local/bin |

### Runner status (2026-05-04)

```json
{
  "runner_status": "OK",
  "mode": "PAPER",
  "orchestrator_available": true,
  "dashboard_available": true,
  "latest_run_available": true,
  "latest_run_id": "desk_run_20260405_010912",
  "summary": "Desk Pro runner ready."
}
```

- Runner operationnel en mode PAPER (pas de trading reel)
- Orchestrator et dashboard disponibles
- Dernier run reference correctement

## Donnees historiques

### Runs

- 38 runs dans data/desk_runs/ (6 mars — 5 avril 2026)
- Dernier run: desk_run_20260405_010912 (SUCCESS, 11 OK / 0 Failed)
- Tous les runs documentes sont SUCCESS
- Session journal: 5 entrees (mars-avril 2026)

### Outputs /shared/desk_pro/latest/

| Fichier | Taille | Date |
| --- | --- | --- |
| dashboard_latest.html | 3166 B | 4 avr 21:08 |
| journal_engine.json | 1172 B | 4 avr 21:08 |
| perf_engine.json | 1040 B | 4 avr 21:08 |
| portfolio_engine.json | 1168 B | 4 avr 21:08 |
| run_summary.json | 2195 B | 4 avr 21:08 |

## Classification

- **Desk Pro core** (runner + orchestrator + dashboard): OPERATIONNEL
- **Desk Pro peripheriques** (analyze, capture, snapshot, retention, state): PRET mais non teste recemment
- **Derniere execution**: 2026-04-05 (~1 mois) — SUCCESS
- **Mode**: PAPER (simulation, pas de trading reel)
- **Fracheur des donnees**: STALE (1 mois)
