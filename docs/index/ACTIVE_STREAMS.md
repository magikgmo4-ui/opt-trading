---
doc_id: OPT_TRADING_ACTIVE_STREAMS
doc_type: reprise
repo: opt-trading
project: opt-trading
module:
go_id:
status: reference
lifecycle_stage: reprise
topic_keys:
  - opt-trading
  - active_streams
  - continuity
  - reprise
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
point_de_reprise: "Section Flux actifs"
updated_at: 2026-05-20
links:
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
  - docs/index/GO_INDEX.md
  - docs/index/REPRISE.md
---

# ACTIVE_STREAMS — opt-trading

## Objet

Ce document référence les flux réellement actifs ou bloqués dans `opt-trading`.

Il sert à :
- distinguer l’actif du simple historique
- rendre la reprise immédiate plus lisible
- éviter la confusion entre chantier en cours et candidat futur

---

## Règles

- ne référencer ici que ce qui est réellement actif, ouvert ou bloqué
- ne pas y mettre les PASS, les simples références ni les archives
- prendre `docs/chantiers/` comme source primaire du statut observable
- pour chaque flux, garder un dernier point établi et une prochaine action claire

## Hiérarchie active

- l'etat reel des dossiers chantier et du repo prime
- `docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md` gouverne la lecture produit / parent / GO / Git
- `docs/index/GO_INDEX.md` reste la verite de liste et de cardinalite retenue
- `docs/index/ACTIVE_STREAMS.md` reste une surface operatoire de lecture de l'actif ou du bloque

---

## Priorite operatoire (8 GO non clos retenus)

- P0 : `GO_TMUX_IDE_OPT_TRADING_CADRAGE_01`
- P1 : `GO_OPT_TRADING_RUNTIME_EXCEPTION_FAMILIES_01`, `GO_GIT_PROGRESSIVE_MIGRATION_START_13`, `GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03`
- P2 : `GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01`, `GO_OPT_TRADING_AI_STRICT_WORKERS_APPS_CLASSIFICATION_01`, `GO_OPT_TRADING_STRICT_WORKERS_ORCHESTRATION_DEPLOYMENT_CLASSIFICATION_REVIEW_01`
- P3 : `GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01`

---

## Flux actifs

### GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01
- statut : active
- repo : opt-trading
- branche : `go/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01`
- dernier point Ã©tabli : chantier parent doc-only mergÃ© pour canoniser la doctrine multi-agents, avec continuitÃ© parent locale et inbox atomique
- prochaine action : appliquer le prÃ©sent batch d'agrÃ©gation, puis ouvrir `GO_OPT_TRADING_PARENT_CONTINUITY_INDEX_INBOX_METHOD_01` seulement si une promotion additionnelle est requise
- blocages : aucun runtime ; entrÃ©e agrÃ©gÃ©e depuis `INDEX_PATCH.md`

### GO_OPT_TRADING_RUNTIME_EXCEPTION_FAMILIES_01
- statut : active
- repo : opt-trading
- branche : `sot/mainline`
- dernier point établi : parent PHASE 3 LOT 5 ouvert ; fiches status familles créées et rattachées à l’audit
- prochaine action : figer survivant/transition/legacy/archive des familles en gap-only
- blocages : aucun blocage explicite ; pas de duplication des preuves existantes

### GO_GIT_PROGRESSIVE_MIGRATION_START_13
- statut : active
- repo : opt-trading
- branche : `sot/mainline`
- dernier point établi : dossier chantier dédié minimal désormais ouvert pour un GO déjà actif dans l’index
- prochaine action : expliciter une suite dédiée seulement si la migration progressive doit être poursuivie comme chantier autonome distinct
- blocages : aucun blocage explicite établi dans `docs/chantiers/GO_GIT_PROGRESSIVE_MIGRATION_START_13/00_cadrage.md`

### GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01
- statut : open
- repo : opt-trading
- branche : `origin/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01`
- dernier point établi : parent AI team intégré doc-only dans `GO_INDEX.md` avec statut `OPEN`
- prochaine action : utiliser cette entrée comme point de reprise si un GO enfant dédié d’audit documentaire doit être rouvert
- blocages : dossier parent complet non matérialisé dans cette copie locale ; reprise à garder repo-first sur l’état prouvé

### GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03
- statut : open
- repo : opt-trading
- branche : non précisée dans `docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03/00_cadrage.md`
- dernier point établi : `db-layer`, `admin-trading`, `student` et `fantome` pointent maintenant leurs alias courts vers `modules/reseau_ssh/scripts/*` avec PASS ; `scripts/reseau_ssh` et `step1b` restent en compat
- prochaine action : ouvrir le lot suivant de réduction de compatibilité sur `scripts/reseau_ssh`, puis qualifier `step1b`
- blocages : ne pas retirer `scripts/reseau_ssh` ni `step1b` avant coupe explicite des usages de rollback / compat

### GO_TMUX_IDE_OPT_TRADING_CADRAGE_01
- statut : active
- repo : opt-trading
- branche : `sot/mainline`
- dernier point etabli : bundle prepare, cadrage canonique ouvert ; le run reel Attention Center est merge en PASS et confirme `GO_TMUX_IDE_OPT_TRADING_IMPL_BASE_01` comme suite immediate
- prochaine action : `GO_TMUX_IDE_OPT_TRADING_IMPL_BASE_01` apres verification de la machine cible
- blocages : valider la machine cible reelle, adapter les panes utiles, confirmer l'emplacement repo reel et executer la validation reelle de `tmux-ide`
- reserve : OpenClaw hors scope pour cette suite ; aucun rattachement machine sans preuve

### GO_OPT_TRADING_AI_STRICT_WORKERS_APPS_CLASSIFICATION_01
- statut : open
- repo : opt-trading
- branche : `sot/mainline`
- dernier point etabli : matrice de classification mergee via PR #645 pour decouper le chantier large AI / strict-workers / apps en buckets distincts
- prochaine action : s'appuyer sur la matrice mergee comme point d'entree canonique et ouvrir les suites bucket par bucket seulement
- blocages : aucun blocage runtime ; ne pas remelanger strategy, Airtable, OpenClaw policy/DBLayer avec le bucket deploy strict-workers

### GO_OPT_TRADING_STRICT_WORKERS_ORCHESTRATION_DEPLOYMENT_CLASSIFICATION_REVIEW_01
- statut : open
- repo : opt-trading
- branche : `sot/mainline`
- dernier point etabli : bucket 1 merge via PR #646 en revue doc-only read-only, bornee aux workflows strict-workers validate/smoke, `deploy/systemd/*`, overrides, `config/machine_runtime_map.yml` et `modules/*/systemd/*`
- prochaine action : decider si la suite ouvre `GO_OPT_TRADING_STRICT_WORKERS_DEPLOY_SURFACES_IMPL_01` ou un GO separe `machine_runtime_map`
- blocages : aucune modification runtime autorisee dans ce GO ; validation humaine requise avant implementation

## Flux bloques / en echec

- aucun flux bloqué établi à ce stade
