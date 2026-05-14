# ROUTING_STANDARD_ADOPTION_ACROSS_SURFACES_01

Adoption du standard opératoire de routage modèle/provider comme règle transversale.

## Surfaces concernées

| Surface | Applique le standard | Provider autorisé | Gate obligatoire |
|---------|:-------------------:|-------------------|:----------------:|
| Student/Ollama local | ✅ Baseline validée | 0.5B/1.5B/deepseek | ✅ |
| Machine distante (SSH) | ⏳ À configurer | Selon provider dispo | ✅ |
| Provider distant API | ⏳ À configurer | Selon contrat | ✅ |
| GPU local | ⏳ À configurer | Modèles plus forts | ✅ |

## Règle transversale

Toute exécution agent, sur toute surface, DOIT :

1. Classifier la tâche (type + risque + format)
2. Appliquer la matrice de routage
3. Produire une trace de décision
4. Exécuter avec session fraîche
5. Documenter le fallback si échec
6. Vérifier l'absence de trade/worker non autorisé

## Étendue

- Le standard s'applique à toute surface où `openclaw agent` est utilisé
- Le standard ne dépend pas du provider choisi (local ou distant)
- Le standard protège contre l'usage abusif du 0.5B comme décisionnel fiable
- Le standard interdit formellement le trading/worker sans GO dédié

## Limites connues de l'adoption

- Provider distant : pas encore configuré → REFUS pour tâche nécessitant format exact
- GPU local : pas encore disponible → modèles lourds non viables
- Machine distante : à valider séparément
