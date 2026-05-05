---
doc_id: GO_OPT_TRADING_AI_TEAM_OBSERVER_DOC_DRAFT_01_DOC_DRAFT_SPEC
doc_type: spec
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_AI_TEAM_OBSERVER_DOC_DRAFT_01
status: open
lifecycle_stage: spec
surface: chantier
source_kind: canonical
updated_at: 2026-05-05
---

# 01_DOC_DRAFT_SPEC — Specification DOC_DRAFT

## Objectif

Transformer la sortie brute d'un worker Observer (READ_INVENTORY) en un brouillon documentaire structure, exploitable par un humain, au format Strict Workers.

## Format DOC_DRAFT

Un DOC_DRAFT est un fichier Markdown produit dans `modules/ai_team_mvp/drafts/` contenant les sections obligatoires suivantes :

```markdown
# DOC_DRAFT — <titre>

## 13_ESTABLISHED
(faits etablis, constats, donnees brutes de l'Observer)

## 14_HYPOTHESIS
(interpretations, hypotheses, pistes de lecture)

## 15_REMAINING_GAP
(ce qui manque, ce qui n'est pas couvert, risques)

## 16_TODO
(actions recommandees, prochaines etapes)

## VERDICT_DRAFT_ONLY
(statut explicite : document non valide, brouillon)
```

## Contraintes d'ecriture

- Ecriture uniquement dans `modules/ai_team_mvp/drafts/`.
- Refus d'ecrire ailleurs (erreur + arret).
- Nom de fichier : `<task_id>_<timestamp>.md`.
- Aucun ecrasement sans confirmation explicite.
- Contenu en Markdown, UTF-8.

## Contrat Strict Workers applique

```text
no_secrets: true
no_env_files: true
no_git_write_ops: true
no_runtime_write_by_default: true
requires_external_validation: true
output_status: DRAFT_ONLY
only_verified_models: true
write_target: modules/ai_team_mvp/drafts/   (seul dossier autorise)
```

## Flux de donnees

```
Observer READ_INVENTORY (stdout)
        |
        v
Task packet observer_doc_draft.json (input_source)
        |
        v
Runner (DOC_DRAFT mode)
        |
        v
modules/ai_team_mvp/drafts/<task_id>_<timestamp>.md
```

## Validation

| Critere | Methode |
|:--------|:--------|
| Fichier genere dans drafts/ | Verifier existence |
| Sections obligatoires presentes | Grep 13_ESTABLISHED..VERDICT_DRAFT_ONLY |
| Aucune ecriture hors drafts/ | git diff --stat |
| Aucun denied_input lu | Runner log |
| Aucun git write | git diff |
| 0 secret | Grep denied_inputs sur le draft |
