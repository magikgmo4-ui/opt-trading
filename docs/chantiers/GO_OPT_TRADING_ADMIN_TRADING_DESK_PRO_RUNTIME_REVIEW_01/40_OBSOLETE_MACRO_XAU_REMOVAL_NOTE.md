---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_RUNTIME_REVIEW_01_MACRO_XAU
doc_type: obsolete_removal_note
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_RUNTIME_REVIEW_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-04
---

# 40_OBSOLETE_MACRO_XAU_REMOVAL_NOTE

## Decision

**macro-xau est OBSOLETE / A RETIRER.**

## Preuve

- `/opt/trading/jobs/macro_xau/run.sh` ABSENT sur la machine
- `/opt/trading/jobs/macro_xau/macro_xau.py` ABSENT sur la machine
- Le module existe uniquement dans `_worktrees/sot-build/jobs/macro_xau/` (archive de build)
- `macro-xau.service` FAILED: "Failed at step EXEC spawning ... No such file or directory"
- `macro-xau.timer` ACTIF: relance toutes les 30 minutes, echec systematique

## Impact actuel

- **Timer actif mais inutile**: genere des echecs toutes les 30 minutes dans les logs
- **Aucun impact fonctionnel**: le service echoue silencieusement (exit code 203/EXEC)
- **Pollution logs**: chaque echec est loggue dans journalctl
- **Pas de cout CPU significatif**: le process meurt immediatement

## Recommandation

1. **Desactiver le timer**: `sudo systemctl disable --now macro-xau.timer`
2. **Desactiver le service**: `sudo systemctl disable macro-xau.service`
3. **Ne pas supprimer les fichiers** systemd sans GO dedie de cleanup
4. **Ne pas reconstruire** le module macro-xau
5. **Ne pas restaurer** jobs/macro_xau/run.sh

## Regles

- Ne pas reconstruire macro-xau
- Ne pas restaurer jobs/macro_xau/run.sh
- Ne pas creer de GO de restauration macro-xau
- Le cleanup systemd (disable timer/service) peut etre fait dans un GO de triage services
