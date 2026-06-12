---
doc_id: OPT_TRADING_MULTI_AGENTS_OPERATIONAL_MATRIX_INTEGRATION_PLAN_01
doc_type: plan
repo: opt-trading
project: opt-trading
module: multi_agents
go_id: GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01
status: open
lifecycle_stage: plan
topic_keys:
  - opt-trading
  - multi_agents
  - operational_matrix
  - governance
  - integration_plan
  - openclaw
  - workflow_ai
  - validated_prompt_factory
search_tags:
  - surface:chantier
  - doc_role:plan
  - governance:operational_matrix
  - integration:multi_agents
  - boundary:openclaw_orchestrator
  - execution:doc_only
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
point_de_reprise: "06_EXECUTION_BUNDLE_PLAN.md"
updated_at: 2026-04-26
links:
  - docs/chantiers/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01/00_INITIAL_PROJECT_DOC.md
  - docs/chantiers/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01/01_EXISTING_SOCLE_READOUT.md
  - docs/chantiers/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01/02_AGENT_SKILL_PROVIDER_MATRIX.md
  - docs/chantiers/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01/03_FRONTMATTER_SEARCH_TAGS_NAMING_DOCTRINE.md
  - docs/chantiers/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01/GAP_INDEXATION.md
---

# 05_OPERATIONAL_MATRIX_INTEGRATION_PLAN — Multi-agents

## 1. Objectif

Etablir le plan complet pour integrer la doctrine multi-agents dans la gouvernance et l'operationnel `opt-trading`, sans implementation runtime.

Ce plan reste doc-only.

## 2. Direction retenue

La doctrine multi-agents doit devenir une couche de methode et d'orchestration, pas un produit runtime autonome.

Elle doit relier :

- `MATRICE_DOC_OPS_MASTER_MATRIX_01` ;
- `workflow_ai` ;
- `validated_prompt_factory` ;
- `deploy_module_multi_machine` ;
- Trae skills ;
- Codex / Claude comme agents ;
- Ollama comme provider local ;
- OpenClaw comme orchestrateur experimental borne ;
- Hermes bridge comme flux experimental avec validation humaine.

## 3. Phases du plan

### Phase A — Ancrage parent

Statut : DONE partiel.

Livrables :

- branche dediee ;
- dossier chantier ;
- `00_INITIAL_PROJECT_DOC.md` ;
- `BRANCH_STATE.md` local ;
- `GAP_INDEXATION.md` ;
- surface globale `docs/index/BRANCH_STATE.md` creee, avec frontmatter a corriger si outil l'autorise dans un lot futur.

### Phase B — Lecture du socle

Statut : DONE.

Livrable :

- `01_EXISTING_SOCLE_READOUT.md`.

Sources lues :

- gouvernance ;
- workflow_ai ;
- validated_prompt_factory ;
- deploy_module_multi_machine ;
- OpenClaw / Hermes ;
- Trae ;
- Ollama / DeepSeek.

### Phase C — Matrice agents / skills / providers

Statut : DONE.

Livrable :

- `02_AGENT_SKILL_PROVIDER_MATRIX.md`.

Decision cle :

```text
Doctrine != Agent != Skill != Provider != Orchestrateur != Deployer != Prompt Generator != Bridge
```

### Phase D — Doctrine metadata / naming / indexation

Statut : DONE.

Livrable :

- `03_FRONTMATTER_SEARCH_TAGS_NAMING_DOCTRINE.md`.

Couvre :

- GO naming ;
- `doc_type` ;
- frontmatter noyau ;
- `topic_keys` ;
- `search_tags` ;
- surfaces documentaires ;
- indexation ouverture/fermeture ;
- interdits.

### Phase E — Propagation index globale

Statut : PARTIAL.

Travaux faits :

- `GAP_INDEXATION.md` detaille la propagation attendue ;
- `docs/index/BRANCH_STATE.md` cree comme nouvelle surface globale.

Gap restant :

- frontmatter du `docs/index/BRANCH_STATE.md` a une indentation a corriger ;
- `GO_INDEX.md`, `NEXT_GO_CANDIDATES.md`, `ACTIVE_STREAMS.md`, `REPRISE.md` doivent etre patches proprement dans un lot controle, idealement localement, pour eviter troncature.

