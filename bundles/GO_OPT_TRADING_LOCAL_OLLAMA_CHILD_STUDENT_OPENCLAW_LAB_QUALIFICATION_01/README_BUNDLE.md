# Bundle IDE — GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_QUALIFICATION_01

## Objet

Qualifier Ollama sur une machine lab/student et préparer OpenClaw comme orchestrateur potentiel.

Ce bundle est le premier bundle réel ancré selon la méthode `bundles/<GO_ID>/`.

## GO servi

```text
GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_QUALIFICATION_01
```

## Parent de contexte

```text
GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01
```

## Branche de stockage du bundle

```text
go/GO_OPT_TRADING_BUNDLES_REPO_STORAGE_PARENT_01
```

## Sources canoniques

- `docs/chantiers/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01/07_LAB_USAGE_SCOPE.md`
- `docs/chantiers/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01/03_SECURITY_BASELINE.md`
- `docs/chantiers/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01/02_MACHINE_QUALIFICATION_PLAN.md`
- `docs/index/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01_INDEX_ENTRY.md`
- `docs/index/BRANCH_STATE.md`
- `docs/chantiers/GO_OPT_TRADING_BUNDLES_REPO_STORAGE_PARENT_01/04A_DEPLOY_BUNDLE_IMPLEMENTATION_ADDENDUM.md`
- `docs/chantiers/GO_OPT_TRADING_BUNDLES_REPO_STORAGE_PARENT_01/06_REAL_USE_RUNBOOK_DEPLOY_BUNDLE.md`

## Contraintes

- machine unique lab/student ;
- localhost d'abord ;
- lab only ;
- pas `admin-trading` server ;
- pas exposition publique ;
- pas shell libre ;
- pas trading live ;
- pas écriture repo automatique ;
- OpenClaw à qualifier comme orchestrateur, pas activé en production.

## Ordre d'exécution

1. `prompts/GO_PROMPT_01_CADRAGE_CHILD.md`
2. `prompts/GO_PROMPT_02_STUDENT_MACHINE_FACTS.md`
3. `prompts/GO_PROMPT_03_OLLAMA_API_TESTS.md`
4. `prompts/GO_PROMPT_04_OPENAI_COMPAT_OPENCLAW.md`
5. `prompts/GO_PROMPT_05_RAG_READONLY_AND_GO_REPRISE.md`
6. `checklists/CHECKLIST_EXECUTION.md`

## Entrypoints

- `README_BUNDLE.md`
- `prompts/GO_PROMPT_01_CADRAGE_CHILD.md`
- `checklists/CHECKLIST_EXECUTION.md`
- `bundle_meta/manifest.json`

## Sortie attendue

- machine facts ;
- Ollama facts ;
- OpenClaw facts ;
- tests P0/P1 ;
- verdict `READY / LIMITED / LAB_ONLY / REJECT` par usage ;
- prochain GO logique.

## Stop conditions

Stop immédiat si :

- exposition publique détectée ;
- cible différente de lab/student ;
- demande de trading live ;
- demande de shell libre ;
- demande d'écriture repo automatique ;
- OpenClaw exige outils élevés non contrôlés.

## Journalisation

Journaliser les résultats dans le sous-GO à créer :

```text
docs/chantiers/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_QUALIFICATION_01/
```

## Point de reprise

```text
GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_QUALIFICATION_01

Bundle:
bundles/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_QUALIFICATION_01/

Première action:
ouvrir le sous-GO de qualification lab/student.
```
