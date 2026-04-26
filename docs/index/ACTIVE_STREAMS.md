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
updated_at: 2026-04-25
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

## Priorité opératoire (14 GO non clos retenus)

- P0 : `GO_OPT_TRADING_DOC_OPS_PARENT_PROJECT_MACHINE_SPLIT_01`, `GO_OPT_TRADING_CONTINUITY_INDEX_REALIGNMENT_01`, `GO_TMUX_IDE_OPT_TRADING_CADRAGE_01`, `GO_OPT_TRADING_OBSOLETE_RECLASS_ARCHIVE_AUDIT_01`
- P1 : `GO_OPT_TRADING_CANON_STRUCTURE_REALIGNMENT_01`, `GO_OPT_TRADING_ROOT_POLICY_AND_RECLASS_01`, `GO_OPT_TRADING_TRAE_PACK_TEXTS_REVISION_01`, `GO_OPT_TRADING_RUNTIME_EXCEPTION_FAMILIES_01`, `GO_OPT_TRADING_REGISTRY_SCOPE_REALIGNMENT_01`, `GO_GIT_PROGRESSIVE_MIGRATION_START_13`, `GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03`
- P2 : `GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01`, `GO_OPT_TRADING_MATRICE_GOUVERNANTE_METADATA_DERIVATION_01`, `GO_OPT_TRADING_PARENT_NAMING_CANON_01`

---

## Flux actifs

### GO_OPT_TRADING_DOC_OPS_PARENT_PROJECT_MACHINE_SPLIT_01
- statut : open
- repo : opt-trading
- branche : `go/GO_OPT_TRADING_DOC_OPS_PARENT_PROJECT_MACHINE_SPLIT_01`
- dernier point établi : parent canonique de reprise repo-first ouvert ; le plan complet de session est figé dans `01_cadrage_parent.md` et `02_go_map.md` ; l’ouverture des 5 parents spécialisés est explicitement reportée après contrôle des branches et des ouverts / non terminés
- prochaine action : exécuter `GO_OPT_TRADING_DOC_OPS_CHILD_BRANCH_CLEANUP_01`, puis `GO_OPT_TRADING_DOC_OPS_CHILD_OPEN_WORK_CONTROL_01`
- blocages : ne pas ouvrir les 5 parents spécialisés avant la fin explicite du contrôle des ouverts / non terminés ; ne pas relancer plusieurs flux principaux en parallèle

### GO_OPT_TRADING_CONTINUITY_INDEX_REALIGNMENT_01
- statut : active
- repo : opt-trading
- branche : `sot/mainline`
- dernier point établi : chantier parent ouvert pour réaligner la continuité index (repo-first, doc-only)
- prochaine action : appliquer le LOT 1 (index) puis LOT 2 (retrait du journal et réalignement continuité) selon `docs/chantiers/GO_OPT_TRADING_CONTINUITY_INDEX_REALIGNMENT_01/00_cadrage.md`
- blocages : aucun blocage explicite ; patchs uniquement si gap réel

### GO_OPT_TRADING_OBSOLETE_RECLASS_ARCHIVE_AUDIT_01
- statut : active
- repo : opt-trading
- branche : `sot/mainline`
- dernier point établi : parent ouvert ; audit repo-first non destructif des familles obsolete / déclassé / archive / legacy / sous arbitrage
- prochaine action : produire la matrice canonique (PHASE C), puis le plan de lots physiques futurs (PHASE D) sans exécution
- blocages : aucun blocage explicite ; aucune action physique avant validation (matrice + lot + risque + rollback)

### GO_OPT_TRADING_CANON_STRUCTURE_REALIGNMENT_01
- statut : active
- repo : opt-trading
- branche : `sot/mainline`
- dernier point établi : parent PHASE 2 LOT 3 ouvert ; `REPO_SURFACES_MAP.md` posé comme carte humaine des surfaces
- prochaine action : stabiliser les ajustements de structure canonique sans dupliquer `registry/*`
- blocages : aucun blocage explicite ; priorité aux écarts réellement observés

