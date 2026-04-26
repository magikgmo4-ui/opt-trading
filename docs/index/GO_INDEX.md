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
updated_at: 2026-04-25
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
| GO_UNIFORM_CONTINUITY_FINAL_MASTER_PLAN_01 | GO_UNIFORM_CONTINUITY_FINAL_MASTER_PLAN_01 | — | REFERENCE | oui | `docs/index/GO_INDEX.md`<br>`docs/chantiers/GO_UNIFORM_CONTINUITY_FINAL_MASTER_PLAN_01/00_cadrage.md` |
| GO_OPT_TRADING_MATRICE_DOC_OPS_PARENT_01 | GO_OPT_TRADING_MATRICE_DOC_OPS_PARENT_01 | — | OPEN | oui | `docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md`<br>`docs/governance/MATRICE_DOC_OPS_MASTER_PLAN_01.md`<br>`docs/chantiers/GO_OPT_TRADING_MATRICE_DOC_OPS_PARENT_01/01_cadrage_parent.md` |
| GO_OPT_TRADING_DOC_OPS_PARENT_PROJECT_MACHINE_SPLIT_01 | GO_OPT_TRADING_DOC_OPS_PARENT_PROJECT_MACHINE_SPLIT_01 | — | OPEN | oui | `docs/chantiers/GO_OPT_TRADING_DOC_OPS_PARENT_PROJECT_MACHINE_SPLIT_01/01_cadrage_parent.md`<br>`docs/chantiers/GO_OPT_TRADING_DOC_OPS_PARENT_PROJECT_MACHINE_SPLIT_01/02_go_map.md` |
| GO_GIT_PROGRESSIVE_MIGRATION_START_13 | GO_GIT_PROGRESSIVE_MIGRATION_START_13 | — | ACTIVE | oui | `docs/index/GO_INDEX.md`<br>`docs/chantiers/GO_GIT_PROGRESSIVE_MIGRATION_START_13/00_cadrage.md` |
| GO_OPT_TRADING_CONTINUITY_INDEX_REALIGNMENT_01 | GO_OPT_TRADING_CONTINUITY_INDEX_REALIGNMENT_01 | — | ACTIVE | oui | `docs/index/GO_INDEX.md`<br>`docs/chantiers/GO_OPT_TRADING_CONTINUITY_INDEX_REALIGNMENT_01/00_cadrage.md`<br>`docs/chantiers/GO_OPT_TRADING_CONTINUITY_INDEX_REALIGNMENT_01/03_decisions.md` |
| GO_OPT_TRADING_CANON_STRUCTURE_REALIGNMENT_01 | GO_OPT_TRADING_CANON_STRUCTURE_REALIGNMENT_01 | — | ACTIVE | oui | `docs/index/GO_INDEX.md`<br>`docs/chantiers/GO_OPT_TRADING_CANON_STRUCTURE_REALIGNMENT_01/00_cadrage.md`<br>`docs/chantiers/GO_OPT_TRADING_CANON_STRUCTURE_REALIGNMENT_01/03_decisions.md`<br>`docs/architecture/REPO_SURFACES_MAP.md` |
| GO_OPT_TRADING_ROOT_POLICY_AND_RECLASS_01 | GO_OPT_TRADING_ROOT_POLICY_AND_RECLASS_01 | — | ACTIVE | oui | `docs/index/GO_INDEX.md`<br>`docs/chantiers/GO_OPT_TRADING_ROOT_POLICY_AND_RECLASS_01/00_cadrage.md`<br>`docs/chantiers/GO_OPT_TRADING_ROOT_POLICY_AND_RECLASS_01/03_decisions.md`<br>`docs/governance/REPO_ROOT_POLICY.md` |
| GO_OPT_TRADING_ROOT_POLICY_AND_RECLASS_01 | GO_OPT_TRADING_TRAE_PACK_TEXTS_REVISION_01 | — | ACTIVE | oui | `docs/index/GO_INDEX.md`<br>`docs/chantiers/GO_OPT_TRADING_TRAE_PACK_TEXTS_REVISION_01/00_cadrage.md`<br>`docs/chantiers/GO_OPT_TRADING_TRAE_PACK_TEXTS_REVISION_01/03_decisions.md`<br>`docs/ot/trae/trae_pack_texts/trae_pack/TRAE_SESSION_OPENING_PACK_V1.1.txt` |
| GO_OPT_TRADING_OBSOLETE_RECLASS_ARCHIVE_AUDIT_01 | GO_OPT_TRADING_OBSOLETE_RECLASS_ARCHIVE_AUDIT_01 | — | ACTIVE | oui | `docs/index/GO_INDEX.md`<br>`docs/chantiers/GO_OPT_TRADING_OBSOLETE_RECLASS_ARCHIVE_AUDIT_01/00_cadrage.md`<br>`docs/chantiers/GO_OPT_TRADING_OBSOLETE_RECLASS_ARCHIVE_AUDIT_01/03_decisions.md` |
| GO_OPT_TRADING_RUNTIME_EXCEPTION_FAMILIES_01 | GO_OPT_TRADING_RUNTIME_EXCEPTION_FAMILIES_01 | — | ACTIVE | oui | `docs/index/GO_INDEX.md`<br>`docs/chantiers/GO_OPT_TRADING_RUNTIME_EXCEPTION_FAMILIES_01/00_cadrage.md`<br>`docs/chantiers/GO_OPT_TRADING_RUNTIME_EXCEPTION_FAMILIES_01/03_decisions.md` |
| GO_OPT_TRADING_REGISTRY_SCOPE_REALIGNMENT_01 | GO_OPT_TRADING_REGISTRY_SCOPE_REALIGNMENT_01 | — | ACTIVE | oui | `docs/index/GO_INDEX.md`<br>`docs/chantiers/GO_OPT_TRADING_REGISTRY_SCOPE_REALIGNMENT_01/00_cadrage.md`<br>`docs/chantiers/GO_OPT_TRADING_REGISTRY_SCOPE_REALIGNMENT_01/03_decisions.md`<br>`registry/README.md` |
| GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03 | GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03 | — | OPEN | oui | `docs/index/GO_INDEX.md`<br>`docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03/00_cadrage.md` |
| GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03 | GO_OPT_TRADING_RESEAU_SSH_UNIFIED_MODULE_CADRAGE_01 | — | OPEN | oui | `docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_UNIFIED_MODULE_CADRAGE_01/00_cadrage.md`<br>`docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03/00_cadrage.md` |
| GO_TMUX_IDE_OPT_TRADING_CADRAGE_01 | GO_TMUX_IDE_OPT_TRADING_CADRAGE_01 | — | ACTIVE | oui | `docs/index/GO_INDEX.md`<br>`docs/chantiers/GO_TMUX_IDE_OPT_TRADING_CADRAGE_01/00_cadrage.md` |
| GO_LOCALCMS_FORMS_INTEGRATION_DOC_01 | GO_LOCALCMS_FORMS_INTEGRATION_DOC_01 | — | OPEN | oui | `docs/index/GO_INDEX.md`<br>`docs/chantiers/GO_LOCALCMS_FORMS_INTEGRATION_DOC_01/00_cadrage.md` |
| GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01 | GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01 | — | OPEN | non | `docs/index/GO_INDEX.md`<br>`docs/chantiers/GO_GIT_AI_TEAM_ARCHITECTURE_PARENT_DOC_ONLY_INTEGRATION_01/03_decisions.md` |
| GO_OPT_TRADING_MATRICE_GOUVERNANTE_METADATA_DERIVATION_01 | GO_OPT_TRADING_MATRICE_GOUVERNANTE_METADATA_DERIVATION_01 | — | OPEN | oui | `docs/index/GO_INDEX.md`<br>`docs/chantiers/GO_OPT_TRADING_MATRICE_GOUVERNANTE_METADATA_DERIVATION_01/00_cadrage.md`<br>`docs/governance/MATRICE_GOUVERNANTE_METADATA_DERIVATION_01.md` |
| GO_OPT_TRADING_PARENT_NAMING_CANON_01 | GO_OPT_TRADING_PARENT_NAMING_CANON_01 | — | OPEN | oui | `docs/index/GO_INDEX.md`<br>`docs/chantiers/GO_OPT_TRADING_PARENT_NAMING_CANON_01/01_cadrage_parent.md` |
| GO_OPT_TRADING_PARENT_NAMING_CANON_01 | GO_OPT_TRADING_CHILD_NAMING_INVENTORY_01 | — | OPEN | oui | `docs/index/GO_INDEX.md`<br>`docs/chantiers/GO_OPT_TRADING_PARENT_NAMING_CANON_01/01_cadrage_parent.md`<br>`docs/chantiers/GO_OPT_TRADING_CHILD_NAMING_INVENTORY_01/00_cadrage.md` |
| GO_OPT_TRADING_PARENT_NAMING_CANON_01 | GO_OPT_TRADING_CHILD_NAMING_NORMALIZER_01 | — | OPEN | oui | `docs/index/GO_INDEX.md`<br>`docs/chantiers/GO_OPT_TRADING_PARENT_NAMING_CANON_01/01_cadrage_parent.md`<br>`docs/chantiers/GO_OPT_TRADING_CHILD_NAMING_NORMALIZER_01/00_cadrage.md` |
| GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01 | GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01 | — | OPEN | oui | `docs/index/GO_INDEX.md`<br>`docs/chantiers/GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01/01_cadrage_parent.md` |
| GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01 | GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01 | GO_OPT_TRADING_UI_LOCALCMS_INVENTORY_01 | REFERENCE | non | `docs/chantiers/GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01/01_cadrage_parent.md` |
| GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01 | GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01 | GO_OPT_TRADING_UI_LOCALCMS_MATRIX_01 | REFERENCE | non | `docs/chantiers/GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01/01_cadrage_parent.md` |
| GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01 | GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01 | GO_OPT_TRADING_UI_LOCALCMS_CONTRACTS_01 | REFERENCE | non | `docs/chantiers/GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01/01_cadrage_parent.md` |
| GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01 | GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01 | GO_OPT_TRADING_UI_LOCALCMS_PILOT_READONLY_01 | REFERENCE | non | `docs/chantiers/GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01/01_cadrage_parent.md` |
| GO_EXTRACTEUR_TAGS_CANONICAL_METHOD_01 | GO_EXTRACTEUR_TAGS_CANONICAL_METHOD_01 | — | REFERENCE | non | `docs/index/GO_INDEX.md`<br>`docs/governance/EXTRACTEUR_TAGS__METHODE_CANONIQUE_V1.md` |
| GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01 | GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01 | — | ACTIVE | oui | `docs/chantiers/GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01/00_cadrage.md`<br>`docs/index/REPRISE.md` |
| GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01 | GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01 | GO_TMUX_RUNTIME_CONVENTIONS_01 | REFERENCE | non | `docs/chantiers/GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01/00_cadrage.md` |
| GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01 | GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01 | GO_OPENCLAW_COMMAND_SCOPE_01 | REFERENCE | non | `docs/chantiers/GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01/00_cadrage.md` |
| GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01 | GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01 | GO_TMUX_RUNTIME_CONTRACT_01 | REFERENCE | non | `docs/chantiers/GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01/00_cadrage.md` |
| GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01 | GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01 | GO_TMUX_OPENCODE_OPENCLAW_MODES_01 | REFERENCE | non | `docs/chantiers/GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01/00_cadrage.md` |
| GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01 | GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01 | GO_RUNTIME_GUARDRAILS_01 | REFERENCE | non | `docs/chantiers/GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01/00_cadrage.md` |

