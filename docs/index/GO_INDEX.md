---
doc_id: OPT_TRADING_GO_INDEX
doc_type: reprise
repo: opt-trading
project: opt-trading
module:
go_id:
status: reference
lifecycle_stage: governance
topic_keys:
  - opt-trading
  - go_index
  - continuity
  - governance
search_tags:
  - surface:continuite
  - doc_role:index
  - closeout:reference
surface: continuity
source_kind: canonical
reference_canonique_principale: docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
point_de_reprise: "Section Tableau canonique des chantiers"
updated_at: 2026-05-09
links:
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
  - docs/governance/REPO_ROLE.md
  - docs/governance/DOC_LAYERS.md
---

# GO_INDEX — opt-trading

## Objet

Ce document référence les GO non clos connus et utiles à la continuité locale de `opt-trading`.

## Rattachement maître

- l'etat reel prouve prime sur toute reconstruction documentaire
- `docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md` gouverne la lecture produit / parent / GO / Git
- `docs/governance/MATRICE_GOUVERNANTE_V2.md` reste une annexe stable secondaire
- `docs/index/GO_INDEX.md` reste la verite de liste locale pour les parents, GO simples et sous-entrees retenues

---

## Snapshot global système

- 2026-04-18  
  → docs/architecture/PROJECT_SNAPSHOT_GLOBAL_2026-04-18.md  
  → vue consolidée projets / infra / chantiers / runtime

---

## Forms / LocalCMS (cadrage)

- GO_LOCALCMS_FORMS_INTEGRATION_DOC_01  
  → docs/chantiers/GO_LOCALCMS_FORMS_INTEGRATION_DOC_01/00_cadrage.md  
  → intégration future forms compatible avec localcms existant (doc-only)

---

## Règles

- l’index référence et synthétise
- il ne remplace ni le dossier chantier ni le closeout
- `GO_INDEX.md` est l’index opératoire des chantiers non clos
- le `Tableau canonique des chantiers` est la vérité de liste de `GO_INDEX.md`
- la section `Entrées` enrichit un GO déjà canonisé dans le tableau ; elle n’ouvre pas un nouveau GO à elle seule
- lorsqu’un chantier passe en `CLOSED`/`PASS`, il doit être retiré de `docs/index/GO_INDEX.md` et déplacé dans `docs/index/GO_CLOSED_INDEX.md`
- les entrées `REFERENCE` peuvent rester dans `GO_INDEX.md` si elles sont utiles à la continuité active et ne correspondent pas à une clôture
- une surface documentaire non chantier peut être citée comme source, support ou référence, mais ne doit pas être listée comme chantier dans le tableau canonique
- un repère de famille dérivé peut exister comme aide transverse non canonique ; il ne doit ni modifier la liste canonique ni porter la priorité opératoire à la place du tableau
- les liens doivent pointer vers les artefacts détaillés dès qu’ils existent

---

## Tableau canonique des chantiers

Ce tableau canonique ne contient que les chantiers non clos utiles à l’opératoire courant.

Normalisation retenue :

- `PARENT = CHANTIER` si aucun parent explicite n'est prouvé dans le repo
- `SOUS_CHANTIER = —` si aucun sous-chantier explicite n'est prouvé dans le repo
- `STATUT` est normalisé en `OPEN`, `ACTIVE`, `CLOSED`, `REFERENCE` ; les entrées `CLOSED`/`PASS` relèvent de `docs/index/GO_CLOSED_INDEX.md`
- `DOSSIER_PRESENT` indique la présence d'un dossier direct sous `docs/chantiers/`

