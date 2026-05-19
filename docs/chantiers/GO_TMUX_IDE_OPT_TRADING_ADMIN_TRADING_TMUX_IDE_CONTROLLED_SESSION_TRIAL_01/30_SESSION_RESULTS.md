# 30_SESSION_RESULTS

## 1_MASTER_TARGET

Documenter les resultats de la session controlee `tmux-ide`.

## 7_CANONICAL_STATE

Execution :

```text
admin-trading:/opt/trading
```

Session cible :

```text
opt-trading-admin-trading
```

## 8_VALIDATE_RESULT

Validation du `ide.yml` temporaire :

```json
{
  "valid": true,
  "errors": []
}
```

Sortie :

```text
VALIDATE_EXIT=0
```

## 9_START_RESULT

Lancement :

```text
timeout 12s npx -y tmux-ide@1.3.1
```

Sortie utile :

```text
Starting "opt-trading-admin-trading" (2 rows, 3 panes)...
[terminated]
START_EXIT=124
SESSION_PRESENT_AFTER_START=YES
```

Interpretation :

- `START_EXIT=124` vient du timeout applique au client TUI interactif ;
- la session a bien ete creee ;
- le timeout a borne l'attache, pas la creation de session.

## 10_TMUX_LIST_RESULT

```text
opt-trading-admin-trading: 1 windows (created Sun May 17 16:00:16 2026)
```

## 11_STATUS_RESULT

`tmux-ide status --json` a confirme :

```json
{
  "session": "opt-trading-admin-trading",
  "running": true,
  "configExists": true,
  "panes": [
    {
      "index": 0,
      "title": "Shell",
      "width": 39,
      "height": 19,
      "active": true
    },
    {
      "index": 1,
      "title": "Git",
      "width": 40,
      "height": 19,
      "active": false
    },
    {
      "index": 2,
      "title": "Docs",
      "width": 80,
      "height": 1,
      "active": false
    }
  ]
}
```

## 12_INSPECT_RESULT

`tmux-ide inspect --json` a confirme :

```text
valid=true
errors=[]
session=opt-trading-admin-trading
rows=2
panes=3
focus=rows.0.panes.0
tmux.running=true
```

Panes inspectees :

| Index | Title | Command | Active |
| --- | --- | --- | --- |
| 0 | `Shell` | `pwd` | true |
| 1 | `Git` | `git status --short --branch` | false |
| 2 | `Docs` | `ls docs/chantiers/GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_IDE_YML_MINIMAL_CONFIG_01` | false |

## 13_STOP_RESULT

Fermeture :

```text
Stopped session "opt-trading-admin-trading"
STOP_EXIT=0
SESSION_PRESENT_AFTER_STOP=NO
```

Cleanup :

```text
TEMP_IDE_YML_REMOVED=/opt/trading/ide.yml
POST_IDE_YML_ABSENT
POST_SESSION_ABSENT
```

## 14_FINAL_REMOTE_STATE

Apres cleanup, le repo distant conserve ses deltas preexistants, mais aucun `ide.yml` actif ne reste et aucune session cible ne reste ouverte.

## 18_VERDICT

```text
PASS_CONTROLLED_SESSION
```
