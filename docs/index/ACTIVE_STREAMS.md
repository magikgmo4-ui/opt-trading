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
updated_at: 2026-04-23
links:
  - docs/index/GO_INDEX.md
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

---

## Priorité opératoire (12 GO non clos)

- P0 : `GO_OPT_TRADING_MATRICE_DOC_OPS_PARENT_01`, `GO_OPT_TRADING_CONTINUITY_INDEX_REALIGNMENT_01`, `GO_TMUX_IDE_OPT_TRADING_CADRAGE_01`, `GO_OPT_TRADING_OBSOLETE_RECLASS_ARCHIVE_AUDIT_01`
- P1 : `GO_OPT_TRADING_CANON_STRUCTURE_REALIGNMENT_01`, `GO_OPT_TRADING_ROOT_POLICY_AND_RECLASS_01`, `GO_OPT_TRADING_RUNTIME_EXCEPTION_FAMILIES_01`, `GO_OPT_TRADING_REGISTRY_SCOPE_REALIGNMENT_01`, `GO_GIT_PROGRESSIVE_MIGRATION_START_13`, `GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03`
- P2 : `GO_OPT_TRADING_JOURNAL_FULL_READING_03`, `GO_OPT_TRADING_JOURNAL_CANON_INTENT_LAYER_04`

---

## Flux actifs

### GO_OPT_TRADING_MATRICE_DOC_OPS_PARENT_01
- statut : open
- repo : opt-trading
- branche : `go/GO_OPT_TRADING_MATRICE_DOC_OPS_PARENT_01`
- dernier point établi : matrice maître finale unique rédigée dans `docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md` ; le parent reste l'enveloppe canonique de cette trajectoire
- prochaine action : aligner / dedupliquer / reclasser les surfaces proches sans ouvrir de parent concurrent
- blocages : aucun blocage explicite ; ne pas dériver vers une synthèse latérale ni vers des sous-lots techniques prématurés

### GO_OPT_TRADING_CONTINUITY_INDEX_REALIGNMENT_01
- statut : active
- repo : opt-trading
- branche : `sot/mainline`
- dernier point établi : chantier parent ouvert pour réaligner la continuité index (repo-first, doc-only)
- prochaine action : appliquer le LOT 1 (index) puis LOT 2 (hiérarchie journal) selon `docs/chantiers/GO_OPT_TRADING_CONTINUITY_INDEX_REALIGNMENT_01/00_cadrage.md`
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

### GO_OPT_TRADING_JOURNAL_CANON_INTENT_LAYER_04
- statut : active
- repo : opt-trading
- branche : non précisée dans `docs/chantiers/GO_OPT_TRADING_JOURNAL_CANON_INTENT_LAYER_04/00_cadrage.md`
- dernier point établi : reprise de lecture après `LOT_S23` avec un nouvel angle orienté intention projet / objectif / choix / pourquoi
- prochaine action : enchaîner sur la lecture de `journal.md`, vérifier le même manque d’intention projet, puis croiser brut et canon
- blocages : aucun blocage explicite établi dans `docs/chantiers/GO_OPT_TRADING_JOURNAL_CANON_INTENT_LAYER_04/00_cadrage.md`

### GO_OPT_TRADING_JOURNAL_FULL_READING_03
- statut : active
- repo : opt-trading
- branche : `sot/mainline`
- dernier point établi : lecture figée volontairement à `JOURNAL_MD_BLOCK_15`; `BLOCK_16` et `BLOCK_17` ne sont pas retenus dans la base canonique courante
- prochaine action : reprendre plus tard à `BLOCK_16` (ligne 4421) seulement si le chantier est rouvert explicitement
- blocages : au-delà de `BLOCK_15`, les segments lus n’apportent pas encore assez d’arbitrages nouveaux ou de doctrine explicite pour être conservés comme continuité canonique

### GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03
- statut : open
- repo : opt-trading
- branche : non précisée dans `docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03/00_cadrage.md`
- dernier point établi : survivant canonique confirmé `modules/reseau_ssh_step2`, avec `step1b` conservé comme prérequis intermédiaire à ce stade
- prochaine action : exécuter le lot audit détaillé de la famille dans ce même GO, sans relancer un audit global du parc
- blocages : il reste à produire la preuve détaillée du survivant réel, la classification explicite de chaque sibling et le correctif minimal de structure / doc / liens si nécessaire

### GO_TMUX_IDE_OPT_TRADING_CADRAGE_01
- statut : active
- repo : opt-trading
- branche : `sot/mainline`
- dernier point établi : bundle préparé, cadrage canonique ouvert
- prochaine action : `GO_TMUX_IDE_OPT_TRADING_IMPL_BASE_01`
- blocages : valider la machine cible réelle, adapter les panes utiles, confirmer l’emplacement repo réel et exécuter la validation réelle de `tmux-ide`

## Flux bloques / en echec

- aucun flux bloqué établi à ce stade
