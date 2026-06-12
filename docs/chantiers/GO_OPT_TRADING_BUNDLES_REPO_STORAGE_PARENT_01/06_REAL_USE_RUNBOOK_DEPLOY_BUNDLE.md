---
doc_id: GO_OPT_TRADING_BUNDLES_REPO_STORAGE_PARENT_01_REAL_USE_RUNBOOK_DEPLOY_BUNDLE
doc_type: runbook
repo: opt-trading
project: opt-trading
module: bundles
go_id: GO_OPT_TRADING_BUNDLES_REPO_STORAGE_PARENT_01
status: accepted
lifecycle_stage: operational_method
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-04-24
topic_keys:
  - opt-trading
  - deploy_bundle
  - deploy_module_multi_machine
  - runbook
  - real-use
  - multi-machine
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_BUNDLES_REPO_STORAGE_PARENT_01/06_REAL_USE_RUNBOOK_DEPLOY_BUNDLE.md
point_de_reprise: "17_RESUME_POINT"
links:
  - docs/chantiers/GO_OPT_TRADING_BUNDLES_REPO_STORAGE_PARENT_01/04A_DEPLOY_BUNDLE_IMPLEMENTATION_ADDENDUM.md
  - docs/chantiers/GO_OPT_TRADING_BUNDLES_REPO_STORAGE_PARENT_01/05_CROSSCHECK_DEPLOY_MODULE_MULTI_MACHINE.md
  - deploy_module_multi_machine/README.md
---

# 06_REAL_USE_RUNBOOK_DEPLOY_BUNDLE

## 1_MASTER_TARGET

Définir l'utilisation réelle d'un `deploy_bundle` pour piloter `deploy_module_multi_machine` sans le remplacer.

Ce runbook est opératoire mais ne déclenche aucun déploiement par lui-même.

## 3_INITIAL_NEED

Documenter au bon endroit une méthode utilisable réellement :

- créer ou récupérer un `deploy_bundle` ;
- vérifier les cibles ;
- lancer preflight ;
- lancer dry-run ;
- lancer deploy réel seulement si validé ;
- produire closeout.

## 7_CANONICAL_STATE

- `deploy_bundle` est reconnu comme type de bundle.
- Le moteur réel reste `deploy_module_multi_machine`.
- Le déploiement réel doit partir d'`admin-trading` comme hub, selon le module existant.
- Les cibles sont Linux/POSIX.
- `cursor-ai` n'est pas cible de déploiement `/opt/trading/...`.

## 11_KEY_DECISIONS

- Preflight obligatoire.
- Dry-run obligatoire avant deploy réel.
- Validation humaine obligatoire avant deploy réel.
- Post-install explicite seulement.
- Cleanup stale lock explicite seulement.
- Closeout obligatoire après action réelle ou tentative.

## 12_INVARIANTS

- Pas de bypass de `deploy_module_multi_machine`.
- Pas de SSH/SCP direct parallèle dans le bundle.
- Pas de secrets.
- Pas de cible Windows.
- Pas de deploy réel sans validation.
- Pas de cleanup lock silencieux.
- Pas de rollback sans trace.

## 13_REAL_USE_SEQUENCE

Séquence opératoire :

```text
1. Lire README_BUNDLE.md
2. Vérifier manifest.json
3. Vérifier targets
4. Vérifier source_dir
5. Exécuter status
6. Exécuter preflight
7. Lire résultat par cible
8. Exécuter plan --dry-run
9. Lire résultat dry-run
10. Demander validation humaine
11. Exécuter deploy réel si validé
12. Exécuter sanity ou vérifier sanity intégrée
13. Produire closeout
```

## 14_COMMANDS_BASE

### Status

```bash
cmd-deploy_module_multi_machine status
```

### Preflight

```bash
cmd-deploy_module_multi_machine preflight \
  --module-name <module> \
  --source-dir /opt/trading/modules/<module> \
  --targets <targets>
```

### Dry-run

```bash
cmd-deploy_module_multi_machine plan \
  --module-name <module> \
  --source-dir /opt/trading/modules/<module> \
  --targets <targets> \
  --dry-run
```

### Deploy réel gated

```bash
cmd-deploy_module_multi_machine deploy \
  --module-name <module> \
  --source-dir /opt/trading/modules/<module> \
  --targets <targets>
```

### Sanity distant

```bash
cmd-deploy_module_multi_machine sanity \
  --module-name <module> \
  --source-dir /opt/trading/modules/<module> \
  --targets <targets>
```

## 15_POST_INSTALL_RULE

Post-install interdit par défaut.

Autorisé seulement si explicitement demandé :

```bash
cmd-deploy_module_multi_machine deploy \
  --module-name <module> \
  --source-dir /opt/trading/modules/<module> \
  --targets <targets> \
  --post-install
```

## 16_LOCK_RULE

Si lock stale :

- documenter le lock ;
- vérifier propriétaire ;
- utiliser cleanup seulement si explicitement validé.

```bash
cmd-deploy_module_multi_machine deploy \
  --module-name <module> \
  --source-dir /opt/trading/modules/<module> \
  --targets <targets> \
  --cleanup-stale-lock
```

## 17_OUTPUT_TO_CAPTURE

À capturer dans le closeout :

```text
MODULE=
SOURCE_DIR=
TARGETS=
STATUS_RESULT=
PREFLIGHT_RESULT=
DRY_RUN_RESULT=
DEPLOY_RESULT=
SANITY_RESULT=
RUN_ID=
LOCK_STATUS=
POST_INSTALL=
FAILURES=
ROLLBACK_REQUIRED=
NEXT_STEP=
```

## 18_STOP_CONDITIONS

Stop immédiat si :

- source_dir absent ;
- target inconnu ;
- SSH FAIL ;
- `/opt/trading` absent ou non writable selon besoin ;
- lock non stale présent ;
- preflight FAIL ;
- dry-run FAIL ;
- sudo requis mais non validé ;
- demande de deploy réel non validée.

## 19_CLOSEOUT_TEMPLATE

```text
# CLOSEOUT deploy_bundle <GO_ID>

## ETAT_DEPART
## TARGETS
## PREFLIGHT
## DRY_RUN
## DEPLOY_REAL_IF_ANY
## SANITY
## LOCKS
## POST_INSTALL
## FAILURES
## ROLLBACK
## VERDICT
## NEXT_STEP
```

## 20_VERDICT

Verdict d'utilisation : `READY_AS_METHOD`.

La méthode est prête comme cadre opératoire. Chaque déploiement réel doit être ouvert ou rattaché à un GO spécifique.

## 17_RESUME_POINT

```text
GO_OPT_TRADING_BUNDLES_REPO_STORAGE_PARENT_01

Fichier:
docs/chantiers/GO_OPT_TRADING_BUNDLES_REPO_STORAGE_PARENT_01/06_REAL_USE_RUNBOOK_DEPLOY_BUNDLE.md

État:
runbook d'utilisation réelle créé.

Prochaine action:
checkpoint parent ou sous-GO pour créer un premier deploy_bundle réel.
```

## RISKS

- À qualifier.
