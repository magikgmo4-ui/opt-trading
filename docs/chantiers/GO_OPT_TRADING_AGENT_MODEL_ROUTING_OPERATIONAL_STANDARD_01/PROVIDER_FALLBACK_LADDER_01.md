# PROVIDER_FALLBACK_LADDER_01

Échelle de fallback provider quand le choix initial échoue.

```text
Échelon 0 : qwen2.5:0.5b-instruct (agent chain)
  ↓ échoue (hallucination, timeout, format incorrect)
Échelon 1 : qwen2.5:1.5b-instruct (direct Ollama)
  ↓ échoue (timeout, format incorrect)
Échelon 2 : deepseek-r1:1.5b (direct Ollama, raisonnement)
  ↓ échoue
Échelon 3 : REFUS documenté
```

## Règles

1. Toujours commencer au plus bas échelon adapté à la tâche
2. Ne pas sauter d'échelon sans raison documentée
3. Chaque échelon doit produire une trace de décision
4. REFUS n'est pas un échec — c'est une décision de sécurité
5. Si un échelon supérieur réussit là où l'inférieur a échoué, documenter le gap de capacité

## Exemple

```yaml
# Tâche: "Liste des fichiers .md dans docs/"
# Classification: read-only, risque faible
# Choix initial: 0.5B agent chain
# Résultat: hallucination (structures inventées)
# Fallback: 1.5B direct
# Résultat fallback: réponse correcte
# Décision: 0.5B insuffisant pour cette tâche → routing ajusté
```
