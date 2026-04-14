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
updated_at: 2026-04-13
links:
  - docs/governance/REPO_ROLE.md
  - docs/governance/DOC_LAYERS.md
---

# GO_INDEX — opt-trading

## Objet

Ce document référence les GO connus et utiles à la continuité locale de `opt-trading`.

Il sert à :
- garder une vue compacte des chantiers connus
- éviter la disparition des GO dans l’historique diffus
- fournir un point d’entrée vers les dossiers chantier, closeouts et reprises

---

## Règles

- l’index référence et synthétise
- il ne remplace ni le dossier chantier ni le closeout
- les GO clos, actifs, bloqués ou archivés peuvent y figurer si leur continuité locale le justifie
- les liens doivent pointer vers les artefacts détaillés dès qu’ils existent

---

## Entrées

### GO_UNIFORM_CONTINUITY_FINAL_MASTER_PLAN_01
- repo : opt-trading
- type : gouvernance / continuité
- statut : reference
- titre court : plan maître uniforme de continuité
- dernier état connu : référentiel consolidé validé comme base documentaire
- lien utile : documentation gouvernance locale et méthode transverse associée

### GO_CONTINUITE_PRODUIT_MULTI_CHANTIER_CANON_01
- repo : opt-trading
- type : gouvernance / continuité produit
- statut : pass
- titre court : hiérarchie produit multi-chantier canonisée
- dernier état connu : structuration Couche 0 / Anneau A / Anneau B posée comme source canonique de continuité produit
- lien utile : `docs/governance/PRODUCT_CONTINUITY_HIERARCHY_01.md`, `docs/governance/AUDIT_CONTINUITE_PRODUIT_OPT_TRADING.md`

### GO_GIT_PROGRESSIVE_MIGRATION_START_13
- repo : opt-trading
- type : migration documentaire
- statut : active
- titre court : démarrage de la migration Git progressive
- dernier état connu : gouvernance locale initiale créée sur `sot/mainline`
- lien utile : `docs/governance/REPO_ROLE.md`, `docs/governance/DOC_LAYERS.md`, `docs/governance/MEMORY_BRICKS_MAPPING.md`

### GO_OPT_TRADING_LOCAL_CONTINUITY_BOOTSTRAP_01
- repo : opt-trading
- type : continuité locale / bootstrap
- statut : pass
- titre court : socle documentaire local posé
- dernier état connu : closeout PASS avec gouvernance locale, index et reprise locale en place
- lien utile : `docs/chantiers/GO_OPT_TRADING_LOCAL_CONTINUITY_BOOTSTRAP_01/90_closeout.md`, `docs/index/REPRISE.md`

### GO_OPT_TRADING_CHANTIER_PILOTE_MEMORY_BRICKS_01
- repo : opt-trading
- type : chantier pilote / memory_bricks
- statut : pass
- titre court : pilote canonique `memory_bricks`
- dernier état connu : closeout PASS posé comme second pilote local directement ancré sur `memory_bricks`
- lien utile : `docs/chantiers/GO_OPT_TRADING_CHANTIER_PILOTE_MEMORY_BRICKS_01/90_closeout.md`, `docs/governance/MEMORY_BRICKS_MAPPING.md`

### GO_UNIFORM_CONTINUITY_HARDENING_01
- repo : opt-trading
- type : hardening documentaire
- statut : active
- titre court : réalignement final des index locaux
- dernier état connu : les index doivent refléter les deux pilotes PASS avant clôture définitive du hardening
- lien utile : `docs/chantiers/GO_UNIFORM_CONTINUITY_HARDENING_01/90_closeout.md`, `docs/index/ACTIVE_STREAMS.md`
