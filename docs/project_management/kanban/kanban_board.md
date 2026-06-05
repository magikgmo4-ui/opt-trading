# Kanban Projet

## Board

| ID | Epic | Tache | Priorite | Statut | Responsable | Debut prevu | Echeance | Effort | Valeur | Risque | Dependances | Critere de fini | Avancement % | References principales | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---:|---|---|
| K-001 | Exploitation | Cartographier l'architecture `/opt/trading` | Haute | Termine | IA + Toi | Fait | Fait | M | Haute | Faible |  | Arborescence, services, scripts et roles identifies | 100 | `/opt/trading/docs/ARCHITECTURE.md`, `/home/student/infra-context-run/snapshot/snapshot_2026-02-26T15-09-46-05-00.txt` | Base de reference etablie |
| K-002 | Exploitation | Identifier les modules actifs et leurs raccourcis | Haute | Termine | IA + Toi | Fait | Fait | M | Haute | Faible | K-001 | Matrice modules -> scripts -> services -> liens produite | 100 | `/opt/trading/modules/deepseek_hub/scripts/install_shortcuts.sh`, `/home/student/menu_audit_student_20260303_182326.log`, `/home/student/shortcut_targets_student_20260303_182326.log` | `student`, `fail2ban`, `deepseek_*` recenses |
| K-003 | Maintenance | Diagnostiquer les liens casses `student` | Haute | Termine | IA + Toi | Fait | Fait | S | Haute | Moyen | K-002 | Cause racine documentee | 100 | `/home/student/shortcut_targets_student_20260303_182326.log`, `/home/student/ref_student/23_repo_file_list.txt` | Conflit entre ancien schema et alias hub |
| K-004 | Maintenance | Sauvegarder l'etat des raccourcis avant correction | Haute | Termine | IA + Toi | Fait | Fait | S | Haute | Faible | K-003 | Backup present et consultable | 100 | `/home/student/tmp/student_shortcut_backup_20260318_182149`, `/home/student/tmp/repair_student_shortcuts.sh` | Backup avant/apres disponible |
| K-005 | Maintenance | Reparer `menu-student`, `cmd-student`, `sanity-student` | Haute | Termine | IA + Toi | Fait | Fait | S | Haute | Moyen | K-004 | Liens recrees et cibles valides | 100 | `/home/student/tmp/repair_student_shortcuts.sh`, `/opt/trading/modules/deepseek_hub/scripts/install_shortcuts.sh` | Pointe maintenant vers `deepseek_hub` |
| K-006 | Qualite | Verifier fonctionnellement `sanity-student` | Haute | Termine | IA + Toi | Fait | Fait | S | Haute | Faible | K-005 | `PASS` obtenu | 100 | `/opt/trading/modules/deepseek_hub/scripts/sanity_check_deepseek_hub.sh` | Verification OK |
| K-007 | Qualite | Verifier `cmd-student` en usage reel | Haute | A faire | Toi + IA | Prochainement | 24h | S | Haute | Moyen | K-005 | Une commande reelle s'execute sans erreur | 0 | `/opt/trading/modules/deepseek_hub/scripts/deepseek_hub_cmd.sh` | Exemple: `cmd-student status` |
| K-008 | Qualite | Verifier `menu-student` en usage reel | Moyenne | A faire | Toi + IA | Prochainement | 24h | S | Moyenne | Faible | K-005 | Le menu s'ouvre et les options principales repondent | 0 | `/opt/trading/modules/deepseek_hub/scripts/deepseek_hub_menu.sh` | Test interactif a faire |
| K-009 | Architecture | Confirmer que l'alias `student` doit viser `deepseek_hub` | Haute | A valider | Toi | Prochainement | 48h | S | Haute | Haute | K-005 | Decision explicite prise | 75 | `/opt/trading/modules/deepseek_hub/scripts/install_shortcuts.sh`, `/opt/trading/docs/student_deepseek_runbook.md` | Techniquement coherent, validation produit utile |
| K-010 | Architecture | Documenter la convention officielle des raccourcis globaux | Haute | A faire | IA + Toi | Cette semaine | Cette semaine | M | Haute | Moyen | K-009 | Regle simple ecrite et partageable | 0 | `/opt/trading/docs/project_management/kanban/kanban_references.md`, `/opt/trading/modules/deepseek_hub/scripts/install_shortcuts.sh` | Eviter nouvelles derives |
| K-011 | Architecture | Eliminer l'ambiguite entre anciens scripts `student_*` et nouveaux alias | Haute | A analyser | IA + Toi | Cette semaine | Cette semaine | M | Haute | Moyen | K-009 | Un seul schema cible retenu | 10 | `/home/student/ref_student/23_repo_file_list.txt`, `/home/student/shortcut_targets_student_20260303_182326.log` | Dette technique encore presente |
| K-012 | Securite | Revoir l'etat reel de `fail2ban` | Haute | A faire | IA + Toi | Cette semaine | Cette semaine | M | Haute | Moyen |  | Sanity + status + bans verifies | 0 | `/home/student/fail2ban_module_v1/install.sh`, `/home/student/fail2ban_module_v1/scripts/fail2ban_sanity_check.sh`, `/home/student/ref_student/10_systemd_enabled.txt` | Wrappers OK, runtime a verifier |
| K-013 | Securite | Verifier la politique UFW actuelle | Moyenne | A analyser | IA + Toi | Cette semaine | Cette semaine | M | Moyenne | Moyen |  | Etat explique et documente | 0 | `/home/student/ref_student/10_systemd_enabled.txt`, `/home/student/ref_student/11_dpkg_list.txt`, `/home/student/infra-context-run/snapshot/snapshot_2026-02-26T15-09-46-05-00.txt` | Exports historiques contradictoires |
| K-014 | Sauvegarde | Tester le workflow backup USB complet | Haute | A faire | IA + Toi | Cette semaine | Cette semaine | M | Haute | Moyen |  | Detect, backup, verify reussis | 0 | `/home/student/student_pack_v2/scripts/usb_detect_mount.sh`, `/home/student/student_pack_v2/scripts/usb_backup_student.sh`, `/home/student/student_pack_v2/scripts/usb_verify_backup.sh` | Important pour resilience ops |
| K-015 | Documentation | Produire une fiche d'exploitation `student/deepseek_hub` | Moyenne | A faire | IA | Cette semaine | Cette semaine | M | Haute | Faible | K-009 | Doc courte, actionnable, validee | 0 | `/opt/trading/docs/student_deepseek_quick_reference.md`, `/opt/trading/docs/student_deepseek_runbook.md` | Pour onboarding et runbook |
| K-016 | Pilotage | Construire un tableau de bord de progression hebdo | Moyenne | En cours | IA + Toi | Aujourd'hui | Cette semaine | S | Moyenne | Faible | K-010 | Vue synthese maintenue chaque semaine | 25 | `/opt/trading/docs/project_management/kanban/kanban_board.md` | Ce board est la base |
| K-017 | Architecture | Officialiser `/opt/trading/student` comme racine canonique | Haute | Termine | IA + Toi | Fait | Fait | S | Haute | Faible | K-009 | Racine, facades et raccourcis globaux alignes | 100 | `/opt/trading/student/README.md`, `/opt/trading/student/docs/ARCHITECTURE.md`, `/opt/trading/student/bin/repair_shortcuts.sh` | Basculé et validé |

