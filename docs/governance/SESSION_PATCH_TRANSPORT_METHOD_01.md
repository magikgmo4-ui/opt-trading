---
doc_id: OPT_TRADING_SESSION_PATCH_TRANSPORT_METHOD_01
doc_type: governance_method
repo: opt-trading
project: opt-trading
module: doc_ops
go_id: GO_OPT_TRADING_DOC_OPS_METHOD_SESSION_PATCH_TRANSPORT_01
status: draft
lifecycle_stage: governance_candidate
surface: governance
source_kind: canonical_candidate
updated_at: 2026-05-21
topic_keys:
  - opt-trading
  - session_docs
  - patch_transport
  - git_apply
  - ide_workload_reduction
reference_canonique_principale: docs/governance/SESSION_PATCH_TRANSPORT_METHOD_01.md
point_de_reprise: "Section 10 - Méthode canonique"
links:
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
  - docs/governance/PARENT_CONTINUITY_INDEX_INBOX_METHOD_01.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_METHOD_SESSION_PATCH_TRANSPORT_01/00_INITIAL_PROJECT_DOC.md
  - tools/session_transport/README.md
---

# SESSION_PATCH_TRANSPORT_METHOD_01

## 1. Objet

Définir la méthode canonique de transport des documents produits en session conversationnelle vers le repo Git, au moyen de fichiers `.patch`.

## 2. Principe

```text
session conversationnelle
  -> produit un .patch
    -> l'utilisateur le dépose à la racine du repo local
      -> bootstrap optionnel vers bundles/<GO_ID>/patches/
        -> dépôt local applique avec git apply --check
          -> git apply
            -> validations
              -> commit local
                -> PR / merge si requis
```

## 3. Statut du `.patch`

Un `.patch` est un artefact de transport.

Il ne remplace pas :

- les fichiers appliqués dans Git;
- le dossier chantier;
- le bundle;
- les index;
- le closeout.

Après application et commit, la source de vérité redevient le repo.

## 4. Zone d'entrée IDE

Emplacement pratique temporaire :

```text
repo root/*.patch
```

Règle :

- l'utilisateur télécharge le patch depuis ChatGPT;
- le dépose à la racine du repo local;
- l'IDE ou l'opérateur applique/boote le patch;
- aucun patch racine ne doit être committé.

## 5. Emplacement canonique

Emplacement principal :

```text
bundles/<GO_ID>/patches/<YYYYMMDD>_<GO_ID>_<slug>.patch
```

Exemple :

```text
bundles/GO_OPT_TRADING_BUNDLES_CHILD_IDE_DEPORTABLE_PACK_01/patches/20260521_GO_OPT_TRADING_BUNDLES_CHILD_IDE_DEPORTABLE_PACK_01_initial_bundle.patch
```

## 6. Emplacement fallback

Si le bundle n'existe pas encore :

```text
docs/chantiers/<GO_ID>/patches/<YYYYMMDD>_<GO_ID>_<slug>.patch
```

Ce fallback doit être temporaire.

Dès que le bundle existe, le patch doit être conservé ou recopié sous :

```text
bundles/<GO_ID>/patches/
```

## 7. Pourquoi `bundles/<GO_ID>/patches/`

- un bundle porte les artefacts opérables;
- un patch est opérable par IDE/local;
- le patch reste rattaché à son GO;
- le dossier chantier garde le contexte et le verdict;
- la racine repo reste propre.

## 8. Règle de nommage

Format :

```text
<YYYYMMDD>_<GO_ID>_<slug>.patch
```

Contraintes :

- date UTC ou locale opérationnelle stable;
- GO_ID complet;
- slug court;
- pas d'espace;
- pas de secrets;
- pas de patch anonyme.

## 9. Scripts d'application

Scripts canoniques :

```text
tools/session_transport/bootstrap_patch_inbox.sh
tools/session_transport/bootstrap_patch_inbox.ps1
tools/session_transport/apply_session_patch.sh
tools/session_transport/apply_session_patch.ps1
```

Ces scripts :

- vérifient le repo Git;
- acceptent un chemin `.patch`;
- peuvent basculer sur une branche cible;
- lancent `git apply --check`;
- appliquent le patch;
- lancent `git diff --check`;
- listent les fichiers modifiés;
- ne commitent pas automatiquement.

## 10. Validation minimale

Après application :

```bash
git diff --check
git status --short --untracked-files=all
git diff --name-only
find . -maxdepth 1 -type f -name '*.patch' -print
```

Validation no-secrets recommandée sur les fichiers modifiés.

## 11. Méthode canonique

Pour tout transport de docs de session vers Git :

1. générer un `.patch` complet depuis la session conversationnelle;
2. télécharger le `.patch`;
3. déposer le `.patch` à la racine du repo local;
4. nommer ou bootstrapper le patch selon `<YYYYMMDD>_<GO_ID>_<slug>.patch`;
5. conserver le patch sous `bundles/<GO_ID>/patches/` si le bundle existe;
6. sinon utiliser temporairement `docs/chantiers/<GO_ID>/patches/`;
7. appliquer localement avec `tools/session_transport/apply_session_patch.*`;
8. valider;
9. commit;
10. ouvrir PR si nécessaire;
11. la conversation fait la review GitHub/PR.

## 12. Interdits

- pas de patch contenant des secrets;
- pas de patch destructif sans garde explicite;
- pas de patch runtime caché dans un GO doc-only;
- pas de patch comme source canonique unique;
- pas de modification d'index global implicite;
- pas de commit automatique par script standard;
- pas de patch à la racine dans le commit.

## 13. Bloc mémoire canonique proposé

```text
Transport docs session -> Git:
les documents préparés en session conversationnelle doivent être transportés vers le repo via un fichier .patch. Le patch téléchargé est déposé temporairement à la racine du repo local, puis bootstrapé vers bundles/<GO_ID>/patches/ avant conservation durable. Le .patch est un artefact de transport, jamais la source canonique finale. Après application et commit, le repo redevient source de vérité. L’IDE doit être réduit à apply -> validate -> commit -> report.
```
