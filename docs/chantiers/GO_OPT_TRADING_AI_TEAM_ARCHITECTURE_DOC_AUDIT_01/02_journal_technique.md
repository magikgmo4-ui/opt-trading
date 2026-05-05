# GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_DOC_AUDIT_01 - 02_journal_technique

## Besoin initial

Executer la passe 3 d'audit technique detaille source par source pour `CrewAI`, `LangGraph`, `AutoGen` et `OpenAI Agents SDK`, en gardant `Marblism` comme reference produit observee seulement.

## Plan retenu

1. Repartir de `7_CANONICAL_STATE` du parent et du support de reprise annonce.
2. Relever des preuves primaires par documentation officielle publique.
3. Produire `ETABLI / HYPOTHESE / GAPS` pour chaque source.
4. Consolider une matrice comparative par axes techniques.
5. Refermer la passe sans conclure sur une stack finale.

## ETABLI

### Marblism - reference produit observee seulement

Preuves : `https://www.marblism.com/`

- Marblism se presente comme une offre de `AI Employees` preconfigures par role metier (`SEO Blog Writer`, `Executive Assistant`, `Lead Generation`, `Receptionist`, `Legal Assistant`).
- La valeur exposee est orientee resultat produit et usages business : inbox, socials, SEO, calls, support, calendar, lead generation.
- Le site mentionne des integrations applicatives (`Gmail`, `Outlook`, `Instagram`, `Facebook`, `X`, `LinkedIn`, `Google Calendar`, etc.) et une boucle de feedback/approval cote utilisateur.
- La surface publique observee ne documente pas de primitives techniques exploitables de type runtime, graph, handoff, memory schema, guardrails ou tracing developer-first.

### CrewAI

Preuves : `https://docs.crewai.com/`, `https://docs.crewai.com/en/concepts/agents`, `https://docs.crewai.com/en/concepts/flows`

- CrewAI expose explicitement trois briques visibles cote dev : `agents`, `crews` et `flows`.
- Un `Agent` peut porter role, goal, tools, memory, knowledge sources, delegation et callbacks ; le produit couvre donc bien un pattern d'equipe a roles specialises.
- `Flows` apportent une orchestration event-driven avec `@start`, `@listen`, `@router`, etat partage, branchements conditionnels, persistence et reprise.
- CrewAI documente un mecanisme `human_feedback` pour inserer des points d'approbation humaine dans un flow.
- CrewAI documente une memoire unifiee accessible dans les flows (`remember`, `recall`, `extract_memories`) et indique une persistence sur disque.
- La documentation publique mentionne aussi de l'observabilite, du monitoring et des surfaces enterprise, mais avec une forte articulation produit/plateforme autour de CrewAI AMP.
- La doc indique que l'ancien code execution integre est deprecie et recommande des sandboxes dediees externes (`E2B`, `Modal`) pour l'execution de code securisee.

### LangGraph

Preuves : `https://docs.langchain.com/oss/python/langgraph/overview`, `https://docs.langchain.com/oss/python/langgraph/persistence`

- LangGraph se presente comme un framework `low-level` centre sur l'orchestration d'agents et workflows stateful longue duree.
- Les axes explicitement revendiques sont : `durable execution`, `human-in-the-loop`, `comprehensive memory`, `streaming`, observabilite/debug via `LangSmith`, et deploiement production.
- Le coeur technique est un graphe compile avec etat, noeuds, edges et checkpoints ; l'execution peut etre reprise a partir de checkpoints via `thread_id`.
- La persistence est un concept central : checkpoints par super-step, historique d'etat, replay, mise a jour d'etat, tolere les pannes et facilite les workflows a interruption humaine.
- LangGraph distingue memoire intra-thread via checkpointer et memoire inter-threads via `Store`, avec options de persistance (`SQLite`, `Postgres`, `Cosmos DB`) et chiffrement possible.
- La documentation insiste sur le fait que LangGraph n'impose pas une architecture d'agent haute abstraction ; l'utilisateur garde la responsabilite du design applicatif.

### AutoGen

Preuves : `https://microsoft.github.io/autogen/stable/`, `https://microsoft.github.io/autogen/stable/user-guide/core-user-guide/quickstart.html`, `https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/quickstart.html`

- AutoGen est decoupe en couches distinctes : `AgentChat`, `Core`, `Extensions`, `Studio`.
- `AgentChat` fournit une couche plus rapide a prendre en main avec agents preconfigures, tools, streaming, human-in-the-loop, teams, state, tracing et workflows `GraphFlow`.
- `Core` expose un modele plus bas niveau fonde sur runtime d'agents, messages, subscriptions, topics et runtimes distribuables.
- La doc `Core` insiste sur la separation entre logique d'agent et infrastructure de communication via `Agent Runtime`.
- AutoGen mentionne explicitement un runtime local single-threaded et un runtime distribue, donc une capacite structurelle pour des systemes multi-processus ou multi-machines.
- `Extensions` couvrent des integrations externes, notamment MCP, OpenAI Assistant Agent, executors Docker et runtimes gRPC.
- `Studio` est presente comme une UI de prototypage sans code, mais repose sur les couches dev-first sous-jacentes.

