---
doc_id: GO_OPT_TRADING_AI_TEAM_MVP_V2_ORCHESTRATOR_ANALYZER_01_CHAIN_CONTRACT
doc_type: spec
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_AI_TEAM_MVP_V2_ORCHESTRATOR_ANALYZER_01
status: open
lifecycle_stage: spec
surface: chantier
source_kind: canonical
updated_at: 2026-05-05
---

# 02_CHAIN_CONTRACT — Contrat de chaîne Orchestrator

## Définition

Une chaîne Orchestrator est une séquence ordonnée de sous-tâches, exécutée par le runner en mode `ORCHESTRATOR_CHAIN`. Chaque sous-tâche :
- Est un task packet JSON valide (compatible Strict Workers)
- Produit une sortie dans `modules/ai_team_mvp/drafts/`
- La sortie est lisible par la sous-tâche suivante

## Règles

1. **Arrêt au premier échec** : si une sous-tâche retourne un code != 0, la chaîne s'arrête immédiatement.
2. **Pas de git write** : aucune sous-tâche ne peut faire d'opération Git.
3. **Sortie en drafts/** : toutes les sorties intermédiaires et finales sont dans `drafts/`.
4. **Validation humaine** : la sortie finale est DRAFT_ONLY, jamais auto-validée.
5. **Idempotence partielle** : relancer la chaîne écrase les sorties intermédiaires (overwrite autorisé pour la chaîne).

## Chaîne v2

```
Step 1: READ_INVENTORY (observer)
  Input : docs/chantiers/ + docs/index/GO_INDEX.md
  Output: stdout + modules/ai_team_mvp/drafts/.observer_output_last.txt

Step 2: ANALYZE_INVENTORY (analyzer)
  Input : modules/ai_team_mvp/drafts/.observer_output_last.txt
  Output: modules/ai_team_mvp/drafts/analyze_inventory_01_<ts>.md

Step 3: DOC_DRAFT (documenter)
  Input : modules/ai_team_mvp/drafts/.observer_output_last.txt
  Output: modules/ai_team_mvp/drafts/documenter_draft_synthesis_01_<ts>.md
```

## Contrat de données entre étapes

| Étape | Sortie clé | Consommée par |
|:------|:-----------|:--------------|
| READ_INVENTORY | Liste des chantiers, fichiers, denied count | ANALYZE_INVENTORY, DOC_DRAFT |
| ANALYZE_INVENTORY | Classification, stats, patterns, recommendations | DOC_DRAFT (optionnel) |
| DOC_DRAFT | Brouillon final structuré | Gatekeeper (humain) |

## Validation de chaîne

| Critère | Méthode |
|:--------|:--------|
| Chaîne complète exécutée sans erreur | Vérifier exit codes des 3 étapes |
| Tous les fichiers intermédiaires produits | Vérifier existence dans drafts/ |
| Aucun git write | git diff --stat |
| Aucun denied_input | Logs de chaque étape |
| Aucune écriture hors drafts/ | git diff --stat |
