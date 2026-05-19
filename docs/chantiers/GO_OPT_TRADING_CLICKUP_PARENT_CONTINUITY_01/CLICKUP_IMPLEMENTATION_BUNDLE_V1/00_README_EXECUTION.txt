CLICKUP_IMPLEMENTATION_BUNDLE_V1

OBJECTIF
Implémenter ClickUp comme cockpit de pilotage opt-trading.

MODE
Manuel contrôlé V1, automatisable ensuite.

PRINCIPE
ClickUp reflète le repo. ClickUp ne remplace ni GitHub, ni docs/, ni GO_INDEX, ni REPRISE, ni BRANCH_STATE.

ORDRE D'EXECUTION
1. Créer workspace OPT-TRADING OPS.
2. Créer spaces.
3. Créer statuts.
4. Créer champs personnalisés.
5. Créer template GO_TASK_TEMPLATE.
6. Importer 3 à 5 GO actifs maximum.
7. Valider que chaque tâche a une preuve repo.
8. Créer dashboards.
9. Documenter le résultat dans le chantier.

REGLE D'ARRET
Si un GO n'a pas de doc_path ou preuve repo, ne pas le marquer PASS dans ClickUp.
