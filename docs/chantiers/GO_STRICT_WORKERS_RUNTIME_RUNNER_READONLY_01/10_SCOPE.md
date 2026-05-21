---
doc_id: GO_STRICT_WORKERS_RUNTIME_RUNNER_READONLY_01_SCOPE
doc_type: scope
go_id: GO_STRICT_WORKERS_RUNTIME_RUNNER_READONLY_01
parent_go: GO_OPT_TRADING_OPENCLAW_PARENT_AUTOMATION_GAPS_CLOSE_01
status: open
lifecycle_stage: impl
---

# 10_SCOPE — livrables et steps

## Steps

1. Créer runner read-only isolé (`scripts/ai/workers/runner_readonly.sh` ou équivalent Python)
2. Valider input schema job packet → rejeter tout packet invalide
3. Bloquer mutations par défaut (no-write guard)
4. Ajouter mode `--dry-run` pour audit sans effet
5. Ajouter sortie JSON normalisée par job
6. Ajouter logs par job (fichier ou ledger léger)
7. Ajouter test fixture read-only
8. Exécuter smoke réel
9. Documenter preuve

## Critères de succès

- Un job packet valide produit une sortie JSON sans modifier le repo ni le runtime
- Un job packet invalide est rejeté avec erreur structurée
- Aucune commande write n'est exécutable via le runner
- Le smoke peut être rejoué à l'identique

## Preuve attendue

- Smoke réussi avec artefacts
- Logs de job produits
- Aucune mutation détectée après run
