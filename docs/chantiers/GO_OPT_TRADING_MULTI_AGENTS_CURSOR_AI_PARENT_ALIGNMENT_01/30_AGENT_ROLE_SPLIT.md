# Separation des roles agents et outils

## Roles retenus

| Surface | Role retenu | Machine principale | Limite |
| --- | --- | --- | --- |
| `ChatGPT` | cadrage, arbitrage, synthese, continuite, preparation des GO et prompts | `cursor-ai` | ne remplace pas le repo, ni les preuves runtime |
| `Claude` | worker local code/docs selon prompt borne | `cursor-ai` | pas de refactor global ni de mutation runtime sans GO |
| `Trae` | IDE / cockpit mission / automation skill-first | `cursor-ai` | pack legacy non souverain ; doctrine active reste `workflow_ai` |
| `Git/GitHub` | verite des branches, commits, diff, PR, historique | `cursor-ai` | support Git, pas doctrine produit |
| `OpenCode` | code engine / runtime terminal si present | cote runtime `tmux/OpenCode/OpenClaw`, pas prouve localement sur `cursor-ai` | non detecte localement dans ce GO |
| `OpenClaw` | orchestrateur experimental borne / provider layer | `db-layer` | ne doit pas etre melange a la gouvernance locale Windows |
| `Ollama` | provider local lab / inference locale differee | `student` | pas de gouvernance, pas de production, pas de trading live |
| `strict workers` | micro-workers a autonomie etroite, sorties `DRAFT_ONLY` avec validation externe | plutot `fantome` / `AI Team` | pas de patch durable ou runtime sans GO distinct |

## Split par machine

| Machine | Chantier principal retenu | Role |
| --- | --- | --- |
| `db-layer` | `GO_OPT_TRADING_MACHINE_DB_LAYER_PARENT_01` + cycles clos `OpenClaw` / `LocalCMS` | machine d'execution actuelle |
| `admin-trading` | `GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01` | runtime trading, collectors, bot_vision, deskpro, webhook, differe pour l'instant |
| `cursor-ai` | `GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01` | orchestration multi-agents, Git, IDE, prompts, continuite |
| `fantome` | `GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01` | AI Team / specialisation agents ; `strict workers` y reste adjacent |
| `student` | `GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01` | lab Ollama differe |

## Frontiere OpenCode / OpenClaw

La source `10_CROSS_CHANTIERS_OPENCLAW_TMUX_AGENTS_REVIEW.md` fixe la separation suivante :

- `tmux` = persistance runtime
- `OpenCode` = production / code engine
- `OpenClaw` = orchestration / control plane runtime
- `GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01` = taxonomie transverse et doctrine

Consequence :

- `cursor-ai` peut porter la gouvernance multi-agents
- `cursor-ai` ne devient pas le proprietaire runtime de `OpenCode/OpenClaw`

## Question du parent machine cursor-ai

### Reponse retenue dans ce GO

- **non, pas maintenant**

### Motif

- la preuve existante dit deja que `cursor-ai` garde `GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01` comme principal
- le besoin courant porte sur orchestration, repo ops, prompts, IDE et arbitrage
- aucun chantier machine `cursor-ai` specifique a du runtime, du reseau ou de l'infra locale n'est prouve comme necessaire

### Condition de reouverture eventuelle

Un parent machine `cursor-ai` ne deviendrait defensable que si un futur lot ouvre explicitement :

- automation Windows locale persistante
- outillage machine specifique hors simple orchestration
- surfaces runtime propres a `cursor-ai`
- contraintes locales de securite / PATH / IDE qui depassent le role documentaire actuel
