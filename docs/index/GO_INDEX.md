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
updated_at: 2026-04-29
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
| GO_OPT_TRADING_MATRICE_DOC_OPS_PARENT_01 | GO_OPT_TRADING_MATRICE_DOC_OPS_PARENT_01 | — | OPEN | oui | `docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md`<br>`docs/governance/MATRICE_DOC_OPS_MASTER_PLAN_01.md`<br>`docs/chantiers/GO_OPT_TRADING_MATRICE_DOC_OPS_PARENT_01/01_cadrage_parent.md` |
| GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01 | GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01 | — | OPEN | oui | `docs/chantiers/GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01/01_cadrage_parent.md`<br>`docs/chantiers/GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01/02_initial_project_doc.md`<br>`docs/chantiers/GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01/03_decisions.md` |
| GO_OPT_TRADING_MACHINE_DB_LAYER_PARENT_01 | GO_OPT_TRADING_MACHINE_DB_LAYER_PARENT_01 | — | OPEN | oui | `docs/chantiers/GO_OPT_TRADING_MACHINE_DB_LAYER_PARENT_01/01_cadrage_parent.md`<br>`docs/chantiers/GO_OPT_TRADING_MACHINE_DB_LAYER_PARENT_01/02_initial_project_doc.md`<br>`docs/chantiers/GO_OPT_TRADING_MACHINE_DB_LAYER_PARENT_01/03_decisions.md` |
| GO_GIT_PROGRESSIVE_MIGRATION_START_13 | GO_GIT_PROGRESSIVE_MIGRATION_START_13 | — | ACTIVE | oui | `docs/index/GO_INDEX.md`<br>`docs/chantiers/GO_GIT_PROGRESSIVE_MIGRATION_START_13/00_cadrage.md` |
| GO_OPT_TRADING_RUNTIME_EXCEPTION_FAMILIES_01 | GO_OPT_TRADING_RUNTIME_EXCEPTION_FAMILIES_01 | — | ACTIVE | oui | `docs/index/GO_INDEX.md`<br>`docs/chantiers/GO_OPT_TRADING_RUNTIME_EXCEPTION_FAMILIES_01/00_cadrage.md`<br>`docs/chantiers/GO_OPT_TRADING_RUNTIME_EXCEPTION_FAMILIES_01/03_decisions.md` |
| GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03 | GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03 | — | OPEN | oui | `docs/index/GO_INDEX.md`<br>`docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03/00_cadrage.md` |
| GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03 | GO_OPT_TRADING_RESEAU_SSH_UNIFIED_MODULE_CADRAGE_01 | — | OPEN | oui | `docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_UNIFIED_MODULE_CADRAGE_01/00_cadrage.md`<br>`docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03/00_cadrage.md` |
| GO_TMUX_IDE_OPT_TRADING_CADRAGE_01 | GO_TMUX_IDE_OPT_TRADING_CADRAGE_01 | — | ACTIVE | oui | `docs/index/GO_INDEX.md`<br>`docs/chantiers/GO_TMUX_IDE_OPT_TRADING_CADRAGE_01/00_cadrage.md` |
| GO_LOCALCMS_FORMS_INTEGRATION_DOC_01 | GO_LOCALCMS_FORMS_INTEGRATION_DOC_01 | — | OPEN | oui | `docs/index/GO_INDEX.md`<br>`docs/chantiers/GO_LOCALCMS_FORMS_INTEGRATION_DOC_01/00_cadrage.md` |
| GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01 | GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01 | — | OPEN | oui | `docs/chantiers/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01/00_cadrage.md`<br>`docs/chantiers/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01/01_initial_project_doc.md`<br>`docs/chantiers/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01/03_decisions.md` |
| GO_OPT_TRADING_PARENT_NAMING_CANON_01 | GO_OPT_TRADING_PARENT_NAMING_CANON_01 | — | OPEN | oui | `docs/index/GO_INDEX.md`<br>`docs/chantiers/GO_OPT_TRADING_PARENT_NAMING_CANON_01/01_cadrage_parent.md` |
| GO_OPT_TRADING_PARENT_NAMING_CANON_01 | GO_OPT_TRADING_CHILD_NAMING_INVENTORY_01 | — | OPEN | oui | `docs/index/GO_INDEX.md`<br>`docs/chantiers/GO_OPT_TRADING_PARENT_NAMING_CANON_01/01_cadrage_parent.md`<br>`docs/chantiers/GO_OPT_TRADING_CHILD_NAMING_INVENTORY_01/00_cadrage.md` |
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

