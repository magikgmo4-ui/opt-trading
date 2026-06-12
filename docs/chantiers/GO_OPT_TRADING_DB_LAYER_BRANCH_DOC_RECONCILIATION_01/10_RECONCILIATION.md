---
doc_id: DB_LAYER_BRANCH_DOC_RECONCILIATION_01_RECONCILIATION
doc_type: reconciliation_table
repo: opt-trading
go_id: GO_OPT_TRADING_DB_LAYER_BRANCH_DOC_RECONCILIATION_01
status: active
surface: chantier
source_kind: derived
updated_at: 2026-05-14
---

# 10_RECONCILIATION - DB_LAYER / OpenClaw

## Sources croisees

| Source | Constat |
| --- | --- |
| `MACHINE_WORK_SPLIT` bloc `DB_LAYER` | 10 branches documentees |
| `BRANCH_STATE.md` | 7 entrees explicites seulement sur cette surface |
| branches Git reelles `db-layer/OpenClaw` | 16 branches remote detectees |
| `ACTIVE_STREAMS.md` | pas de stream OpenClaw db-layer autonome actif ; seule la ligne `reseau_ssh` mentionne un PASS alias machine |
| parent OpenClaw | chaine `parent -> child -> runtime -> closeout` deja closee, pas de reprise runtime requise |

## Branches reelles observees

| Branche | Scope | Status vs `origin/sot/mainline` | Ahead | Behind | Classification | Note |
| --- | --- | --- | ---: | ---: | --- | --- |
| `doc/GO_OPENCLAW_INFRA_BASELINE_01` | remote | DIVERGED | 1 | 1237 | `REFERENCE` | branche historique OpenClaw deja ancree dans le canon local, a conserver comme reference |
| `go/GO_OPENCLAW_OPT_TRADING_CHILD_GATEWAY_SUPERVISION_TMUX_01` | remote | DIVERGED | 2 | 688 | `DROP_MERGED` | child doc-only clos ; la chaine est closee documentairement ; cleanup interdit dans ce GO |
| `go/GO_OPENCLAW_OPT_TRADING_CHILD_GATEWAY_SUPERVISION_TMUX_CLOSEOUT_01` | remote | DIVERGED | 1 | 680 | `REFERENCE` | closeout de chaine, a conserver comme trace |
| `go/GO_OPENCLAW_OPT_TRADING_CHILD_GATEWAY_SUPERVISION_TMUX_RUNTIME_01` | remote | DIVERGED | 3 | 681 | `A_VERIFIER` | runtime ferme documentairement mais branche remote encore residuelle ; pas de cleanup ici |
| `go/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01` | remote | DIVERGED | 9 | 905 | `ACTIVE` | parent reel `db-layer` conserve comme ancre doc |
| `go/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_DOC_REALIGN_01` | remote | DIVERGED | 1 | 698 | `REFERENCE` | lot de realignement parent cite comme dernier review GO du parent |
| `go/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_PERMISSION_MATRIX_01` | remote | BEHIND_ONLY | 0 | 372 | `A_VERIFIER` | OpenClaw oui, mais rattachement `db-layer` non prouve dans les index machine |
| `go/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_SCHEMA_01` | remote | BEHIND_ONLY | 0 | 354 | `A_VERIFIER` | idem, chantier OpenClaw security ouvert hors bloc `DB_LAYER` |
| `go/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_YAML_DRAFT_01` | remote | DIVERGED | 2 | 353 | `A_VERIFIER` | idem, doc-only runtime security hors rattachement machine prouve |
| `go/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_PARENT_01` | remote | BEHIND_ONLY | 0 | 374 | `A_VERIFIER` | parent OpenClaw security documente localement mais absent du bloc `DB_LAYER` |
| `go/GO_OPENCLAW_STATE_DIR_REPAIR_10` | remote | DIVERGED | 1 | 814 | `REFERENCE` | lot OpenClaw historique deja conserve comme reference de classification |
| `go/GO_OPT_TRADING_MACHINE_DB_LAYER_PARENT_REVIEW_01` | remote | DIVERGED | 1 | 814 | `A_VERIFIER` | present dans `MACHINE_WORK_SPLIT`, absent de `BRANCH_STATE`, aucune preuve locale suffisante de statut produit |
| `go/GO_OPT_TRADING_REPO_SURFACES_PARENT_CARTOGRAPHY_01` | remote | DIVERGED | 1 | 926 | `A_VERIFIER` | present dans bloc `DB_LAYER`, deja `A_VERIFIER` dans `BRANCH_STATE` |
| `go/GO_OPT_TRADING_UI_LOCALCMS_DB_LAYER_CONSUMER_REALIGNMENT_01` | remote | DIVERGED | 1 | 814 | `A_VERIFIER` | present dans `MACHINE_WORK_SPLIT`, absent de `BRANCH_STATE`, preuve locale insuffisante |
| `go/GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_DB_LAYER_CLOSEOUT_01` | remote | DIVERGED | 1 | 814 | `REFERENCE` | closeout tmux db-layer, reference runtime closee |
| `go/GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_DB_LAYER_REVIEW_01` | remote | DIVERGED | 1 | 814 | `REFERENCE` | review tmux db-layer, reference historique closee |

