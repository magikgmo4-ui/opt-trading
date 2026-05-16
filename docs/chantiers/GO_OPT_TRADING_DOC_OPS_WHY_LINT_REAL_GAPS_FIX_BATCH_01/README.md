# GO_OPT_TRADING_DOC_OPS_WHY_LINT_REAL_GAPS_FIX_BATCH_01

## Scope

- `docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/00_INITIAL_PROJECT_DOC.md`

## Decision

- Corriger uniquement le document d'entree du chantier dans ce batch 01.
- Reporter les autres fichiers parce qu'ils cumulent des gaps de structure ou des ambiguities de classe documentaire deja signalees dans le plan V1.

## Objectif

- Corriger un vrai gap WHY a haute confiance, sans auto-fix, sans correction massive et sans toucher au validateur.

## Etat canonique et continuite

- Base canonique : PR #442 mergee, merge commit `68cdbefb588577cfc16de617cfc1d49d244c4a91` present dans le repo.
- Continuite : ce batch prolonge la sequence `baseline V1 -> remediation plan V1 -> real gaps fix plan V1`.
- Reprise suivante : ouvrir un batch court sur d'autres `MISSING_WHY_SECTION` a haute confiance avant de traiter les gaps de structure plus ambigus.

## Gap initial

- `MISSING_WHY_SECTION` sur le document d'entree du chantier.
- Le document avait le cadrage et les contraintes, mais pas de WHY explicite.

## Correction appliquee

- Ajout d'une section `## WHY` concise.
- Le WHY explicite que ce cadrage sert a verifier les gaps documentaires avant toute extension du systeme, en restant lecture seule et warning-only.

## Validation

- `git diff --check` : OK.
- Scan read-only WHY lint : le fichier cible ne remonte plus sur `MISSING_WHY_SECTION`.
- Les autres findings restants sont hors lot.

## Risques restants

- Beaucoup de documents anciens gardent des marqueurs manquants.
- Les artefacts de rapport et de triage restent sources de bruit de self-reference.
- Aucun changement n'a ete fait au validateur.

## Gaps reportes

- Tous les autres `MISSING_WHY_SECTION` et les findings de structure (`MISSING_FINAL_TARGET`, `MISSING_INVARIANTS`, `MISSING_RESUME_POINT`) restent a traiter dans des lots suivants.

## Statut

- PASS: batch manuel borne, diff reviewable, validateur intact.
