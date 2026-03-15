# OPT-TRADING — SYNTHÈSE OPÉRATIONNELLE DU KANBAN

Source : construite à partir de `docs/ot/kanban/opt_trading_kanban_source_of_truth.md` et des statuts déjà établis dans les closings / documents de continuité de la session.

## Tableau de synthèse

| Bloc | État | Nature | Réouverture | Suite |
|---|---|---|---|---|
| SHARED / SSHFS | ÉTABLI / STABLE | infra | non | GO_OT_NEXT_MISSION_SELECTION_01 |
| Starter Pack / Opening | ÉTABLI / STABLE | doctrine repo | non | GO_OT_NEXT_MISSION_SELECTION_01 |
| validated_prompt_factory | CLOSE | outil opérateur | non | aucune |
| trae_module_validator | ÉTABLI / ACTIVE (FORMALISÉ) | outil opérateur | non | GO_OT_NEXT_MISSION_SELECTION_01 |
| Socle doctrinal Trae | ÉTABLI / PARTIEL | helper doctrinal | CONFIRMÉ PARTIELLEMENT (adoption) | GO_OT_NEXT_MISSION_SELECTION_01 |
| Runtime vs snapshot repo | DIVERGENT / SUIVI | gouvernance ops | NON CONFIRMÉ MAIS ACCEPTÉ (invariant documenté) | GO_OT_NEXT_MISSION_SELECTION_01 |
| Rules Trae V1 | MANQUANT / À OUVRIR | couche V1 | oui | après sélection explicite |
| Agents Trae V1 | MANQUANT / À OUVRIR | couche V1 | oui | après Rules |
| Skills Trae V1 | MANQUANT | couche V1 | oui | après Agents |
| MCP Policy V1 | MANQUANT / REPORTÉ | gouvernance | oui | après Skills si besoin prouvé |

## Règle de maintenance
- mettre à jour ce tableau à chaque closing qui change un statut, une preuve réelle, un point de reprise, une interdiction de réouverture ou l’ordre logique de la suite ;
- ce tableau ne remplace pas le détail du kanban ;
- en cas de conflit, le kanban détaillé et les closings priment.
