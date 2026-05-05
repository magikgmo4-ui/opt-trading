---
doc_id: GO_OPT_TRADING_AI_TEAM_PATCH_DRAFT_01_PATCH_DRAFT_CONTRACT
doc_type: spec
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_AI_TEAM_PATCH_DRAFT_01
status: open
lifecycle_stage: spec
surface: chantier
source_kind: canonical
updated_at: 2026-05-05
---

# 01_PATCH_DRAFT_CONTRACT — Contrat PATCH_DRAFT

## Definition

PATCH_DRAFT est une tache de l'Analyzer qui produit une **proposition de modification** sur un fichier cible. La proposition est un document Markdown au format diff-like, jamais applique automatiquement.

## Principe

```
Fichier cible (read-only)  →  Analyzer (PATCH_DRAFT)  →  Proposition (drafts/patches/)
                                     │
                               Gatekeeper HITL
                               (validation humaine
                                avant application)
```

## Contrat

### Ce que PATCH_DRAFT fait

1. Lit le fichier cible (read-only, verifie denied_inputs).
2. Genere une proposition de modification structuree.
3. Ecrit la proposition dans `drafts/patches/<task_id>_<ts>.md`.
4. Produit les sections Strict Workers obligatoires.

### Ce que PATCH_DRAFT ne fait JAMAIS

1. Modifier le fichier cible.
2. Executer `git diff`, `git apply`, `git add`, `git commit`.
3. Ecrire hors de `drafts/patches/`.
4. Appliquer le patch automatiquement.
5. Lire ou ecrire des fichiers correspondant aux denied_inputs.

## Format de sortie

```markdown
# PATCH_DRAFT — <titre>

**Worker**: analyzer
**Task**: <task_id>
**Target**: <fichier cible>

## 13_ESTABLISHED
(contenu actuel du fichier, sections concernees)

## 14_HYPOTHESIS
(pourquoi ce changement, quel impact attendu)

## 15_REMAINING_GAP
(ce que le patch ne couvre pas, risques)

## 16_TODO
(actions pour appliquer le patch manuellement)

## PATCH_PROPOSAL
```diff
--- a/<fichier>
+++ b/<fichier>
@@ -ligne,offset +ligne,offset @@
-ligne originale
+ligne proposee
```

## VERDICT_DRAFT_ONLY
PROPOSITION — ne pas appliquer sans validation humaine.
```

## Garde-fous

| Garde-fou | Implementation |
|-----------|----------------|
| Verifier denied_inputs sur la cible | `safe_read_file()` avec patterns |
| Refuser les fichiers hors repo | `os.path.abspath` doit etre sous REPO_ROOT |
| Ecriture uniquement dans patches/ | `write_target` check |
| Pas de git | `denied_commands` dans le contrat |
| DRAFT_ONLY | `output_status` obligatoire |

## Cible du smoke

Fichier cible pour le smoke : `modules/ai_team_mvp/README.md`

Justification : fichier non sensible, sous versionnement, petit, modifiable sans risque. La proposition sera d'ajouter une section documentant PATCH_DRAFT dans le README.
