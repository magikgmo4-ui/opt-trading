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
surface: chantier
source_kind: canonical
updated_at: 2026-04-20
links:
  - docs/governance/REPO_ROLE.md
  - docs/governance/DOC_LAYERS.md
---

# GO_INDEX — opt-trading

## Objet

Ce document référence les GO non clos connus et utiles à la continuité locale de `opt-trading`.

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
- lorsqu’un chantier passe en `CLOSED`/`PASS`, il doit être retiré de `docs/index/GO_INDEX.md` et déplacé dans `docs/index/GO_CLOSED_INDEX.md`
- les entrées `REFERENCE` peuvent rester dans `GO_INDEX.md` si elles sont utiles à la continuité active et ne correspondent pas à une clôture
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
| GO_UNIFORM_CONTINUITY_FINAL_MASTER_PLAN_01 | GO_UNIFORM_CONTINUITY_FINAL_MASTER_PLAN_01 | — | REFERENCE | oui | `docs/index/GO_INDEX.md`<br>`docs/chantiers/GO_UNIFORM_CONTINUITY_FINAL_MASTER_PLAN_01/00_cadrage.md` |
| GO_GIT_PROGRESSIVE_MIGRATION_START_13 | GO_GIT_PROGRESSIVE_MIGRATION_START_13 | — | ACTIVE | oui | `docs/index/GO_INDEX.md`<br>`docs/chantiers/GO_GIT_PROGRESSIVE_MIGRATION_START_13/00_cadrage.md` |
| GO_OPT_TRADING_CONTINUITY_INDEX_REALIGNMENT_01 | GO_OPT_TRADING_CONTINUITY_INDEX_REALIGNMENT_01 | — | ACTIVE | oui | `docs/index/GO_INDEX.md`<br>`docs/chantiers/GO_OPT_TRADING_CONTINUITY_INDEX_REALIGNMENT_01/00_cadrage.md`<br>`docs/chantiers/GO_OPT_TRADING_CONTINUITY_INDEX_REALIGNMENT_01/03_decisions.md` |
| GO_OPT_TRADING_CANON_STRUCTURE_REALIGNMENT_01 | GO_OPT_TRADING_CANON_STRUCTURE_REALIGNMENT_01 | — | ACTIVE | oui | `docs/index/GO_INDEX.md`<br>`docs/chantiers/GO_OPT_TRADING_CANON_STRUCTURE_REALIGNMENT_01/00_cadrage.md`<br>`docs/chantiers/GO_OPT_TRADING_CANON_STRUCTURE_REALIGNMENT_01/03_decisions.md`<br>`docs/architecture/REPO_SURFACES_MAP.md` |
| GO_OPT_TRADING_ROOT_POLICY_AND_RECLASS_01 | GO_OPT_TRADING_ROOT_POLICY_AND_RECLASS_01 | — | ACTIVE | oui | `docs/index/GO_INDEX.md`<br>`docs/chantiers/GO_OPT_TRADING_ROOT_POLICY_AND_RECLASS_01/00_cadrage.md`<br>`docs/chantiers/GO_OPT_TRADING_ROOT_POLICY_AND_RECLASS_01/03_decisions.md`<br>`docs/governance/REPO_ROOT_POLICY.md` |
| GO_OPT_TRADING_OBSOLETE_RECLASS_ARCHIVE_AUDIT_01 | GO_OPT_TRADING_OBSOLETE_RECLASS_ARCHIVE_AUDIT_01 | — | ACTIVE | oui | `docs/index/GO_INDEX.md`<br>`docs/chantiers/GO_OPT_TRADING_OBSOLETE_RECLASS_ARCHIVE_AUDIT_01/00_cadrage.md`<br>`docs/chantiers/GO_OPT_TRADING_OBSOLETE_RECLASS_ARCHIVE_AUDIT_01/03_decisions.md` |
| GO_OPT_TRADING_RUNTIME_EXCEPTION_FAMILIES_01 | GO_OPT_TRADING_RUNTIME_EXCEPTION_FAMILIES_01 | — | ACTIVE | oui | `docs/index/GO_INDEX.md`<br>`docs/chantiers/GO_OPT_TRADING_RUNTIME_EXCEPTION_FAMILIES_01/00_cadrage.md`<br>`docs/chantiers/GO_OPT_TRADING_RUNTIME_EXCEPTION_FAMILIES_01/03_decisions.md` |
| GO_OPT_TRADING_REGISTRY_SCOPE_REALIGNMENT_01 | GO_OPT_TRADING_REGISTRY_SCOPE_REALIGNMENT_01 | — | ACTIVE | oui | `docs/index/GO_INDEX.md`<br>`docs/chantiers/GO_OPT_TRADING_REGISTRY_SCOPE_REALIGNMENT_01/00_cadrage.md`<br>`docs/chantiers/GO_OPT_TRADING_REGISTRY_SCOPE_REALIGNMENT_01/03_decisions.md`<br>`registry/README.md` |
| GO_COLLECTORS_LIFECYCLE_COMPAT_CADRAGE_01 | GO_COLLECTORS_LIFECYCLE_COMPAT_CADRAGE_01 | — | OPEN | non | `docs/index/GO_INDEX.md`<br>`docs/COLLECTORS_LIFECYCLE_COMPAT_SPEC_01.md` |
| GO_OPT_TRADING_JOURNAL_CANON_INTENT_LAYER_04 | GO_OPT_TRADING_JOURNAL_CANON_INTENT_LAYER_04 | — | ACTIVE | oui | `docs/index/GO_INDEX.md`<br>`docs/chantiers/GO_OPT_TRADING_JOURNAL_CANON_INTENT_LAYER_04/00_cadrage.md` |
| GO_OPT_TRADING_JOURNAL_FULL_READING_03 | GO_OPT_TRADING_JOURNAL_FULL_READING_03 | — | ACTIVE | oui | `docs/index/GO_INDEX.md`<br>`docs/chantiers/GO_OPT_TRADING_JOURNAL_FULL_READING_03/00_cadrage.md` |
| GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03 | GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03 | — | OPEN | oui | `docs/index/GO_INDEX.md`<br>`docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03/00_cadrage.md` |
| GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03 | GO_OPT_TRADING_RESEAU_SSH_UNIFIED_MODULE_CADRAGE_01 | — | OPEN | oui | `docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_UNIFIED_MODULE_CADRAGE_01/00_cadrage.md`<br>`docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03/00_cadrage.md` |
| GO_TMUX_IDE_OPT_TRADING_CADRAGE_01 | GO_TMUX_IDE_OPT_TRADING_CADRAGE_01 | — | ACTIVE | oui | `docs/index/GO_INDEX.md`<br>`docs/chantiers/GO_TMUX_IDE_OPT_TRADING_CADRAGE_01/00_cadrage.md` |
| GO_LOCALCMS_FORMS_INTEGRATION_DOC_01 | GO_LOCALCMS_FORMS_INTEGRATION_DOC_01 | — | OPEN | oui | `docs/index/GO_INDEX.md`<br>`docs/chantiers/GO_LOCALCMS_FORMS_INTEGRATION_DOC_01/00_cadrage.md` |
| GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01 | GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01 | — | OPEN | oui | `docs/index/GO_INDEX.md`<br>`docs/chantiers/GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01/01_cadrage_parent.md` |
| GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01 | GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01 | GO_OPT_TRADING_UI_LOCALCMS_INVENTORY_01 | REFERENCE | non | `docs/chantiers/GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01/01_cadrage_parent.md` |
| GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01 | GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01 | GO_OPT_TRADING_UI_LOCALCMS_MATRIX_01 | REFERENCE | non | `docs/chantiers/GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01/01_cadrage_parent.md` |
| GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01 | GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01 | GO_OPT_TRADING_UI_LOCALCMS_CONTRACTS_01 | REFERENCE | non | `docs/chantiers/GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01/01_cadrage_parent.md` |
| GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01 | GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01 | GO_OPT_TRADING_UI_LOCALCMS_PILOT_READONLY_01 | REFERENCE | non | `docs/chantiers/GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01/01_cadrage_parent.md` |
| GO_EXTRACTEUR_TAGS_CANONICAL_METHOD_01 | GO_EXTRACTEUR_TAGS_CANONICAL_METHOD_01 | — | REFERENCE | oui | `docs/index/GO_INDEX.md`<br>`docs/chantiers/GO_EXTRACTEUR_TAGS_CANONICAL_METHOD_01/EXTRACTEUR_TAGS__METHODE_CANONIQUE_V1.md` |
| GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01 | GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01 | — | ACTIVE | oui | `docs/chantiers/GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01/00_cadrage.md`<br>`docs/index/REPRISE.md` |
| GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01 | GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01 | GO_TMUX_RUNTIME_CONVENTIONS_01 | REFERENCE | non | `docs/chantiers/GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01/00_cadrage.md` |
| GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01 | GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01 | GO_OPENCLAW_COMMAND_SCOPE_01 | REFERENCE | non | `docs/chantiers/GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01/00_cadrage.md` |
| GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01 | GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01 | GO_TMUX_RUNTIME_CONTRACT_01 | REFERENCE | non | `docs/chantiers/GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01/00_cadrage.md` |
| GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01 | GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01 | GO_TMUX_OPENCODE_OPENCLAW_MODES_01 | REFERENCE | non | `docs/chantiers/GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01/00_cadrage.md` |
| GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01 | GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01 | GO_RUNTIME_GUARDRAILS_01 | REFERENCE | non | `docs/chantiers/GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01/00_cadrage.md` |

