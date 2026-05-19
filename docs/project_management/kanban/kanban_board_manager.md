# Board Manager

## Parametres

- Repo folder: `/opt/trading/docs/project_management/kanban`
- Working branch: `docs/kanban-pilotage-20260318`
- Horizon: immediate ops stabilization + architecture cleanup

## Vue ultra concise

| ID | Tache | Statut | Priorite | Prochaine action | Reference cle |
|---|---|---|---|---|---|
| K-007 | Verifier `cmd-student` en reel | A faire | Haute | Lancer `cmd-student status` | `/opt/trading/modules/deepseek_hub/scripts/deepseek_hub_cmd.sh` |
| K-008 | Verifier `menu-student` en reel | A faire | Moyenne | Ouvrir le menu et tester les options 1-3 | `/opt/trading/modules/deepseek_hub/scripts/deepseek_hub_menu.sh` |
| K-009 | Valider l'alias `student` -> `deepseek_hub` | A valider | Haute | Confirmer la decision produit | `/opt/trading/modules/deepseek_hub/scripts/install_shortcuts.sh` |
| K-010 | Documenter la convention des raccourcis | A faire | Haute | Ecrire la regle officielle | `/opt/trading/docs/project_management/kanban/kanban_references.md` |
| K-011 | Supprimer l'ambiguite des anciens scripts `student_*` | A analyser | Haute | Choisir schema cible unique | `/home/student/ref_student/23_repo_file_list.txt` |
| K-012 | Verifier `fail2ban` | A faire | Haute | Lancer sanity + status + bans | `/home/student/fail2ban_module_v1/scripts/fail2ban_sanity_check.sh` |
| K-013 | Clarifier UFW | A analyser | Moyenne | Comparer etat courant vs exports | `/home/student/ref_student/10_systemd_enabled.txt` |
| K-014 | Tester backup USB | A faire | Haute | Enchainer detect -> backup -> verify | `/home/student/student_pack_v2/scripts/usb_backup_student.sh` |
| K-015 | Produire la fiche d'exploitation | A faire | Moyenne | Ecrire quick reference | `/opt/trading/docs/student_deepseek_quick_reference.md` |
| K-016 | Tenir le tableau de bord hebdo | En cours | Moyenne | Mettre a jour chaque semaine | `/opt/trading/docs/project_management/kanban/kanban_board.md` |

## Decision log minimal

| Sujet | Etat | Decision attendue |
|---|---|---|
| Alias global `student` | A valider | Conserver `deepseek_hub` comme cible officielle ou revenir a un alias legacy |
| Convention des scripts | A analyser | Garder un seul schema de chemins pour eviter les liens casses |
| UFW | A analyser | Confirmer l'etat reel et la politique cible |
