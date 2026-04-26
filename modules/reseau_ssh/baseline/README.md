# reseau_ssh baseline

Sous-ensemble baseline interne du module canonique `reseau_ssh`.

Ce dossier conserve les artefacts utiles issus de l'ancien `step1b` :
- bloc `hosts`
- configuration SSH Linux/Windows
- helper Windows `cursor-ai`
- inventaire baseline minimal

Les commandes publiées passent par [modules/reseau_ssh/scripts/cmd.sh](/C:/Users/ghost/opt-trading/modules/reseau_ssh/scripts/cmd.sh) :
- `baseline-dry-run`
- `baseline-apply`
- `baseline-hostname`
- `baseline-sanity`
- `baseline-show-hosts`
- `baseline-show-ssh`

Ce dossier n'est plus un module séparé.

## Target
1 module canonique par famille.
