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
updated_at: 2026-04-16
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

## Flux actifs

### GO_GIT_PROGRESSIVE_MIGRATION_START_13
- statut : active
- repo : opt-trading
- branche : `sot/mainline`
- dernier point établi : dossier chantier dédié minimal désormais ouvert pour un GO déjà actif dans l’index
- prochaine action : expliciter une suite dédiée seulement si la migration progressive doit être poursuivie comme chantier autonome distinct
- blocages : aucun blocage explicite établi dans `docs/chantiers/GO_GIT_PROGRESSIVE_MIGRATION_START_13/00_cadrage.md`

### GO_GITHUB_PARK_AUDIT_EXPANSION_01
- statut : open
- repo : opt-trading
- branche : non précisée dans `docs/chantiers/GO_GITHUB_PARK_AUDIT_EXPANSION_01/00_cadrage.md`
- dernier point établi : cadrage validé, chantier séquencé, next GO défini
- prochaine action : lancer `GO_GITHUB_PARK_BRANCH_TRUNK_CROSS_AUDIT_01`
- blocages : la consolidation reste partielle tant que le rattachement `branch ↔ trunk ↔ chantier`, le découpage complet des familles de modules et la cartographie fichier par fichier ne sont pas produits

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
- dernier point établi : le cadre inter-repos est posé, mais la couche humaine vivante n’est pas encore réinjectée proprement dans la continuité stable
- prochaine action : relire le journal canon complet et produire des blocs de validation humaine fidèles, courts et exploitables
- blocages : le journal mêle contexte humain utile, commandes, décisions et éléments possiblement obsolètes

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

### GO_UNIFORM_CONTINUITY_HARDENING_02
- statut : open
- repo : opt-trading
- branche : non précisée dans `docs/chantiers/GO_UNIFORM_CONTINUITY_HARDENING_02/00_cadrage.md`
- dernier point établi : règle de normalisation retenue, lot patchable figé, lot ambigu séparé, point de reprise canonique posé sans application des patchs
- prochaine action : `GO_APPLY_UNIFORM_WORKFLOW_MEMORY_DOCUMENTATION_01` seulement après validation du présent cadrage
- blocages : application docs-only du lot patchable non faite, décision explicite sur les closings `.txt` non prise, bascule d’index éventuelle encore ouverte

## Flux bloques / en echec

### GO_UNIFORM_CONTINUITY_HARDENING_01
- statut : fail
- repo : opt-trading
- branche : `sot/mainline`
- dernier point établi : hardening diagnostiqué et préparé, mais non appliqué sur les fichiers existants dans ce flux
- prochaine action : appliquer les mises à jour préparées sur `GO_INDEX.md`, `ACTIVE_STREAMS.md`, `REPRISE.md` et `NEXT_GO_CANDIDATES.md`, puis reproduire le meme travail sur `localcms`
- blocages : le connecteur GitHub expose dans ce flux une limite qui n’a pas permis de finaliser proprement la mise a jour en place des fichiers existants
