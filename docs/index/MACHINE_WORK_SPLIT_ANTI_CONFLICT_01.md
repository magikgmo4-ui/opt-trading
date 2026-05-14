---
doc_id: OPT_TRADING_MACHINE_WORK_SPLIT_ANTI_CONFLICT_01
doc_type: index
repo: opt-trading
project: opt-trading
status: reference
lifecycle_stage: continuity_index
topic_keys:
  - machines
  - routing
  - anti-collision
  - branches
  - continuity
  - work_split
surface: index
source_kind: canonical
updated_at: 2026-05-14
links:
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
  - docs/index/BRANCH_STATE.md
  - docs/index/BRANCH_PROJECT_MAP.md
  - docs/index/GO_INDEX.md
  - docs/index/ACTIVE_STREAMS.md
---

# MACHINE_WORK_SPLIT_ANTI_CONFLICT_01

## Objet

Vue de routage machine anti-conflit du repo `opt-trading`.

Elle sert a :
- repondre aux demandes `chantiers pour <machine>` sans rearbitrage complet ;
- eviter les collisions Git entre machines ;
- distinguer les chantiers actifs des archives et des PASS historiques.

## Sources de verite

Cette fiche est subordonnee a :
- `docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md`
- `docs/index/GO_INDEX.md`
- `docs/index/ACTIVE_STREAMS.md`
- `docs/index/BRANCH_STATE.md`
- `docs/index/GO_CLOSED_INDEX.md`

La source canonique de statut branche reste `BRANCH_STATE.md`.
La source canonique des chantiers non clos reste `GO_INDEX.md`.

## Regle de routage

- `chantiers pour cursor-ai` => bloc **CURSOR_AI**
- `chantiers pour admin-trading` => bloc **ADMIN_TRADING**
- `chantiers pour db-layer` => bloc **DB_LAYER**
- `chantiers pour student` => bloc **STUDENT / OLLAMA**
- `chantiers pour fantome` => bloc **FANTOME**

## Regle de maintenance

- toute branche rattachee a une machine doit etre ajoutee dans le bloc correspondant ;
- toute suppression executee et tracee dans `BRANCH_STATE.md` doit etre reportee ici ;
- une branche Git ne prouve pas seule un chantier actif ;
- les GO `CLOSED` / `PASS` ne doivent pas rester dans un bloc machine comme chantiers actifs ;
- quand une chaine machine passe `CLOSED_FINAL`, ne garder que les archives/references et les reprises explicitement prouvees.

---

## Bloc CURSOR_AI

### DOC_OPS — WHY_LAYER_ACTIVE

| Branche / GO | Statut | Note |
| --- | --- | --- |
| `go/GO_OPT_TRADING_CURSOR_AI_DOC_OPS_CHILD_WHY_LAYER_AUDIT_01` | ACTIVE | WHY layer audit doc-only ; aucun runtime |
| `GO_OPT_TRADING_CURSOR_AI_OBSERVER_TRADINGVIEW_MCP_ALERT_WEBHOOK_APPLICATION_ACTIVE_01` | ACTIVE_CONTINUITY | Application alert webhook non fermee |
| `go/GO_OPT_TRADING_DOC_OPS_CHILD_OPEN_WORK_CONTROL_01` | BLOCKED | Delta `reseau_ssh` non merge ; conserver sous revue |

### References / historique cursor-ai

| Famille | Statut | Note |
| --- | --- | --- |
| TradingView MCP Observer | CLOSED | Parents/transport/docs merges ou supprimes selon closeout |
| Bundles / Claude cowork / live artifacts | MERGED / REFERENCE | Gardes comme contexte documentaire, pas comme nouveaux GO actifs |
| Branch audits `REMAINING_*` | REFERENCE | References d'audit Git |

---

## Bloc ADMIN_TRADING

| Branche / GO | Statut | Note |
| --- | --- | --- |
| `GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01` | OPEN | Parent machine admin-trading dans `GO_INDEX.md` |
| `go/GO_OPT_TRADING_ADMIN_TRADING_*` | ACTIVE / REVIEW | Surface la plus active : runtime, paper, Desk Pro, webhook, Telegram, guards |
| `go/GO_TRADING_PIPELINE_BOTPRESS_OPERATOR_PARENT_01` | REVIEW | Pipeline Botpress operator parent |
| `go/GO_OPT_TRADING_STRATEGY_INDICATOR_PARENT_01` | REVIEW | Strategy indicator parent |
| `go/GO_OPT_TRADING_WEB3_DATA_ADAPTERS_AUDIT_01` | REVIEW | Web3 data adapters audit |
| `go/GO_SKYAI_COMPETITORS_WEB3_AI_DATA_01` | REVIEW | SKYAI competitors Web3 AI data |