| PARENT | CHANTIER | SOUS_CHANTIER | STATUT | DOSSIER_PRESENT | SOURCE |
| --- | --- | --- | --- | --- | --- |
| GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01 | GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01 | â€” | OPEN | oui | `docs/chantiers/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01/00_INITIAL_PROJECT_DOC.md`<br>`docs/chantiers/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01/PARENT_STATE.md`<br>`docs/chantiers/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01/INDEX_PATCH.md` |
| GO_UNIFORM_CONTINUITY_FINAL_MASTER_PLAN_01 | GO_UNIFORM_CONTINUITY_FINAL_MASTER_PLAN_01 | — | REFERENCE | oui | `docs/index/GO_INDEX.md`<br>`docs/chantiers/GO_UNIFORM_CONTINUITY_FINAL_MASTER_PLAN_01/00_cadrage.md` |
| GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01 | GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01 | — | OPEN | oui | `docs/chantiers/GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01/01_cadrage_parent.md`<br>`docs/chantiers/GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01/02_initial_project_doc.md`<br>`docs/chantiers/GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01/03_decisions.md` |
| GO_OPT_TRADING_MACHINE_DB_LAYER_PARENT_01 | GO_OPT_TRADING_MACHINE_DB_LAYER_PARENT_01 | — | OPEN | oui | `docs/chantiers/GO_OPT_TRADING_MACHINE_DB_LAYER_PARENT_01/01_cadrage_parent.md`<br>`docs/chantiers/GO_OPT_TRADING_MACHINE_DB_LAYER_PARENT_01/02_initial_project_doc.md`<br>`docs/chantiers/GO_OPT_TRADING_MACHINE_DB_LAYER_PARENT_01/03_decisions.md` |
| GO_GIT_PROGRESSIVE_MIGRATION_START_13 | GO_GIT_PROGRESSIVE_MIGRATION_START_13 | — | ACTIVE | oui | `docs/index/GO_INDEX.md`<br>`docs/chantiers/GO_GIT_PROGRESSIVE_MIGRATION_START_13/00_cadrage.md` |
| GO_OPT_TRADING_RUNTIME_EXCEPTION_FAMILIES_01 | GO_OPT_TRADING_RUNTIME_EXCEPTION_FAMILIES_01 | — | ACTIVE | oui | `docs/index/GO_INDEX.md`<br>`docs/chantiers/GO_OPT_TRADING_RUNTIME_EXCEPTION_FAMILIES_01/00_cadrage.md`<br>`docs/chantiers/GO_OPT_TRADING_RUNTIME_EXCEPTION_FAMILIES_01/03_decisions.md` |
| GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03 | GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03 | — | OPEN | oui | `docs/index/GO_INDEX.md`<br>`docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03/00_cadrage.md` |
| GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03 | GO_OPT_TRADING_RESEAU_SSH_UNIFIED_MODULE_CADRAGE_01 | — | OPEN | oui | `docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_UNIFIED_MODULE_CADRAGE_01/00_cadrage.md`<br>`docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03/00_cadrage.md` |
| GO_TMUX_IDE_OPT_TRADING_CADRAGE_01 | GO_TMUX_IDE_OPT_TRADING_CADRAGE_01 | — | ACTIVE | oui | `docs/index/GO_INDEX.md`<br>`docs/chantiers/GO_TMUX_IDE_OPT_TRADING_CADRAGE_01/00_cadrage.md` |
| GO_LOCALCMS_FORMS_INTEGRATION_DOC_01 | GO_LOCALCMS_FORMS_INTEGRATION_DOC_01 | — | OPEN | oui | `docs/index/GO_INDEX.md`<br>`docs/chantiers/GO_LOCALCMS_FORMS_INTEGRATION_DOC_01/00_cadrage.md` |
| GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01 | GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01 | — | OPEN | oui | `docs/chantiers/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01/00_cadrage.md`<br>`docs/chantiers/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01/01_initial_project_doc.md`<br>`docs/chantiers/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01/03_decisions.md` |
| GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01 | GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_DBLAYER_OPENCLAW_REMOTE_EXEC_CANONICALIZE_01 | — | OPEN | oui | `docs/chantiers/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_DBLAYER_OPENCLAW_REMOTE_EXEC_CANONICALIZE_01/00_INITIAL_PROJECT_DOC.md`<br>`docs/chantiers/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_DBLAYER_OPENCLAW_REMOTE_EXEC_CANONICALIZE_01/03_REMOTE_EXEC_STATE.md` |
| GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01 | GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01 | — | OPEN | oui | `docs/index/GO_INDEX.md`<br>`docs/chantiers/GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01/01_cadrage_parent.md` |
| GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01 | GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01 | GO_OPT_TRADING_UI_LOCALCMS_INVENTORY_01 | REFERENCE | non | `docs/chantiers/GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01/01_cadrage_parent.md` |
| GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01 | GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01 | GO_OPT_TRADING_UI_LOCALCMS_MATRIX_01 | REFERENCE | non | `docs/chantiers/GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01/01_cadrage_parent.md` |
| GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01 | GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01 | GO_OPT_TRADING_UI_LOCALCMS_CONTRACTS_01 | REFERENCE | non | `docs/chantiers/GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01/01_cadrage_parent.md` |
| GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01 | GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01 | GO_OPT_TRADING_UI_LOCALCMS_PILOT_READONLY_01 | REFERENCE | non | `docs/chantiers/GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01/01_cadrage_parent.md` |
| GO_EXTRACTEUR_TAGS_CANONICAL_METHOD_01 | GO_EXTRACTEUR_TAGS_CANONICAL_METHOD_01 | — | REFERENCE | non | `docs/index/GO_INDEX.md`<br>`docs/governance/EXTRACTEUR_TAGS__METHODE_CANONIQUE_V1.md` |
| GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01 | GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01 | — | OPEN | oui | `docs/chantiers/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01/REPRISE_DB_LAYER_20260505.md`<br>`docs/index/inbox/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01.md`<br>`docs/chantiers/GO_OPENCLAW_OPT_TRADING_CHILD_GATEWAY_SUPERVISION_TMUX_CLOSEOUT_01/CLOSEOUT_20260505.md` |
| GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01 | GO_OPENCLAW_OPT_TRADING_CHILD_DBLAYER_SSH_LOCAL_GATEWAY_VALIDATION_01 | — | OPEN | oui | `docs/chantiers/GO_OPENCLAW_OPT_TRADING_CHILD_DBLAYER_SSH_LOCAL_GATEWAY_VALIDATION_01/00_INITIAL_PROJECT_DOC.md`<br>`docs/chantiers/GO_OPENCLAW_OPT_TRADING_CHILD_DBLAYER_SSH_LOCAL_GATEWAY_VALIDATION_01/DBLAYER_SSH_LOCAL_GATEWAY_VALIDATION_REPORT_01.md`<br>`docs/chantiers/GO_OPENCLAW_OPT_TRADING_CHILD_DBLAYER_SSH_LOCAL_GATEWAY_VALIDATION_01/90_CLOSEOUT.md` |
| GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01 | GO_OPENCLAW_OPT_TRADING_CHILD_DBLAYER_ORCHESTRATOR_FIRST_CONTROLLED_JOB_01 | — | OPEN | oui | `docs/chantiers/GO_OPENCLAW_OPT_TRADING_CHILD_DBLAYER_ORCHESTRATOR_FIRST_CONTROLLED_JOB_01/00_INITIAL_PROJECT_DOC.md`<br>`docs/chantiers/GO_OPENCLAW_OPT_TRADING_CHILD_DBLAYER_ORCHESTRATOR_FIRST_CONTROLLED_JOB_01/DBLAYER_ORCHESTRATOR_FIRST_CONTROLLED_JOB_PLAN_01.md`<br>`docs/chantiers/GO_OPENCLAW_OPT_TRADING_CHILD_DBLAYER_ORCHESTRATOR_FIRST_CONTROLLED_JOB_01/DBLAYER_ORCHESTRATOR_FIRST_CONTROLLED_JOB_REPORT_01.md`<br>`docs/chantiers/GO_OPENCLAW_OPT_TRADING_CHILD_DBLAYER_ORCHESTRATOR_FIRST_CONTROLLED_JOB_01/90_CLOSEOUT.md` |
| GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01 | GO_OPENCLAW_OPT_TRADING_CHILD_DBLAYER_ORCHESTRATOR_OPERATIONAL_RUNBOOK_01 | — | OPEN | oui | `docs/chantiers/GO_OPENCLAW_OPT_TRADING_CHILD_DBLAYER_ORCHESTRATOR_OPERATIONAL_RUNBOOK_01/00_INITIAL_PROJECT_DOC.md`<br>`docs/chantiers/GO_OPENCLAW_OPT_TRADING_CHILD_DBLAYER_ORCHESTRATOR_OPERATIONAL_RUNBOOK_01/DBLAYER_ORCHESTRATOR_OPERATIONAL_RUNBOOK_01.md`<br>`docs/chantiers/GO_OPENCLAW_OPT_TRADING_CHILD_DBLAYER_ORCHESTRATOR_OPERATIONAL_RUNBOOK_01/90_CLOSEOUT.md` |
| GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01 | GO_OPENCLAW_OPT_TRADING_CHILD_DBLAYER_ORCHESTRATOR_READONLY_WORKFLOW_SMOKE_01 | — | OPEN | oui | `docs/chantiers/GO_OPENCLAW_OPT_TRADING_CHILD_DBLAYER_ORCHESTRATOR_READONLY_WORKFLOW_SMOKE_01/00_INITIAL_PROJECT_DOC.md`<br>`docs/chantiers/GO_OPENCLAW_OPT_TRADING_CHILD_DBLAYER_ORCHESTRATOR_READONLY_WORKFLOW_SMOKE_01/DBLAYER_ORCHESTRATOR_READONLY_WORKFLOW_SMOKE_PLAN_01.md`<br>`docs/chantiers/GO_OPENCLAW_OPT_TRADING_CHILD_DBLAYER_ORCHESTRATOR_READONLY_WORKFLOW_SMOKE_01/DBLAYER_ORCHESTRATOR_READONLY_WORKFLOW_SMOKE_REPORT_01.md`<br>`docs/chantiers/GO_OPENCLAW_OPT_TRADING_CHILD_DBLAYER_ORCHESTRATOR_READONLY_WORKFLOW_SMOKE_01/90_CLOSEOUT.md` |
| GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01 | GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01 | — | ACTIVE | oui | `docs/chantiers/GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01/00_cadrage.md`<br>`docs/index/REPRISE.md` |
| GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01 | GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01 | GO_TMUX_RUNTIME_CONVENTIONS_01 | REFERENCE | non | `docs/chantiers/GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01/00_cadrage.md` |
| GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01 | GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01 | GO_OPENCLAW_COMMAND_SCOPE_01 | REFERENCE | non | `docs/chantiers/GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01/00_cadrage.md` |
| GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01 | GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01 | GO_TMUX_RUNTIME_CONTRACT_01 | REFERENCE | non | `docs/chantiers/GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01/00_cadrage.md` |
| GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01 | GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01 | GO_TMUX_OPENCODE_OPENCLAW_MODES_01 | REFERENCE | non | `docs/chantiers/GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01/00_cadrage.md` |
| GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01 | GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01 | GO_RUNTIME_GUARDRAILS_01 | REFERENCE | non | `docs/chantiers/GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01/00_cadrage.md` |
| GO_OPT_TRADING_CLICKUP_PARENT_CONTINUITY_01 | GO_OPT_TRADING_CLICKUP_PARENT_CONTINUITY_01 | — | OPEN | oui | `docs/chantiers/GO_OPT_TRADING_CLICKUP_PARENT_CONTINUITY_01/00_INITIAL_PROJECT_DOC.md`<br>`docs/chantiers/GO_OPT_TRADING_CLICKUP_PARENT_CONTINUITY_01/CLICKUP_IMPLEMENTATION_BUNDLE_V1/INDEX.md`<br>`docs/chantiers/GO_OPT_TRADING_CLICKUP_PARENT_CONTINUITY_01/90_CLOSEOUT.md` |
| GO_OPT_TRADING_STRICT_WORKERS_PARENT_01 | GO_OPT_TRADING_STRICT_WORKERS_PARENT_01 | — | OPEN | non | branche `go/GO_OPT_TRADING_STRICT_WORKERS_PARENT_01`<br>`docs/chantiers/GO_OPT_TRADING_STRICT_WORKERS_PARENT_01/00_INITIAL_PROJECT_DOC.md` |