---

## Priorité opératoire (14 GO non clos)

- P0 : `GO_OPT_TRADING_DOC_OPS_PARENT_PROJECT_MACHINE_SPLIT_01`, `GO_OPT_TRADING_CONTINUITY_INDEX_REALIGNMENT_01`, `GO_TMUX_IDE_OPT_TRADING_CADRAGE_01`, `GO_OPT_TRADING_OBSOLETE_RECLASS_ARCHIVE_AUDIT_01`
- P1 : `GO_OPT_TRADING_CANON_STRUCTURE_REALIGNMENT_01`, `GO_OPT_TRADING_ROOT_POLICY_AND_RECLASS_01`, `GO_OPT_TRADING_TRAE_PACK_TEXTS_REVISION_01`, `GO_OPT_TRADING_RUNTIME_EXCEPTION_FAMILIES_01`, `GO_OPT_TRADING_REGISTRY_SCOPE_REALIGNMENT_01`, `GO_GIT_PROGRESSIVE_MIGRATION_START_13`, `GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03`
- P2 : `GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01`, `GO_OPT_TRADING_MATRICE_GOUVERNANTE_METADATA_DERIVATION_01`, `GO_OPT_TRADING_PARENT_NAMING_CANON_01`

Le passage de 13 a 14 GO non clos retenus correspond a l'ouverture du GO :
- `GO_OPT_TRADING_TRAE_PACK_TEXTS_REVISION_01`

