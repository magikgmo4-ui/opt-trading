# Dependances et differes

## Dependances stabilisees
- `GO_OPT_TRADING_MACHINE_DB_LAYER_PARENT_01`
  - `db-layer` reste la machine prioritaire actuelle.
- `GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01`
  - le parent runtime reste ouvert et structurant.
- `GO_OPENCLAW_STATE_DIR_REPAIR_10`
  - le repair local a fourni la correction owner-session necessaire.

## Elements differes
- `admin-trading`
  - reste la machine trading reelle future
  - hors scope de ce closeout
- `GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01`
  - non active
  - aucun dossier local prouve sur cette ligne
  - a considerer plus tard seulement
- `reseau_ssh`
  - non bloquant pour les controles read-only de ce cycle
  - reste transverse pour les validations physiques multi-machines plus larges

## Risques restants
- le parent runtime global `GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01` reste ouvert au sens gouvernance et outillage plus large
- la version live `2026.3.11` reste differente d'une preuve historique plus ancienne `2026.4.2`
- le `state_dir` reste un point de vigilance documentaire, mais sans symptome bloquant dans l'etat final retenu

## Prochain GO recommande
- `GO_OPT_TRADING_UI_LOCALCMS_DB_LAYER_CONSUMER_REALIGNMENT_01`

## Justification
- Le cycle borne `OpenClaw/db-layer` est suffisamment clarifie et stabilise localement.
- `admin-trading` ne doit pas etre rouvert maintenant.
- `LocalCMS` redevient le prochain sujet logique sur `db-layer`.

## RISKS

- À qualifier.
