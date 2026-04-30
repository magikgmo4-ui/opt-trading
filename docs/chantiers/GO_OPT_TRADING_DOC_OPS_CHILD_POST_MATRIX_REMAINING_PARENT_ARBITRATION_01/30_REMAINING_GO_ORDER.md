---
doc_id: GO_OPT_TRADING_DOC_OPS_CHILD_POST_MATRIX_REMAINING_PARENT_ARBITRATION_01_GO_ORDER
doc_type: go_order
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
  - docs/index/ACTIVE_STREAMS.md
  - docs/index/NEXT_GO_CANDIDATES.md
---

# 30_REMAINING_GO_ORDER

## Validation globale

Ordre cible valide avec une correction de cadrage :

- `GO_OPT_TRADING_BUNDLES_REPO_STORAGE_PARENT_01` reste hors ordre principal machine, car il est transverse / methode ;
- `GO_OPT_TRADING_STRICT_WORKERS_PARENT_01` est absorbe dans l'etape `AI_TEAM_FANTOME_ALIGNMENT_01` ;
- `GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01` reste volontairement a la fin, apres clarification ou closeout des GO OpenClaw deja actifs.

## Ordre final recommande

| Ordre | GO recommande | Justification courte | Dependances |
| --- | --- | --- | --- |
| `1` | `GO_OPT_TRADING_DOC_OPS_CHILD_POST_MATRIX_REMAINING_PARENT_ARBITRATION_01` | figer l'arbitrage et la carte machine avant toute reprise | aucune |
| `2` | `GO_OPT_TRADING_MACHINE_DB_LAYER_PARENT_REVIEW_01` | `db-layer` est l'hote reel actuel et le meilleur point de reprise machine | sortie de l'arbitrage |
| `3` | `GO_OPT_TRADING_UI_LOCALCMS_DB_LAYER_CONSUMER_REALIGNMENT_01` | realigner l'usage `LocalCMS` sur l'hote reel sans absorber le parent projet | revue `db-layer` |
| `4` | `GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_DB_LAYER_REVIEW_01` | clarifier l'etat runtime OpenClaw sur l'hote reel courant sans reinventer une nouvelle architecture | revue `db-layer` |
| `5` | `GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_CLOSEOUT_01` | fermer le gate transverse avant d'ouvrir `admin-trading` ou `student` | clarification `db-layer` + OpenClaw runtime |
| `6` | `GO_OPT_TRADING_MULTI_AGENTS_CURSOR_AI_PARENT_ALIGNMENT_01` | redonner un principal unique et prioritaire au poste `cursor-ai` | SSH clarifie pour eviter l'empilement |
| `7` | `GO_OPT_TRADING_AI_TEAM_FANTOME_ALIGNMENT_01` | aligner `fantome` avec `AI Team` en absorbant `strict workers` | reprise `cursor-ai` posee |
| `8` | `GO_OPT_TRADING_MACHINE_ADMIN_TRADING_RUNTIME_INTEGRATION_REVIEW_01` | reprendre la machine trading reelle seulement apres clarification `db-layer` / OpenClaw / SSH | etapes `2` a `5` |
| `9` | `GO_OPT_TRADING_MACHINE_STUDENT_PARENT_REVIEW_LATER_01` | rouvrir `student` seulement comme lab differe, avec `local Ollama` | etapes `2` a `6` minimales |
| `10` | `GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01` | ne traiter le parent orchestrateur qu'apres clarification des GO OpenClaw existants | etape `4` au minimum, idealement `4` + `5` |

## Actifs reels hors ordre principal

| Element | Statut retenu | Pourquoi hors ordre principal |
| --- | --- | --- |
| `GO_OPT_TRADING_BUNDLES_REPO_STORAGE_PARENT_01` | transverse, methode de travail, a consolider plus tard | utile pour les bundles et la reprise Ollama, mais pas un principal machine |
| `GO_GIT_PROGRESSIVE_MIGRATION_START_13` | actif reel | flux de methode a garder vivant sans l'injecter dans l'arbitrage machine |
| `GO_OPT_TRADING_RUNTIME_EXCEPTION_FAMILIES_01` | actif reel | flux transverse runtime, pas un parent machine |
| `GO_LOCALCMS_FORMS_INTEGRATION_DOC_01` | differe | reste un sous-sujet du parent `GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01` |

## Differes explicites

- `GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01` : differe mais non abandonne.
- `GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01` : differe sur `student`.
- `GO_OPT_TRADING_STRICT_WORKERS_PARENT_01` : differe comme branche autonome, absorbe sous `AI Team`.

## Elements a consolider plus tard

- `GO_OPT_TRADING_BUNDLES_REPO_STORAGE_PARENT_01`
- `GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01`
- toute repropagation index canonique des branches hors index, seulement si la reprise effective de ces parents redevient prioritaire

## Next GO recommande

`GO_OPT_TRADING_MACHINE_DB_LAYER_PARENT_REVIEW_01`