### OpenAI Agents SDK

Preuves : `https://openai.github.io/openai-agents-python/`

- L'OpenAI Agents SDK se positionne comme un package Python leger avec peu d'abstractions et quelques primitives centrales : `Agents`, `Handoffs / Agents as tools`, `Guardrails`.
- Le SDK revendique un agent loop gere, le tool calling, des guardrails, des sessions, du tracing, du human-in-the-loop et des mecanismes de sandbox agents/workspaces.
- La documentation distingue explicitement `Agents SDK` et `Responses API` : le SDK ajoute un runtime plus haut niveau autour des appels modele.
- Le SDK documente des sessions persistantes, des integrations MCP, des outils, des handoffs et des surfaces realtime/voice.
- La proposition est clairement Python-first et volontairement minimaliste en primitives, avec personnalisation possible quand necessaire.

## HYPOTHESE

### Marblism

- Le pattern produit observable de Marblism peut aider a cadrer les roles metier, les boucles d'approbation et les integrations attendues, mais pas la forme exacte du runtime interne.

### CrewAI

- CrewAI semble pertinent si la priorite future devient une combinaison directe `roles + orchestration + HITL + memory + UX produit` avec un temps d'amorcage faible.
- La forte presence de surfaces AMP/enterprise suggere qu'une partie des usages production/ops peut etre plus confortable dans l'ecosysteme CrewAI complet que dans la seule lib coeur.

### LangGraph

- LangGraph semble plus adapte si la cible interne privilegie la maitrise fine de l'orchestration, la reprise, les interruptions humaines, les etats persistants et la composabilite faible abstraction.
- Le cout d'integration et de design applicatif risque d'etre plus eleve qu'avec des frameworks plus prescriptifs.

### AutoGen

- AutoGen semble offrir la palette la plus etagee pour separer prototypage rapide (`AgentChat`, `Studio`) et architecture plus explicite/distribuee (`Core`).
- Cette richesse modulaire peut aussi augmenter la charge de choix et de normalisation si une architecture interne simple est recherchee.

### OpenAI Agents SDK

- Le SDK semble particulierement pertinent si l'architecture cible veut rester proche des primitives OpenAI recentes, avec handoffs, guardrails et outillage Python sans couche conceptuelle lourde.
- L'interet des `sandbox agents` est eleve pour des cas de travail sur fichiers/workspaces, mais depend de l'adequation au perimetre technique reel du produit interne.

## GAPS

### Marblism

- Pas de documentation technique publique suffisante pour qualifier runtime, persistence, observabilite, securite, topologie d'agents ou schema memoire.
- Pas de preuve publique exploitable pour une comparaison technique framework-to-framework.

### CrewAI

- Le partage exact entre capacites open-source et capacites veritablement dependantes de surfaces AMP/enterprise doit etre revalide avant toute decision future.
- La granularite des garanties de persistence, d'observabilite et de securisation runtime doit etre examinee plus profondement si CrewAI reste en shortlist.

### LangGraph

- La documentation confirme bien la puissance du moteur d'orchestration, mais pas une architecture d'equipe d'agents pre-modelee equivalente a un produit type Marblism.
- Le niveau d'effort necessaire pour recomposer roles, policies, UX operateur et gouvernance metier reste a estimer.

### AutoGen

- Le recouvrement exact entre `AgentChat`, `Core`, `GraphFlow`, `Studio` et extensions doit etre consolide pour eviter une lecture trop large du perimetre reel de chaque couche.
- Les primitives memoire, approval et observabilite meritent une passe de preuve plus fine si AutoGen est retenu dans le cadrage suivant.

### OpenAI Agents SDK

- La portabilite hors ecosysteme OpenAI, ainsi que le cout d'adhesion aux primitives SDK pour des besoins tres custom, restent a qualifier.
- Le comportement exact des sessions, guardrails et sandboxs en environnement produit cible demande une passe complementaire si cette piste est poursuivie.

## Matrice comparative consolidee

