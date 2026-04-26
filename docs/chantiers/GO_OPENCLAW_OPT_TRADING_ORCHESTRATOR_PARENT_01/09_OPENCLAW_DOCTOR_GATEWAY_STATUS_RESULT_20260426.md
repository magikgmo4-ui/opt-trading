---
doc_id: GO_OPENCLAW_DOCTOR_GATEWAY_STATUS_RESULT_20260426
doc_type: runtime_audit_result
repo: opt-trading
project: opt-trading
module: openclaw_operator_bridge
go_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_AUDIT_RUNTIME_01
parent_go_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01
status: result
lifecycle_stage: audit_result
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-04-26
topic_keys:
  - openclaw
  - db-layer
  - doctor
  - gateway_status
  - systemd_user
  - loopback
  - service_config
  - foreground_gateway
search_tags:
  - surface:chantier
  - doc_role:runtime_audit_result
  - parent:GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01
  - audit:doctor_gateway_status
  - verdict:gateway_configured_not_running
reference_canonique_principale: docs/chantiers/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01/08_RUNTIME_AUDIT_OPENCLAW_USER_RESULT_20260426.md
point_de_reprise: "17_RESUME_POINT"
links:
  - docs/chantiers/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01/08_RUNTIME_AUDIT_OPENCLAW_USER_RESULT_20260426.md
  - docs/chantiers/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01/04_OPERATOR_BRIDGE_SPEC.md
---

# 09_OPENCLAW_DOCTOR_GATEWAY_STATUS_RESULT_20260426

## 1_MASTER_TARGET

Documenter la sortie réelle de `openclaw doctor` et `openclaw gateway status` exécutés sous l'utilisateur canonique `openclaw@db-layer`.

## 7_CANONICAL_STATE

Commande exécutée :

```bash
sudo -u openclaw -H bash -lc '
whoami
command -v openclaw
openclaw --version
openclaw doctor
openclaw gateway status
'
```

Résultat établi :

```text
user=openclaw
openclaw_path=/usr/local/bin/openclaw
version=OpenClaw 2026.3.11 (29dc654)
config=/home/openclaw/.openclaw/openclaw.json
gateway_target=ws://127.0.0.1:18789
bind=loopback
port=18789
dashboard=http://127.0.0.1:18789/
logs=/tmp/openclaw-1001/openclaw-2026-04-26.log
systemd_service=disabled
runtime=unknown
gateway=not_running
rpc_probe=failed
```

## 13_ESTABLISHED

### Positif

- Le contexte utilisateur canonique `openclaw` est valide.
- CLI OpenClaw disponible via `/usr/local/bin/openclaw`.
- Version CLI/runtime observée : `2026.3.11 (29dc654)`.
- Config active : `/home/openclaw/.openclaw/openclaw.json`.
- Gateway configuré en loopback.
- Port configuré : `18789`.
- Dashboard attendu : `http://127.0.0.1:18789/`.
- Logs attendus : `/tmp/openclaw-1001/openclaw-2026-04-26.log`.
- Aucun warning de sécurité channel détecté par doctor.
- Skills : `Eligible: 12`, `Missing requirements: 41`, `Blocked by allowlist: 0`.
- Plugins : `Loaded: 4`, `Disabled: 34`, `Errors: 0`.

### Négatif / bloquant

- Gateway non lancé.
- RPC probe échoué.
- Service systemd user désactivé / indisponible.
- `systemctl --user` indisponible avec erreur bus/permission.
- Service config signalée comme non standard ou obsolète.
- Service Gateway PATH non défini.
- Multiple state directories détectés : `/home/ghost/.openclaw` et active state dir `~/.openclaw` sous `openclaw`.

## VERDICT

```text
GATEWAY_CONFIGURED_NOT_RUNNING_SYSTEMD_USER_BLOCKER
```

Interprétation :

- Le Gateway existe et est configuré.
- Le Gateway n'est pas actif maintenant.
- Le blocage principal n'est pas la configuration réseau, mais le mode de supervision/runtime.
- La solution doit choisir entre :
  - réparer/activer systemd user ;
  - lancer Gateway en foreground sous superviseur contrôlé ;
  - créer un wrapper tmux/supervisor dédié ;
  - ne pas utiliser le bridge tant que le Gateway n'est pas stable.

## 14_HYPOTHESIS

- Le runtime historique a probablement fonctionné en foreground ou sous un autre superviseur.
- Le service systemd user n'est pas fiable dans l'environnement actuel.
- Le lancement foreground contrôlé peut être le plus petit prochain pas pour valider le Gateway.
- Une réparation automatique `doctor --fix` ou `doctor --repair` doit rester interdite tant qu'un GO fix n'est pas ouvert.

## 15_REMAINING_GAP

- Lire `/tmp/openclaw-1001/openclaw-2026-04-26.log`.
- Vérifier `openclaw status`.
- Vérifier l'aide exacte pour lancer Gateway foreground.
- Déterminer si tmux est le superviseur préférable.
- Déterminer si systemd user peut être réparé proprement.
- Confirmer si `doctor --fix` modifie uniquement state/config/service ou plus largement.

## 16_TODO

### Passe lecture-only suivante

```bash
set -Eeuo pipefail
trap 'echo "FAIL at line $LINENO: $BASH_COMMAND" >&2' ERR

sudo -u openclaw -H bash -lc '
openclaw status 2>&1 | sed -n "1,160p"
echo "--- gateway help"
openclaw gateway --help 2>&1 | sed -n "1,160p"
echo "--- log tail"
tail -160 /tmp/openclaw-1001/openclaw-2026-04-26.log 2>/dev/null || true
'
```

### GO suivant probable

```text
GO_OPENCLAW_OPT_TRADING_CHILD_GATEWAY_SUPERVISION_FIX_01
```

Objectif : décider et documenter le mode stable de supervision Gateway : systemd user, tmux foreground, ou autre superviseur.

## 17_RESUME_POINT

```text
OpenClaw est installé et configuré sous openclaw@db-layer.
Gateway cible: ws://127.0.0.1:18789.
Bind: loopback.
Gateway non lancé.
Blocage: systemd user unavailable / service config issue.
Bridge reste bloqué.
Next: lecture logs + openclaw status + gateway help, puis GO supervision fix.
```

## 18_TO_DOCUMENT

- `OPENCLAW_GATEWAY_CONFIGURED_NOT_RUNNING_20260426`
- `OPENCLAW_SYSTEMD_USER_BLOCKER_01`
- `OPENCLAW_GATEWAY_SUPERVISION_FIX_NEXT_01`

## 19_TO_REMEMBER

- OpenClaw sur `db-layer` est configuré en loopback mais non lancé ; le blocage courant est la supervision du Gateway, pas l'existence du Gateway.
