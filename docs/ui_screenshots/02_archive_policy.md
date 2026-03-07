# UI Screenshots — Archive Policy (proposée)

## Problème
Le cleanup quotidien peut éliminer trop vite des captures utiles si elles restent mélangées avec les artefacts de routine.

## Politique cible

### Tier 1 — Working / Daily
Captures temporaires et artefacts opérationnels de courte durée.
Exemples :
- snapshots fréquents
- captures intermédiaires
- artefacts de runs non sélectionnés

### Tier 2 — Archive / Memory
Captures conservées avec analyse associée.
Exemples :
- screenshot sélectionné + analyse synthèse
- screenshot d’un setup important
- screenshot de revue historique utile
- screenshot retenu pour apprentissage / comparaison

## Règle de conservation
Une capture ne doit entrer dans **Archive / Memory** que si au moins un des éléments suivants existe :
- analyse associée
- annotation / résumé
- lien vers une session/run
- utilité démontrée pour revue future

## Direction UI
La future UI `screenshots_analyses_passees` doit lire prioritairement la zone Archive / Memory, pas la zone Daily brute.
