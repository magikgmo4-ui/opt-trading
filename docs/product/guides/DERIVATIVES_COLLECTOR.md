---
doc_id: OPT_TRADING_GUIDE_DERIVATIVES_COLLECTOR
doc_type: user_guide
repo: opt-trading
status: reference
lifecycle_stage: product_usage
source_kind: canonical
updated_at: 2026-05-18
links:
  - docs/COLLECTORS_FAMILY_DOCTRINE_01.md
  - docs/COLLECTORS_MIGRATION_MAP_01.md
  - docs/chantiers/GO_COLLECTORS_BASELINE_INVENTORY_01/90_CLOSEOUT.md
  - docs/chantiers/GO_COLLECTORS_SELECTIVE_RUNTIME_EXTRACTION_DECISION_01/90_CLOSEOUT.md
  - docs/chantiers/GO_COLLECTORS_HELPER_EXTRACTION_IMPL_10_V2/90_CLOSEOUT.md
---

# Guide - derivatives_collector

## 1_MASTER_TARGET

Collecteur canonique compatible famille collector, doctrine/vocabulaire/artifacts/config/surface operateur alignes.

## FINAL_TARGET

Module collecteur unifie avec doctrine famille appliquee (phases 0-5), outputs standardises, wrappers operationnels.

## CURRENT_STATE

`USABLE_LIMITED` -- Module operationnel multi-versions (V3->V13). Doctrine famille alignee, separation runtime maintenue, helper extractions prouvees deroulees sans migration de logique metier.

## USAGE_ALLOWED_NOW

- Collecter des donnees de marches derives.
- Exporter en JSON/CSV.
- Exploiter la surface dans le cadre de la doctrine famille alignee.

## USAGE_FORBIDDEN_NOW

- Forcer une migration runtime immediate vers `collectors_core`.
- Ajouter un provider supplementaire avant la fin de la convergence.
- Utiliser comme produit fini sans limites.

## IMPLEMENTATION_PATH

1. Preserver la separation runtime `derivatives_collector` / `collectors_core`.
2. N'extraire que des helpers utilitaires prouvables.
3. Clarifier les callers secondaires comme `marketdata` seulement si besoin reel.
4. Maintenir la surface operateur et les exports sans migration business prematuree.

## CONTINUITY_STATE

Actif -- doctrine famille alignee ; futures extractions uniquement si prouvees et ciblees.

## MACHINE / SURFACE

`admin-trading` (runtime collecte).

## REPRISE_POINT

```text
docs/COLLECTORS_MIGRATION_MAP_01.md
docs/COLLECTORS_FAMILY_DOCTRINE_01.md
docs/chantiers/GO_COLLECTORS_SELECTIVE_RUNTIME_EXTRACTION_DECISION_01/90_CLOSEOUT.md
docs/chantiers/GO_COLLECTORS_HELPER_EXTRACTION_IMPL_10_V2/90_CLOSEOUT.md
```

## TODO

1. Poursuivre seulement les extractions helper-first prouvees.
2. Garder la logique metier hors des extractions utilitaires.
3. Clarifier `marketdata` et autres callers secondaires uniquement si utile.

## REMAINING_GAP

Rollout selectif des helper extractions, convergence surface operateur et clarification des callers secondaires si besoin reel.

## NEXT_GO

Poursuivre le rollout des helper extractions prouvees sans casser la separation runtime.

## PROMOTION_CONDITIONS

`USABLE_LIMITED` -> `USABLE_NOW` quand :
- surface operateur stabilisee,
- callers secondaires clarifies,
- aucun besoin d'extraction business non borne,
- closeout produit plus stable pose.

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
- Comprendre que la separation runtime avec `collectors_core` reste volontaire.

## Commandes / acces

- Module : `modules/derivatives_collector/`
- Doctrine famille : `docs/COLLECTORS_FAMILY_DOCTRINE_01.md`
- Migration map : `docs/COLLECTORS_MIGRATION_MAP_01.md`
- Chaine helper extraction : `docs/chantiers/GO_COLLECTORS_HELPER_EXTRACTION_IMPL_10_V2/90_CLOSEOUT.md`

## Procedure simple

1. Verifier l'etat du collector via wrapper cmd.
2. Lancer une collecte.
3. Verifier les exports JSON/CSV.
4. Revenir a la doctrine famille si une extraction ou un refactor est envisage.
5. Ne pas ajouter de provider ni forcer une migration business sans GO dedie.

## Verification PASS

- Exports lisibles.
- Donnees coherentes avec les marches cibles.
- Doctrine famille respectee.
- Aucune migration runtime forcee.

## Limites

- Surface encore `USABLE_LIMITED`.
- Migration runtime vers `collectors_core` non forcee.
- Appels secondaires a clarifier au cas par cas.

## Depannage

- Exports incoherents : verifier config et logs.
- Doctrine famille floue : relire `COLLECTORS_FAMILY_DOCTRINE_01.md`.
- Nouveau provider necessaire : ouvrir un GO dedie, sans casser la separation runtime.

## Source canonique

- `docs/COLLECTORS_FAMILY_DOCTRINE_01.md`
- `docs/COLLECTORS_MIGRATION_MAP_01.md`
 - `docs/chantiers/GO_COLLECTORS_SELECTIVE_RUNTIME_EXTRACTION_DECISION_01/90_CLOSEOUT.md`
 - `docs/chantiers/GO_COLLECTORS_HELPER_EXTRACTION_IMPL_10_V2/90_CLOSEOUT.md`

## RISKS

- À qualifier.
