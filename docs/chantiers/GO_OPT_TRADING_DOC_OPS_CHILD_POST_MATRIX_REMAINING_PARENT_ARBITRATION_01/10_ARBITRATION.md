---
doc_id: GO_OPT_TRADING_DOC_OPS_CHILD_POST_MATRIX_REMAINING_PARENT_ARBITRATION_01_ARBITRATION
doc_type: arbitration
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_DOC_OPS_CHILD_POST_MATRIX_REMAINING_PARENT_ARBITRATION_01
status: open
lifecycle_stage: arbitration
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-04-29
links:
  - docs/index/GO_INDEX.md
  - docs/index/GO_CLOSED_INDEX.md
  - docs/index/GO_PARENT_THREAD_MAP.md
  - docs/index/BRANCH_STATE.md
---

# 10_ARBITRATION

## Synthese

L'arbitrage confirme qu'aucun nouveau parent n'est requis pour couvrir les machines et surfaces restantes.
Les parents deja ouverts suffisent, a condition de :

- garder `db-layer`, `admin-trading`, `cursor-ai`, `fantome` et `student` chacun avec un principal distinct ;
- laisser `reseau_ssh`, `bundles`, `git progressive migration` et `runtime exception families` comme surfaces transverses ;
- ne pas rouvrir les familles fermees gouvernance / matrice / naming.

## Parents ouverts retenus

| Element | Preuve locale | Classification | Statut arbitre | Decision |
| --- | --- | --- | --- | --- |
| `GO_OPT_TRADING_MACHINE_DB_LAYER_PARENT_01` | `GO_INDEX.md`, dossier chantier present | parent machine, actif reel | prioritaire | garder comme principal `db-layer` |
| `GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01` | `GO_INDEX.md`, dossier chantier present | parent machine, actif reel, differe | utile | garder comme principal `admin-trading`, mais plus tard |
| `GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01` | `GO_INDEX.md`, dossier chantier present | parent projet, actif reel | utile | garder comme parent projet, ne pas absorber dans `db-layer` |
| `GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01` | `GO_INDEX.md`, `PARENT_STATE.md` | parent projet, transverse, actif reel | utile | garder comme principal `cursor-ai` |
| `GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01` | `GO_INDEX.md`, dossier chantier present | parent projet, actif reel | utile | garder comme principal `fantome` |
| `GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01` | `GO_INDEX.md`, dossier chantier present | parent runtime, actif reel | utile | garder comme parent runtime, ne pas absorber dans `db-layer` |
| `GO_OPT_TRADING_BUNDLES_REPO_STORAGE_PARENT_01` | branche distante + dossier prouve sur la branche | transverse, methode de travail, a consolider plus tard | ouvert hors index | garder hors sequence machine |
| `GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01` | branche distante + dossier prouve sur la branche | parent projet, differe | ouvert hors index | rattacher a `student`, ne pas prioriser maintenant |
| `GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01` | branche distante + dossier prouve sur la branche | parent runtime, a consolider plus tard | ouvert hors index | ne pas ouvrir maintenant |
| `GO_OPT_TRADING_STRICT_WORKERS_PARENT_01` | branche distante + closeout draft only prouve | parent projet, differe, a consolider plus tard | non canonise localement | consolider sous `GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01` |

## GO actifs et surfaces utiles

| Element | Preuve locale | Classification | Statut arbitre | Decision |
| --- | --- | --- | --- | --- |
| `GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03` | `GO_INDEX.md`, `GO_PARENT_THREAD_MAP.md` | transverse, actif reel | prioritaire | garder comme gate multi-machine avant `admin-trading` et `student` |
| `GO_OPT_TRADING_RESEAU_SSH_UNIFIED_MODULE_CADRAGE_01` | `GO_INDEX.md`, dossier chantier present | transverse, actif reel | subordonne | traiter dans le fil `reseau_ssh`, pas comme machine |
| `GO_LOCALCMS_FORMS_INTEGRATION_DOC_01` | `GO_INDEX.md`, dossier chantier present | projet, differe | secondaire | laisser sous le parent `GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01` |
| `GO_GIT_PROGRESSIVE_MIGRATION_START_13` | `GO_INDEX.md`, `ACTIVE_STREAMS.md` | methode de travail, actif reel | parallele | garder actif hors ordre machine principal |
| `GO_OPT_TRADING_RUNTIME_EXCEPTION_FAMILIES_01` | `GO_INDEX.md`, `ACTIVE_STREAMS.md` | transverse, actif reel | parallele | garder actif hors ordre machine principal |
| `GO_TMUX_IDE_OPT_TRADING_CADRAGE_01` | `GO_INDEX.md`, `ACTIVE_STREAMS.md` | methode de travail, actif reel | utile | rattacher au poste `cursor-ai` comme surface secondaire |

