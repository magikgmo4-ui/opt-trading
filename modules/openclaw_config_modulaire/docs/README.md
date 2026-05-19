# openclaw_config_modulaire

Module durable pour gérer une config OpenClaw modulaire avec le même standard que les autres modules du projet.

## Objectif
- sortir des gros collages dans le terminal ;
- garder un `openclaw.json` racine court ;
- déplacer `agents` et `tools` dans `~/.openclaw/config.d/` ;
- fournir `sanity`, `cmd`, `menu`, `apply_safe`, `rollback`, `install_shortcuts`.

## Flux standard
1. `sanity.sh`
2. `cmd.sh backup`
3. `cmd.sh apply`
4. `cmd.sh validate`
5. redémarrer le gateway
6. `cmd.sh probe`
7. rollback si nécessaire

## Points de sécurité
- le token gateway est récupéré depuis la config live et réinjecté dans le template ;
- un backup daté est créé avant toute installation ;
- si `openclaw config validate` échoue, le module peut restaurer le dernier backup ;
- aucune élévation n’est activée.

## Fichiers gérés
- `~/.openclaw/openclaw.json`
- `~/.openclaw/config.d/agents.json5`
- `~/.openclaw/config.d/tools.json5`

## Commandes rapides
- `cmd-openclaw_config_modulaire status`
- `cmd-openclaw_config_modulaire apply`
- `cmd-openclaw_config_modulaire validate`
- `cmd-openclaw_config_modulaire probe`
- `cmd-openclaw_config_modulaire rollback`