Decision de prudence :

- ne pas patcher les gros index via contenu tronque ;
- documenter le gap et le traiter dans le bundle d'execution.

### Phase F — Bundle d'execution

Statut : TODO.

Livrable :

- `06_EXECUTION_BUNDLE_PLAN.md` ;
- bundle zip local a produire par IDE ou machine cible a partir du dossier chantier.

### Phase G — Promotion canonique eventuelle

Statut : FUTURE.

Conditions :

- closeout parent PASS ;
- index globaux alignes ;
- pas de contradiction avec les chantiers OpenClaw runtime ;
- validation humaine.

Promotion possible :

- une version stable dans `docs/governance/` si doctrine souveraine ;
- une carte dans `docs/architecture/` si vue de surface ;
- maintien dans `docs/chantiers/` si doctrine encore en cadrage.

## 4. Matrice operationnelle cible

| Couche | Surface | Statut cible | Role |
| --- | --- | --- | --- |
| Gouvernance | `docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md` | reference | regle souveraine |
| Execution gates | `workflow_ai/WORKFLOW.md` | reference | GO/STOP et gates |
| Prompting | `modules/validated_prompt_factory/` | actif | generation de prompts |
| IDE/skills | `docs/ot/trae/` | reference / support | skills et missions multi-etapes |
| Agents cloud/local | Codex / Claude | externe controle | execution bornee |
| Provider local | Ollama / DeepSeek | support | inference locale learning-only |
| Orchestrateur experimental | OpenClaw | borne | provider/gateway/chaine locale |
| Deploiement | `deploy_module_multi_machine` | actif | transfert multi-machine valide |
| Continuité | `docs/index/*` | active | reprise et flux |
| Chantiers | `docs/chantiers/<GO_ID>/` | actif | preuves locales |

## 5. Regles d'execution

- chaque etape doit produire un document ou une mise a jour documentee ;
- chaque commit doit rester lisible et borne ;
- aucune mutation runtime ;
- aucune config live OpenClaw ;
- aucun trading live ;
- aucun merge automatique ;
- aucun skill promu agent ;
- aucun provider promu orchestrateur ;
- aucun bundle promu source canonique.

## 6. Plan de propagation index

### Lot E1 — Branch state

- corriger `docs/index/BRANCH_STATE.md` frontmatter ;
- conserver entree branche actuelle ;
- ajouter lien depuis surfaces de reprise si necessaire.

### Lot E2 — GO_INDEX

- ajouter l'entree parent ;
- garder statut `OPEN` ;
- pointer vers `00_INITIAL_PROJECT_DOC.md`, `BRANCH_STATE.md`, `GAP_INDEXATION.md`.

### Lot E3 — ACTIVE_STREAMS

- ajouter flux actif multi-agents ;
- priorite recommandee : P1 ;
- next action : finaliser bundle et indexation.

### Lot E4 — NEXT_GO_CANDIDATES

- ajouter parent avec next primaire `aucun nouveau GO` ;
- next action : `06_EXECUTION_BUNDLE_PLAN.md` puis closeout ou propagation.

### Lot E5 — REPRISE

- ajouter entree de reprise avec etat etabli, gap restant, next action.

## 7. Plan de bundle

Le bundle d'execution doit contenir :

- tous les documents du chantier ;
- prompt d'execution ;
- liste de commandes Git locales ;
- checklist de validation ;
- instructions de patch index global ;
- hors-scope runtime ;
- point de reprise.

## 8. Critere de PASS futur

Le chantier parent pourra etre clos PASS si :

- socle lu et documente ;
- matrice agents/skills/providers posee ;
- doctrine frontmatter/search_tags/naming posee ;
- indexation globale alignee ou gap explicitement reporte ;
- bundle d'execution prepare ;
- aucune mutation runtime ;
- aucune contradiction avec OpenClaw target canon ;
- point de reprise clair.

## 9. Point de reprise

Prochain document : `06_EXECUTION_BUNDLE_PLAN.md`.

## RISKS

- À qualifier.
