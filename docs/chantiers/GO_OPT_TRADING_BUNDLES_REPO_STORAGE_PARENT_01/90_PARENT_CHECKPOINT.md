---
doc_id: GO_OPT_TRADING_BUNDLES_REPO_STORAGE_PARENT_01_PARENT_CHECKPOINT
doc_type: parent_checkpoint
repo: opt-trading
project: opt-trading
module: bundles
go_id: GO_OPT_TRADING_BUNDLES_REPO_STORAGE_PARENT_01
status: paused
lifecycle_stage: parent_checkpoint
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-04-24
topic_keys:
  - opt-trading
  - bundles
  - github
  - ide
  - deploy_bundle
  - ollama
  - branch-reprise
  - checkpoint
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_BUNDLES_REPO_STORAGE_PARENT_01/90_PARENT_CHECKPOINT.md
point_de_reprise: "17_RESUME_POINT"
links:
  - docs/chantiers/GO_OPT_TRADING_BUNDLES_REPO_STORAGE_PARENT_01/00_PARENT_CADRAGE.md
  - docs/chantiers/GO_OPT_TRADING_BUNDLES_REPO_STORAGE_PARENT_01/01_BUNDLE_STORAGE_METHOD.md
  - docs/chantiers/GO_OPT_TRADING_BUNDLES_REPO_STORAGE_PARENT_01/02_BUNDLE_RETRIEVAL_METHOD.md
  - docs/chantiers/GO_OPT_TRADING_BUNDLES_REPO_STORAGE_PARENT_01/03_MATRIX_ADDITION_PROPOSAL.md
  - docs/chantiers/GO_OPT_TRADING_BUNDLES_REPO_STORAGE_PARENT_01/04_BUNDLE_IMPLEMENTATION_METHOD.md
  - docs/chantiers/GO_OPT_TRADING_BUNDLES_REPO_STORAGE_PARENT_01/04A_DEPLOY_BUNDLE_IMPLEMENTATION_ADDENDUM.md
  - docs/chantiers/GO_OPT_TRADING_BUNDLES_REPO_STORAGE_PARENT_01/05_CROSSCHECK_DEPLOY_MODULE_MULTI_MACHINE.md
  - docs/chantiers/GO_OPT_TRADING_BUNDLES_REPO_STORAGE_PARENT_01/06_REAL_USE_RUNBOOK_DEPLOY_BUNDLE.md
  - bundles/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_QUALIFICATION_01/README_BUNDLE.md
  - bundles/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_QUALIFICATION_01/bundle_meta/manifest.json
  - docs/index/GO_OPT_TRADING_BUNDLES_REPO_STORAGE_PARENT_01_INDEX_ENTRY.md
---

# 90_PARENT_CHECKPOINT — GO_OPT_TRADING_BUNDLES_REPO_STORAGE_PARENT_01

## 1_MASTER_TARGET

Checkpoint de pause du chantier parent dédié à la méthode de stockage, récupération et implémentation des bundles IDE dans GitHub.

Ce checkpoint trace explicitement les deux branches distinctes :

- branche bundles : chantier courant de méthode bundles ;
- branche Ollama : chantier séparé à reprendre plus tard.

## 3_INITIAL_NEED

Séparer le sujet bundles du chantier Ollama, créer un parent dédié, documenter la méthode durable, puis ancrer le premier bundle réel demandé pour Ollama/OpenClaw lab.

Correction utilisateur à intégrer :

```text
Et la branche ollama surtout
Les 2
```

## 7_CANONICAL_STATE

### Branche 1 — bundles

```text
GO:
GO_OPT_TRADING_BUNDLES_REPO_STORAGE_PARENT_01

Branche:
go/GO_OPT_TRADING_BUNDLES_REPO_STORAGE_PARENT_01

Rôle:
chantier parent bundles / méthode GitHub / récupération / implémentation / deploy_bundle

Statut:
paused, branche ouverte
```

### Branche 2 — Ollama

```text
GO:
GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01

Branche:
go/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01

Rôle:
chantier parent Ollama local / lab student / OpenClaw orchestrateur potentiel

Statut:
paused, branche ouverte, à reprendre plus tard
```

### Premier bundle réel

```text
Bundle:
bundles/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_QUALIFICATION_01/

Statut:
READY_AS_FIRST_REAL_BUNDLE_NOT_EXECUTED

Dernier commit connu du bundle:
44e24e9be51490dfbf80f990b9008bf52f054e37
```

## 11_KEY_DECISIONS

- GitHub devient la source durable privilégiée pour les bundles IDE.
- Les bundles durables sont stockés décompressés sous `bundles/<GO_ID>/`.
- Le ZIP reste un artefact secondaire de transport.
- `/shared` peut servir de miroir machine, mais pas de source canonique.
- Google Drive peut servir à la lecture humaine, mais pas de source canonique IDE.
- `deploy_bundle` est un type reconnu.
- `deploy_bundle` encadre `deploy_module_multi_machine` sans le remplacer.
- Le premier bundle réel est celui d'Ollama/OpenClaw lab.
- La branche Ollama reste distincte de la branche bundles.
- Les deux branches restent ouvertes.

## 12_INVARIANTS

- Ne pas mélanger le parent bundles avec le parent Ollama.
- Ne pas fermer la branche Ollama depuis le chantier bundles.
- Ne pas fermer la branche bundles sans décision explicite.
- Pas de secrets dans les bundles.
- Pas de bundle sans README.
- Pas de bundle sans manifest.
- Pas de ZIP comme seule source durable.
- Pas de runtime patch dans ce parent.
- Pas de déploiement réel dans ce parent.
- Pas de bypass de `deploy_module_multi_machine` pour les `deploy_bundle`.
- Pas de deploy réel sans preflight, dry-run et validation humaine.