---

## Priorite operatoire (7 GO non clos)

- P0 : `GO_TMUX_IDE_OPT_TRADING_CADRAGE_01`
- P1 : `GO_OPT_TRADING_RUNTIME_EXCEPTION_FAMILIES_01`, `GO_GIT_PROGRESSIVE_MIGRATION_START_13`, `GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03`, `GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01`
- P2 : `GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01`, `GO_OPT_TRADING_CLICKUP_PARENT_CONTINUITY_01`

Le passage de 6 a 7 GO non clos retenus correspond a la re-inscription documentaire du parent :
- `GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01`

Le passage a 5 GO non clos retenus correspond a la sortie de `GO_OPT_TRADING_PARENT_NAMING_CANON_01` apres closeout parent.

Le parent `GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01` reste ouvert et canonique dans le tableau, mais hors perimetre d'absorption de cette priorisation resserree.

Historique recent :
- le palier precedent a 10 GO non clos correspondait au maintien temporaire de `GO_OPT_TRADING_CONTINUITY_INDEX_REALIGNMENT_01` et `GO_OPT_TRADING_CANON_STRUCTURE_REALIGNMENT_01` comme actifs avant closeout local

---

## Entrées

### GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01
- repo : opt-trading
- type : chantier parent machine / doc-only
- statut : open
- titre court : parent canonique de la machine admin-trading
- dernier état connu : parent ouvert dans `GO_OPT_TRADING_DOC_OPS_CHILD_PARENT_OPENING_BATCH_01` puis audite dans `GO_OPT_TRADING_DOC_OPS_CHILD_PARENT_CONFORMITY_AUDIT_01` ; conformite locale validee contre la matrice maitre
- lien utile : `docs/chantiers/GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01/01_cadrage_parent.md`, `docs/chantiers/GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01/02_initial_project_doc.md`, `docs/chantiers/GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01/03_decisions.md`

