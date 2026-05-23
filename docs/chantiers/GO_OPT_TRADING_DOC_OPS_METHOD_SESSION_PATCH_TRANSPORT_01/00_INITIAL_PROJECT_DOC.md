---
doc_id: GO_OPT_TRADING_DOC_OPS_METHOD_SESSION_PATCH_TRANSPORT_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: doc_ops
go_id: GO_OPT_TRADING_DOC_OPS_METHOD_SESSION_PATCH_TRANSPORT_01
status: draft
lifecycle_stage: method_canonization
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-05-21
topic_keys:
  - opt-trading
  - doc_ops
  - session_docs
  - patch_transport
  - global_indexes
  - index_aggregation
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_DOC_OPS_METHOD_SESSION_PATCH_TRANSPORT_01/00_INITIAL_PROJECT_DOC.md
point_de_reprise: "17_RESUME_POINT"
links:
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
  - docs/governance/PARENT_CONTINUITY_INDEX_INBOX_METHOD_01.md
  - docs/governance/SESSION_PATCH_TRANSPORT_METHOD_01.md
  - docs/governance/GLOBAL_INDEX_UPDATE_TRIGGER_RULE_01.md
  - tools/session_transport/README.md
---

# GO_OPT_TRADING_DOC_OPS_METHOD_SESSION_PATCH_TRANSPORT_01

## 1_MASTER_TARGET

Canoniser une méthode de transport des docs préparées en session conversationnelle vers Git, en utilisant des fichiers `.patch` applicables localement, afin de réduire la charge IDE à `apply -> validate -> commit`.

## 2_INITIAL_PROJECT_DOC

Ce chantier ajoute une méthode doc-ops sans runtime.

Il formalise :

- l'emplacement temporaire d'entrée des `.patch`;
- l'emplacement canonique des `.patch`;
- les scripts d'application locale;
- le statut des `.patch` comme transport, pas source canonique finale;
- la règle de suggestion / déclenchement des mises à jour d'index globaux.

## 3_INITIAL_NEED

Les sessions conversationnelles peuvent produire beaucoup de documents utiles. Pour éviter de consommer l'IDE à recopier, structurer et corriger des docs, la session doit produire un `.patch` Git prêt à appliquer.

L'utilisateur veut aussi éviter :

- contradictions;
- doublons;
- fourches;
- écarts;
- index globaux modifiés trop tôt;
- perte d'horizon produit / master target.

## 4_MASTER_PROJECT_PLAN

1. Garder `bundles/<GO_ID>/` comme emplacement principal des artefacts opérables.
2. Ajouter `bundles/<GO_ID>/patches/` comme emplacement canonique des `.patch`.
3. Utiliser la racine du repo comme inbox temporaire de dépôt manuel.
4. Ajouter des scripts locaux d'application sous `tools/session_transport/`.
5. Ajouter une méthode de gouvernance pour les index globaux.
6. Ne pas modifier les index globaux dans ce GO.
7. Laisser un point de reprise clair.

## 5_GO_PLAN

Livrables :

- `docs/governance/SESSION_PATCH_TRANSPORT_METHOD_01.md`
- `docs/governance/GLOBAL_INDEX_UPDATE_TRIGGER_RULE_01.md`
- `tools/session_transport/README.md`
- `tools/session_transport/apply_session_patch.sh`
- `tools/session_transport/apply_session_patch.ps1`
- `tools/session_transport/bootstrap_patch_inbox.sh`
- `tools/session_transport/bootstrap_patch_inbox.ps1`
- `docs/index/inbox/GO_OPT_TRADING_DOC_OPS_METHOD_SESSION_PATCH_TRANSPORT_01.md`

## 6_FINAL_TARGET

À terme, toute session conversationnelle qui produit des docs pour Git peut fournir :

```text
.patch + emplacement cible + script apply + validation + mémoire courte
```

L'IDE n'a plus à reconstruire la méthode.

## 7_CANONICAL_STATE

La continuité locale parent + inbox existe déjà.

