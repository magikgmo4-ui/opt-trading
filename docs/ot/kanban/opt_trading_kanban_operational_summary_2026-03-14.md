# OPT-TRADING — SYNTHÈSE OPÉRATIONNELLE DU KANBAN

Source : construite à partir de `docs/ot/kanban/opt_trading_kanban_source_of_truth.md` et des statuts déjà établis dans les closings / documents de continuité de la session.

## Tableau de synthèse

| Bloc | État | Nature | Réouverture | Suite |
|---|---|---|---|---|
| SHARED / SSHFS | ÉTABLI / STABLE | infra | non | GO_OT_TRAE_AGENTS_V1_OPEN_01 |
| Starter Pack / Opening | ÉTABLI / STABLE | doctrine repo | non | GO_OT_TRAE_AGENTS_V1_OPEN_01 |
| validated_prompt_factory | CLOSE | outil opérateur | non | aucune |
| trae_module_validator | ÉTABLI / ACTIVE (FORMALISÉ) | outil opérateur | non | GO_OT_TRAE_AGENTS_V1_OPEN_01 |
| Socle doctrinal Trae | ÉTABLI / PARTIEL | helper doctrinal | CONFIRMÉ PARTIELLEMENT (adoption) | GO_OT_TRAE_AGENTS_V1_OPEN_01 |
| Runtime vs snapshot repo | DIVERGENT / SUIVI | gouvernance ops | NON CONFIRMÉ MAIS ACCEPTÉ (invariant documenté) | GO_OT_TRAE_AGENTS_V1_OPEN_01 |
| Trae pré-V1 (statut global) | PRE_V1_COHERENT_AVEC_DELTAS_FINAUX | orchestration / système | non | GO_OT_TRAE_AGENTS_V1_OPEN_01 |
| CONTRADICTOIRE (cadrage) | CLOSE (CADRÉ / OPPOSABLE) | gouvernance | non | GO_OT_TRAE_AGENTS_V1_OPEN_01 |
| Rules Trae V1 | ACTIVE (V1_OPEN) | couche V1 | oui | ouverture actée (doc-only) ; suite: GO_OT_TRAE_AGENTS_V1_OPEN_01 |
| Agents Trae V1 | ÉTABLI / GELÉ (PRE-V1, OPPOSABLE) | couche V1 | oui | gel pré-V1 acté (doc-only) ; suite: GO_OT_TRAE_AGENTS_V1_OPEN_01 |
| Skills Trae V1 | ÉTABLI / GELÉ (PRE-V1, OPPOSABLE) | couche V1 | oui | gel pré-V1 acté (doc-only) ; suite: GO_OT_TRAE_AGENTS_V1_OPEN_01 |
| MCP Policy V1 | ÉTABLI / GELÉ (PRE-V1, OPPOSABLE) | gouvernance | oui | gel pré-V1 acté (doc-only) ; suite: GO_OT_TRAE_AGENTS_V1_OPEN_01 |

## Règle de maintenance
- mettre à jour ce tableau à chaque closing qui change un statut, une preuve réelle, un point de reprise, une interdiction de réouverture ou l’ordre logique de la suite ;
- ce tableau ne remplace pas le détail du kanban ;
- en cas de conflit, le kanban détaillé et les closings priment.
