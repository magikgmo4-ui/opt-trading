# TERMUX IMPLEMENTATION GUIDE

## ROLE
Termux is the Android execution shell. It must stay an operator client, not a trading runtime.

## INSTALL BASELINE
Use a maintained Termux source. Avoid deprecated Play Store packages when possible.

```bash
pkg update
pkg upgrade
pkg install openssh tmux git nano jq coreutils
```

## DIRECTORY MODEL
```txt
~/.termux/tasker/          # scripts callable by Tasker
~/operator/                # local operator scripts and notes
~/.ssh/                    # SSH keys and config
```

## PASTE-SAFE SETUP
```bash
set -Eeuo pipefail
mkdir -p ~/.termux/tasker ~/operator ~/.ssh
chmod 700 ~/.termux ~/.termux/tasker ~/.ssh
pkg install -y openssh tmux git jq
```

## SSH READINESS CHECK
```bash
ssh -V
ls -ld ~/.ssh
```

## TMUX READINESS CHECK
```bash
tmux -V
tmux ls || true
```

## ANDROID CONSTRAINTS
- Battery optimization may kill Termux sessions.
- Background execution may require opening Termux once after reboot.
- Notifications must stay enabled for reliable long-running foreground sessions.

## PASS CRITERIA
- `ssh -V` works.
- `tmux -V` works.
- `~/.termux/tasker` exists with mode 700.
- A non-destructive SSH command can reach `db-layer` or `admin-trading`.

## FAIL CONDITIONS
- Android kills Termux during test.
- SSH keys are missing or world-readable.
- Tasker cannot invoke Termux commands.