### GO_OPT_TRADING_MACHINE_DB_LAYER_PARENT_01
- repo : opt-trading
- type : chantier parent machine / doc-only
- statut : open
- titre court : parent canonique de la machine db-layer
- dernier état connu : parent ouvert dans `GO_OPT_TRADING_DOC_OPS_CHILD_PARENT_OPENING_BATCH_01` puis audite dans `GO_OPT_TRADING_DOC_OPS_CHILD_PARENT_CONFORMITY_AUDIT_01` ; conformite locale validee contre la matrice maitre
- lien utile : `docs/chantiers/GO_OPT_TRADING_MACHINE_DB_LAYER_PARENT_01/01_cadrage_parent.md`, `docs/chantiers/GO_OPT_TRADING_MACHINE_DB_LAYER_PARENT_01/02_initial_project_doc.md`, `docs/chantiers/GO_OPT_TRADING_MACHINE_DB_LAYER_PARENT_01/03_decisions.md`

### GO_UNIFORM_CONTINUITY_FINAL_MASTER_PLAN_01
- repo : opt-trading
- type : gouvernance / continuité
- statut : reference
- titre court : plan maître uniforme de continuité
- dernier état connu : référentiel consolidé validé comme base documentaire
- lien utile : `docs/chantiers/GO_UNIFORM_CONTINUITY_FINAL_MASTER_PLAN_01/00_cadrage.md`

### GO_GIT_PROGRESSIVE_MIGRATION_START_13
- repo : opt-trading
- type : migration documentaire
- statut : active
- titre court : démarrage de la migration Git progressive
- dernier état connu : gouvernance locale initiale créée sur `sot/mainline`
- lien utile : `docs/chantiers/GO_GIT_PROGRESSIVE_MIGRATION_START_13/00_cadrage.md`, `docs/governance/REPO_ROLE.md`, `docs/governance/DOC_LAYERS.md`, `docs/governance/MEMORY_BRICKS_MAPPING.md`

### GO_OPT_TRADING_RUNTIME_EXCEPTION_FAMILIES_01
- repo : opt-trading
- type : patch local / doc-only
- statut : active
- titre court : familles mixtes / lignées runtime-exception
- dernier état connu : parent PHASE 3 LOT 5 ouvert ; fiches status courtes posées et rattachées à l’audit famille
- lien utile : `docs/chantiers/GO_OPT_TRADING_RUNTIME_EXCEPTION_FAMILIES_01/00_cadrage.md`, `docs/chantiers/GO_OPT_TRADING_RUNTIME_EXCEPTION_FAMILIES_01/03_decisions.md`

### GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03
- repo : opt-trading
- type : consolidation modules / reseau_ssh
- statut : open
- titre court : consolidation ciblée de la famille reseau_ssh*
- dernier état connu : `modules/reseau_ssh` est le canonique repo-side ; `db-layer`, `admin-trading`, `student` et `fantome` ont maintenant leurs alias courts repointés vers le canonique avec PASS ; `step1b` et `scripts/reseau_ssh` restent en compat
- lien utile : `docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03/00_cadrage.md`, `docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_CANONICAL_RENAME_REGISTRY_01/01_plan_operationnel_step_by_step.md`, `docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_MACHINE_SIDE_REPOINT_01/10_step_09_execution_resultats.md`