| Axe | Source | Preuve | Limite | Interet |
| --- | --- | --- | --- | --- |
| Modele d'equipe a roles | Marblism | Offre publique par `AI Employees` specialises par role metier | Produit observe, pas dev docs | Tres utile pour la forme produit attendue |
| Modele d'equipe a roles | CrewAI | `Agents` avec role, goal, delegation, tools, memory | Forte proximite produit/plateforme | Eleve pour equipes specialisees rapidement configurables |
| Modele d'equipe a roles | LangGraph | Graph framework low-level, pas de role model preimpose | Plus d'assemblage applicatif necessaire | Eleve si design interne tres controle |
| Modele d'equipe a roles | AutoGen | `AgentChat` plus `Core` et patterns multi-agent | Couches nombreuses a borner | Eleve pour architectures modulaires |
| Modele d'equipe a roles | OpenAI Agents SDK | `Agents`, `Handoffs`, `Agents as tools` | Primitives plus minimales | Eleve pour coordination simple et nette |
| Orchestration | CrewAI | `Flows` avec `@start`, `@listen`, `@router`, branching | Semantique propre au framework | Eleve pour workflows event-driven lisibles |
| Orchestration | LangGraph | Graphes, noeuds, edges, compile, super-steps | Abstraction plus bas niveau | Tres eleve pour controle fin et reprise |
| Orchestration | AutoGen | `Core` runtime/messages/subscriptions ; `GraphFlow` cote AgentChat | Plusieurs couches a comparer | Eleve pour runtime et patterns varies |
| Orchestration | OpenAI Agents SDK | Agent loop gere, handoffs, agents as tools | Moins large qu'un moteur de graphe generaliste | Eleve pour orchestration legere |
| Memoire / etat | CrewAI | Memory unifiee dans flows ; etat de flow ; persistence SQLite documentee | Niveau exact de garanties a confirmer | Moyen a eleve |
| Memoire / etat | LangGraph | Checkpoints, threads, store inter-threads, replay | Plus de plomberie applicative | Tres eleve pour etat durable et auditabilite |
| Memoire / etat | AutoGen | State management documente ; couches multiples | Preuves fines encore a consolider | Moyen a eleve |
| Memoire / etat | OpenAI Agents SDK | Sessions persistantes et memory layer documentees | A qualifier en profondeur sur cas reel | Eleve |
| Human-in-the-loop | Marblism | Le site parle d'approvals et feedback utilisateur | Marketing, pas specifics techniques | Moyen pour cible UX |
| Human-in-the-loop | CrewAI | `@human_feedback` dans les flows | Dependances version/plateforme a verifier | Eleve |
| Human-in-the-loop | LangGraph | Interrupts et reprise par checkpoints | Demande plus de design | Tres eleve |
| Human-in-the-loop | AutoGen | Tutoriels dedies et interventions possibles | Passe detaillee encore manquante | Eleve |
| Human-in-the-loop | OpenAI Agents SDK | Rubrique dediee `Human-in-the-loop` | Details operatoires a creuser | Eleve |
| Outils / surfaces reelles | Marblism | Integrations Gmail, Outlook, socials, calendar annoncees | Pas de details dev publics | Moyen pour reference produit |
| Outils / surfaces reelles | CrewAI | Tools, knowledge sources, integrations enterprise | Part open-source vs enterprise a distinguer | Eleve |
| Outils / surfaces reelles | LangGraph | Integrable avec modeles et tools sans imposer LangChain | Peu prescriptif | Eleve pour architecture interne sur mesure |
| Outils / surfaces reelles | AutoGen | Extensions MCP, OpenAI assistants, Docker, gRPC | Ecosysteme riche donc plus complexe | Tres eleve |
| Outils / surfaces reelles | OpenAI Agents SDK | Function tools, MCP, sandbox agents | Ecosysteme plus centre SDK/OpenAI | Eleve |
| Observabilite | CrewAI | Monitoring/observability mis en avant dans docs/index | Surface potentiellement couplee plateforme | Moyen a eleve |
| Observabilite | LangGraph | LangSmith trace/debug/eval documentes | Couplage ecosysteme LangSmith | Tres eleve |
| Observabilite | AutoGen | Logging, telemetry, tracing documentes | Passe detaillee non faite ici | Eleve |
| Observabilite | OpenAI Agents SDK | Tracing natif documente | Depth a verifier sur usage interne | Eleve |
| Securite / execution | CrewAI | Execution integree depreciee ; sandbox externe recommandee | Moins integre nativement | Moyen |
| Securite / execution | LangGraph | Chiffrement checkpointers et persistance outillee | Pas un sandbox applicatif complet a lui seul | Eleve sur persistance, moyen sur execution isolee |
| Securite / execution | AutoGen | Docker executors et runtime distribue via extensions | Architecture plus lourde | Eleve |
| Securite / execution | OpenAI Agents SDK | Guardrails et sandbox agents documentes | A qualifier sur contraintes produit reelles | Tres eleve |

## REPRISE

