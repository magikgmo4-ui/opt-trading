# workflow_post_change_v2

Hook post-change operateur pour tracer un evenement de changement et, si demande, declencher des roadmaps DeepSeek cote `student`.

## Role
- enregistrer un evenement post-change
- pousser/logguer si les scripts support existent
- declencher en tache de fond `cmd-deepseek_response roadmap_module` et `cmd-deepseek_thinking roadmap_module`

## Contenu
- `scripts/post_change.sh` : logique principale
- `scripts/cmd.sh`, `menu.sh`, `sanity_check.sh`
- `scripts/sanity_check_post_change_v2.sh` : verification ciblee du hook

## Comportement observe
- la capture de journal local est retiree
- la copie `student` locale est retiree
- le hook tente encore :
  - `scripts/push_and_log.sh` si disponible
  - `scripts/log_event_to_student.sh` sinon
  - deux triggers SSH vers `student` pour les roadmaps DeepSeek

## Statut
- actif
- outil operateur, pas runtime produit

## Notes de consolidation
- garder cette surface alignee avec la doctrine post-journal actuelle
- toute evolution doit rester compatible avec l'abandon du journal local et la logique de continuite actuelle