### GO_TMUX_IDE_OPT_TRADING_CADRAGE_01
- repo : opt-trading
- type : outillage / tmux-ide
- statut : active
- titre court : cadrage IDE terminale tmux-ide
- dernier etat connu : bundle prepare, cadrage canonique ouvert ; le run reel Attention Center est merge en PASS et confirme `GO_TMUX_IDE_OPT_TRADING_IMPL_BASE_01` comme suite documentaire et operatoire
- prochaine action : ouvrir `GO_TMUX_IDE_OPT_TRADING_IMPL_BASE_01` ; machine cible a verifier avant execution ; OpenClaw hors scope pour cette suite
- lien utile : `docs/chantiers/GO_TMUX_IDE_OPT_TRADING_CADRAGE_01/00_cadrage.md`

### GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01
- repo : opt-trading
- type : intégration UI / producer-consumer
- statut : open
- titre court : chantier parent UI opt-trading producer → localcms consumer
- dernier état connu : cadrage parent posé ; `opt-trading` reste producer canonique et `localcms` consumer UI ; reprise recommandée sur `GO_OPT_TRADING_UI_LOCALCMS_INVENTORY_01`
- lien utile : `docs/chantiers/GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01/01_cadrage_parent.md`

### GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01
- repo : opt-trading
- type : reprise documentaire / parent OpenClaw / db-layer
- statut : open
- titre court : parent OpenClaw operateur hors continuite canonique a realigner
- dernier etat connu : parent reel de reference sur branche dediee `go/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01` ; la chaine TMUX historique est closee, et la prochaine passe canonique retenue est le gate `SSH/local db-layer` du child `GO_OPENCLAW_OPT_TRADING_CHILD_DBLAYER_SSH_LOCAL_GATEWAY_VALIDATION_01`
- lien utile : `docs/chantiers/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01/REPRISE_DB_LAYER_20260505.md`, `docs/index/inbox/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01.md`, `docs/chantiers/GO_OPENCLAW_OPT_TRADING_CHILD_DBLAYER_SSH_LOCAL_GATEWAY_VALIDATION_01/00_INITIAL_PROJECT_DOC.md`, `docs/chantiers/GO_OPENCLAW_OPT_TRADING_CHILD_DBLAYER_SSH_LOCAL_GATEWAY_VALIDATION_01/DBLAYER_SSH_LOCAL_GATEWAY_VALIDATION_REPORT_01.md`, `docs/chantiers/GO_OPENCLAW_OPT_TRADING_CHILD_GATEWAY_SUPERVISION_TMUX_CLOSEOUT_01/CLOSEOUT_20260505.md`

### GO_OPENCLAW_OPT_TRADING_CHILD_DBLAYER_SSH_LOCAL_GATEWAY_VALIDATION_01
- repo : opt-trading
- type : child OpenClaw / validation SSH gate / execution locale db-layer
- statut : open
- titre court : validation `fantome -> SSH -> db-layer` pour `OpenClaw` local
- dernier etat connu : ouverture canonique du GO pour assumer `SSH` comme transport gouverne, stopper l'idee d'installation `openclaw` sur `fantome`, et borner les controles locaux `db-layer` a identite machine, repo, Git, CLI, `Gateway V2`, orchestrateur et dry-run builder
- lien utile : `docs/chantiers/GO_OPENCLAW_OPT_TRADING_CHILD_DBLAYER_SSH_LOCAL_GATEWAY_VALIDATION_01/00_INITIAL_PROJECT_DOC.md`, `docs/chantiers/GO_OPENCLAW_OPT_TRADING_CHILD_DBLAYER_SSH_LOCAL_GATEWAY_VALIDATION_01/DBLAYER_SSH_LOCAL_GATEWAY_VALIDATION_REPORT_01.md`, `docs/chantiers/GO_OPENCLAW_OPT_TRADING_CHILD_DBLAYER_SSH_LOCAL_GATEWAY_VALIDATION_01/90_CLOSEOUT.md`, `docs/index/inbox/GO_OPENCLAW_OPT_TRADING_CHILD_DBLAYER_SSH_LOCAL_GATEWAY_VALIDATION_01.md`

### GO_OPENCLAW_OPT_TRADING_CHILD_DBLAYER_ORCHESTRATOR_FIRST_CONTROLLED_JOB_01
- repo : opt-trading
- type : child orchestrator / first controlled job / db-layer
- statut : open
- titre court : premier job orchestrateur OpenClaw controle sur db-layer
- dernier etat connu : PASSE — sample-run 11 modules PAPER mode, 11/11 OK, aucun effet de bord, git status clean
- lien utile : `docs/chantiers/GO_OPENCLAW_OPT_TRADING_CHILD_DBLAYER_ORCHESTRATOR_FIRST_CONTROLLED_JOB_01/00_INITIAL_PROJECT_DOC.md`, `docs/chantiers/GO_OPENCLAW_OPT_TRADING_CHILD_DBLAYER_ORCHESTRATOR_FIRST_CONTROLLED_JOB_01/DBLAYER_ORCHESTRATOR_FIRST_CONTROLLED_JOB_PLAN_01.md`, `docs/chantiers/GO_OPENCLAW_OPT_TRADING_CHILD_DBLAYER_ORCHESTRATOR_FIRST_CONTROLLED_JOB_01/DBLAYER_ORCHESTRATOR_FIRST_CONTROLLED_JOB_REPORT_01.md`, `docs/chantiers/GO_OPENCLAW_OPT_TRADING_CHILD_DBLAYER_ORCHESTRATOR_FIRST_CONTROLLED_JOB_01/90_CLOSEOUT.md`, `docs/index/inbox/GO_OPENCLAW_OPT_TRADING_CHILD_DBLAYER_ORCHESTRATOR_FIRST_CONTROLLED_JOB_01.md`

