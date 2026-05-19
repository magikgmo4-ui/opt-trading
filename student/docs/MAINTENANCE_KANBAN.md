# Student Maintenance Kanban

## Board

| ID | Tache | Statut | Priorite | Objectif de fin |
|---|---|---|---|---|
| M-01 | Inventorier les legacy paths encore actifs | A faire | Haute | liste validee des anciens chemins encore reellement utilises |
| M-02 | Reduire les doublons `deepseek_student` | A faire | Haute | role final clarifie entre wrapper riche et helper backend |
| M-03 | Retirer les installateurs non officiels | A faire | Moyenne | un seul installateur officiel conserve : `/opt/trading/student/bin/install_shortcuts.sh` |
| M-04 | Nettoyer la doc historique redondante | A faire | Moyenne | ancienne doc marquee historique, doc canonique mise en avant |
| M-05 | Passer `student` en run maintenance | En cours | Haute | checks periodiques definis : `sanity-student`, `cmd-student status`, revue doc |

## Mode Maintenance Recommande

- source de verite : `/opt/trading/student`
- commandes officielles :
  - `sanity-student`
  - `cmd-student`
  - `menu-student`

## Revue Periodique

1. lancer `sanity-student`
2. lancer `cmd-student status`
3. verifier la coherence de la doc canonique
4. nettoyer un lot legacy a la fois

## Priorite D'Execution

1. `M-01`
2. `M-02`
3. `M-03`
4. `M-04`
5. `M-05`
