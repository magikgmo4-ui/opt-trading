---
doc_id: DB_LAYER_A_VERIFIER_REVIEW_01_TABLE
doc_type: review_table
repo: opt-trading
go_id: GO_OPT_TRADING_DB_LAYER_A_VERIFIER_REVIEW_01
status: active
surface: chantier
source_kind: derived
updated_at: 2026-05-14
---

# 10_A_VERIFIER_REVIEW - Tableau de decision

| Branche | Ancien statut | Etat Git reel | MACHINE_WORK_SPLIT | BRANCH_STATE | Dossier chantier | Nouveau statut | Justification |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `go/GO_OPENCLAW_OPT_TRADING_CHILD_GATEWAY_SUPERVISION_TMUX_RUNTIME_01` | `A_VERIFIER` | remote, `DIVERGED`, `ahead 3`, `behind 681` | absent | present | `RUNTIME_LOG.md` present | `A_VERIFIER` | branche runtime residuelle encore non mergee ; closeout documentaire present mais delta Git non absorbe |
| `go/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_PARENT_01` | `A_VERIFIER` | remote, `BEHIND_ONLY`, `0/374` | absent | present | spec + inbox locales presentes | `KEEP_ACTIVE` | parent doc-only ouvert, statut `OPENING_DRAFT`, suite child explicite |
| `go/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_PERMISSION_MATRIX_01` | `A_VERIFIER` | remote, `BEHIND_ONLY`, `0/372` | absent | present | doc child present | `KEEP_ACTIVE` | child doc-only materialise dans le parent runtime security |
| `go/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_SCHEMA_01` | `A_VERIFIER` | remote, `BEHIND_ONLY`, `0/354` | absent | present | doc child present | `KEEP_ACTIVE` | child doc-only materialise et sequence parent->child explicite |
| `go/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_YAML_DRAFT_01` | `A_VERIFIER` | remote, `DIVERGED`, `2/353` | absent | present | pas de dossier local dedie isole, mais branche rattachee au parent security | `KEEP_ACTIVE` | draft child coherent avec le parent security encore ouvert |
| `go/GO_OPT_TRADING_MACHINE_DB_LAYER_PARENT_REVIEW_01` | `A_VERIFIER` | remote, `DIVERGED`, `1/814` | present | present | aucun dossier local dedie trouve | `A_VERIFIER` | preuve locale insuffisante pour distinguer review active vs reference |
| `go/GO_OPT_TRADING_UI_LOCALCMS_DB_LAYER_CONSUMER_REALIGNMENT_01` | `A_VERIFIER` | remote, `DIVERGED`, `1/814` | present | present | aucun dossier local dedie trouve | `A_VERIFIER` | branche presente dans le bloc machine mais sans preuve locale suffisante |
| `go/GO_OPT_TRADING_AIRTABLE_ORCHESTRATION_PARENT_01` | `A_VERIFIER` | remote absent observe | present | present | dossier local riche present (`99_VERDICT.md`, plan, architecture) | `KEEP_REFERENCE` | chantier doc-only materialise localement ; absence du remote observee, donc reference plutot qu'actif branche |
| `go/GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01` | `A_VERIFIER` | remote absent observe | present | present | dossier local riche present, statut `OPEN` dans `01_cadrage_parent.md` | `KEEP_REFERENCE` | la branche manque dans le Git observe, mais la surface documentaire est materalisee et reutilisee par des child docs |
| `go/GO_OPT_TRADING_REPO_SURFACES_PARENT_CARTOGRAPHY_01` | `A_VERIFIER` | remote, `DIVERGED`, `1/926` | present | present | aucun dossier local dedie trouve | `A_VERIFIER` | preuve locale insuffisante |

## Resultat

### Reclassements proposes

- vers `KEEP_ACTIVE` : 4
- vers `KEEP_REFERENCE` : 2
- reste `A_VERIFIER` : 4
- vers `DROP_MERGED` : 0

### Branches restantes `A_VERIFIER`

- `go/GO_OPENCLAW_OPT_TRADING_CHILD_GATEWAY_SUPERVISION_TMUX_RUNTIME_01`
- `go/GO_OPT_TRADING_MACHINE_DB_LAYER_PARENT_REVIEW_01`
- `go/GO_OPT_TRADING_UI_LOCALCMS_DB_LAYER_CONSUMER_REALIGNMENT_01`
- `go/GO_OPT_TRADING_REPO_SURFACES_PARENT_CARTOGRAPHY_01`
