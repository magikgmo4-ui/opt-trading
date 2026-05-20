---
doc_id: OPT_TRADING_REPRISE
doc_type: reprise
repo: opt-trading
project: opt-trading
module:
go_id:
status: reference
lifecycle_stage: reprise
topic_keys:
  - opt-trading
  - reprise
  - continuity
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
point_de_reprise: "Section Matrice de reprise canonique"
updated_at: 2026-05-20
links:
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
  - docs/index/GO_INDEX.md
  - docs/index/ACTIVE_STREAMS.md
---

# REPRISE — opt-trading

## Point de reprise

Base de pilotage active retenue pour `opt-trading` :

- perimetre = **8 GO non clos retenus** dans la priorisation resserree (`active` / `open`)
- canon décisionnel = **état réel du repo `opt-trading`, relu sous la matrice maître**
- bundles zip = **supports secondaires** de lecture, transfert ou exécution IDE
- exclusion explicite = `pass` et `reference` hors exécution courante
- `GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01` et `GO_OPT_TRADING_CLICKUP_PARENT_CONTINUITY_01` restent `OPEN` dans `GO_INDEX.md`, mais hors pilotage immédiat de cette passe resserrée

## Runtime (hors matrice active)

- runtime continuity pointer :
  - docs/chantiers/GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01/03_decisions.md

- état télécommande distante (figé) :
  - implémentation non stabilisée (verdict PARTIAL)
  - prochaine reprise sur tranche minimale lecture / statut / confirmation

## Sources canoniques

- `docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md`
- `docs/index/ACTIVE_STREAMS.md`
- `docs/index/GO_INDEX.md`

## Règle d’exécution

- **Source canonique principale** : état réel prouvé du repo `opt-trading`
- **Hiérarchie de lecture** : état réel -> `MATRICE_DOC_OPS_MASTER_MATRIX_01.md` -> annexes stables -> `GO_INDEX.md` -> surfaces opératoires
- **Bundles zip** : accélérateurs de lecture / transfert / exécution IDE
- **Présence dans le repo** : les bundles et supports listés ici sont des noms de supports secondaires ; ils peuvent être absents du repo (non trackés)
- **Interdiction de dérive** : un bundle zip ne remplace jamais l’état réel du repo
- **Extraction de continuité** : seuls les resultats documentaires extraits conserves sous `docs/governance/HUMAN_*` font encore foi comme archive utile
- **Liste active a piloter** : les 8 GO de la priorisation resserree ci-dessous, avec maintien du parent multi-agents comme reprise locale hors absorption

## Matrice de reprise canonique