## 13_ESTABLISHED

### Documents du chantier bundles

- `00_PARENT_CADRAGE.md`
- `01_BUNDLE_STORAGE_METHOD.md`
- `02_BUNDLE_RETRIEVAL_METHOD.md`
- `03_MATRIX_ADDITION_PROPOSAL.md`
- `04_BUNDLE_IMPLEMENTATION_METHOD.md`
- `04A_DEPLOY_BUNDLE_IMPLEMENTATION_ADDENDUM.md`
- `05_CROSSCHECK_DEPLOY_MODULE_MULTI_MACHINE.md`
- `06_REAL_USE_RUNBOOK_DEPLOY_BUNDLE.md`
- `90_PARENT_CHECKPOINT.md`

### Premier bundle réel

```text
bundles/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_QUALIFICATION_01/
├── README_BUNDLE.md
├── prompts/
│   ├── GO_PROMPT_01_CADRAGE_CHILD.md
│   ├── GO_PROMPT_02_STUDENT_MACHINE_FACTS.md
│   ├── GO_PROMPT_03_OLLAMA_API_TESTS.md
│   ├── GO_PROMPT_04_OPENAI_COMPAT_OPENCLAW.md
│   └── GO_PROMPT_05_RAG_READONLY_AND_GO_REPRISE.md
├── checklists/
│   └── CHECKLIST_EXECUTION.md
└── bundle_meta/
    └── manifest.json
```

### Branche Ollama à reprendre

```text
Branche:
go/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01

Checkpoint connu:
docs/chantiers/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01/90_PARENT_CHECKPOINT.md

Index connu:
docs/index/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01_INDEX_ENTRY.md
```

## 14_HYPOTHESIS

À valider plus tard :

- ancrage direct de la méthode bundles dans `MATRICE_DOC_OPS_MASTER_MATRIX_01.md` ;
- création de templates réutilisables de bundles ;
- miroir `/shared/bundles/` ;
- premier test réel d'utilisation du bundle Ollama/OpenClaw ;
- reprise de la branche Ollama avec le bundle comme support d'exécution.

## 15_REMAINING_GAP

- La proposition matrice est documentée mais pas appliquée dans la matrice maîtresse.
- Le premier bundle réel est ancré mais pas encore exécuté.
- Aucun sous-GO de qualification Ollama/OpenClaw n'a encore été exécuté via ce bundle.
- Aucun template générique `deploy_bundle` n'a encore été créé sous `bundles/_templates/`.
- Les deux branches restent ouvertes : bundles et Ollama.

## 16_TODO

Prochaines actions possibles :

1. reprendre la branche Ollama : `go/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01` ;
2. utiliser le bundle pour ouvrir/exécuter `GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_QUALIFICATION_01` ;
3. créer un sous-GO pour appliquer la proposition bundles à la matrice maîtresse ;
4. créer un template générique `deploy_bundle` ;
5. créer un miroir `/shared/bundles/` si nécessaire ;
6. décider plus tard du sort des deux branches.

## 17_RESUME_POINT

```text
POINT DE REPRISE GLOBAL

Branche bundles:
go/GO_OPT_TRADING_BUNDLES_REPO_STORAGE_PARENT_01

État bundles:
chantier parent bundles ouvert
méthode GitHub documentée
méthode de récupération documentée
méthode d’implémentation documentée
deploy_bundle validé
recroisement deploy_module_multi_machine documenté
runbook d’utilisation réelle documenté
premier bundle réel ancré
checkpoint parent posé

Branche Ollama:
go/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01

État Ollama:
chantier parent Ollama local ouvert
lab/student + OpenClaw documentés
checkpoint posé
indexation minimale corrigée
à reprendre plus tard

Premier bundle réel:
bundles/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_QUALIFICATION_01/

Statut du bundle:
READY_AS_FIRST_REAL_BUNDLE_NOT_EXECUTED

Ce qui est prouvé:
- bundle présent dans GitHub
- structure README / prompts / checklist / manifest présente
- méthode bundles validée par un premier cas réel
- pas de runtime touché
- pas de test machine exécuté
- les deux branches restent ouvertes et distinctes

Ce qui reste:
- proposition matrice non appliquée à la matrice maîtresse
- bundle non exécuté
- sous-GO Ollama/OpenClaw non encore ouvert/exécuté depuis ce bundle

Reprise opérationnelle Ollama:
1. checkout `go/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01`
2. lire `docs/chantiers/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01/90_PARENT_CHECKPOINT.md`
3. ouvrir le bundle dans la branche bundles ou le récupérer par Git
4. exécuter `bundles/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_QUALIFICATION_01/prompts/GO_PROMPT_01_CADRAGE_CHILD.md`
```

## 18_TO_DOCUMENT

- patch matrice si validation ;
- template générique bundles ;
- éventuel miroir `/shared/bundles/` ;
- closeout d'exécution du premier bundle réel ;
- décision ultérieure sur les deux branches ouvertes.

## 19_TO_REMEMBER

Memory candidate :

```text
Les bundles IDE durables dans opt-trading doivent être stockés décompressés sous bundles/<GO_ID>/ avec README, manifest, prompts/checklists/scripts séparés. Le ZIP est secondaire. Les deploy_bundle encadrent deploy_module_multi_machine sans le remplacer. Si un bundle sert un autre chantier, tracer explicitement les deux branches de reprise.
```
