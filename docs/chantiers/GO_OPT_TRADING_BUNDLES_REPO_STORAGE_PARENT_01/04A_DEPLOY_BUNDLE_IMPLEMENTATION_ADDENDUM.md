---
doc_id: GO_OPT_TRADING_BUNDLES_REPO_STORAGE_PARENT_01_DEPLOY_BUNDLE_IMPLEMENTATION_ADDENDUM
doc_type: bundle_implementation_addendum
repo: opt-trading
project: opt-trading
module: bundles
go_id: GO_OPT_TRADING_BUNDLES_REPO_STORAGE_PARENT_01
status: accepted
lifecycle_stage: method_application
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-04-24
topic_keys:
  - opt-trading
  - bundles
  - deploy_bundle
  - deploy_module_multi_machine
  - implementation
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_BUNDLES_REPO_STORAGE_PARENT_01/04A_DEPLOY_BUNDLE_IMPLEMENTATION_ADDENDUM.md
point_de_reprise: "17_RESUME_POINT"
links:
  - docs/chantiers/GO_OPT_TRADING_BUNDLES_REPO_STORAGE_PARENT_01/04_BUNDLE_IMPLEMENTATION_METHOD.md
  - docs/chantiers/GO_OPT_TRADING_BUNDLES_REPO_STORAGE_PARENT_01/05_CROSSCHECK_DEPLOY_MODULE_MULTI_MACHINE.md
  - deploy_module_multi_machine/README.md
---

# 04A_DEPLOY_BUNDLE_IMPLEMENTATION_ADDENDUM

## 1_MASTER_TARGET

Appliquer la validation du recroisement avec `deploy_module_multi_machine` en ajoutant officiellement le type `deploy_bundle` à la méthode d'implémentation des bundles.

## 3_INITIAL_NEED

Demande utilisateur :

> Ok je valide documente au bon endroit pour utilisation réelle et applique

## 7_CANONICAL_STATE

- `deploy_bundle` est désormais un type de bundle reconnu.
- Il sert à encadrer une opération `deploy_module_multi_machine`.
- Il ne remplace pas `deploy_module_multi_machine`.
- Il ne contient pas le runtime à déployer.
- Il contient prompts, checklists, scripts légers et manifest nécessaires à l'opérateur.

## 8_VALIDATED_PLAN

Définition appliquée :

```text
deploy_bundle = bundle IDE/opérateur qui prépare, guide, vérifie et journalise une opération deploy_module_multi_machine, sans contourner le module de déploiement.
```

## 10_SELECTED_SETUP

Structure canonique :

```text
bundles/<GO_ID>/
├── README_BUNDLE.md
├── prompts/
│   ├── GO_PROMPT_01_PREFLIGHT.md
│   ├── GO_PROMPT_02_DEPLOY_DRY_RUN.md
│   ├── GO_PROMPT_03_DEPLOY_REAL.md
│   └── GO_PROMPT_04_CLOSEOUT.md
├── checklists/
│   ├── CHECKLIST_TARGETS.md
│   ├── CHECKLIST_PREFLIGHT.md
│   ├── CHECKLIST_DEPLOY.md
│   └── CHECKLIST_ROLLBACK.md
├── scripts/
│   ├── README_SCRIPTS.md
│   ├── run_preflight.sh
│   └── run_deploy_dry_run.sh
└── bundle_meta/
    ├── manifest.json
    └── validation_report.md
```

## 11_KEY_DECISIONS

- Un `deploy_bundle` utilise `cmd-deploy_module_multi_machine` pour les opérations réelles.
- Il ne doit pas embarquer de logique SSH/SCP/tar parallèle.
- Il commence par `preflight`.
- Il passe par `plan --dry-run` avant `deploy` réel.
- Le `deploy` réel exige validation humaine.
- Le post-install et cleanup stale lock sont explicites, jamais implicites.

## 12_INVARIANTS