| GO | status | priority | repo canonical refs | supports secondaires (noms) | etat etabli | gap restant | next action |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01` | open | P1 | `docs/chantiers/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01/PARENT_STATE.md`; `docs/chantiers/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01/INDEX_PATCH.md`; `docs/governance/PARENT_CONTINUITY_INDEX_INBOX_METHOD_01.md` | continuitÃ© parent locale complÃ¨te posÃ©e ; mÃ©thode local-first et inbox atomique mergÃ©es ; OpenClaw bornÃ© hors runtime dans ce chantier | entrÃ©e d'index agrÃ©gÃ©e par `GO_OPT_TRADING_INDEX_AGGREGATION_BATCH_01`; closeout final Ã©ventuel Ã  produire | ouvrir `GO_OPT_TRADING_PARENT_CONTINUITY_INDEX_INBOX_METHOD_01` seulement si une promotion additionnelle est requise, sinon surveiller les prochains INDEX_PATCH |
| `GO_TMUX_IDE_OPT_TRADING_CADRAGE_01` | active | P0 | `docs/chantiers/GO_TMUX_IDE_OPT_TRADING_CADRAGE_01/00_cadrage.md`; `docs/chantiers/GO_OPT_TRADING_CLAUDE_COWORK_CHILD_ATTENTION_CENTER_REAL_RUN_01/90_CLOSEOUT.md` | `GO_TMUX_IDE_OPT_TRADING_CADRAGE_01_bundle.zip`; `consolidation_targets_ide_bundle.zip` | Bundle prepare, cadrage ouvert, real run Attention Center passe et merge | Validation machine cible / panes / repo reel non prouvee | **Executer `GO_TMUX_IDE_OPT_TRADING_IMPL_BASE_01`** (machine cible a verifier avant execution ; OpenClaw hors scope) |
| `GO_OPT_TRADING_RUNTIME_EXCEPTION_FAMILIES_01` | active | P1 | `docs/chantiers/GO_OPT_TRADING_RUNTIME_EXCEPTION_FAMILIES_01/00_cadrage.md`; `docs/chantiers/GO_OPT_TRADING_RUNTIME_EXCEPTION_FAMILIES_01/03_decisions.md` | Aucun bundle canonique | Parent PHASE 3 LOT 5 ouvert ; fiches status courtes publiées | Arbitrages de lignée encore ouverts sur plusieurs familles mixtes | **Consolider survivant/transition/legacy/archive en gap-only** |
| `GO_GIT_PROGRESSIVE_MIGRATION_START_13` | active | P1 | `docs/chantiers/GO_GIT_PROGRESSIVE_MIGRATION_START_13/00_cadrage.md` | `zip_repos_audit_bundle.zip`; `zip_repos_audit_synthese_complete.md`; `zip_repos_audit_synthese_complete.json`; `zip_docs_line_reading_complete.md` | Dossier minimal ouvert pour GO actif | Suite autonome encore insuffisamment explicitée | **Formaliser la suite opératoire dédiée du chantier de migration avant tout lot d’exécution** |
| `GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03` | open | P1 | `docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03/00_cadrage.md`; `docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_CANONICAL_RENAME_REGISTRY_01/01_plan_operationnel_step_by_step.md`; `docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_MACHINE_SIDE_REPOINT_01/10_step_09_execution_resultats.md` | `reseau_ssh_physical_consolidation_bundle_01.zip` | `db-layer`, `admin-trading`, `student` et `fantome` ont leurs alias courts repointés vers `modules/reseau_ssh/scripts/*` avec PASS ; `step1b` et `scripts/reseau_ssh` restent en compat | Reste a arbitrer la reduction des compatibilites et le retrait progressif des anciens points d'entree | **Ouvrir le lot de réduction de compatibilité sur `scripts/reseau_ssh`, puis qualifier `step1b`** |
| `GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01` | open | P2 | `docs/index/GO_INDEX.md`; `docs/chantiers/GO_GIT_AI_TEAM_ARCHITECTURE_PARENT_DOC_ONLY_INTEGRATION_01/03_decisions.md` | Aucun bundle dédié identifié | Parent AI team intégré doc-only dans `GO_INDEX.md` avec statut `OPEN` | Dossier parent complet non matérialisé dans cette copie locale ; reprise enfant encore non réouverte | **Utiliser l’entrée `OPEN` comme base si un GO enfant d’audit documentaire doit être relancé** |
| `GO_OPT_TRADING_AI_STRICT_WORKERS_APPS_CLASSIFICATION_01` | open | P2 | `docs/chantiers/GO_OPT_TRADING_AI_STRICT_WORKERS_APPS_CLASSIFICATION_01/00_classification_matrix.md` | Aucun bundle dédié identifié | PR #645 mergee ; matrice bucketisee disponible sur `sot/mainline` | Le decoupage est pose mais ne doit pas etre melange a nouveau dans un chantier unique | **Reprendre uniquement par bucket deja classe, sans relancer de discovery globale** |
| `GO_OPT_TRADING_STRICT_WORKERS_ORCHESTRATION_DEPLOYMENT_CLASSIFICATION_REVIEW_01` | open | P2 | `docs/chantiers/GO_OPT_TRADING_STRICT_WORKERS_ORCHESTRATION_DEPLOYMENT_CLASSIFICATION_REVIEW_01/00_INITIAL_PROJECT_DOC.md`; `docs/chantiers/GO_OPT_TRADING_STRICT_WORKERS_ORCHESTRATION_DEPLOYMENT_CLASSIFICATION_REVIEW_01/20_CLASSIFICATION_REVIEW.md`; `docs/chantiers/GO_OPT_TRADING_STRICT_WORKERS_ORCHESTRATION_DEPLOYMENT_CLASSIFICATION_REVIEW_01/90_REPRISE_POINT.md` | Aucun bundle dédié identifié | PR #646 mergee ; bucket 1 strict-workers orchestration/deployment est ouvert en revue doc-only read-only | La suite implementation repo-only n'est pas encore decidee | **Valider humainement le bucket 1 puis choisir entre GO deploy/workflows et GO `machine_runtime_map`** |
