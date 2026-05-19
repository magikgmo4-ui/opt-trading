# SURFACE_TO_PROVIDER_USAGE_MATRIX_01

Matrice surface → provider autorisé selon standard.

| Surface | Providers disponibles | Usage validé | Gate requise |
|---------|---------------------|:------------:|:------------:|
| Student/Ollama local | 0.5B agent chain, 1.5B direct, deepseek direct | ✅ | ✅ |
| Distant (SSH) | À configurer | ⏳ | ✅ |
| Distant (API) | À configurer | ⏳ | ✅ |
| GPU local | À configurer | ⏳ | ✅ |

## Règle

- Toute surface doit avoir au moins un provider validé avant usage agent
- Toute surface doit appliquer la gate capacité/fallback
- Toute surface doit produire une trace de routage
- Student/Ollama sert de baseline de référence pour les nouvelles surfaces