---

## Priorité opératoire (11 GO non clos)

- P0 : `GO_OPT_TRADING_CONTINUITY_INDEX_REALIGNMENT_01`, `GO_TMUX_IDE_OPT_TRADING_CADRAGE_01`, `GO_OPT_TRADING_OBSOLETE_RECLASS_ARCHIVE_AUDIT_01`
- P1 : `GO_OPT_TRADING_CANON_STRUCTURE_REALIGNMENT_01`, `GO_OPT_TRADING_ROOT_POLICY_AND_RECLASS_01`, `GO_OPT_TRADING_RUNTIME_EXCEPTION_FAMILIES_01`, `GO_OPT_TRADING_REGISTRY_SCOPE_REALIGNMENT_01`, `GO_GIT_PROGRESSIVE_MIGRATION_START_13`, `GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03`
- P2 : `GO_OPT_TRADING_JOURNAL_FULL_READING_03`, `GO_OPT_TRADING_JOURNAL_CANON_INTENT_LAYER_04`

Le passage de 10 à 11 GO non clos correspond à l’ouverture du parent :
- `GO_OPT_TRADING_OBSOLETE_RECLASS_ARCHIVE_AUDIT_01`

Historique (PHASE 4) :
- le passage de 10 à 11 GO non clos a correspondu à l’ouverture de `GO_APPLY_UNIFORM_WORKFLOW_MEMORY_DOCUMENTATION_01`
- ce GO est clos (PASS), donc il reste hors exécution courante

