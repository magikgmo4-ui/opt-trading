---
doc_id: OPT_TRADING_MULTI_AGENTS_EXISTING_SOCLE_READOUT_01
doc_type: socle_readout
repo: opt-trading
project: opt-trading
module: multi_agents
go_id: GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01
status: open
lifecycle_stage: readout
topic_keys:
  - opt-trading
  - multi_agents
  - workflow_ai
  - validated_prompt_factory
  - deploy_module_multi_machine
  - openclaw
  - hermes
  - trae
  - ollama
search_tags:
  - surface:chantier
  - doc_role:socle_readout
  - integration:workflow_ai
  - integration:validated_prompt_factory
  - integration:deploy_module_multi_machine
  - integration:openclaw
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
point_de_reprise: "02_AGENT_SKILL_PROVIDER_MATRIX.md"
updated_at: 2026-04-26
links:
  - docs/chantiers/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01/00_INITIAL_PROJECT_DOC.md
  - workflow_ai/WORKFLOW.md
  - modules/validated_prompt_factory/README.md
  - docs/deploy_module_multi_machine_continuity.md
  - docs/product_targets/OPENCLAW_TARGET_CANON.md
  - docs/product_targets/DEEPSEEK_OLLAMA_TARGET_CANON.md
  - docs/hermes/HERMES_OPENCLAW_BRIDGE_RUNBOOK_V1.md
  - docs/hermes/03_bridge_openclaw.md
  - modules/menu_openclaw/docs/GO_OPENCLAW_CHAIN_03.md
  - modules/model_provider_openclaw/docs/GO_OPENCLAW_PROVIDER_POLICY_04.md
  - docs/ot/trae/04_SKILLS_V1.txt
  - docs/ot/trae/08_MULTI_STEP_MISSION_CHECKLIST_V1.txt
---

# 01_EXISTING_SOCLE_READOUT — Multi-agents

## 1. Objet

Documenter le socle existant a partir du repo, sans reconstruire les briques deja presentes.

Ce readout sert de base pour la matrice multi-agents et pour la doctrine frontmatter / search tags / naming.

## 2. Sources lues

### Gouvernance

- `docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md`
- role : matrice souveraine pour placement documentaire, naming, frontmatter, indexation, branche, propagation.

### Workflow AI

- `workflow_ai/WORKFLOW.md`
- role : doctrine gatee pour tout agent ou IDE.
- etat etabli : travail previsible, audit-able, controle par validation humaine `GO/STOP`.
- chaine de responsabilite : Orchestrator / Executor / Reviewer.
- gates : cadre, source de verite, plan, backup, implementation incrementale, cloture doc + kanban + reprise.

### Validated Prompt Factory

- `modules/validated_prompt_factory/README.md`
- role : transformer une synthese validee en prompt specialise.
- modes etablis : `chatgpt_session`, `trae_module`, `trae_patch`, `bundle_transfer`.
- posture obligatoire : proposer les roles, exemples de sortie, recommander posture, puis demarrer.
- statut : module existant, non a reconstruire.

### Deploy Module Multi Machine

- `docs/deploy_module_multi_machine_continuity.md`
- role : standard logistique multi-machine.
- orchestrateur : `admin-trading`.
- cibles primaires : `student`, `db-layer`.
- capacites confirmees : `status`, `plan`, `preflight`, `deploy`, `--post-install`, menu/CLI, run_id, lock distant, cleanup explicite.
- statut : bras de deploiement, pas agent IA.

### OpenClaw / Hermes

- `docs/product_targets/OPENCLAW_TARGET_CANON.md`
- `docs/hermes/03_bridge_openclaw.md`
- `docs/hermes/HERMES_OPENCLAW_BRIDGE_RUNBOOK_V1.md`
- `modules/menu_openclaw/docs/GO_OPENCLAW_CHAIN_03.md`
- `modules/model_provider_openclaw/docs/GO_OPENCLAW_PROVIDER_POLICY_04.md`
- `modules/evidence_openclaw/docs/GO_OPENCLAW_EVIDENCE_01.md`
- `modules/evidence_openclaw/docs/GO_OPENCLAW_SYNC_02.md`
- `modules/openclaw_config_modulaire/app/openclaw_root_template.json5`

