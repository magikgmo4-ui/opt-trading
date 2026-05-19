---
doc_id: OPT_TRADING_MULTI_AGENTS_CANON_PARENT_INITIAL_PROJECT_DOC_01
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: multi_agents
go_id: GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01
status: open
lifecycle_stage: cadrage
topic_keys:
  - opt-trading
  - multi_agents
  - openclaw
  - codex
  - claude
  - trae
  - ollama
  - workflow_ai
  - validated_prompt_factory
  - deploy_module_multi_machine
  - governance
  - frontmatter
  - search_tags
  - naming
  - indexation
search_tags:
  - surface:chantier
  - doc_role:initial_project_doc
  - family:openclaw_agents_prompt_factory
  - governance:multi_agents_doctrine
  - integration:workflow_ai
  - integration:validated_prompt_factory
  - integration:deploy_module_multi_machine
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
point_de_reprise: "17_RESUME_POINT"
updated_at: 2026-04-26
links:
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
  - workflow_ai/WORKFLOW.md
  - modules/validated_prompt_factory/README.md
  - docs/deploy_module_multi_machine_continuity.md
  - docs/product_targets/OPENCLAW_TARGET_CANON.md
  - docs/ot/project_cards/PROJECT_CARD_OPENCLAW_01.md
  - docs/architecture/REPO_SURFACES_MAP.md
  - docs/index/GO_INDEX.md
  - docs/index/NEXT_GO_CANDIDATES.md
  - docs/index/ACTIVE_STREAMS.md
  - docs/index/REPRISE.md
---

# GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01 — INITIAL PROJECT DOC

## 1_MASTER_TARGET

Canoniser la doctrine multi-agents `Codex / Claude / Trae / Ollama` dans `opt-trading`, avec `OpenClaw` comme orchestrateur experimental borne, sans rouvrir ni reconstruire les chantiers OpenClaw deja actifs.

Le but est documentaire et operationnel : aligner la place des agents, skills, providers, prompts, bundles, index, naming, frontmatter et search tags dans la matrice gouvernante et dans la matrice operationnelle du repo.

## 2_INITIAL_PROJECT_DOC

Ce document est le document transporteur initial du chantier parent. Il fige la reponse validee precedente et sert de reference autonome hors session.

Il doit rester stable tant que le projet ne change pas explicitement ou implicitement. Les documents suivants du chantier pourront affiner le plan, mais ne doivent pas remplacer cette base sans decision documentee.

## 3_INITIAL_NEED

Demande utilisateur :

- ouvrir un chantier parent sur une branche dediee ;
- documenter l'integralite de la derniere reponse validee ;
- produire une documentation complete independante de la session ;
- canoniser la documentation presente et sa place dans la doc, la matrice gouvernante et la matrice operationnelle ;
- integrer naming, indexation, frontmatter et search tags dans la doctrine multi-agents ;
- partir de l'existant, pour une coherence parfaite dans l'execution ;
- ensuite seulement affiner les recherches, etablir un plan complet, le documenter et preparer un bundle d'execution ;
- rester sur le sujet multi-agents, car d'autres chantiers existent deja sur OpenClaw.

## 4_MASTER_PROJECT_PLAN

Plan maitre du chantier parent :

1. ancrer le chantier parent et la branche dediee ;
2. documenter le socle existant valide ;
3. canoniser la typologie `agents / skills / providers / orchestrateur / deployer / prompt factory` ;
4. aligner cette typologie avec `MATRICE_DOC_OPS_MASTER_MATRIX_01` ;
5. definir les champs frontmatter et `search_tags` utiles pour les documents multi-agents ;
6. definir le nommage GO et les surfaces documentaires associees ;
7. integrer `workflow_ai`, `validated_prompt_factory` et `deploy_module_multi_machine` comme briques existantes, non a reconstruire ;
8. separer strictement ce chantier multi-agents des chantiers OpenClaw runtime deja actifs ;
9. produire ensuite une recherche approfondie et un plan complet ;
10. produire enfin un bundle d'execution transportable.

## 5_GO_PLAN

GO parent : `GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01`.

Role : chantier parent doc-only de canonisation multi-agents.

Surface principale : `docs/chantiers/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01/`.

Branche support : `go/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01`.

## 6_FINAL_TARGET

Cible de phase courante : ouvrir le chantier proprement et poser une base documentaire autonome.

Livrables minimum de cette phase :

