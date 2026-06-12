# OpenClaw sur db-layer

## Relation db-layer <-> OpenClaw
- `db-layer` est confirme comme hote actuel de `OpenClaw`.
- Le parent runtime reste `GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01`.
- Ce GO ne requalifie pas `db-layer` en parent runtime `OpenClaw`.

## Etat verifie
- Binaire present sur `db-layer` : `/usr/local/bin/openclaw`.
- Home runtime present : `/home/openclaw/.openclaw`.
- Module repo present : `/opt/trading/modules/menu_openclaw`.
- Configuration runtime lue par le module gateway : `/home/openclaw/.openclaw/openclaw.json`.
- Point de boucle locale attendu par le gateway : `ws://127.0.0.1:18789`.

## Constat runtime au moment du controle
- Controle en lecture seule via `modules/gateway_openclaw/scripts/cmd.sh status`.
- `SESSION_STATUS=stopped`.
- Boucle locale `127.0.0.1:18789` non joignable au moment du controle.
- `OpenClaw` est donc confirme comme installe sur `db-layer`, mais pas actif sur ce point de controle.

## Frontiere avec admin-trading
- `admin-trading` reste la machine trading reelle future.
- Les surfaces `bot_vision`, `deskpro`, `webhook`, `collectors` et runtime trading ne sont pas ouvertes ici.
- L'integration `admin-trading` doit revenir apres clarification `db-layer` + `OpenClaw` + `reseau_ssh`.

## Gaps et checks suivants
- Cause du `SESSION_STATUS=stopped` non analysee dans ce GO.
- Etat detaille `tmux` / logs / relance non traite ici.
- Une revue runtime dediee `OpenClaw` sur `db-layer` reste necessaire.

## RISKS

- À qualifier.
