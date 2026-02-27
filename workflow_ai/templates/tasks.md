# tasks.md — Plan atomique (checklist)

> Règle: 1 case = 1 livrable vérifiable (fichiers + commandes + critères)

## Backlog
- [ ] Gate 0: cadrage (objectif/contraintes/DONE/risques)
- [ ] Gate 1: créer/mettre à jour la source de vérité
- [ ] Gate 2: plan petits pas
- [ ] Gate 3: backup avant changement
- [ ] Gate 4: incrément 1 (MVP)
- [ ] Gate 5: tests + sanity + rollback
- [ ] Gate 6: update docs + changelog

## Détails (exemple)
- [ ] Créer endpoint POST /desk/snapshot
  - Fichiers: modules/desk_pro/api/routes.py
  - Commandes: curl ... (200 attendu)
  - Critères succès: snapshot persisté
  - Rollback: git checkout -- <files> / apply patch inverse
