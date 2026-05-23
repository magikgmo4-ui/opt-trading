# Chaîne canonique — Résumé des 4 bundles

## Ordre d'exécution

```text
1. FINAL_COMBINED    — Session → IDE Patch Transport
2. IDE_APPLICATION_MATRIX — Matrice d'application IDE
3. TARGET_MASTER_TARGET_METHOD — Target / Master Target
4. FORMAT            — Patch Zip Execution Format
```

---

## 1. FINAL_COMBINED

**GO:** `GO_OPT_TRADING_DOC_OPS_SESSION_PATCH_TRANSPORT_FINAL_COMBINED_01`

**But :** Rendre une session conversationnelle capable de produire des chantiers Git transportables par patch, applicables par IDE avec matrice unique.

**Livrables (26 fichiers) :**

| Catégorie | Fichiers |
|---|---|
| Gouvernance | `SESSION_PATCH_TRANSPORT_METHOD_01.md`, `GLOBAL_INDEX_UPDATE_TRIGGER_RULE_01.md` |
| Chantier | `METHOD_SESSION_PATCH_TRANSPORT_01/00_INITIAL_PROJECT_DOC.md` |
| Bundle prompts | 4 prompts : PRECHECK_AND_SCOPE, DOC_ONLY_APPLY, REVIEW_AND_CLOSEOUT, CI_TRIAGE |
| Bundle checklists | 3 checklists : EXECUTION, VALIDATION, NO_FRICTION |
| Bundle templates | 4 templates : PATCH_PLAN, PR_REVIEW_PACKET, CI_FAILURE_TRIAGE, REPRISE_PACKET |
| Bundle meta | `manifest.json`, `validation_report.md`, `README_BUNDLE.md`, `patches/README_PATCHES.md` |
| Tools | `apply_session_patch.sh/.ps1`, `bootstrap_patch_inbox.sh/.ps1`, `tools/README.md` |
| Index | Parent chantier + inbox entries |

**Directives :** Un patch n'est jamais commité à la racine. Il est déposé → vérifié → bootstrappé vers `bundles/<GO_ID>/patches/` → appliqué → commité → push. Le `bootstrap_patch_inbox.sh` fait le renommage et le déplacement.

---

## 2. IDE_APPLICATION_MATRIX

**GO:** `GO_OPT_TRADING_DOC_OPS_SESSION_PATCH_IDE_APPLICATION_MATRIX_01`

**But :** Formaliser la matrice d'application des patchs par l'IDE (étape par étape, sans reconstruction du plan).

**Livrables (4 fichiers) :**

| Fichier | Rôle |
|---|---|
| `SESSION_PATCH_IDE_APPLICATION_MATRIX_01.md` | Gouvernance : méthode d'application IDE |
| `bundles/.../docs/EXEMPLE_MATRICE_APPLICATION_PATCH.md` | Matrice concrète : ordre, vérifications, rollback |
| `bundles/.../prompts/GO_PROMPT_05_IDE_PATCH_APPLICATION_MATRIX.md` | Prompt IDE : appliquer un patch via la matrice |
| `docs/index/inbox/...md` | Entrée d'index |

**Directives :** L'IDE suit la matrice : checkout branche → `git apply --check` → `git apply` → `git diff --check` → add → commit → push → PR. Ne jamais appliquer un patch sans passer par la matrice.

---

## 3. TARGET_MASTER_TARGET_METHOD

**GO:** `GO_OPT_TRADING_BUNDLES_TARGET_MASTER_TARGET_METHOD_01`

**But :** Définir le système target/master_target pour qu'un bundle soit évaluable : chaque bundle a une target finale et s'inscrit dans un master target horizontal.

**Livrables (6 fichiers) :**

| Fichier | Rôle |
|---|---|
| `BUNDLE_TARGET_AND_MASTER_TARGET_METHOD_01.md` | Gouvernance : méthode target/master_target |
| `bundles/BUNDLE_TARGET_INDEX.md` | Index léger de tous les targets |
| `bundles/.../TARGETS.md` | Target + master_target + critères de complétion |
| `bundles/.../bundle_meta/target_card.json` | Fiche machine-readable (target_id, status, critères) |
| `docs/chantiers/.../00_INITIAL_PROJECT_DOC.md` | Chantier de la méthode |
| `docs/index/inbox/...md` | Entrée d'index |

**Directives :** Un bundle déclare sa `6_FINAL_TARGET` et son `1_MASTER_TARGET`. L'atteinte du target est vérifiée par des critères binaires. Après target atteint, on évalue : master_target_reached ? next_bundle_candidate ? global_index_update_candidate ?

---

## 4. FORMAT

**GO:** `GO_OPT_TRADING_DOC_OPS_CHILD_PATCH_ZIP_EXECUTION_FORMAT_BUNDLE_01` + contenu V2

**But :** Formaliser le format d'exécution des patchs zip (processus complet de création, transport et application entre session et IDE).

**Livrables (24 fichiers — 6 structure bundle + 18 contenu V2) :**

| Catégorie | Fichiers |
|---|---|
| Structure bundle | `README_BUNDLE.md`, `TARGETS.md`, `target_card.json`, `patches/README_PATCHES.md` + inbox |
| Gouvernance | `PATCH_ZIP_EXECUTION_FORMAT_V2_01.md` |
| Chantier complet | 8 fichiers : launch prompt, session context, e2e runbook, job graph, external apps, evidence contract, cowork checklist, target gaps |
| Job packets AI workers | 8 JSON : read inventory, fast triage, patch draft, test plan, doc draft, endpoint audit, write gated |
| Chantier bundle method | `00_INITIAL_PROJECT_DOC.md` |

**Directives :** Le format V2 est patch-first : le `.patch` est l'artefact canonique d'échange Git ; le `.zip` est un sidecar optionnel réservé aux charges lourdes, temporaires ou hors repo. Les job packets automatisent le diagnostic, le draft et le test des patchs via workers AI.

---

## Schéma global

```text
SESSION → plan validé
         → target/master_target (méthode #3)
         → bundle avec TARGETS.md (méthode #3)
         → .patch déposé à la racine (méthode #1)
         → bootstrap vers bundles/<GO_ID>/patches/ (tool #1)
         → matrice IDE pour application (méthode #2)
         → format zip pour exécution (méthode #4)
         → commit + PR + merge
         → évaluation target/master_target (méthode #3)
```

**Règle d'or :** Aucun `.patch` n'est commité à la racine. Le patch source est toujours archivé sous `bundles/<GO_ID>/patches/` avant application.

## Livraison

| # | GO | PR | Statut |
|---|---|---|---|
| 1 | FINAL_COMBINED | [#701](https://github.com/magikgmo4-ui/opt-trading/pull/701) | livré |
| 2 | IDE_APPLICATION_MATRIX | dans `806bf575` | livré |
| 3 | TARGET_MASTER_TARGET_METHOD | dans `806bf575` | livré |
| 4a | FORMAT bundle | [#697](https://github.com/magikgmo4-ui/opt-trading/pull/697) | livré |
| 4b | FORMAT V2 content | [#700](https://github.com/magikgmo4-ui/opt-trading/pull/700) | livré |
