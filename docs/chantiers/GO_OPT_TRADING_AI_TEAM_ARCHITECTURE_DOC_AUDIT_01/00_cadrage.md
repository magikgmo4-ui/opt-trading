# GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_DOC_AUDIT_01 - 00_cadrage

## Besoin initial

Executer un audit documentaire technique detaille, source par source, pour les frameworks et surfaces de reference utiles a une future architecture interne d'equipe d'agents, sans rouvrir le parent et sans choisir de stack finale dans ce GO.

## Cible finale locale GO

Produire un dossier enfant `doc-only` qui :
- reprend le point canonique de reprise valide ;
- audite `CrewAI`, `LangGraph`, `AutoGen` et `OpenAI Agents SDK` ;
- garde `Marblism` comme reference produit observee seulement ;
- distingue clairement `ETABLI`, `HYPOTHESE` et `GAPS` ;
- consolide une matrice comparative `axe x source x preuve x limite x interet`.

## 7_CANONICAL_STATE

- branche canonique de reprise : `GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01`
- fichier canonique de session : `docs/chantiers/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_DOC_AUDIT_01/SESSION_REPRISE.txt`
- ancre GitHub validee : commit `304fdf5`
- prochaine action coherente : `PASSE 3 - AUDIT TECHNIQUE DETAILLE SOURCE PAR SOURCE`

## Invariants

- repartir de `7_CANONICAL_STATE` ;
- ne pas rouvrir le parent ;
- rester strictement `doc-only` ;
- ne conclure sur aucune stack finale dans ce GO ;
- traiter `Marblism` comme reference produit observee, pas comme base technique interne ;
- documenter uniquement des constats bornes par preuves explicites.

## Sources de preuve retenues

- `https://docs.crewai.com/`
- `https://docs.crewai.com/en/concepts/agents`
- `https://docs.crewai.com/en/concepts/flows`
- `https://docs.langchain.com/oss/python/langgraph/overview`
- `https://docs.langchain.com/oss/python/langgraph/persistence`
- `https://microsoft.github.io/autogen/stable/`
- `https://microsoft.github.io/autogen/stable/user-guide/core-user-guide/quickstart.html`
- `https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/quickstart.html`
- `https://openai.github.io/openai-agents-python/`
- `https://www.marblism.com/`

## Sortie attendue de la passe 3

- journal technique de passe 3 avec constats par source ;
- decisions bornees interdisant toute conclusion prematuree sur une stack ;
- support de reprise local aligne sur l'ancre GitHub fournie.
