# References Utilisees Pour Le Kanban

## Parametres de travail

- Repo principal utilise: `/opt/trading`
- Branche de travail creee pour cette documentation: `docs/kanban-pilotage-20260318`
- Dossier fixe pour les exports et la planification: `/opt/trading/student/exports/kanban`

## Sources principales internes au repo

| Reference | Utilisation dans le Kanban |
|---|---|
| `/opt/trading/student/bin/install_shortcuts.sh` | Reference canonique pour l'installation des raccourcis globaux |
| `/opt/trading/student/scripts/deepseek_hub/deepseek_hub_cmd.sh` | Base canonique de la carte `K-007` |
| `/opt/trading/student/scripts/deepseek_hub/deepseek_hub_menu.sh` | Base canonique de la carte `K-008` |
| `/opt/trading/student/scripts/deepseek_hub/sanity_check_deepseek_hub.sh` | Base canonique de la verification `K-006` |
| `/opt/trading/docs/ARCHITECTURE.md` | Support de la cartographie globale `K-001` |
| `/opt/trading/docs/student_deepseek_quick_reference.md` | Support documentaire de `K-015` |
| `/opt/trading/student/docs/RUNBOOK.md` | Support documentaire canonique de `K-009` et `K-015` |

## Sources externes au repo utilisees comme preuves d'etat

| Reference | Utilisation dans le Kanban |
|---|---|
| `/home/student/menu_audit_student_20260303_182326.log` | Inventaire des commandes `menu-*`, `cmd-*`, `sanity-*` |
| `/home/student/shortcut_targets_student_20260303_182326.log` | Preuve des liens `student` casses et de l'etat des wrappers |
| `/home/student/ref_student/23_repo_file_list.txt` | Preuve de coexistence des scripts top-level et `scripts/student/` |
| `/home/student/ref_student/10_systemd_enabled.txt` | Base des cartes services / securite / UFW |
| `/home/student/ref_student/11_dpkg_list.txt` | Verification de la presence des paquets ops et securite |
| `/home/student/infra-context-run/snapshot/snapshot_2026-02-26T15-09-46-05-00.txt` | Photo machine de reference, services actifs, liens valides au 26/02 |
| `/home/student/fail2ban_module_v1/install.sh` | Reference d'installation de `fail2ban` |
| `/home/student/fail2ban_module_v1/scripts/fail2ban_sanity_check.sh` | Base de la carte `K-012` |
| `/home/student/student_pack_v2/scripts/usb_detect_mount.sh` | Base de la carte `K-014` |
| `/home/student/student_pack_v2/scripts/usb_backup_student.sh` | Base de la carte `K-014` |
| `/home/student/student_pack_v2/scripts/usb_verify_backup.sh` | Base de la carte `K-014` |
| `/home/student/tmp/repair_student_shortcuts.sh` | Preuve du correctif applique et de la logique de backup/reparation |
| `/home/student/tmp/student_shortcut_backup_20260318_182149` | Preuve du backup avant/apres correction |

## Documents cites plus haut dans les echanges et retenus dans le board

| Document | Role |
|---|---|
| `/opt/trading/docs/ARCHITECTURE.md` | Vue d'ensemble de l'architecture |
| `/opt/trading/docs/student_deepseek_quick_reference.md` | Quick reference operateur |
| `/opt/trading/student/docs/RUNBOOK.md` | Runbook d'exploitation canonique |
| `/home/student/shortcut_targets_student_20260303_182326.log` | Audit detaille des cibles de raccourcis |
| `/home/student/menu_audit_student_20260303_182326.log` | Inventaire des raccourcis exposes |
| `/home/student/ref_student/23_repo_file_list.txt` | Evidence de l'etat cible historicise |
| `/home/student/infra-context-run/snapshot/snapshot_2026-02-26T15-09-46-05-00.txt` | Snapshot machine de reference |

## Hypotheses de pilotage retenues

1. L'alias `student` est aujourd'hui redirige vers `deepseek_hub` de maniere volontaire et fonctionnelle.
2. La derive historique vient d'une coexistence de deux conventions de scripts `student`.
3. Le Kanban doit suivre a la fois la stabilisation immediate et la dette d'architecture.
