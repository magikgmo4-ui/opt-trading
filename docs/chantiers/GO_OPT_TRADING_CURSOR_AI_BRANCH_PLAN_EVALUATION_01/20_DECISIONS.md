# 20_DECISIONS — Cursor-ai branch plan

## Decisions

### DROP_MERGED : `OBSERVER_TRADINGVIEW_MCP_01`

- **Decision** : Supprimer la branche remote. Le parent MCP est merged (PR #200).
- **Action** : `git push origin --delete go/GO_OPT_TRADING_CURSOR_AI_OBSERVER_TRADINGVIEW_MCP_01`
- **Condition** : Aucune. Le contenu est entierement dans `sot/mainline`.

### REVIEW_MERGE : `OPERATIONS_PARENT_01`

- **Decision** : Revoir et merger si le contenu doc-only est utile.
- **Contenu** : 5 fichiers de continuite operations (00_START, 10_CHILDREN_INDEX, 20_POST_MERGE_REPRISE, 30_SHARED_PACKET_OPTION_B, 40_ALERT_WEBHOOK_TEMPLATE).
- **Risque** : Faible. Doc-only.

### REVIEW_MERGE : `POST_MERGE_REPRISE_01`

- **Decision** : Revoir et merger si utile.
- **Contenu** : 5 fichiers post-merge reprise (00_START, 10_POST_MERGE_STATE, 20_OPERATOR_COMMANDS, 30_LIGHT_SMOKE, 90_CLOSEOUT).
- **Risque** : Faible. Doc-only.

### REVIEW_MERGE : `SHARED_PACKET_01`

- **Decision** : Revoir et merger si utile.
- **Contenu** : 5 fichiers shared packet export + .gitignore.
- **Note** : Inclut un `.gitignore`. Seule branche avec un fichier non-.md.
- **Risque** : Faible. Doc + .gitignore.

### KEEP_ACTIVE : `ALERT_WEBHOOK_TEMPLATE_01` et `PARENT_CLOSEOUT_01`

- **Decision** : Conserver comme chantiers enfants actifs.
- **Note** : Ces deux branches partagent le meme commit `78915bb`. Une fois l'une mergee, l'autre devient DROP_DUPLICATE.
- **Action proposee** : Choisir une branche a merger, supprimer l'autre comme duplicate.

## Prochain GO recommande

1. Supprimer `OBSERVER_TRADINGVIEW_MCP_01` (DROP_MERGED).
2. Merger les 3 branches REVIEW_MERGE dans l'ordre : OPERATIONS_PARENT, POST_MERGE_REPRISE, SHARED_PACKET.
3. Merger ALERT_WEBHOOK_TEMPLATE_01 ou PARENT_CLOSEOUT_01, supprimer le duplicate.

## RISKS

- À qualifier.