### GO_OPENCLAW_OPT_TRADING_CHILD_DBLAYER_ORCHESTRATOR_OPERATIONAL_RUNBOOK_01
- repo : opt-trading
- type : child orchestrator / runbook operationnel / db-layer
- statut : open
- titre court : runbook operationnel de l'orchestrateur OpenClaw sur db-layer
- dernier etat connu : nouveau GO doc-only pour figer le mode d'usage valide de `db-layer` apres le premier job controle ; focus sur prechecks, commandes autorisees/interdites, dry-run/read-only, logs, stop conditions, conditions avant extension write-gated
- lien utile : `docs/chantiers/GO_OPENCLAW_OPT_TRADING_CHILD_DBLAYER_ORCHESTRATOR_OPERATIONAL_RUNBOOK_01/00_INITIAL_PROJECT_DOC.md`, `docs/chantiers/GO_OPENCLAW_OPT_TRADING_CHILD_DBLAYER_ORCHESTRATOR_OPERATIONAL_RUNBOOK_01/DBLAYER_ORCHESTRATOR_OPERATIONAL_RUNBOOK_01.md`, `docs/chantiers/GO_OPENCLAW_OPT_TRADING_CHILD_DBLAYER_ORCHESTRATOR_OPERATIONAL_RUNBOOK_01/90_CLOSEOUT.md`, `docs/index/inbox/GO_OPENCLAW_OPT_TRADING_CHILD_DBLAYER_ORCHESTRATOR_OPERATIONAL_RUNBOOK_01.md`

### GO_OPENCLAW_OPT_TRADING_CHILD_DBLAYER_ORCHESTRATOR_READONLY_WORKFLOW_SMOKE_01
- repo : opt-trading
- type : child orchestrator / smoke read-only workflow / db-layer
- statut : open
- titre court : smoke read-only borne sur le workflow orchestrateur db-layer
- dernier etat connu : nouveau GO pour appliquer le runbook sur le workflow public autorise `sample-run` en mode PAPER, verifier traces, resume et clean status post-execution sans live ni secret
- lien utile : `docs/chantiers/GO_OPENCLAW_OPT_TRADING_CHILD_DBLAYER_ORCHESTRATOR_READONLY_WORKFLOW_SMOKE_01/00_INITIAL_PROJECT_DOC.md`, `docs/chantiers/GO_OPENCLAW_OPT_TRADING_CHILD_DBLAYER_ORCHESTRATOR_READONLY_WORKFLOW_SMOKE_01/DBLAYER_ORCHESTRATOR_READONLY_WORKFLOW_SMOKE_PLAN_01.md`, `docs/chantiers/GO_OPENCLAW_OPT_TRADING_CHILD_DBLAYER_ORCHESTRATOR_READONLY_WORKFLOW_SMOKE_01/DBLAYER_ORCHESTRATOR_READONLY_WORKFLOW_SMOKE_REPORT_01.md`, `docs/chantiers/GO_OPENCLAW_OPT_TRADING_CHILD_DBLAYER_ORCHESTRATOR_READONLY_WORKFLOW_SMOKE_01/90_CLOSEOUT.md`, `docs/index/inbox/GO_OPENCLAW_OPT_TRADING_CHILD_DBLAYER_ORCHESTRATOR_READONLY_WORKFLOW_SMOKE_01.md`

### GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01
- repo : opt-trading
- type : architecture documentaire / parent AI team
- statut : open
- titre court : parent canonique architecture equipe d'agents
- dernier état connu : parent materialise sur la ligne courante avec set doc-only d'ouverture complet ; branche dediee toujours active pour la suite du flux parent
- lien utile : `docs/chantiers/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01/00_cadrage.md`, `docs/chantiers/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01/01_initial_project_doc.md`, `docs/chantiers/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01/03_decisions.md`

### GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_DBLAYER_OPENCLAW_REMOTE_EXEC_CANONICALIZE_01
- repo : opt-trading
- type : child AI team / canonisation doc-only / remote exec
- statut : open
- titre court : canonisation du lot `db-layer -> OpenClaw -> SSH -> fantome`
- dernier état connu : les preuves `109/110/111` sorties du parent AI team ont ete deplacees dans un child explicite pour respecter l'invariant "pas d'execution implicite sans GO enfant" ; la sequence documentee reste `REVIEW_REQUIRED`
- lien utile : `docs/chantiers/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_DBLAYER_OPENCLAW_REMOTE_EXEC_CANONICALIZE_01/00_INITIAL_PROJECT_DOC.md`, `docs/chantiers/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_DBLAYER_OPENCLAW_REMOTE_EXEC_CANONICALIZE_01/01_REMOTE_EXEC_PLAN.md`, `docs/chantiers/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_DBLAYER_OPENCLAW_REMOTE_EXEC_CANONICALIZE_01/02_REMOTE_EXEC_LOG.md`, `docs/chantiers/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_DBLAYER_OPENCLAW_REMOTE_EXEC_CANONICALIZE_01/03_REMOTE_EXEC_STATE.md`