Le passage de 8 à 10 GO non clos correspond à l’ouverture PHASE 3 des parents :
- `GO_OPT_TRADING_RUNTIME_EXCEPTION_FAMILIES_01`
- `GO_OPT_TRADING_REGISTRY_SCOPE_REALIGNMENT_01`

Le passage de 6 à 8 GO non clos correspond à l’ouverture PHASE 2 des parents :
- `GO_OPT_TRADING_CANON_STRUCTURE_REALIGNMENT_01`
- `GO_OPT_TRADING_ROOT_POLICY_AND_RECLASS_01`

---

## Entrées

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

### GO_OPT_TRADING_CONTINUITY_INDEX_REALIGNMENT_01
- repo : opt-trading
- type : patch local / doc-only
- statut : active
- titre court : réalignement continuité index
- dernier état connu : chantier parent ouvert pour réaligner `docs/index/*` et déclasser `docs/next/NEXT_GO_CANDIDATES.md`
- lien utile : `docs/chantiers/GO_OPT_TRADING_CONTINUITY_INDEX_REALIGNMENT_01/00_cadrage.md`, `docs/chantiers/GO_OPT_TRADING_CONTINUITY_INDEX_REALIGNMENT_01/03_decisions.md`

### GO_OPT_TRADING_CANON_STRUCTURE_REALIGNMENT_01
- repo : opt-trading
- type : patch local / doc-only
- statut : active
- titre court : carte canonique des surfaces du repo
- dernier état connu : parent PHASE 2 LOT 3 ouvert ; carte humaine `REPO_SURFACES_MAP.md` posée sans duplication de `registry/*`
- lien utile : `docs/chantiers/GO_OPT_TRADING_CANON_STRUCTURE_REALIGNMENT_01/00_cadrage.md`, `docs/chantiers/GO_OPT_TRADING_CANON_STRUCTURE_REALIGNMENT_01/03_decisions.md`, `docs/architecture/REPO_SURFACES_MAP.md`