## Priorite operatoire (6 GO non clos)

- P0 : `GO_TMUX_IDE_OPT_TRADING_CADRAGE_01`
- P1 : `GO_OPT_TRADING_RUNTIME_EXCEPTION_FAMILIES_01`, `GO_GIT_PROGRESSIVE_MIGRATION_START_13`, `GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03`
- P2 : `GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01`, `GO_OPT_TRADING_PARENT_NAMING_CANON_01`

Le passage a 6 GO non clos retenus correspond a la sortie des flux actifs de :
- `GO_OPT_TRADING_ROOT_POLICY_AND_RECLASS_01`
- `GO_OPT_TRADING_OBSOLETE_RECLASS_ARCHIVE_AUDIT_01`

Le parent `GO_OPT_TRADING_MATRICE_DOC_OPS_PARENT_01` reste ouvert et canonique dans le tableau, mais n'est pas retenu dans cette priorisation operatoire resserree.

Le parent `GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01` reste ouvert et canonique dans le tableau, mais hors perimetre d'absorption de cette priorisation resserree.

Historique recent :
- le palier precedent a 10 GO non clos correspondait au maintien temporaire de `GO_OPT_TRADING_CONTINUITY_INDEX_REALIGNMENT_01` et `GO_OPT_TRADING_CANON_STRUCTURE_REALIGNMENT_01` comme actifs avant closeout local

---

## Entrées

### GO_OPT_TRADING_MATRICE_DOC_OPS_PARENT_01
- repo : opt-trading
- type : gouvernance / chantier parent / doc-only
- statut : open
- titre court : matrice maître doc ops
- dernier état connu : matrice maître finale unique rédigée et publiée comme surface canonique ; parent maintenu ouvert pour le lot d'alignement des surfaces proches
- lien utile : `docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md`, `docs/governance/MATRICE_DOC_OPS_MASTER_PLAN_01.md`, `docs/chantiers/GO_OPT_TRADING_MATRICE_DOC_OPS_PARENT_01/01_cadrage_parent.md`

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
- dernier état connu : parent materialise sur la ligne courante avec set doc-only d'ouverture complet ; branche dediee toujours active pour la suite du flux parent
- lien utile : `docs/chantiers/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01/00_cadrage.md`, `docs/chantiers/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01/01_initial_project_doc.md`, `docs/chantiers/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01/03_decisions.md`

### GO_OPT_TRADING_PARENT_NAMING_CANON_01
- repo : opt-trading
- type : gouvernance / nommage / chantier parent
- statut : open
- titre court : parent canonique naming et audit futur
- dernier état connu : politique par surface stable, module audit-only livre, pas de renommage reel dans le lot initial ; reprise recommandee sur l'inventaire
- lien utile : `docs/chantiers/GO_OPT_TRADING_PARENT_NAMING_CANON_01/01_cadrage_parent.md`, `docs/governance/NAMING_CANON_POLICY_01.md`

### GO_OPT_TRADING_CHILD_NAMING_INVENTORY_01
- repo : opt-trading
- type : audit repo-first
- statut : open
- titre court : inventaire des ecarts de nommage
- dernier état connu : cadrage ouvert pour recenser les ecarts sans appliquer de correction ; aucun inventaire verifiable n'est encore publie dans le repo
- lien utile : `docs/chantiers/GO_OPT_TRADING_CHILD_NAMING_INVENTORY_01/00_cadrage.md`

### GO_EXTRACTEUR_TAGS_CANONICAL_METHOD_01
- repo : opt-trading
- type : gouvernance / extraction / documentation
- statut : reference
- titre court : méthode canonique d’extraction par tags
- dernier état connu : fiche de référence initiale créée sur `sot/mainline` pour séparer extraction, classification, routage mémoire vs doc et écriture contrôlée
- lien utile : `docs/governance/EXTRACTEUR_TAGS__METHODE_CANONIQUE_V1.md`
