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
updated_at: 2026-04-25
links:
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
  - docs/index/GO_INDEX.md
  - docs/index/ACTIVE_STREAMS.md
---

# REPRISE — opt-trading

## Point de reprise

Base de pilotage active retenue pour `opt-trading` :

- perimetre = **14 GO non clos retenus** (`active` / `open`)
- canon décisionnel = **état réel du repo `opt-trading`, relu sous la matrice maître**
- bundles zip = **supports secondaires** de lecture, transfert ou exécution IDE
- exclusion explicite = `pass` et `reference` hors exécution courante

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
- **Liste active a piloter** : strictement les 14 GO ci-dessous

## Matrice de reprise canonique

| GO | status | priority | repo canonical refs | supports secondaires (noms) | etat etabli | gap restant | next action |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01` | open | P1 | `docs/chantiers/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01/PARENT_STATE.md`; `docs/chantiers/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01/INDEX_PATCH.md`; `docs/governance/PARENT_CONTINUITY_INDEX_INBOX_METHOD_01.md` | continuitÃ© parent locale complÃ¨te posÃ©e ; mÃ©thode local-first et inbox atomique mergÃ©es ; OpenClaw bornÃ© hors runtime dans ce chantier | entrÃ©e d'index agrÃ©gÃ©e par `GO_OPT_TRADING_INDEX_AGGREGATION_BATCH_01`; closeout final Ã©ventuel Ã  produire | ouvrir `GO_OPT_TRADING_PARENT_CONTINUITY_INDEX_INBOX_METHOD_01` seulement si une promotion additionnelle est requise, sinon surveiller les prochains INDEX_PATCH |
| `GO_OPT_TRADING_DOC_OPS_PARENT_PROJECT_MACHINE_SPLIT_01` | open | P0 | `docs/chantiers/GO_OPT_TRADING_DOC_OPS_PARENT_PROJECT_MACHINE_SPLIT_01/01_cadrage_parent.md`; `docs/chantiers/GO_OPT_TRADING_DOC_OPS_PARENT_PROJECT_MACHINE_SPLIT_01/02_go_map.md` | Aucun bundle canonique | Parent canonique de reprise repo-first ouvert ; l'ordre de session est figé et l'ouverture des 5 parents spécialisés est explicitement différée | Qualification des branches ouvertes / merged / de référence, contrôle des ouverts / non terminés, choix du flux principal unique, puis seulement carte cible future et ouverture canonique des 5 parents | **Exécuter `GO_OPT_TRADING_DOC_OPS_CHILD_BRANCH_CLEANUP_01`, puis `GO_OPT_TRADING_DOC_OPS_CHILD_OPEN_WORK_CONTROL_01`** |
| `GO_OPT_TRADING_DOC_OPS_CHILD_ARBITRAGE_SEED_01` | closeout | P0 | `docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_ARBITRAGE_SEED_01/00_cadrage.md`; `docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_ARBITRAGE_SEED_01/90_closeout.md` | Seed arbitration closeout artifacts | Arbitre seed closout effectué pour 7 seeds; prêt pour passage au restart | GO_OPT_TRADING_DOC_OPS_CHILD_PRIMARY_RESTART_01 |
| `GO_OPT_TRADING_CONTINUITY_INDEX_REALIGNMENT_01` | active | P0 | `docs/chantiers/GO_OPT_TRADING_CONTINUITY_INDEX_REALIGNMENT_01/00_cadrage.md`; `docs/chantiers/GO_OPT_TRADING_CONTINUITY_INDEX_REALIGNMENT_01/03_decisions.md` | Aucun bundle canonique | Chantier parent ouvert pour réaligner la continuité index | Contradictions d’index + concurrence NEXT + hiérarchie journal à propager | **Exécuter LOT 1 : réaligner `docs/index/*` et déclasser `docs/next/NEXT_GO_CANDIDATES.md`** |
| `GO_TMUX_IDE_OPT_TRADING_CADRAGE_01` | active | P0 | `docs/chantiers/GO_TMUX_IDE_OPT_TRADING_CADRAGE_01/00_cadrage.md` | `GO_TMUX_IDE_OPT_TRADING_CADRAGE_01_bundle.zip`; `consolidation_targets_ide_bundle.zip` | Bundle préparé, cadrage ouvert | Validation machine cible / panes / repo réel non prouvée | **Exécuter `GO_TMUX_IDE_OPT_TRADING_IMPL_BASE_01`** |
| `GO_OPT_TRADING_OBSOLETE_RECLASS_ARCHIVE_AUDIT_01` | active | P0 | `docs/chantiers/GO_OPT_TRADING_OBSOLETE_RECLASS_ARCHIVE_AUDIT_01/00_cadrage.md`; `docs/chantiers/GO_OPT_TRADING_OBSOLETE_RECLASS_ARCHIVE_AUDIT_01/03_decisions.md` | `OPT_TRADING_OBSOLETE_RECLASS_AUDIT_BUNDLE.zip` | Parent ouvert (audit/qualification repo-first, doc-only, non destructif) | Matrice canonique à produire + plan de lots physiques futurs | **Produire la matrice (PHASE C) puis le plan de lots (PHASE D)** |
| `GO_OPT_TRADING_CANON_STRUCTURE_REALIGNMENT_01` | active | P1 | `docs/chantiers/GO_OPT_TRADING_CANON_STRUCTURE_REALIGNMENT_01/00_cadrage.md`; `docs/chantiers/GO_OPT_TRADING_CANON_STRUCTURE_REALIGNMENT_01/03_decisions.md` | Aucun bundle canonique | Parent PHASE 2 LOT 3 ouvert ; carte humaine des surfaces publiée | Arbitrages de structure canonique à poursuivre selon écarts réels | **Consolider la carte des surfaces et ses points d’ancrage sans dupliquer `registry/*`** |
| `GO_OPT_TRADING_ROOT_POLICY_AND_RECLASS_01` | active | P1 | `docs/chantiers/GO_OPT_TRADING_ROOT_POLICY_AND_RECLASS_01/00_cadrage.md`; `docs/chantiers/GO_OPT_TRADING_ROOT_POLICY_AND_RECLASS_01/03_decisions.md` | Aucun bundle canonique | Parent PHASE 2 LOT 4 ouvert ; politique racine posée | Arbitrages de reclassement racine encore ouverts | **Consolider les classes racine et les arbitrages documentés sans chevaucher la politique frontière** |
| `GO_OPT_TRADING_TRAE_PACK_TEXTS_REVISION_01` | active | P1 | `docs/chantiers/GO_OPT_TRADING_TRAE_PACK_TEXTS_REVISION_01/00_cadrage.md`; `docs/chantiers/GO_OPT_TRADING_TRAE_PACK_TEXTS_REVISION_01/03_decisions.md`; `docs/ot/trae/README.md`; `docs/ot/trae/trae_pack_texts/README.md` | Aucun bundle canonique | `trae_pack_texts/` est désormais rangé sous `docs/ot/trae/trae_pack_texts/` ; `README.md` porte l'usage vivant et `trae_pack/` reste une archive de lecture compatible doc/IDE | Vérifier si le lot peut être clos doc-only sans casser les références historiques déjà publiées | **Confirmer le gel du pack legacy après push et n'ouvrir un nouveau lot que si un helper repo-native manque réellement** |
| `GO_OPT_TRADING_RUNTIME_EXCEPTION_FAMILIES_01` | active | P1 | `docs/chantiers/GO_OPT_TRADING_RUNTIME_EXCEPTION_FAMILIES_01/00_cadrage.md`; `docs/chantiers/GO_OPT_TRADING_RUNTIME_EXCEPTION_FAMILIES_01/03_decisions.md` | Aucun bundle canonique | Parent PHASE 3 LOT 5 ouvert ; fiches status courtes publiées | Arbitrages de lignée encore ouverts sur plusieurs familles mixtes | **Consolider survivant/transition/legacy/archive en gap-only** |
| `GO_OPT_TRADING_REGISTRY_SCOPE_REALIGNMENT_01` | active | P1 | `docs/chantiers/GO_OPT_TRADING_REGISTRY_SCOPE_REALIGNMENT_01/00_cadrage.md`; `docs/chantiers/GO_OPT_TRADING_REGISTRY_SCOPE_REALIGNMENT_01/03_decisions.md` | Aucun bundle canonique | Parent PHASE 3 LOT 6 ouvert ; scope/exception clarifiés dans `registry/README.md` | Couverture déclarative à consolider sans dérive doctrinale | **Poursuivre l’alignement scope registry via la source canonique unique** |
| `GO_GIT_PROGRESSIVE_MIGRATION_START_13` | active | P1 | `docs/chantiers/GO_GIT_PROGRESSIVE_MIGRATION_START_13/00_cadrage.md` | `zip_repos_audit_bundle.zip`; `zip_repos_audit_synthese_complete.md`; `zip_repos_audit_synthese_complete.json`; `zip_docs_line_reading_complete.md` | Dossier minimal ouvert pour GO actif | Suite autonome encore insuffisamment explicitée | **Formaliser la suite opératoire dédiée du chantier de migration avant tout lot d’exécution** |
| `GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03` | open | P1 | `docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03/00_cadrage.md`; `docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_CANONICAL_RENAME_REGISTRY_01/01_plan_operationnel_step_by_step.md`; `docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_MACHINE_SIDE_REPOINT_01/10_step_09_execution_resultats.md` | `reseau_ssh_physical_consolidation_bundle_01.zip` | `db-layer`, `admin-trading`, `student` et `fantome` ont leurs alias courts repointés vers `modules/reseau_ssh/scripts/*` avec PASS ; `step1b` et `scripts/reseau_ssh` restent en compat | Reste a arbitrer la reduction des compatibilites et le retrait progressif des anciens points d'entree | **Ouvrir le lot de réduction de compatibilité sur `scripts/reseau_ssh`, puis qualifier `step1b`** |
| `GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01` | open | P2 | `docs/index/GO_INDEX.md`; `docs/chantiers/GO_GIT_AI_TEAM_ARCHITECTURE_PARENT_DOC_ONLY_INTEGRATION_01/03_decisions.md` | Aucun bundle dédié identifié | Parent AI team intégré doc-only dans `GO_INDEX.md` avec statut `OPEN` | Dossier parent complet non matérialisé dans cette copie locale ; reprise enfant encore non réouverte | **Utiliser l’entrée `OPEN` comme base si un GO enfant d’audit documentaire doit être relancé** |
| `GO_OPT_TRADING_MATRICE_GOUVERNANTE_METADATA_DERIVATION_01` | open | P2 | `docs/chantiers/GO_OPT_TRADING_MATRICE_GOUVERNANTE_METADATA_DERIVATION_01/00_cadrage.md`; `docs/chantiers/GO_OPT_TRADING_MATRICE_GOUVERNANTE_METADATA_DERIVATION_01/03_decisions.md`; `docs/governance/MATRICE_GOUVERNANTE_METADATA_DERIVATION_01.md` | Aucun bundle canonique | Doctrine légère de dérivation ouverte, bornée à un pilote documentaire post-maître | Pilotage borné encore à finir avant toute extension plus large | **Poursuivre le pilote documentaire borné sans rouvrir la matrice ni la synchronisation réelle** |
| `GO_OPT_TRADING_PARENT_NAMING_CANON_01` | open | P2 | `docs/chantiers/GO_OPT_TRADING_PARENT_NAMING_CANON_01/01_cadrage_parent.md`; `docs/governance/NAMING_CANON_POLICY_01.md` | Aucun bundle canonique | Parent naming ouvert en audit-only ; aucun renommage réel inclus dans le lot initial | Inventaire réel, rapport V1 du module et qualification des exceptions legacy restent à produire | **Reprendre sur `GO_OPT_TRADING_CHILD_NAMING_INVENTORY_01` avant tout lot d’application** |
