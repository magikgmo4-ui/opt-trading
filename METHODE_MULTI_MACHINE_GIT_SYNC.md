# Methode Multi-Machine Git Sync

## Objectif

Eviter les conflits recurrents lies aux divergences local/remote et au travail simultane multi-machine.

## Regle centrale

Une branche active = une seule machine writer a la fois.

## Protocole d'entree obligatoire avant toute modification

1. git fetch --prune
2. verifier la branche courante
3. verifier que le worktree est propre ou que l'etat sale est asume explicitement
4. verifier ahead/behind vs origin
5. si behind > 0 : git pull --rebase obligatoire avant edition
6. si ahead > 0 et travail non publie : ne pas changer de machine avant arbitrage

## Protocole de sortie obligatoire avant changement de machine

1. committer ce qui doit l'etre
2. git push si la branche doit rester transferable
3. sinon stash explicite + note de reprise
4. documenter machine owner, etat de sync, dernier point etabli, prochaine action

## Interdictions

- pas de travail en ecriture sur la meme branche depuis deux machines
- pas de git pull merge implicite
- pas de force push brut
- pas de reprise sur une machine secondaire sans fetch + verification ahead/behind

## Travail parallele

Si parallelisme reel requis, ouvrir une branche dediee par GO ou par lot, pas plusieurs machines sur la meme branche.

## Politique de publication

- branche partagee ou transferable => push avant changement de machine
- branche locale temporaire => rester sur la meme machine tant que non publiee

## Reecriture d'historique

Autorisee seulement sur branche personnelle avec git push --force-with-lease apres verification explicite.