### GO_OPT_TRADING_ROOT_POLICY_AND_RECLASS_01
- repo : opt-trading
- type : patch local / doc-only
- statut : active
- titre court : politique racine canonique interne du repo
- dernier état connu : parent PHASE 2 LOT 4 ouvert ; `REPO_ROOT_POLICY.md` posé sans redéfinir la frontière repo/hors-repo
- lien utile : `docs/chantiers/GO_OPT_TRADING_ROOT_POLICY_AND_RECLASS_01/00_cadrage.md`, `docs/chantiers/GO_OPT_TRADING_ROOT_POLICY_AND_RECLASS_01/03_decisions.md`, `docs/governance/REPO_ROOT_POLICY.md`

### GO_OPT_TRADING_OBSOLETE_RECLASS_ARCHIVE_AUDIT_01
- repo : opt-trading
- type : audit / qualification / préparation reclassement physique
- statut : active
- titre court : audit obsolete / déclassé / archive / legacy / sous arbitrage
- dernier état connu : parent ouvert (audit repo-first non destructif) ; groupes racine / workflow_post_change / docs historiques / supports locaux ciblés
- lien utile : `docs/chantiers/GO_OPT_TRADING_OBSOLETE_RECLASS_ARCHIVE_AUDIT_01/00_cadrage.md`, `docs/chantiers/GO_OPT_TRADING_OBSOLETE_RECLASS_ARCHIVE_AUDIT_01/02_journal_technique.md`, `docs/chantiers/GO_OPT_TRADING_OBSOLETE_RECLASS_ARCHIVE_AUDIT_01/03_decisions.md`

### GO_OPT_TRADING_RUNTIME_EXCEPTION_FAMILIES_01
- repo : opt-trading
- type : patch local / doc-only
- statut : active
- titre court : familles mixtes / lignées runtime-exception
- dernier état connu : parent PHASE 3 LOT 5 ouvert ; fiches status courtes posées et rattachées à l’audit famille
- lien utile : `docs/chantiers/GO_OPT_TRADING_RUNTIME_EXCEPTION_FAMILIES_01/00_cadrage.md`, `docs/chantiers/GO_OPT_TRADING_RUNTIME_EXCEPTION_FAMILIES_01/03_decisions.md`