La méthode bundle existe déjà.

Ce GO ajoute la couche manquante : transport `.patch` de session vers repo.

## 8_VALIDATED_PLAN

Aucune modification des index globaux.

Les nouvelles règles restent sous `docs/governance/` et l'entrée d'agrégation reste dans `docs/index/inbox/`.

## 9_SELECTED_SOLUTION

Zone d'entrée pratique :

```text
repo root/*.patch
```

Emplacement canonique des patchs :

```text
bundles/<GO_ID>/patches/<YYYYMMDD>_<GO_ID>_<slug>.patch
```

Fallback si le bundle n'existe pas encore :

```text
docs/chantiers/<GO_ID>/patches/<YYYYMMDD>_<GO_ID>_<slug>.patch
```

Mais le fallback doit être migré vers `bundles/<GO_ID>/patches/` dès que le bundle est créé.

## 10_SELECTED_SETUP

Scripts d'application :

```text
tools/session_transport/apply_session_patch.sh
tools/session_transport/apply_session_patch.ps1
tools/session_transport/bootstrap_patch_inbox.sh
tools/session_transport/bootstrap_patch_inbox.ps1
```

Ils déplacent ou appliquent localement un patch, valident le diff, détectent les fichiers modifiés et ne commitent pas automatiquement.

## 11_KEY_DECISIONS

- `.patch` = transport de session, pas source de vérité durable.
- Une fois appliqué et committé, les fichiers Git deviennent la source de vérité.
- Les `.patch` peuvent être conservés sous `bundles/<GO_ID>/patches/` comme preuve et accélérateur.
- Les patchs téléchargés vont d'abord à la racine du repo local.
- Les patchs racine ne sont jamais committés tels quels.
- Les index globaux ne sont pas modifiés par défaut.
- La session conversationnelle peut suggérer un batch d'agrégation lorsque le master target change réellement.

## 12_INVARIANTS

- No secrets.
- No runtime.
- No trading live.
- No automatic global index update.
- No automatic commit from script.
- No patch as sole canonical source.
- No root-level patch committed.
- No parent closeout interpreted as product/master target closeout without verification.

## 13_ESTABLISHED

- `GO_INDEX.md` référence les GO non clos utiles.
- `GO_CLOSED_INDEX.md` reçoit les chantiers CLOSED/PASS sortis de `GO_INDEX.md`.
- `ACTIVE_STREAMS.md` référence l'actif ou le bloqué.
- `NEXT_GO_CANDIDATES.md` mappe 1 parent actif vers 1 next GO primaire.
- `REPRISE.md` est un support opératoire, pas une seconde vérité de liste.

## 14_HYPOTHESIS

- La méthode `.patch` peut devenir le transport standard des docs de session vers Git.
- Les index globaux doivent être mis à jour plus vite uniquement quand un changement de master target est réel.
- Le répertoire racine du repo est la meilleure zone d'entrée temporaire pour l'IDE.

## 15_REMAINING_GAP

- Appliquer ce patch final.
- Valider les scripts localement.
- Utiliser la méthode sur le bundle `GO_OPT_TRADING_BUNDLES_CHILD_IDE_DEPORTABLE_PACK_01`.
- Ouvrir au besoin un GO batch d'agrégation si un master target réel est atteint.

## 16_TODO

1. Déposer le patch final à la racine du repo.
2. Appliquer le patch final.
3. Déplacer tout autre patch racine vers `bundles/<GO_ID>/patches/`.
4. Vérifier `git diff --check`.
5. Vérifier scripts.
6. Committer.
7. Conserver les futurs `.patch` sous `bundles/<GO_ID>/patches/`.

## 17_RESUME_POINT

```text
GO_OPT_TRADING_DOC_OPS_METHOD_SESSION_PATCH_TRANSPORT_01

État:
méthode patch transport préparée en session.

Prochaine action:
appliquer le patch final localement, valider les scripts, commit.

Interdits:
index globaux, runtime, trading live, secrets, commit automatique par script, patch racine committé.
```
