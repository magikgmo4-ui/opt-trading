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

# Guide - derivatives_collector

## 1_MASTER_TARGET

Collecteur canonique compatible famille collector, doctrine/vocabulaire/artifacts/config/surface operateur alignes.

## FINAL_TARGET

Module collecteur unifie avec doctrine famille appliquee (phases 0-5), outputs standardises, wrappers operationnels.

## CURRENT_STATE

`USABLE_LIMITED` -- Module operationnel multi-versions (V3->V13). Convergence doctrinale en cours. Artifacts, vocabulaire, config et surface operateur en cours d'alignement.

## USAGE_ALLOWED_NOW

- Collecter des donnees de marches derives.
- Exporter en JSON/CSV.
- Suivre la convergence doctrinale (phases 0-5).

## USAGE_FORBIDDEN_NOW

- Forcer une migration runtime immediate vers `collectors_core`.
- Ajouter un provider supplementaire avant la fin de la convergence.
- Utiliser comme produit fini sans limites.

## IMPLEMENTATION_PATH

1. Phase 0 : baseline inventory (`GO_COLLECTORS_BASELINE_INVENTORY_01`).
2. Phase 1 : vocabulary alignment.
3. Phase 2 : artifact family alignment.
4. Phase 3 : config boundary alignment.
5. Phase 4 : operator surface alignment.
6. Phase 5 : selective runtime extraction decision.

## CONTINUITY_STATE

Actif -- convergence doctrinale en cours.

## MACHINE / SURFACE

`admin-trading` (runtime collecte).

## REPRISE_POINT

```text
docs/COLLECTORS_MIGRATION_MAP_01.md
docs/COLLECTORS_FAMILY_DOCTRINE_01.md
```

## TODO

1. Baseline inventory.
2. Vocabulary alignment.
3. Artifact family alignment.
4. Config boundary alignment.
5. Operator surface alignment.

## REMAINING_GAP

Convergence doctrinale (phases 0-5), artifacts/vocabulaire/config/surface operateur a aligner.

## NEXT_GO

`GO_COLLECTORS_BASELINE_INVENTORY_01`

## PROMOTION_CONDITIONS

`USABLE_LIMITED` -> `USABLE_NOW` quand :
- phases 0-5 terminees,
- doctrine famille appliquee,
- closeout famille pose.

## Ce que c'est

Collecteur canonique de donnees de marches derives pour le trading.

## A quoi ca sert

Collecter les donnees marches derives, les exporter, alimenter les moteurs d'analyse.

## Quand l'utiliser

- Collecter des donnees de marches derives.
- Exporter vers les moteurs d'analyse.
- Suivre la convergence doctrinale.

## Quand ne pas l'utiliser

- Comme produit fini (convergence en cours).
- Pour forcer une migration runtime vers `collectors_core`.
- Pour ajouter un provider #3 prematurement.

## Prerequis

- Acces a `modules/derivatives_collector/`.
- Lecture de `docs/COLLECTORS_FAMILY_DOCTRINE_01.md`.
- Lecture de `docs/COLLECTORS_MIGRATION_MAP_01.md`.

## Commandes / acces

- Module : `modules/derivatives_collector/`
- Doctrine famille : `docs/COLLECTORS_FAMILY_DOCTRINE_01.md`
- Migration map : `docs/COLLECTORS_MIGRATION_MAP_01.md`

## Procedure simple

1. Verifier l'etat du collector via wrapper cmd.
2. Lancer une collecte.
3. Verifier les exports JSON/CSV.
4. Consulter la migration map pour la phase en cours.
5. Ne pas ajouter de provider avant convergence.

## Verification PASS

- Exports lisibles.
- Donnees coherentes avec les marches cibles.
- Doctrine famille respectee.
- Aucune migration runtime forcee.

## Limites

- Convergence doctrinale en cours (phases 0-5).
- Migration runtime vers `collectors_core` non immediate ni forcee.
- Pas de provider #3 avant convergence.

## Depannage

- Exports incoherents : verifier config et logs.
- Doctrine famille floue : relire `COLLECTORS_FAMILY_DOCTRINE_01.md`.
- Nouveau provider necessaire : attendre convergence, ouvrir GO dedie.

## Source canonique

- `docs/COLLECTORS_FAMILY_DOCTRINE_01.md`
- `docs/COLLECTORS_MIGRATION_MAP_01.md`
