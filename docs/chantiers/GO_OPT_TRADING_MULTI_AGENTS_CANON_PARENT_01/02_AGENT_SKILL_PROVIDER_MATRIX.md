---
doc_id: OPT_TRADING_MULTI_AGENTS_AGENT_SKILL_PROVIDER_MATRIX_01
doc_type: matrix
repo: opt-trading
project: opt-trading
module: multi_agents
go_id: GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01
status: open
lifecycle_stage: matrix
topic_keys:
  - opt-trading
  - multi_agents
  - agents
  - skills
  - providers
  - orchestrator
  - codex
  - claude
  - trae
  - ollama
  - openclaw
search_tags:
  - surface:chantier
  - doc_role:agent_skill_provider_matrix
  - governance:multi_agents_doctrine
  - boundary:openclaw_orchestrator
  - provider:ollama
  - ide:trae
  - agent:codex
  - agent:claude
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
point_de_reprise: "03_FRONTMATTER_SEARCH_TAGS_NAMING_DOCTRINE.md"
updated_at: 2026-04-26
links:
  - docs/chantiers/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01/01_EXISTING_SOCLE_READOUT.md
  - docs/ot/trae/04_SKILLS_V1.txt
  - docs/ot/trae/08_MULTI_STEP_MISSION_CHECKLIST_V1.txt
  - workflow_ai/WORKFLOW.md
  - modules/validated_prompt_factory/README.md
  - docs/deploy_module_multi_machine_continuity.md
  - docs/product_targets/OPENCLAW_TARGET_CANON.md
  - docs/product_targets/DEEPSEEK_OLLAMA_TARGET_CANON.md
  - modules/menu_openclaw/docs/GO_OPENCLAW_CHAIN_03.md
  - modules/model_provider_openclaw/docs/GO_OPENCLAW_PROVIDER_POLICY_04.md
---

# 02_AGENT_SKILL_PROVIDER_MATRIX — Multi-agents

## 1. Objet

Fixer une matrice claire entre :

- agents ;
- skills ;
- providers ;
- orchestrateurs ;
- deployers ;
- prompt generators ;
- bridges.

But : eviter la confusion entre un agent autonome, un skill borne, un modele local, un orchestrateur experimental, un module logistique et une doctrine de gouvernance.

## 2. Definitions canoniques

| Type | Definition | Exemple repo |
| --- | --- | --- |
| Agent | entite qui porte une mission ou une partie de mission | Codex, Claude, agent OpenClaw `builder` |
| Skill | operation repetable, bornee, a input/output fixe | Trae `classify_mission`, `extract_established_state` |
| Provider | source de modele ou backend d'inference | Ollama, OpenRouter, OpenAI compatible local |
| Orchestrateur | routeur de missions/capacites sous garde-fous | OpenClaw, ChatGPT gouvernance session |
| Deployer | outil logistique de transfert/deploiement | deploy_module_multi_machine |
| Prompt generator | transforme synthese validee en prompt executable | validated_prompt_factory |
| Doctrine | regles souveraines de conduite et validation | workflow_ai, matrice gouvernante |
| Bridge | liaison bornee entre deux surfaces | Hermes -> OpenClaw -> validation -> repo |

## 3. Matrice principale

| Surface | Type canonique | Role valide | Entree | Sortie | Limite |
| --- | --- | --- | --- | --- | --- |
| ChatGPT | Orchestrateur gouvernance session | cadrage, arbitrage, synthese, plans | demande utilisateur + repo/docs | decisions, GO, docs, prompts | ne remplace pas repo ni preuves runtime |
| `workflow_ai` | Doctrine | gates, GO/STOP, backup, closeout | mission | parcours controle | ne produit pas le patch seul |
| Codex | Agent GitHub | branches, PR, diffs, corrections paralleles | prompt borne + repo | diff/PR/rapport | pas merge auto, pas gouvernance finale |
| Claude | Agent local profond | lecture repo, patch local, refactor borne, docs | prompt borne + repo local | modifications locales + rapport | pas refactor global sans GO |
| Trae | IDE / cockpit mission | appliquer workflow, conduire missions, utiliser skills | prompt structure + repo | patch/doc/report | pas runtime bot libre |
| Trae skills | Skills | operations repetees et bornees | inputs explicites | outputs fixes | ne portent pas une mission entiere |
| Ollama / DeepSeek | Provider local | inference locale, sandbox, fallback | prompt/API HTTP | reponse modele locale | learning-only, pas decision autonome |
| OpenClaw | Orchestrateur experimental / provider layer | router agents/providers/chaine locale | consigne bornee | execution/etat/preuve | pas runtime principal non controle |
| model_provider_openclaw | Policy provider | valider agents -> providers/modeles/limites | YAML/policy | status/export JSON | ne modifie pas config live seul |
| gateway_openclaw | Gateway local | pilotage loopback local | commande OpenClaw bornee | gateway/status | pas exposition large |
| evidence_openclaw | Evidence exporter | produire preuves relisibles | runtime existant | docs_evidence | pas mutation runtime |
| deploy_module_multi_machine | Deployer | plan/preflight/deploy entre machines | module + cible | deploy + preuve | pas agent IA ni decision |
| validated_prompt_factory | Prompt generator | prompt specialise depuis synthese validee | synthese structuree | prompt mode | pas arbitrage projet final |
| Hermes bridge | Bridge experimental | generation -> execution bornee -> validation | script/patch borne | artefact + observation | pas auto-commit |

