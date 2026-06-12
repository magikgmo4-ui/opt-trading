---
doc_id: OPT_TRADING_MULTI_AGENTS_FRONTMATTER_SEARCH_TAGS_NAMING_DOCTRINE_01
doc_type: doctrine
repo: opt-trading
project: opt-trading
module: multi_agents
go_id: GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01
status: open
lifecycle_stage: doctrine
topic_keys:
  - opt-trading
  - multi_agents
  - frontmatter
  - search_tags
  - naming
  - indexation
  - governance
search_tags:
  - surface:chantier
  - doc_role:doctrine
  - governance:frontmatter
  - governance:search_tags
  - governance:naming
  - governance:indexation
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
point_de_reprise: "05_OPERATIONAL_MATRIX_INTEGRATION_PLAN.md"
updated_at: 2026-04-26
links:
  - docs/chantiers/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01/02_AGENT_SKILL_PROVIDER_MATRIX.md
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
  - docs/architecture/REPO_SURFACES_MAP.md
  - docs/index/GO_INDEX.md
  - docs/index/ACTIVE_STREAMS.md
  - docs/index/REPRISE.md
---

# 03_FRONTMATTER_SEARCH_TAGS_NAMING_DOCTRINE — Multi-agents

## 1. Objet

Canoniser la maniere de documenter les surfaces multi-agents dans `opt-trading`.

Ce document applique la matrice gouvernante au domaine :

- Codex ;
- Claude ;
- Trae ;
- Ollama / DeepSeek ;
- OpenClaw ;
- workflow_ai ;
- validated_prompt_factory ;
- deploy_module_multi_machine ;
- Hermes bridge.

## 2. Principe souverain

La matrice gouvernante reste superieure a cette doctrine.

Cette doctrine ne cree pas une matrice concurrente. Elle derive les regles applicables aux documents multi-agents.

Ordre d'arbitrage :

1. etat reel prouve du repo ;
2. `MATRICE_DOC_OPS_MASTER_MATRIX_01` ;
3. documents canoniques existants ;
4. dossier chantier multi-agents ;
5. search tags et derives.

## 3. Naming GO multi-agents

Forme canonique :

```text
GO_<SCOPE>_<PRODUCT_OR_SURFACE>_<ROLE>_<OBJECT>_<NN>
```

### Scope recommande

- `GO_OPT_TRADING` pour une doctrine repo-level ;
- `GO_OPENCLAW` uniquement pour un lot OpenClaw runtime ou module OpenClaw direct ;
- `GO_TRAE` uniquement pour une surface Trae dediee ;
- `GO_CODEX`, `GO_CLAUDE`, `GO_OLLAMA` seulement si le lot porte explicitement une integration dediee a cet outil.

### Product / surface recommande

Pour ce chantier :

```text
MULTI_AGENTS
```

Pour les lots derives possibles :

- `OPENCLAW` si runtime/config/provider OpenClaw ;
- `PROMPT_FACTORY` si module Prompt Factory ;
- `WORKFLOW_AI` si doctrine gates ;
- `DEPLOY_MULTI_MACHINE` si logistique de deploiement ;
- `TRAE` si cockpit/skills Trae.

### Role recommande

- `CANON` : doctrine canonique ;
- `PARENT` : parent structurel prouve ;
- `MATRIX` : matrice ;
- `PLAN` : plan ;
- `BUNDLE` : bundle d'execution ;
- `INTEGRATION` : integration bornee ;
- `READOUT` : lecture/synthese repo-first ;
- `BOUNDARY` : frontieres/perimetres ;
- `POLICY` : regles applicables.

## 4. Doc types recommandes

| Document | doc_type | Surface | Role |
| --- | --- | --- | --- |
| Initial project doc | `initial_project_doc` | chantier | figer la demande initiale et le plan parent |
| Socle readout | `socle_readout` | chantier | lecture repo-first des references existantes |
| Agent matrix | `matrix` | chantier ou architecture | separer roles et responsabilites |
| Doctrine | `doctrine` | chantier puis governance si promue | fixer regles derivees |
| Integration plan | `plan` | chantier | plan executable par phases |
| Bundle plan | `bundle_plan` | chantier | definir artefact transportable |
| Branch state | `branch_state` | chantier | trace Git locale |
| Index gap | `gap_indexation` | chantier | propagation restante explicite |
| Closeout | `closeout` | chantier | fermer et propager |

## 5. Frontmatter noyau obligatoire

Tout document multi-agents canonique doit contenir :

