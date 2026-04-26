---
doc_id: GO_OPENCLAW_RUNTIME_AUDIT_OPENCLAW_USER_RESULT_20260426
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
  - runtime_audit
  - openclaw_user
  - state_dir
  - gateway
  - port_18789
  - stopped_runtime
search_tags:
  - surface:chantier
  - doc_role:runtime_audit_result
  - parent:GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01
  - audit:db_layer
  - user:openclaw
  - verdict:runtime_state_present_gateway_stopped
reference_canonique_principale: docs/chantiers/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01/07_RUNTIME_AUDIT_RECROSS_WITH_EXISTING_DOCS.md
point_de_reprise: "17_RESUME_POINT"
links:
  - docs/chantiers/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01/07_RUNTIME_AUDIT_RECROSS_WITH_EXISTING_DOCS.md
  - modules/evidence_openclaw/docs/GO_OPENCLAW_SYNC_02.md
  - modules/menu_openclaw/docs/GO_OPENCLAW_INFRA_BASELINE_01.md
---

# 08_RUNTIME_AUDIT_OPENCLAW_USER_RESULT_20260426

## 1_MASTER_TARGET

Documenter la seconde passe d'audit ciblée sur l'utilisateur canonique `openclaw@db-layer`.

## 7_CANONICAL_STATE

Audit exécuté depuis `ghost@db-layer` avec inspection explicite de l'utilisateur `openclaw`.

Résultat :

```text
openclaw:x:1001:1001::/home/openclaw:/bin/bash
uid=1001(openclaw) gid=1001(openclaw) groupes=1001(openclaw),125(docker)
```

Le dossier home et le state dir existent :

```text
/home/openclaw
/home/openclaw/.openclaw
```

Aucun process OpenClaw actif détecté au moment de la capture :

```text
ps -ef | grep -i openclaw
# résultat utile : seulement le grep lancé par ghost
```

Aucun port `18789` actif détecté au moment de la capture :

```text
ss -ltnp | grep 18789 || true
# aucun résultat
```

## 13_ESTABLISHED

### Établi positif

- L'utilisateur canonique `openclaw` existe.
- L'utilisateur `openclaw` appartient au groupe `docker`.
- Le home `/home/openclaw` existe.
- Le state dir `/home/openclaw/.openclaw` existe.
- Les artefacts historiques OpenClaw existent sous `/home/openclaw`.
- La documentation antérieure mentionnant `openclaw@db-layer` n'est pas inventée.

### Établi négatif courant

- Aucun Gateway actif visible maintenant.
- Aucun process OpenClaw actif visible maintenant.
- Aucun port `18789` en écoute maintenant.
- Le runtime documenté historiquement n'est pas prouvé actif au moment de l'audit.

## CORRECTION FINALE DU VERDICT

La documentation existante établit une preuve historique de Gateway loopback `OK`.

L'audit machine actuel établit que le runtime courant n'est pas actif ou pas visible au moment de la passe.

Verdict :

```text
RUNTIME_STATE_PRESENT_GATEWAY_STOPPED_OR_INACTIVE
```

## 14_HYPOTHESIS

- Le Gateway a probablement déjà été configuré puis arrêté.
- Le daemon n'est pas lancé actuellement ou pas installé comme service actif.
- La divergence de version entre `ghost` CLI et doc historique reste à vérifier.
- Le prochain pas doit être un diagnostic `doctor/gateway/onboard` sous utilisateur `openclaw`, sans mutation automatique.

## 15_REMAINING_GAP

- Version CLI sous `openclaw`.
- Sortie `openclaw doctor` sous `openclaw`.
- Sortie `openclaw gateway status` sous `openclaw`.
- État systemd user de `openclaw`.
- Chemins logs actifs.
- Fichier config actif sans exposition de secrets.
- Méthode de démarrage contrôlée du Gateway.

## 16_TODO

Prochaine commande read-only :

```bash
set -Eeuo pipefail
trap 'echo "FAIL at line $LINENO: $BASH_COMMAND" >&2' ERR

sudo -u openclaw -H bash -lc 'whoami; pwd; command -v openclaw; openclaw --version; openclaw doctor 2>&1 | sed -n "1,160p"; openclaw gateway status 2>&1 | sed -n "1,120p"; openclaw onboard --help 2>&1 | sed -n "1,80p"'
```

Si la commande échoue par environnement PATH, vérifier :

```bash
sudo -u openclaw -H bash -lc 'echo $PATH; ls -lah ~/.npm-global/bin; ls -lah ~/.openclaw | sed -n "1,80p"'
```

## 17_RESUME_POINT

```text
Le bon utilisateur openclaw existe.
Le state dir canonique existe.
Le Gateway documenté historiquement n'est pas actif maintenant.
Next : diagnostic OpenClaw CLI/doctor/gateway sous sudo -u openclaw -H.
Bridge reste bloqué jusqu'à Gateway actif et audité.
```

## 18_TO_DOCUMENT

- `OPENCLAW_USER_EXISTS_STATE_DIR_EXISTS_20260426`
- `OPENCLAW_GATEWAY_HISTORICAL_OK_CURRENTLY_INACTIVE_01`
- `OPENCLAW_NEXT_DOCTOR_UNDER_CANONICAL_USER_01`

## 19_TO_REMEMBER

- `openclaw@db-layer` existe avec state dir canonique, mais le Gateway n'était pas actif au moment de l'audit du 2026-04-26.