## 4. Codex

### Role retenu

Codex est l'agent GitHub parallele.

Usages recommandes :

- ouvrir ou travailler sur branches isolees ;
- produire PR/diff ;
- faire corrections ciblees ;
- comparer approches ;
- fournir revue de code ;
- executer lots GitHub bornes.

### Interdits

- merge automatique ;
- decision finale de gouvernance ;
- refactor global sans GO ;
- mutation runtime OpenClaw ;
- trading live.

## 5. Claude

### Role retenu

Claude est l'agent local profond.

Usages recommandes :

- lecture repo locale complete ;
- sous-agents specialises ;
- analyse longue ;
- patch minimal ;
- documentation operatoire ;
- tests locaux.

### Interdits

- refactor global par defaut ;
- mutation multi-surface sans GO ;
- suppression/reclassement massif sans closeout ;
- execution runtime non reversible.

## 6. Trae

### Role retenu

Trae est le cockpit IDE et la surface skills la plus proche du workflow existant.

Le canon Trae etabli que :

- les agents portent la mission ;
- les skills portent les operations ;
- un skill ne doit pas devenir faux agent ou gouvernance concurrente.

### Usages recommandes

- appliquer Prompt Socle Workflow ;
- utiliser Prompt Factory ;
- produire patchs Trae ;
- conduire missions multi-etapes ;
- generer rapports standardises ;
- produire ou consommer bundles.

## 7. Ollama / DeepSeek

### Role retenu

Ollama / DeepSeek est provider local et couche cognitive locale.

Usages recommandes :

- inference locale ;
- analyse learning-only ;
- fallback modele ;
- API HTTP `/api/chat` ;
- tests sur `student` ;
- sandbox privee.

### Interdits

- decision autonome de trading ;
- gouvernance projet ;
- merge Git ;
- orchestration multi-machine ;
- execution live non validee.

## 8. OpenClaw

### Role retenu

OpenClaw est orchestrateur experimental borne et provider layer local.

Il peut coordonner :

- agents definis ;
- providers autorises ;
- gateway local ;
- evidence ;
- configuration modulaire ;
- bridges bornes.

### Frontiere

OpenClaw ne remplace pas :

- `workflow_ai` ;
- matrice gouvernante ;
- Prompt Factory ;
- deploy multi-machine ;
- validation humaine ;
- repo source of truth.

## 9. Mapping OpenClaw agents

| Agent OpenClaw | Role possible | Provider policy | Equivalent externe |
| --- | --- | --- | --- |
| `orchestrateur` | route mission locale bornee | provider autorise + limites | ChatGPT gouvernance / Trae mission driver |
| `builder` | generation patch/script borne | provider autorise + fallback | Claude/Codex selon contexte |
| `reviewer` | verification scope/preuve | provider autorise + limites strictes | Claude review / Codex review |
| `lab` | experimentation locale | provider local ou fallback | Ollama sandbox |
| `codexoauth` | integration Codex/OAuth observee | a qualifier | Codex bridge potentiel |

## 10. Sequence multi-agents recommandee

1. ChatGPT ou gouvernance cadre le GO.
2. `workflow_ai` impose gates et GO/STOP.
3. Prompt Factory genere le prompt specialise.
4. Trae / Claude / Codex execute selon le role.
5. OpenClaw orchestre seulement si la mission est locale, bornee et controlee.
6. Ollama sert de provider local si besoin, jamais comme decisionnaire.
7. Evidence / report / closeout documentent la preuve.
8. Deploy multi-machine intervient seulement si un deploiement est valide.

## 11. Decision

La doctrine multi-agents doit utiliser cette separation comme base canonique :

```text
Doctrine != Agent != Skill != Provider != Orchestrateur != Deployer != Prompt Generator != Bridge
```

## 12. Point de reprise

Prochain document : `03_FRONTMATTER_SEARCH_TAGS_NAMING_DOCTRINE.md`.
