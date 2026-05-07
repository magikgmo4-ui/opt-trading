---
doc_id: OPT_TRADING_GUIDE_DERIVATIVES_COLLECTOR
doc_type: user_guide
repo: opt-trading
status: reference
lifecycle_stage: product_usage
source_kind: canonical
updated_at: 2026-05-07
links:
  - docs/COLLECTORS_FAMILY_DOCTRINE_01.md
  - docs/COLLECTORS_MIGRATION_MAP_01.md
---

# Guide utilisateur - derivatives_collector

## Ce que c'est

derivatives_collector est le collecteur canonique de donnees de marches derives pour le trading.

## A quoi ca sert

Il sert a collecter les donnees de marches derives, les exporter en JSON/CSV, et alimenter les moteurs d'analyse et de trading.

## Quand l'utiliser

- pour collecter des donnees de marches derives (futures, options, perps) ;
- pour exporter les donnees vers les moteurs d'analyse ;
- pour suivre la convergence doctrinale de la famille collector.

## Quand ne pas l'utiliser

- comme produit fini sans limites (la convergence doctrinale est en cours) ;
- pour forcer une migration runtime immediate vers `collectors_core` ;
- pour ajouter un provider supplementaire avant la fin de la convergence.

## Prerequis

- acces au module `modules/derivatives_collector/` ;
- lecture de `docs/COLLECTORS_FAMILY_DOCTRINE_01.md` ;
- lecture de `docs/COLLECTORS_MIGRATION_MAP_01.md` ;
- connaissance des phases 0-5 de convergence.

## Commandes / acces

- Module : `modules/derivatives_collector/`
- Doctrine famille : `docs/COLLECTORS_FAMILY_DOCTRINE_01.md`
- Migration map : `docs/COLLECTORS_MIGRATION_MAP_01.md`

## Procedure simple

1. Verifier l'etat du collector via son wrapper cmd.
2. Lancer une collecte selon la configuration.
3. Verifier les exports JSON/CSV produits.
4. Consulter la migration map pour connaitre la phase de convergence en cours.
5. Ne pas ajouter de provider supplementaire avant la fin de la convergence.

## Verification PASS

- le collector produit des exports lisibles ;
- les donnees sont coherentes avec les marches cibles ;
- la doctrine famille est respectee ;
- aucune migration runtime forcee n'est en cours sans validation.

## Limites

- la convergence doctrinale est en cours (phases 0-5) ;
- le vocabulaire, les artifacts, la config et la surface operateur sont en cours d'alignement ;
- la migration runtime vers `collectors_core` n'est pas immediate ni forcee ;
- pas de provider supplementaire avant convergence.

## Depannage

- Si les exports sont incoherents : verifier la config et les logs.
- Si la doctrine famille n'est pas claire : relire `COLLECTORS_FAMILY_DOCTRINE_01.md`.
- Si un nouveau provider est necessaire : attendre la fin de la convergence et ouvrir un GO dedie.

## Source canonique

- `docs/COLLECTORS_FAMILY_DOCTRINE_01.md`
- `docs/COLLECTORS_MIGRATION_MAP_01.md`

## NEXT_GO

`GO_COLLECTORS_BASELINE_INVENTORY_01`