### GO_OPT_TRADING_REGISTRY_SCOPE_REALIGNMENT_01
- repo : opt-trading
- type : patch local / doc-only
- statut : active
- titre court : réalignement scope registry
- dernier état connu : parent PHASE 3 LOT 6 ouvert ; `registry/README.md` complété sur périmètre/exceptions
- lien utile : `docs/chantiers/GO_OPT_TRADING_REGISTRY_SCOPE_REALIGNMENT_01/00_cadrage.md`, `docs/chantiers/GO_OPT_TRADING_REGISTRY_SCOPE_REALIGNMENT_01/03_decisions.md`, `registry/README.md`

### GO_COLLECTORS_LIFECYCLE_COMPAT_CADRAGE_01
- repo : opt-trading
- type : cadrage module durable / collectors
- statut : open
- titre court : cadrage compatibilité lifecycle collectors
- dernier état connu : diagnostic repo-first réalisé sur `origin/inventory/collectors-baseline-01` avec verdict `RE-SCOPE` (risque cassant sur `relref()/relative_to(MODULE_DIR)` si `OUTPUT_DIR` est relatif au root projet), écarts spec/runtime tracés
- lien utile : `docs/COLLECTORS_LIFECYCLE_COMPAT_SPEC_01.md`

### GO_OPT_TRADING_JOURNAL_CANON_INTENT_LAYER_04
- repo : opt-trading
- type : journal / lecture canonique
- statut : active
- titre court : lecture canonique orientée intention projet
- dernier état connu : reprise de lecture après LOT_S23 avec angle intention / objectif / choix / pourquoi, premier bloc visé LOT_S24 à LOT_S28
- lien utile : `docs/chantiers/GO_OPT_TRADING_JOURNAL_CANON_INTENT_LAYER_04/00_cadrage.md`

### GO_OPT_TRADING_JOURNAL_FULL_READING_03
- repo : opt-trading
- type : journal / lecture complète
- statut : active
- titre court : lecture complète du journal canon
- dernier état connu : cadre inter-repos posé, mais couche humaine vivante pas encore réinjectée proprement dans la continuité stable
- lien utile : `docs/chantiers/GO_OPT_TRADING_JOURNAL_FULL_READING_03/00_cadrage.md`

### GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03
- repo : opt-trading
- type : consolidation modules / reseau_ssh
- statut : open
- titre court : consolidation ciblée de la famille reseau_ssh*
- dernier état connu : survivant canonique confirmé modules/reseau_ssh_step2, avec step1b conservé comme prérequis intermédiaire
- lien utile : `docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03/00_cadrage.md`

### GO_TMUX_IDE_OPT_TRADING_CADRAGE_01
- repo : opt-trading
- type : outillage / tmux-ide
- statut : active
- titre court : cadrage IDE terminale tmux-ide
- dernier état connu : bundle préparé, cadrage canonique ouvert, next GO GO_TMUX_IDE_OPT_TRADING_IMPL_BASE_01
- lien utile : `docs/chantiers/GO_TMUX_IDE_OPT_TRADING_CADRAGE_01/00_cadrage.md`

### GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01
- repo : opt-trading
- type : intégration UI / producer-consumer
- statut : open
- titre court : chantier parent UI opt-trading producer → localcms consumer
- dernier état connu : cadrage parent posé ; `opt-trading` reste producer canonique et `localcms` consumer UI ; reprise recommandée sur `GO_OPT_TRADING_UI_LOCALCMS_INVENTORY_01`
- lien utile : `docs/chantiers/GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01/01_cadrage_parent.md`

### GO_EXTRACTEUR_TAGS_CANONICAL_METHOD_01
- repo : opt-trading
- type : gouvernance / extraction / documentation
- statut : reference
- titre court : méthode canonique d’extraction par tags
- dernier état connu : fiche de référence initiale créée sur `sot/mainline` pour séparer extraction, classification, routage mémoire vs doc et écriture contrôlée
- lien utile : `docs/chantiers/GO_EXTRACTEUR_TAGS_CANONICAL_METHOD_01/EXTRACTEUR_TAGS__METHODE_CANONIQUE_V1.md`