Le passage de 12 a 13 GO non clos retenus correspond a l'ouverture du parent :
- `GO_OPT_TRADING_DOC_OPS_PARENT_PROJECT_MACHINE_SPLIT_01`

Le passage de 11 a 12 GO non clos retenus correspond a l'ouverture du GO :
- `GO_OPT_TRADING_MATRICE_GOUVERNANTE_METADATA_DERIVATION_01`

Le passage de 10 a 11 GO non clos retenus correspond a l'ouverture du parent :
- `GO_OPT_TRADING_PARENT_NAMING_CANON_01`

Le passage de 9 a 10 GO non clos retenus correspond a l'ouverture du parent :
- `GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01`

Le passage de 8 a 9 GO non clos retenus correspond a l'ouverture du parent :
- `GO_OPT_TRADING_OBSOLETE_RECLASS_ARCHIVE_AUDIT_01`

Le parent `GO_OPT_TRADING_MATRICE_DOC_OPS_PARENT_01` reste ouvert et canonique dans le tableau, mais n'est pas retenu dans cette priorisation operatoire resserree.

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

### GO_OPT_TRADING_MATRICE_DOC_OPS_PARENT_01
- repo : opt-trading
- type : gouvernance / chantier parent / doc-only
- statut : open
- titre court : matrice maître doc ops
- dernier état connu : matrice maître finale unique rédigée et publiée comme surface canonique ; parent maintenu ouvert pour le lot d'alignement des surfaces proches
- lien utile : `docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md`, `docs/governance/MATRICE_DOC_OPS_MASTER_PLAN_01.md`, `docs/chantiers/GO_OPT_TRADING_MATRICE_DOC_OPS_PARENT_01/01_cadrage_parent.md`