### GO_OPT_TRADING_CLICKUP_PARENT_CONTINUITY_01
- repo : opt-trading
- type : chantier parent / ClickUp continuity / bundle d'implémentation
- statut : open
- titre court : continuité ClickUp parent et bundle d'exécution
- dernier état connu : bundle doc-only mergé localement dans sot/mainline (c8362b7) ; closeout de phase review/merge produit ; parent non fermé
- prochaine action : recroiser avec GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01 et GO_OPT_TRADING_STRICT_WORKERS_PARENT_01, puis décider du GO d'implémentation ClickUp
- lien utile : `docs/chantiers/GO_OPT_TRADING_CLICKUP_PARENT_CONTINUITY_01/00_INITIAL_PROJECT_DOC.md`, `docs/chantiers/GO_OPT_TRADING_CLICKUP_PARENT_CONTINUITY_01/CLICKUP_IMPLEMENTATION_BUNDLE_V1/INDEX.md`, `docs/chantiers/GO_OPT_TRADING_CLICKUP_PARENT_CONTINUITY_01/90_CLOSEOUT.md`

### GO_OPT_TRADING_STRICT_WORKERS_PARENT_01
- repo : opt-trading
- type : chantier parent / strict workers / agents
- statut : open
- titre court : parent canonique strict workers IA a autonomie etroite
- dernier etat connu : dossier complet sur branche `go/GO_OPT_TRADING_STRICT_WORKERS_PARENT_01` (initial_doc, progress, smoke_exec, smoke_validation, closeout draft) ; non merge dans mainline
- prochaine action : merger le dossier dans mainline ou poursuivre sur branche, puis ouvrir le GO d'implementation strict workers
- lien utile : branche `go/GO_OPT_TRADING_STRICT_WORKERS_PARENT_01`, `docs/chantiers/GO_OPT_TRADING_STRICT_WORKERS_PARENT_01/00_INITIAL_PROJECT_DOC.md` (sur branche)

### GO_EXTRACTEUR_TAGS_CANONICAL_METHOD_01
- repo : opt-trading
- type : gouvernance / extraction / documentation
- statut : reference
- titre court : méthode canonique d’extraction par tags
- dernier état connu : fiche de référence initiale créée sur `sot/mainline` pour séparer extraction, classification, routage mémoire vs doc et écriture contrôlée
- lien utile : `docs/governance/EXTRACTEUR_TAGS__METHODE_CANONIQUE_V1.md`

### GO_OPT_TRADING_ADMIN_TRADING_RUNTIME_SYNC_AFTER_PAPER_GUARDS_01
- repo : opt-trading
- type : runtime sync / verification
- statut : COMPLETE
- titre court : sync runtime admin-trading + verification guards PAPER_TEST
- dernier etat connu : runtime synchronise sur `sot/mainline @ 50df15c3` ; `GET /api/paper/guards` retourne 200 avec guards correctement bloquants
- verdict : PASS_SYNC_BLOCKING_GUARDS
- payload PAPER_TEST : non envoyé
- lien utile : `docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_RUNTIME_SYNC_AFTER_PAPER_GUARDS_01/90_CLOSEOUT.md`

### GO_OPT_TRADING_ADMIN_TRADING_PAPER_FLAGS_CONFIG_01
- repo : opt-trading
- type : configuration / paper flags
- statut : COMPLETE
- titre court : configurer flags paper pour guards ok:true
- dernier etat connu : flags configurés sur admin-trading ; `GET /api/paper/guards` retourne `ok: true` avec tous les guards PASS
- verdict : PASS_CONFIG
- payload PAPER_TEST : non envoyé
- lien utile : `docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_PAPER_FLAGS_CONFIG_01/90_CLOSEOUT.md`

### GO_OPT_TRADING_ADMIN_TRADING_PAPER_TEST_RETRY_01
- repo : opt-trading
- type : execution / PAPER_TEST
- statut : COMPLETE
- titre court : exécution PAPER_TEST contrôlée via paper adapter
- dernier etat connu : PAPER_TEST envoyé et exécuté ; position BTC/USDT ouverte en simulation ; guards ok:true avant et après
- verdict : PASS_PAPER_TEST_EXECUTED
- payload PAPER_TEST : envoyé (paper adapter, aucun trade réel)
- lien utile : `docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_PAPER_TEST_RETRY_01/90_CLOSEOUT.md`

### GO_OPT_TRADING_ADMIN_TRADING_PAPER_POSITION_CLOSE_01
- repo : opt-trading
- type : position close / paper
- statut : COMPLETE
- titre court : fermer position paper BTC/USDT du retry
- dernier etat connu : position BTC/USDT BUY 0.1 @ 65000.0 fermée ; positions préexistantes inchangées ; guards ok:true
- verdict : PASS_POSITION_CLOSED
- payload : aucun (édition directe positions.json)
- lien utile : `docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_PAPER_POSITION_CLOSE_01/90_CLOSEOUT.md`

