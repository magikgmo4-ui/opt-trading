# openclaw_config_modulaire

Gestion modulaire de la configuration OpenClaw avec apply safe, validation et rollback.

## Role
- garder un `openclaw.json` racine court
- externaliser `agents` et `tools` dans `~/.openclaw/config.d/`
- sauvegarder avant application
- valider puis permettre un rollback si necessaire

## Contenu
- `app/openclaw_root_template.json5`, `agents.json5`, `tools.json5`
- `scripts/cmd.sh` : `status`, `backup`, `apply`, `validate`, `health`, `probe`, `rollback`, `paths`
- `scripts/apply_safe.sh`, `rollback.sh`, `sanity.sh`, `install_shortcuts.sh`
- `docs/README.md`

## Fichiers geres
- `~/.openclaw/openclaw.json`
- `~/.openclaw/config.d/agents.json5`
- `~/.openclaw/config.d/tools.json5`

## Integration
- peut etre deploye par `install_module_openclaw`
- s'articule avec `gateway_openclaw` pour le redemarrage et les probes apres apply

## Statut
- actif
- composant de configuration structurelle de la suite OpenClaw

## Notes de consolidation
- ce module porte la config modulaire et la securite d'application
- ne pas le reduire a une simple facade `configure_openclaw`