- `00_INITIAL_PROJECT_DOC.md` ;
- `BRANCH_STATE.md` ;
- entree d'indexation minimale ;
- point de reprise ;
- statut explicite : doc-only, aucune mutation runtime.

## 7_CANONICAL_STATE

Etat valide issu de la verification GitHub :

- le repo canonique est `magikgmo4-ui/opt-trading` ;
- la branche canonique de base est `sot/mainline` ;
- `workflow_ai/` existe a la racine ;
- `workflow_ai/WORKFLOW.md` est la doctrine canonique d'execution gatee ;
- `modules/validated_prompt_factory/` existe ;
- `modules/validated_prompt_factory/README.md` decrit le module et ses modes ;
- `docs/deploy_module_multi_machine_continuity.md` documente le standard multi-machine ;
- OpenClaw existe deja comme cible produit et modules partiels ;
- `docs/product_targets/OPENCLAW_TARGET_CANON.md` borne OpenClaw comme labo Linux cloisonne / provider experimental ;
- le dossier racine `/bundles/` n'est pas confirme comme surface trackee ;
- les bundles restent des supports secondaires de transfert, pas source de verite.

## 8_VALIDATED_PLAN

Plan valide immediat :

1. ouvrir branche dediee ;
2. creer le dossier chantier parent ;
3. documenter la reponse validee dans ce fichier autonome ;
4. poser `BRANCH_STATE.md` ;
5. indexer le chantier dans les surfaces actives minimales ;
6. ne pas modifier OpenClaw runtime ;
7. ne pas modifier configs live ;
8. ne pas ouvrir de strategie trading live ;
9. preparer ensuite une recherche approfondie a partir du socle etabli.

## 9_SELECTED_SOLUTION

Solution retenue : chantier parent doc-only dedie a la doctrine multi-agents, distinct des chantiers OpenClaw runtime.

OpenClaw est traite ici comme objet d'orchestration et de frontiere, pas comme chantier d'implementation runtime.

## 10_SELECTED_SETUP

Setup documentaire :

- branche : `go/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01` ;
- dossier : `docs/chantiers/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01/` ;
- source canonique de gouvernance : `docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md` ;
- references socle : `workflow_ai/WORKFLOW.md`, `modules/validated_prompt_factory/README.md`, `docs/deploy_module_multi_machine_continuity.md`, `docs/product_targets/OPENCLAW_TARGET_CANON.md`.

## 11_KEY_DECISIONS

- Ne pas reconstruire `workflow_ai` : il existe deja.
- Ne pas reconstruire `validated_prompt_factory` : il existe deja.
- Ne pas traiter `deploy_module_multi_machine` comme un agent IA : c'est un standard logistique.
- Ne pas promouvoir OpenClaw en runtime principal dans ce chantier.
- Utiliser OpenClaw comme orchestrateur experimental borne par la gouvernance.
- Integrer `frontmatter`, `topic_keys`, `search_tags`, naming et indexation dans la doctrine multi-agents.
- Garder ce chantier centre sur multi-agents, pas sur l'implementation OpenClaw runtime.

## 12_INVARIANTS

- Repo GitHub `opt-trading` reste source de verite.
- `workflow_ai` impose les gates.
- Prompt Factory produit les prompts ; il ne decide pas.
- `deploy_module_multi_machine` deploie seulement apres validation.
- OpenClaw reste cloisonne sur `db-layer` selon le canon actuel.
- Pas d'ouverture `tools/channels/nodes` dans ce chantier.
- Pas de trading live automatique.
- Pas de merge automatique Codex.
- Pas de refactor Claude global sans cadrage.
- Pas de runtime mutation dans cette phase.

## 13_ESTABLISHED

### Surfaces GitHub trouvees

| Surface | Statut | Role |
| --- | --- | --- |
| `workflow_ai/` | present | doctrine execution gatee |
| `modules/validated_prompt_factory/` | present | generation de prompts valides |
| `docs/deploy_module_multi_machine_continuity.md` | present | standard multi-machine |
| `docs/product_targets/OPENCLAW_TARGET_CANON.md` | present | cible canon OpenClaw bornee |
| `modules/menu_openclaw/` et modules voisins | presents | surfaces OpenClaw partielles |

### Lecture du socle valide

`workflow_ai/WORKFLOW.md` definit l'objectif de rendre le travail avec Cursor ou tout agent previsible, audit-able et controle par validation humaine `GO/STOP`.

Il positionne :

