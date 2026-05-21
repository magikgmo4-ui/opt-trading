---
doc_id: GO_OPT_TRADING_OPENCLAW_PARENT_AUTOMATION_GAPS_CLOSE_01_PREPARED_MATRIX
doc_type: prepared_matrix
go_id: GO_OPT_TRADING_OPENCLAW_PARENT_AUTOMATION_GAPS_CLOSE_01
status: draft
lifecycle_stage: preparation
surface: docs/chantiers
source_kind: canonical
---

# 50_PREPARED_MATRIX — consolidation préparatoire pour GAP_01

Cible : ouvrir `GO_OPENCLAW_AI_TEAM_AUTOMATION_CAPABILITY_MATRIX_01`.

---

## 1_ACTEURS (issus du repo)

| actor_id | Source | Détail |
|---|---|---|
| humain | `10_GAPS_REGISTER.md` | Opérateur, approbateur HITL |
| OpenClaw | `10_GAPS_REGISTER.md` + `agent_model_matrix.yaml` | Orchestrateur, builder, reviewer, lab |
| strict_worker | `10_GAPS_REGISTER.md` + `STRICT_WORKERS_AUTONOMIE_ETROITE_01.md` | Agent IA borné, couloir fermé, A1-A4 |
| team_ai_manager | `10_GAPS_REGISTER.md` + `10_ROLES_JOBS_TASKS_INVENTORY.md` | Coordonne spécialistes, HITL |
| specialist_worker | `10_GAPS_REGISTER.md` + `10_ROLES_JOBS_TASKS_INVENTORY.md` | Raisonnement, volume, long contexte, flash/tri |
| app_bridge | `10_GAPS_REGISTER.md` | Bridge vers app externe (Airtable, ClickUp, Botpress, Sheets, Telegram, Gmail, Calendar, Drive, Figma, LocalCMS) |

## 2_SURFACES (issues du repo)

| surface_id | Source | Périmètre |
|---|---|---|
| repo | `10_GAPS_REGISTER.md`, `REPO_SURFACES_MAP.md` | docs, registry, workflow_ai, modules, scripts, config, schemas, adapters, tests, tools |
| tmux | `10_GAPS_REGISTER.md`, `machine_runtime_map.yml` | Sessions tmux par machine (openclaw, trading, desk) |
| Telegram | `10_GAPS_REGISTER.md` | Bots, chat control, notifications, signaux |
| TradingView | `10_GAPS_REGISTER.md` | Webhooks, alertes, signaux TV |
| Airtable | `10_GAPS_REGISTER.md`, `30_APPS_RETAINED_AND_MAINTENANCE_MATRIX.md` | Base bridges, inventaires |
| ClickUp | `10_GAPS_REGISTER.md`, `30_APPS_RETAINED_AND_MAINTENANCE_MATRIX.md` | Tâches humaines, planification |
| Botpress | `10_GAPS_REGISTER.md`, `30_APPS_RETAINED_AND_MAINTENANCE_MATRIX.md` | Chatbot, interface utilisateur |
| Sheets | `10_GAPS_REGISTER.md`, `30_APPS_RETAINED_AND_MAINTENANCE_MATRIX.md` | Google Sheets, exports |
| LocalCMS | `10_GAPS_REGISTER.md`, `30_APPS_RETAINED_AND_MAINTENANCE_MATRIX.md` | Cockpit opérateur, état, contrôles |
| DeskPro | `10_GAPS_REGISTER.md` | Desk automation, vision, capture |

### Surfaces additionnelles documentées (hors gap nominal mais pertinentes)

| surface_id | Source |
|---|---|
| MACHINE_OPS | `PERMISSION_MATRIX_01.md` |
| NETWORK | `PERMISSION_MATRIX_01.md` |
| SECRETS | `PERMISSION_MATRIX_01.md` |
| FILESYSTEM | `PERMISSION_MATRIX_01.md` |
| GIT | `PERMISSION_MATRIX_01.md` |
| SERVICES | `PERMISSION_MATRIX_01.md` (systemd, ports) |

