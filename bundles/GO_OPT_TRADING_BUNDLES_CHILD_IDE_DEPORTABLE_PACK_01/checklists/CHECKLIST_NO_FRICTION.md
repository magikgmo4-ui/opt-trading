# CHECKLIST_NO_FRICTION

## Objectif

Éviter contradiction, doublon, fourche, écart ou pollution des surfaces canoniques.

## Avant application

- [ ] Confirmer le parent `GO_OPT_TRADING_BUNDLES_REPO_STORAGE_PARENT_01`.
- [ ] Confirmer que la méthode bundle existe déjà.
- [ ] Confirmer qu'on applique la méthode, sans la remplacer.
- [ ] Confirmer absence de bundle équivalent.
- [ ] Confirmer que les patchs racine sont seulement temporaires.

## Pendant application

- [ ] Ne pas modifier les index globaux.
- [ ] Ne pas créer de doctrine concurrente.
- [ ] Ne pas renommer des surfaces existantes.
- [ ] Ne pas reclassifier le parent.
- [ ] Ne pas ajouter de runtime.
- [ ] Ne pas ajouter de scripts destructifs.
- [ ] Déplacer les patchs conservés sous `bundles/<GO_ID>/patches/`.

## Stop conditions

- [ ] Fichier équivalent déjà présent.
- [ ] Branche divergente.
- [ ] Scope dépassé.
- [ ] Secret détecté.
- [ ] Conflit Git.
- [ ] Besoin d'index global non explicitement validé.
- [ ] Patch racine staged par erreur.