Etat etabli :

- OpenClaw est un labo Linux cloisonne et gouverne.
- Role systeme : couche experimentale / provider.
- Pas produit user-facing.
- Pas runtime principal.
- Pas systeme ouvert non controle.
- Le bridge Hermes -> OpenClaw -> validation -> repo est borne.
- Pas d'auto-commit.
- Pas d'execution non controlee.
- Validation humaine obligatoire.
- La chaine operateur standard OpenClaw comprend : `install_module_openclaw`, `openclaw_config_modulaire`, `gateway_openclaw`, `configure_openclaw`, `doctor_openclaw`, `evidence_openclaw`.
- `model_provider_openclaw` est la couche de policy provider/model en amont.
- La config root template garde le gateway en mode local / loopback / token.

### Trae

- `docs/ot/trae/04_SKILLS_V1.txt`
- `docs/ot/trae/08_MULTI_STEP_MISSION_CHECKLIST_V1.txt`

Etat etabli :

- Les agents portent la mission.
- Les skills portent les operations.
- Un skill ne doit pas devenir faux agent, mission entiere deguisee ou gouvernance concurrente.
- Une mission multi-etapes exige but, inputs, sortie attendue, emplacement, portee machine, preuve minimale, statut.

### Ollama / DeepSeek

- `docs/product_targets/DEEPSEEK_OLLAMA_TARGET_CANON.md`

Etat etabli :

- Role systeme : couche cognitive locale.
- Acces privilegie : API HTTP `/api/chat` et hub/menu unifie.
- Validation externe obligatoire.
- Learning-only, pas decision autonome.
- Ne devient pas systeme autonome de trading ni decisionnaire final.

## 3. Socle transverse etabli

Le repo possede deja quatre briques structurantes :

1. `workflow_ai` : doctrine de conduite gatee.
2. `validated_prompt_factory` : generation standardisee de prompts.
3. `deploy_module_multi_machine` : logistique de deploiement multi-machine.
4. `OpenClaw` : orchestrateur/provider experimental cloisonne, deja borne par doc.

Ces briques doivent etre alignees, pas reconstruites.

## 4. Lecture par roles

| Role canonique | Surface existante | Fonction |
| --- | --- | --- |
| Gouvernance | `MATRICE_DOC_OPS_MASTER_MATRIX_01` | regles souveraines |
| Doctrine d'execution | `workflow_ai` | gates et GO/STOP |
| Prompt generator | `validated_prompt_factory` | prompts specialises |
| Deployer | `deploy_module_multi_machine` | deploiement multi-machine |
| Orchestrateur experimental | OpenClaw | gateway/provider/chaine bornee |
| Agent IDE / skills | Trae | conduite mission + operations repetees |
| Provider local | Ollama / DeepSeek | inference locale controlee |
| Bridge experimental | Hermes -> OpenClaw | generation/execution bornee avec validation |

## 5. Decisions de canonisation

- La doctrine multi-agents doit etre subordonnee a la matrice gouvernante.
- Les documents multi-agents nouveaux doivent porter frontmatter complet.
- Les `search_tags` doivent rester derives et ne pas remplacer `topic_keys`.
- Les agents, skills, providers, orchestrateurs et deployers doivent etre separes.
- OpenClaw ne doit pas absorber `workflow_ai`, Prompt Factory ou deploy multi-machine.
- Les chantiers OpenClaw runtime existants ne doivent pas etre reouverts par ce chantier.

## 6. Gaps restants

- produire la matrice agents/skills/providers ;
- formaliser la doctrine frontmatter/search_tags/naming ;
- definir le plan complet d'integration ;
- preparer un bundle d'execution doc-only ;
- propager l'indexation globale avec prudence.

## 7. Point de reprise

Prochain fichier : `02_AGENT_SKILL_PROVIDER_MATRIX.md`.