## Ecart `MACHINE_WORK_SPLIT` vs Git reel

### Present dans le bloc `DB_LAYER`

- `go/GO_OPT_TRADING_MACHINE_DB_LAYER_PARENT_REVIEW_01`
- `go/GO_OPT_TRADING_UI_LOCALCMS_DB_LAYER_CONSUMER_REALIGNMENT_01`
- `go/GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_DB_LAYER_REVIEW_01`
- `go/GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_DB_LAYER_CLOSEOUT_01`
- `go/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01`
- `go/GO_OPENCLAW_STATE_DIR_REPAIR_10`
- `doc/GO_OPENCLAW_INFRA_BASELINE_01`
- `go/GO_OPT_TRADING_AIRTABLE_ORCHESTRATION_PARENT_01`
- `go/GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01`
- `go/GO_OPT_TRADING_REPO_SURFACES_PARENT_CARTOGRAPHY_01`

### Presentes dans le bloc `DB_LAYER` mais absentes du Git reel observe

- `go/GO_OPT_TRADING_AIRTABLE_ORCHESTRATION_PARENT_01`
- `go/GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01`

### Presents en Git reel mais absents du bloc `DB_LAYER`

- `go/GO_OPENCLAW_OPT_TRADING_CHILD_GATEWAY_SUPERVISION_TMUX_01`
- `go/GO_OPENCLAW_OPT_TRADING_CHILD_GATEWAY_SUPERVISION_TMUX_CLOSEOUT_01`
- `go/GO_OPENCLAW_OPT_TRADING_CHILD_GATEWAY_SUPERVISION_TMUX_RUNTIME_01`
- `go/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_DOC_REALIGN_01`
- `go/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_PARENT_01`
- `go/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_PERMISSION_MATRIX_01`
- `go/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_SCHEMA_01`
- `go/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_YAML_DRAFT_01`

## Ecart `BRANCH_STATE` vs Git reel

### Deja representes dans `BRANCH_STATE`

- `go/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01`
- `go/GO_OPENCLAW_OPT_TRADING_CHILD_GATEWAY_SUPERVISION_TMUX_01`
- `go/GO_OPENCLAW_OPT_TRADING_CHILD_GATEWAY_SUPERVISION_TMUX_RUNTIME_01`
- `doc/GO_OPENCLAW_INFRA_BASELINE_01`
- `go/GO_OPT_TRADING_AIRTABLE_ORCHESTRATION_PARENT_01`
- `go/GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01`
- `go/GO_OPT_TRADING_REPO_SURFACES_PARENT_CARTOGRAPHY_01`

### Manquantes dans `BRANCH_STATE`

- `go/GO_OPENCLAW_OPT_TRADING_CHILD_GATEWAY_SUPERVISION_TMUX_CLOSEOUT_01`
- `go/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_DOC_REALIGN_01`
- `go/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_PARENT_01`
- `go/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_PERMISSION_MATRIX_01`
- `go/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_SCHEMA_01`
- `go/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_YAML_DRAFT_01`
- `go/GO_OPENCLAW_STATE_DIR_REPAIR_10`
- `go/GO_OPT_TRADING_MACHINE_DB_LAYER_PARENT_REVIEW_01`
- `go/GO_OPT_TRADING_UI_LOCALCMS_DB_LAYER_CONSUMER_REALIGNMENT_01`
- `go/GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_DB_LAYER_CLOSEOUT_01`
- `go/GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_DB_LAYER_REVIEW_01`

## Constat cle

La surface `db-layer/OpenClaw` n'appelle pas de reprise runtime. Le prochain besoin prouve est documentaire : representer proprement les branches reelles dans `MACHINE_WORK_SPLIT` et/ou `BRANCH_STATE`, en separant :

- les references historiques OpenClaw deja fermees,
- le parent `GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01` encore actif comme ancre,
- les branches OpenClaw security qui existent mais ne sont pas encore rattachees machine de facon canonique,
- les branches `DB_LAYER` encore sans preuve de statut suffisante.

## RISKS

- À qualifier.
