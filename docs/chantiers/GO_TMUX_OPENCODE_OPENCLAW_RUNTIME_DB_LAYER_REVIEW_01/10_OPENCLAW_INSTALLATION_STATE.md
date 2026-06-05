# Installation OpenClaw sur db-layer

## Etat etabli avant ce GO
- `OpenClaw` etait deja documente comme runtime local de reference sur `db-layer`.
- `GO_OPENCLAW_SYNC_02` portait une preuve historique `gateway OK` sur `ws://127.0.0.1:18789`.
- `GO_OPT_TRADING_MACHINE_DB_LAYER_PARENT_REVIEW_01` a ensuite etabli que le gateway etait arrete au moment du controle precedent.

## Etat verifie dans ce GO
- Acces SSH lecture seule disponible sur `db-layer`.
- Hote confirme : `db-layer`.
- Utilisateur de session distante confirme : `ghost`.
- Alias SSH resolu localement vers `ghost@192.168.0.100`.
- Binaire `OpenClaw` present : `/usr/local/bin/openclaw`.
- Version lue via `openclaw --version` : `OpenClaw 2026.3.11 (29dc654)`.
- Repertoire runtime confirme sous l'utilisateur `openclaw` : `~/.openclaw`.
- Fichier de configuration present : `~/.openclaw/openclaw.json`.
- Repertoires confirmes :
  - `~/.openclaw/workspace-orchestrateur`
  - `~/.openclaw/canvas`
  - `~/.openclaw/agents`
  - `~/.openclaw/logs`
- State dir secondaire de vigilance confirme : `/home/ghost/.openclaw`.

## Commandes read-only executees
- `ssh db-layer 'hostname; whoami; pwd'`
- `ssh db-layer 'command -v openclaw || true; openclaw --version || true'`
- `ssh -G db-layer | Select-String '^hostname |^user '`
- `ssh db-layer "sudo -iu openclaw bash -lc 'command -v tmux || true; command -v opencode || true; test -f ~/.openclaw/openclaw.json && echo CONFIG_PRESENT; ls -la ~/.openclaw 2>/dev/null || true; ls -la ~/.openclaw/logs 2>/dev/null || true'"`
- `ssh db-layer "sudo -iu openclaw bash -lc 'test -d ~/.openclaw/workspace-orchestrateur && echo WORKSPACE_ORCHESTRATEUR_PRESENT; test -d ~/.openclaw/canvas && echo CANVAS_DIR_PRESENT; test -d ~/.openclaw/agents && echo AGENTS_DIR_PRESENT'"`
- `ssh db-layer 'test -d /home/ghost/.openclaw && echo GHOST_STATE_DIR_PRESENT || true'`

## Points de lecture retenus
- `tmux` est bien present dans le PATH de l'utilisateur `openclaw` : `/usr/bin/tmux`.
- Aucun binaire `opencode` n'a ete observe dans le PATH de `openclaw` pendant cette passe.
- La documentation historique `GO_OPENCLAW_SYNC_02` consignait la version `2026.4.2`, alors que l'etat live relu ici expose `2026.3.11`.
- Le log gateway du `2026-04-22` est coherent avec `current v2026.3.11`, ce qui confirme au minimum un decalage entre preuve historique et etat runtime courant.

## Gaps
- Aucun secret ni contenu complet de `openclaw.json` n'a ete expose dans ce GO.
- La materialisation locale des sous-GO `GO_TMUX_RUNTIME_CONVENTIONS_01`, `GO_OPENCLAW_COMMAND_SCOPE_01`, `GO_TMUX_RUNTIME_CONTRACT_01`, `GO_TMUX_OPENCODE_OPENCLAW_MODES_01` et `GO_RUNTIME_GUARDRAILS_01` n'a pas ete prouvee sous forme de dossiers `docs/chantiers/`.
- `GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01` n'est pas materialise localement et reste seulement une reference differee.

## RISKS

- À qualifier.
