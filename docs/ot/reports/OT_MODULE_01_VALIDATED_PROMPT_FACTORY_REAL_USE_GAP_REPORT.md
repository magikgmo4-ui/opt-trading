# OT-MODULE-01 — VALIDATED_PROMPT_FACTORY (REAL USE) — GAP REPORT

Date (America/Montreal) : 2026-03-14

## GAP-01 — Continuité absente dans le mode bundle_transfer (template)
- **Type** : À CORRIGER (écart prouvé)
- **Constat** : le prompt généré en mode `bundle_transfer` ne rendait pas les champs `CONTRAINTES`, `DEPENDANCES`, `SUITE`, `POINT DE REPRISE`.
- **Impact** : prompt moins “workflow-compatible” (continuité doc+kanban+reprise non portée jusqu’au prompt).
- **Preuve** : code du template `bundle_transfer` dans `modules/validated_prompt_factory/app/validated_prompt_factory.py` (avant patch) n’incluait pas ces champs.
- **Correction appliquée** : template `bundle_transfer` étendu pour inclure contraintes/risques/suite/point de reprise.
- **Preuve post-correctif** : `state/vpf_real_use_2026-03-14/prompt_bundle_transfer.txt` contient désormais `## SUITE` et `## POINT DE REPRISE`.

## RÉSERVE MINEURE — Wrappers bash en environnement Windows
- **Type** : RÉSERVE MINEURE (non bloquant)
- **Constat** : `cmd.sh` et `sanity.sh` sont des scripts bash ; l’exécution native Windows n’est pas le chemin nominal.
- **Impact** : sur poste Windows, l’usage “réel” passe par l’appel direct du script Python.
- **Point à confirmer** : parcours complet via wrappers sur machine Linux cible.

