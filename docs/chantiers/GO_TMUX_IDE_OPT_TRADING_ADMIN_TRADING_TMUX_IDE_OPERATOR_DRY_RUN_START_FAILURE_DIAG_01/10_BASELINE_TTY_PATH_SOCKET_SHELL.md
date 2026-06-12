# 10_BASELINE_TTY_PATH_SOCKET_SHELL

## 1_MASTER_TARGET

Capturer le baseline distant TTY, PATH, socket, shell, config tmux et versions, sans mutation durable.

## 2_COMMAND_SCOPE

Commande distante executee dans :

```text
admin-trading:/opt/trading
```

Sans :

- `apt install`
- `npm install -g`
- upgrade `tmux`
- upgrade `tmux-ide`
- `tmux kill-server`
- creation de `ide.yml` durable
- mutation Git

## 3_BASELINE_OUTPUT

```text
hostname=admin-trading
kernel=Linux admin-trading 6.1.0-44-amd64 Debian 6.1.164-1 x86_64
uid=1000(ghost)
pwd=/opt/trading
USER=ghost
SHELL=/bin/bash
PATH=/usr/local/bin:/usr/bin:/bin:/usr/games
TERM=xterm-256color
SSH_TTY=/dev/pts/0
TMUX=
TMUX_TMPDIR=
STTY_SIZE=0 0
tty=/dev/pts/0
STDIN_TTY=YES
STDOUT_TTY=YES
```

Node stdout dimensions in the same SSH/TTY context:

```json
{"columns":0,"rows":0,"isTTY":true}
```

Interpretation:

```text
TTY_PRESENT=YES
STDOUT_IS_TTY=YES
STDOUT_COLUMNS=0
STDOUT_ROWS=0
```

## 4_BINARIES_AND_VERSIONS

```text
tmux=/usr/bin/tmux
node=/usr/bin/node
npm=/usr/bin/npm
npx=/usr/bin/npx
timeout=/usr/bin/timeout
bash=/usr/bin/bash
sh=/usr/bin/sh
tmux 3.3a
node v18.20.4
npm 9.2.0
npx 9.2.0
```

Interpretation :

- Debian 12 / Bookworm est coherent avec `tmux 3.3a` ;
- les prerequis declares par `tmux-ide@1.3.1` sont satisfaits ;
- `tmux` est resolu par PATH dans `/usr/bin/tmux`.

## 5_TMUX_CONFIGS

Configs recherchees :

```text
/etc/tmux.conf: absent
/home/ghost/.tmux.conf: absent
/home/ghost/.config/tmux/tmux.conf: absent
```

Interpretation :

```text
USER_TMUX_CONFIG_NOT_ROOT_CAUSE=YES
SYSTEM_TMUX_CONFIG_NOT_ROOT_CAUSE=YES
```

## 6_SOCKET_BASELINE

```text
/tmp exists
/tmp/tmux-1000 exists
tmux ls: no server running on /tmp/tmux-1000/default
tmux -L opt-trading-diag-baseline-01 ls: No such file or directory before test
```

Interpretation :

- aucun serveur tmux global actif n'a ete observe sur le socket par defaut ;
- le socket dedie `opt-trading-diag-baseline-01` etait absent avant test ;
- aucun cleanup global n'a ete requis.

## 7_SUPPORT_DOC_ALIGNMENT

La doc support `TMUX_IDE_DEB12_OPERATOR_SUPPORT_DIAG_01` indiquait que la version tmux n'etait pas l'hypothese principale. Les probes confirment ce point :

```text
TMUX_VERSION_OK=YES
NODE_VERSION_OK=YES
PATH_OK=YES
TTY_PRESENT=YES
TTY_SIZE_ZERO=YES
TMUX_CONFIG_ABSENT=YES
```

## 17_RESUME_POINT

```text
REPRISE:
Baseline confirme TTY presente mais stdout dimensions 0x0.
PATH et configs tmux ne sont pas la cause principale.

NEXT:
Lire 20_TMUX_MINIMAL_ISOLATED_PROBES.md.
```

## RISKS

- À qualifier.