### GO_OPT_TRADING_ROOT_POLICY_AND_RECLASS_01
- statut : active
- repo : opt-trading
- branche : `sot/mainline`
- dernier point établi : parent PHASE 2 LOT 4 ouvert ; `REPO_ROOT_POLICY.md` posé pour la racine interne
- prochaine action : consolider les règles de reclassement racine par arbitrages documentés
- blocages : aucun blocage explicite ; ne pas redéfinir la frontière repo/hors-repo

### GO_OPT_TRADING_TRAE_PACK_TEXTS_REVISION_01
- statut : active
- repo : opt-trading
- branche : `sot/mainline`
- dernier point établi : `trae_pack_texts/` a été déplacé sous `docs/ot/trae/trae_pack_texts/` ; un `README.md` repo-native y porte désormais la synthèse vivante, et `trae_pack/` est requalifié en archive de lecture compatible doc/IDE
- prochaine action : vérifier après push si le lot peut passer en closeout doc-only, sans réactiver les anciens templates comme doctrine vivante
- blocages : ne pas re-promouvoir ces packs comme source canonique ; éviter toute duplication doctrinale avec `workflow_ai/` et le starter pack

### GO_OPT_TRADING_RUNTIME_EXCEPTION_FAMILIES_01
- statut : active
- repo : opt-trading
- branche : `sot/mainline`
- dernier point établi : parent PHASE 3 LOT 5 ouvert ; fiches status familles créées et rattachées à l’audit
- prochaine action : figer survivant/transition/legacy/archive des familles en gap-only
- blocages : aucun blocage explicite ; pas de duplication des preuves existantes

### GO_OPT_TRADING_REGISTRY_SCOPE_REALIGNMENT_01
- statut : active
- repo : opt-trading
- branche : `sot/mainline`
- dernier point établi : parent PHASE 3 LOT 6 ouvert ; scope/exception clarifiés dans `registry/README.md`
- prochaine action : consolider la couverture déclarative sans créer de doctrine parallèle
- blocages : aucun blocage explicite ; rester sur la source canonique `registry/README.md`

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

### GO_OPT_TRADING_MATRICE_GOUVERNANTE_METADATA_DERIVATION_01
- statut : open
- repo : opt-trading
- branche : `sot/mainline`
- dernier point établi : doctrine légère de dérivation ouverte sous la matrice maître, avec pilote borné avant toute application plus large
- prochaine action : poursuivre le pilote documentaire borné avant toute extension repo-wide
- blocages : ne pas rouvrir la matrice, ni promouvoir les dérivés au-dessus des surfaces souveraines

### GO_OPT_TRADING_PARENT_NAMING_CANON_01
- statut : open
- repo : opt-trading
- branche : `sot/mainline`
- dernier point établi : parent naming canon ouvert en audit-only ; aucun renommage réel dans le lot initial
- prochaine action : reprendre sur `GO_OPT_TRADING_CHILD_NAMING_INVENTORY_01` avant tout lot d’application
- blocages : aucun nouveau `<PRODUCT_OR_SURFACE>` ne doit être tenu pour valide sans preuve canonique ; aucune campagne rétroactive immédiate

### GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03
- statut : open
- repo : opt-trading
- branche : non précisée dans `docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03/00_cadrage.md`
- dernier point établi : `db-layer`, `admin-trading`, `student` et `fantome` pointent maintenant leurs alias courts vers `modules/reseau_ssh/scripts/*` avec PASS ; le runtime legacy `scripts/reseau_ssh` est archivé repo-side ; les commandes `baseline-*` sont absorbées ; `step1b` est archivé repo-side ; plus aucun alias `step1b` n'est publié sur les 4 hôtes
- prochaine action : nettoyer les répertoires `step1b` résiduels côté machines sans toucher au canonique
- blocages : ne pas supprimer les copies machine-side avant runbook dédié et rollback explicite

### GO_TMUX_IDE_OPT_TRADING_CADRAGE_01
- statut : active
- repo : opt-trading
- branche : `sot/mainline`
- dernier point établi : bundle préparé, cadrage canonique ouvert
- prochaine action : `GO_TMUX_IDE_OPT_TRADING_IMPL_BASE_01`
- blocages : valider la machine cible réelle, adapter les panes utiles, confirmer l’emplacement repo réel et exécuter la validation réelle de `tmux-ide`

## Flux bloques / en echec

- aucun flux bloqué établi à ce stade
