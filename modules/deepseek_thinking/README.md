# deepseek_thinking

Module specialise pour produire le "thinking" DeepSeek cote `student`, avec sorties archivees et generation de roadmap par module.

## Role
- lancer une requete Ollama avec `think=true`
- ecrire les sorties dans `_student_archive/thinking`
- produire des roadmaps par module via script Python dedie

## Contenu
- `scripts/deepseek_thinking_cmd.sh` : commandes `run`, `tail`, `roadmap_module`
- `scripts/deepseek_thinking_menu.sh`
- `scripts/roadmap_thinking_by_module.py`
- wrappers generiques `cmd`, `menu`, `sanity`

## Statut
- actif en compatibilite operatoire
- famille a consolider avec `deepseek_hub`

## Notes de consolidation
- `deepseek_hub` indique deja qu'il unifie et corrige `deepseek_thinking`
- ne pas supprimer ce module tant que la famille `deepseek*` n'a pas un survivant final confirme
- a lire avec `modules/deepseek_hub/README.md` et `modules/deepseek_student/README.md`
