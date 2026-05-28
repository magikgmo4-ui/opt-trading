# 10_PILOT_SCOPE

## Périmètre du pilote

Le pilote couvre la boucle minimale :

```
GO_PROMPT (fichier local)
  → pilot_runner.py
    → lire prompt
    → générer run_id
    → valider handoff contract
    → vérifier stop conditions
    → écrire preuve JSON + Markdown
    → retourner verdict + exit code
```

## Ce qui est DANS le périmètre

- Lecture d'un fichier `GO_PROMPT` local.
- Génération d'un `run_id` unique par run.
- Validation du contrat (`handoff_contract.py`).
- Évaluation des stop conditions (`stop_conditions.py`).
- Écriture d'une preuve structurée dans `artifacts/automation_ops/semiauto_pilot/<run_id>/`.
- Exit code déterministe (0 / 2 / 3).

## Ce qui est HORS périmètre

- Merge automatique de PR.
- Appel à GitHub Actions.
- Appel à l'API trading (Bitget, etc.).
- Suppression de jobs ou de fichiers.
- Modification de `secrets/`.
- Mode autre que `dry_run`.

## Gate humain

Toute preuve contient `"human_gate_required": true`. L'opérateur doit valider manuellement avant tout `next_go`.
