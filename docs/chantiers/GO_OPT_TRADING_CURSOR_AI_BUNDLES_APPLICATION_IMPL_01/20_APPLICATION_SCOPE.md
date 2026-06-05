# 20_APPLICATION_SCOPE

## Perimetre application cursor-ai

### In scope

1. **Catalogue bundles cursor-ai** : Structure `bundles/` dans le repo
2. **Methode de creation bundle** : Re-utiliser la convention du CADRAGE parent
3. **Methode de recuperation bundle** : Procedure standardisee
4. **Point de reprise operateur** : Fiche de reprise bundle pour cursor-ai
5. **Bundles existants a recenser** :
   - `bundles/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_QUALIFICATION_01/`

### Out of scope

- Implementation runtime (scripts, daemon, service)
- Integration admin-trading
- Integration db-layer
- Creation de nouveaux bundles Ollama
- Activation de flux de production

## Structure bundles actuelle

```
bundles/
  GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_QUALIFICATION_01/
    README_BUNDLE.md
    bundle_meta/manifest.json
    checklists/CHECKLIST_EXECUTION.md
    prompts/GO_PROMPT_01_CADRAGE_CHILD.md
    prompts/GO_PROMPT_02_STUDENT_MACHINE_FACTS.md
    prompts/GO_PROMPT_03_OLLAMA_API_TESTS.md
    prompts/GO_PROMPT_04_OPENAI_COMPAT_OPENCLAW.md
    prompts/GO_PROMPT_05_RAG_READONLY_AND_GO_REPRISE.md
```

## Methode d'application Bundles cursor-ai

### Creation d'un bundle

1. Creer `bundles/<BUNDLE_NAME>/`
2. Ecrire `README_BUNDLE.md` (description, objectif, invariants)
3. Ecrire `bundle_meta/manifest.json` (schema, type, owner)
4. Ajouter `checklists/CHECKLIST_EXECUTION.md` (steps operationnels)
5. Ajouter `prompts/` (GO prompts pour IDE)
6. Optionnel : `scripts/` (scripts d'application, sans runtime live)

### Recuperation d'un bundle

1. Consulter `bundles/` dans le repo
2. Lire `README_BUNDLE.md` pour le contexte
3. Executer `CHECKLIST_EXECUTION.md` step by step
4. Utiliser `prompts/GO_PROMPT_*.md` dans l'IDE

### Conventions

- Machine owner = cursor-ai (sauf bundle specifique a une autre machine)
- Aucun secret, .env, token dans les bundles
- Aucun output live tracke
- Doc-only sauf scripts d'application sans runtime

## RISKS

- À qualifier.