- Pas de bypass de `deploy_module_multi_machine`.
- Pas de déploiement sans preflight.
- Pas de déploiement réel sans validation humaine.
- Pas de cible Windows.
- Pas de secret dans le bundle.
- Pas de post-install implicite.
- Pas de cleanup stale lock implicite.
- Pas d'écriture registry sans GO séparé.

## 13_MANIFEST_EXTENSION

Champs obligatoires pour `deploy_bundle` :

```json
{
  "bundle_type": "deploy_bundle",
  "deploy_engine": "deploy_module_multi_machine",
  "deploy_engine_command": "cmd-deploy_module_multi_machine",
  "module_name": "<module>",
  "source_dir": "/opt/trading/modules/<module>",
  "target_machines": ["student", "db-layer"],
  "requires_preflight": true,
  "requires_dry_run": true,
  "requires_human_approval_for_real_deploy": true,
  "post_install_default": false,
  "cleanup_stale_lock_default": false
}
```

## 14_REQUIRED_PROMPTS

- `GO_PROMPT_01_PREFLIGHT.md`
- `GO_PROMPT_02_DEPLOY_DRY_RUN.md`
- `GO_PROMPT_03_DEPLOY_REAL.md`
- `GO_PROMPT_04_CLOSEOUT.md`

## 15_REQUIRED_CHECKLISTS

- `CHECKLIST_TARGETS.md`
- `CHECKLIST_PREFLIGHT.md`
- `CHECKLIST_DEPLOY.md`
- `CHECKLIST_ROLLBACK.md`

## 16_COMMANDS_REFERENCE

```bash
cmd-deploy_module_multi_machine status
```

```bash
cmd-deploy_module_multi_machine preflight --module-name <module> --source-dir /opt/trading/modules/<module> --targets <targets>
```

```bash
cmd-deploy_module_multi_machine plan --module-name <module> --source-dir /opt/trading/modules/<module> --targets <targets> --dry-run
```

```bash
cmd-deploy_module_multi_machine deploy --module-name <module> --source-dir /opt/trading/modules/<module> --targets <targets>
```

```bash
cmd-deploy_module_multi_machine sanity --module-name <module> --source-dir /opt/trading/modules/<module> --targets <targets>
```

## 17_ACCEPTANCE_CRITERIA

```text
BUNDLE_TYPE=deploy_bundle
DEPLOY_ENGINE=deploy_module_multi_machine
PREFLIGHT_PROMPT=PASS
DRY_RUN_PROMPT=PASS
REAL_DEPLOY_PROMPT_GATED=PASS
CLOSEOUT_PROMPT=PASS
TARGET_CHECKLIST=PASS
ROLLBACK_CHECKLIST=PASS
NO_SECRETS=PASS
NO_BYPASS=PASS
MANIFEST_EXTENDED=PASS
```

## 18_FAILURE_MODES

| Problème | Verdict | Correctif |
|---|---|---|
| script de déploiement parallèle | FAIL | utiliser `deploy_module_multi_machine` |
| pas de preflight | FAIL | ajouter prompt preflight |
| pas de dry-run | FAIL | ajouter prompt dry-run |
| deploy réel non gated | FAIL | ajouter validation humaine |
| pas de rollback checklist | PARTIAL | ajouter checklist rollback |
| targets flous | FAIL | fixer aliases ou user@host |

## 20_SELECTED_SOLUTION

Solution appliquée :

```text
La méthode d'implémentation des bundles reconnaît deploy_bundle comme type spécialisé pour piloter deploy_module_multi_machine.
```

## 17_RESUME_POINT

```text
GO_OPT_TRADING_BUNDLES_REPO_STORAGE_PARENT_01

Fichier:
docs/chantiers/GO_OPT_TRADING_BUNDLES_REPO_STORAGE_PARENT_01/04A_DEPLOY_BUNDLE_IMPLEMENTATION_ADDENDUM.md

État:
deploy_bundle validé et appliqué comme type de bundle.

Prochaine action:
créer le runbook d'utilisation réelle ou checkpoint parent.
```

## RISKS

- À qualifier.
