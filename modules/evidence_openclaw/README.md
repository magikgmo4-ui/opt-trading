# evidence_openclaw

Module de capture de preuves OpenClaw et de generation d'un prompt documentaire fonde sur ces preuves.

## Role
- detecter le workspace du default agent
- exporter des fichiers de preuve dans ce workspace
- generer un prompt strict pour la documentation OpenClaw a partir de ces preuves

## Contenu
- `scripts/cmd.sh` : `detect-workspace`, `status`, `export-docs`, `print-doc-prompt`, `evidence-dir`, `show-files`
- `scripts/menu.sh`, `sanity.sh`, `install_shortcuts.sh`
- `docs/README.md`, `RUNBOOK.txt`, `ETABLI.txt`, `GO_OPENCLAW_*.md`

## Preuves exportees
- `01_doctor_status.txt`
- `02_configure_status.txt`
- `03_doctor_quick.txt`
- `04_workspace_context.txt`
- `90_PROMPT_DOCS.txt`

## Integration
- depend de `doctor_openclaw` et `configure_openclaw` si leurs wrappers sont disponibles
- ecrit dans `docs_evidence/openclaw_current_state` du workspace OpenClaw detecte

## Statut
- actif
- module de preuve et de continuité documentaire

## Notes de consolidation
- ne pas melanger ce module avec les modules runtime du gateway
- sa valeur est dans la preuve exportee et le prompt documentaire, pas dans le pilotage runtime