### GO_OPT_TRADING_ADMIN_TRADING_PAPER_TEST_CYCLE_CLOSEOUT_01
- repo : opt-trading
- type : cycle closeout / PAPER_TEST
- statut : COMPLETE
- titre court : closeout cycle PAPER_TEST complet
- dernier etat connu : cycle complet validé (guards → exec → tracking → close) ; aucun trade réel ; guards ok:true
- verdict : PASS_CYCLE_COMPLETE
- payload : aucun (documentation only)
- lien utile : `docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_PAPER_TEST_CYCLE_CLOSEOUT_01/90_CLOSEOUT.md`

### GO_OPT_TRADING_ADMIN_TRADING_PAPER_SCENARIOS_EXPANSION_01
- repo : opt-trading
- type : paper scenarios / expansion
- statut : COMPLETE
- titre court : scénarios paper additionnels (SELL, invalid, guard fail, ledger)
- dernier etat connu : 5/5 scénarios PASS ; positions nettoyées ; guards ok:true
- verdict : PASS_ALL_SCENARIOS
- payload : PAPER_TEST (paper adapter)
- lien utile : `docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_PAPER_SCENARIOS_EXPANSION_01/90_CLOSEOUT.md`

### GO_OPT_TRADING_ADMIN_TRADING_PAPER_VALIDATION_GLOBAL_CLOSEOUT_01
- repo : opt-trading
- type : global closeout / paper validation
- statut : COMPLETE
- titre court : closeout global validation paper admin-trading
- dernier etat connu : 10 PRs/GOs consolidés ; preuves collectées ; conditions production définies ; production non ouverte
- verdict : PASS_GLOBAL_PAPER_VALIDATION
- payload : aucun (doc-only)
- lien utile : `docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_PAPER_VALIDATION_GLOBAL_CLOSEOUT_01/90_CLOSEOUT.md`

### GO_OPT_TRADING_ADMIN_TRADING_PRODUCTION_READINESS_CONDITIONS_01
- repo : opt-trading
- type : production readiness / conditions
- statut : COMPLETE
- titre court : conditions production readiness admin-trading
- dernier etat connu : 7 conditions évaluées (0 SATISFIED, 2 PARTIAL, 4 MISSING, 1 BLOCKED) ; production non ouverte
- verdict : PASS_CONDITIONS_DEFINED
- payload : aucun (doc-only)
- lien utile : `docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_PRODUCTION_READINESS_CONDITIONS_01/90_CLOSEOUT.md`

### GO_OPT_TRADING_ADMIN_TRADING_PRODUCTION_RISK_LIMITS_AND_KILL_SWITCH_01
- repo : opt-trading
- type : production readiness / risk limits + kill switch
- statut : COMPLETE
- titre court : spécification risk limits et kill switch production
- dernier etat connu : risk limits et kill switch spécifiés ; rollback plan documenté ; validation gates définis ; production non ouverte
- verdict : PARTIAL (spécifié, non implémenté)
- payload : aucun (doc-only)
- lien utile : `docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_PRODUCTION_RISK_LIMITS_AND_KILL_SWITCH_01/90_CLOSEOUT.md`

### GO_OPT_TRADING_ADMIN_TRADING_PRODUCTION_RISK_LIMITS_AND_KILL_SWITCH_IMPL_01
- repo : opt-trading
- type : implementation / risk limits + kill switch
- statut : COMPLETE
- titre court : implémentation risk limits et kill switch
- dernier etat connu : risk limits et kill switch implémentés et testés ; endpoints fonctionnels ; production non ouverte
- verdict : PASS_IMPLEMENTED
- payload : aucun (runtime changes only)
- lien utile : `docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_PRODUCTION_RISK_LIMITS_AND_KILL_SWITCH_IMPL_01/90_CLOSEOUT.md`

### GO_OPT_TRADING_ADMIN_TRADING_PRODUCTION_MONITORING_AND_SECRETS_AUDIT_01
- repo : opt-trading
- type : production readiness / monitoring + secrets audit
- statut : COMPLETE
- titre court : audit monitoring et secrets admin-trading
- dernier etat connu : monitoring PARTIAL (services actifs, P&L manquant) ; secrets PARTIAL (TV_WEBHOOK_KEY non défini) ; production non ouverte
- verdict : PARTIAL
- payload : aucun (doc-only)
- lien utile : `docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_PRODUCTION_MONITORING_AND_SECRETS_AUDIT_01/90_CLOSEOUT.md`

### GO_OPT_TRADING_ADMIN_TRADING_PRODUCTION_MONITORING_PNL_ALERT_THRESHOLDS_01
- repo : opt-trading
- type : production readiness / monitoring spec
- statut : COMPLETE
- titre court : spécification P&L tracking et alert thresholds
- dernier etat connu : P&L tracking et alert thresholds spécifiés ; monitoring reste PARTIAL ; production non ouverte
- verdict : PARTIAL (spécifié, non implémenté)
- payload : aucun (doc-only)
- lien utile : `docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_PRODUCTION_MONITORING_PNL_ALERT_THRESHOLDS_01/90_CLOSEOUT.md`
