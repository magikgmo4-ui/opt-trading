---
doc_id: GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_OPENCLAW_CLI_LOCAL_DRYRUN_INVOCATION_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
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
  - local
source_kind: canonical
updated_at: 2026-05-14
---

# GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_OPENCLAW_CLI_LOCAL_DRYRUN_INVOCATION_01

## 1_MASTER_TARGET

Verifier la presence du CLI `openclaw` sur `fantome`, documenter le chemin d'installation si absent, et preparer l'invocation locale dry-run du builder agent.

## 2_STATE (entree)

```text
parent_go = PASS / MERGED (PR #411, 91258c7)
OpenClaw Builder = LOCAL_OPERATIONAL_RUNBOOK_COMPLETE
remote/SSH = BLOCKED
Gateway V2 = stable (documente)
CLI openclaw = ABSENT sur fantome
```

## 3_VERIFICATION_CLI

```yaml
check_path: ABSENT
check_command: ABSENT
check_type: ABSENT
check_pip: ABSENT
check_pipx: ABSENT
check_npm: ABSENT
check_binaires: ABSENT (/usr/local/bin, /usr/bin, ~/.local/bin)
conclusion: CLI openclaw non installe sur fantome
```

## 4_INFRASTRUCTURE_EXISTANTE

Les modules OpenClaw suivants existent dans le repo `opt-trading`:

| Module | Role | 
|--------|------|
| `openclaw_config_modulaire/` | Configuration des agents (orchestrateur, builder, reviewer, lab) |
| `gateway_openclaw/` | Scripts de gestion du gateway tmux (start, stop, logs) |
| `install_module_openclaw/` | Registre et script d'installation des modules vers `/opt/trading` |
| `doctor_openclaw/` | Diagnostics et verifications |
| `configure_openclaw/` | Application de configuration |
| `menu_openclaw/` | Menu interactif |
| `model_provider_openclaw/` | Configuration du provider de modele |
| `evidence_openclaw/` | Collecte de preuves |
| `tradingview_observer_openclaw/` | Observer TradingView |

### Configuration agents (agents.json5)

```json5
agents:
  - orchestrateur (default): gpt-5.4, tools minimal, peut spawner builder/reviewer/lab
  - builder: gpt-5.4, tools coding, deny runtime/browser/canvas/nodes/cron/gateway
  - reviewer: gpt-5.4, tools messaging, deny browser/canvas/nodes/cron/gateway
  - lab: gpt-5.4, tools coding, deny runtime/browser/canvas/nodes/cron/gateway
```

### Gateway tmux (gateway_env.sh)

```bash
TARGET_USER=openclaw
TARGET_HOME=/home/openclaw
SESSION=openclaw-gateway
LOG_DIR=/home/openclaw/.openclaw/logs
```

## 5_CHEMIN_D_INSTALLATION_DOCUMENTE

### 5.1 Installation du CLI openclaw (binaire principal)

Le binaire `openclaw` n'est pas present. Les modules du repo sont des scripts de configuration et de gestion qui dependent d'un binaire `openclaw` deja installe.

Chemins probables d'installation du binaire openclaw:

| Methode | Commande indicative | Risque |
|---------|---------------------|--------|
| npm global | `npm install -g openclaw` | WAN requis |
| Homebrew | `brew install openclaw` | WAN requis |
| Pre-built binary | Telechargement depuis releases GitHub | WAN requis |
| pip | `pip install openclaw` | WAN requis |
| Source (Go/Rust) | `git clone + build` | WAN + build requis |

### 5.2 Installation des modules locaux

Une fois le binaire `openclaw` installe, les modules du repo peuvent etre deployes:

```bash
cd /home/fantome/opt-trading/modules/install_module_openclaw
bash scripts/cmd.sh install gateway_openclaw
bash scripts/cmd.sh install openclaw_config_modulaire
# ... autres modules selon besoin
```

Le script `cmd.sh` copie les modules vers `/opt/trading` via sudo.

### 5.3 Demarrage du gateway

```bash
cd /opt/trading/modules/gateway_openclaw
bash scripts/start.sh   # Lance une session tmux openclaw-gateway
bash scripts/logs.sh     # Verifie les logs
```

## 6_BLOCKAGE

```text
STATUS: BLOCKED_AWAITING_CLI_INSTALL

L'installation du CLI openclaw est NECESSAIRE avant toute invocation builder.
Elle est BLOQUEE car :
- aucune commande d'installation n'a ete validee
- l'installation requiert probablement un acces WAN
- le choix de la methode d'installation n'est pas arrete
- l'approbation humaine explicite est requise

Prochaine etape : STOP. Attendre validation humaine pour :
1. choix de la methode d'installation
2. confirmation que le WAN necessaire est acceptable
3. execution de l'installation
4. verification que le CLI est fonctionnel
```

## 7_CONSTRAINTS_VERIFICATION

```text
[x] Aucun SSH reel
[x] Aucune commande remote
[x] Aucun secret
[x] Aucun patch runtime
[x] Aucun admin-trading
[x] Aucune installation automatique (respecte l'instruction : documenter sans executer)
[x] Read-only (verification CLI uniquement)
[x] Validation humaine requise avant toute installation
```

## 8_NEXT

Si validation humaine recue pour l'installation :
→ installer le CLI openclaw
→ invoquer `openclaw agent --agent builder --message "..." --dry-run`
→ produire le rapport d'invocation

Si BLOCKED :
→ closeout avec statut documente
→ le prochain GO pourra reprendre avec le CLI installe