- `docs/master_pack/mission_starter_pack/00_mission_start_guide.md` comme point d'entree ;
- `workflow_ai/WORKFLOW.md` comme doctrine canonique ;
- `workflow_ai/templates/specs.md` et `workflow_ai/templates/tasks.md` comme templates ;
- `docs/ot/kanban/*` comme continuite ;
- `docs/ot/trae/08_MULTI_STEP_MISSION_CHECKLIST_V1.txt` comme modele de missions longues ;
- `modules/validated_prompt_factory/README.md` comme prompt generation ;
- `docs/deploy_module_multi_machine_continuity.md` comme deploiement multi-machine.

`validated_prompt_factory` transforme une synthese validee en prompt final specialise. Ses modes etablis sont :

- `chatgpt_session` ;
- `trae_module` ;
- `trae_patch` ;
- `bundle_transfer`.

`deploy_module_multi_machine` est le standard multi-machine valide sur `admin-trading`, avec cibles principales `student` et `db-layer`.

OpenClaw est actuellement documente comme labo Linux cloisonne et gouverne, couche experimentale / provider, non expose directement aux flux critiques.

## 14_HYPOTHESIS

Hypotheses a valider dans la phase de recherche suivante :

- des documents OpenClaw recents peuvent deja definir une partie de l'orchestration multi-agents ;
- des chantiers actifs peuvent deja porter des decisions sur tmux / OpenCode / OpenClaw runtime ;
- la matrice operationnelle peut exiger une surface dediee pour les agents, distincte des product targets ;
- le dossier `/bundles/` peut exister localement comme support non tracke, meme s'il n'est pas confirme dans GitHub.

Aucune de ces hypotheses ne doit etre transformee en decision sans preuve.

## 15_REMAINING_GAP

Gaps restants :

- lire plus profondement les docs OpenClaw liees a Hermes, menu, gateway, provider et config modulaire ;
- lire les docs Trae pack et les rapports Prompt Factory ;
- etablir la matrice `agent / skill / provider / orchestrateur / deployer / prompt generator` ;
- fixer les frontmatter types pour la doctrine multi-agents ;
- fixer les `search_tags` recommandes ;
- fixer la place dans `docs/governance`, `docs/architecture`, `docs/chantiers`, `docs/index`, `registry` si besoin ;
- preparer le plan complet ;
- preparer le bundle d'execution.

## 16_TODO

Prochains documents proposes dans ce chantier :

- `01_EXISTING_SOCLE_READOUT.md` ;
- `02_AGENT_SKILL_PROVIDER_MATRIX.md` ;
- `03_FRONTMATTER_SEARCH_TAGS_NAMING_DOCTRINE.md` ;
- `04_OPENCLAW_ORCHESTRATION_BOUNDARIES.md` ;
- `05_OPERATIONAL_MATRIX_INTEGRATION_PLAN.md` ;
- `06_EXECUTION_BUNDLE_PLAN.md` ;
- `90_CLOSEOUT.md` uniquement apres validation.

## 17_RESUME_POINT

Reprendre depuis ce fichier.

Etat courant : chantier parent ouvert sur branche dediee, base GitHub verifiee, socle existant reconnu, OpenClaw borne comme orchestrateur experimental/provider cloisonne, phase courante doc-only.

Prochaine action : affiner les recherches a partir du socle valide et produire `01_EXISTING_SOCLE_READOUT.md`, puis la matrice agents/skills/providers.

## 18_TO_DOCUMENT

TAGS a extraire pour documentation canonique future :

- `MULTI_AGENTS_CANON_PARENT`
- `WORKFLOW_AI_GATED_DOCTRINE`
- `VALIDATED_PROMPT_FACTORY_PROMPT_LAYER`
- `DEPLOY_MODULE_MULTI_MACHINE_LOGISTICS_LAYER`
- `OPENCLAW_ORCHESTRATOR_BOUNDARY`
- `AGENT_SKILL_PROVIDER_MATRIX`
- `FRONTMATTER_SEARCH_TAGS_NAMING`

## 19_TO_REMEMBER

Memory Bricks candidates, projet uniquement :

- `workflow_ai` = doctrine gatee pour tout agent ou IDE ;
- `validated_prompt_factory` = transformation de synthese validee en prompt specialise ;
- `deploy_module_multi_machine` = bras logistique multi-machine, pas agent IA ;
- OpenClaw = orchestrateur experimental/provider cloisonne, pas runtime principal ;
- la doctrine multi-agents doit integrer naming, frontmatter, search tags et indexation des le cadrage.
