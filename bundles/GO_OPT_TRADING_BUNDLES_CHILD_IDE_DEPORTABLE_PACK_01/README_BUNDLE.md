# Bundle GO_OPT_TRADING_BUNDLES_CHILD_IDE_DEPORTABLE_PACK_01

## Objet

Paquet IDE déportable pour réduire la charge de travail IDE.

Ce bundle contient des prompts, checklists, templates et patchs prêts à utiliser pour cadrer, appliquer, valider, reviewer et fermer un travail doc-only ou pré-implémentation.

## GO servi

```text
GO_OPT_TRADING_BUNDLES_CHILD_IDE_DEPORTABLE_PACK_01
```

## Parent canonique

```text
GO_OPT_TRADING_BUNDLES_REPO_STORAGE_PARENT_01
```

## Branche recommandée

```text
go/GO_OPT_TRADING_BUNDLES_CHILD_IDE_DEPORTABLE_PACK_01
```

## Sources canoniques

- `docs/chantiers/GO_OPT_TRADING_BUNDLES_REPO_STORAGE_PARENT_01/01_BUNDLE_STORAGE_METHOD.md`
- `docs/chantiers/GO_OPT_TRADING_BUNDLES_REPO_STORAGE_PARENT_01/04_BUNDLE_IMPLEMENTATION_METHOD.md`
- `docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md`
- `docs/index/MACHINE_WORK_SPLIT_ANTI_CONFLICT_01.md`
- `docs/governance/SESSION_PATCH_TRANSPORT_METHOD_01.md`

## Contraintes

- doc-only ;
- no secrets ;
- no runtime ;
- no trading live ;
- no global indexes ;
- no new sovereign doctrine ;
- no duplicate bundle method ;
- no root-level patch committed.

## Patch inbox pratique

Pour l'IDE/humain :

```text
1. Télécharger le .patch depuis la session.
2. Le déposer à la racine du repo local.
3. L'appliquer ou le bootstrapper.
4. Ne jamais committer le patch depuis la racine.
```

Stockage canonique après bootstrap :

```text
bundles/<GO_ID>/patches/
```

## Ordre d'exécution

1. Lire `prompts/GO_PROMPT_01_PRECHECK_AND_SCOPE.md`.
2. Appliquer `prompts/GO_PROMPT_02_DOC_ONLY_APPLY.md`.
3. Valider avec `checklists/CHECKLIST_VALIDATION.md`.
4. Reviewer avec `prompts/GO_PROMPT_03_REVIEW_AND_CLOSEOUT.md`.
5. Utiliser `prompts/GO_PROMPT_04_CI_TRIAGE_IF_NEEDED.md` seulement si CI échoue.

## Entrypoints

```text
prompts/GO_PROMPT_01_PRECHECK_AND_SCOPE.md
prompts/GO_PROMPT_02_DOC_ONLY_APPLY.md
checklists/CHECKLIST_EXECUTION.md
checklists/CHECKLIST_NO_FRICTION.md
docs/REPRISE_PACKET_TEMPLATE.md
patches/README_PATCHES.md
```

## Sortie attendue

L'IDE doit retourner :

- branche courante ;
- fichiers créés/modifiés ;
- résultat `git diff --check` ;
- résultat no-secrets ;
- fichiers hors scope ;
- commit SHA si créé ;
- prochain geste.

## Stop conditions

Arrêter si :

- conflit Git non trivial ;
- branche existante avec contenu divergent ;
- fichier similaire déjà existant ;
- runtime touché ;
- index global modifié ;
- secret détecté ;
- scope dépassé ;
- patch racine sur le point d'être committé.
