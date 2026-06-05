# 30_DRY_RUN_RESULTS

## 1_MASTER_TARGET

Documenter les resultats observes du dry-run operateur `tmux-ide`.

## 2_PRECHECK_RESULT

```text
PRECHECK_REPO_START
/opt/trading
REMOTE_GIT_STATE=behind 44 with preexisting modified/untracked files
PRECHECK_REPO_END
PRE_IDE_YML_ABSENT=YES
PRE_SESSION_ABSENT=YES
TEMP_IDE_YML_CREATED=/opt/trading/ide.yml
```

## 3_VALIDATE_RESULT

Commande :

```bash
npx -y tmux-ide@1.3.1 validate --json
```

Sortie :

```json
{
  "valid": true,
  "errors": []
}
```

Verdict :

```text
VALIDATE_PASS
```

## 4_START_RESULT

Commande :

```bash
timeout 12s npx -y tmux-ide@1.3.1
```

Sortie utile :

```text
tmux command failed
SESSION_PRESENT_AFTER_START=NO
START_EXIT=1
```

Interpretation :

- le fichier temporaire `ide.yml` etait valide statiquement ;
- le lancement interactif a echoue avant creation de session ;
- le timeout n'est pas la cause observee, car `START_EXIT=1` et non `124` ;
- aucune session `opt-trading-admin-trading` n'a ete observee apres le lancement.

## 5_STATUS_INSPECT_STOP_RESULT

Les commandes suivantes n'ont pas ete atteintes dans le chemin nominal :

```bash
npx -y tmux-ide@1.3.1 status --json
npx -y tmux-ide@1.3.1 inspect --json
npx -y tmux-ide@1.3.1 stop
```

Raison :

```text
START_EXIT=1
SESSION_PRESENT_AFTER_START=NO
```

## 6_CLEANUP_RESULT

Checks post-run executes :

```bash
ssh admin-trading "cd /opt/trading && test ! -e ide.yml && echo POST_IDE_YML_ABSENT=YES"
ssh admin-trading "! tmux has-session -t opt-trading-admin-trading >/dev/null 2>&1 && echo POST_SESSION_ABSENT=YES"
ssh admin-trading "test ! -e /tmp/tmux_ide_operator_dry_run_01.sh && echo POST_TEMP_SCRIPT_ABSENT=YES"
```

Resultats :

```text
POST_IDE_YML_ABSENT=YES
POST_SESSION_ABSENT=YES
POST_TEMP_SCRIPT_ABSENT=YES
```

## 7_ADDITIONAL_SANITY

Check read-only execute apres cleanup :

```bash
ssh admin-trading "tmux -V && cd /opt/trading && npx -y tmux-ide@1.3.1 validate --json"
```

Sorties :

```text
tmux 3.3a
```

```json
{
  "error": "Cannot read ide.yml: ENOENT: no such file or directory, open '/opt/trading/ide.yml'",
  "code": "READ_ERROR"
}
```

Interpretation :

- `tmux` est present ;
- le `READ_ERROR` post-cleanup confirme qu'aucun `ide.yml` actif ne reste ;
- ce check n'est pas utilise comme validation du dry-run, seulement comme sanity apres cleanup.

## 8_RESULT_SUMMARY

| Element | Etat |
| --- | --- |
| prechecks bloquants | PASS |
| `ide.yml` temporaire | cree puis supprime |
| `validate --json` | PASS |
| lancement session | FAIL |
| start exit | `1` |
| message start | `tmux command failed` |
| session apres start | absente |
| status/inspect | non atteints |
| stop nominal | non atteint |
| cleanup | PASS |
| installation globale | non effectuee |
| mutation Git distante | non effectuee |
| workflow applicatif | non lance |

## 18_VERDICT

```text
BLOCKED_START_TMUX_COMMAND_FAILED
```

## RISKS

- À qualifier.