## Reference-only confirme

| Element | Classification | Decision |
| --- | --- | --- |
| `GO_UNIFORM_CONTINUITY_FINAL_MASTER_PLAN_01` | reference-only | conserver comme reference |
| `GO_EXTRACTEUR_TAGS_CANONICAL_METHOD_01` | reference-only | conserver comme reference |
| `GO_OPT_TRADING_UI_LOCALCMS_INVENTORY_01` | reference-only | ne pas reouvrir hors reprise explicite du parent LocalCMS |
| `GO_OPT_TRADING_UI_LOCALCMS_MATRIX_01` | reference-only | ne pas reouvrir hors reprise explicite du parent LocalCMS |
| `GO_OPT_TRADING_UI_LOCALCMS_CONTRACTS_01` | reference-only | ne pas reouvrir hors reprise explicite du parent LocalCMS |
| `GO_OPT_TRADING_UI_LOCALCMS_PILOT_READONLY_01` | reference-only | ne pas reouvrir hors reprise explicite du parent LocalCMS |
| `GO_TMUX_RUNTIME_CONVENTIONS_01` | reference-only | conserver sous le parent runtime OpenClaw |
| `GO_OPENCLAW_COMMAND_SCOPE_01` | reference-only | conserver sous le parent runtime OpenClaw |
| `GO_TMUX_RUNTIME_CONTRACT_01` | reference-only | conserver sous le parent runtime OpenClaw |
| `GO_TMUX_OPENCODE_OPENCLAW_MODES_01` | reference-only | conserver sous le parent runtime OpenClaw |
| `GO_RUNTIME_GUARDRAILS_01` | reference-only | conserver sous le parent runtime OpenClaw |

## GO fermes a ne pas rouvrir

| Element | Classification | Decision |
| --- | --- | --- |
| `GO_OPT_TRADING_MATRICE_DOC_OPS_PARENT_01` | GO ferme a ne pas rouvrir | ferme, hors perimetre |
| `GO_OPT_TRADING_MATRICE_GOUVERNANTE_CANONIZATION_01` | GO ferme a ne pas rouvrir | ferme, hors perimetre |
| `GO_OPT_TRADING_MATRICE_GOUVERNANTE_METADATA_DERIVATION_01` | GO ferme a ne pas rouvrir | ferme, hors perimetre |
| `GO_OPT_TRADING_PARENT_NAMING_CANON_01` | GO ferme a ne pas rouvrir | ferme, hors perimetre |
| `GO_OPT_TRADING_DOC_OPS_PARENT_PROJECT_MACHINE_SPLIT_01` | GO ferme a ne pas rouvrir | ferme, hors perimetre |
| `GO_OPT_TRADING_DOC_OPS_CHILD_PARENT_CONFORMITY_AUDIT_01` | GO ferme a ne pas rouvrir | ferme, hors perimetre |
| `GO_OPT_TRADING_CONTINUITY_INDEX_REALIGNMENT_01` | GO ferme a ne pas rouvrir | ferme, hors perimetre |
| `GO_OPT_TRADING_CANON_STRUCTURE_REALIGNMENT_01` | GO ferme a ne pas rouvrir | ferme, hors perimetre |

## GO orphelins bloquants

Verdict : `NON`

Raison retenue :

- `db-layer` a deja son parent machine ;
- `admin-trading` a deja son parent machine ;
- `cursor-ai` est couvert par `GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01` ;
- `fantome` est couvert par `GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01`, qui absorbe `strict workers` ;
- `student` a deja un meilleur candidat prouve avec `GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01`, mais il reste differe ;
- `bundles` et `OpenClaw orchestrator` sont des chantiers existants a consolider plus tard, pas des trous de gouvernance necessitant un nouveau parent.

## Verdict intermediaire

`PASS_DOC_ARBITRATION`

Le perimetre restant est couvert par les parents deja ouverts, avec quatre rattachements explicites a ne pas perdre :

- `bundles` = transverse / methode, hors chantier machine ;
- `strict workers` = a fondre sous `AI Team Architecture` ;
- `local Ollama` = `student`, differe ;
- `OpenClaw orchestrator` = a traiter apres clarification des GO OpenClaw deja actifs.