### GO_OPT_TRADING_DOC_OPS_PARENT_PROJECT_MACHINE_SPLIT_01
- repo : opt-trading
- type : gouvernance / chantier parent / orchestration de reprise repo-first
- statut : open
- titre court : parent canonique de reprise avant structuration project/machine
- dernier état connu : parent canonique de reprise repo-first ouvert sur branche dédiée ; le vrai plan de session est figé dans l'ordre branches/supports ouverts -> ouverts/non terminés -> flux principal unique -> seulement ensuite carte cible et ouverture future des 5 parents spécialisés
- lien utile : `docs/chantiers/GO_OPT_TRADING_DOC_OPS_PARENT_PROJECT_MACHINE_SPLIT_01/01_cadrage_parent.md`, `docs/chantiers/GO_OPT_TRADING_DOC_OPS_PARENT_PROJECT_MACHINE_SPLIT_01/02_go_map.md`

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

### GO_OPT_TRADING_TRAE_PACK_TEXTS_REVISION_01
- repo : opt-trading
- type : patch local / doc-only / reclassement documentaire
- statut : active
- titre court : révision et relocalisation documentaire de `trae_pack_texts`
- dernier état connu : le pack legacy Trae a été déplacé de la racine vers `docs/ot/trae/trae_pack_texts/` ; un lot dédié reste ouvert pour qualifier son contenu, son usage et sa place exacte dans la continuité
- lien utile : `docs/chantiers/GO_OPT_TRADING_TRAE_PACK_TEXTS_REVISION_01/00_cadrage.md`, `docs/chantiers/GO_OPT_TRADING_TRAE_PACK_TEXTS_REVISION_01/03_decisions.md`, `docs/ot/trae/README.md`

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

### GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03
- repo : opt-trading
- type : consolidation modules / reseau_ssh
- statut : open
- titre court : consolidation ciblée de la famille reseau_ssh*
- dernier état connu : `modules/reseau_ssh` est le canonique repo-side ; `db-layer`, `admin-trading`, `student` et `fantome` ont leurs alias courts repointés vers le canonique ; `scripts/reseau_ssh` et `step1b` sont archivés repo-side ; les répertoires machine-side `step1b` sont archivés localement ; `db-layer`, `admin-trading` et `student` valident `baseline-*` + `sanity-reseau_ssh`, tandis que `fantome` reste borné par l'absence de `PyYAML` pour le deep sanity
- lien utile : `docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03/00_cadrage.md`, `docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_CANONICAL_RENAME_REGISTRY_01/01_plan_operationnel_step_by_step.md`, `docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_MACHINE_SIDE_REPOINT_01/10_step_09_execution_resultats.md`, `docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_STEP1B_ARCHIVE_01/03_step_02_execution_archive.md`, `docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_STEP1B_MACHINE_CLEANUP_01/03_step_02_execution_cleanup.md`

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

### GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01
- repo : opt-trading
- type : architecture documentaire / parent AI team
- statut : open
- titre court : parent canonique architecture equipe d'agents
- dernier état connu : parent integre doc-only dans `GO_INDEX.md` avec statut `OPEN`; dossier parent complet attendu sur branche distante mais non materialise dans cette copie locale
- lien utile : `docs/chantiers/GO_GIT_AI_TEAM_ARCHITECTURE_PARENT_DOC_ONLY_INTEGRATION_01/03_decisions.md`

### GO_OPT_TRADING_MATRICE_GOUVERNANTE_METADATA_DERIVATION_01
- repo : opt-trading
- type : gouvernance / metadata derivee / doc-only
- statut : open
- titre court : doctrine legere de derivation post-matrice
- dernier état connu : GO ouvert sous la matrice maitre DOC OPS, avec `docs/governance/MATRICE_GOUVERNANTE_V2.md` relue comme annexe stable secondaire pour cadrer frontmatter enrichi, `search_tags`, groupes d'objets et registry derive, sans rouvrir la doctrine matrice ni la synchronisation documentaire reelle
- lien utile : `docs/chantiers/GO_OPT_TRADING_MATRICE_GOUVERNANTE_METADATA_DERIVATION_01/00_cadrage.md`, `docs/chantiers/GO_OPT_TRADING_MATRICE_GOUVERNANTE_METADATA_DERIVATION_01/03_decisions.md`, `docs/governance/MATRICE_GOUVERNANTE_METADATA_DERIVATION_01.md`

### GO_OPT_TRADING_PARENT_NAMING_CANON_01
- repo : opt-trading
- type : gouvernance / nommage / chantier parent
- statut : open
- titre court : parent canonique naming et audit futur
- dernier état connu : politique par surface subordonnee au canon GO ; pas de renommage reel dans le lot initial ; reprise recommandee sur l'inventaire
- lien utile : `docs/chantiers/GO_OPT_TRADING_PARENT_NAMING_CANON_01/01_cadrage_parent.md`, `docs/governance/NAMING_CANON_POLICY_01.md`

### GO_OPT_TRADING_CHILD_NAMING_INVENTORY_01
- repo : opt-trading
- type : audit repo-first
- statut : open
- titre court : inventaire des ecarts de nommage
- dernier état connu : cadrage ouvert pour recenser les ecarts sans appliquer de correction
- lien utile : `docs/chantiers/GO_OPT_TRADING_CHILD_NAMING_INVENTORY_01/00_cadrage.md`

### GO_OPT_TRADING_CHILD_NAMING_NORMALIZER_01
- repo : opt-trading
- type : module durable audit-only
- statut : open
- titre court : module naming_normalizer
- dernier état connu : squelette V2 pret pour audit, verification de structure GO canonique et rapport
- lien utile : `docs/chantiers/GO_OPT_TRADING_CHILD_NAMING_NORMALIZER_01/00_cadrage.md`, `modules/naming_normalizer/README.md`

### GO_EXTRACTEUR_TAGS_CANONICAL_METHOD_01
- repo : opt-trading
- type : gouvernance / extraction / documentation
- statut : reference
- titre court : méthode canonique d’extraction par tags
- dernier état connu : fiche de référence initiale créée sur `sot/mainline` pour séparer extraction, classification, routage mémoire vs doc et écriture contrôlée
- lien utile : `docs/governance/EXTRACTEUR_TAGS__METHODE_CANONIQUE_V1.md`
