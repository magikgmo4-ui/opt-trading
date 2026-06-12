# git_fleet_guard — runbook V1 / V1.1

## But
Auditer l'état Git du parc avant toute remédiation.

## Préconditions
- accès SSH fonctionnel si audit distant
- repo présent sur les machines ciblées
- branche cible par défaut : `origin/sot/mainline`

## Audit standard
```bash
cmd-git_fleet_guard audit --machines admin-trading,student,db-layer
```

## Audit ciblé
```bash
cmd-git_fleet_guard audit --machines student,db-layer
```

## Lecture du dernier rapport
```bash
cmd-git_fleet_guard report --format md
```

## Interprétation
- `clean` : repo propre et synchronisé
- `review_required` : stash, divergence ou working tree sale
- `inaccessible` : machine ou repo non accessible

## Interdits V1
- pas de reset automatique
- pas de rebase automatique
- pas de stash automatique
- pas de push automatique

## Remediation guidee V1.1
```bash
cmd-git_fleet_guard remediate
```

## Remediation guidee ciblee
```bash
cmd-git_fleet_guard remediate --machine admin-trading
```

## Interdits V1.1
- pas de reset automatique
- pas de rebase automatique
- pas de stash automatique
- pas de push automatique
- pas de pull automatique
- pas de checkout automatique

## Sortie attendue V1.1
- diagnostic court
- niveau de risque
- commandes recommandees
- avertissements
- resultat attendu si l'operateur execute la remediaton

## RISKS

- À qualifier.