## Colonnes Kanban

| A faire | A analyser | En cours | A valider | Bloque | Termine |
|---|---|---|---|---|---|
| Non lance | Besoin de cadrage | Travail actif | Decision/validation | Attente externe | Fait et teste |

## Vue synthese

| Epic | Nb taches | A faire | En cours | A valider | Bloque | Termine | Avancement global |
|---|---:|---:|---:|---:|---:|---:|---:|
| Exploitation | 2 | 0 | 0 | 0 | 0 | 2 | 100% |
| Maintenance | 3 | 0 | 0 | 0 | 0 | 3 | 100% |
| Qualite | 3 | 2 | 0 | 0 | 0 | 1 | 33% |
| Architecture | 3 | 1 | 0 | 1 | 0 | 0 | 28% |
| Securite | 2 | 1 | 0 | 0 | 0 | 0 | 5% |
| Sauvegarde | 1 | 1 | 0 | 0 | 0 | 0 | 0% |
| Documentation | 1 | 1 | 0 | 0 | 0 | 0 | 0% |
| Pilotage | 1 | 0 | 1 | 0 | 0 | 0 | 25% |
| Consolidation Student | 1 | 0 | 0 | 0 | 0 | 1 | 100% |

## Top priorites recommandees

1. `K-007` verifier `cmd-student` en reel
2. `K-009` valider fonctionnellement que `student = deepseek_hub`
3. `K-012` verifier `fail2ban`
4. `K-014` tester backup USB
5. `K-010` figer une convention officielle des raccourcis

## RISKS

- À qualifier.
