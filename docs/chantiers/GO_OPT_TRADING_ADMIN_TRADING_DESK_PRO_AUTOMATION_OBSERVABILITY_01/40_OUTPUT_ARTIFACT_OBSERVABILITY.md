---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_OBSERVABILITY_01_OUTPUTS
doc_type: output_artifact_observability
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_OBSERVABILITY_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-09
---

# 40_OUTPUT_ARTIFACT_OBSERVABILITY - Output Artifact Observability

## Passive artifact scan

Les scans autorises ont retourne des artefacts existants lies a Desk Pro et a d'autres surfaces documentaires, sans preuve d'un nouvel artefact genere par `desk_pro_dry_run.timer`.

## Observations utiles

- `/opt/trading/data/logs/desk_pro/latest_run_id.txt`
- `/opt/trading/data/logs/desk_pro/latest_status.txt`
- `/opt/trading/data/desk_runs/.../run_summary.json`
- `/srv/sftp/shared_files/shared/desk_pro/latest/run_summary.json`
- `/srv/sftp/shared_files/shared/desk_pro/latest/journal_engine.json`
- `/srv/sftp/shared_files/shared/desk_pro/latest/perf_engine.json`
- `/srv/sftp/shared_files/shared/desk_pro/latest/portfolio_engine.json`

## Limits

- le filtre autorise est large et remonte aussi des fichiers historiques non relies a ce timer
- aucun nom d'artefact specifique au dry-run timer n'est visible naturellement
- aucun artefact ne peut etre attribue avec certitude a `desk_pro_dry_run.service` sans execution naturelle ulterieure

## Conclusion

La surface d'observabilite fichier existe deja, mais l'attribution au timer dry-run reste a confirmer apres un futur declenchement observe passivement ou dans un GO de start gate.

## RISKS

- À qualifier.
