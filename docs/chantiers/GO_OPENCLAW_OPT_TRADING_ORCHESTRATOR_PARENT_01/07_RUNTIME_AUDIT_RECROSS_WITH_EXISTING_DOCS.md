---
doc_id: GO_OPENCLAW_RUNTIME_AUDIT_RECROSS_EXISTING_DOCS_20260426
doc_type: audit_recross
repo: opt-trading
project: opt-trading
module: openclaw_operator_bridge
go_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_AUDIT_RUNTIME_01
parent_go_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01
status: correction
lifecycle_stage: audit_recross
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-04-26
topic_keys:
  - openclaw
  - db-layer
  - gateway
  - recross
  - state_dir
  - openclaw_user
  - ghost_user
search_tags:
  - surface:chantier
  - doc_role:audit_recross
  - parent:GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01
  - audit:db_layer
  - correction:user_context
  - runtime:gateway_existing_docs
reference_canonique_principale: modules/evidence_openclaw/docs/GO_OPENCLAW_SYNC_02.md
point_de_reprise: "17_RESUME_POINT"
links:
  - modules/evidence_openclaw/docs/GO_OPENCLAW_SYNC_02.md
  - modules/menu_openclaw/docs/GO_OPENCLAW_INFRA_BASELINE_01.md
  - docs/chantiers/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01/06_RUNTIME_AUDIT_DB_LAYER_RESULT_20260426.md
---

# 07_RUNTIME_AUDIT_RECROSS_WITH_EXISTING_DOCS

## 1_MASTER_TARGET

Corriger la lecture du premier audit `db-layer` en la recroisant avec les documents OpenClaw déjà présents dans le repo.

## 7_CANONICAL_STATE

Le premier audit a été exécuté sous :

```text
user=ghost
host=db-layer
```

Les documents existants indiquent que le runtime documentaire de référence est :

```text
user=openclaw
host=db-layer
workspace=/home/openclaw/.openclaw/workspace-orchestrateur
gateway=ws://127.0.0.1:18789
version_app=2026.4.2
```

## 13_ESTABLISHED

### Depuis `GO_OPENCLAW_SYNC_02`

- utilisateur de référence : `openclaw`
- hôte : `db-layer`
- workspace : `/home/openclaw/.openclaw/workspace-orchestrateur`
- configuration valide : `~/.openclaw/openclaw.json`
- 5 agents : `orchestrateur`, `builder`, `reviewer`, `lab`, `codexoauth`
- gateway loopback : `ws://127.0.0.1:18789` notée `OK`
- adresse `db-layer` : `192.168.0.100`
- version applicative : `2026.4.2`
- vigilance : double state dir avec `/home/ghost/.openclaw`

### Depuis `GO_OPENCLAW_INFRA_BASELINE_01`

- `db-layer` est l'hôte canonique OpenClaw.
- Gateway/dashboard/websocket doivent rester en loopback.
- Port attendu : `18789`.
- Bind attendu : `127.0.0.1`.
- State dir `/home/ghost/.openclaw` est un point de vigilance.
- La suite doit partir d'un read-only machine-sourcé.

## CORRECTION DU VERDICT PRECEDENT

Le verdict `PASS_WITH_FIXES_REQUIRED` du fichier `06_RUNTIME_AUDIT_DB_LAYER_RESULT_20260426.md` reste valide uniquement pour le contexte :

```text
ghost@db-layer
```

Il ne prouve pas que le gateway canonique `openclaw@db-layer` est absent.

## VERDICT RECADRE

```text
PARTIAL_AUDIT_WRONG_USER_CONTEXT
```

Le bon prochain audit doit être exécuté dans le contexte `openclaw@db-layer` ou avec lecture explicite des process/services appartenant à l'utilisateur `openclaw`.

## 14_HYPOTHESIS

- Le gateway existe probablement dans le contexte `openclaw@db-layer`, conformément aux documents existants.
- Il peut être arrêté au moment courant, ou simplement invisible depuis les commandes lancées sous `ghost` sans inspection complète.
- Le double state dir `/home/ghost/.openclaw` peut expliquer la divergence entre CLI détecté sous `ghost` et runtime documentaire sous `openclaw`.

## 15_REMAINING_GAP

- Vérifier si l'utilisateur `openclaw` existe toujours.
- Vérifier les process OpenClaw appartenant à `openclaw`.
- Vérifier `systemd --user` pour l'utilisateur `openclaw`.
- Vérifier le socket `127.0.0.1:18789` sous le contexte runtime réel.
- Vérifier les logs sous `/home/openclaw/.openclaw`.
- Vérifier la version runtime réelle actuelle, car la doc mentionne `2026.4.2` alors que la CLI sous `ghost` montre `2026.3.11`.

## 16_TODO

Exécuter une deuxième passe read-only, ciblée utilisateur canonique :

```bash
set -Eeuo pipefail
trap 'echo "FAIL at line $LINENO: $BASH_COMMAND" >&2' ERR

OUT="$HOME/openclaw_db_layer_runtime_recross_$(date +%Y%m%d_%H%M%S).txt"
{
  echo "# OPENCLAW DB-LAYER RECROSS - CANONICAL USER"
  echo "timestamp=$(date -Is)"
  echo

  echo "## USERS"
  getent passwd openclaw || true
  id openclaw 2>/dev/null || true
  echo

  echo "## PROCESS CHECK ALL USERS"
  ps -ef | grep -i '[o]penclaw' || true
  ps -ef | grep -i '[n]ode' || true
  echo

  echo "## PORT CHECK"
  ss -ltnp 2>/dev/null | grep -E '18789|node|openclaw' || true
  echo

  echo "## OPENCLAW HOME PATHS"
  sudo -n ls -lah /home/openclaw 2>/dev/null || ls -lah /home/openclaw 2>/dev/null || true
  sudo -n find /home/openclaw/.openclaw -maxdepth 3 -type f 2>/dev/null | sed -n '1,120p' || true
  echo

  echo "## CONFIG PATHS ONLY"
  sudo -n find /home/openclaw/.openclaw -maxdepth 3 \( -name '*config*' -o -name 'openclaw.json' \) 2>/dev/null | sed -n '1,80p' || true
  echo

  echo "## LOG PATHS"
  sudo -n find /home/openclaw/.openclaw /tmp -maxdepth 4 -iname '*openclaw*' -type f 2>/dev/null | sed -n '1,120p' || true
  echo

  echo "## SYSTEMD USER OPENCLAW - IF AVAILABLE"
  sudo -n -u openclaw XDG_RUNTIME_DIR=/run/user/$(id -u openclaw 2>/dev/null) systemctl --user list-units --type=service 2>/dev/null | grep -i openclaw || true
  echo

  echo "## LOOPBACK PROBE"
  timeout 3 bash -lc 'cat < /dev/null > /dev/tcp/127.0.0.1/18789' >/dev/null 2>&1 && echo 'port_18789_tcp=OPEN' || echo 'port_18789_tcp=CLOSED'
  echo

  echo "## VERDICT PLACEHOLDER"
  echo "runtime_recross_status=TO_CLASSIFY"
} | tee "$OUT"

echo "AUDIT_FILE=$OUT"
```

## 17_RESUME_POINT

Le premier audit ne contredit pas la doc existante : il a été exécuté sous `ghost`, alors que la doc canonique référence `openclaw@db-layer`.

Prochaine action : audit read-only ciblé sur `openclaw@db-layer`, puis reclassement définitif du runtime.
