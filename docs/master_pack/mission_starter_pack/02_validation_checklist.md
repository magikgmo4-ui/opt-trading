# CHECKLIST DE VALIDATION DE FIN DE MISSION

Avant de clore une mission, vérifier :

## 1. SÉCURITÉ RUNTIME
- [ ] Aucun script de production (`scripts/student/`, `scripts/admin_trading/`) n'a été cassé ou supprimé par erreur ?
- [ ] Aucun wrapper global (`/usr/local/bin`) n'a été modifié sans validation ?
- [ ] Les permissions d'exécution (`chmod +x`) sont-elles préservées ?

## 2. COHÉRENCE DOCUMENTAIRE
- [ ] Le `docs/master_pack/00_current_state_and_standards.md` est-il toujours à jour avec la réalité ?
- [ ] Si une exception runtime a été découverte, est-elle ajoutée à la matrice des exceptions ?
- [ ] Si un nouvel entrypoint est créé, est-il documenté ?
- [ ] La doc canonique touchée par la mission a-t-elle été mise à jour ?
- [ ] Le kanban source of truth est-il mis à jour (statut + point de reprise) ?

## 3. PROPRETÉ
- [ ] Pas de fichiers temporaires (`tmp_`, `test_`) laissés à la racine ?
- [ ] Les rapports de mission sont-ils bien nommés et complets ?
- [ ] Le statut final est-il clair (PASS, PARTIAL, FAIL) ?

## RISKS

- À qualifier.
