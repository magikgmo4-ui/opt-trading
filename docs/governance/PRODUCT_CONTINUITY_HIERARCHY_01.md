---
doc_id: OPT_TRADING_PRODUCT_CONTINUITY_HIERARCHY_01
doc_type: governance_product_hierarchy
repo: opt-trading
project: opt-trading
module:
go_id:
status: reference
lifecycle_stage: governance
topic_keys:
  - opt-trading
  - product_continuity
  - hierarchy
  - governance
surface: governance
source_kind: canonical
reference_canonique_principale: docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
updated_at: 2026-04-23
links:
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
  - docs/governance/AUDIT_CONTINUITE_PRODUIT_OPT_TRADING.md
  - docs/governance/MATRICE_GOUVERNANTE_METADATA_DERIVATION_01.md
---

# PRODUCT CONTINUITY HIERARCHY — 01

## Role aligne avec la matrice maitre

- role actuel : hierarchie canonique de continuite produit
- role cible : annexe canonique stable sous `MATRICE_DOC_OPS_MASTER_MATRIX_01.md`
- ce document precise la couche produit, mais ne remplace ni la matrice maitre, ni la doctrine de nommage, ni la doctrine Git, ni les surfaces operatoires

## 1. Objet
Ce document pose la structuration canonique multi-chantier du projet opt-trading.
Il remplace l'inventaire historique par une continuité produit hiérarchisée en 3 niveaux, garantissant la préservation de la trajectoire produit, des objectifs finaux et du paysage global.

## 2. Modèle de continuité (3 niveaux)

### Couche 0 — Socle transverse
Fondations garantissant la méthode et la mémoire du projet.
- **Méthode uniforme + couche humaine** : Fixe comment conserver et transmettre l'état, la trajectoire produit et la reprise.
- **memory_bricks** : Compaction dérivée, traçable, utile à la reprise.

### Anneau A — Produits prioritaires (Centres de gravité)
Les vrais produits finis avec des résultats opératoires ciblés.
- **Desk Pro** : Cockpit paper trading exploitable, multi-machine, opérable sur la surface canonique.
- **Trading Dual Stack V1** : Framework commun LAB + REALTIME borné, gardant un noyau de règles cohérent.
- **Bot Vision** : Pipeline vision cross-platform où un provider headless browser unifie bot_vision entre Windows et Linux sans dépendre de ShareX, produisant des artefacts Desk Pro exploitables.

### Anneau B — Registre court des projets structurants
Paysage global conservé pour ne pas perdre l'historique et les briques de soutien.
- **webhook** : Point d'entrée runtime central (chaîne signaux).
- **perf** : Couche monitor-only (discipline trading).
- **quant** : Logique recherche avant exécution.
- **LocalCMS** : Consumer structuré, continuité inter-repos.
- **Student / db-layer** : Satellites machines de Desk Pro.
- **collector family** : Famille transverse d'ingestion.
- **Trae / agents / prompt factory** : Outillage de structuration IA.
- **surface opérateur / openclaw** : Cockpits locaux et briques d'usage.

## 3. Règle de dérivation
La dérivation des memory_bricks ne s'effectue **qu'après** la stabilisation des synthèses produit (fiches produit finales) de l'Anneau A.
