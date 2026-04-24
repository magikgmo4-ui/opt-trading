# audit

Module de methode et de wrappers pour conduire un audit structure du repo, distinct du dossier racine `audit/`.

## Role
- cadrer une methode d'audit stricte en plusieurs passes
- exposer des checklists et guides de thinking pour l'analyse
- fournir les wrappers standard `cmd/menu/sanity` pour la surface module

## Contenu
- `docs/AUDIT_STRICT_CHECKLIST.md` : checklist obligatoire en trois passes
- `docs/AUDIT_THINKING_GUIDE.md` : guide d'observations libres et de priorisation
- `scripts/cmd.sh` : commandes generiques `info`, `readme`, `ls`, `grep`, `menu`
- `scripts/menu.sh`, `scripts/install_shortcuts.sh`, `scripts/sanity_check.sh`

## Integration
- complete le dossier racine `audit/`, qui stocke les preuves et packs dates
- ne doit pas etre confondu avec la surface top-level de preuves :
  - `modules/audit` = methode / wrapper
  - `audit/` = artefacts, packs, sorties et historique

## Statut
- actif
- module de methode et d'outillage, pas depot de preuves

## Notes de consolidation
- a garder distinct du dossier racine `audit/`
- a traiter dans les conventions `repo / tooling / authoring`, pas comme surface produit