- base canonique : `docs/chantiers/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_DOC_AUDIT_01/SESSION_REPRISE.txt`
- passe executee ici : `PASSE 3 - AUDIT TECHNIQUE DETAILLE SOURCE PAR SOURCE`
- prochaine suite logique, sans conclure ici sur une stack finale : synthese architecturale cible par axes internes, en repartant de la matrice ci-dessus.

## Verdict PASS / OPEN / FAIL

PASS

## PASSE 3B — STRICT_WORKERS SEED ARTEFACT (INTERNAL)

Preuves : branche `go/GO_OPT_TRADING_STRICT_WORKERS_PARENT_01`, `docs/agents/strict_workers/`

### ETABLI

- Strict Workers est un parent actif cote fantome, non merge dans mainline, mais pleinement documente sur sa branche.
- `STRICT_WORKERS_AUTONOMIE_ETROITE_01.md` definit une doctrine complete : agent a autonomie etroite, couloir ferme, validation externe obligatoire, interdits permanents.
- `MODELS_MATRIX_01.md` qualifie 14 modeles OpenCode Zen (CONFIRMED_OFFICIAL_DOC) + 6 pending (A_VERIFIER_ENDPOINT), avec quotas 5h/semaine/mois et profils conseilles.
- `tasks.index.json` definit 6 types de taches autorisees (READ_INVENTORY, PATCH_DRAFT, DOC_DRAFT, TESTPLAN, CHERRY_PICK_INVENTORY, FAST_TRIAGE) avec autonomie max (A1/A2), garde-fous (`no_secrets`, `no_env_files`, `no_git_write_ops`, `no_runtime_write_by_default`), required_sections et preferred_workers.
- `models.registry.json` liste 14 modeles VERIFIED + 6 modele PENDING.
- `02_READONLY_SMOKE_EXEC_REPORT.md` et `03_READONLY_SMOKE_VALIDATION.md` prouvent un smoke READ_INVENTORY execute et valide (VALIDATION_PASS_DRAFT_ONLY).
- `90_CLOSEOUT.md` confirme CLOSEOUT_PARENT_DRAFT_ONLY : phase gelee, aucun PATCH_DRAFT execute, aucun write runtime.

### Positionnement dans l'audit

Strict Workers n'est **pas un framework externe**. C'est un **seed artefact interne** qui peut servir de brique a l'architecture cible :

| Axe | Apport Strict Workers |
| --- | --- |
| Modele d'equipe a roles | Non applicable (pas un framework multi-agent) |
| Orchestration | Runner securise en couloir ferme, pas d'orchestrateur multi-agent |
| Memoire / etat | Gestion explicite via required_sections (13_ESTABLISHED, 14_HYPOTHESIS, etc.) |
| Human-in-the-loop | Validation externe obligatoire + consolidation modele fort/humain |
| Outils / surfaces reelles | Tasks index ferme + denied_inputs/denied_commands |
| Observabilite | Sortie DRAFT_ONLY structuree + git diff verification |
| Securite / execution | Garde-fous no_secrets, no_env_files, no_git_write_ops, no_runtime_write_by_default |
| Modele IA | 14 modeles qualifies avec quotas reels, 6 task types bornes |

### Interet pour l'architecture cible

- Strict Workers fournit deja une **politique de securite complete** (garde-fous, denied inputs/commands, no_runtime_write_by_default) utilisable comme socle.
- Le **tasks index** et le **format de sortie obligatoire** sont directement transposables en contrats d'architecture.
- La **matrice de modeles** avec quotas reels evite de speculer sur des capacites IA : les modeles sont prouves et quotas connus.
- Le **smoke READ_INVENTORY valide** donne une preuve reelle (pas juste une spec) de ce qu'un strict worker peut faire.
- **Ne remplace pas** un framework d'orchestration ou de memoire (LangGraph, CrewAI, etc.) mais **completerait** n'importe lequel comme couche de securite.

### GAPS

- Aucun runner runtime verrouille (strict workers fonctionne aujourd'hui via OpenCode/OpenClaw manuellement).
- Aucun PATCH_DRAFT execute (la phase est gelee en DRAFT_ONLY).
- Aucune integration avec un framework d'orchestration n'est testee.
- Les modeles pending (MiMo-V2, DeepSeek V4, etc.) restent a confirmer via endpoint.

## REPRISE

- base canonique : `docs/chantiers/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_DOC_AUDIT_01/SESSION_REPRISE.txt`
- passe executee ici : `PASSE 3B - STRICT_WORKERS SEED ARTEFACT (INTERNAL)`
- prochaine suite logique : `PASSE 4 - SYNTHESE D'ARCHITECTURE CIBLE INTERNE PAR AXES`
