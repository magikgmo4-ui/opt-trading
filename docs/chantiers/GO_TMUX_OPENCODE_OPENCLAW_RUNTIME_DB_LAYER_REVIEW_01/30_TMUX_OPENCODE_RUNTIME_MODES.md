# Modes runtime connus

## Role documentaire de reference
- Le parent `GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01` fixe la separation suivante :
  - `tmux` = persistance
  - `OpenCode` = production
  - `OpenClaw` = orchestration
  - `Telegram` = interface distante
- Ce parent reste un cadrage runtime et ne doit pas etre absorbe dans le parent machine `db-layer`.

## Mode `tmux`
- Le module `gateway_openclaw` documente un pilotage via `tmux` quand `systemd --user` n'est pas disponible.
- Session attendue : `openclaw-gateway`.
- Binaire `tmux` prouve sur `db-layer` : `/usr/bin/tmux`.
- Au moment du controle, aucune session `tmux` visible n'a ete relevee pour `openclaw`.

## Mode `OpenClaw gateway`
- Le module `gateway_openclaw` porte les surfaces `sanity`, `status`, `start`, `logs`, `attach`, `stop`, `health`, `probe`, `paths`.
- Le backend documente reste `openclaw gateway run`.
- Le gateway est concu pour tourner sous l'utilisateur `openclaw`.
- L'etat runtime relu ici est `stopped`, avec loopback non joignable.

## Mode `OpenCode`
- `OpenCode` reste present comme role dans le parent runtime.
- Aucun executable `opencode` n'a ete prouve dans le PATH de `openclaw` pendant cette revue.
- Ce GO ne conclut donc pas a une absence globale de `OpenCode`, seulement a l'absence de preuve live comme commande distincte dans ce contexte.

## Dashboard / canvas / browser
- La baseline `GO_OPENCLAW_INFRA_BASELINE_01` garde `gateway / dashboard / websocket` en loopback.
- La meme baseline fixe `browser.enabled = false`.
- Le log `gateway_foreground.log` montre un canvas local monte historiquement sur `http://127.0.0.1:18789/__openclaw__/canvas/`.
- Le repertoire `~/.openclaw/canvas` est present.
- Le dashboard/canvas n'est pas re-prouve comme actif maintenant, puisque le gateway est arrete au moment de cette passe.

## Relation avec la doc existante
- Les runbooks modules `menu_openclaw`, `gateway_openclaw`, `doctor_openclaw`, `configure_openclaw` et `evidence_openclaw` portent l'operatoire reel le plus utile pour `db-layer`.
- Les sous-GO `GO_TMUX_RUNTIME_CONVENTIONS_01`, `GO_OPENCLAW_COMMAND_SCOPE_01`, `GO_TMUX_RUNTIME_CONTRACT_01`, `GO_TMUX_OPENCODE_OPENCLAW_MODES_01` et `GO_RUNTIME_GUARDRAILS_01` restent references dans l'index et le parent runtime, mais ne sont pas materialises localement sous `docs/chantiers/` sur cette ligne.
- `GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01` n'est pas actif ici ; il reste a considerer plus tard, apres clarification runtime locale.

## Limites
- Aucun mode headless supplementaire n'a ete relance ou verifie au-dela des logs existants.
- Aucun token, secret ou contenu de configuration sensible n'a ete expose.

## RISKS

- À qualifier.
