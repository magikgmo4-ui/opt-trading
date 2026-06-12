# Dependances et suite

## Dependances retenues
- `GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03`
  - Necessaire avant les tests physiques multi-machines finaux.
  - Porte la consolidation transverse des alias, probes et chemins d'acces.
- `GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01`
  - Conserve le cadrage projet producteur/consommateur autour de `LocalCMS`.
  - Le realignment `db-layer` doit rester dans cette famille, pas dans le parent machine.
- `GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01`
  - Conserve le cadrage runtime `OpenClaw`.
  - Porte la clarification operationnelle du gateway, du port `18789` et du mode `tmux` / `OpenCode`.
- `GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01`
  - Reste ouvert pour la machine trading reelle.
  - Ne doit pas etre relance avant la clarification `db-layer` + `OpenClaw` + `reseau_ssh`.

## Ordre de reprise recommande depuis ce GO
1. `GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_DB_LAYER_REVIEW_01`
2. `GO_OPT_TRADING_UI_LOCALCMS_DB_LAYER_CONSUMER_REALIGNMENT_01`
3. `GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_CLOSEOUT_01`
4. `GO_OPT_TRADING_MACHINE_ADMIN_TRADING_RUNTIME_INTEGRATION_REVIEW_01`

## Justification courte
- Le principal gap operationnel observe ici est `OpenClaw` installe mais non actif sur `db-layer`.
- Le realignment `LocalCMS` reste important, mais il ne bloque pas autant que l'etat runtime `OpenClaw` constate en direct.
- Les validations physiques finales restent dependantes de `reseau_ssh`.
- `admin-trading` doit rester differe tant que la machine prioritaire actuelle n'est pas clarifiee.

## Next GO recommande
- `GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_DB_LAYER_REVIEW_01`

## RISKS

- À qualifier.