## 3_PERMISSIONS (issues du repo)

| permission | Équivalent L0-L8 | Définition | Source |
|---|---|---|---|
| read | L0-L1 | Lecture, extraction, inventaire | `GAPS_REGISTER`, `PERMISSION_MATRIX` |
| draft | L2 | Proposition, plan, brouillon sans write | idem |
| patch_draft | L3 | Patch avec trace, sans effet direct | idem |
| write_gated | L4-L6 | Write sous gate avec validation externe | idem + `A4_WRITE_GATE_POLICY.md` |
| forbidden | L0 | Interdit par défaut | idem |

## 4_GATES (issues du repo)

| gate | Définition | Source |
|---|---|---|
| none | Pas de gate | `10_GAPS_REGISTER.md` |
| dry_run | Simulation sans write | `10_GAPS_REGISTER.md`, tasks.index.json |
| human_approve | Approbation humaine requise | `10_GAPS_REGISTER.md`, `A4_WRITE_GATE_POLICY.md` |
| dual_confirm | Double confirmation requise | `10_GAPS_REGISTER.md` |

## 5_MATRICE CIBLE (template ligne)

Chaque intersection `actor_id × surface_id` doit produire :

| actor_id | surface_id | permission | gate | log_required | rollback_required | evidence_ref | status |
|---|---|---|---|---|---|---|---|
| ... | ... | ... | ... | true/false | true/false | chemin | OPEN/PARTIAL/PASS |

## 6_GAP ANALYSIS — ce que la matrice cible doit résoudre

1. Les acteurs et surfaces existent de manière éparse dans le repo mais ne sont pas consolidés dans une table unique `actor × surface × permission`.
2. `PERMISSION_MATRIX_01.md` utilise L0-L8 et une liste de surfaces différente de celles du gap register. Un mapping L0-L8 → read/draft/patch_draft/write_gated/forbidden est nécessaire.
3. `rollback_required` n'est défini nulle part par intersection — seulement au niveau macro (GAP_12).
4. Le statut de chaque intersection est implicite, pas traçable.
5. La matrice doit relier chaque intersection à un `evidence_ref` concret (chemin fichier, test, artefact).
6. Les 3 scénarios de validation (read-only signal, draft patch repo, app external write gated) doivent produire des preuves référençables dans la matrice.

## 7_PREMIERS ACTEURS ET SURFACES CONSOLIDÉS (pré-remplissage)

Basé sur l'existant, les lignes les moins controversées pour la matrice :

| actor_id | surface_id | permission | gate | log_required | rollback_required |
|---|---|---|---|---|---|
| humain | repo | write_gated | human_approve | true | true |
| humain | Telegram | write_gated | human_approve | true | false |
| OpenClaw | repo | patch_draft | dry_run | true | true |
| OpenClaw | Telegram | read | none | true | false |
| strict_worker | repo | read | none | true | false |
| team_ai_manager | repo | patch_draft | human_approve | true | true |
| specialist_worker | repo | patch_draft | dry_run | true | true |
| app_bridge | Airtable | write_gated | human_approve | true | true |
| app_bridge | Telegram | read | none | true | false |
| app_bridge | Sheets | read | none | true | false |

Ces lignes sont une base de départ, pas une version figée.

## 8_SCÉNARIOS DE VALIDATION (préparés)

| # | Scénario | Acteur | Surface | Permission testée | Gate testée |
|---|---|---|---|---|---|
| 1 | read-only signal | strict_worker | Telegram | read | none |
| 2 | draft patch repo | specialist_worker | repo | patch_draft | dry_run |
| 3 | app external write gated | app_bridge | Airtable | write_gated | human_approve |

---

Prochaine étape : ouvrir `GO_OPENCLAW_AI_TEAM_AUTOMATION_CAPABILITY_MATRIX_01` sur cette base consolidée.
