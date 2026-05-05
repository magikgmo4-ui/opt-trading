---
doc_id: GO_OPT_TRADING_BUNDLES_REPO_STORAGE_PARENT_01_CROSSCHECK_DEPLOY_MODULE_MULTI_MACHINE
doc_type: crosscheck
repo: opt-trading
project: opt-trading
module: bundles
go_id: GO_OPT_TRADING_BUNDLES_REPO_STORAGE_PARENT_01
status: draft
lifecycle_stage: crosscheck
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-04-24
topic_keys:
  - opt-trading
  - bundles
  - deploy_module_multi_machine
  - multi-machine
  - github
  - shared
  - tar-gz
  - ssh
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_BUNDLES_REPO_STORAGE_PARENT_01/05_CROSSCHECK_DEPLOY_MODULE_MULTI_MACHINE.md
point_de_reprise: "17_RESUME_POINT"
links:
  - docs/chantiers/GO_OPT_TRADING_BUNDLES_REPO_STORAGE_PARENT_01/01_BUNDLE_STORAGE_METHOD.md
  - docs/chantiers/GO_OPT_TRADING_BUNDLES_REPO_STORAGE_PARENT_01/02_BUNDLE_RETRIEVAL_METHOD.md
  - docs/chantiers/GO_OPT_TRADING_BUNDLES_REPO_STORAGE_PARENT_01/04_BUNDLE_IMPLEMENTATION_METHOD.md
  - deploy_module_multi_machine/README.md
  - docs/deploy_module_multi_machine_continuity.md
---

# 05_CROSSCHECK_DEPLOY_MODULE_MULTI_MACHINE

## 1_MASTER_TARGET

Recroiser la méthode des bundles GitHub avec `deploy_module_multi_machine` pour clarifier ce qui relève :

- du stockage durable GitHub ;
- du bundle IDE / documentation opérable ;
- du déploiement multi-machine runtime ;
- du transport `/shared` ou `tar.gz` ;
- de la reprise machine.

## 3_INITIAL_NEED

Demande utilisateur :

> Recroiser avec deploy_module_multi_machine

## 7_CANONICAL_STATE

État établi du module `deploy_module_multi_machine` d'après `deploy_module_multi_machine/README.md` :

- module d'orchestration infra pour déployer automatiquement un module vers plusieurs machines Linux via SSH ;
- orchestrateur principal : `admin-trading` ;
- registry possible : `registry/machines_registry.yaml` et `registry/modules_registry.yaml` ;
- packaging local d'un module en `tar.gz` ;
- copie distante via `scp` ;
- installation sous `/opt/trading/<module>` ;
- sanity check distant si détecté ;
- `preflight` disponible ;
- `deploy` disponible ;
- `sanity` disponible ;
- `--post-install` optionnel ;
- locks distants par `install_path` sous `/tmp/deploy_module_multi_machine_locks/` ;
- cleanup stale lock explicite ;
- cible POSIX/Linux seulement ;
- pas de déploiement Windows.

## 8_VALIDATED_PLAN

Le recroisement doit éviter une confusion :

```text
bundle IDE GitHub != module runtime déployé
bundle IDE GitHub != tar.gz temporaire deploy_module_multi_machine
bundle IDE GitHub peut cependant fournir les artefacts et prompts pour piloter un déploiement multi-machine
```

## 9_SELECTED_SOLUTION

Positionnement retenu :

```text
bundles/<GO_ID>/
  = support IDE / opérateur / prompts / checklists / scripts légers

deploy_module_multi_machine
  = outil runtime d'orchestration SSH pour modules Linux

/shared/bundles/<GO_ID>/
  = miroir de transport optionnel

/tmp/<module>_<run_id>.tar.gz
  = artefact temporaire généré par deploy_module_multi_machine
```

## 10_SELECTED_SETUP — architecture croisée

```text
GitHub repo opt-trading
├── bundles/<GO_ID>/
│   ├── README_BUNDLE.md
│   ├── prompts/
│   ├── checklists/
│   ├── scripts/
│   └── bundle_meta/manifest.json
│
├── docs/chantiers/<GO_ID>/
│   └── cadrage / décisions / closeout
│
└── deploy_module_multi_machine/
    ├── app/
    ├── scripts/
    └── config/

admin-trading
└── deploy_module_multi_machine
    -> preflight
    -> tar.gz temporaire
    -> scp
    -> install /opt/trading/<module>
    -> sanity distant
```

## 11_KEY_DECISIONS

- Les bundles GitHub ne remplacent pas `deploy_module_multi_machine`.
- `deploy_module_multi_machine` ne remplace pas les bundles IDE.
- Un bundle peut contenir des prompts/checklists/scripts pour piloter `deploy_module_multi_machine`.
- Les artefacts `tar.gz` générés par `deploy_module_multi_machine` restent temporaires, pas source canonique.
- Les modules runtime à déployer doivent rester sous leur surface module habituelle.
- Les bundles doivent pointer vers le GO et les commandes de déploiement, pas empaqueter silencieusement le runtime.

## 12_INVARIANTS

- Pas de secrets dans les bundles.
- Pas de déploiement réel sans preflight.
- Pas de cible Windows avec `deploy_module_multi_machine`.
- Pas de runtime patch caché dans un bundle IDE.
- Pas d'installation sur cible sans GO explicite.
- Pas de confusion entre `/shared` miroir et GitHub source.
- Pas de confusion entre `tar.gz` temporaire et bundle canonique.
- Pas de post-install distant sans décision explicite.

## 13_ESTABLISHED — relation fonctionnelle

### Bundle GitHub

Rôle :

- préparer l'opérateur ;
- fournir prompts ;
- fournir checklists ;
- fournir scripts de pilotage légers ;
- documenter les commandes ;
- pointer vers les sources canoniques ;
- permettre reprise IDE.

