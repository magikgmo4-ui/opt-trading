---
doc_id: BUNDLES_BUNDLE_TYPES_01
doc_type: bundle/bundle_types
repo: opt-trading
machine: cursor-ai
status: active
lifecycle_stage: workflow_active
links:
  - bundles/ACTIVE_WORKFLOW.md
  - bundles/CURSOR_AI_BUNDLES_REPRISE.md
---

# BUNDLE_TYPES — Types de bundles cursor-ai

## Types de bundles documentes

### 1. Reprise bundle

**Usage** : redemarrer un GO existant depuis son dernier checkpoint.

**Contenu minimal** :
- Fiche de reprise (REPRISE_TEMPLATE)
- Prompt de reprise standard
- Reference au dernier commit / PR merge

**Exemple** : `bundles/CURSOR_AI_BUNDLES_REPRISE.md`

### 2. Operator pack

**Usage** : packager des artefacts reutilisables en pack operateur standard.

**Contenu minimal** :
- README (survol, invariants)
- PROMPT_TEMPLATES (prompts standard)
- REPRISE_TEMPLATE (template de reprise)
- NO_COMMIT_RULES (regles de securite)

**Exemple** : `bundles/claude-artifacts/`

### 3. IDE handoff bundle

**Usage** : transmettre un bundle documentaire d'un IDE a un autre operateur.

**Contenu minimal** :
- BUNDLE_MANIFEST (manifeste et contexte)
- IDE_HANDOFF (instructions IDE)
- Prompts specifiques
- Regles de securite source

**Exemple** : `docs/chantiers/GO_LIVE_ARTIFACTS_CLAUDE_COWORK_IDE_BUNDLE_01/`

### 4. Prompt bundle

**Usage** : fournir des prompts prets a l'emploi pour un type de GO specifique.

**Contenu minimal** :
- PROMPT_TEMPLATES avec prompts GO standard
- Instructions d'usage

**Exemple** : `bundles/claude-artifacts/PROMPT_TEMPLATES.md`

### 5. PR merge bundle

**Usage** : standardiser l'ouverture et le merge de PR doc-only.

**Contenu minimal** :
- Template de PR
- Checklist de verification pre-merge
- Script de merge

### 6. Closeout bundle

**Usage** : standardiser le closeout d'un GO.

**Contenu minimal** :
- Template CLOSEOUT
- Checklist de verification post-merge
- Fiche de verdict

### 7. Admin-trading gate bundle

**Usage** : FUTURE SEULEMENT — spec de gate avant admin-trading.

**Statut** : non ouvert. Necessite demande explicite.

**Contenu minimal (futur)** :
- Spec de gate admin-trading
- Conditions d'ouverture
- Checklist de securite

## Mapping bundle / machine

| Bundle type | Machine autorisee | Statut |
| --- | --- | --- |
| Reprise bundle | cursor-ai, student, db-layer | ACTIF |
| Operator pack | cursor-ai | ACTIF |
| IDE handoff bundle | cursor-ai | ACTIF |
| Prompt bundle | cursor-ai | ACTIF |
| PR merge bundle | cursor-ai | ACTIF |
| Closeout bundle | cursor-ai | ACTIF |
| Admin-trading gate bundle | admin-trading (futur only) | FERME |

## Extension

De nouveaux types de bundle peuvent etre ajoutes si :
1. Ils sont doc-only.
2. Ils ne touchent pas au runtime.
3. Ils ne contiennent pas de secrets.
4. Ils sont documentes dans `bundles/BUNDLE_TYPES.md`.