```yaml
doc_id:
doc_type:
repo: opt-trading
project: opt-trading
module:
go_id:
status:
lifecycle_stage:
topic_keys:
search_tags:
surface:
source_kind:
reference_canonique_principale:
point_de_reprise:
updated_at:
links:
```

## 6. Regles `topic_keys`

`topic_keys` portent la lecture stable.

Recommandes :

```yaml
topic_keys:
  - opt-trading
  - multi_agents
  - governance
  - workflow_ai
  - validated_prompt_factory
  - deploy_module_multi_machine
  - openclaw
  - codex
  - claude
  - trae
  - ollama
```

Selon le document, reduire aux termes reellement utiles. Ne pas bourrer les tags.

## 7. Regles `search_tags`

`search_tags` sont derives et legers. Ils ne remplacent pas `topic_keys`.

Formats recommandes :

```yaml
search_tags:
  - surface:chantier
  - doc_role:matrix
  - governance:multi_agents_doctrine
  - integration:workflow_ai
  - integration:validated_prompt_factory
  - integration:deploy_module_multi_machine
  - boundary:openclaw_orchestrator
  - provider:ollama
  - ide:trae
  - agent:codex
  - agent:claude
```

Regles :

- utiliser `key:value` ;
- eviter les phrases ;
- eviter les doublons avec `topic_keys` sauf besoin de recherche ;
- ne pas faire porter une decision par un tag ;
- ne jamais corriger une contradiction documentaire avec un tag.

## 8. Surfaces documentaires

| Type de contenu | Surface primaire | Surface secondaire |
| --- | --- | --- |
| chantier actif multi-agents | `docs/chantiers/<GO_ID>/` | `docs/index/*` |
| doctrine promue stable | `docs/governance/` | `docs/architecture/` |
| carte de roles | `docs/architecture/` si generalisee | chantier pendant cadrage |
| continuite active | `docs/index/` | dossier chantier |
| module runtime OpenClaw | `modules/*_openclaw/` | docs module |
| target produit OpenClaw/Ollama | `docs/product_targets/` | docs/status |
| bundles | support secondaire | jamais source de verite |
| registry derive | `registry/*` | jamais source souveraine |

## 9. Indexation minimale a l'ouverture

A l'ouverture d'un parent multi-agents :

- dossier chantier ;
- `00_INITIAL_PROJECT_DOC.md` ;
- `BRANCH_STATE.md` local si branche dediee ;
- entree dans `GO_INDEX.md` ou `GAP_INDEXATION.md` explicite ;
- `ACTIVE_STREAMS.md` si flux actif ;
- `NEXT_GO_CANDIDATES.md` si le parent entre dans les next actifs ;
- `REPRISE.md` si point de reprise utile.

## 10. Indexation minimale a la fermeture

A la fermeture :

- `90_CLOSEOUT.md` ;
- propagation `GO_INDEX` ;
- mise a jour `ACTIVE_STREAMS` ;
- mise a jour `NEXT_GO_CANDIDATES` ;
- mise a jour `REPRISE` ;
- decision sur branche ;
- decision sur promotion eventuelle vers `docs/governance` ou `docs/architecture`.

## 11. Doctrine des roles dans le frontmatter

Champ `module` recommande :

| Cas | module |
| --- | --- |
| doctrine transverse | `multi_agents` |
| OpenClaw direct | `openclaw` |
| Prompt Factory | `validated_prompt_factory` |
| workflow gates | `workflow_ai` |
| Trae skills | `trae` |
| Ollama / DeepSeek | `ollama` ou `deepseek_ollama` |
| deploy multi-machine | `deploy_module_multi_machine` |

## 12. Interdits

- pas de `GO_OPENCLAW` pour un document qui parle surtout de multi-agents generaux ;
- pas de `search_tags` comme source de verite ;
- pas de branche deduite sans `BRANCH_STATE` ;
- pas de bundle comme canon ;
- pas de skill presente comme agent ;
- pas de provider presente comme orchestrateur ;
- pas de deployer presente comme agent ;
- pas de Prompt Factory presente comme gouvernance.

## 13. Decision

Cette doctrine devient la base de travail du chantier parent.

Elle pourra etre promue plus tard vers `docs/governance/` ou `docs/architecture/` seulement apres closeout et validation.

## 14. Point de reprise

Prochain document : `05_OPERATIONAL_MATRIX_INTEGRATION_PLAN.md`.

## RISKS

- À qualifier.
