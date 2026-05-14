# MODEL_TASK_BOUNDARY_MATRIX_01

Matrice de correspondance modèle ↔ type de tâche.

## Légende

| Symbole | Signification |
|:-------:|---------------|
| ✅ | Usage validé |
| ⚠️ | Possible mais limité |
| ❌ | Non fonctionnel ou interdit |
| — | Non testé |

## Matrice

| Tâche | 0.5B | 1.5B | 3B | deepseek-r1:1.5b |
|-------|:----:|:----:|:--:|:----------------:|
| Smoke pipeline | ✅ | ✅ | ❌ | ❌ |
| Diagnostic session | ✅ | ✅ | ❌ | ❌ |
| Read-only simple | ✅ | ✅ | ❌ | ❌ |
| Reply exact | ❌ | ⚠️ | ❌ | ❌ |
| Format JSON/structuré | ❌ | ⚠️ | ❌ | ❌ |
| Multi-étapes (3-5) | ⚠️ | ⚠️ | ❌ | ❌ |
| Raisonnement | ❌ | ⚠️ | ⚠️ | ⚠️ |
| Trading / signal | ❌ | ❌ | ❌ | ❌ |
| Worker continu | ❌ | ❌ | ❌ | ❌ |

## Recommandations

- **Par défaut** : utiliser 0.5B pour toute tâche où la réponse exacte n'est pas critique
- **Si format exact exigé** : ne pas utiliser l'agent local, passer par un appel direct Ollama avec prompt contrôlé
- **Si raisonnement nécessaire** : envisager deepseek-r1:1.5b via direct Ollama (pas agent chain)
- **Si trading** : REFUS — ce runtime n'est pas dimensionné pour ça
