# TASK_TO_MODEL_CAPABILITY_MATRIX_01

Matrice de correspondance type de tâche → modèle/provider recommandé.

## Matrice

| Type de tâche | Modèle recommandé | Pipeline | Fallback |
|---------------|-------------------|:--------:|----------|
| Smoke pipeline | 0.5B agent chain | ✅ | — |
| Diagnostic session | 0.5B agent chain | ✅ | 1.5B direct |
| Read-only non structuré | 0.5B agent chain | ✅ | 1.5B direct |
| Read-only format libre | 0.5B agent chain | ✅ | — |
| Résumé court | 0.5B agent chain | ⚠️ lent | 1.5B direct |
| Classification simple | 0.5B agent chain | ⚠️ non fiable | 1.5B direct |
| Format exact (JSON, CSV) | 1.5B direct Ollama | ❌ | REFUS |
| Raisonnement multi-étapes | 1.5B direct Ollama | ❌ | REFUS |
| Décision sans supervision | PROVIDER DISTANT | ❌ | REFUS |
| Trading ou signal | — | ❌ | REFUS |
| Worker continu | — | ❌ | REFUS |

## Légende

| Symbole | Signification |
|:-------:|---------------|
| ✅ | Usage validé |
| ⚠️ | Possible mais limité |
| ❌ | Non fonctionnel ou interdit |

## Note

La colonne "Pipeline" indique si le modèle est compatible avec la chaîne `openclaw agent` complète (avec tools). Les modèles marqués ❌ nécessitent un appel direct Ollama (`/api/chat` ou `/api/generate`).