Point de reprise : recroiser avec `GO_INDEX.md`, `ACTIVE_STREAMS.md` et `BRANCH_STATE.md` avant tout GO runtime.

---

## Bloc DB_LAYER

| Branche / GO | Statut | Note |
| --- | --- | --- |
| `GO_OPT_TRADING_MACHINE_DB_LAYER_PARENT_01` | OPEN | Parent machine db-layer dans `GO_INDEX.md` |
| `GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01` | OPEN | Parent OpenClaw conserve comme ancre db-layer |
| `go/GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_DB_LAYER_CLOSEOUT_01` | CLOSED / REFERENCE | Runtime tmux ferme ; ne pas rouvrir sans GO cible |
| `go/GO_OPENCLAW_STATE_DIR_REPAIR_10` | REVIEW | State dir repair |
| `doc/GO_OPENCLAW_INFRA_BASELINE_01` | REVIEW | Infra baseline |
| `go/GO_OPT_TRADING_AIRTABLE_ORCHESTRATION_PARENT_01` | REVIEW | Airtable orchestration parent |
| `go/GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01` | REVIEW | Repo KG parent graph system |
| `go/GO_OPT_TRADING_REPO_SURFACES_PARENT_CARTOGRAPHY_01` | REVIEW | Repo surfaces parent cartography |

---

## Bloc STUDENT / OLLAMA

### Etat canonique

```text
STUDENT_OLLAMA_AGENT:
  final_status: CLOSED_FINAL
  runtime_status: CLOSED
  audit_status: PASS
  indexation_status: REPAIRED
  branch_cleanup_decision: PASS
  remote_branch_cleanup_execution: EXECUTED
  count_reconciliation: PASS
  active_student_go: none
  next_student_go_required: false
```

### Chantiers actifs

Aucun chantier actif `student` / `ollama` n'est retenu dans `GO_INDEX.md` ou `ACTIVE_STREAMS.md`.

Les GO Student/Ollama historiques qui etaient PASS / ABSORBED / CLOSED_FINAL sont retires de ce bloc machine pour eviter leur relecture comme chantiers ouverts.

### Branches conservees en reference

| Branche | Statut | Note |
| --- | --- | --- |
| `save/student-2026-04-01` | KEEP_ARCHIVE | Snapshot/archive de reference ; ne pas rouvrir comme chantier actif |
| `feat/student-mimo-bitget-live-equity` | KEEP_ARCHIVE | Reference historique MIMO/Bitget ; non actif |
| `go/GO_OPT_TRADING_MACHINE_STUDENT_PARENT_01` | KEEP_ARCHIVE | Parent machine conserve comme ancre/archive ; non actif |

### GO historiques clos/pass retires du routage actif

| Famille | Statut | Note |
| --- | --- | --- |
| Parent machine Student | CLOSED_FINAL | Chaine fermee ; aucun GO enfant requis |
| Parent Local Ollama | CLOSED_FINAL | Absorbe par fermeture Student/Ollama |
| Lab children Student/OpenClaw/Ollama | PASS / ABSORBED | Branches remote nettoyees ; ne pas lister comme actifs |
| Agent standardization Student/Ollama | PASS / ABSORBED | Inclus dans cleanup/reconciliation ; ne pas relancer |
| Post-closure audit / index repair / remote cleanup / count reconciliation | PASS | Fermeture documentaire et Git executee |

### Evaluation prochains GO logiques depuis index global

Aucun prochain GO logique propre a `student` n'est ouvert par l'index global.

Le seul rattachement `student` restant dans les flux actifs est transversal : `GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03` mentionne que les alias courts `student` pointent deja vers le canonique `modules/reseau_ssh/scripts/*` avec PASS. La prochaine action de ce flux est generale (`scripts/reseau_ssh` puis `step1b`) et ne rouvre pas Student/Ollama.

Conclusion : ne pas proposer de nouveau GO `student` sauf demande explicite de reouverture ou preuve d'un nouveau besoin runtime.

---

## Bloc FANTOME

| Branche / GO | Statut | Note |
| --- | --- | --- |
| `GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01` | OPEN | AI team architecture parent |
| `go/GO_OPT_TRADING_STRICT_WORKERS_PARENT_01` | OPEN | Strict workers parent ; dossier a merger ou poursuivre |
| `go/GO_OPT_TRADING_CLICKUP_PARENT_CONTINUITY_01` | OPEN | ClickUp parent continuity ; implementation differee |

---

## Point de reprise

Pour toute suite sur ce routage machine :
1. relire `docs/index/BRANCH_STATE.md` ;
2. recroiser avec l'etat Git reel ;
3. ajuster ici seulement si le rattachement machine change reellement ;
4. ne pas surclasser un cas sans preuve repo/PR/documentaire ;
5. pour `student`, partir de `CLOSED_FINAL` et ne pas rouvrir sans demande explicite ou nouveau besoin runtime prouve.
