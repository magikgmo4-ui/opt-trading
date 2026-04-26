---
doc_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_AUDIT_RUNTIME_01
doc_type: runtime_audit_protocol
repo: opt-trading
project: opt-trading
module: openclaw_operator_bridge
go_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_AUDIT_RUNTIME_01
parent_go_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01
status: open
lifecycle_stage: audit
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-04-26
topic_keys:
  - openclaw
  - db-layer
  - runtime_audit
  - gateway
  - node
  - auth
  - logs
  - network
  - docker
  - systemd
search_tags:
  - surface:chantier
  - doc_role:runtime_audit_protocol
  - parent:GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01
  - audit:db_layer
  - runtime:openclaw
reference_canonique_principale: docs/chantiers/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01/00_INITIAL_PROJECT_DOC.md
point_de_reprise: "17_RESUME_POINT"
links:
  - docs/chantiers/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01/00_INITIAL_PROJECT_DOC.md
  - docs/chantiers/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01/04_OPERATOR_BRIDGE_SPEC.md
---

# GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_AUDIT_RUNTIME_01

## 1_MASTER_TARGET

Auditer l'état réel OpenClaw sur `db-layer` avant toute implémentation du bridge.

## 3_INITIAL_NEED

Le bridge est spécifié mais ne doit pas être implémenté avant vérification runtime : installation, version, gateway, ports, logs, auth, daemon, Docker, réseau et exposition.

## 6_FINAL_TARGET

Produire une preuve d'audit locale permettant de décider :

- `PASS_RUNTIME_READY`
- `PASS_WITH_FIXES_REQUIRED`
- `FAIL_RUNTIME_UNKNOWN`
- `FAIL_SECURITY_BLOCKER`

## 7_CANONICAL_STATE

- Parent OpenClaw ouvert.
- Bridge spec créée.
- Audit réel `db-layer` requis avant implémentation.
- Aucun changement runtime autorisé par ce GO sauf lecture et diagnostic.

## 8_VALIDATED_PLAN

1. Vérifier host et OS.
2. Vérifier présence CLI OpenClaw.
3. Vérifier process Gateway.
4. Vérifier ports ouverts.
5. Vérifier services systemd user/system.
6. Vérifier logs connus.
7. Vérifier Docker et permissions.
8. Vérifier réseau et bind address.
9. Vérifier présence config/auth sans afficher secrets.
10. Produire rapport texte.

## 12_INVARIANTS

- Lecture seule.
- Ne pas afficher de secrets.
- Ne pas ouvrir de port.
- Ne pas modifier systemd.
- Ne pas installer ou réparer automatiquement.
- Ne pas lancer bridge.
- Ne pas toucher trading live.

## 16_TODO — Script audit paste-safe

```bash
set -Eeuo pipefail
trap 'echo "FAIL at line $LINENO: $BASH_COMMAND" >&2' ERR

OUT="$HOME/openclaw_db_layer_audit_$(date +%Y%m%d_%H%M%S).txt"
{
  echo "# OPENCLAW DB-LAYER RUNTIME AUDIT"
  echo "timestamp=$(date -Is)"
  echo

  echo "## HOST"
  hostnamectl 2>/dev/null || true
  uname -a
  id
  echo

  echo "## OPENCLAW CLI"
  command -v openclaw || true
  openclaw --version 2>/dev/null || true
  echo

  echo "## OPENCLAW COMMANDS HELP"
  openclaw --help 2>/dev/null | sed -n '1,80p' || true
  echo

  echo "## PROCESSES"
  ps -ef | grep -i '[o]penclaw' || true
  ps -ef | grep -i '[n]ode' || true
  echo

  echo "## PORTS 18789 / NODE / LISTEN"
  ss -ltnp 2>/dev/null | grep -E '18789|node|openclaw' || true
  echo

  echo "## SYSTEMD USER"
  systemctl --user list-units --type=service 2>/dev/null | grep -i openclaw || true
  systemctl --user status openclaw 2>/dev/null | sed -n '1,120p' || true
  echo

  echo "## SYSTEMD SYSTEM"
  systemctl list-units --type=service 2>/dev/null | grep -i openclaw || true
  systemctl status openclaw 2>/dev/null | sed -n '1,120p' || true
  echo

  echo "## LOG CANDIDATES"
  ls -lah /tmp/openclaw-* 2>/dev/null || true
  find /tmp -maxdepth 3 -iname '*openclaw*' -type f 2>/dev/null | head -50 || true
  echo

  echo "## RECENT LOG TAILS (SANITIZED REVIEW REQUIRED)"
  for f in $(find /tmp -maxdepth 3 -iname '*openclaw*' -type f 2>/dev/null | head -5); do
    echo "--- $f"
    tail -80 "$f" 2>/dev/null || true
  done
  echo

  echo "## DOCKER"
  command -v docker || true
  docker --version 2>/dev/null || true
  docker ps 2>/dev/null || true
  groups
  ls -l /var/run/docker.sock 2>/dev/null || true
  echo

  echo "## NETWORK SUMMARY"
  ip -br addr 2>/dev/null || true
  ip route 2>/dev/null || true
  echo

  echo "## CONFIG CANDIDATES - PATHS ONLY"
  find "$HOME" -maxdepth 4 \( -iname '*openclaw*' -o -iname '.openclaw*' \) 2>/dev/null | sed -n '1,120p' || true
  echo

  echo "## VERDICT PLACEHOLDER"
  echo "runtime_status=TO_CLASSIFY"
} | tee "$OUT"

echo "AUDIT_FILE=$OUT"
```

## 17_RESUME_POINT

Exécuter le script sur `db-layer`, récupérer le rapport texte, puis classer le runtime avant de passer au mapping avancé ou à l'implémentation bridge.
