---
doc_id: GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_OPENCLAW_CLI_LOCAL_DRYRUN_INVOCATION_01_REPORT
doc_type: discovery_report
repo: opt-trading
project: opt-trading
module: agents
go_id: GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_OPENCLAW_CLI_LOCAL_DRYRUN_INVOCATION_01
parent_go_id: GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_OPENCLAW_BUILDER_LOCAL_OPERATIONAL_RUNBOOK_01
machine: fantome
status: gated_pending_install
lifecycle_stage: cli_discovery
topic_keys:
  - openclaw
  - cli
  - dry-run
  - invocation
  - discovery
source_kind: canonical
updated_at: 2026-05-14
---

# OPENCLAW_CLI_LOCAL_DRYRUN_INVOCATION_REPORT_01

## 13_ESTABLISHED

Verification de presence du CLI `openclaw` sur `fantome` realisee le 2026-05-14.

Resultat : **CLI ABSENT**. Aucun binaire `openclaw` detecte dans le systeme.

## Verification exhaustive

| Source | Resultat |
|--------|----------|
| `which openclaw` | ABSENT |
| `command -v openclaw` | ABSENT |
| `type openclaw` | ABSENT |
| `pip list` | ABSENT |
| `pipx list` | ABSENT |
| `npm list -g` | ABSENT |
| `/usr/local/bin/openclaw*` | ABSENT |
| `/usr/bin/openclaw*` | ABSENT |
| `~/.local/bin/openclaw*` | ABSENT |

## Infrastructure OpenClaw existante

Le repo `opt-trading` contient **9 modules** OpenClaw complets avec scripts, configuration et documentation. L'architecture est prete pour une installation.

### Modules presents

| Module | Fichiers | Description |
|--------|----------|-------------|
| `openclaw_config_modulaire` | agents.json5, tools.json5, openclaw_root_template.json5, scripts | Configuration des 4 agents |
| `gateway_openclaw` | gateway_env.sh, start.sh, stop.sh, logs.sh, attach.sh | Gestion du gateway tmux |
| `install_module_openclaw` | modules_registry.json, cmd.sh, sanity.sh | Installation des modules |
| `doctor_openclaw` | RUNBOOK.txt, cmd.sh, sanity.sh | Diagnostics |
| `configure_openclaw` | - | Application de config |
| `menu_openclaw` | - | Menu interactif |
| `model_provider_openclaw` | - | Provider de modele |
| `evidence_openclaw` | - | Collecte de preuves |
| `tradingview_observer_openclaw` | - | Observer TradingView |

### Agents configures

```text
orchestrateur : gpt-5.4 | tools: minimal | peut spawner builder/reviewer/lab
builder       : gpt-5.4 | tools: coding | deny runtime/browser/canvas/nodes/cron/gateway
reviewer      : gpt-5.4 | tools: messaging | deny browser/canvas/nodes/cron/gateway
lab           : gpt-5.4 | tools: coding | deny runtime/browser/canvas/nodes/cron/gateway
```

### Gateway tmux

```text
TARGET_USER = openclaw
SESSION = openclaw-gateway
LOG_DIR = /home/openclaw/.openclaw/logs
```

## Analyse

L'infrastructure de configuration est complete et prete. Le seul composant manquant est le binaire `openclaw` lui-meme.

Le module `install_module_openclaw` gere le deploiement des modules vers `/opt/trading` mais ne gere pas l'installation du binaire principal.

## Chemin d'installation documente

### Option 1 : npm (si openclaw est un package npm)
```bash
# WAN requis
npm install -g openclaw
```

### Option 2 : pip (si openclaw est un package Python)
```bash
# WAN requis
pip install openclaw
```

### Option 3 : binaire pre-compile
```bash
# WAN requis pour le telechargement
# URL a determiner selon la source officielle OpenClaw
```

### Option 4 : build from source
```bash
# WAN + build chain requis
git clone <repo-openclaw>
cd openclaw
make build  # ou go build / cargo build
```

### Post-installation : deploiement des modules
```bash
cd /home/fantome/opt-trading/modules/install_module_openclaw
bash scripts/cmd.sh install gateway_openclaw
bash scripts/cmd.sh install openclaw_config_modulaire
```

## Premier dry-run planifie (post-installation)

Une fois le CLI installe, la commande dry-run planifiee est :

```bash
openclaw agent --agent builder \
  --message "Return a JSON object only with keys: status, role, constraints, next_step. status must be BUILDER_DRYRUN_OK. Do not run commands. Do not modify files. Do not use SSH. Do not call remote systems." \
  --json \
  --dry-run
```

Cette commande est conforme au runbook local (PR #411) et herite de toutes les contraintes de la chaine OpenClaw Builder.

## Verdict

```text
PASS_GATED

GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_OPENCLAW_CLI_LOCAL_DRYRUN_INVOCATION_01

CLI openclaw absent - documente.
Infrastructure de configuration prete.
Chemin d'installation documente.
Installation bloquee en attente de validation humaine.
Aucun SSH, remote, secret, ou write non planifie.
```