### deploy_module_multi_machine

Rôle :

- qualifier cibles avec `preflight` ;
- empaqueter module source en `tar.gz` ;
- uploader vers cibles ;
- installer sous `/opt/trading/<module>` ;
- lancer sanity ;
- gérer locks et collisions ;
- reporter statuts machine.

## 14_HYPOTHESIS

Hypothèse utile : un bundle de type `machine_bundle` peut servir de couche opérateur au-dessus de `deploy_module_multi_machine`.

Exemple :

```text
bundles/GO_DEPLOY_EXAMPLE_01/
├── prompts/GO_PROMPT_01_PREFLIGHT.md
├── prompts/GO_PROMPT_02_DEPLOY_DRY_RUN.md
├── prompts/GO_PROMPT_03_DEPLOY_REAL.md
├── checklists/CHECKLIST_PREFLIGHT.md
├── checklists/CHECKLIST_ROLLBACK.md
└── scripts/run_preflight.sh
```

Mais le déploiement réel reste effectué par `deploy_module_multi_machine`, pas par le bundle lui-même.

## 15_REMAINING_GAP

À décider plus tard :

- créer un template de bundle spécialisé `deploy_module_multi_machine` ;
- ajouter un type `deploy_bundle` dans la méthode ;
- créer un premier bundle réel pour déployer un module précis ;
- relier les résultats de preflight/deploy à un closeout de chantier ;
- décider si `/shared/bundles/` doit être miroir officiel.

## 16_TODO — ajustement méthode bundles

Ajouter à la méthode d'implémentation la classe :

```text
deploy_bundle
```

Définition :

```text
Bundle IDE/opérateur qui prépare et encadre un déploiement multi-machine, sans remplacer deploy_module_multi_machine.
```

Contenu recommandé :

- prompt preflight ;
- prompt deploy dry-run ;
- prompt deploy réel ;
- checklist cibles ;
- checklist rollback ;
- commandes `cmd-deploy_module_multi_machine` ;
- manifest avec `target_machines` ;
- sortie attendue par machine.

## 20_DEPLOY_BUNDLE_TEMPLATE

Structure proposée :

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

## 21_DEPLOY_COMMANDS_REFERENCE

Commandes issues du module existant à référencer dans les bundles :

```bash
cmd-deploy_module_multi_machine status
```

```bash
cmd-deploy_module_multi_machine preflight --module-name <module> --source-dir /opt/trading/modules/<module> --targets student,db-layer
```

```bash
cmd-deploy_module_multi_machine plan --module-name <module> --source-dir /opt/trading/modules/<module> --targets student,db-layer --dry-run
```

```bash
cmd-deploy_module_multi_machine deploy --module-name <module> --source-dir /opt/trading/modules/<module> --targets student,db-layer
```

```bash
cmd-deploy_module_multi_machine sanity --module-name <module> --source-dir /opt/trading/modules/<module> --targets student,db-layer
```

## 22_OUTPUT_SCHEMA_FOR_DEPLOY_BUNDLE

Sortie attendue par cible :

```json
{
  "target": "student",
  "stage": "preflight|plan|deploy|sanity|post_install|lock",
  "status": "ok|partial|blocked|failed|skipped",
  "run_id": "...",
  "install_path": "/opt/trading/<module>",
  "lock": {
    "exists": false,
    "stale": false,
    "owner_run_id": null
  },
  "sanity": "ok|failed|skipped",
  "next_action": "..."
}
```

## 23_MATRIX_ADDITION_REFINEMENT

La proposition matrice doit distinguer :

| Objet | Surface canonique | Rôle |
|---|---|---|
| bundle IDE | `bundles/<GO_ID>/` | artefacts opérateur/IDE |
| deploy bundle | `bundles/<GO_ID>/` | orchestration documentée d'un déploiement multi-machine |
| tar.gz runtime | `/tmp/<module>_<run_id>.tar.gz` | artefact temporaire de déploiement |
| module source | `modules/<module>/` ou surface module réelle | source runtime à déployer |
| module installé | `/opt/trading/<module>` sur cible | runtime distant |

## 24_ACCEPTANCE_CRITERIA

Un bundle croisé avec `deploy_module_multi_machine` est accepté si :

```text
DEPLOY_MODULE_REFERENCE=present
PREFLIGHT_PROMPT=present
DRY_RUN_PROMPT=present
DEPLOY_REAL_PROMPT=present_if_allowed
ROLLBACK_CHECKLIST=present
TARGETS_DECLARED=present
NO_SECRETS=pass
NO_DIRECT_SCP_SCRIPT_BYPASS=pass
DEPLOY_MODULE_MULTI_MACHINE_USED=pass
```

## 25_VERDICT

Verdict : `COMPATIBLE_WITH_SEPARATION`.

La méthode bundles et `deploy_module_multi_machine` sont compatibles si leurs rôles restent séparés :

- bundle = support opérateur/versionné ;
- deploy module = mécanisme runtime multi-machine ;
- tar.gz = temporaire ;
- GitHub = source durable ;
- `/shared` = miroir de transport possible.

## 17_RESUME_POINT

```text
GO_OPT_TRADING_BUNDLES_REPO_STORAGE_PARENT_01

Fichier:
docs/chantiers/GO_OPT_TRADING_BUNDLES_REPO_STORAGE_PARENT_01/05_CROSSCHECK_DEPLOY_MODULE_MULTI_MACHINE.md

État:
recroisement avec deploy_module_multi_machine documenté.

Décision:
les bundles peuvent encadrer deploy_module_multi_machine mais ne le remplacent pas.

Prochaine action:
mettre à jour la méthode ou checkpoint parent.
```
