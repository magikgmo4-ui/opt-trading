# configure_openclaw

Facade operateur standardisee pour la configuration OpenClaw au niveau utilisateur.

## Role
- lancer la configuration OpenClaw
- valider la config courante
- lire / ecrire des chemins de configuration
- gerer les agents et l'identite de workspace
- ouvrir le dashboard OpenClaw

## Contenu
- `scripts/cmd.sh` : `status`, `validate`, `config-file`, `wizard`, `dashboard`, `agents-*`, `get`, `set`, `unset`
- `scripts/menu.sh`, `sanity.sh`, `install_shortcuts.sh`
- `docs/README.md`, `RUNBOOK.txt`, `ETABLI.txt`, `PROMPT_STANDARD.txt`

## Integration
- s'insere dans la chaine documentee par `menu_openclaw`
- s'appuie sur le binaire `openclaw` et la config utilisateur active

## Statut
- actif
- composant de configuration / post-install de la suite OpenClaw

## Notes de consolidation
- a lire avec `openclaw_config_modulaire` :
  - `openclaw_config_modulaire` gere la config modulaire et son apply/rollback
  - `configure_openclaw` sert de facade operateur sur la configuration live
